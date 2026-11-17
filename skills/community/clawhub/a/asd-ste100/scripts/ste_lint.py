#!/usr/bin/env python3
"""Deterministic ASD-STE100 checks for English instruction text.

Checks only what a machine can check:
  - sentence length over 25 words (error) and over 20 (warning)
  - semicolons outside code
  - common non-approved words, with a replacement
  - advisory passive voice and phrasal verbs

It does not check meaning, one-instruction-per-sentence, synonym drift,
or whether a rewrite preserved a condition. Those need a reader.

Usage:
    python3 ste_lint.py PATH...
    python3 ste_lint.py --check PATH...
    python3 ste_lint.py --json PATH...
    python3 ste_lint.py --stats PATH...
    python3 ste_lint.py --limit 25 PATH...

Exit code is 1 with --check when at least one error is found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BANNED = {
    "ensure": "make sure",
    "utilize": "use",
    "utilise": "use",
    "leverage": "use",
    "facilitate": "help",
    "commence": "start",
    "initiate": "start",
    "terminate": "stop",
    "prior to": "before",
    "in order to": "to",
    "perform": "do",
    "conduct": "do",
    "execute": "do",
    "demonstrate": "show",
    "additionally": "also",
    "furthermore": "also",
    "assist": "help",
    "attempt": "try",
    "sufficient": "enough",
    "purchase": "buy",
    "obtain": "get",
    "provide": "give",
    "require": "need",
}

PHRASAL = [
    "spin up",
    "reach out",
    "kick off",
    "carry out",
    "set up",
    "find out",
    "figure out",
    "roll out",
    "touch base",
]

PASSIVE = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+"
    r"([a-z]+ed|done|made|set|put|shown|written|built|sent|kept|held|found|given|taken|run)\b",
    re.IGNORECASE,
)

WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\u2019\-./]*")
ABBREV = re.compile(r"\b(e\.g|i\.e|etc|vs|no|fig|approx|cf)\.$", re.IGNORECASE)


def clean(text: str) -> str:
    """Remove markup that is not prose, keeping one token per code span or URL."""
    text = re.sub(r"<!--.*?-->", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`[^`]*`", "CODE", text)
    text = re.sub(r"https?://\S+", "URL", text)
    text = text.replace("**", "").replace("__", "")
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)]|>)\s+", "", text)
    return text.strip()


def sentences(line: str) -> list[str]:
    """Split a line into sentences, keeping abbreviations intact."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])", line)
    out: list[str] = []
    buffer = ""
    for part in parts:
        buffer = f"{buffer} {part}".strip() if buffer else part
        if ABBREV.search(buffer):
            continue
        out.append(buffer)
        buffer = ""
    if buffer:
        out.append(buffer)
    return out


def iter_lines(path: Path):
    """Yield (line_number, cleaned_text) for prose lines outside fences and frontmatter."""
    in_fence = False
    in_frontmatter = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if number == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("|"):
            continue
        yield number, clean(raw)


def iter_sentences(path: Path):
    """Yield (line_number, sentence, words) for each sentence in prose lines."""
    for number, text in iter_lines(path):
        if not text:
            continue
        for sentence in sentences(text):
            yield number, sentence, WORD.findall(sentence)


def lint(path: Path, error_limit: int, warn_limit: int) -> list[dict]:
    findings: list[dict] = []
    for number, sentence, words in iter_sentences(path):
        if len(words) > error_limit:
            findings.append(
                {
                    "file": str(path),
                    "line": number,
                    "level": "error",
                    "rule": "5.1/6.3",
                    "message": f"{len(words)} words (limit {error_limit}): {sentence}",
                }
            )
        elif len(words) > warn_limit:
            findings.append(
                {
                    "file": str(path),
                    "line": number,
                    "level": "warning",
                    "rule": "5.1/6.3",
                    "message": f"{len(words)} words (warning above {warn_limit}): {sentence}",
                }
            )

        if ";" in sentence:
            findings.append(
                {
                    "file": str(path),
                    "line": number,
                    "level": "error",
                    "rule": "8.1",
                    "message": f"semicolon: {sentence}",
                }
            )

        lower = sentence.lower()
        for bad, good in BANNED.items():
            pattern = r"\b" + re.escape(bad) + r"\b" if " " not in bad else re.escape(bad)
            if re.search(pattern, lower):
                findings.append(
                    {
                        "file": str(path),
                        "line": number,
                        "level": "warning",
                        "rule": "1.1",
                        "message": f"'{bad}' -> '{good}': {sentence}",
                    }
                )

        match = PASSIVE.search(sentence)
        if match:
            findings.append(
                {
                    "file": str(path),
                    "line": number,
                    "level": "warning",
                    "rule": "3.6",
                    "message": f"possible passive voice ('{match.group(0)}'): {sentence}",
                }
            )

        for phrase in PHRASAL:
            if phrase in lower:
                findings.append(
                    {
                        "file": str(path),
                        "line": number,
                        "level": "warning",
                        "rule": "9.3",
                        "message": f"phrasal verb '{phrase}': {sentence}",
                    }
                )
    return findings


def stats(path: Path, error_limit: int, warn_limit: int) -> dict:
    """Count sentences, length breaches, semicolons, errors, and warnings."""
    total = over_warn = over_error = semicolons = 0
    for _number, sentence, words in iter_sentences(path):
        total += 1
        if len(words) > warn_limit:
            over_warn += 1
        if len(words) > error_limit:
            over_error += 1
        if ";" in sentence:
            semicolons += 1
    findings = lint(path, error_limit, warn_limit)
    errors = sum(1 for f in findings if f["level"] == "error")
    return {
        "file": str(path),
        "sentences": total,
        "over_20": over_warn,
        "over_25": over_error,
        "semicolons": semicolons,
        "errors": errors,
        "warnings": len(findings) - errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic ASD-STE100 checks.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--limit", type=int, default=25, help="error limit (default 25)")
    parser.add_argument(
        "--warn", type=int, default=20, help="warning limit (default 20)"
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--stats", action="store_true", help="per-file summary table")
    parser.add_argument("--check", action="store_true", help="exit 1 on errors")
    args = parser.parse_args()

    missing = [str(p) for p in args.paths if not p.is_file()]
    if missing:
        print(f"not a file: {', '.join(missing)}", file=sys.stderr)
        return 2

    all_findings: list[dict] = []
    for path in args.paths:
        all_findings.extend(lint(path, args.limit, args.warn))

    if args.stats and not args.json:
        header = (
            f"{'file':<40}{'sentences':>10}{'over20':>8}"
            f"{'over25':>8}{'semicolons':>12}{'errors':>8}{'warnings':>10}"
        )
        print(header)
        for path in args.paths:
            row = stats(path, args.limit, args.warn)
            print(
                f"{row['file']:<40}{row['sentences']:>10}{row['over_20']:>8}"
                f"{row['over_25']:>8}{row['semicolons']:>12}"
                f"{row['errors']:>8}{row['warnings']:>10}"
            )
    elif args.json:
        print(json.dumps(all_findings, indent=2))
    else:
        for finding in all_findings:
            print(
                f"{finding['file']}:{finding['line']}: "
                f"{finding['level'].upper()} [{finding['rule']}] {finding['message']}"
            )
        errors = sum(1 for f in all_findings if f["level"] == "error")
        warnings = len(all_findings) - errors
        print(f"\n{errors} error(s), {warnings} warning(s), {len(all_findings)} total")

    if args.check:
        return 1 if any(f["level"] == "error" for f in all_findings) else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
