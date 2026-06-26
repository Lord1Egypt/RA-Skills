#!/usr/bin/env python3
"""
diff_text.py - Compare two text files and produce a unified, side-by-side, or
HTML diff. Uses Python's stdlib `difflib` so the output format is the same as
`difflib.unified_diff` and `difflib.HtmlDiff`.

Usage:
    diff_text.py FILE1 FILE2 [--mode unified|side|html] [--output PATH]
                              [--context N] [--ignore-case]
                              [--ignore-whitespace] [--json]

Options:
    --mode MODE          unified (default), side, or html
    --output PATH        write diff to PATH (extension is auto-checked for html mode)
    --context N          context lines around each change (unified only, default 3)
    --ignore-case        case-fold lines before comparing
    --ignore-whitespace  collapse runs of whitespace before comparing
    --json               emit a JSON summary on stderr (changed_lines, etc.)
    --quiet              suppress the summary
    -h, --help           show this help

Exit codes:
    0  files are identical
    1  files differ (diff was produced normally)
    2  bad arguments / unsafe path / missing file
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import List

from _common import safe_path

WS_RE = re.compile(r"\s+")


def normalize(line: str, ignore_case: bool, ignore_ws: bool) -> str:
    if ignore_ws:
        line = WS_RE.sub(" ", line).strip()
    if ignore_case:
        line = line.casefold()
    return line


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("file1", nargs="?")
    p.add_argument("file2", nargs="?")
    p.add_argument("--mode", choices=("unified", "side", "html"), default="unified")
    p.add_argument("--output")
    p.add_argument("--context", type=int, default=3)
    p.add_argument("--ignore-case", dest="ignore_case", action="store_true")
    p.add_argument("--ignore-whitespace", dest="ignore_ws", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.file1 or not args.file2:
        print(__doc__)
        return 0 if args.help else 2

    try:
        a_path = safe_path(args.file1)
        b_path = safe_path(args.file2)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    for p_ in (a_path, b_path):
        if not p_.is_file():
            print(f"Error: not a file: {p_}", file=sys.stderr)
            return 2

    out_path = None
    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        if args.mode == "html" and out_path.suffix.lower() != ".html":
            print(f"Error: --mode html requires .html output extension",
                  file=sys.stderr)
            return 2

    a_lines = a_path.read_text(encoding="utf-8", errors="replace").splitlines()
    b_lines = b_path.read_text(encoding="utf-8", errors="replace").splitlines()

    if args.ignore_case or args.ignore_ws:
        a_cmp = [normalize(l, args.ignore_case, args.ignore_ws) for l in a_lines]
        b_cmp = [normalize(l, args.ignore_case, args.ignore_ws) for l in b_lines]
    else:
        a_cmp, b_cmp = a_lines, b_lines

    identical = a_cmp == b_cmp

    if args.mode == "unified":
        diff_lines = list(difflib.unified_diff(
            a_cmp if (args.ignore_case or args.ignore_ws) else a_lines,
            b_cmp if (args.ignore_case or args.ignore_ws) else b_lines,
            fromfile=str(a_path), tofile=str(b_path),
            n=args.context, lineterm="",
        ))
        out_text = "\n".join(diff_lines)
    elif args.mode == "side":
        # Custom 2-column rendering
        cols: List[str] = []
        width = 60
        sm = difflib.SequenceMatcher(a=a_cmp, b=b_cmp)
        cols.append(f"{'--- ' + a_path.name:<{width}} | {'+++ ' + b_path.name}")
        cols.append("-" * (width * 2 + 3))
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for li, lj in zip(a_lines[i1:i2], b_lines[j1:j2]):
                    cols.append(f"{li[:width]:<{width}} | {lj[:width]}")
            elif tag == "delete":
                for li in a_lines[i1:i2]:
                    cols.append(f"{li[:width]:<{width}} | {'< removed >'}")
            elif tag == "insert":
                for lj in b_lines[j1:j2]:
                    cols.append(f"{'< added >':<{width}} | {lj[:width]}")
            elif tag == "replace":
                left = a_lines[i1:i2]
                right = b_lines[j1:j2]
                m = max(len(left), len(right))
                for k in range(m):
                    li = left[k] if k < len(left) else "< removed >"
                    lj = right[k] if k < len(right) else "< added >"
                    cols.append(f"{li[:width]:<{width}} | {lj[:width]}")
        out_text = "\n".join(cols)
    else:  # html
        out_text = difflib.HtmlDiff(wrapcolumn=80).make_file(
            a_lines, b_lines, fromdesc=str(a_path), todesc=str(b_path),
            context=False
        )

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text + ("\n" if out_text and not out_text.endswith("\n") else ""),
                            encoding="utf-8")
    else:
        if out_text:
            print(out_text)

    # Count changes using a SequenceMatcher pass
    sm = difflib.SequenceMatcher(a=a_cmp, b=b_cmp)
    added = removed = changed = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert":
            added += (j2 - j1)
        elif tag == "delete":
            removed += (i2 - i1)
        elif tag == "replace":
            changed += max(i2 - i1, j2 - j1)

    summary = {
        "file1": str(a_path),
        "file2": str(b_path),
        "identical": identical,
        "added_lines": added,
        "removed_lines": removed,
        "changed_lines": changed,
        "mode": args.mode,
        "output": str(out_path) if out_path else None,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            if identical:
                print(f"diff: identical", file=sys.stderr)
            else:
                print(f"diff: +{added} -{removed} ~{changed} ({args.mode})",
                      file=sys.stderr)

    return 0 if identical else 1


if __name__ == "__main__":
    sys.exit(main())
