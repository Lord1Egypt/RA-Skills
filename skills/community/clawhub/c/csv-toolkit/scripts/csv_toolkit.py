#!/usr/bin/env python3
"""CSV manipulation toolkit — parse, filter, sort, convert, and analyze CSV files.

Features:
- View CSV with formatted table output
- Filter rows by column conditions
- Sort by any column (asc/desc)
- Select specific columns
- Convert CSV ↔ JSON (records or lines)
- Get column statistics (count, min, max, mean, unique)
- Deduplicate rows
- Merge multiple CSV files
- Head/tail viewing

No external dependencies (Python stdlib only).
"""

import argparse
import csv
import io
import json
import os
import sys
from collections import defaultdict


def read_csv(filepath, delimiter=",", encoding="utf-8"):
    """Read a CSV file and return headers + rows."""
    with open(filepath, "r", encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        headers = next(reader, None)
        if headers is None:
            return [], []
        rows = list(reader)
    return headers, rows


def format_table(headers, rows, max_width=40):
    """Format headers and rows as a plain text table."""
    if not headers:
        return "(empty)"

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = min(max(col_widths[i], len(str(cell))), max_width)

    def truncate(val, width):
        s = str(val)
        return s[:width-1] + "…" if len(s) > width else s.ljust(width)

    # Header
    header_line = " | ".join(truncate(h, col_widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * w for w in col_widths)

    lines = [header_line, sep_line]
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        line = " | ".join(truncate(padded[i], col_widths[i]) for i in range(len(headers)))
        lines.append(line)

    return "\n".join(lines)


def cmd_view(args):
    """View CSV as a formatted table."""
    headers, rows = read_csv(args.file, delimiter=args.delimiter, encoding=args.encoding)
    if args.head:
        rows = rows[:args.head]
    elif args.tail:
        rows = rows[-args.tail:]
    print(format_table(headers, rows))
    print(f"\n({len(rows)} rows shown)")


def parse_condition(cond_str):
    """Parse a filter condition like 'age>30' or 'name==John'."""
    for op in [">=", "<=", "!=", "==", ">", "<", "="]:
        if op in cond_str:
            col, val = cond_str.split(op, 1)
            return col.strip(), op if op != "=" else "==", val.strip()
    raise ValueError(f"Invalid condition: {cond_str}. Use col==val, col>val, col<val, col!=val")


def matches_condition(cell_val, op, cond_val):
    """Check if a cell value matches a condition."""
    # Try numeric comparison first
    try:
        cell_num = float(cell_val)
        cond_num = float(cond_val)
        if op == "==":
            return cell_num == cond_num
        elif op == "!=":
            return cell_num != cond_num
        elif op == ">":
            return cell_num > cond_num
        elif op == "<":
            return cell_num < cond_num
        elif op == ">=":
            return cell_num >= cond_num
        elif op == "<=":
            return cell_num <= cond_num
    except ValueError:
        pass

    # Fall back to string comparison
    if op == "==":
        return cell_val.strip().lower() == cond_val.strip().lower()
    elif op == "!=":
        return cell_val.strip().lower() != cond_val.strip().lower()
    elif op == ">":
        return cell_val.strip().lower() > cond_val.strip().lower()
    elif op == "<":
        return cell_val.strip().lower() < cond_val.strip().lower()
    elif op == ">=":
        return cell_val.strip().lower() >= cond_val.strip().lower()
    elif op == "<=":
        return cell_val.strip().lower() <= cond_val.strip().lower()
    return False


def cmd_filter(args):
    """Filter rows by conditions."""
    headers, rows = read_csv(args.file, delimiter=args.delimiter, encoding=args.encoding)
    conditions = []
    for c in args.where:
        col, op, val = parse_condition(c)
        if col not in headers:
            print(f"Error: Column '{col}' not found. Available: {', '.join(headers)}", file=sys.stderr)
            sys.exit(1)
        col_idx = headers.index(col)
        conditions.append((col_idx, op, val))

    filtered = []
    for row in rows:
        match = True
        for col_idx, op, val in conditions:
            cell = row[col_idx] if col_idx < len(row) else ""
            if not matches_condition(cell, op, val):
                match = False
                break
        if match:
            filtered.append(row)

    if args.output:
        write_csv(args.output, headers, filtered, delimiter=args.delimiter)
        print(f"Wrote {len(filtered)} rows to {args.output}")
    else:
        print(format_table(headers, filtered))
        print(f"\n({len(filtered)} rows matched)")


def cmd_sort(args):
    """Sort rows by a column."""
    headers, rows = read_csv(args.file, delimiter=args.delimiter, encoding=args.encoding)
    if args.by not in headers:
        print(f"Error: Column '{args.by}' not found. Available: {', '.join(headers)}", file=sys.stderr)
        sys.exit(1)

    col_idx = headers.index(args.by)

    def sort_key(row):
        val = row[col_idx] if col_idx < len(row) else ""
        try:
            return (0, float(val))
        except ValueError:
            return (1, val.lower())

    rows.sort(key=sort_key, reverse=args.desc)

    if args.output:
        write_csv(args.output, headers, rows, delimiter=args.delimiter)
        print(f"Wrote {len(rows)} sorted rows to {args.output}")
    else:
        print(format_table(headers, rows))


def cmd_select(args):
    """Select specific columns."""
    headers, rows = read_csv(args.file, delimiter=args.delimiter, encoding=args.encoding)
    cols = [c.strip() for c in args.columns.split(",")]
    indices = []
    for c in cols:
        if c not in headers:
            print(f"Error: Column '{c}' not found. Available: {', '.join(headers)}", file=sys.stderr)
            sys.exit(1)
        indices.append(headers.index(c))

    new_headers = [headers[i] for i in indices]
    new_rows = []
    for row in rows:
        new_rows.append([row[i] if i < len(row) else "" for i in indices])

    if args.output:
        write_csv(args.output, new_headers, new_rows, delimiter=args.delimiter)
        print(f"Wrote {len(new_rows)} rows with columns [{', '.join(cols)}] to {args.output}")
    else:
        print(format_table(new_headers, new_rows))


def cmd_to_json(args):
    """Convert CSV to JSON."""
    headers, rows = read_csv(args.file, delimiter=args.delimiter, encoding=args.encoding)
    records = []
    for row in rows:
        record = {}
        for i, h in enumerate(headers):
            val = row[i] if i < len(row) else ""
            # Try to parse numbers
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    pass
            record[h] = val
        records.append(record)

    output = json.dumps(records, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Wrote {len(records)} records to {args.output}")
    else:
        print(output)


def cmd_from_json(args):
    """Convert JSON to CSV."""
    with open(args.file, "r") as f:
        data = json.load(f)

    if not isinstance(data, list) or len(data) == 0:
        print("Error: JSON must be a non-empty array of objects.", file=sys.stderr)
        sys.exit(1)

    # Collect all keys across all records for headers
    headers = []
    seen = set()
    for record in data:
        for key in record:
            if key not in seen:
                headers.append(key)
                seen.add(key)

    rows = []
    for record in data:
        rows.append([str(record.get(h, "")) for h in headers])

    if args.output:
        write_csv(args.output, headers, rows, delimiter=args.delimiter)
        print(f"Wrote {len(rows)} rows to {args.output}")
    else:
        print(format_table(headers, rows))


def cmd_stats(args):
    """Show column statistics."""
    headers, rows = read_csv(args.file, delimiter=args.delimiter, encoding=args.encoding)

    cols = headers if not args.columns else [c.strip() for c in args.columns.split(",")]
    for c in cols:
        if c not in headers:
            print(f"Warning: Column '{c}' not found, skipping.", file=sys.stderr)
            continue

        col_idx = headers.index(c)
        values = [row[col_idx] if col_idx < len(row) else "" for row in rows]
        non_empty = [v for v in values if v.strip()]
        unique = set(non_empty)

        # Try numeric stats
        nums = []
        for v in non_empty:
            try:
                nums.append(float(v))
            except ValueError:
                pass

        print(f"\n=== {c} ===")
        print(f"  Total rows:   {len(values)}")
        print(f"  Non-empty:    {len(non_empty)}")
        print(f"  Unique:       {len(unique)}")

        if nums:
            print(f"  Numeric vals: {len(nums)}")
            print(f"  Min:          {min(nums)}")
            print(f"  Max:          {max(nums)}")
            print(f"  Mean:         {sum(nums) / len(nums):.2f}")
            sorted_nums = sorted(nums)
            mid = len(sorted_nums) // 2
            median = sorted_nums[mid] if len(sorted_nums) % 2 else (sorted_nums[mid-1] + sorted_nums[mid]) / 2
            print(f"  Median:       {median}")
        else:
            top_vals = sorted(((v, values.count(v)) for v in unique), key=lambda x: -x[1])[:5]
            if top_vals:
                print(f"  Top values:   {', '.join(f'{v} ({c})' for v, c in top_vals)}")


def cmd_dedup(args):
    """Remove duplicate rows."""
    headers, rows = read_csv(args.file, delimiter=args.delimiter, encoding=args.encoding)
    seen = set()
    unique_rows = []
    removed = 0
    for row in rows:
        key = tuple(row)
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)
        else:
            removed += 1

    if args.output:
        write_csv(args.output, headers, unique_rows, delimiter=args.delimiter)
        print(f"Wrote {len(unique_rows)} unique rows to {args.output} (removed {removed} duplicates)")
    else:
        print(format_table(headers, unique_rows))
        print(f"\n({removed} duplicates removed, {len(unique_rows)} rows remaining)")


def cmd_merge(args):
    """Merge multiple CSV files."""
    all_headers = None
    all_rows = []

    for filepath in args.files:
        headers, rows = read_csv(filepath, delimiter=args.delimiter, encoding=args.encoding)
        if all_headers is None:
            all_headers = headers
        elif headers != all_headers:
            print(f"Warning: {filepath} has different headers, using first file's headers", file=sys.stderr)
        all_rows.extend(rows)

    if all_headers is None:
        print("Error: No valid CSV files provided.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        write_csv(args.output, all_headers, all_rows, delimiter=args.delimiter)
        print(f"Merged {len(args.files)} files, {len(all_rows)} total rows → {args.output}")
    else:
        print(format_table(all_headers, all_rows))
        print(f"\n({len(all_rows)} total rows from {len(args.files)} files)")


def write_csv(filepath, headers, rows, delimiter=","):
    """Write headers + rows to a CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(
        description="CSV manipulation toolkit — view, filter, sort, convert, and analyze CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--delimiter", "-d", default=",", help="CSV delimiter (default: comma)")
    parser.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # view
    p_view = sub.add_parser("view", help="View CSV as formatted table")
    p_view.add_argument("file", help="CSV file path")
    p_view.add_argument("--head", type=int, help="Show first N rows")
    p_view.add_argument("--tail", type=int, help="Show last N rows")

    # filter
    p_filter = sub.add_parser("filter", help="Filter rows by conditions")
    p_filter.add_argument("file", help="CSV file path")
    p_filter.add_argument("--where", "-w", nargs="+", required=True,
                          help="Filter conditions (e.g., 'age>30' 'status==active')")
    p_filter.add_argument("--output", "-o", help="Output file (default: stdout)")

    # sort
    p_sort = sub.add_parser("sort", help="Sort by column")
    p_sort.add_argument("file", help="CSV file path")
    p_sort.add_argument("--by", required=True, help="Column to sort by")
    p_sort.add_argument("--desc", action="store_true", help="Sort descending")
    p_sort.add_argument("--output", "-o", help="Output file")

    # select
    p_select = sub.add_parser("select", help="Select specific columns")
    p_select.add_argument("file", help="CSV file path")
    p_select.add_argument("--columns", "-c", required=True, help="Comma-separated column names")
    p_select.add_argument("--output", "-o", help="Output file")

    # to-json
    p_tojson = sub.add_parser("to-json", help="Convert CSV to JSON")
    p_tojson.add_argument("file", help="CSV file path")
    p_tojson.add_argument("--output", "-o", help="Output file")

    # from-json
    p_fromjson = sub.add_parser("from-json", help="Convert JSON array to CSV")
    p_fromjson.add_argument("file", help="JSON file path")
    p_fromjson.add_argument("--output", "-o", help="Output file")

    # stats
    p_stats = sub.add_parser("stats", help="Column statistics")
    p_stats.add_argument("file", help="CSV file path")
    p_stats.add_argument("--columns", "-c", help="Specific columns (comma-separated, default: all)")

    # dedup
    p_dedup = sub.add_parser("dedup", help="Remove duplicate rows")
    p_dedup.add_argument("file", help="CSV file path")
    p_dedup.add_argument("--output", "-o", help="Output file")

    # merge
    p_merge = sub.add_parser("merge", help="Merge multiple CSV files")
    p_merge.add_argument("files", nargs="+", help="CSV files to merge")
    p_merge.add_argument("--output", "-o", help="Output file")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmd_map = {
        "view": cmd_view,
        "filter": cmd_filter,
        "sort": cmd_sort,
        "select": cmd_select,
        "to-json": cmd_to_json,
        "from-json": cmd_from_json,
        "stats": cmd_stats,
        "dedup": cmd_dedup,
        "merge": cmd_merge,
    }

    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
