#!/usr/bin/env python3
"""Analyze Diagram IR complexity before layout/build."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from diagram_ir_tools import analyze_diagram
from validate_contracts import load_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Diagram IR complexity.")
    parser.add_argument("--diagram", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", action="store_true")
    args = parser.parse_args()

    analysis = analyze_diagram(load_json(args.diagram))
    payload = json.dumps(analysis, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    if args.json_output or not args.output:
        print(payload, end="")
    else:
        print(f"diagram analysis written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
