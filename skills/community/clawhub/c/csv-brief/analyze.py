#!/usr/bin/env python3
"""Profile CSV files for the csv-brief skill. Standard library only.

    python3 analyze.py file1.csv [file2.csv ...] > profile.json
"""
import csv
import json
import sys
from collections import Counter


def to_number(value):
    try:
        return float(value.replace(",", "").replace("$", "").strip())
    except (ValueError, AttributeError):
        return None


def profile(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return {"file": path, "rows": 0, "columns": []}
    columns = []
    for name in rows[0].keys():
        values = [(r.get(name) or "").strip() for r in rows]
        present = [v for v in values if v != ""]
        numbers = [n for n in (to_number(v) for v in present) if n is not None]
        col = {"name": name, "blanks": len(values) - len(present), "distinct": len(set(present))}
        if present and len(numbers) == len(present):
            col.update(type="number", sum=round(sum(numbers), 2), min=min(numbers), max=max(numbers),
                       mean=round(sum(numbers) / len(numbers), 2))
        else:
            col.update(type="text", top=Counter(present).most_common(5))
        columns.append(col)
    seen = Counter(tuple(r.values()) for r in rows)
    return {"file": path, "rows": len(rows), "columns": columns,
            "duplicate_rows": sum(c - 1 for c in seen.values() if c > 1)}


if __name__ == "__main__":
    out = []
    for p in sys.argv[1:]:
        try:
            out.append(profile(p))
        except Exception as e:  # report and keep going
            out.append({"file": p, "error": str(e)})
    json.dump(out, sys.stdout, indent=2)
