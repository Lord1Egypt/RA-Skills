#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import os
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist' / 'auto-proteomics.skill'
IGNORE_FILE = ROOT / '.skillignore'


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


def main() -> int:
    patterns = load_patterns(IGNORE_FILE)
    DIST.parent.mkdir(parents=True, exist_ok=True)
    files = []
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == DIST.relative_to(ROOT).as_posix():
            continue
        if ignored(rel, patterns):
            continue
        files.append(path)
    files.sort()
    with zipfile.ZipFile(DIST, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, arcname=(ROOT.name + '/' + path.relative_to(ROOT).as_posix()))
    print(f'Built {DIST}')
    print(f'Included {len(files)} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
