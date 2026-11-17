#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from research_outputs import compare

parser = argparse.ArgumentParser(description="Compare two normalized competitive-intelligence evidence snapshots.")
parser.add_argument("old", type=Path)
parser.add_argument("new", type=Path)
parser.add_argument("--output", type=Path)
args = parser.parse_args()
changes = compare(args.old, args.new)
payload = json.dumps(changes, ensure_ascii=False, indent=2) + "\n"
if args.output:
    args.output.write_text(payload, encoding="utf-8")
print(payload, end="")
