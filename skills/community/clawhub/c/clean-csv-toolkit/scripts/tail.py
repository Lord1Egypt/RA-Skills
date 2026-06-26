#!/usr/bin/env python3
"""
Print the last N rows of a CSV / TSV / JSONL file in a readable form.

Like `tail` for shell, but format-aware: parses the source and outputs in
a chosen format. Uses a single streaming pass with a bounded ring buffer,
so it works on multi-gigabyte files without loading the whole file.

Usage:
  python3 tail.py <input> [-n N] [--as csv|tsv|jsonl|md|aligned]
                          [--output file]
                          [--no-header]
                          [--columns col1,col2,...]

Default N is 10. Default output format is `aligned`.

Exit codes:
  0 = success
  1 = empty file (no header detected)
  2 = bad arguments / missing input / unsafe path / unknown --as / unknown column
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
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
                        help="Number of rows to print (default 10)")
    parser.add_argument("--as", dest="as_fmt",
                        choices=tuple(sorted(ALLOWED_AS)),
                        default="aligned",
                        help="Output format (default: aligned)")
    parser.add_argument("--output", default="",
                        help="Write to file instead of stdout")
    parser.add_argument("--no-header", action="store_true",
                        help="Skip the header row in `csv|tsv|md|aligned` modes")
    parser.add_argument("--columns", default="",
                        help="Comma-separated subset of column names to keep")
    args = parser.parse_args()

    if args.rows < 0:
        print_error("-n must be >= 0")
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

            # Bounded ring buffer so we never load more than N rows in memory.
            buf: deque = deque(maxlen=args.rows or 1)
            if args.rows == 0:
                # Caller asked for zero rows; consume nothing and emit header only.
                pass
            else:
                for row in rows:
                    buf.append({h: row.get(h, "") for h in use_headers})

            write_rows(
                list(buf), use_headers, args.as_fmt,
                out_path=out_path, include_header=not args.no_header,
            )
    except Exception as e:
        print_error(f"tail failed: {e.__class__.__name__}: {e}")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
