#!/usr/bin/env python3
"""Concatenate multiple CSV files vertically (stack rows)."""

import argparse, csv, sys

def main():
    p = argparse.ArgumentParser(description='Merge/concatenate CSV files')
    p.add_argument('files', nargs='+', help='CSV files to merge')
    p.add_argument('--delimiter', default=',')
    p.add_argument('--encoding', default='utf-8')
    p.add_argument('--output', '-o', required=True, help='Output file')
    p.add_argument('--dedupe', action='store_true', help='Remove duplicate rows after merge')
    args = p.parse_args()

    all_rows = []
    fieldnames = None

    for fpath in args.files:
        with open(fpath, 'r', encoding=args.encoding) as f:
            reader = csv.DictReader(f, delimiter=args.delimiter)
            if fieldnames is None:
                fieldnames = reader.fieldnames
            all_rows.extend(list(reader))

    if args.dedupe:
        seen = set()
        unique = []
        for row in all_rows:
            key = tuple(row.items())
            if key not in seen:
                seen.add(key)
                unique.append(row)
        all_rows = unique

    with open(args.output, 'w', newline='', encoding=args.encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=args.delimiter)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Merged {len(args.files)} files: {len(all_rows)} rows written to {args.output}")

if __name__ == '__main__':
    main()
