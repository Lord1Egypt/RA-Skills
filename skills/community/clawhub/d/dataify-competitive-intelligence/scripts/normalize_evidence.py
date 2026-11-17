#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from research_outputs import normalize

parser = argparse.ArgumentParser(description="Normalize successful competitive-intelligence actions into traceable evidence.")
parser.add_argument("run", type=Path)
args = parser.parse_args()
state = args.run if args.run.name == "state.json" else args.run / "state.json"
print(json.dumps(normalize(state), ensure_ascii=False, indent=2))
