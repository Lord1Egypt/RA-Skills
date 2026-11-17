#!/usr/bin/env python3
"""Normalize non-business Diagram IR defaults without changing relationships."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from diagram_ir_tools import normalize_diagram
from validate_contracts import load_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize Diagram IR defaults.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--style", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    normalized = normalize_diagram(load_json(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"normalized diagram written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
