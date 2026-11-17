#!/usr/bin/env python3
"""Estimate recurring-context token savings between original and slimmed SKILL.md files."""

import argparse
import math
from pathlib import Path


def stats(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    return {
        "lines": len(text.splitlines()),
        "chars": len(text),
        "cjk": sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", required=True)
    parser.add_argument("--slimmed", required=True)
    parser.add_argument("--tokens-per-char", type=float, default=0.6)
    args = parser.parse_args()
    if args.tokens_per_char <= 0:
        raise SystemExit("--tokens-per-char must be > 0")

    original_path = Path(args.original)
    slimmed_path = Path(args.slimmed)
    if not original_path.exists() or not slimmed_path.exists():
        raise SystemExit("ORIGINAL_OR_SLIMMED_NOT_FOUND")

    original = stats(original_path)
    slimmed = stats(slimmed_path)
    original_tokens = math.ceil(original["chars"] * args.tokens_per_char)
    slimmed_tokens = math.ceil(slimmed["chars"] * args.tokens_per_char)
    saved_tokens = original_tokens - slimmed_tokens
    saved_percent = (saved_tokens / original_tokens * 100.0) if original_tokens else 0.0

    print(f"tokens_per_char={args.tokens_per_char:.2f}")
    print(f"original_lines={original['lines']}")
    print(f"slimmed_lines={slimmed['lines']}")
    print(f"original_chars={original['chars']}")
    print(f"slimmed_chars={slimmed['chars']}")
    print(f"original_estimated_tokens={original_tokens}")
    print(f"slimmed_estimated_tokens={slimmed_tokens}")
    print(f"saved_estimated_tokens={saved_tokens}")
    print(f"saved_percent={saved_percent:.1f}")
    print("note=Estimate is not a billing promise; use --tokens-per-char 0.6 and 0.8 for a range.")


if __name__ == "__main__":
    main()
