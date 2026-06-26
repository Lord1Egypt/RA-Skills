#!/usr/bin/env python3
"""
Profile a CSV / TSV / JSONL file.

Prints a structural overview: row count, column types (auto-detected),
null counts per column, distinct counts (capped), sample values, file
size, and the detected encoding/dialect.

Usage:
  python3 inspect.py <input>
  python3 inspect.py <input> --json
  python3 inspect.py <input> --sample 5 --distinct-cap 50

Exit codes:
  0 = success
  1 = profiling failed
  2 = bad arguments / missing input / unsafe path
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _common import (
    safe_path,
    sniff_encoding,
    sniff_dialect,
    open_table,
    infer_column_type,
    human_bytes,
    print_error,
)


def profile(path: Path, sample: int, distinct_cap: int) -> Dict:
    encoding = sniff_encoding(path)
    kind, _ = sniff_dialect(path, encoding)

    with open_table(path, encoding=encoding) as (k, headers, rows):
        col_values: Dict[str, List[str]] = {h: [] for h in headers}
        col_nulls: Dict[str, int] = {h: 0 for h in headers}
        col_distinct: Dict[str, Counter] = {h: Counter() for h in headers}
        row_count = 0

        for row in rows:
            row_count += 1
            for h in headers:
                v = row.get(h, "")
                if v is None or str(v).strip() == "":
                    col_nulls[h] += 1
                else:
                    if len(col_values[h]) < 2000:
                        col_values[h].append(str(v))
                    # Track distinct count up to (cap + 1) so we know if it overflowed
                    if len(col_distinct[h]) <= distinct_cap:
                        col_distinct[h][str(v)] += 1

    columns = []
    for h in headers:
        vals = col_values[h]
        col_type = infer_column_type(vals)
        distinct = col_distinct[h]
        distinct_count = len(distinct)
        overflow = distinct_count > distinct_cap
        sample_values = vals[:sample]
        columns.append({
            "name": h,
            "type": col_type,
            "null_count": col_nulls[h],
            "null_pct": round(100.0 * col_nulls[h] / row_count, 2) if row_count else 0.0,
            "distinct_count": distinct_count if not overflow else f">{distinct_cap}",
            "sample": sample_values,
        })

    return {
        "path": str(path),
        "size": path.stat().st_size,
        "size_human": human_bytes(path.stat().st_size),
        "encoding": encoding,
        "kind": kind,
        "row_count": row_count,
        "column_count": len(headers),
        "columns": columns,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[1])
    parser.add_argument("input", help="Path to a .csv / .tsv / .jsonl file")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout")
    parser.add_argument("--sample", type=int, default=3,
                        help="Number of sample values to keep per column (default 3)")
    parser.add_argument("--distinct-cap", type=int, default=50,
                        help="Stop counting distinct values once this many are seen "
                             "(default 50). Useful for huge low-cardinality columns.")
    args = parser.parse_args()

    try:
        path = safe_path(args.input).resolve()
    except ValueError as e:
        print_error(str(e))
        return 2

    if not path.is_file():
        print_error(f"not a file: {path}")
        return 2

    if args.sample < 0 or args.distinct_cap < 1:
        print_error("--sample must be >= 0 and --distinct-cap must be >= 1")
        return 2

    try:
        report = profile(path, sample=args.sample, distinct_cap=args.distinct_cap)
    except Exception as e:
        print_error(f"profiling failed: {e.__class__.__name__}: {e}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    # Human-readable text output
    print(f"file:      {report['path']}")
    print(f"size:      {report['size_human']} ({report['size']} bytes)")
    print(f"encoding:  {report['encoding']}")
    print(f"kind:      {report['kind']}")
    print(f"rows:      {report['row_count']}")
    print(f"columns:   {report['column_count']}")
    print()
    print(f"{'#':>3}  {'name':<28}  {'type':<10}  {'nulls':>8}  {'null%':>6}  {'distinct':>10}  sample")
    print("-" * 100)
    for i, c in enumerate(report["columns"], start=1):
        name = c["name"] if len(c["name"]) <= 28 else c["name"][:25] + "..."
        sample_str = ", ".join(repr(s) if len(s) <= 20 else repr(s[:17] + "...") for s in c["sample"])
        print(f"{i:>3}  {name:<28}  {c['type']:<10}  {c['null_count']:>8}  "
              f"{c['null_pct']:>6.2f}  {str(c['distinct_count']):>10}  {sample_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
