#!/usr/bin/env python3
"""Legacy CLI wrapper.

This file is kept for backward compatibility.
New structured entrypoint lives in src/anime_character_loader/cli.py.
"""

from pathlib import Path
import sys


def _bootstrap_src_path() -> None:
    repo_root = Path(__file__).resolve().parent
    src_dir = repo_root / "src"
    src_dir_str = str(src_dir)
    if src_dir_str not in sys.path:
        sys.path.insert(0, src_dir_str)


def main() -> int:
    _bootstrap_src_path()
    from anime_character_loader.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
