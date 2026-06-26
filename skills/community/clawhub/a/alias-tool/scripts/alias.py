#!/usr/bin/env python3
"""Alias Tool - Command aliases."""
import argparse, os, json, sys
ALIAS_FILE = os.path.expanduser('~/.aliasrc')
parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='?', default=None)
parser.add_argument('cmd', nargs='?', default=None)
parser.add_argument('--list', '-l', action='store_true')
args = parser.parse_args()

aliases = {}
if os.path.exists(ALIAS_FILE):
    aliases = json.load(open(ALIAS_FILE))

if args.list:
    for k, v in aliases.items():
        print(f"alias {k}='{v}'")
elif args.name and args.cmd:
    aliases[args.name] = args.cmd
    json.dump(aliases, open(ALIAS_FILE, 'w'))
    print(f"Alias added: {args.name}='{args.cmd}'")
elif args.name:
    print(aliases.get(args.name, f"Alias not found: {args.name}"))
else:
    print("Usage: alias <name> [cmd] or alias --list")
