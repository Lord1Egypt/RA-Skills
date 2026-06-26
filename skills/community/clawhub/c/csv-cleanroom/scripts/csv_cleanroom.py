#!/usr/bin/env python3
import argparse, csv, json, statistics

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--out", default="csv_profile.json")
    args = ap.parse_args()
    with open(args.csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    fields = reader.fieldnames or []
    null_counts = {field: 0 for field in fields}
    for row in rows:
        for field in fields:
            if row.get(field, "") in ("", None):
                null_counts[field] += 1
    out = {"rows": len(rows), "columns": fields, "null_counts": null_counts}
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
