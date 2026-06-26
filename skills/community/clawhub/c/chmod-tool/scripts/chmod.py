#!/usr/bin/env python3
"""Chmod Tool - Change permissions."""
import argparse, os, sys
parser = argparse.ArgumentParser()
parser.add_argument('mode')
parser.add_argument('file')
args = parser.parse_args()
try:
    os.chmod(args.file, int(args.mode, 8))
    print(f"Changed: {args.file}")
except Exception as e: print(f"Error: {e}", file=sys.stderr)
