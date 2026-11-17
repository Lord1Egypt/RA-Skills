#!/usr/bin/env python3
"""Recommend a semantic layout type for a Diagram IR file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from diagram_ir_tools import recommend_layout
from validate_contracts import load_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend Diagram IR layout.")
    parser.add_argument("--diagram", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    recommendation = recommend_layout(load_json(args.diagram))
    payload = json.dumps(recommendation, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(f"diagram layout recommendation written: {args.output}")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
