#!/usr/bin/env python3
"""
extract.py - Pull structured items (URLs, emails, phones, IPs, hashtags,
@mentions, hex colors, money) out of any text file.

Usage:
    extract.py INPUT --kind KIND [--output OUT] [--unique] [--sort] [--json]

Kinds:
    url            HTTP / HTTPS URLs
    email          RFC-ish email addresses
    phone          E.164-style and common international forms
    ipv4           dotted-quad IPv4 addresses (basic shape)
    ipv6           IPv6 address candidates
    hashtag        #hashtag tokens
    mention        @mention tokens
    hex-color      #RRGGBB / #RGB color literals
    money          currency-prefixed amounts ($1,234.56, \u20ac99, \u00a35.00, \u20b91200)
    iso-date       YYYY-MM-DD calendar dates (loose)

Options:
    --kind KIND     what to extract (required)
    --output PATH   write to file instead of stdout (extension picks format:
                    .txt one per line, .json a list, .jsonl one object/line)
    --unique        drop duplicates
    --sort          sort the output
    --with-line     prefix each match with the (1-based) line number it came from
    --json          when printing to stdout, emit a JSON list instead of one-per-line
    --quiet         do not print the count summary at the end
    -h, --help      show this help

Exit codes:
    0  one or more matches found
    1  zero matches found
    2  bad arguments / missing input / unsafe path / unknown kind
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List

from _common import iter_lines, safe_path

# Patterns are intentionally pragmatic, not strictly RFC-compliant.
PATTERNS = {
    # URL ends at whitespace or < > " '. We then strip a single trailing
    # sentence-style punctuation character that almost never belongs to the URL
    # (the cleanup happens in the post-processing loop in main()).
    "url": re.compile(r"https?://[^\s<>\"']+"),
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    # Phone heuristic: must be one of three telltale formats so we don't
    # gobble up dates (YYYY-MM-DD), IPs (1.2.3.4), or credit cards (4-4-4-4).
    #   1) international: +<digits> with separators, 8+ digits total
    #   2) parenthesized area code: (XXX) XXX-XXXX
    #   3) classic 3-3-4 with dash/space separators (NOT 4-2-2 like a date)
    "phone": re.compile(
        r"\+\d[\d\s\-().]{6,}\d"
        r"|"
        r"\(\d{3}\)[\s\-]?\d{3}[\s\-]?\d{4}"
        r"|"
        r"\b\d{3}[\s\-]\d{3}[\s\-]\d{4}\b"
    ),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "ipv6": re.compile(
        r"\b(?:[A-Fa-f0-9]{1,4}:){2,7}[A-Fa-f0-9]{1,4}\b"
    ),
    "hashtag": re.compile(r"(?<![\w&])#[A-Za-z][\w]{1,}"),
    "mention": re.compile(r"(?<![\w])@[A-Za-z][\w.\-]{1,}"),
    "hex-color": re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b"),
    "money": re.compile(
        r"(?:[$\u20ac\u00a3\u00a5\u20b9])\s?\d[\d,]*(?:\.\d{1,2})?"
    ),
    "iso-date": re.compile(r"\b\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\b"),
}


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--kind")
    p.add_argument("--output")
    p.add_argument("--unique", action="store_true")
    p.add_argument("--sort", action="store_true")
    p.add_argument("--with-line", dest="with_line", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input:
        print(__doc__)
        return 0 if args.help else 2
    if not args.kind:
        print("Error: --kind is required", file=sys.stderr)
        return 2
    if args.kind not in PATTERNS:
        print(f"Error: unknown --kind '{args.kind}'. Allowed: "
              f"{', '.join(sorted(PATTERNS))}", file=sys.stderr)
        return 2

    try:
        in_path = safe_path(args.input)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        out_ext = out_path.suffix.lower()
        if out_ext not in (".txt", ".json", ".jsonl", ""):
            print(f"Error: unsupported output extension '{out_ext}'. "
                  f"Allowed: .txt, .json, .jsonl", file=sys.stderr)
            return 2
    else:
        out_path = None
        out_ext = ".txt"

    pat = PATTERNS[args.kind]
    matches: List[dict] = []
    plain: List[str] = []
    seen: set = set()

    # Strip a single trailing punctuation char from URLs (common scrape artifact)
    URL_TRAIL = set(".,;:)]}'\"!?")

    for line_no, line in enumerate(iter_lines(in_path), start=1):
        for m in pat.finditer(line):
            value = m.group(0)
            if args.kind == "url" and value and value[-1] in URL_TRAIL:
                value = value.rstrip(".,;:)]}'\"!?")
                if not value:
                    continue
            if args.unique:
                if value in seen:
                    continue
                seen.add(value)
            plain.append(value)
            matches.append({"line": line_no, "match": value})

    if args.sort:
        plain.sort()
        matches.sort(key=lambda r: r["match"])

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_ext == ".json":
            out_path.write_text(json.dumps(plain, indent=2), encoding="utf-8")
        elif out_ext == ".jsonl":
            with out_path.open("w", encoding="utf-8") as f:
                for m in matches:
                    f.write(json.dumps(m, ensure_ascii=False) + "\n")
        else:  # .txt or empty
            with out_path.open("w", encoding="utf-8") as f:
                for m in matches:
                    if args.with_line:
                        f.write(f"{m['line']}\t{m['match']}\n")
                    else:
                        f.write(m['match'] + "\n")
        if not args.quiet:
            print(f"Extract({args.kind}): {len(matches)} match(es) "
                  f"-> {out_path}", file=sys.stderr)
    else:
        if args.as_json:
            print(json.dumps(plain, indent=2))
        else:
            for m in matches:
                if args.with_line:
                    print(f"{m['line']}\t{m['match']}")
                else:
                    print(m['match'])
        if not args.quiet:
            print(f"Extract({args.kind}): {len(matches)} match(es)",
                  file=sys.stderr)

    return 0 if matches else 1


if __name__ == "__main__":
    sys.exit(main())
