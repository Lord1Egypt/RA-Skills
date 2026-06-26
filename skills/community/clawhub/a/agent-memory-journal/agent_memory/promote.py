from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .normalize import claims_match, normalize_claim, token_counter
from .storage import VALID_CATEGORIES, append_core_memory, init_memory_root

EPISODIC_LINE_RE = re.compile(r"^-\s+(\d{2}:\d{2})\s+(.*?)(?:\s+\[(.*)\])?$")
FIELD_RE = re.compile(r"(category|importance|source):([^\s\]]+)")
DEFAULT_MATCH_THRESHOLD = 0.60
DEFAULT_OVERLAP_THRESHOLD = 0.5
DEFAULT_TRIGGERS = [
    r'\bremember\b',
    r'\bdecision\b',
    r'\bdecided\b',
    r'\bfrom now on\b',
    r'\balways\b',
    r'\bpriority\b',
]


@dataclass
class Candidate:
    text: str
    normalized_claim: str
    tokens: list[str]
    category: str | None
    importance: str
    source: str
    refs: list[str]
    distinct_days: int
    occurrences: int
    score: float


def _parse_metadata(blob: str | None) -> dict[str, str]:
    if not blob:
        return {}
    return {match.group(1): match.group(2) for match in FIELD_RE.finditer(blob)}


def iter_episodic_entries(root: str | Path):
    paths = init_memory_root(root)
    for path in sorted(paths.episodic_dir.glob('*.md')):
        day = path.stem.split('/')[-1]
        lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        for line_no, line in enumerate(lines, start=1):
            match = EPISODIC_LINE_RE.match(line.strip())
            if not match:
                continue
            hhmm, text, meta_blob = match.groups()
            meta = _parse_metadata(meta_blob)
            yield {
                'date': day,
                'time': hhmm,
                'text': text.strip(),
                'category': meta.get('category'),
                'importance': meta.get('importance', 'normal'),
                'source': meta.get('source', 'agent'),
                'ref': f'{path}:{line_no}',
            }


def _counter_overlap_ratio(a: str, b: str) -> float:
    ca = token_counter(a)
    cb = token_counter(b)
    if not ca or not cb:
        return 0.0
    overlap = sum(min(ca[token], cb[token]) for token in ca if token in cb)
    denom = min(sum(ca.values()), sum(cb.values())) or 1
    return overlap / denom


def _guess_category(text: str) -> str | None:
    from .migrate import CATEGORY_HINTS
    lowered = text.lower()
    for needle, category in CATEGORY_HINTS.items():
        if needle in lowered:
            return category
    return None


def collect_candidates(root: str | Path, match_threshold: float = DEFAULT_MATCH_THRESHOLD, overlap_threshold: float = DEFAULT_OVERLAP_THRESHOLD) -> list[Candidate]:
    groups: list[dict] = []
    for entry in iter_episodic_entries(root):
        normalized, tokens = normalize_claim(entry['text'])
        if not normalized:
            continue
        matched_group = None
        for group in groups:
            # Semantic deduplication logic: combined Jaccard and Token Overlap
            if claims_match(group['representative'], entry['text'], threshold=match_threshold) or _counter_overlap_ratio(group['representative'], entry['text']) >= overlap_threshold:
                matched_group = group
                break
        if not matched_group:
            # New candidate discovery
            guessed_cat = _guess_category(entry['text'])
            matched_group = {
                'representative': entry['text'],
                'normalized_claim': normalized,
                'tokens': tokens,
                'category': entry['category'] or guessed_cat,
                'importance': entry['importance'],
                'source': entry['source'],
                'refs': [],
                'days': set(),
                'occurrences': 0,
            }
            groups.append(matched_group)
        matched_group['refs'].append(entry['ref'])
        matched_group['days'].add(entry['date'])
        matched_group['occurrences'] += 1
        if not matched_group['category'] and entry['category'] in VALID_CATEGORIES:
            matched_group['category'] = entry['category']
        if entry['importance'] == 'high':
            matched_group['importance'] = 'high'
    candidates: list[Candidate] = []
    for group in groups:
        score = float(group['occurrences'] + len(group['days']))
        if group['importance'] == 'high':
            score += 1.0
        candidates.append(
            Candidate(
                text=group['representative'],
                normalized_claim=group['normalized_claim'],
                tokens=group['tokens'],
                category=group['category'],
                importance=group['importance'],
                source=group['source'],
                refs=list(group['refs']),
                distinct_days=len(group['days']),
                occurrences=group['occurrences'],
                score=score,
            )
        )
    candidates.sort(key=lambda item: (-item.score, -(item.distinct_days), item.text.lower()))
    return candidates


def promote_repeated_candidates(root: str | Path, min_distinct_days: int = 2, match_threshold: float = DEFAULT_MATCH_THRESHOLD, overlap_threshold: float = DEFAULT_OVERLAP_THRESHOLD) -> list[Candidate]:
    promoted: list[Candidate] = []
    for candidate in collect_candidates(root, match_threshold=match_threshold, overlap_threshold=overlap_threshold):
        if candidate.category not in VALID_CATEGORIES:
            continue
        if candidate.distinct_days < min_distinct_days:
            continue
        try:
            append_core_memory(root, category=candidate.category, text=candidate.text, source='auto')
        except ValueError:
            continue
        promoted.append(candidate)
    return promoted
