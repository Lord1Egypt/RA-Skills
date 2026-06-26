#!/usr/bin/env python3
"""Clean CSV data: deduplicate, fill missing values, strip whitespace, fix encoding."""

import argparse, csv, sys

def main():
    p = argparse.ArgumentParser(description='Clean and normalize CSV data')
    p.add_argument('file', help='CSV file path')
    p.add_argument('--delimiter', default=',')
    p.add_argument('--encoding', default='utf-8')
    p.add_argument('--output', '-o', required=True, help='Output file')
    p.add_argument('--dedupe', action='store_true', help='Remove exact duplicate rows')
    p.add_argument('--dedupe-on', help='Deduplicate based on specific column(s), comma-separated')
    p.add_argument('--fill-missing', help='Replace empty cells with this value')
    p.add_argument('--strip', action='store_true', help='Strip whitespace from all fields')
    p.add_argument('--drop-empty-rows', action='store_true', help='Drop rows where all fields are empty')
    args = p.parse_args()

    with open(args.file, 'r', encoding=args.encoding) as f:
        reader = csv.DictReader(f, delimiter=args.delimiter)
        data = list(reader)
        fieldnames = reader.fieldnames

    original_count = len(data)

    # Strip whitespace
    if args.strip:
        for row in data:
            for k in row:
                if row[k]:
                    row[k] = row[k].strip()

    # Fill missing
    if args.fill_missing:
        for row in data:
            for k in row:
                if not row[k] or row[k].strip() == '':
                    row[k] = args.fill_missing

    # Drop empty rows
    if args.drop_empty_rows:
        data = [row for row in data if any(v.strip() for v in row.values() if v)]

    # Deduplicate
    if args.dedupe:
        if args.dedupe_on:
            dedupe_cols = [c.strip() for c in args.dedupe_on.split(',')]
            seen = set()
            unique = []
            for row in data:
                key = tuple(row.get(c, '') for c in dedupe_cols)
                if key not in seen:
                    seen.add(key)
                    unique.append(row)
            data = unique
        else:
            seen = set()
            unique = []
            for row in data:
                key = tuple(row.items())
                if key not in seen:
                    seen.add(key)
                    unique.append(row)
            data = unique

    with open(args.output, 'w', newline='', encoding=args.encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=args.delimiter)
        writer.writeheader()
        writer.writerows(data)

    removed = original_count - len(data)
    print(f"Cleaned: {original_count} → {len(data)} rows (removed {removed})")
    print(f"Written to {args.output}")

if __name__ == '__main__':
    main()
