#!/usr/bin/env python3
"""infer_schema.py — Scan data files and produce a statistical profile per column.

Usage:
  python3 infer_schema.py --input <file-or-dir> [--sample N] [--json] [--out FILE]

Supported: .csv .tsv .json .jsonl .xlsx (xlsx needs openpyxl; falls back to csv engine)
Zero dependencies otherwise (stdlib only).
"""
import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import datetime

MAX_SCAN_ROWS_DEFAULT = 20000
SAMPLE_VALUES = 5

INT_RE = re.compile(r"^-?\d{1,19}$")
FLOAT_RE = re.compile(r"^-?\d+\.\d+$|^-?\d*\.?\d+[eE][+-]?\d+$")
BOOL_TRUE = {"true", "false", "yes", "no", "y", "n", "1", "0", "t", "f"}
DATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%SZ"]
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def sniff_dialect(path):
    with open(path, "r", encoding="utf-8-sig", errors="replace", newline="") as f:
        sample = f.read(65536)
    dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|") if sample.strip() else None
    return dialect


def iter_csv(path, delimiter=","):
    dialect = sniff_dialect(path) if delimiter is None else None
    with open(path, "r", encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect, delimiter=delimiter)
        for row in reader:
            yield {k: (v if v is not None else "") for k, v in row.items()}


def iter_jsonl(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj, dict):
                yield obj


def load_json_rows(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        data = json.load(f)
    if isinstance(data, list):
        return iter(data)
    if isinstance(data, dict):
        # common wrappers: {"data": [...]}, {"records": [...]}
        for key in ("data", "records", "items", "results"):
            if key in data and isinstance(data[key], list):
                return iter(data[key])
        return iter([data])
    return iter([])


def load_xlsx_rows(path):
    try:
        from openpyxl import load_workbook  # type: ignore
    except ImportError:
        print(f"WARNING: {path}: .xlsx needs openpyxl; skipping (pip install openpyxl)", file=sys.stderr)
        return iter([])
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    header = None
    for row in rows:
        if header is None:
            header = [str(h) if h is not None else f"col{i}" for i, h in enumerate(row)]
            continue
        yield {h: ("" if v is None else str(v)) for h, v in zip(header, row)}


def rows_for(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return iter_csv(path, delimiter=",")
    if ext == ".tsv":
        return iter_csv(path, delimiter="\t")
    if ext == ".jsonl" or ext == ".ndjson":
        return iter_jsonl(path)
    if ext == ".json":
        return load_json_rows(path)
    if ext == ".xlsx":
        return load_xlsx_rows(path)
    raise ValueError(f"unsupported extension: {ext}")


def try_dates(v):
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(v, fmt)
            return fmt
        except ValueError:
            continue
    return None


def infer_type(v, seen):
    """Vote-based type inference for one non-empty string value."""
    if INT_RE.match(v):
        seen["int"] += 1
    elif FLOAT_RE.match(v):
        seen["float"] += 1
    elif v.strip().lower() in BOOL_TRUE:
        seen["bool"] += 1
    elif UUID_RE.match(v):
        seen["uuid"] += 1
    else:
        d = try_dates(v)
        if d:
            seen["date"] += 1
        elif EMAIL_RE.match(v):
            seen["email"] += 1
        else:
            seen["text"] += 1


def resolve_type(counts, max_len, distinct_ratio, n):
    if not counts or n == 0:
        return "text"
    total = sum(counts.values())
    # dominant type must cover >= 90% of non-null values
    best, best_n = max(counts.items(), key=lambda kv: kv[1])
    if best_n / total < 0.9:
        return "text"  # mixed
    if best in ("int", "float") and "float" in counts and counts.get("int", 0) and best == "int" and counts.get("float", 0) / total > 0.02:
        return "float"  # ints + floats -> float
    return best if best != "email" else "text"


def profile_file(path, max_rows):
    cols = None
    stats = None
    n = 0
    for row in rows_for(path):
        if cols is None:
            cols = list(row.keys())
            stats = {c: Counter() for c in cols}
            meta = {c: {"nonnull": 0, "maxlen": 0, "distinct": Counter(), "samples": []} for c in cols}
        n += 1
        if n > max_rows:
            break
        for c in cols:
            v = row.get(c)
            v = "" if v is None else str(v).strip()
            if v == "":
                continue
            meta[c]["nonnull"] += 1
            meta[c]["maxlen"] = max(meta[c]["maxlen"], len(v))
            meta[c]["distinct"][v] += 1
            if len(meta[c]["samples"]) < SAMPLE_VALUES:
                if v not in meta[c]["samples"]:
                    meta[c]["samples"].append(v)
            infer_type(v, stats[c])
    if cols is None:
        return {"file": path, "rows_scanned": 0, "columns": []}
    columns = []
    for c in cols:
        nonnull = meta[c]["nonnull"]
        distinct = len(meta[c]["distinct"])
        counts = dict(stats[c])
        t = resolve_type(counts, meta[c]["maxlen"], distinct, nonnull)
        col = {
            "name": c,
            "inferred_type": t,
            "null_rate": round(1 - nonnull / n, 4) if n else 1.0,
            "distinct": distinct,
            "distinct_ratio": round(distinct / nonnull, 4) if nonnull else 0,
            "max_len": meta[c]["maxlen"],
            "samples": meta[c]["samples"],
        }
        if counts:
            col["type_votes"] = counts
        # key candidates
        # key candidates: require enough rows so tiny-file coincidences don't over-flag
        if nonnull == n and distinct == nonnull and n >= 10:
            col["primary_key_candidate"] = True
        columns.append(col)
    return {"file": path, "rows_scanned": n, "truncated": n > max_rows, "columns": columns}


def main():
    ap = argparse.ArgumentParser(description="Column-level statistical profiler for data files")
    ap.add_argument("--input", required=True, help="file or directory")
    ap.add_argument("--sample", type=int, default=MAX_SCAN_ROWS_DEFAULT, help="max rows per file")
    ap.add_argument("--json", action="store_true", help="JSON output (default)")
    ap.add_argument("--out", help="write JSON to this file instead of stdout")
    args = ap.parse_args()

    paths = []
    if os.path.isdir(args.input):
        for root, _dirs, files in os.walk(args.input):
            for fn in sorted(files):
                if os.path.splitext(fn)[1].lower() in (".csv", ".tsv", ".json", ".jsonl", ".ndjson", ".xlsx"):
                    paths.append(os.path.join(root, fn))
    else:
        paths = [args.input]

    profiles = []
    for p in paths:
        try:
            profiles.append(profile_file(p, args.sample))
        except Exception as e:
            profiles.append({"file": p, "error": str(e)})

    out = json.dumps({"profiles": profiles}, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"profiles written to {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
