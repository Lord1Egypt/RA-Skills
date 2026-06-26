#!/usr/bin/env python3
"""Join two CSV files on a common column (inner/left/outer join)."""

import argparse, csv, sys

def main():
    p = argparse.ArgumentParser(description='Join two CSV files on a column')
    p.add_argument('left', help='Left CSV file')
    p.add_argument('right', help='Right CSV file')
    p.add_argument('--on', required=True, help='Column name to join on')
    p.add_argument('--how', choices=['inner', 'left', 'outer'], default='inner')
    p.add_argument('--delimiter', default=',')
    p.add_argument('--encoding', default='utf-8')
    p.add_argument('--output', '-o', required=True, help='Output file')
    args = p.parse_args()

    with open(args.left, 'r', encoding=args.encoding) as f:
        left_data = list(csv.DictReader(f, delimiter=args.delimiter))
    left_fieldnames = list(left_data[0].keys()) if left_data else []

    with open(args.right, 'r', encoding=args.encoding) as f:
        right_data = list(csv.DictReader(f, delimiter=args.delimiter))
    right_fieldnames = list(right_data[0].keys()) if right_data else []

    # Build index on right side
    right_index = {}
    for row in right_data:
        key = row.get(args.on, '')
        if key not in right_index:
            right_index[key] = []
        right_index[key].append(row)

    left_keys = set(row.get(args.on, '') for row in left_data)
    right_keys = set(right_index.keys())

    if args.how == 'inner':
        matched_keys = left_keys & right_keys
    elif args.how == 'left':
        matched_keys = left_keys
    else:  # outer
        matched_keys = left_keys | right_keys

    # Build output fieldnames
    join_cols = left_fieldnames + [c for c in right_fieldnames if c != args.on]
    if args.on not in join_cols:
        join_cols.insert(0, args.on)

    output_rows = []
    left_index = {row.get(args.on, ''): row for row in left_data}

    for key in sorted(matched_keys):
        left_row = left_index.get(key, {})
        right_rows = right_index.get(key, [{}])
        for right_row in right_rows:
            merged = {}
            # Left side
            for c in left_fieldnames:
                merged[c] = left_row.get(c, '')
            # Right side (skip the join column to avoid dup)
            for c in right_fieldnames:
                if c != args.on:
                    merged[f"{c}"] = right_row.get(c, '')
            output_rows.append(merged)

    with open(args.output, 'w', newline='', encoding=args.encoding) as f:
        writer = csv.DictWriter(f, fieldnames=join_cols, delimiter=args.delimiter, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Join ({args.how}) on '{args.on}': {len(output_rows)} rows → {args.output}")

if __name__ == '__main__':
    main()
