#!/usr/bin/env python3
"""
grep.py - Pattern-match log lines with optional timestamp + level filters.
Like grep, but log-aware: filter by time window, log level, named regex
groups, and context lines.

Usage:
    grep.py INPUT [--pattern REGEX] [options]

Filters (combine with AND):
    --pattern REGEX            regex that must match the line (case-sensitive
                               by default; use --ignore-case to fold).
    --not-pattern REGEX        regex that must NOT match
    --level LVL[,LVL2...]      keep only lines with one of these levels
    --since TIMESTAMP          drop lines older than TIMESTAMP
    --until TIMESTAMP          drop lines newer than TIMESTAMP
    --invert                   final selection: keep lines that DO NOT pass

Context:
    -B N, --before N           print N lines BEFORE each match
    -A N, --after N            print N lines AFTER each match
    -C N, --context N          shorthand for -B N -A N

Output:
    --output PATH              write matched lines to PATH (default: stdout)
    --with-line                prefix each line with the (1-based) source line
    --quiet                    suppress the summary on stderr
    --json                     emit a machine-readable summary on stderr
    -h, --help                 show this help

Timestamp formats accepted by --since / --until include the same formats
parse.py understands (ISO 8601, apache-style, syslog). For syslog dates
without a year, the current year is assumed.

Exit codes:
    0  at least one line matched
    1  zero matches
    2  bad arguments / unsafe path / missing file / bad regex / bad timestamp
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from _common import (iter_lines, safe_path, extract_timestamp, extract_level,
                     parse_timestamp, LEVEL_CANONICAL)


def parse_window(s: str) -> Optional[datetime]:
    return parse_timestamp(s)


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--pattern")
    p.add_argument("--not-pattern", dest="not_pattern")
    p.add_argument("--ignore-case", dest="ignore_case", action="store_true")
    p.add_argument("--level")
    p.add_argument("--since")
    p.add_argument("--until")
    p.add_argument("--invert", action="store_true")
    p.add_argument("-B", "--before", type=int, default=0)
    p.add_argument("-A", "--after", type=int, default=0)
    p.add_argument("-C", "--context", type=int, default=0)
    p.add_argument("--output")
    p.add_argument("--with-line", dest="with_line", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
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

    pat = None
    if args.pattern:
        try:
            pat = re.compile(args.pattern,
                             re.IGNORECASE if args.ignore_case else 0)
        except re.error as e:
            print(f"Error: bad --pattern: {e}", file=sys.stderr)
            return 2
    not_pat = None
    if args.not_pattern:
        try:
            not_pat = re.compile(args.not_pattern,
                                 re.IGNORECASE if args.ignore_case else 0)
        except re.error as e:
            print(f"Error: bad --not-pattern: {e}", file=sys.stderr)
            return 2

    levels = None
    if args.level:
        levels = set()
        for lvl in args.level.split(","):
            lvl = lvl.strip().upper()
            if not lvl:
                continue
            levels.add(LEVEL_CANONICAL.get(lvl, lvl))

    since_ts = None
    if args.since:
        since_ts = parse_window(args.since)
        if since_ts is None:
            print(f"Error: could not parse --since: {args.since!r}",
                  file=sys.stderr)
            return 2
    until_ts = None
    if args.until:
        until_ts = parse_window(args.until)
        if until_ts is None:
            print(f"Error: could not parse --until: {args.until!r}",
                  file=sys.stderr)
            return 2

    out_path = None
    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

    before = args.before or args.context
    after = args.after or args.context

    def matches(line: str) -> bool:
        if pat is not None and not pat.search(line):
            return False
        if not_pat is not None and not_pat.search(line):
            return False
        if levels is not None:
            lvl = extract_level(line)
            if lvl is None or lvl not in levels:
                return False
        if since_ts is not None or until_ts is not None:
            ts = extract_timestamp(line)
            if ts is None:
                # No timestamp on this line - skip when time window required
                return False
            if since_ts is not None and ts < since_ts:
                return False
            if until_ts is not None and ts > until_ts:
                return False
        return True

    matched = 0
    scanned = 0
    output_lines: List[str] = []
    before_buf: deque = deque(maxlen=before) if before > 0 else None
    after_remaining = 0

    for line_no, line in enumerate(iter_lines(in_path), start=1):
        scanned += 1
        is_match = matches(line)
        if args.invert:
            is_match = not is_match

        if is_match:
            # Flush before context
            if before_buf is not None:
                for (n, l) in before_buf:
                    output_lines.append((f"{n}\t{l}" if args.with_line else l))
                before_buf.clear()
            output_lines.append((f"{line_no}\t{line}" if args.with_line else line))
            matched += 1
            after_remaining = after
        else:
            if after_remaining > 0:
                output_lines.append((f"{line_no}\t{line}" if args.with_line else line))
                after_remaining -= 1
            elif before_buf is not None:
                before_buf.append((line_no, line))

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            for ln in output_lines:
                f.write(ln + "\n")
    else:
        for ln in output_lines:
            print(ln)

    summary = {
        "input": str(in_path),
        "scanned": scanned,
        "matched": matched,
        "emitted": len(output_lines),
        "output": str(out_path) if out_path else None,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            extra = ""
            if (before or after) and len(output_lines) > matched:
                extra = f" (+{len(output_lines)-matched} context)"
            dest = f" -> {out_path}" if out_path else ""
            print(f"grep: {matched}/{scanned} matched{extra}{dest}",
                  file=sys.stderr)

    return 0 if matched > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
