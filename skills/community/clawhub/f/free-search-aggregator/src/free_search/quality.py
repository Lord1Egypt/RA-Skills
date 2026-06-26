"""Search result quality optimization: relevance scoring, dedup, reranking."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

# ── Tokenization ────────────────────────────────────────────────────────────

_TOKEN_PATTERN = re.compile(r"[\w\u4e00-\u9fff\u3040-\u30ff]+", re.UNICODE)


def _tokenize(text: str) -> set[str]:
    """Split text into lowercase token set (works for Latin + CJK)."""
    return {m.group().lower() for m in _TOKEN_PATTERN.finditer(text)} if text else set()


# ── Relevance Scoring ───────────────────────────────────────────────────────


def relevance_score(query: str, title: str, snippet: str) -> float:
    """Compute relevance of a result to the query (0.0–1.0).

    Weighted: title match 60%, snippet match 40%.
    """
    q_tokens = _tokenize(query)
    if not q_tokens:
        return 0.0

    t_tokens = _tokenize(title)
    s_tokens = _tokenize(snippet)

    title_overlap = len(q_tokens & t_tokens) / len(q_tokens) if q_tokens else 0.0
    snippet_overlap = len(q_tokens & s_tokens) / len(q_tokens) if q_tokens else 0.0

    return min(1.0, title_overlap * 0.6 + snippet_overlap * 0.4)


# ── Similarity ──────────────────────────────────────────────────────────────


def title_similarity(a: str, b: str) -> float:
    """Jaccard token similarity between two titles."""
    ta = _tokenize(a)
    tb = _tokenize(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


# ── Domain Extraction ───────────────────────────────────────────────────────


def _extract_domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc.lower()
        # Strip www. prefix for grouping
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""


# ── Deduplication ────────────────────────────────────────────────────────────


def deduplicate_results(
    results: list[dict[str, Any]],
    *,
    title_threshold: float = 0.80,
) -> list[dict[str, Any]]:
    """Remove near-duplicate results by URL canonicalization + title similarity.

    Preserves order; keeps the first occurrence.
    """
    kept: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    kept_titles: list[str] = []

    for item in results:
        url = (item or {}).get("url", "")
        title = (item or {}).get("title", "")

        # URL-level dedup
        domain_path = _extract_domain(url) + urlparse(url).path.rstrip("/").lower()
        if domain_path in seen_urls:
            continue

        # Title similarity dedup
        is_dup = False
        for prev_title in kept_titles:
            if title_similarity(title, prev_title) >= title_threshold:
                is_dup = True
                break
        if is_dup:
            continue

        seen_urls.add(domain_path)
        kept_titles.append(title)
        kept.append(item)

    return kept


# ── Reranking ────────────────────────────────────────────────────────────────


def rerank_results(
    query: str,
    results: list[dict[str, Any]],
    *,
    max_per_domain: int = 3,
) -> list[dict[str, Any]]:
    """Rerank results by relevance + domain diversity.

    - Computes relevance_score for each result
    - Limits max_per_domain results from the same domain
    - Sorts by score descending, preserving ties by original order
    """
    scored: list[tuple[float, int, dict[str, Any]]] = []
    for idx, item in enumerate(results):
        title = (item or {}).get("title", "")
        snippet = (item or {}).get("snippet", "")
        score = relevance_score(query, title, snippet)
        # Bonus for longer snippets (information richness)
        snippet_len = len(snippet) if snippet else 0
        length_bonus = min(0.1, snippet_len / 1000.0)
        item["_relevance_score"] = round(score + length_bonus, 4)
        scored.append((score + length_bonus, idx, item))

    # Sort by score desc, then original position
    scored.sort(key=lambda x: (-x[0], x[1]))

    # Domain diversity filter
    domain_counts: dict[str, int] = {}
    output: list[dict[str, Any]] = []
    for _score, _idx, item in scored:
        domain = _extract_domain(item.get("url", ""))
        if domain:
            count = domain_counts.get(domain, 0)
            if count >= max_per_domain:
                continue
            domain_counts[domain] = count + 1
        output.append(item)

    return output


# ── Filtering ────────────────────────────────────────────────────────────────


def filter_low_quality(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove results that are clearly low quality."""
    filtered: list[dict[str, Any]] = []
    for item in results:
        title = (item or {}).get("title", "")
        snippet = (item or {}).get("snippet", "")
        url = (item or {}).get("url", "")

        # Skip results with no title or extremely short title
        if not title or len(title.strip()) < 3:
            continue
        # Skip results with no URL
        if not url:
            continue
        # Keep results even with empty snippet (some valid results lack snippets)
        # but deprioritize them in reranking via score

        filtered.append(item)
    return filtered


# ── Full Pipeline ────────────────────────────────────────────────────────────


def optimize_results(
    query: str,
    results: list[dict[str, Any]],
    *,
    max_per_domain: int = 3,
    title_dedup_threshold: float = 0.80,
) -> list[dict[str, Any]]:
    """Full quality optimization pipeline.

    1. Filter low-quality results
    2. Deduplicate (URL + title similarity)
    3. Rerank by relevance + domain diversity

    Returns optimized result list. Does not mutate input.
    """
    if not results:
        return []

    # Work on copies to avoid mutating input
    items = [dict(r) for r in results if r]

    items = filter_low_quality(items)
    items = deduplicate_results(items, title_threshold=title_dedup_threshold)
    items = rerank_results(query, items, max_per_domain=max_per_domain)

    # Clean up internal scoring keys before returning
    for item in items:
        item.pop("_relevance_score", None)

    return items
