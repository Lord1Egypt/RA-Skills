#!/usr/bin/env python3
"""
Diff two CSV / TSV / JSONL files by one or more key columns.

For every key value present in either file the script classifies the row as:
  added     - present only in the new file
  removed   - present only in the old file
  changed   - present in both, but at least one non-key value differs
  unchanged - identical in both files (not printed unless --show-unchanged)

Usage:
  python3 diff.py <old> <new> --key id
  python3 diff.py <old> <new> --key customer_id,date
  python3 diff.py <old> <new> --key id --json --output diff.json
  python3 diff.py <old> <new> --key id --show-unchanged

Exit codes:
  0 = files are identical on the requested key(s)
  1 = files differ (at least one added/removed/changed)
  2 = bad arguments / missing input / unsafe path / key column missing
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _common import (
    safe_path,
    open_table,
    print_error,
)


def load_keyed(path: Path, key_columns: List[str]) -> Tuple[List[str], Dict[Tuple[str, ...], Dict[str, str]]]:
    """Return (headers, {key_tuple: row_dict}). Last occurrence wins."""
    with open_table(path) as (kind, headers, rows):
        if not headers:
            raise ValueError(f"{path}: input has no header row")
        missing = [c for c in key_columns if c not in headers]
        if missing:
            raise ValueError(f"{path}: key column(s) missing from header: {', '.join(missing)}")
        out: Dict[Tuple[str, ...], Dict[str, str]] = {}
        for row in rows:
            key = tuple((row.get(c) or "").strip() for c in key_columns)
            out[key] = dict(row)
        return list(headers), out


def diff(old_path: Path, new_path: Path, key_columns: List[str]) -> Dict:
    old_headers, old_rows = load_keyed(old_path, key_columns)
    new_headers, new_rows = load_keyed(new_path, key_columns)

    old_keys = set(old_rows.keys())
    new_keys = set(new_rows.keys())

    added_keys = sorted(new_keys - old_keys)
    removed_keys = sorted(old_keys - new_keys)
    common_keys = sorted(new_keys & old_keys)

    # All non-key columns to compare. Union of both headers.
    union_cols = []
    seen = set()
    for h in old_headers + new_headers:
        if h in key_columns:
            continue
        if h not in seen:
            seen.add(h)
            union_cols.append(h)

    changed: List[Dict] = []
    unchanged_count = 0

    for k in common_keys:
        old_row = old_rows[k]
        new_row = new_rows[k]
        diffs: Dict[str, Dict[str, str]] = {}
        for c in union_cols:
            old_v = (old_row.get(c) or "")
            new_v = (new_row.get(c) or "")
            if old_v != new_v:
                diffs[c] = {"old": old_v, "new": new_v}
        if diffs:
            changed.append({"key": list(k), "changes": diffs})
        else:
            unchanged_count += 1

    return {
        "old": str(old_path),
        "new": str(new_path),
        "key_columns": key_columns,
        "added_count": len(added_keys),
        "removed_count": len(removed_keys),
        "changed_count": len(changed),
        "unchanged_count": unchanged_count,
        "added": [{"key": list(k), "row": new_rows[k]} for k in added_keys],
        "removed": [{"key": list(k), "row": old_rows[k]} for k in removed_keys],
        "changed": changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[1])
    parser.add_argument("old", help="Path to the old file")
    parser.add_argument("new", help="Path to the new file")
    parser.add_argument("--key", required=True,
                        help="Comma-separated list of key columns")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout")
    parser.add_argument("--output", default="",
                        help="Optional file path for the full JSON report")
    parser.add_argument("--show-unchanged", action="store_true",
                        help="Include unchanged-row count in text output")
    parser.add_argument("--max-print", type=int, default=20,
                        help="Max rows per category to print in text mode (default 20)")
    args = parser.parse_args()

    try:
        old_path = safe_path(args.old).resolve()
        new_path = safe_path(args.new).resolve()
    except ValueError as e:
        print_error(str(e))
        return 2
    if not old_path.is_file():
        print_error(f"old not a file: {old_path}")
        return 2
    if not new_path.is_file():
        print_error(f"new not a file: {new_path}")
        return 2

    key_columns = [c.strip() for c in args.key.split(",") if c.strip()]
    if not key_columns:
        print_error("--key must contain at least one column name")
        return 2

    try:
        report = diff(old_path, new_path, key_columns)
    except ValueError as e:
        print_error(str(e))
        return 2
    except Exception as e:
        print_error(f"diff failed: {e.__class__.__name__}: {e}")
        return 2

    if args.output:
        try:
            out_path = safe_path(args.output).resolve()
        except ValueError as e:
            print_error(str(e))
            return 2
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"old:        {report['old']}")
        print(f"new:        {report['new']}")
        print(f"key:        {', '.join(report['key_columns'])}")
        print(f"added:      {report['added_count']}")
        print(f"removed:    {report['removed_count']}")
        print(f"changed:    {report['changed_count']}")
        if args.show_unchanged:
            print(f"unchanged:  {report['unchanged_count']}")

        def show_section(title, items, formatter):
            if not items:
                return
            print()
            print(f"--- {title} ({len(items)}) ---")
            for it in items[: args.max_print]:
                print(formatter(it))
            if len(items) > args.max_print:
                print(f"... ({len(items) - args.max_print} more)")

        show_section("ADDED", report["added"],
                     lambda it: "  + " + " | ".join(it["key"]))
        show_section("REMOVED", report["removed"],
                     lambda it: "  - " + " | ".join(it["key"]))

        if report["changed"]:
            print()
            print(f"--- CHANGED ({len(report['changed'])}) ---")
            for it in report["changed"][: args.max_print]:
                key_s = " | ".join(it["key"])
                print(f"  ~ {key_s}")
                for col, c in it["changes"].items():
                    print(f"      {col}: {c['old']!r} -> {c['new']!r}")
            if len(report["changed"]) > args.max_print:
                print(f"... ({len(report['changed']) - args.max_print} more)")

    return 0 if (report["added_count"] + report["removed_count"] + report["changed_count"]) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
