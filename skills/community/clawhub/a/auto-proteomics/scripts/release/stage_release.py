#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IGNORE_FILE = ROOT / '.skillignore'
DEFAULT_STAGE_DIR = ROOT / 'dist' / 'release' / ROOT.name


def load_patterns(path: Path) -> list[str]:
    patterns = []
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        patterns.append(line)
    return patterns


def ignored(rel_path: str, patterns: list[str]) -> bool:
    normalized = rel_path.replace(os.sep, '/')
    for pattern in patterns:
        cleaned = pattern.rstrip('/')
        if pattern.endswith('/'):
            if fnmatch.fnmatch(normalized, cleaned) or fnmatch.fnmatch(normalized, cleaned + '/*'):
                return True
        if fnmatch.fnmatch(normalized, pattern):
            return True
        if fnmatch.fnmatch(normalized, cleaned):
            return True
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Stage a clean public release directory')
    parser.add_argument('--output-dir', default=str(DEFAULT_STAGE_DIR), help='Stage directory path')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    stage_dir = Path(args.output_dir).resolve()
    patterns = load_patterns(IGNORE_FILE)

    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith('dist/'):
            continue
        if ignored(rel, patterns):
            continue
        target = stage_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied += 1

    print(f'Staged {copied} files to {stage_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
