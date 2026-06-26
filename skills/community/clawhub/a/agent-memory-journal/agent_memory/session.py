from __future__ import annotations

import re
from pathlib import Path

from .normalize import claims_match, token_counter
from .promote import Candidate, DEFAULT_MATCH_THRESHOLD, DEFAULT_OVERLAP_THRESHOLD
from .storage import VALID_CATEGORIES, init_memory_root

SESSION_LINE_RE = re.compile(r"^-\s+(\d{2}:\d{2})\s+(.*?)(?:\s+\[(.*)\])?$")
FIELD_RE = re.compile(r"(category|importance|source):([^\s\]]+)")


def _parse_metadata(blob: str | None) -> dict[str, str]:
    if not blob:
        return {}
    return {match.group(1): match.group(2) for match in FIELD_RE.finditer(blob)}


def _overlap_ratio(a: str, b: str) -> float:
    ca = token_counter(a)
    cb = token_counter(b)
    if not ca or not cb:
        return 0.0
    overlap = sum(min(ca[token], cb[token]) for token in ca if token in cb)
    denom = min(sum(ca.values()), sum(cb.values())) or 1
    return overlap / denom


def collect_session_candidates(root: str | Path, match_threshold: float = DEFAULT_MATCH_THRESHOLD, overlap_threshold: float = DEFAULT_OVERLAP_THRESHOLD) -> list[Candidate]:
    paths = init_memory_root(root)
    groups: list[dict] = []
    for path in sorted(paths.sessions_dir.glob('*.md')):
        session_id = path.stem
        for line_no, line in enumerate(path.read_text(encoding='utf-8', errors='ignore').splitlines(), start=1):
            match = SESSION_LINE_RE.match(line.strip())
            if not match:
                continue
            _hhmm, text, blob = match.groups()
            meta = _parse_metadata(blob)
            matched = None
            for group in groups:
                if claims_match(group['representative'], text, threshold=match_threshold) or _overlap_ratio(group['representative'], text) >= overlap_threshold:
                    matched = group
                    break
            if not matched:
                matched = {
                    'representative': text,
                    'category': meta.get('category'),
                    'importance': meta.get('importance', 'normal'),
                    'source': meta.get('source', 'agent'),
                    'refs': [],
                    'sessions': set(),
                    'occurrences': 0,
                    'tokens': [],
                    'normalized_claim': text.lower(),
                }
                groups.append(matched)
            matched['refs'].append(f'{path}:{line_no}')
            matched['sessions'].add(session_id)
            matched['occurrences'] += 1
            if not matched['category'] and meta.get('category') in VALID_CATEGORIES:
                matched['category'] = meta.get('category')
    out: list[Candidate] = []
    for group in groups:
        out.append(Candidate(
            text=group['representative'],
            normalized_claim=group['normalized_claim'],
            tokens=group['tokens'],
            category=group['category'],
            importance=group['importance'],
            source=group['source'],
            refs=group['refs'],
            distinct_days=len(group['sessions']),
            occurrences=group['occurrences'],
            score=float(group['occurrences'] + len(group['sessions'])),
        ))
    out.sort(key=lambda item: (-item.score, item.text.lower()))
    return out
