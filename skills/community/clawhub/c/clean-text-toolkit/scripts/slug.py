#!/usr/bin/env python3
"""
slug.py - Turn a string (or a column of strings) into URL-safe slugs.

Two modes:

  Single string:
      slug.py --text "Hello, World!"
      -> hello-world

  Batch (one line in, one slug out):
      slug.py INPUT OUTPUT [options]

Usage:
    slug.py --text "STRING" [options]
    slug.py INPUT OUTPUT [options]

Options:
    --text STRING       slugify a single string and print it to stdout
    --separator CHAR    word separator (default: '-')
    --max-length N      truncate the slug to N characters (default: 80, 0 = no limit)
    --lower             lowercase (default: on; use --no-lower to disable)
    --no-lower          keep original case
    --ascii             transliterate non-ASCII to a best-effort ASCII fallback
                        (decompose Unicode + drop combining marks)
    --keep-dots         keep '.' in the slug (useful for filenames)
    --dedupe            also drop adjacent duplicate slugs in batch mode
    --json              emit a JSON summary on stderr
    --quiet             suppress the summary
    -h, --help          show this help

Exit codes:
    0  success
    1  batch mode produced zero non-empty slugs
    2  bad arguments / unsafe path / missing file / both --text and batch given
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import List

from _common import iter_lines, safe_path, write_lines


_NONWORD_RE_KEEPDOTS = re.compile(r"[^\w.]+", flags=re.UNICODE)
_NONWORD_RE = re.compile(r"[^\w]+", flags=re.UNICODE)


def slugify(text: str, separator: str = "-", lower: bool = True,
            ascii_only: bool = False, max_length: int = 80,
            keep_dots: bool = False) -> str:
    if text is None:
        return ""
    s = unicodedata.normalize("NFKD", str(text))
    if ascii_only:
        # Drop combining marks then encode/decode to drop anything not in ASCII
        s = "".join(c for c in s if not unicodedata.combining(c))
        s = s.encode("ascii", "ignore").decode("ascii")
    pat = _NONWORD_RE_KEEPDOTS if keep_dots else _NONWORD_RE
    s = pat.sub(separator, s)
    # Collapse runs of the separator
    if separator:
        sep_re = re.compile(re.escape(separator) + r"+")
        s = sep_re.sub(separator, s)
    # Strip leading/trailing separator (and dots if keeping them)
    strip_chars = separator + ("." if keep_dots else "")
    s = s.strip(strip_chars)
    if lower:
        s = s.lower()
    if max_length and len(s) > max_length:
        s = s[:max_length].rstrip(strip_chars)
    return s


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--text")
    p.add_argument("--separator", default="-")
    p.add_argument("--max-length", dest="max_length", type=int, default=80)
    p.add_argument("--lower", action="store_true", default=True)
    p.add_argument("--no-lower", dest="lower", action="store_false")
    p.add_argument("--ascii", action="store_true")
    p.add_argument("--keep-dots", dest="keep_dots", action="store_true")
    p.add_argument("--dedupe", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help:
        print(__doc__)
        return 0

    # Mode dispatch
    if args.text is not None:
        if args.input or args.output:
            print("Error: --text is mutually exclusive with INPUT/OUTPUT batch mode",
                  file=sys.stderr)
            return 2
        s = slugify(args.text, args.separator, args.lower, args.ascii,
                    args.max_length, args.keep_dots)
        print(s)
        # Exit 1 if the input slugified to an empty string (consistent with
        # batch mode, where an all-empty result also returns 1).
        return 0 if s else 1

    if not args.input or not args.output:
        print(__doc__)
        return 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    seen: set = set()
    written: List[str] = []
    scanned = 0
    empty = 0

    for line in iter_lines(in_path):
        scanned += 1
        s = slugify(line, args.separator, args.lower, args.ascii,
                    args.max_length, args.keep_dots)
        if not s:
            empty += 1
            continue
        if args.dedupe:
            if s in seen:
                continue
            seen.add(s)
        written.append(s)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_lines(out_path, written)

    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "scanned": scanned,
        "written": len(written),
        "empty_after_slugify": empty,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            print(f"Slug: {scanned} lines -> {len(written)} slugs "
                  f"({empty} empty) -> {out_path}", file=sys.stderr)
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
