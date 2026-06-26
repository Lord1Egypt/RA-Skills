#!/usr/bin/env python3
"""Single-entry Baidu research command for agents."""

from __future__ import annotations

import sys

import adaptive_search
import lookup


def split_mode(argv: list[str]) -> tuple[str | None, list[str]]:
    cleaned: list[str] = []
    mode: str | None = None
    skip_next = False
    for index, item in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        if item == "--mode" and index + 1 < len(argv):
            mode = argv[index + 1]
            skip_next = True
            continue
        if item.startswith("--mode="):
            mode = item.split("=", 1)[1]
            continue
        cleaned.append(item)
    return mode, cleaned


def main() -> int:
    argv = sys.argv[1:]
    mode, argv_without_mode = split_mode(argv)
    if mode == "lookup":
        sys.argv = ["lookup.py", *argv_without_mode]
        return lookup.main()
    if argv and not argv[0].startswith("-"):
        argv = ["--topic", argv[0], *argv[1:]]
    sys.argv = ["adaptive_search.py", *argv]
    return adaptive_search.main()


if __name__ == "__main__":
    raise SystemExit(main())
