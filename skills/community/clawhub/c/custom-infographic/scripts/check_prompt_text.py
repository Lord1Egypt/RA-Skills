#!/usr/bin/env python3
"""Pre-flight no-duplicate gate for a custom-infographic prompt.

The invariant this enforces:

  * Every renderable string in an assembled prompt is delimited by BACKTICKS.
  * Each backticked string appears EXACTLY ONCE in the whole prompt file.
  * Any meta-reference to a string (e.g. in a constraint sentence) is written
    as PLAIN TEXT, without backticks — so backticked spans are exactly the
    renderable set, nothing more.
  * The prompt contains exactly ONE label enumeration (the "CRITICAL: Text
    Accuracy" block). A second list at the end of the prompt, or repeated cell
    headings in the layout/style guidance, is what makes image models render a
    string twice.

Run this before generate_image.py. A non-zero exit means DO NOT GENERATE.

Usage:
    python check_prompt_text.py prompts/infographic.md
    python check_prompt_text.py prompts/infographic.md --strings labels.txt

`--strings FILE` additionally asserts every expected string is present (as a
backticked span) exactly once — use it to catch a dropped chip as well as a
duplicated one.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

BACKTICKED = re.compile(r"`([^`\n]+)`")

# A second enumeration section is forbidden; these markers indicate one.
FORBIDDEN_MARKERS = (
    "Text labels (in",
    "Text labels:",
    "TEXT_LABELS",
)

# Backticked spans that are symbols/instructions rather than labels, and may
# legitimately repeat. Kept tiny on purpose — add only true syntax, never a label.
DEFAULT_ALLOWED = {"`"}  # a lone backtick mention, if any


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt", help="path to the assembled prompt file")
    ap.add_argument("--strings", help="optional file of expected strings, one per line")
    ap.add_argument("--allow", action="append", default=[], help="span allowed to repeat (repeatable)")
    args = ap.parse_args()

    try:
        text = open(args.prompt, encoding="utf-8").read()
    except OSError as exc:
        print(f"FAIL: cannot read prompt: {exc}")
        return 2

    spans = BACKTICKED.findall(text)
    counts = Counter(spans)
    allowed = set(DEFAULT_ALLOWED) | set(args.allow)

    problems: list[str] = []

    for span, n in sorted(counts.items()):
        if n > 1 and span not in allowed:
            problems.append(f"renderable string appears {n}x (must be exactly once): {span!r}")

    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            problems.append(f"second label enumeration present ({marker!r}) — the prompt must enumerate strings exactly once")

    if args.strings:
        try:
            expected = [ln.strip() for ln in open(args.strings, encoding="utf-8") if ln.strip()]
        except OSError as exc:
            print(f"FAIL: cannot read strings file: {exc}")
            return 2
        for s in expected:
            n = counts.get(s, 0)
            if n == 0:
                problems.append(f"expected string missing (or not backticked): {s!r}")
            elif n > 1 and s not in allowed:
                problems.append(f"expected string listed {n}x: {s!r}")

    if problems:
        print("FAIL: prompt duplicates renderable text — do not generate")
        for p in problems:
            print("  -", p)
        return 1

    print(f"OK: {len(spans)} renderable strings, each appears exactly once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
