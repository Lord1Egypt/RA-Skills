#!/usr/bin/env python3
"""Cat Tool - Display files."""
import argparse, sys
parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*', default=['-'])
args = parser.parse_args()
for f in args.files:
    try:
        print(open(f).read(), end='')
    except: print(f"Error reading: {f}", file=sys.stderr)
