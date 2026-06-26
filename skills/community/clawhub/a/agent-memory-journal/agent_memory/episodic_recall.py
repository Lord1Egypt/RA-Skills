from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .bm25 import BM25Index


@dataclass
class EpisodicRecallHit:
    text: str
    path: str
    score: float
    line_no: int


def recall_recent(root: str | Path, days: int = 2, k: int = 100) -> list[EpisodicRecallHit]:
    root_path = Path(root).expanduser().resolve()
    episodic_dir = root_path / 'episodic'
    if not episodic_dir.exists() or k <= 0:
        return []
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=max(0, days))
    hits: list[EpisodicRecallHit] = []
    for daily_file in sorted(episodic_dir.glob('*.md'), reverse=True):
        try:
            day = datetime.strptime(daily_file.stem, '%Y-%m-%d').date()
        except ValueError:
            continue
        if day < cutoff:
            break
        for line_no, line in enumerate(daily_file.read_text(encoding='utf-8', errors='ignore').splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue
            hits.append(EpisodicRecallHit(text=stripped[2:], path=str(daily_file), score=0.0, line_no=line_no))
            if len(hits) >= k:
                return hits
    return hits


def recall_episodic(root: str | Path, query: str, k: int = 5) -> list[EpisodicRecallHit]:
    root_path = Path(root).expanduser().resolve()
    episodic_dir = root_path / 'episodic'
    if not query.strip():
        return []
    if k < 0:
        raise ValueError('k must be >= 0')
    if k == 0 or not episodic_dir.exists():
        return []
    docs = []
    meta = []
    for daily_file in sorted(episodic_dir.glob('*.md')):
        for line_no, line in enumerate(daily_file.read_text(encoding='utf-8', errors='ignore').splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue
            docs.append(stripped[2:])
            meta.append((str(daily_file), line_no))
    if not docs:
        return []
    
    root_path = Path(root).expanduser().resolve()
    cache_path = root_path / 'index' / 'episodic_bm25.json'
    index = BM25Index.from_cache(cache_path, docs)
    scores = index.score(query)
    hits = [
        EpisodicRecallHit(text=doc, path=path, score=score, line_no=line_no)
        for doc, score, (path, line_no) in zip(docs, scores, meta)
        if score > 0
    ]
    hits.sort(key=lambda item: (-item.score, item.path, item.line_no))
    return hits[:k]
