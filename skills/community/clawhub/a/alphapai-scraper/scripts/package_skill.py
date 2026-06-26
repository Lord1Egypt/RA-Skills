#!/usr/bin/env python3
"""
Create a publish-safe copy of the skill folder without local secrets.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
EXCLUDED_NAMES = {
    "token.json",
    "token.local.json",
    "cookies.json",
    "cookies.local.json",
    "credentials.json",
    "credentials.local.json",
    "settings.json",
    "settings.local.json",
}


def ignore(path: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in EXCLUDED_NAMES or name.startswith(".DS_Store"):
            ignored.add(name)
    return ignored


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a publish-safe skill copy")
    parser.add_argument(
        "--dest",
        default=str(SKILL_DIR.parent / "dist" / "alphapai-scraper"),
        help="Destination directory",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    dest = Path(args.dest).expanduser().resolve()
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL_DIR, dest, ignore=ignore)
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
