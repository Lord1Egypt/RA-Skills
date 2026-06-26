#!/usr/bin/env python3
"""
errors.py - Aggregate errors from a log file: count by level, bucket by
time (minute / hour / day), and surface the most common error messages.

Usage:
    errors.py INPUT [--output PATH] [--bucket minute|hour|day]
                    [--top N] [--level LVL[,LVL2...]] [--json]

Options:
    --bucket minute|hour|day  time bucket size for the timeline (default: hour)
    --top N                   how many top error messages to surface (default: 10)
    --level LVL[,LVL2...]     only count these levels
                              (default: WARN,ERROR,FATAL)
    --output PATH             write a JSON / Markdown report to PATH
                              instead of printing to stdout. Extension picks
                              format: .json | .md | .csv (timeline only)
    --json                    when printing to stdout, emit JSON
    --quiet                   suppress the summary on stderr
    -h, --help                show this help

Exit codes:
    0  at least one matching log line found
    1  zero matching lines (no errors / no recognizable timestamps)
    2  bad arguments / unsafe path / missing file / unknown level /
       unsupported output extension
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from _common import (iter_lines, safe_path, extract_timestamp, extract_level,
                     LEVEL_CANONICAL)

VALID_LEVELS = sorted(set(LEVEL_CANONICAL.values()))


def bucket_key(ts: datetime, bucket: str) -> str:
    if bucket == "minute":
        return ts.strftime("%Y-%m-%dT%H:%M")
    if bucket == "hour":
        return ts.strftime("%Y-%m-%dT%H")
    if bucket == "day":
        return ts.strftime("%Y-%m-%d")
    return ts.strftime("%Y-%m-%dT%H")


# Normalize message: replace numbers, hex ids, uuids, file:line into placeholders
NUM_RE = re.compile(r"\b\d+\b")
HEX_RE = re.compile(r"\b[0-9a-fA-F]{8,}\b")
UUID_RE = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
PATH_LINE_RE = re.compile(r"(?:[\w./\-]+):\d+")
TIMESTAMP_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})?")


def fingerprint(message: str) -> str:
    s = TIMESTAMP_RE.sub("<TS>", message)
    s = UUID_RE.sub("<UUID>", s)
    s = HEX_RE.sub("<HEX>", s)
    s = PATH_LINE_RE.sub(lambda m: m.group(0).split(":")[0] + ":<LINE>", s)
    s = NUM_RE.sub("<N>", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > 200:
        s = s[:200] + "..."
    return s


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--bucket", choices=("minute", "hour", "day"), default="hour")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--level", default="WARN,ERROR,FATAL")
    p.add_argument("--output")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input:
        print(__doc__)
        return 0 if args.help else 2

    try:
        in_path = safe_path(args.input)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    wanted_levels = set()
    for lvl in args.level.split(","):
        lvl = lvl.strip().upper()
        if not lvl:
            continue
        canonical = LEVEL_CANONICAL.get(lvl, lvl)
        if canonical not in VALID_LEVELS:
            print(f"Error: unknown level '{lvl}'. Allowed: {', '.join(VALID_LEVELS)}",
                  file=sys.stderr)
            return 2
        wanted_levels.add(canonical)

    out_path = None
    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        if out_path.suffix.lower() not in (".json", ".md", ".csv"):
            print(f"Error: --output extension must be .json, .md, or .csv",
                  file=sys.stderr)
            return 2

    by_level: Counter = Counter()
    timeline: Dict[str, Counter] = defaultdict(Counter)
    message_groups: Counter = Counter()
    sample_per_group: Dict[str, str] = {}
    n_matched = 0
    n_scanned = 0
    first_ts: Optional[datetime] = None
    last_ts: Optional[datetime] = None

    for line in iter_lines(in_path):
        n_scanned += 1
        lvl = extract_level(line)
        if not lvl or lvl not in wanted_levels:
            continue
        by_level[lvl] += 1
        ts = extract_timestamp(line)
        if ts is not None:
            timeline[bucket_key(ts, args.bucket)][lvl] += 1
            if first_ts is None or ts < first_ts:
                first_ts = ts
            if last_ts is None or ts > last_ts:
                last_ts = ts
        fp = fingerprint(line)
        message_groups[fp] += 1
        if fp not in sample_per_group:
            sample_per_group[fp] = line[:300]
        n_matched += 1

    if n_matched == 0:
        if not args.quiet:
            print(f"errors: scanned {n_scanned} lines, no matching log entries "
                  f"(looking for levels: {','.join(sorted(wanted_levels))})",
                  file=sys.stderr)
        return 1

    top_groups = message_groups.most_common(args.top)
    summary = {
        "input": str(in_path),
        "lines_scanned": n_scanned,
        "lines_matched": n_matched,
        "levels": dict(by_level),
        "first_timestamp": first_ts.isoformat() if first_ts else None,
        "last_timestamp": last_ts.isoformat() if last_ts else None,
        "bucket": args.bucket,
        "timeline": {k: dict(v) for k, v in sorted(timeline.items())},
        "top_groups": [
            {"count": c, "fingerprint": fp, "sample": sample_per_group[fp]}
            for fp, c in top_groups
        ],
    }

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        ext = out_path.suffix.lower()
        if ext == ".json":
            out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        elif ext == ".csv":
            # Just the timeline as CSV
            with out_path.open("w", encoding="utf-8") as f:
                cols = ["bucket"] + sorted({lvl for v in timeline.values() for lvl in v})
                f.write(",".join(cols) + "\n")
                for k in sorted(timeline):
                    row = [k] + [str(timeline[k].get(lvl, 0)) for lvl in cols[1:]]
                    f.write(",".join(row) + "\n")
        else:  # .md
            lines: List[str] = []
            lines.append(f"# Error report: {in_path}\n")
            lines.append(f"- Lines scanned: **{n_scanned}**")
            lines.append(f"- Lines matched: **{n_matched}**")
            if first_ts and last_ts:
                lines.append(f"- Range: {first_ts.isoformat()} \u2192 {last_ts.isoformat()}")
            lines.append("")
            lines.append("## By level")
            for lvl, c in by_level.most_common():
                lines.append(f"- {lvl}: {c}")
            lines.append("")
            lines.append(f"## Timeline ({args.bucket} buckets)")
            for k in sorted(timeline):
                parts = ", ".join(f"{lvl}={c}" for lvl, c in
                                  sorted(timeline[k].items()))
                lines.append(f"- {k}: {parts}")
            lines.append("")
            lines.append(f"## Top {len(top_groups)} message group(s)")
            for c, (fp, _) in zip([g[1] for g in top_groups], top_groups):
                lines.append(f"### {c}x")
                lines.append(f"```\n{sample_per_group[fp]}\n```")
                lines.append("")
            out_path.write_text("\n".join(lines), encoding="utf-8")
    else:
        if args.as_json:
            print(json.dumps(summary, indent=2))
        else:
            print(f"Error report for {in_path}")
            print(f"  Lines scanned: {n_scanned}")
            print(f"  Lines matched: {n_matched}")
            if first_ts and last_ts:
                print(f"  Range: {first_ts.isoformat()} -> {last_ts.isoformat()}")
            print()
            print("  By level:")
            for lvl, c in by_level.most_common():
                print(f"    {lvl:<6s} {c}")
            print()
            print(f"  Top {len(top_groups)} message group(s):")
            for fp, c in top_groups:
                preview = sample_per_group[fp]
                if len(preview) > 120:
                    preview = preview[:120] + "..."
                print(f"    {c:>5d}  {preview}")

    if not args.quiet:
        print(f"errors: {n_matched} matched / {n_scanned} scanned" +
              (f" -> {out_path}" if out_path else ""), file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
