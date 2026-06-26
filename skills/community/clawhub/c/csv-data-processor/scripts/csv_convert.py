#!/usr/bin/env python3
"""Convert CSV to JSON, JSON to CSV, or CSV to SQL INSERT statements."""

import argparse, csv, json, sqlite3, sys

def csv_to_json(csv_path, delimiter, encoding, has_header, pretty):
    with open(csv_path, 'r', encoding=encoding) as f:
        if has_header:
            reader = csv.DictReader(f, delimiter=delimiter)
            data = list(reader)
        else:
            reader = csv.reader(f, delimiter=delimiter)
            rows = list(reader)
            if rows:
                cols = [f"col{i}" for i in range(len(rows[0]))]
                data = [dict(zip(cols, r)) for r in rows]
            else:
                data = []
    indent = 2 if pretty else None
    return json.dumps(data, indent=indent, default=str)

def json_to_csv(json_path, delimiter, encoding):
    with open(json_path, 'r', encoding=encoding) as f:
        data = json.load(f)
    if not data:
        return ""
    if isinstance(data, dict):
        data = [data]
    fieldnames = list(data[0].keys())
    output = []
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)
    return '\n'.join(output)

def csv_to_sql(csv_path, delimiter, encoding, has_header, table):
    with open(csv_path, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)
    if not rows:
        return ""
    if has_header:
        cols = rows[0]
        data = rows[1:]
    else:
        cols = [f"col{i}" for i in range(len(rows[0]))]
        data = rows

    lines = [f"-- Converted from {csv_path}", f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(cols)});", ""]
    for row in data:
        vals = []
        for v in row:
            if v == '' or v is None:
                vals.append('NULL')
            else:
                try:
                    float(v)
                    vals.append(v)
                except ValueError:
                    vals.append(repr(v))
        lines.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(vals)});")
    return '\n'.join(lines)

def main():
    p = argparse.ArgumentParser(description='Convert between CSV, JSON, and SQL')
    p.add_argument('input', help='Input file')
    p.add_argument('--to', choices=['json', 'csv', 'sql'], required=True, help='Target format')
    p.add_argument('--delimiter', default=',')
    p.add_argument('--encoding', default='utf-8')
    p.add_argument('--no-header', action='store_true')
    p.add_argument('--table', default='data', help='Table name for SQL output')
    p.add_argument('--pretty', action='store_true', help='Pretty-print JSON')
    p.add_argument('--output', '-o', help='Output file (default: stdout)')
    args = p.parse_args()

    if args.to == 'json':
        result = csv_to_json(args.input, args.delimiter, args.encoding, not args.no_header, args.pretty)
    elif args.to == 'csv':
        result = json_to_csv(args.input, args.delimiter, args.encoding)
    elif args.to == 'sql':
        result = csv_to_sql(args.input, args.delimiter, args.encoding, not args.no_header, args.table)

    if args.output:
        with open(args.output, 'w', encoding=args.encoding) as f:
            f.write(result)
            if not result.endswith('\n'):
                f.write('\n')
        print(f"Written to {args.output}")
    else:
        print(result)

if __name__ == '__main__':
    main()
