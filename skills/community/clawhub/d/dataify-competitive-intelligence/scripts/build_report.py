#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from research_outputs import build_report

parser = argparse.ArgumentParser(description="Build Markdown and JSON reports with validated evidence links.")
parser.add_argument("run", type=Path)
parser.add_argument("--findings-json", type=Path)
args = parser.parse_args()
state = args.run if args.run.name == "state.json" else args.run / "state.json"
markdown, structured = build_report(state, args.findings_json)
print(json.dumps({"markdown": str(markdown), "json": str(structured)}, indent=2))
