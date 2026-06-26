#!/usr/bin/env python3
"""
AITable Record Importer

Import records from CSV file into AITable.
Usage: python import_records.py --base-id BASE_ID --table-id TABLE_ID data.csv
"""

import argparse
import subprocess
import json
import sys
import csv


def run_dws(args):
    """Run dws command."""
    cmd = ["dws"] + args + ["--yes"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return False
    return True


def import_record(base_id, table_id, fields):
    """Import a single record."""
    args = [
        "aitable", "record", "create",
        "--base-id", base_id,
        "--table-id", table_id,
        "--fields", json.dumps(fields, ensure_ascii=False)
    ]
    return run_dws(args)


def main():
    parser = argparse.ArgumentParser(description="Import records from CSV into AITable")
    parser.add_argument("csv_file", help="CSV file to import")
    parser.add_argument("--base-id", required=True, help="AITable Base ID")
    parser.add_argument("--table-id", required=True, help="AITable Table ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview without importing")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for imports")
    
    args = parser.parse_args()
    
    # Read CSV file
    try:
        with open(args.csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = list(reader)
    except FileNotFoundError:
        print(f"Error: File not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not records:
        print("No records found in CSV file")
        sys.exit(0)
    
    print(f"Found {len(records)} records to import")
    print(f"Base ID: {args.base_id}")
    print(f"Table ID: {args.table_id}")
    print(f"Fields: {', '.join(records[0].keys())}")
    
    if args.dry_run:
        print("\nDry run - no records will be imported")
        print(f"\nFirst record preview:")
        print(json.dumps(records[0], indent=2, ensure_ascii=False))
        sys.exit(0)
    
    # Import records
    success_count = 0
    error_count = 0
    
    print(f"\nImporting records...")
    for i, record in enumerate(records, 1):
        # Clean up field names (remove whitespace, handle special chars)
        fields = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in record.items()}
        
        print(f"[{i}/{len(records)}] Importing: {fields.get('name', fields.get('title', 'N/A'))}")
        
        if import_record(args.base_id, args.table_id, fields):
            success_count += 1
        else:
            error_count += 1
            print(f"  Failed to import record {i}")
        
        # Progress indicator
        if i % args.batch_size == 0:
            print(f"  Progress: {i}/{len(records)} records processed")
    
    print(f"\nImport completed:")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {len(records)}")


if __name__ == "__main__":
    main()
