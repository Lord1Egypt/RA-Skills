#!/usr/bin/env python3
"""
redact.py - Anonymize text by replacing PII-like patterns with placeholder
tokens. Useful before sharing logs, transcripts, or examples publicly.

Usage:
    redact.py INPUT OUTPUT [--kinds K1,K2,...] [options]

Kinds (default: all):
    email, phone, ipv4, ipv6, url, credit-card, ssn-us, uuid, hex-token,
    aws-access-key, jwt

Options:
    --kinds K[,K2,...]    only redact these kinds (default: all)
    --token-template STR  Python format string for the placeholder. Default:
                          "[REDACTED_{kind}_{i}]". Available fields:
                          {kind}, {i} (1-based index per kind), {value}.
    --keep-counts         instead of {i}, increment per OCCURRENCE
                          (the same email always gets the same number)
    --preserve-length     pad/truncate the placeholder to match the original
                          length so positions are preserved (best-effort)
    --json                emit machine-readable summary
    --quiet               suppress text summary on stderr
    -h, --help            show this help

Exit codes:
    0  one or more redactions made
    1  zero matches found
    2  bad arguments / missing file / unsafe path / unknown kind
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from _common import read_text, safe_path, write_text

PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    # Phone: tightened to avoid grabbing IPs (1.2.3.4), dates (YYYY-MM-DD),
    # and credit cards (4-4-4-4). Three accepted shapes:
    #   1) international: +<digits with separators>
    #   2) US-style parenthesized area code
    #   3) classic 3-3-4 with dash/space separators
    "phone": re.compile(
        r"\+\d[\d\s\-().]{6,}\d"
        r"|"
        r"\(\d{3}\)[\s\-]?\d{3}[\s\-]?\d{4}"
        r"|"
        r"\b\d{3}[\s\-]\d{3}[\s\-]\d{4}\b"
    ),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "ipv6": re.compile(r"\b(?:[A-Fa-f0-9]{1,4}:){2,7}[A-Fa-f0-9]{1,4}\b"),
    "url": re.compile(r"https?://[^\s<>\"']+"),
    # Visa / MC / Amex / Discover-ish: 13-19 digits with optional separators
    "credit-card": re.compile(r"\b(?:\d[ \-]*){13,19}\b"),
    "ssn-us": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "uuid": re.compile(
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
    ),
    "hex-token": re.compile(r"\b[A-Fa-f0-9]{32,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b"),
}


def luhn_valid(num: str) -> bool:
    """Simple Luhn check so 'credit-card' regex hits fewer false positives."""
    digits = [int(c) for c in num if c.isdigit()]
    if not (13 <= len(digits) <= 19):
        return False
    s = 0
    parity = (len(digits) - 2) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return s % 10 == 0


def redact(text: str, kinds: List[str], template: str,
           keep_counts: bool, preserve_length: bool) -> Tuple[str, Dict[str, int], Dict[str, Dict[str, str]]]:
    """Return (redacted_text, counts_per_kind, mapping_per_kind).

    mapping_per_kind[kind] -> dict mapping original value to placeholder string.
    """
    counts: Dict[str, int] = {k: 0 for k in kinds}
    mappings: Dict[str, Dict[str, str]] = {k: {} for k in kinds}

    # Apply in a deterministic order, longest-pattern-first to avoid
    # truncating a JWT by matching the embedded hex first.
    order = sorted(kinds, key=lambda k: -len(PATTERNS[k].pattern))

    for kind in order:
        pat = PATTERNS[kind]
        per_kind_index = {0: 0}

        def replace(match: re.Match) -> str:
            value = match.group(0)
            if kind == "credit-card" and not luhn_valid(value):
                return value  # ignore non-Luhn-valid numbers
            mapping = mappings[kind]
            if keep_counts and value in mapping:
                return mapping[value]
            per_kind_index[0] += 1
            i = per_kind_index[0] if not keep_counts else len(mapping) + 1
            placeholder = template.format(kind=kind, i=i, value=value)
            if preserve_length:
                if len(placeholder) < len(value):
                    placeholder = placeholder + "*" * (len(value) - len(placeholder))
                else:
                    placeholder = placeholder[: len(value)]
            counts[kind] += 1
            if keep_counts:
                mapping[value] = placeholder
            else:
                mapping[value] = placeholder
            return placeholder

        text = pat.sub(replace, text)

    return text, counts, mappings


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--kinds")
    p.add_argument("--token-template", dest="template",
                   default="[REDACTED_{kind}_{i}]")
    p.add_argument("--keep-counts", dest="keep_counts", action="store_true")
    p.add_argument("--preserve-length", dest="preserve_length", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    kinds = [k.strip() for k in args.kinds.split(",")] if args.kinds \
            else list(PATTERNS.keys())
    bad = [k for k in kinds if k not in PATTERNS]
    if bad:
        print(f"Error: unknown kinds: {','.join(bad)}. Allowed: "
              f"{', '.join(sorted(PATTERNS))}", file=sys.stderr)
        return 2

    # Validate template by trying it once
    try:
        _ = args.template.format(kind="test", i=1, value="x")
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error: bad --token-template: {e}", file=sys.stderr)
        return 2

    text = read_text(in_path)
    redacted, counts, _mappings = redact(
        text, kinds, args.template, args.keep_counts, args.preserve_length
    )
    write_text(out_path, redacted)

    total = sum(counts.values())
    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "kinds": kinds,
        "counts": counts,
        "total_redactions": total,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            parts = [f"{k}={c}" for k, c in counts.items() if c]
            print(f"Redact: {total} redaction(s) "
                  f"[{', '.join(parts) if parts else 'none'}] -> {out_path}",
                  file=sys.stderr)
    return 0 if total > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
