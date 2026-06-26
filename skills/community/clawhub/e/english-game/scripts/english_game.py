#!/usr/bin/env python3
from __future__ import annotations

import argparse
import string
from typing import List

ABSENT = "⬛"
PRESENT = "🟨"
CORRECT = "🟩"


def normalize_word(text: str) -> str:
    value = (text or "").strip().lower()
    if not value:
        raise ValueError("word cannot be empty")
    if any(ch not in string.ascii_lowercase for ch in value):
        raise ValueError("word must contain only english letters a-z")
    return value


def score_guess(target_word: str, guess_word: str) -> List[str]:
    target = list(normalize_word(target_word))
    guess = list(normalize_word(guess_word))
    if len(target) != len(guess):
        raise ValueError("guess length must match target length")

    result = [ABSENT] * len(guess)
    remaining = {}

    for idx, (g, t) in enumerate(zip(guess, target)):
        if g == t:
            result[idx] = CORRECT
        else:
            remaining[t] = remaining.get(t, 0) + 1

    for idx, g in enumerate(guess):
        if result[idx] == CORRECT:
            continue
        if remaining.get(g, 0) > 0:
            result[idx] = PRESENT
            remaining[g] -= 1

    return result


def format_score_output(target_word: str, guess_word: str) -> str:
    target = normalize_word(target_word)
    guess = normalize_word(guess_word)
    row = "".join(score_guess(target, guess))
    solved = str(target == guess).lower()
    return f"guess: {guess.upper()}\nscore: {row}\nsolved: {solved}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Helpers for the Feishu English Game")
    sub = parser.add_subparsers(dest="command", required=True)

    vocab_score = sub.add_parser("vocab-score", help="Score one Wordle-style guess")
    vocab_score.add_argument("--target-word", required=True)
    vocab_score.add_argument("--guess", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "vocab-score":
        print(format_score_output(args.target_word, args.guess))
        return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
