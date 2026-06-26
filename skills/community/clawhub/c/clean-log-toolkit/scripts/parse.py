#!/usr/bin/env python3
"""
parse.py - Parse a log file into structured rows (timestamp, level, message)
or apply a custom regex with named groups. Output as TSV / CSV / JSONL.

Auto-detects common log formats:
    - apache-combined   (Common Log Format + referrer + user-agent)
    - apache-common     (CLF)
    - nginx-access      (default nginx access log)
    - syslog            (rfc3164: 'Jan  1 12:34:56 host process[pid]: msg')
    - json-line         (one JSON object per line)
    - generic           (try to find timestamp + level + message)

Usage:
    parse.py INPUT OUTPUT [--format AUTO|...] [--regex PATTERN] [options]

Options:
    --format FMT             one of apache-combined, apache-common,
                             nginx-access, syslog, json-line, generic, auto
                             (default: auto)
    --regex PATTERN          custom regex with named groups; overrides --format
    --fields F1,F2,...       for JSONL/json-line, keep only these fields
                             (otherwise keep all)
    --json                   alias for output format JSONL (also picked from
                             output extension)
    --quiet                  suppress the summary on stderr
    --json-summary           emit a machine-readable summary on stderr
    --skip-unparseable       silently skip lines that don't match
                             (default: emit them with kind='unparsed')
    -h, --help               show this help

Exit codes:
    0  at least one row produced
    1  zero parseable rows
    2  bad arguments / unsafe path / missing file / unsupported format /
       bad regex / unknown format / unsupported output extension
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Tuple

from _common import (iter_lines, safe_path, extract_timestamp,
                     extract_level, parse_timestamp)

ALLOWED_OUTPUT_EXTS = {".csv", ".tsv", ".jsonl"}


# ---- Built-in format patterns ---------------------------------------------

BUILTIN_FORMATS: Dict[str, Pattern[str]] = {
    "apache-common": re.compile(
        r'^(?P<host>\S+) \S+ (?P<user>\S+) '
        r'\[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\S+)$'
    ),
    "apache-combined": re.compile(
        r'^(?P<host>\S+) \S+ (?P<user>\S+) '
        r'\[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\S+) '
        r'"(?P<referer>[^"]*)" '
        r'"(?P<user_agent>[^"]*)"'
    ),
    "nginx-access": re.compile(
        r'^(?P<host>\S+) - (?P<user>\S+) '
        r'\[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\d+) '
        r'"(?P<referer>[^"]*)" '
        r'"(?P<user_agent>[^"]*)"'
    ),
    "syslog": re.compile(
        r'^(?P<timestamp>[A-Z][a-z]{2} {1,2}\d{1,2} \d{2}:\d{2}:\d{2}) '
        r'(?P<host>\S+) '
        r'(?P<process>[\w\-./]+)(?:\[(?P<pid>\d+)\])?: '
        r'(?P<message>.*)$'
    ),
}


def detect_format(sample: List[str]) -> str:
    """Sniff the format from the first ~50 lines."""
    if not sample:
        return "generic"
    # JSON-line: first non-empty line begins with '{'
    for line in sample:
        s = line.lstrip()
        if not s:
            continue
        if s.startswith("{"):
            return "json-line"
        break
    # Try the regex formats in order of specificity
    for name in ("apache-combined", "nginx-access", "apache-common", "syslog"):
        pat = BUILTIN_FORMATS[name]
        hit = sum(1 for line in sample if pat.match(line))
        if hit >= max(1, len(sample) // 4):  # >=25% of sample
            return name
    return "generic"


def parse_row(line: str, fmt: str, pat: Optional[Pattern[str]],
              custom_pat: Optional[Pattern[str]]) -> Optional[Dict[str, str]]:
    if custom_pat is not None:
        m = custom_pat.search(line)
        if not m:
            return None
        return {k: ("" if v is None else v) for k, v in m.groupdict().items()}

    if fmt == "json-line":
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            return None
        if not isinstance(obj, dict):
            return None
        return {k: ("" if v is None else str(v)) for k, v in obj.items()}

    if pat is not None:
        m = pat.match(line)
        if not m:
            return None
        return {k: ("" if v is None else v) for k, v in m.groupdict().items()}

    # Generic: best-effort timestamp + level + message
    ts = extract_timestamp(line)
    lvl = extract_level(line)
    return {
        "timestamp": ts.isoformat() if ts else "",
        "level": lvl or "",
        "message": line,
    }


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--format", default="auto",
                   choices=("auto", "apache-common", "apache-combined",
                            "nginx-access", "syslog", "json-line", "generic"))
    p.add_argument("--regex")
    p.add_argument("--fields")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--json-summary", dest="json_summary", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--skip-unparseable", dest="skip_bad", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    ext = out_path.suffix.lower()
    if ext not in ALLOWED_OUTPUT_EXTS:
        print(f"Error: unsupported output extension '{ext}'. "
              f"Allowed: {', '.join(sorted(ALLOWED_OUTPUT_EXTS))}.", file=sys.stderr)
        return 2

    custom_pat = None
    if args.regex:
        try:
            custom_pat = re.compile(args.regex)
        except re.error as e:
            print(f"Error: bad --regex: {e}", file=sys.stderr)
            return 2
        if not custom_pat.groupindex:
            print("Error: --regex must contain at least one named group "
                  "(e.g. '(?P<name>...)')", file=sys.stderr)
            return 2

    fmt = args.format
    if not custom_pat and fmt == "auto":
        sample: List[str] = []
        for line in iter_lines(in_path):
            sample.append(line)
            if len(sample) >= 50:
                break
        fmt = detect_format(sample)

    pat = BUILTIN_FORMATS.get(fmt) if fmt in BUILTIN_FORMATS else None

    fields_filter = None
    if args.fields:
        fields_filter = [f.strip() for f in args.fields.split(",") if f.strip()]

    rows_in = 0
    rows_out = 0
    rows_unparsed = 0
    header_seen: List[str] = []  # for json-line we need union of keys
    pending_rows: List[Dict[str, str]] = []
    use_buffer = (fmt == "json-line" and ext in (".csv", ".tsv")) or \
                 (custom_pat is None and pat is None and ext in (".csv", ".tsv"))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt_out = "jsonl" if ext == ".jsonl" else ("tsv" if ext == ".tsv" else "csv")

    # If we know the header up-front (a builtin pattern with fixed groupindex,
    # or a --regex with fixed groupindex), stream directly.
    fixed_header: Optional[List[str]] = None
    if custom_pat is not None:
        fixed_header = list(custom_pat.groupindex.keys())
    elif pat is not None:
        fixed_header = list(pat.groupindex.keys())
    elif fmt == "generic":
        fixed_header = ["timestamp", "level", "message"]

    def write_csv_buffered(rows: List[Dict[str, str]]) -> None:
        nonlocal rows_out
        if not rows:
            return
        # Compute union header in insertion order
        seen: set = set()
        cols: List[str] = []
        for r in rows:
            for k in r:
                if k not in seen:
                    seen.add(k); cols.append(k)
        if fields_filter:
            cols = [c for c in fields_filter if c in seen]
        delim = "\t" if fmt_out == "tsv" else ","
        with out_path.open("w", encoding="utf-8", newline="") as fout:
            w = csv.DictWriter(fout, fieldnames=cols, delimiter=delim,
                               extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
                rows_out += 1

    if not use_buffer:
        delim = "\t" if fmt_out == "tsv" else ","
        fout = out_path.open("w", encoding="utf-8", newline="")
        try:
            if fmt_out == "jsonl":
                writer = None
            else:
                writer = csv.DictWriter(fout, fieldnames=fixed_header,
                                        delimiter=delim, extrasaction="ignore")
                writer.writeheader()

            for line in iter_lines(in_path):
                if not line:
                    continue
                rows_in += 1
                row = parse_row(line, fmt, pat, custom_pat)
                if row is None:
                    rows_unparsed += 1
                    if args.skip_bad:
                        continue
                    row = {"kind": "unparsed", "message": line}

                if fields_filter:
                    row = {k: row.get(k, "") for k in fields_filter}

                if fmt_out == "jsonl":
                    fout.write(json.dumps(row, ensure_ascii=False) + "\n")
                else:
                    writer.writerow(row)
                rows_out += 1
        finally:
            fout.close()
    else:
        # Buffered path (json-line -> CSV/TSV with dynamic header)
        for line in iter_lines(in_path):
            if not line:
                continue
            rows_in += 1
            row = parse_row(line, fmt, pat, custom_pat)
            if row is None:
                rows_unparsed += 1
                if args.skip_bad:
                    continue
                row = {"kind": "unparsed", "message": line}
            pending_rows.append(row)
        write_csv_buffered(pending_rows)

    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "format": "regex" if custom_pat else fmt,
        "lines_scanned": rows_in,
        "rows_written": rows_out,
        "unparsed": rows_unparsed,
    }
    if not args.quiet:
        if args.json_summary:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            print(f"Parse({summary['format']}): {rows_in} lines -> "
                  f"{rows_out} rows ({rows_unparsed} unparsed) -> {out_path}",
                  file=sys.stderr)
    return 0 if rows_out > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
