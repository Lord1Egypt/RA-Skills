#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser(description="Update docs/cccc/state.json")
parser.add_argument("--state", default="docs/cccc/state.json")
parser.add_argument("--set", action="append", default=[], help="Set key=value at top level")
parser.add_argument("--append-risk", action="append", default=[])
args = parser.parse_args()

path = Path(args.state)
if not path.exists():
    raise SystemExit(f"Missing state file: {path}")

data = json.loads(path.read_text())

for item in args.set:
    if "=" not in item:
        raise SystemExit(f"Invalid --set value: {item}")
    key, value = item.split("=", 1)
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = value
    data[key] = parsed

if args.append_risk:
    data.setdefault("known_risks", [])
    data["known_risks"].extend(args.append_risk)

data["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
