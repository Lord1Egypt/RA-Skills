#!/usr/bin/env python3
"""
Validate a CSV / TSV / JSONL file against a small schema written in JSON.

Schema format:

  {
    "required_columns": ["id", "email", "amount"],
    "columns": {
      "id":     {"type": "int", "required": true, "unique": true},
      "email":  {"type": "string", "required": true, "regex": ".+@.+\\\\..+"},
      "amount": {"type": "float", "min": 0, "max": 100000},
      "status": {"type": "string", "enum": ["pending", "approved", "rejected"]}
    }
  }

Each column constraint is optional. `type` is one of:
  int | float | bool | date | datetime | string

Usage:
  python3 validate.py <input> --schema schema.json
  python3 validate.py <input> --schema schema.json --json
  python3 validate.py <input> --schema schema.json --max-errors 100

Exit codes:
  0 = file passed validation
  1 = file failed validation (at least one rule violated)
  2 = bad arguments / missing input / unsafe path / schema malformed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _common import (
    safe_path,
    open_table,
    print_error,
)


def _coerce(value: str, expected_type: str):
    """Try to coerce a string to expected_type. Returns (ok, coerced_or_none)."""
    if value is None or str(value).strip() == "":
        return True, None
    s = str(value).strip()
    if expected_type == "int":
        try:
            return True, int(s)
        except ValueError:
            return False, None
    if expected_type == "float":
        try:
            return True, float(s)
        except ValueError:
            return False, None
    if expected_type == "bool":
        if s.lower() in {"true", "yes", "y", "1", "t"}:
            return True, True
        if s.lower() in {"false", "no", "n", "0", "f"}:
            return True, False
        return False, None
    if expected_type == "date":
        from datetime import datetime
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return True, datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return False, None
    if expected_type == "datetime":
        from datetime import datetime
        for fmt in (
            "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M",
        ):
            try:
                return True, datetime.strptime(s, fmt)
            except ValueError:
                continue
        return False, None
    # string: anything non-empty is fine
    return True, s


def load_schema(schema_path: Path) -> Dict:
    try:
        data = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"schema is not valid JSON: {e}") from e
    if not isinstance(data, dict):
        raise ValueError("schema must be a JSON object")
    columns = data.get("columns", {})
    if not isinstance(columns, dict):
        raise ValueError("schema.columns must be an object")
    return data


def validate(path: Path, schema: Dict, max_errors: int) -> Dict:
    required_columns = schema.get("required_columns") or []
    col_rules = schema.get("columns") or {}

    # Pre-compile regexes
    compiled: Dict[str, re.Pattern] = {}
    for cname, rules in col_rules.items():
        if "regex" in rules:
            try:
                compiled[cname] = re.compile(rules["regex"])
            except re.error as e:
                raise ValueError(f"column {cname!r} has invalid regex: {e}") from e

    errors: List[Dict] = []
    row_count = 0
    seen_unique: Dict[str, set] = {
        c: set() for c, r in col_rules.items() if r.get("unique")
    }

    def add_error(row_idx: int, col: str, kind: str, detail: str, value=None):
        if len(errors) >= max_errors:
            return
        entry = {"row": row_idx, "column": col, "kind": kind, "detail": detail}
        if value is not None:
            entry["value"] = value
        errors.append(entry)

    with open_table(path) as (kind, headers, rows):
        # Missing required columns
        missing = [c for c in required_columns if c not in headers]
        for c in missing:
            add_error(0, c, "missing_column", f"required column not found in header")

        for row_idx, row in enumerate(rows, start=1):
            row_count += 1
            for cname, rules in col_rules.items():
                if cname not in headers:
                    continue
                raw = row.get(cname, "")
                value = (raw or "").strip()

                if rules.get("required") and value == "":
                    add_error(row_idx, cname, "null_in_required", "value is empty/null")
                    continue

                if value == "":
                    continue  # blank value, no other checks apply

                # Type check
                expected_type = rules.get("type")
                coerced = None
                if expected_type:
                    ok, coerced = _coerce(value, expected_type)
                    if not ok:
                        add_error(row_idx, cname, "bad_type",
                                  f"value does not match type {expected_type!r}",
                                  value=value)
                        continue

                # min / max (numeric)
                if expected_type in ("int", "float") and coerced is not None:
                    if "min" in rules and coerced < rules["min"]:
                        add_error(row_idx, cname, "below_min",
                                  f"value {coerced} < min {rules['min']}",
                                  value=value)
                    if "max" in rules and coerced > rules["max"]:
                        add_error(row_idx, cname, "above_max",
                                  f"value {coerced} > max {rules['max']}",
                                  value=value)

                # Enum
                if "enum" in rules:
                    allowed = set(str(x) for x in rules["enum"])
                    if value not in allowed:
                        add_error(row_idx, cname, "not_in_enum",
                                  f"value not in allowed set",
                                  value=value)

                # Regex
                if cname in compiled and not compiled[cname].search(value):
                    add_error(row_idx, cname, "regex_mismatch",
                              "value did not match regex",
                              value=value)

                # Unique
                if rules.get("unique"):
                    if value in seen_unique[cname]:
                        add_error(row_idx, cname, "duplicate_unique",
                                  "value already seen earlier in this column",
                                  value=value)
                    else:
                        seen_unique[cname].add(value)

    return {
        "path": str(path),
        "row_count": row_count,
        "error_count": len(errors),
        "errors_truncated": len(errors) >= max_errors,
        "errors": errors,
        "verdict": "pass" if not errors else "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[1])
    parser.add_argument("input", help="Path to a .csv / .tsv / .jsonl file")
    parser.add_argument("--schema", required=True, help="Path to JSON schema")
    parser.add_argument("--json", action="store_true", help="Emit JSON report to stdout")
    parser.add_argument("--max-errors", type=int, default=200,
                        help="Stop collecting after this many errors (default 200)")
    args = parser.parse_args()

    try:
        path = safe_path(args.input).resolve()
        schema_path = safe_path(args.schema).resolve()
    except ValueError as e:
        print_error(str(e))
        return 2
    if not path.is_file():
        print_error(f"input not a file: {path}")
        return 2
    if not schema_path.is_file():
        print_error(f"schema not found: {schema_path}")
        return 2
    if args.max_errors < 1:
        print_error("--max-errors must be >= 1")
        return 2

    try:
        schema = load_schema(schema_path)
    except ValueError as e:
        print_error(str(e))
        return 2

    try:
        report = validate(path, schema, max_errors=args.max_errors)
    except ValueError as e:
        print_error(str(e))
        return 2
    except Exception as e:
        print_error(f"validation failed: {e.__class__.__name__}: {e}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"file:    {report['path']}")
        print(f"rows:    {report['row_count']}")
        print(f"errors:  {report['error_count']}"
              + (" (truncated)" if report['errors_truncated'] else ""))
        print(f"verdict: {report['verdict']}")
        if report["errors"]:
            print()
            print(f"{'row':>6}  {'column':<22}  {'kind':<22}  detail")
            print("-" * 96)
            for e in report["errors"][:50]:
                row = e["row"]
                col = e["column"] if len(e["column"]) <= 22 else e["column"][:19] + "..."
                kind = e["kind"]
                detail = e["detail"]
                if "value" in e:
                    detail = f"{detail} | value={e['value']!r}"
                if len(detail) > 60:
                    detail = detail[:57] + "..."
                print(f"{row:>6}  {col:<22}  {kind:<22}  {detail}")
            if len(report["errors"]) > 50:
                print(f"... ({len(report['errors']) - 50} more)")

    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
