#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import shutil


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive previous daily html before overwrite")
    parser.add_argument("target", help="Target html file path, e.g. output/daily/2026-04-02.html")
    parser.add_argument(
        "--archive-dir",
        default="output/archive",
        help="Archive directory root (default: output/archive)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = Path(args.target)
    if not target.exists():
        print("SKIP: target does not exist")
        return

    now = datetime.now()
    archive_root = Path(args.archive_dir)
    archive_root.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y-%m-%d-%H-%M")
    archive_path = archive_root / f"{stamp}.html"

    counter = 1
    while archive_path.exists():
        archive_path = archive_root / f"{stamp}-{counter}.html"
        counter += 1

    shutil.move(str(target), str(archive_path))
    print(f"ARCHIVED: {target} -> {archive_path}")


if __name__ == "__main__":
    main()
