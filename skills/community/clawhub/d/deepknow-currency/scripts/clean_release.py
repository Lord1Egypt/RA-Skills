#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import sys


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def transient_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in root.rglob("__pycache__"):
        if directory.is_dir():
            paths.append(directory)
    for pyc_file in root.rglob("*.pyc"):
        if pyc_file.is_file():
            paths.append(pyc_file)
    return sorted(set(paths))


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    root = skill_root()
    paths = transient_paths(root)
    if check_only:
        if paths:
            for path in paths:
                print(path.relative_to(root))
            return 1
        print("CLEAN")
        return 0

    for path in paths:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    print(f"REMOVED={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
