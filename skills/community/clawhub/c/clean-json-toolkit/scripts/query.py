#!/usr/bin/env python3
"""
query.py - jq-style path queries into a JSON / JSONL file. No external `jq`,
no `eval`.

Path syntax:
    .key                   object key access
    .key.nested            chained access
    .key.0                 numeric index into an array (also .key[0])
    .[]                    iterate over an array (one result per item)
    .key.[]                iterate over the array at .key
    .key.[].field          map each array item to .field
    .                      identity (the whole document)
    "key with spaces"      quoted key (use within a path: ."key with spaces")

Usage:
    query.py INPUT PATH [--output PATH] [--json|--jsonl|--lines|--raw]

Examples:
    query.py data.json .users
    query.py data.json '.users.[].email'
    query.py data.json '.items.[].price' --raw
    query.py orders.jsonl '.amount' --lines

Output modes:
    --json    (default) print each result as pretty JSON, separated by newlines
    --jsonl   one compact JSON value per line
    --lines   plain text: for scalars, just the value; for objects/arrays,
              compact JSON. Useful for piping to other tools.
    --raw     same as --lines but strips surrounding quotes from string scalars.

Exit codes:
    0  at least one result
    1  zero results
    2  bad arguments / unsafe path / missing file / bad path syntax / invalid JSON
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, List

from _common import load_json, safe_path


_TOK_RE = re.compile(
    r'\s*('
    r'"(?:[^"\\]|\\.)*"'      # quoted key
    r"|\["                     # [
    r"|\]"                     # ]
    r"|\."                     # .
    r"|\d+"                    # number (index)
    r"|[A-Za-z_][A-Za-z0-9_\-]*"  # identifier
    r')'
)


def parse_path(path: str) -> List[Any]:
    """Return a list of steps. Each step is one of:
        ('key', str)        -> object key access
        ('idx', int)        -> array index access
        ('iter', None)      -> iterate over array
    """
    s = path.strip()
    if s in (".", ""):
        return []
    if not s.startswith("."):
        raise ValueError(f"path must start with '.', got {path!r}")
    pos = 1
    steps: List[Any] = []
    while pos < len(s):
        m = _TOK_RE.match(s, pos)
        if not m:
            raise ValueError(f"cannot tokenize path near: {s[pos:pos+15]!r}")
        tok = m.group(1)
        pos = m.end()
        if tok == ".":
            continue
        if tok == "[":
            # Either [] (iterate) or [N]
            m2 = _TOK_RE.match(s, pos)
            if not m2:
                raise ValueError("expected ']' or index after '['")
            tk = m2.group(1)
            pos = m2.end()
            if tk == "]":
                steps.append(("iter", None))
                continue
            if tk.isdigit():
                steps.append(("idx", int(tk)))
                # consume closing ]
                m3 = _TOK_RE.match(s, pos)
                if not m3 or m3.group(1) != "]":
                    raise ValueError("missing ']' after index")
                pos = m3.end()
                continue
            raise ValueError(f"unexpected token in [...]: {tk!r}")
        if tok == "]":
            raise ValueError("unexpected ']'")
        if tok.startswith('"') and tok.endswith('"'):
            steps.append(("key", tok[1:-1].encode().decode("unicode_escape")))
            continue
        if tok.isdigit():
            # .0 form (index without brackets)
            steps.append(("idx", int(tok)))
            continue
        # identifier
        steps.append(("key", tok))
    return steps


def apply_path(data: Any, steps: List[Any]) -> List[Any]:
    """Apply the steps to data, returning a flat list of results."""
    current: List[Any] = [data]
    for kind, val in steps:
        nxt: List[Any] = []
        for item in current:
            if kind == "key":
                if isinstance(item, dict) and val in item:
                    nxt.append(item[val])
            elif kind == "idx":
                if isinstance(item, list) and 0 <= val < len(item):
                    nxt.append(item[val])
            elif kind == "iter":
                if isinstance(item, list):
                    nxt.extend(item)
                elif isinstance(item, dict):
                    nxt.extend(item.values())
        current = nxt
        if not current:
            return []
    return current


def emit(results: List[Any], mode: str, out) -> None:
    if mode == "json":
        for r in results:
            out.write(json.dumps(r, indent=2, ensure_ascii=False) + "\n")
    elif mode == "jsonl":
        for r in results:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    elif mode == "lines":
        for r in results:
            if isinstance(r, (dict, list)):
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
            else:
                out.write(("" if r is None else str(r)) + "\n")
    else:  # raw
        for r in results:
            if isinstance(r, str):
                out.write(r + "\n")
            elif isinstance(r, (dict, list)):
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
            else:
                out.write(("" if r is None else str(r)) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("path", nargs="?")
    p.add_argument("--output")
    grp = p.add_mutually_exclusive_group()
    grp.add_argument("--json", dest="mode", action="store_const", const="json")
    grp.add_argument("--jsonl", dest="mode", action="store_const", const="jsonl")
    grp.add_argument("--lines", dest="mode", action="store_const", const="lines")
    grp.add_argument("--raw", dest="mode", action="store_const", const="raw")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.path:
        print(__doc__)
        return 0 if args.help else 2

    mode = args.mode or "json"

    try:
        in_path = safe_path(args.input)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    try:
        data, kind = load_json(in_path)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        return 2

    try:
        steps = parse_path(args.path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # If the file is JSONL, treat the data as a list and iterate by default
    # (so `.amount` works directly on a JSONL file of objects).
    if kind == "jsonl" and steps and steps[0][0] != "iter":
        # Implicit iteration over the top-level list
        results: List[Any] = []
        for item in data:
            results.extend(apply_path(item, steps))
    else:
        results = apply_path(data, steps)

    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            emit(results, mode, f)
        if not args.quiet:
            print(f"query: {len(results)} result(s) -> {out_path}", file=sys.stderr)
    else:
        emit(results, mode, sys.stdout)
        if not args.quiet:
            print(f"query: {len(results)} result(s)", file=sys.stderr)

    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
