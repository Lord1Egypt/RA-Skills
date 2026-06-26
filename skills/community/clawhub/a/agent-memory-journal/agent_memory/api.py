from __future__ import annotations

from pathlib import Path

from .core_recall import recall_core
from .episodic_recall import recall_episodic
from .hot import rebuild_agent_md
from .ingest import ingest_cycle
from .legacy import LegacyJournal
from .models import RecallResult
from .review_memory import log_review_findings
from .storage import append_core_memory, append_episodic_note, append_session_note, init_memory_root, supersede_memory

WARM_SCORE_WEIGHT = 2.0
PER_TIER_FETCH_MULTIPLIER = 2


class Journal:
    def __init__(self, root: str | Path = '.'):
        self.root = Path(root).expanduser().resolve()
        self.v2_root = self.root if self.root.name == '.memory' else self.root / '.memory'

    def init(self) -> Path:
        return init_memory_root(self.v2_root).root

    def recall(self, query: str, k: int = 5, tier: str = 'all'):
        if tier == 'warm':
            hits = self.recall_core(query, k=k)
            return [
                RecallResult(
                    text=h.text,
                    path=h.path,
                    line_no=h.line_no,
                    score=h.score,
                    tier='warm',
                    category=h.category
                ) for h in hits
            ]
        if tier == 'cold':
            hits = recall_episodic(self.v2_root, query=query, k=k)
            return [
                RecallResult(
                    text=h.text,
                    path=h.path,
                    line_no=h.line_no,
                    score=h.score,
                    tier='cold'
                ) for h in hits
            ]
        if tier == 'all':
            per_tier = max(1, k * PER_TIER_FETCH_MULTIPLIER)
            warm_hits = self.recall_core(query, k=per_tier)
            warm_results = [
                RecallResult(
                    text=h.text,
                    path=h.path,
                    line_no=h.line_no,
                    score=h.score * WARM_SCORE_WEIGHT,
                    tier='warm',
                    category=h.category
                ) for h in warm_hits
            ]

            cold_hits = recall_episodic(self.v2_root, query=query, k=per_tier)
            cold_results = [
                RecallResult(
                    text=h.text,
                    path=h.path,
                    line_no=h.line_no,
                    score=h.score,
                    tier='cold'
                ) for h in cold_hits
            ]

            merged = warm_results + cold_results
            merged.sort(key=lambda item: (-item.score, item.path, item.line_no))
            return merged[: max(1, k)]
        return []

    def note(self, text: str, category: str | None = None, importance: str = 'normal', source: str = 'agent') -> Path:
        return append_episodic_note(self.v2_root, text=text, category=category, importance=importance, source=source)

    def remember(self, text: str, category: str, source: str = 'agent', pinned: bool = False, supersedes: str | None = None) -> Path:
        if supersedes and not self.forget(supersedes):
            raise ValueError(f"cannot supersede missing memory id: {supersedes}")
        path = append_core_memory(self.v2_root, category=category, text=text, source=source, pinned=pinned, supersedes=supersedes)
        if pinned:
            rebuild_agent_md(self.v2_root)
        return path

    def forget(self, memory_id: str) -> bool:
        success = supersede_memory(self.v2_root, memory_id=memory_id)
        if success:
            # Cheap pass over core/; ensures any pinned line we just superseded
            # disappears from AGENT.md without waiting for the next ingest.
            rebuild_agent_md(self.v2_root)
        return success

    def session_note(self, session_id: str, text: str, category: str | None = None, importance: str = 'normal', source: str = 'agent') -> Path:
        return append_session_note(self.v2_root, session_id=session_id, text=text, category=category, importance=importance, source=source)

    def recall_core(self, query: str, k: int = 5, update_last_seen: bool = True):
        return recall_core(self.v2_root, query=query, k=k, update_last_seen=update_last_seen)

    def ingest(self):
        return ingest_cycle(self.v2_root)

    def log_review_findings(self, session_id: str, findings: list[str], category: str = 'gotcha'):
        return log_review_findings(self.v2_root, session_id=session_id, findings=findings, category=category)
