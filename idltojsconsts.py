#!/usr/bin/env python2

# This software is licensed under the MIT License.
# Copyright (c) 2017 Volker Mische (http://vmx.cx/)

# Extract constants out of an IDL file into a valid JavaScript file.
# This is used for the B2G project to convert things from Gonk into
# libraries that don't have a dependency on Gecko, but just on
# Web technologies.

# This is using gecko/xpcom/idl-parser/xpidl/ for parsing the IDL file

# I'd like to thank https://github.com/azu/XPIDL-JSDOC/blob/master/jsdoc.py for
# making it way easier for me to figure out things.

import os
import sys


def extract_consts(gecko_dir, filenames):
    import xpidl

    # The directories where the base IDLs are
    idl_xpcom_base_dir = os.path.join(gecko_dir, 'xpcom', 'base')
    idl_dom_base_dir = os.path.join(gecko_dir, 'dom', 'interfaces', 'base')

    # By default also include the directories the given IDLs are in
    idl_dirs = [os.path.dirname(ff) for ff in filenames] + [
        idl_xpcom_base_dir, idl_dom_base_dir]

    p = xpidl.IDLParser()
    for f in filenames:
        idl = p.parse(open(f).read(), filename=f)
        idl.resolve(idl_dirs, p)
        for production in idl.productions:
            if production.kind == 'interface':
                # Print interfaces even if they don't have any const members,
                # as they might still be of use as empty containers to get
                # things working
                print("const {} = {{".format(production.name))
                for member in production.members:
                    if member.kind == 'const':
                        print("    {}: {},".format(member.name,
                                                   member.value(idl)))
                print("};")

def add_xpidl_import_path(gecko_dir):
    import_dir = os.path.join(gecko_dir, 'xpcom', 'idl-parser', 'xpidl')
    sys.path.append(import_dir)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        print("Usage: {} <path-to-gecko-src> <IDL-file>...".format(argv[0]))
        return 2

    gecko_dir = argv[1]
    idl_files = argv[2:]

    add_xpidl_import_path(gecko_dir)
    extract_consts(gecko_dir, idl_files)


if __name__ == '__main__':
    sys.exit(main())
