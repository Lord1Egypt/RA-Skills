#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

HOME = Path.home()
SRC = HOME / '.easyclaw' / 'workspace'
DST = HOME / '.openclaw' / 'workspace'
STAGE = DST / 'imports' / 'easyclaw'

STAGE_FILES = [
    'AGENTS.md',
    'SOUL.md',
    'CORE-PRINCIPLE.md',
    'MEMORY.md',
    'USER.md',
    'IDENTITY.md',
    'HEARTBEAT.md',
    'docs/context-management.md',
]


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def backup(path: Path) -> Path:
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    out = path.with_name(f'{path.name}.bak.easyclaw-brain-{ts}')
    shutil.copy2(path, out)
    return out


def copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    ensure_parent(dst)
    shutil.copy2(src, dst)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Stage or selectively import EasyClaw brain files.')
    parser.add_argument('--import-memory', action='store_true', help='Import MEMORY.md and memory/ into the active workspace')
    args = parser.parse_args()

    staged = []
    for rel in STAGE_FILES:
        src = SRC / rel
        dst = STAGE / rel
        if copy_if_exists(src, dst):
            staged.append(rel)

    print('Staged files:')
    for rel in staged:
        print(f'- {rel} -> {STAGE / rel}')

    # Stage directories for reference
    for rel in ['memory', '.memos']:
        src_dir = SRC / rel
        if src_dir.exists():
            dst_dir = STAGE / rel
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f'- {rel}/ -> {dst_dir}')

    if not args.import_memory:
        print('\nStaging complete. Re-run with --import-memory to copy MEMORY.md and memory/ into the active workspace.')
        return 0

    src_memory = SRC / 'MEMORY.md'
    dst_memory = DST / 'MEMORY.md'
    if src_memory.exists() and dst_memory.exists():
        b = backup(dst_memory)
        print(f'Backed up existing MEMORY.md -> {b}')
    if src_memory.exists():
        copy_if_exists(src_memory, dst_memory)
        print(f'Imported MEMORY.md -> {dst_memory}')

    src_mem_dir = SRC / 'memory'
    dst_mem_dir = DST / 'memory'
    if src_mem_dir.exists():
        dst_mem_dir.mkdir(parents=True, exist_ok=True)
        imported = 0
        skipped = 0
        for src_file in src_mem_dir.rglob('*'):
            if src_file.is_dir():
                continue
            rel = src_file.relative_to(src_mem_dir)
            dst_file = dst_mem_dir / rel
            if dst_file.exists():
                skipped += 1
                continue
            ensure_parent(dst_file)
            shutil.copy2(src_file, dst_file)
            imported += 1
        print(f'Imported memory files: {imported}, skipped existing: {skipped}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
