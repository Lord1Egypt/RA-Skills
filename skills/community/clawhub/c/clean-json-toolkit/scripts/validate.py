#!/usr/bin/env python3
"""
validate.py - Check a JSON / JSONL file against a small, pragmatic schema.
NOT a full JSON Schema implementation; targeted at the 90% of validation
checks an agent actually needs.

Schema format (a JSON file):
    {
      "required": ["name", "email"],
      "fields": {
        "name":   {"type": "string", "min_length": 1},
        "email":  {"type": "string", "regex": "^[^@]+@[^@]+\\.[^@]+$"},
        "age":    {"type": "int", "min": 0, "max": 130},
        "tags":   {"type": "array", "item_type": "string"},
        "role":   {"type": "string", "enum": ["admin", "user", "guest"]}
      },
      "allow_extra": true
    }

Supported field rules:
    type           string | int | float | bool | null | array | object | any
    required       boolean (alternative to top-level "required" list)
    min / max      numeric bounds (works for int / float)
    min_length / max_length   string or array length bounds
    enum           list of allowed exact values
    regex          for strings: re.search match
    item_type      for arrays: type of every element

Top-level:
    required       array of field names that must exist and be non-null
    fields         per-field rules
    allow_extra    if false, unknown fields cause an error (default: true)

Usage:
    validate.py INPUT --schema SCHEMA.json [--strict] [--max-errors N] [--json]

Options:
    --schema PATH       schema file (required)
    --strict            stop at the first error (default: collect all)
    --max-errors N      cap the error list at N (default: 100)
    --json              emit a machine-readable report on stdout
    --quiet             suppress text summary on stderr
    -h, --help          show this help

Exit codes:
    0  validation passed (all rows OK)
    1  one or more errors found
    2  bad arguments / unsafe path / missing file / invalid JSON / bad schema
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from _common import load_json, safe_path, type_of


TYPE_PY = {
    "string": str, "int": int, "float": (int, float), "bool": bool,
    "null": type(None), "array": list, "object": dict, "any": object,
}


def _validate_value(value: Any, rules: Dict[str, Any], path: str,
                    errors: List[Dict[str, str]]) -> None:
    t = rules.get("type")
    if t == "int" and isinstance(value, bool):
        errors.append({"path": path, "code": "bad_type", "expected": "int",
                       "got": "bool", "value": str(value)})
        return
    if t and t != "any":
        py_type = TYPE_PY.get(t)
        if py_type is None:
            errors.append({"path": path, "code": "schema_error",
                           "msg": f"unknown type {t!r}"})
            return
        if not isinstance(value, py_type):
            errors.append({"path": path, "code": "bad_type", "expected": t,
                           "got": type_of(value), "value": str(value)[:60]})
            return

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "min" in rules and value < rules["min"]:
            errors.append({"path": path, "code": "below_min", "value": str(value),
                           "min": str(rules["min"])})
        if "max" in rules and value > rules["max"]:
            errors.append({"path": path, "code": "above_max", "value": str(value),
                           "max": str(rules["max"])})

    if isinstance(value, (str, list)):
        if "min_length" in rules and len(value) < rules["min_length"]:
            errors.append({"path": path, "code": "below_min_length",
                           "len": str(len(value)),
                           "min_length": str(rules["min_length"])})
        if "max_length" in rules and len(value) > rules["max_length"]:
            errors.append({"path": path, "code": "above_max_length",
                           "len": str(len(value)),
                           "max_length": str(rules["max_length"])})

    if "enum" in rules and value not in rules["enum"]:
        errors.append({"path": path, "code": "not_in_enum",
                       "value": str(value)[:60],
                       "enum": ",".join(str(e) for e in rules["enum"])})

    if "regex" in rules and isinstance(value, str):
        if not re.search(rules["regex"], value):
            errors.append({"path": path, "code": "regex_mismatch",
                           "value": value[:60], "regex": rules["regex"]})

    if isinstance(value, list) and "item_type" in rules:
        it = rules["item_type"]
        py_type = TYPE_PY.get(it)
        if py_type is None:
            errors.append({"path": path, "code": "schema_error",
                           "msg": f"unknown item_type {it!r}"})
        else:
            for i, item in enumerate(value):
                if not isinstance(item, py_type):
                    errors.append({"path": f"{path}[{i}]", "code": "bad_item_type",
                                   "expected": it, "got": type_of(item),
                                   "value": str(item)[:60]})


def validate_one(obj: Any, schema: Dict[str, Any], prefix: str,
                 errors: List[Dict[str, str]], max_errors: int,
                 strict: bool) -> bool:
    required = schema.get("required", []) or []
    fields = schema.get("fields", {}) or {}
    allow_extra = schema.get("allow_extra", True)

    if not isinstance(obj, dict):
        errors.append({"path": prefix or "$", "code": "bad_type",
                       "expected": "object", "got": type_of(obj)})
        return False

    for r in required:
        if r not in obj or obj[r] is None:
            errors.append({"path": f"{prefix}.{r}" if prefix else r,
                           "code": "missing_required"})
            if strict:
                return False
            if len(errors) >= max_errors:
                return False

    for name, rules in fields.items():
        if name not in obj:
            if rules.get("required"):
                errors.append({"path": f"{prefix}.{name}" if prefix else name,
                               "code": "missing_required"})
                if strict:
                    return False
            continue
        _validate_value(obj[name], rules, f"{prefix}.{name}" if prefix else name,
                        errors)
        if strict and errors:
            return False
        if len(errors) >= max_errors:
            return False

    if not allow_extra:
        known = set(fields.keys())
        for k in obj:
            if k not in known and k not in required:
                errors.append({"path": f"{prefix}.{k}" if prefix else k,
                               "code": "unexpected_field"})
                if strict:
                    return False

    return True


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--schema")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--max-errors", dest="max_errors", type=int, default=100)
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input:
        print(__doc__)
        return 0 if args.help else 2
    if not args.schema:
        print("Error: --schema PATH is required", file=sys.stderr)
        return 2

    try:
        in_path = safe_path(args.input)
        sc_path = safe_path(args.schema)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2
    if not sc_path.is_file():
        print(f"Error: schema not a file: {sc_path}", file=sys.stderr)
        return 2

    try:
        schema = json.loads(sc_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: schema is not valid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(schema, dict):
        print("Error: schema must be a top-level JSON object", file=sys.stderr)
        return 2

    try:
        data, kind = load_json(in_path)
    except json.JSONDecodeError as e:
        print(f"Error: input is not valid JSON: {e}", file=sys.stderr)
        return 2

    errors: List[Dict[str, str]] = []
    n_objects = 0

    if kind == "jsonl":
        for i, obj in enumerate(data):
            n_objects += 1
            validate_one(obj, schema, f"[{i}]", errors,
                         args.max_errors, args.strict)
            if args.strict and errors:
                break
            if len(errors) >= args.max_errors:
                break
    elif isinstance(data, list):
        for i, obj in enumerate(data):
            n_objects += 1
            validate_one(obj, schema, f"[{i}]", errors,
                         args.max_errors, args.strict)
            if args.strict and errors:
                break
            if len(errors) >= args.max_errors:
                break
    else:
        n_objects = 1
        validate_one(data, schema, "", errors, args.max_errors, args.strict)

    summary = {
        "input": str(in_path),
        "schema": str(sc_path),
        "objects_checked": n_objects,
        "errors": errors,
        "n_errors": len(errors),
        "verdict": "pass" if not errors else "fail",
    }

    if args.as_json:
        print(json.dumps(summary, indent=2))
    elif not args.quiet:
        if not errors:
            print(f"validate: PASS ({n_objects} object(s) OK against {sc_path})")
        else:
            print(f"validate: FAIL ({n_objects} checked, {len(errors)} error(s))")
            for e in errors[:20]:
                parts = [f"{k}={v}" for k, v in e.items() if k != "path"]
                print(f"  {e.get('path','?'):<40s} {' '.join(parts)}")
            if len(errors) > 20:
                print(f"  ... and {len(errors)-20} more")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
