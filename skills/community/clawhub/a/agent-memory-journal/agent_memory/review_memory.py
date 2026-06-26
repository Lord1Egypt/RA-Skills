from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .session import collect_session_candidates
from .storage import append_session_note, init_memory_root, sanitize_session_id


@dataclass
class ReviewMemoryReport:
    notes_written: int
    session_candidates: int
    session_id: str


def log_review_findings(root: str | Path, session_id: str, findings: list[str], category: str = 'gotcha') -> ReviewMemoryReport:
    root_path = Path(root).expanduser().resolve()
    v2_root = init_memory_root(root_path if root_path.name == '.memory' else root_path / '.memory').root
    effective_session_id = sanitize_session_id(session_id)
    written = 0
    for finding in findings:
        text = finding.strip()
        if not text:
            continue
        append_session_note(v2_root, session_id=effective_session_id, text=text, category=category, importance='high', source='subagent')
        written += 1
    candidates = collect_session_candidates(v2_root)
    return ReviewMemoryReport(
        notes_written=written,
        session_candidates=len(candidates),
        session_id=effective_session_id,
    )
