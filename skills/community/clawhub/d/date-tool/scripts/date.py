#!/usr/bin/env python3
"""Date Tool - Show date/time."""
import argparse, datetime
parser = argparse.ArgumentParser()
parser.add_argument('format', nargs='?', default='%Y-%m-%d %H:%M:%S')
args = parser.parse_args()
print(datetime.datetime.now().strftime(args.format))
