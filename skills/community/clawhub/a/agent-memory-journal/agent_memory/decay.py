from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .hot import _has_metadata_flag
from .storage import init_memory_root

CREATED_RE = re.compile(r'created:([^\s\]]+)')
LAST_SEEN_RE = re.compile(r'last_seen:([^\s\]]+)')


@dataclass
class DecayReport:
    archived: int
    retained: int
    archive_path: str


def _parse_iso_field(match: re.Match[str] | None) -> datetime | None:
    if not match:
        return None
    try:
        parsed = datetime.fromisoformat(match.group(1).replace('Z', '+00:00'))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _last_activity_at(line: str) -> datetime | None:
    last_seen = _parse_iso_field(LAST_SEEN_RE.search(line))
    created = _parse_iso_field(CREATED_RE.search(line))
    if last_seen and created:
        return max(last_seen, created)
    return last_seen or created


def archive_unpinned_core(root: str | Path, max_age_days: int = 30, max_active_per_file: int = 50) -> DecayReport:
    paths = init_memory_root(root)
    archived = 0
    retained = 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    for core_file in sorted(paths.core_dir.glob('*.md')):
        lines = core_file.read_text(encoding='utf-8', errors='ignore').splitlines()
        header = []
        bullets = []
        for line in lines:
            if line.strip().startswith('- '):
                bullets.append(line)
            else:
                header.append(line)
        pinned = [line for line in bullets if _has_metadata_flag(line, 'pinned:true')]
        unpinned = [line for line in bullets if not _has_metadata_flag(line, 'pinned:true')]
        stale = []
        fresh = []
        for line in unpinned:
            last_activity = _last_activity_at(line)
            if last_activity and last_activity < cutoff:
                stale.append(line)
            else:
                fresh.append(line)
        keep_count = max(0, max_active_per_file - len(pinned))
        keep_fresh = fresh[-keep_count:] if keep_count else []
        move_limit = fresh[:-keep_count] if keep_count else fresh[:]
        move_unpinned = stale + move_limit
        if move_unpinned:
            archive_target = paths.archive_core_dir / core_file.name
            if not archive_target.exists():
                archive_target.write_text(f'# Archived {core_file.stem.title()}\n\n', encoding='utf-8')
            with archive_target.open('a', encoding='utf-8') as handle:
                for line in move_unpinned:
                    handle.write(line + '\n')
            archived += len(move_unpinned)
        new_lines = header[:]
        if new_lines and new_lines[-1] != '':
            new_lines.append('')
        new_lines.extend(pinned + keep_fresh)
        core_file.write_text('\n'.join(new_lines).rstrip() + '\n', encoding='utf-8')
        retained += len(pinned) + len(keep_fresh)
    return DecayReport(archived=archived, retained=retained, archive_path=str(paths.archive_core_dir))
