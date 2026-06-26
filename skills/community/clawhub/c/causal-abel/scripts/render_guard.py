#!/usr/bin/env python
"""Guard visible Abel prose against raw graph identifiers."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NODE_ID_RE = re.compile(r"\b[A-Z0-9][A-Z0-9-]{0,11}\.(?:price|volume)\b")
SIGNED_DECIMAL_RE = re.compile(r"(?<!\w)[+-](?:\d+\.\d{3,}|0\.\d{3,})\b")


def _read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def _iter_matches(pattern: re.Pattern[str], text: str, rule: str) -> list[tuple[str, str, int, int]]:
    out: list[tuple[str, str, int, int]] = []
    for match in pattern.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        col = match.start() - text.rfind("\n", 0, match.start())
        out.append((rule, match.group(0), line, col))
    return out


def _forbidden_token_re(token: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9-]){re.escape(token)}(?![A-Za-z0-9-])")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("direct_graph", "proxy_routed"), required=True)
    parser.add_argument("--text-file", help="Visible-layer draft to check. Reads stdin if omitted.")
    parser.add_argument(
        "--forbid-token",
        action="append",
        default=[],
        help="Exact raw ticker/token that must not appear in visible prose.",
    )
    args = parser.parse_args()

    text = _read_text(args.text_file)
    violations: list[tuple[str, str, int, int]] = []
    violations.extend(_iter_matches(NODE_ID_RE, text, "raw_node_id"))
    violations.extend(_iter_matches(SIGNED_DECIMAL_RE, text, "signed_prediction_decimal"))

    if args.mode == "proxy_routed":
        for token in args.forbid_token:
            violations.extend(
                _iter_matches(_forbidden_token_re(token), text, f"raw_forbidden_token:{token}")
            )

    if not violations:
        print("PASS")
        return 0

    print("FAIL")
    for rule, snippet, line, col in violations:
        print(f"{rule}\tline {line}\tcol {col}\t{snippet}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
