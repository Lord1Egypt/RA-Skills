#!/usr/bin/env python3
"""Env Tool - Environment variables."""
import argparse, os
parser = argparse.ArgumentParser()
parser.add_argument('var', nargs='?', default=None)
args = parser.parse_args()
if args.var:
    print(os.environ.get(args.var, ''))
else:
    for k, v in sorted(os.environ.items()):
        print(f"{k}={v}")
