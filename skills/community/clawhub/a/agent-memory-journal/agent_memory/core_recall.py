from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import re
from .bm25 import BM25Index
import os
import shutil
import tempfile
from .storage import MemoryPaths, _refresh_manifest_entry, split_claim_and_metadata, utc_now_iso


@dataclass
class CoreRecallHit:
    text: str
    category: str
    path: str
    score: float
    line_no: int


def _stamp_line(line: str, timestamp: str) -> str:
    if 'last_seen:' in line:
        return re.sub(r'last_seen:[^\s\]]+', f'last_seen:{timestamp}', line)
    if line.endswith(']'):
        return line[:-1] + f' last_seen:{timestamp}]'
    return line + f' [last_seen:{timestamp}]'


def _bulk_update_last_seen(root: Path, hits: list['CoreRecallHit']) -> None:
    if not hits:
        return
    timestamp = utc_now_iso()
    by_path: dict[str, list[int]] = {}
    for hit in hits:
        by_path.setdefault(hit.path, []).append(hit.line_no)
    paths = MemoryPaths(root)
    for path_str, line_nos in by_path.items():
        target = Path(path_str)
        if not target.exists():
            continue
        lines = target.read_text(encoding='utf-8', errors='ignore').splitlines()
        touched = False
        for line_no in line_nos:
            if line_no < 1 or line_no > len(lines):
                continue
            new_line = _stamp_line(lines[line_no - 1], timestamp)
            if new_line != lines[line_no - 1]:
                lines[line_no - 1] = new_line
                touched = True
        if not touched:
            continue
        fd, temp_path = tempfile.mkstemp(dir=str(target.parent), prefix=target.name + '.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as handle:
                handle.write('\n'.join(lines).rstrip() + '\n')
            shutil.move(temp_path, str(target))
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            continue
        try:
            _refresh_manifest_entry(paths, target)
        except Exception:
            pass


def recall_core(root: str | Path, query: str, k: int = 5, update_last_seen: bool = True) -> list[CoreRecallHit]:
    root_path = Path(root).expanduser().resolve()
    core_dir = root_path / 'core'
    if not query.strip():
        return []
    if k < 0:
        raise ValueError('k must be >= 0')
    if k == 0 or not core_dir.exists():
        return []
    category_map = {
        'decisions': 'decision',
        'constraints': 'constraint',
        'gotchas': 'gotcha',
        'preferences': 'preference',
        'capabilities': 'capability',
    }
    docs = []
    meta = []
    for core_file in sorted(core_dir.glob('*.md')):
        category = category_map.get(core_file.stem, core_file.stem)
        for line_no, line in enumerate(core_file.read_text(encoding='utf-8', errors='ignore').splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue
            claim, _metadata = split_claim_and_metadata(stripped)
            docs.append(claim)
            meta.append((category, str(core_file), line_no))
    if not docs:
        return []

    cache_path = root_path / 'index' / 'core_bm25.json'
    index = BM25Index.from_cache(cache_path, docs)
    scores = index.score(query)
    hits = [
        CoreRecallHit(text=doc, category=category, path=path, score=score, line_no=line_no)
        for doc, score, (category, path, line_no) in zip(docs, scores, meta)
        if score > 0
    ]
    hits.sort(key=lambda item: (-item.score, item.category, item.line_no))
    results = hits[:k]
    if update_last_seen:
        _bulk_update_last_seen(root_path, results)
    return results
