#!/usr/bin/env python3
"""
follow.py - Stream a log file as it grows (tail -F equivalent), with
optional regex / level / time-window filters from grep.py.

Unlike `tail -F`, this is log-aware:
  - Filter by --pattern / --not-pattern (regex)
  - Filter by --level (WARN,ERROR,FATAL...)
  - Filter by --since (only show entries newer than this timestamp)
  - Detect log rotation: if the file shrinks / inode changes, reopen from
    the start of the new file

Usage:
    follow.py INPUT [--pattern REGEX] [--level LVL[,LVL2]]
                    [--since TIMESTAMP] [--lines N] [--no-rotate]
                    [--max-events N] [--timeout SECONDS] [--with-line] [--json]

Options:
    --lines N           print the last N lines first, then follow (default: 10)
    --no-rotate         do not detect rotation; keep reading even after
                        truncation (matches `tail -f` behavior)
    --max-events N      exit after N matched events (useful for tests / CI)
    --timeout SECONDS   exit after this many seconds of inactivity
    --interval SECONDS  poll interval (default: 0.5)
    --pattern REGEX     keep only lines matching this regex
    --not-pattern REGEX drop lines matching this regex
    --ignore-case       case-fold for both patterns
    --level LVL[,LVL2]  keep only lines with one of these levels
    --since TIMESTAMP   drop lines older than this timestamp
    --with-line         prefix each line with its (1-based) source line
    --json              output each matched line as a JSON envelope
                        {"line": N, "ts": "...", "level": "...", "text": "..."}
    --quiet             suppress the startup summary on stderr
    -h, --help          show this help

Exit codes:
    0   exited cleanly (max-events reached, timeout, or Ctrl-C)
    1   missing input file at startup
    2   bad arguments / unsafe path / bad regex / bad timestamp
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Optional

from _common import (safe_path, extract_timestamp, extract_level,
                     parse_timestamp, LEVEL_CANONICAL)


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--lines", type=int, default=10)
    p.add_argument("--no-rotate", dest="no_rotate", action="store_true")
    p.add_argument("--max-events", dest="max_events", type=int, default=0)
    p.add_argument("--timeout", type=float, default=0)
    p.add_argument("--interval", type=float, default=0.5)
    p.add_argument("--pattern")
    p.add_argument("--not-pattern", dest="not_pattern")
    p.add_argument("--ignore-case", dest="ignore_case", action="store_true")
    p.add_argument("--level")
    p.add_argument("--since")
    p.add_argument("--with-line", dest="with_line", action="store_true")
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
        return 1

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
            if lvl:
                levels.add(LEVEL_CANONICAL.get(lvl, lvl))

    since_ts = None
    if args.since:
        since_ts = parse_timestamp(args.since)
        if since_ts is None:
            print(f"Error: could not parse --since: {args.since!r}",
                  file=sys.stderr)
            return 2

    def matches(line: str) -> bool:
        if pat is not None and not pat.search(line):
            return False
        if not_pat is not None and not_pat.search(line):
            return False
        if levels is not None:
            lvl = extract_level(line)
            if lvl is None or lvl not in levels:
                return False
        if since_ts is not None:
            ts = extract_timestamp(line)
            if ts is None or ts < since_ts:
                return False
        return True

    def emit(line_no: int, line: str) -> None:
        if args.as_json:
            envelope = {
                "line": line_no, "text": line,
                "ts": (extract_timestamp(line).isoformat()
                       if extract_timestamp(line) else None),
                "level": extract_level(line),
            }
            sys.stdout.write(json.dumps(envelope, ensure_ascii=False) + "\n")
        elif args.with_line:
            sys.stdout.write(f"{line_no}\t{line}\n")
        else:
            sys.stdout.write(line + "\n")
        sys.stdout.flush()

    # Handle SIGINT / SIGTERM cleanly
    interrupted = {"flag": False}
    def _sig(_signum, _frame):
        interrupted["flag"] = True
    signal.signal(signal.SIGINT, _sig)
    signal.signal(signal.SIGTERM, _sig)

    # Print the last N lines first (head)
    line_no = 0
    if args.lines > 0:
        buf: deque = deque(maxlen=args.lines)
        line_count = 0
        with in_path.open("r", encoding="utf-8", errors="replace") as f:
            for line_count, line in enumerate(f, start=1):
                line = line.rstrip("\n").rstrip("\r")
                buf.append((line_count, line))
        for n, ln in buf:
            if matches(ln):
                emit(n, ln)
        line_no = line_count

    if not args.quiet:
        print(f"follow: tailing {in_path} (poll={args.interval}s, "
              f"lines-prefix={args.lines})", file=sys.stderr)

    fp = in_path.open("r", encoding="utf-8", errors="replace")
    fp.seek(0, 2)  # seek to end
    cur_inode = os.fstat(fp.fileno()).st_ino
    cur_size = os.fstat(fp.fileno()).st_size

    matched_total = 0
    last_event_t = time.time()

    while not interrupted["flag"]:
        chunk = fp.readline()
        if chunk:
            line = chunk.rstrip("\n").rstrip("\r")
            line_no += 1
            if matches(line):
                emit(line_no, line)
                matched_total += 1
                last_event_t = time.time()
                if args.max_events and matched_total >= args.max_events:
                    break
            continue

        # No new data; check for rotation, then sleep
        try:
            st = in_path.stat()
            if not args.no_rotate:
                if st.st_ino != cur_inode or st.st_size < cur_size:
                    if not args.quiet:
                        print(f"follow: detected rotation, reopening "
                              f"{in_path}", file=sys.stderr)
                    fp.close()
                    fp = in_path.open("r", encoding="utf-8", errors="replace")
                    cur_inode = os.fstat(fp.fileno()).st_ino
                    cur_size = os.fstat(fp.fileno()).st_size
                    line_no = 0
                    continue
            cur_size = st.st_size
        except FileNotFoundError:
            # File temporarily gone (e.g. mid-rotation). Wait a bit and retry.
            time.sleep(args.interval)
            continue

        if args.timeout and (time.time() - last_event_t) >= args.timeout:
            if not args.quiet:
                print(f"follow: timeout after {args.timeout}s of inactivity",
                      file=sys.stderr)
            break

        time.sleep(args.interval)

    fp.close()
    if not args.quiet:
        print(f"follow: exiting after {matched_total} matched event(s)",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
