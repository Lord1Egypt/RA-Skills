#!/usr/bin/env python3
"""Chown Tool - Change ownership."""
import argparse, os, sys
parser = argparse.ArgumentParser()
parser.add_argument('owner')
parser.add_argument('file')
args = parser.parse_args()
try:
    import pwd, grp
    u, g = args.owner.split(':') if ':' in args.owner else (args.owner, None)
    uid = pwd.getpwnam(u).pw_uid
    gid = grp.getgrnam(g).gr_gid if g else -1
    os.chown(args.file, uid, gid)
    print(f"Changed: {args.file}")
except Exception as e: print(f"Error: {e}", file=sys.stderr)
