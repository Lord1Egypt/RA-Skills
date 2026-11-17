#!/usr/bin/env python3
"""Audit a short-drama retention plan for hooks, payoffs, comments, and cliffhangers."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

REQUIRED = [
    "series", "episode", "opening_hook", "opening_question", "promise",
    "midpoint_turn", "cliffhanger_type", "cliffhanger", "payoff",
    "open_loop", "comment_prompt", "shareable_moment", "next_episode_tease",
]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("retention_plan")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.retention_plan)
    if not path.exists():
        print(f"missing file: {path}")
        sys.exit(1)
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    errors, warnings = [], []
    missing_headers = [h for h in REQUIRED if h not in headers]
    if missing_headers:
        errors.append(f"missing headers: {missing_headers}")
    for i, row in enumerate(rows, start=2):
        for field in REQUIRED:
            if not (row.get(field) or "").strip():
                warnings.append(f"row {i}: empty {field}")
    # repeated cliffhanger types
    by_series = {}
    for row in rows:
        by_series.setdefault(row.get("series", ""), []).append(row)
    for series, series_rows in by_series.items():
        seq = [r.get("cliffhanger_type", "") for r in series_rows]
        run = 1
        for i in range(1, len(seq)):
            if seq[i] and seq[i] == seq[i-1]:
                run += 1
                if run >= 3:
                    warnings.append(f"series {series}: cliffhanger type '{seq[i]}' repeats {run}+ times in a row")
            else:
                run = 1
        if len(series_rows) > 1 and not any("finale" in (r.get("notes","") + r.get("episode","")).lower() for r in series_rows):
            # not an error; just a planning reminder
            pass
    counts = Counter(r.get("cliffhanger_type", "") for r in rows if r.get("cliffhanger_type"))
    result = {"status": "fail" if errors else "pass", "rows": len(rows), "errors": errors, "warnings": warnings, "cliffhanger_types": dict(counts)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"STATUS: {result['status'].upper()}  rows={len(rows)}")
        print("Cliffhanger types:", counts)
        for e in errors: print("[FAIL]", e)
        for w in warnings[:80]: print("[WARN]", w)
        if len(warnings) > 80: print(f"... {len(warnings)-80} more warnings")
    if errors or not rows:
        sys.exit(1)

if __name__ == "__main__":
    main()
