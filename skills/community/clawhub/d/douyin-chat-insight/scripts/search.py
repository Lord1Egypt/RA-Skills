#!/usr/bin/env python3
"""BM25-ish keyword search over data/*.csv for agent routing helpers."""
from __future__ import annotations

import argparse
import csv
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CSV_CONFIG = [
    ("rules.csv", ["id", "keyword", "action", "note"]),
    ("report_rules.csv", ["id", "keyword", "action", "note"]),
]


def tokenize(text: str):
    return re.findall(r"[\w\u4e00-\u9fff]+", (text or "").lower())


def load_rows():
    rows = []
    for name, _fields in CSV_CONFIG:
        path = DATA / name
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)
    return rows


def search(query: str, limit: int = 5):
    rows = load_rows()
    q = tokenize(query)
    if not q or not rows:
        return []
    df = Counter()
    docs = []
    for r in rows:
        text = " ".join(str(v) for v in r.values())
        toks = tokenize(text)
        docs.append((r, toks))
        for t in set(toks):
            df[t] += 1
    N = len(docs)
    scored = []
    for r, toks in docs:
        tf = Counter(toks)
        score = 0.0
        for t in q:
            if tf[t] == 0:
                continue
            idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
            score += idf * (tf[t])
        if score > 0:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return scored[:limit]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()
    hits = search(args.query, args.limit)
    if not hits:
        print("NO_HITS")
        return 0
    for score, r in hits:
        print(f"{score:.3f}\t{r.get('action','')}\t{r.get('keyword','')}\t{r.get('note','')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
