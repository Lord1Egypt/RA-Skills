#!/usr/bin/env python3
"""Validate one Diagram IR file against schema and semantic rules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from diagram_ir_tools import validate_diagram_semantics
from validate_contracts import issue, load_json, validate_schema_subset


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Diagram IR contract.")
    parser.add_argument("--diagram", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parents[1] / "schemas" / "diagram-ir.schema.json")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json-output", action="store_true")
    args = parser.parse_args()

    try:
        diagram = load_json(args.diagram)
        schema = load_json(args.schema)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    errors = validate_schema_subset(diagram, schema, args.diagram, args.strict)
    errors.extend(validate_diagram_semantics(diagram, issue, args.diagram, "/"))

    if args.json_output:
        print(json.dumps({"ok": not errors, "issues": errors}, ensure_ascii=False, indent=2))
    elif errors:
        for item in errors:
            print(
                f"{item['file']} {item['pointer']} {item['code']}: "
                f"actual={item['actual_value']!r}; allowed={item['allowed_values']!r}; "
                f"repair={item['repair_suggestion']}",
                file=sys.stderr,
            )
    else:
        print("diagram validation passed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
