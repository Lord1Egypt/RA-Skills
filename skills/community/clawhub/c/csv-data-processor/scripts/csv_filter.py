#!/usr/bin/env python3
"""Filter, sort, and select columns from CSV data."""

import argparse, csv, json, sys

def main():
    p = argparse.ArgumentParser(description='Filter and transform CSV data')
    p.add_argument('file', help='CSV file path')
    p.add_argument('--delimiter', default=',')
    p.add_argument('--encoding', default='utf-8')
    p.add_argument('--no-header', action='store_true')
    p.add_argument('--where', help='Filter expression, e.g. "age > 25", "name == \\"Alice\\""')
    p.add_argument('--select', help='Comma-separated column names to keep')
    p.add_argument('--sort', help='Column name to sort by')
    p.add_argument('--desc', action='store_true', help='Sort descending')
    p.add_argument('--limit', type=int, help='Max rows to output')
    p.add_argument('--output', '-o', help='Output file (default: stdout)')
    args = p.parse_args()

    with open(args.file, 'r', encoding=args.encoding) as f:
        reader = csv.DictReader(f, delimiter=args.delimiter)
        data = list(reader)

    if not data:
        print("(no data)")
        return

    # Filter
    if args.where:
        filtered = []
        for row in data:
            env = {k: v for k, v in row.items()}
            # Try numeric conversion for comparison
            for k, v in env.items():
                try:
                    env[k] = int(v)
                except ValueError:
                    try:
                        env[k] = float(v)
                    except ValueError:
                        pass
            try:
                if eval(args.where, {"__builtins__": {}}, env):
                    filtered.append(row)
            except Exception as e:
                print(f"Filter error: {e}")
                sys.exit(1)
        data = filtered

    # Select columns
    if args.select:
        cols = [c.strip() for c in args.select.split(',')]
        data = [{k: row.get(k, '') for k in cols} for row in data]

    # Sort
    if args.sort:
        try:
            data.sort(key=lambda r: (r.get(args.sort, ''),), reverse=args.desc)
        except TypeError:
            data.sort(key=lambda r: (float(r.get(args.sort, 0)),), reverse=args.desc)

    # Limit
    if args.limit:
        data = data[:args.limit]

    # Collect fieldnames preserving order
    if args.select:
        fieldnames = cols
    else:
        fieldnames = list(data[0].keys())

    outfile = open(args.output, 'w', newline='', encoding=args.encoding) if args.output else sys.stdout
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=args.delimiter)
    writer.writeheader()
    writer.writerows(data)
    if args.output:
        outfile.close()
        print(f"Wrote {len(data)} rows to {args.output}")
    else:
        # Also print summary to stderr
        print(f"({len(data)} rows)", file=sys.stderr)

if __name__ == '__main__':
    main()
