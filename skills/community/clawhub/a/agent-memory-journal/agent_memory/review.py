from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .hot import _has_metadata_flag, effective_hot_budget, rebuild_agent_md
from .storage import extract_state
from .promote import DEFAULT_MATCH_THRESHOLD, DEFAULT_OVERLAP_THRESHOLD, collect_candidates
from .session import collect_session_candidates
from .storage import init_memory_root


@dataclass
class ReviewReport:
    status: str
    episodic_candidates: int
    repeated_episodic_candidates: int
    session_candidates: int
    pinned_core_items: int
    hot_chars: int
    hot_path: str


def _count_pinned_core_items(root: str | Path) -> int:
    paths = init_memory_root(root)
    count = 0
    for core_file in paths.core_dir.glob('*.md'):
        for line in core_file.read_text(encoding='utf-8', errors='ignore').splitlines():
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue
            if not _has_metadata_flag(stripped, 'pinned:true'):
                continue
            if extract_state(stripped) == 'superseded':
                continue
            count += 1
    return count


def review_state(root: str | Path) -> ReviewReport:
    paths = init_memory_root(root)
    rebuild = rebuild_agent_md(paths.root)
    hot_text = paths.hot_file.read_text(encoding='utf-8', errors='ignore')
    episodic = collect_candidates(paths.root, match_threshold=DEFAULT_MATCH_THRESHOLD, overlap_threshold=DEFAULT_OVERLAP_THRESHOLD)
    session = collect_session_candidates(paths.root, match_threshold=DEFAULT_MATCH_THRESHOLD, overlap_threshold=DEFAULT_OVERLAP_THRESHOLD)
    repeated = sum(1 for item in episodic if item.distinct_days >= 2)
    budget = effective_hot_budget(paths.config)
    status = 'OK' if len(hot_text) <= budget else 'ISSUES_FOUND'
    return ReviewReport(
        status=status,
        episodic_candidates=len(episodic),
        repeated_episodic_candidates=repeated,
        session_candidates=len(session),
        pinned_core_items=_count_pinned_core_items(paths.root),
        hot_chars=len(hot_text),
        hot_path=rebuild['path'],
    )
