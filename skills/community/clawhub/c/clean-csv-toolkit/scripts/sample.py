#!/usr/bin/env python3
"""
Pick a uniformly random sample of N rows from a CSV / TSV / JSONL file.

Uses reservoir sampling (algorithm R), so the script makes a single
streaming pass and never loads the whole file. Memory use is O(N), not
O(file_size). Output is in row order of the reservoir, not insertion
order; pass --preserve-order to re-sort by original row index.

Usage:
  python3 sample.py <input> [-n N] [--seed SEED]
                            [--as csv|tsv|jsonl|md|aligned]
                            [--output file]
                            [--columns col1,col2,...]
                            [--preserve-order]

Default N is 10. Default seed is None (non-deterministic). Pass --seed
to get reproducible samples for tests.

Exit codes:
  0 = success (at least one row sampled or input had no data rows)
  1 = empty file (no header)
  2 = bad arguments / missing input / unsafe path / unknown --as / unknown column
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _common import (
    safe_path,
    open_table,
    print_error,
)
from _preview import (
    select_columns,
    write_rows,
    ALLOWED_AS,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[1])
    parser.add_argument("input", help="Path to a .csv / .tsv / .jsonl file")
    parser.add_argument("-n", "--rows", type=int, default=10,
                        help="Number of rows to sample (default 10)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Optional integer seed for reproducible sampling")
    parser.add_argument("--as", dest="as_fmt",
                        choices=tuple(sorted(ALLOWED_AS)),
                        default="aligned",
                        help="Output format (default: aligned)")
    parser.add_argument("--output", default="",
                        help="Write to file instead of stdout")
    parser.add_argument("--columns", default="",
                        help="Comma-separated subset of column names to keep")
    parser.add_argument("--preserve-order", action="store_true",
                        help="Emit sampled rows in their original row order. "
                             "Default emits them in reservoir order.")
    args = parser.parse_args()

    if args.rows < 1:
        print_error("-n must be >= 1")
        return 2

    try:
        in_path = safe_path(args.input).resolve()
    except ValueError as e:
        print_error(str(e))
        return 2
    if not in_path.is_file():
        print_error(f"not a file: {in_path}")
        return 2

    out_path = None
    if args.output:
        try:
            out_path = safe_path(args.output).resolve()
        except ValueError as e:
            print_error(str(e))
            return 2

    selected_cols = None
    if args.columns.strip():
        selected_cols = [c.strip() for c in args.columns.split(",") if c.strip()]

    rng = random.Random(args.seed)

    try:
        with open_table(in_path) as (kind, headers, rows):
            if not headers:
                print_error("input has no header row")
                return 1

            try:
                use_headers = select_columns(headers, selected_cols)
            except KeyError as e:
                print_error(str(e))
                return 2

            # Algorithm R reservoir sampling. Keep (row_index, row_dict)
            # tuples so --preserve-order can re-sort cheaply.
            reservoir = []
            for i, row in enumerate(rows):
                kept = {h: row.get(h, "") for h in use_headers}
                if i < args.rows:
                    reservoir.append((i, kept))
                else:
                    j = rng.randint(0, i)
                    if j < args.rows:
                        reservoir[j] = (i, kept)

            if args.preserve_order:
                reservoir.sort(key=lambda t: t[0])

            sampled = [r for _, r in reservoir]
            write_rows(sampled, use_headers, args.as_fmt, out_path=out_path)
    except Exception as e:
        print_error(f"sample failed: {e.__class__.__name__}: {e}")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
