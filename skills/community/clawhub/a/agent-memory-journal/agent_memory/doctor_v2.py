from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .hot import effective_hot_budget
from .storage import init_memory_root


@dataclass
class DoctorReport:
    status: str
    hot_chars: int
    hot_over_limit: bool
    manifest_mismatches: list[str]
    checked_files: int


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def refresh_manifest(root: str | Path) -> dict[str, object]:
    paths = init_memory_root(root)
    tracked = {}
    for file_path in sorted(paths.core_dir.glob('*.md')):
        tracked[str(file_path.relative_to(paths.root))] = _hash_file(file_path)
    manifest = {
        'schema': 1,
        'layout': 'agent-memory-v2',
        'core_sha256': tracked,
    }
    target = paths.index_dir / 'manifest.json'
    target.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def doctor_verify(root: str | Path, fix: bool = False) -> DoctorReport:
    paths = init_memory_root(root)
    manifest_path = paths.index_dir / 'manifest.json'
    if not manifest_path.exists() or fix:
        refresh_manifest(paths.root)

    mismatches: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except Exception:
        manifest = {}
        mismatches.append('invalid:manifest-json')

    schema = manifest.get('schema')
    layout = manifest.get('layout')
    tracked = manifest.get('core_sha256')

    if schema != 1:
        mismatches.append('invalid:schema')
    if layout != 'agent-memory-v2':
        mismatches.append('invalid:layout')
    if not isinstance(tracked, dict) or not tracked:
        manifest = refresh_manifest(paths.root)
        tracked = manifest.get('core_sha256', {})

    checked = 0
    if not isinstance(tracked, dict):
        mismatches.append('invalid:core_sha256')
        tracked = {}

    for rel_path, expected in tracked.items():
        if not isinstance(rel_path, str) or not isinstance(expected, str):
            mismatches.append('invalid:core_sha256-entry')
            continue
        file_path = paths.root / rel_path
        checked += 1
        if not file_path.exists():
            mismatches.append(f'missing:{rel_path}')
            continue
        actual = _hash_file(file_path)
        if actual != expected:
            mismatches.append(f'mismatch:{rel_path}')
    hot_chars = len(paths.hot_file.read_text(encoding='utf-8', errors='ignore')) if paths.hot_file.exists() else 0
    hot_budget = effective_hot_budget(paths.config)
    hot_over_limit = hot_chars > hot_budget
    status = 'OK' if not mismatches and not hot_over_limit and checked > 0 else 'ISSUES_FOUND'
    return DoctorReport(
        status=status,
        hot_chars=hot_chars,
        hot_over_limit=hot_over_limit,
        manifest_mismatches=mismatches,
        checked_files=checked,
    )
