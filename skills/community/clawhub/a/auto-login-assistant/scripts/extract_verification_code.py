#!/usr/bin/env python3
"""Extract likely verification codes from plain text."""

from __future__ import annotations

import argparse
import json
import re
import sys

CODE_PATTERNS = [
    re.compile(r"\b(?P<code>\d{6})\b"),
    re.compile(r"\b(?P<code>\d{4,8})\b"),
    re.compile(r"\b(?P<code>[A-Z0-9]{6,8})\b"),
]

KEYWORD_BONUS = {
    "verification": 2,
    "security code": 2,
    "otp": 2,
    "one-time": 2,
    "code": 1,
    "login": 1,
    "sign in": 1,
}


def score_candidate(text: str, code: str, start: int, end: int) -> int:
    window_start = max(0, start - 80)
    window_end = min(len(text), end + 80)
    window = text[window_start:window_end].lower()
    score = 0
    for keyword, bonus in KEYWORD_BONUS.items():
        if keyword in window:
            score += bonus
    if code.isdigit() and len(code) == 6:
        score += 2
    return score


def extract_candidates(text: str) -> list[dict]:
    seen = set()
    candidates = []
    for pattern in CODE_PATTERNS:
        for match in pattern.finditer(text):
            code = match.group("code")
            if code in seen:
                continue
            seen.add(code)
            candidates.append(
                {
                    "code": code,
                    "score": score_candidate(text, code, match.start(), match.end()),
                }
            )
    candidates.sort(key=lambda item: (-item["score"], item["code"]))
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="Verification text. If omitted, read stdin.")
    parser.add_argument("--top", type=int, default=3, help="Maximum number of candidates to return")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        raise SystemExit("no text provided")

    result = extract_candidates(text)[: max(args.top, 1)]
    json.dump(result, sys.stdout, ensure_ascii=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
