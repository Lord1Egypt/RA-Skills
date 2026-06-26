#!/usr/bin/env python3
"""
normalize.py - Clean up messy text: whitespace, line endings, smart quotes,
zero-width chars, accidental BOM, mixed tabs/spaces, and case.

Usage:
    normalize.py INPUT OUTPUT [transforms...]

Transforms (apply in the order given on the command line):
    --trim                  strip leading/trailing whitespace per line
    --collapse-spaces       collapse runs of spaces/tabs into one space per line
    --strip-blank           remove empty / whitespace-only lines
    --to-unix               convert CRLF / CR endings to LF
    --to-crlf               convert all endings to CRLF
    --dehyphenate           join words split across lines with a trailing hyphen
                            (common in OCR / PDF text)
    --unsmart               turn typographic punctuation back into ASCII
                            (smart quotes, dashes, ellipsis)
    --strip-bom             remove a leading UTF-8 byte-order mark
    --strip-zwsp            remove zero-width spaces, joiners, and BOMs anywhere
    --tabs-to-spaces N      replace each leading tab with N spaces (default 4)
    --spaces-to-tabs N      replace runs of N leading spaces with one tab
    --lower                 lowercase everything
    --upper                 uppercase everything
    --title                 title-case each line
    --normalize-unicode FORM
                            apply unicodedata.normalize(FORM, text)
                            (NFC / NFD / NFKC / NFKD)

Options:
    --json                  emit a JSON summary on stderr
    --quiet                 suppress the summary
    -h, --help              show this help

Exit codes:
    0  success
    2  bad arguments / unsafe path / missing file / unsupported transform
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Callable, List, Tuple

from _common import read_text, safe_path, write_text


SMART_MAP = {
    "\u2018": "'", "\u2019": "'", "\u201A": "'", "\u201B": "'",
    "\u201C": '"', "\u201D": '"', "\u201E": '"', "\u201F": '"',
    "\u2013": "-", "\u2014": "-", "\u2015": "-",
    "\u2026": "...",
    "\u00B7": "*", "\u2022": "*",
    "\u00A0": " ",  # nbsp -> regular space
}
ZWSP_RE = re.compile(r"[\u200B\u200C\u200D\u2060\uFEFF]")
DEHY_RE = re.compile(r"(\w+)-\n(\w+)")


def transform_trim(text: str) -> str:
    return "\n".join(line.strip() for line in text.splitlines()) + ("\n" if text.endswith("\n") else "")


def transform_collapse(text: str) -> str:
    out_lines = []
    pat = re.compile(r"[ \t]+")
    for line in text.splitlines():
        out_lines.append(pat.sub(" ", line))
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def transform_strip_blank(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if line.strip()) + \
           ("\n" if text.endswith("\n") else "")


def transform_to_unix(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def transform_to_crlf(text: str) -> str:
    return transform_to_unix(text).replace("\n", "\r\n")


def transform_dehyphenate(text: str) -> str:
    return DEHY_RE.sub(r"\1\2", text)


def transform_unsmart(text: str) -> str:
    out = []
    for ch in text:
        out.append(SMART_MAP.get(ch, ch))
    return "".join(out)


def transform_strip_bom(text: str) -> str:
    if text.startswith("\ufeff"):
        return text[1:]
    return text


def transform_strip_zwsp(text: str) -> str:
    return ZWSP_RE.sub("", text)


def transform_tabs_to_spaces(n: int) -> Callable[[str], str]:
    if n <= 0:
        raise ValueError("--tabs-to-spaces N must be > 0")
    repl = " " * n

    def fn(text: str) -> str:
        out = []
        for line in text.splitlines():
            # Only replace LEADING tabs
            stripped = line.lstrip("\t")
            n_tabs = len(line) - len(stripped)
            out.append(repl * n_tabs + stripped)
        return "\n".join(out) + ("\n" if text.endswith("\n") else "")
    return fn


def transform_spaces_to_tabs(n: int) -> Callable[[str], str]:
    if n <= 0:
        raise ValueError("--spaces-to-tabs N must be > 0")
    chunk = " " * n
    pat = re.compile(r"^(?:" + chunk + ")+")

    def fn(text: str) -> str:
        out = []
        for line in text.splitlines():
            m = pat.match(line)
            if m:
                count = len(m.group(0)) // n
                out.append("\t" * count + line[m.end():])
            else:
                out.append(line)
        return "\n".join(out) + ("\n" if text.endswith("\n") else "")
    return fn


def transform_lower(text: str) -> str: return text.lower()
def transform_upper(text: str) -> str: return text.upper()


def transform_title(text: str) -> str:
    return "\n".join(line.title() for line in text.splitlines()) + \
           ("\n" if text.endswith("\n") else "")


def transform_normalize_unicode(form: str) -> Callable[[str], str]:
    if form not in ("NFC", "NFD", "NFKC", "NFKD"):
        raise ValueError(f"--normalize-unicode requires NFC/NFD/NFKC/NFKD, got {form!r}")
    return lambda text: unicodedata.normalize(form, text)


def build_pipeline(argv: List[str]) -> List[Tuple[str, Callable[[str], str]]]:
    """Walk the argv to build an ordered list of (name, fn) pairs."""
    pipeline: List[Tuple[str, Callable[[str], str]]] = []
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok == "--trim":
            pipeline.append((tok, transform_trim))
        elif tok == "--collapse-spaces":
            pipeline.append((tok, transform_collapse))
        elif tok == "--strip-blank":
            pipeline.append((tok, transform_strip_blank))
        elif tok == "--to-unix":
            pipeline.append((tok, transform_to_unix))
        elif tok == "--to-crlf":
            pipeline.append((tok, transform_to_crlf))
        elif tok == "--dehyphenate":
            pipeline.append((tok, transform_dehyphenate))
        elif tok == "--unsmart":
            pipeline.append((tok, transform_unsmart))
        elif tok == "--strip-bom":
            pipeline.append((tok, transform_strip_bom))
        elif tok == "--strip-zwsp":
            pipeline.append((tok, transform_strip_zwsp))
        elif tok == "--tabs-to-spaces":
            i += 1
            pipeline.append((tok, transform_tabs_to_spaces(int(argv[i]))))
        elif tok == "--spaces-to-tabs":
            i += 1
            pipeline.append((tok, transform_spaces_to_tabs(int(argv[i]))))
        elif tok == "--lower":
            pipeline.append((tok, transform_lower))
        elif tok == "--upper":
            pipeline.append((tok, transform_upper))
        elif tok == "--title":
            pipeline.append((tok, transform_title))
        elif tok == "--normalize-unicode":
            i += 1
            pipeline.append((tok, transform_normalize_unicode(argv[i].upper())))
        else:
            raise ValueError(f"unknown transform: {tok!r}")
        i += 1
    return pipeline


def main() -> int:
    # Use a permissive argparse just to grab in/out + flags; everything
    # else is parsed manually so we preserve user order.
    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if len(sys.argv) < 3:
        print("Error: usage: normalize.py INPUT OUTPUT [transforms...]",
              file=sys.stderr)
        return 2

    args = list(sys.argv[1:])
    in_arg = args.pop(0)
    out_arg = args.pop(0)

    # Pop --json / --quiet wherever they appear
    as_json = False
    quiet = False
    rest: List[str] = []
    for a in args:
        if a == "--json":
            as_json = True
        elif a == "--quiet":
            quiet = True
        else:
            rest.append(a)

    try:
        in_path = safe_path(in_arg)
        out_path = safe_path(out_arg)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    try:
        pipeline = build_pipeline(rest)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    text = read_text(in_path)
    original_len = len(text)
    applied: List[str] = []
    for name, fn in pipeline:
        text = fn(text)
        applied.append(name)
    write_text(out_path, text)

    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "original_chars": original_len,
        "final_chars": len(text),
        "delta_chars": len(text) - original_len,
        "transforms": applied,
    }
    if not quiet:
        if as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            print(f"Normalize: {original_len} -> {len(text)} chars "
                  f"({len(applied)} transform(s)) -> {out_path}",
                  file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
