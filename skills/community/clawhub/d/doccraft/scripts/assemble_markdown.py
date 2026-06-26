#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge markdown chapter files into one ordered document."
    )
    parser.add_argument("inputs", nargs="+", help="Markdown files or directories")
    parser.add_argument("--out", help="Optional output markdown path")
    parser.add_argument("--title", help="Optional document title")
    return parser.parse_args()


def collect_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
            continue
        if path.is_dir():
            files.extend(sorted(path.glob("*.md"), key=lambda item: item.name.lower()))
    return sorted(files, key=lambda item: item.name.lower())


def read_blocks(files: list[Path]) -> list[str]:
    blocks: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8").strip()
        if text:
            blocks.append(text)
    return blocks


def main() -> int:
    args = parse_args()
    files = collect_files(args.inputs)
    blocks = read_blocks(files)
    parts: list[str] = []
    if args.title:
        parts.append(f"# {args.title}")
    parts.extend(blocks)
    merged = "\n\n".join(parts).rstrip() + "\n"
    if args.out:
        Path(args.out).write_text(merged, encoding="utf-8")
    else:
        print(merged, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
