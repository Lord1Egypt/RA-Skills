from __future__ import annotations

import re
from pathlib import Path

from .normalize import claims_match
from .storage import VALID_CATEGORIES, append_core_memory, init_memory_root

CATEGORY_HINTS = {
    'decision': 'decision',
    'decided': 'decision',
    'must': 'constraint',
    'always': 'constraint',
    'avoid': 'gotcha',
    'bug': 'gotcha',
    'prefer': 'preference',
    'likes': 'preference',
    'can now': 'capability',
    'supports': 'capability',
    'restored': 'capability',
}
TIMESTAMP_PREFIX_RE = re.compile(r'^\d{1,2}:\d{2}\s+')


def _guess_category(text: str) -> str:
    lowered = text.lower()
    for needle, category in CATEGORY_HINTS.items():
        if needle in lowered:
            return category
    return 'decision'


def _strip_legacy_prefix(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith('- '):
        cleaned = cleaned[2:].lstrip()
    cleaned = TIMESTAMP_PREFIX_RE.sub('', cleaned)
    return cleaned.strip()


def _iter_legacy_daily(root: Path):
    legacy = root / 'memory'
    if not legacy.exists():
        return
    for path in sorted(legacy.glob('*.md')):
        if path.name.startswith('.'):
            continue
        for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
            stripped = line.strip()
            if stripped.startswith('- '):
                yield path.stem, stripped


def _iter_legacy_long(root: Path):
    long_file = root / 'MEMORY.md'
    if not long_file.exists():
        return
    for line in long_file.read_text(encoding='utf-8', errors='ignore').splitlines():
        stripped = line.strip()
        if stripped.startswith('- '):
            yield stripped[2:].strip()


def _existing_core_claims(v2_root: Path) -> list[str]:
    paths = init_memory_root(v2_root)
    claims: list[str] = []
    for core_file in paths.core_dir.glob('*.md'):
        for line in core_file.read_text(encoding='utf-8', errors='ignore').splitlines():
            stripped = line.strip()
            if stripped.startswith('- '):
                claims.append(stripped[2:].split(' [', 1)[0].strip())
    return claims


def _append_imported_episodic(v2_root: Path, date_str: str, text: str, category: str) -> tuple[Path, bool]:
    paths = init_memory_root(v2_root)
    target = paths.episodic_dir / f'{date_str}.md'
    line = f'- 00:00 {text} [category:{category} source:import]\n'
    existing_lines = target.read_text(encoding='utf-8', errors='ignore').splitlines() if target.exists() else []
    if line.rstrip('\n') not in existing_lines:
        with target.open('a', encoding='utf-8') as handle:
            handle.write(line)
        return target, True
    return target, False


def import_legacy_workspace(root: str | Path) -> dict[str, int]:
    workspace = Path(root).expanduser().resolve()
    v2 = init_memory_root(workspace / '.memory')

    imported_episodic = 0
    imported_core = 0
    seen_core: list[str] = _existing_core_claims(v2.root)

    for date_str, line in _iter_legacy_daily(workspace) or []:
        text = _strip_legacy_prefix(line)
        category = _guess_category(text)
        _target, added = _append_imported_episodic(v2.root, date_str=date_str, text=text, category=category)
        if added:
            imported_episodic += 1

    for text in _iter_legacy_long(workspace) or []:
        if any(claims_match(existing, text, threshold=0.85) for existing in seen_core):
            continue
        category = _guess_category(text)
        if category not in VALID_CATEGORIES:
            category = 'decision'
        append_core_memory(v2.root, category=category, text=text, source='import', pinned=False)
        seen_core.append(text)
        imported_core += 1

    return {
        'episodic_imported': imported_episodic,
        'core_imported': imported_core,
    }
