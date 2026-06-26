#!/usr/bin/env python3
from __future__ import annotations

import os
import re
from pathlib import Path


def _looks_like_workspace(path: Path) -> bool:
    return (path / 'MEMORY.md').exists() or (path / 'memory').exists()


def resolve_workspace() -> Path:
    env = os.environ.get('AGENT_MEMORY_WORKSPACE', '').strip()
    if env:
        p = Path(env).expanduser().resolve()
        if _looks_like_workspace(p):
            return p

    cwd = Path.cwd().resolve()
    for base in [cwd, *cwd.parents]:
        if _looks_like_workspace(base):
            return base

    here = Path(__file__).resolve()
    for base in [*here.parents]:
        if _looks_like_workspace(base):
            return base

    return cwd


WORKSPACE = resolve_workspace()
INDEX_DIR = WORKSPACE / '.memory-index'
INDEX_FILE = INDEX_DIR / 'index.jsonl'
META_FILE = INDEX_DIR / 'meta.json'
MEMORY_DIR = WORKSPACE / 'memory'
MEMORY_MD = WORKSPACE / 'MEMORY.md'
LEARNINGS_MD = MEMORY_DIR / 'learnings.md'
DAILY_MEMORY_RE = re.compile(r'^20\d{2}-\d{2}-\d{2}\.md$')


def list_daily_memory_files() -> list[Path]:
    if not MEMORY_DIR.exists():
        return []
    return [
        p
        for p in sorted(MEMORY_DIR.iterdir())
        if p.is_file() and DAILY_MEMORY_RE.fullmatch(p.name)
    ]
