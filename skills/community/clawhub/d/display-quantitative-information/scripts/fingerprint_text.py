#!/usr/bin/env python3
"""Check a draft visualization critique for repetitive stock language."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

STOCK_PHRASES = [
    "show the data",
    "small multiples",
    "chartjunk",
    "data-ink",
    "direct labels",
    "zero baseline",
    "graphical integrity",
    "visual clutter",
    "make comparison easier",
    "avoid distortion",
    "clearer and more honest",
]


def read_text(path: Optional[str]) -> str:
    if not path or path == "-":
        return sys.stdin.read()
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"Error: input file not found: {path}")


def sentence_starts(text: str) -> Counter[str]:
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    starts: Counter[str] = Counter()
    for sent in sentences:
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", sent.lower())
        if len(words) >= 2:
            starts[" ".join(words[:2])] += 1
    return starts


def analyze(text: str) -> Dict[str, Any]:
    lower = text.lower()
    phrase_counts = {phrase: len(re.findall(re.escape(phrase), lower)) for phrase in STOCK_PHRASES}
    phrase_counts = {k: v for k, v in phrase_counts.items() if v > 1}
    starts = {k: v for k, v in sentence_starts(text).items() if v > 1}
    warnings: List[str] = []
    if phrase_counts:
        warnings.append("Repeated stock visualization terms detected; keep them only where they diagnose a real issue.")
    if starts:
        warnings.append("Repeated sentence starts detected; vary opener shapes across critique items.")
    return {"warnings": warnings, "repeated_stock_phrases": phrase_counts, "repeated_sentence_starts": starts, "character_count": len(text)}


def print_markdown(result: Dict[str, Any]) -> None:
    if result["warnings"]:
        print("Fingerprint warnings:")
        for warning in result["warnings"]:
            print(f"- {warning}")
    else:
        print("No major repetition warnings.")
    if result["repeated_stock_phrases"]:
        print("\nStock phrase counts:")
        for phrase, count in sorted(result["repeated_stock_phrases"].items()):
            print(f"- {phrase}: {count}")
    if result["repeated_sentence_starts"]:
        print("\nRepeated sentence starts:")
        for start, count in sorted(result["repeated_sentence_starts"].items()):
            print(f"- {start}: {count}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check a draft visualization critique for repetitive stock language.")
    parser.add_argument("--input", help="Text or Markdown file. Omit or use - for stdin.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    result = analyze(read_text(args.input))
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
