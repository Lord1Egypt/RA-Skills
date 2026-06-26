#!/usr/bin/env python3
"""
lines.py - Line-oriented utilities: deduplicate, sort, count, shuffle, head,
tail. Streams where it can (head, tail, count). Sort and dedupe load the
file (but each line is small, so 1M lines is fine).

Usage:
    lines.py INPUT --op OP [options]

Operations:
    count        print rows / characters / bytes
    dedupe       drop duplicate lines (preserves first occurrence by default)
    sort         sort lines (lexicographic; numeric with --numeric)
    shuffle      randomize order (deterministic with --seed)
    head         keep the first N (default 10) lines
    tail         keep the last N (default 10) lines, streamed

Common options:
    --output PATH        write to PATH instead of stdout
    --case-insensitive   for dedupe / sort, fold case before comparing
    --keep last|first    for dedupe, which occurrence wins (default: first)
    --numeric            for sort, sort numerically (non-numeric lines last)
    --reverse            for sort/shuffle, reverse the final order
    --seed N             for shuffle, deterministic seed
    -n N                 for head/tail, how many lines (default 10)
    --json               emit a JSON summary on stderr
    --quiet              suppress the summary
    -h, --help           show this help

Exit codes:
    0  success
    1  the operation produced zero lines of output
    2  bad arguments / unsafe path / missing file / unknown op
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import deque
from pathlib import Path
from typing import Iterable, List

from _common import iter_lines, safe_path, write_lines

OPS = {"count", "dedupe", "sort", "shuffle", "head", "tail"}


def _emit(lines: Iterable[str], out_path) -> int:
    n = 0
    if out_path is None:
        for line in lines:
            print(line)
            n += 1
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
                n += 1
    return n


def to_number(s: str):
    try:
        return int(s)
    except (TypeError, ValueError):
        pass
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--op")
    p.add_argument("--output")
    p.add_argument("--case-insensitive", dest="ci", action="store_true")
    p.add_argument("--keep", choices=("first", "last"), default="first")
    p.add_argument("--numeric", action="store_true")
    p.add_argument("--reverse", action="store_true")
    p.add_argument("--seed", type=int)
    p.add_argument("-n", dest="n", type=int, default=10)
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input:
        print(__doc__)
        return 0 if args.help else 2
    if not args.op:
        print("Error: --op is required", file=sys.stderr)
        return 2
    if args.op not in OPS:
        print(f"Error: unknown op '{args.op}'. Allowed: {', '.join(sorted(OPS))}",
              file=sys.stderr)
        return 2

    try:
        in_path = safe_path(args.input)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    out_path = None
    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

    summary = {"input": str(in_path), "op": args.op}
    n_out = 0

    if args.op == "count":
        n_lines = 0
        n_chars = 0
        for line in iter_lines(in_path):
            n_lines += 1
            n_chars += len(line)
        n_bytes = in_path.stat().st_size
        summary.update({"lines": n_lines, "chars": n_chars, "bytes": n_bytes})
        if not args.quiet:
            if args.as_json:
                print(json.dumps(summary, indent=2))
            else:
                print(f"{n_lines}\tlines")
                print(f"{n_chars}\tchars")
                print(f"{n_bytes}\tbytes\t{in_path}")
        return 0 if n_lines > 0 else 1

    elif args.op == "dedupe":
        kept: List[str] = []
        if args.keep == "first":
            seen: set = set()
            for line in iter_lines(in_path):
                key = line.casefold() if args.ci else line
                if key in seen:
                    continue
                seen.add(key)
                kept.append(line)
        else:  # last
            keyed: dict = {}
            order: List[str] = []
            for line in iter_lines(in_path):
                key = line.casefold() if args.ci else line
                if key not in keyed:
                    order.append(key)
                keyed[key] = line
            kept = [keyed[k] for k in order]
        if args.reverse:
            kept.reverse()
        n_out = _emit(kept, out_path)
        summary.update({"kept": n_out})

    elif args.op == "sort":
        lines = list(iter_lines(in_path))
        if args.numeric:
            def key_fn(s):
                n = to_number(s)
                return (1, 0.0) if n is None else (0, n)
        elif args.ci:
            def key_fn(s): return s.casefold()
        else:
            def key_fn(s): return s
        lines.sort(key=key_fn, reverse=args.reverse)
        n_out = _emit(lines, out_path)
        summary.update({"lines": n_out})

    elif args.op == "shuffle":
        lines = list(iter_lines(in_path))
        rng = random.Random(args.seed) if args.seed is not None else random.Random()
        rng.shuffle(lines)
        if args.reverse:
            lines.reverse()
        n_out = _emit(lines, out_path)
        summary.update({"lines": n_out, "seed": args.seed})

    elif args.op == "head":
        if args.n < 0:
            print("Error: -n must be >= 0", file=sys.stderr)
            return 2
        out_lines: List[str] = []
        for i, line in enumerate(iter_lines(in_path)):
            if i >= args.n:
                break
            out_lines.append(line)
        n_out = _emit(out_lines, out_path)
        summary.update({"lines": n_out})

    elif args.op == "tail":
        if args.n < 0:
            print("Error: -n must be >= 0", file=sys.stderr)
            return 2
        buf = deque(maxlen=args.n)
        for line in iter_lines(in_path):
            buf.append(line)
        n_out = _emit(list(buf), out_path)
        summary.update({"lines": n_out})

    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            dest = out_path if out_path else "<stdout>"
            print(f"Lines({args.op}): {n_out} line(s) -> {dest}", file=sys.stderr)

    return 0 if n_out > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
