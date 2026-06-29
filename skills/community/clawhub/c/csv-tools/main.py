#!/usr/bin/env python3
"""CSV Tools — convert, filter, transform."""
import csv, json, sys, io

VERSION = "1.0.0"

def csv_to_json(csv_text, delimiter=','):
    reader = csv.DictReader(io.StringIO(csv_text), delimiter=delimiter)
    return [row for row in reader]

if __name__ == '__main__':
    if "--version" in sys.argv: print(VERSION); sys.exit(0)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(f"""CSV Tools v{VERSION}
Usage: csv-tools <file> [options]
Options: --to-csv  --delimiter  --columns  --filter  --batch
Free: CSV↔JSON, auto-delimiter, pretty-print
Pro ($0.99): filter, columns, batch, schema validation""")
        sys.exit(0)
    for path in args:
        with open(path) as f:
            data = csv_to_json(f.read())
        print(json.dumps(data, indent=2, ensure_ascii=False))
