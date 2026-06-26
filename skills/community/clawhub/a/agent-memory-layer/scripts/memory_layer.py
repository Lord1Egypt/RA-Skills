"""
Agent Memory Layer — Three-tier memory system
AgentBounty: MemoryAI Inc $5,800
"""
import json
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Optional


@dataclass
class MemoryItem:
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    priority: float = 1.0
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    ttl_seconds: Optional[float] = None
    id: str = field(default="")

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(f"{self.content}{self.timestamp}".encode()).hexdigest()[:12]

    @property
    def expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return (datetime.now() - self.timestamp).total_seconds() > self.ttl_seconds


class ShortTermMemory:
    """Working memory with TTL-based expiry. Redis-compatible interface."""

    def __init__(self, ttl_seconds: float = 3600, max_items: int = 100):
        self.ttl_seconds = ttl_seconds
        self.max_items = max_items
        self._store: list[MemoryItem] = []

    def add(self, content: str, priority: float = 1.0, ttl: Optional[float] = None) -> str:
        item = MemoryItem(
            content=content,
            priority=priority,
            ttl_seconds=ttl or self.ttl_seconds,
        )
        self._store.append(item)
        # Evict lowest priority if over limit
        if len(self._store) > self.max_items:
            self._store.sort(key=lambda x: x.priority)
            self._store.pop(0)
        return item.id

    def recall(self, limit: int = 10) -> list[dict]:
        active = [i for i in self._store if not i.expired]
        active.sort(key=lambda x: (x.priority, x.timestamp), reverse=True)
        return [{"id": i.id, "content": i.content, "priority": i.priority, "age_sec": (datetime.now() - i.timestamp).total_seconds()} for i in active[:limit]]

    def clear(self):
        self._store.clear()

    def prune(self):
        self._store = [i for i in self._store if not i.expired]


class LongTermMemory:
    """Persistent knowledge store with tag-based and semantic retrieval."""

    def __init__(self, storage_path: Optional[Path] = None):
        self._store: list[MemoryItem] = []
        self._tag_index: dict[str, list[str]] = defaultdict(list)
        self.storage_path = storage_path
        if storage_path and storage_path.exists():
            self._load()

    def store(self, content: str, tags: list[str] = None, metadata: dict = None) -> str:
        item = MemoryItem(content=content, tags=tags or [], metadata=metadata or {}, ttl_seconds=None)
        self._store.append(item)
        for tag in (tags or []):
            self._tag_index[tag].append(item.id)
        if self.storage_path:
            self._save()
        return item.id

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """Simple keyword search. In production, replace with vector similarity."""
        query_lower = query.lower()
        scored = []
        for item in self._store:
            score = 0.0
            if query_lower in item.content.lower():
                score += 1.0
            for tag in item.tags:
                if query_lower in tag.lower():
                    score += 0.5
            if score > 0:
                scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"id": i.id, "content": i.content, "tags": i.tags, "score": s} for s, i in scored[:limit]]

    def by_tag(self, tag: str) -> list[dict]:
        ids = set(self._tag_index.get(tag, []))
        return [{"id": i.id, "content": i.content, "tags": i.tags} for i in self._store if i.id in ids]

    def _save(self):
        data = [{"id": i.id, "content": i.content, "tags": i.tags, "metadata": i.metadata, "timestamp": i.timestamp.isoformat()} for i in self._store]
        self.storage_path.write_text(json.dumps(data, indent=2))

    def _load(self):
        data = json.loads(self.storage_path.read_text())
        for item in data:
            m = MemoryItem(content=item["content"], tags=item.get("tags", []), metadata=item.get("metadata", {}), id=item["id"], timestamp=datetime.fromisoformat(item["timestamp"]))
            self._store.append(m)
            for tag in m.tags:
                self._tag_index[tag].append(m.id)


@dataclass
class Episode:
    event: str
    timestamp: datetime = field(default_factory=datetime.now)
    outcome: str = "unknown"
    duration_min: float = 0.0
    context: dict = field(default_factory=dict)
    id: str = ""
    consolidation_count: int = 0

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(f"{self.event}{self.timestamp}".encode()).hexdigest()[:12]

    @property
    def weight(self) -> float:
        """Decay function: recent episodes weighted higher."""
        age_hours = (datetime.now() - self.timestamp).total_seconds() / 3600
        decay = max(0.1, 1.0 - age_hours / 720)  # 30-day half-life
        recency_boost = 1.0 if age_hours < 1 else 0.8 if age_hours < 24 else 0.5
        return decay * recency_boost * (1 + self.consolidation_count * 0.2)


class EpisodicMemory:
    """Timeline-ordered experience memory with decay and consolidation."""

    def __init__(self, consolidation_threshold: int = 3):
        self._episodes: list[Episode] = []
        self.consolidation_threshold = consolidation_threshold

    def record(self, event: str, outcome: str = "unknown", duration_min: float = 0.0, context: dict = None) -> str:
        ep = Episode(event=event, outcome=outcome, duration_min=duration_min, context=context or {})
        self._episodes.append(ep)
        return ep.id

    def find_similar(self, query: str, limit: int = 5) -> list[dict]:
        query_lower = query.lower()
        scored = []
        for ep in self._episodes:
            score = 0.0
            if query_lower in ep.event.lower():
                score += 1.0
            if query_lower in ep.outcome.lower():
                score += 0.5
            score *= ep.weight
            if score > 0:
                scored.append((score, ep))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"id": e.id, "event": e.event, "outcome": e.outcome, "weight": round(e.weight, 2), "score": round(s, 2)} for s, e in scored[:limit]]

    def recent(self, hours: float = 24, limit: int = 20) -> list[dict]:
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [e for e in self._episodes if e.timestamp >= cutoff]
        recent.sort(key=lambda x: x.timestamp, reverse=True)
        return [{"id": e.id, "event": e.event, "outcome": e.outcome, "when": e.timestamp.isoformat()} for e in recent[:limit]]

    def get_consolidation_candidates(self) -> list[Episode]:
        """Find episodes that should be promoted to long-term memory."""
        event_counts = defaultdict(list)
        for ep in self._episodes:
            key = ep.event[:50]  # normalize by first 50 chars
            event_counts[key].append(ep)

        candidates = []
        for key, eps in event_counts.items():
            if len(eps) >= self.consolidation_threshold:
                # Mark as consolidated
                for ep in eps:
                    ep.consolidation_count += 1
                candidates.append(eps[0])  # representative episode
        return candidates


class AgentMemory:
    """Unified memory interface combining all three tiers."""

    def __init__(self, agent_id: str, storage_dir: Optional[Path] = None):
        self.agent_id = agent_id
        base = storage_dir or Path(f".agent_memory/{agent_id}")
        base.mkdir(parents=True, exist_ok=True)

        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(base / "long_term.json")
        self.episodic = EpisodicMemory()

    def consolidate(self):
        """Promote recurring episodic memories to long-term."""
        candidates = self.episodic.get_consolidation_candidates()
        for ep in candidates:
            self.long_term.store(
                content=f"Pattern: {ep.event} → {ep.outcome}",
                tags=["consolidated", "pattern", ep.outcome],
                metadata={"source_episode": ep.id, "consolidation_count": ep.consolidation_count}
            )

    def full_context(self, query: str = "", limit: int = 20) -> dict:
        """Gather context from all memory tiers."""
        result = {
            "working": self.short_term.recall(limit=5),
            "knowledge": self.long_term.search(query, limit=limit) if query else [],
            "episodes": self.episodic.find_similar(query, limit=5) if query else self.episodic.recent(limit=5),
        }
        return result
