#!/usr/bin/env python3
import os
from pathlib import Path


def detect_workspace_root() -> Path:
    env_root = os.environ.get('OPENCLAW_WORKSPACE')
    if env_root:
        return Path(env_root).expanduser().resolve()

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / 'AGENTS.md').exists() and (parent / 'skills').is_dir():
            return parent

    return current.parents[3]


def detect_skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def favorites_paths() -> dict[str, Path]:
    workspace_root = detect_workspace_root()
    skill_root = detect_skill_root()
    favorites_root = workspace_root / 'favorites'

    entries_dir = favorites_root / 'entries'
    snapshots_dir = favorites_root / 'snapshots'
    reports_dir = favorites_root / 'reports'

    for path in (favorites_root, entries_dir, snapshots_dir, reports_dir):
        path.mkdir(parents=True, exist_ok=True)

    return {
        'workspace_root': workspace_root,
        'skill_root': skill_root,
        'favorites_root': favorites_root,
        'entries_dir': entries_dir,
        'snapshots_dir': snapshots_dir,
        'reports_dir': reports_dir,
    }
