#!/usr/bin/env python3

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


EXCLUDE_DIRS = {"__pycache__"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".DS_Store", ".uploading.cfg", ".xsd"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a clean distributable zip for a skill folder."
    )
    parser.add_argument(
        "--skill-dir",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the skill directory",
    )
    parser.add_argument("--out", required=True, help="Output zip file path")
    return parser.parse_args()


def should_skip(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    return any(str(path).endswith(suffix) for suffix in EXCLUDE_SUFFIXES)


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir).resolve()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_dir.rglob("*")):
            if not file_path.is_file():
                continue
            if should_skip(file_path):
                continue
            zf.write(file_path, file_path.relative_to(skill_dir.parent))

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
