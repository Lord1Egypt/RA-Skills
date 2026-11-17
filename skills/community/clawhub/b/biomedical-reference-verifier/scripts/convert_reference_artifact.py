#!/usr/bin/env python3
"""Convert verifier audit artifacts and reusable reference indexes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verifier_prior_results import INDEX_SCHEMA, audit_to_index, index_to_audit, write_json_atomic


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert reference-audit JSON and reference-index JSON in either direction.")
    parser.add_argument("input")
    parser.add_argument("--to", choices=["index", "audit"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read input artifact: {exc}")
    if not isinstance(payload, dict):
        raise SystemExit("Input must be a JSON object")
    warnings: list[str] = []
    converted = audit_to_index(payload, warnings) if args.to == "index" else index_to_audit(payload, warnings)
    output = Path(args.output)
    write_json_atomic(output, converted)
    print(f"Wrote {args.to} artifact: {args.output}")
    if args.to == "index":
        print(f"Schema: {INDEX_SCHEMA}; entries: {len(converted['entries'])}")
    for warning in warnings:
        print(f"Warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
