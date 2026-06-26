#!/usr/bin/env python3
"""
Small wrapper around Calibre's ebook-convert CLI.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


COMMON_MACOS_PATHS = [
    "/Applications/calibre.app/Contents/MacOS/ebook-convert",
    "/Applications/Calibre.app/Contents/MacOS/ebook-convert",
]


def find_ebook_convert() -> str | None:
    binary = shutil.which("ebook-convert")
    if binary:
        return binary

    for candidate in COMMON_MACOS_PATHS:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert ebook/document files using Calibre's ebook-convert.",
    )
    parser.add_argument("input_file", help="Source file path.")
    parser.add_argument("output_file", help="Target file path with desired extension.")
    parser.add_argument(
        "extra_args",
        nargs=argparse.REMAINDER,
        help="Additional ebook-convert arguments. Prefix them with --.",
    )
    return parser


def normalize_extra_args(extra_args: list[str]) -> list[str]:
    if extra_args[:1] == ["--"]:
        return extra_args[1:]
    return extra_args


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input_file).expanduser().resolve()
    output_path = Path(args.output_file).expanduser().resolve()

    if not input_path.is_file():
        print(f"[calibre-convert] Input file not found: {input_path}", file=sys.stderr)
        return 2

    output_dir = output_path.parent
    if not output_dir.exists():
        print(f"[calibre-convert] Output directory does not exist: {output_dir}", file=sys.stderr)
        return 2

    converter = find_ebook_convert()
    if not converter:
        print(
            "[calibre-convert] Could not find `ebook-convert`. Install Calibre or add it to PATH.",
            file=sys.stderr,
        )
        return 3

    command = [converter, str(input_path), str(output_path), *normalize_extra_args(args.extra_args)]

    try:
        completed = subprocess.run(command, check=False)
    except OSError as exc:
        print(f"[calibre-convert] Failed to start converter: {exc}", file=sys.stderr)
        return 4

    if completed.returncode != 0:
        print(
            f"[calibre-convert] Conversion failed with exit code {completed.returncode}.",
            file=sys.stderr,
        )
        return completed.returncode

    if not output_path.exists():
        print(
            "[calibre-convert] Conversion command finished but output file was not created.",
            file=sys.stderr,
        )
        return 5

    print(f"[calibre-convert] Created: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
