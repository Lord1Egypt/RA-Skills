#!/usr/bin/env python3
"""
wordcount.py - Word / character / line / sentence statistics for a text file.

By default prints a one-line summary. Use --top N to also print the top-N
most frequent words.

Usage:
    wordcount.py INPUT [--top N] [--stopwords FILE] [--min-length N]
                       [--ignore-case] [--json]

Options:
    --top N            also print the top-N most frequent words (0 = skip)
    --stopwords PATH   read a stopword list (one word per line) and drop
                       those words before counting
    --min-length N     drop words shorter than N characters
    --ignore-case      lowercase before counting (default: case-sensitive)
    --regex PATTERN    custom word-boundary regex (default: r"[A-Za-z']+")
    --json             emit the stats as a JSON object on stdout
    -h, --help         show this help

Exit codes:
    0  success (at least one word found)
    1  empty input (zero words)
    2  bad arguments / unsafe path / missing file / bad stopwords file
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from _common import read_text, safe_path

SENT_RE = re.compile(r"[.!?]+(?:\s|$)")
DEFAULT_WORD_RE = r"[A-Za-z']+"


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("--top", type=int, default=0)
    p.add_argument("--stopwords")
    p.add_argument("--min-length", dest="min_length", type=int, default=1)
    p.add_argument("--ignore-case", dest="ignore_case", action="store_true")
    p.add_argument("--regex", default=DEFAULT_WORD_RE)
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
    try:
        word_re = re.compile(args.regex)
    except re.error as e:
        print(f"Error: bad --regex: {e}", file=sys.stderr)
        return 2

    stopwords: set = set()
    if args.stopwords:
        try:
            sw_path = safe_path(args.stopwords)
            if not sw_path.is_file():
                print(f"Error: stopwords file not found: {sw_path}",
                      file=sys.stderr)
                return 2
            for line in sw_path.read_text(encoding="utf-8").splitlines():
                w = line.strip()
                if w and not w.startswith("#"):
                    stopwords.add(w.casefold() if args.ignore_case else w)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

    text = read_text(in_path)
    n_chars = len(text)
    n_chars_nospace = sum(1 for c in text if not c.isspace())
    n_lines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
    n_sentences = len(SENT_RE.findall(text)) or (1 if text.strip() else 0)
    n_bytes = in_path.stat().st_size

    counter: Counter = Counter()
    n_words = 0
    for tok in word_re.findall(text):
        if args.ignore_case:
            tok = tok.casefold()
        if len(tok) < args.min_length:
            continue
        if tok in stopwords:
            continue
        counter[tok] += 1
        n_words += 1

    top_n = counter.most_common(args.top) if args.top > 0 else []
    n_unique = len(counter)

    summary = {
        "input": str(in_path),
        "bytes": n_bytes,
        "chars": n_chars,
        "chars_nospace": n_chars_nospace,
        "lines": n_lines,
        "sentences": n_sentences,
        "words": n_words,
        "unique_words": n_unique,
        "top": [{"word": w, "count": c} for w, c in top_n],
    }

    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"{'Bytes':<18} {n_bytes:>10}")
        print(f"{'Chars':<18} {n_chars:>10}")
        print(f"{'Chars (no space)':<18} {n_chars_nospace:>10}")
        print(f"{'Lines':<18} {n_lines:>10}")
        print(f"{'Sentences':<18} {n_sentences:>10}")
        print(f"{'Words':<18} {n_words:>10}")
        print(f"{'Unique words':<18} {n_unique:>10}")
        if top_n:
            print()
            print(f"Top {len(top_n)} word(s):")
            width = max(len(w) for w, _ in top_n) + 2
            for w, c in top_n:
                print(f"  {w:<{width}} {c}")

    return 0 if n_words > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
