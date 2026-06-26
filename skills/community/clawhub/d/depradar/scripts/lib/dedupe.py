"""Deduplication for /depradar — same pattern as last30days.

Within-source: remove near-duplicates using character trigram Jaccard similarity.
Cross-source: link related items across sources using hybrid similarity.
"""
from __future__ import annotations

import re
from typing import Callable, Dict, List, Set, Tuple, TypeVar

T = TypeVar("T")

# Common English stopwords to ignore during token comparison
_STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "i", "you", "he", "she", "it", "we",
    "they", "this", "that", "these", "those", "my", "your", "his", "her",
    "its", "our", "their", "not", "no", "if", "as", "so", "than", "then",
    "when", "how", "what", "which", "who", "why", "where", "all", "any",
    "each", "more", "also", "just", "about", "up", "out", "into", "after",
    "before", "can", "go", "get", "how",
}


def char_trigrams(text: str) -> Set[str]:
    """Generate character 3-grams from text."""
    # Normalize: lowercase and collapse whitespace
    normalized = re.sub(r"\s+", " ", text.lower().strip())
    if len(normalized) < 3:
        return {normalized} if normalized else set()
    return {normalized[i:i+3] for i in range(len(normalized) - 2)}


def token_set(text: str) -> Set[str]:
    """Tokenize text into lowercase words, remove stopwords."""
    words = re.findall(r"[a-zA-Z0-9_\-]+", text.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}


def jaccard(a: Set, b: Set) -> float:
    """Jaccard similarity: |A∩B| / |A∪B|."""
    if not a and not b:
        return 1.0
    intersection = len(a & b)
    union = len(a | b)
    if union == 0:
        return 0.0
    return intersection / union


def hybrid_similarity(text_a: str, text_b: str) -> float:
    """Max of char_trigram_jaccard and token_jaccard."""
    if not text_a or not text_b:
        return 0.0
    tri_sim = jaccard(char_trigrams(text_a), char_trigrams(text_b))
    tok_sim = jaccard(token_set(text_a), token_set(text_b))
    return max(tri_sim, tok_sim)


def dedupe_items(
    items: list,
    get_text_fn: Callable,
    threshold: float = 0.70,
) -> list:
    """Remove near-duplicates within a list. Keep higher-scored item.

    Args:
        items: List of any objects with a `score` attribute.
        get_text_fn: Callable(item) -> str returning the text to compare.
        threshold: Jaccard similarity threshold above which items are considered
                   duplicates. Default 0.70.

    Returns:
        Deduplicated list, sorted by score descending.
    """
    if not items:
        return items

    # Sort by score descending so we always keep the better-scored item
    sorted_items = sorted(items, key=lambda x: getattr(x, "score", 0), reverse=True)

    kept: List = []
    kept_texts: List[Tuple[Set[str], Set[str]]] = []  # (trigrams, tokens)

    for item in sorted_items:
        text = get_text_fn(item)
        tri = char_trigrams(text)
        tok = token_set(text)

        is_dup = False
        for k_tri, k_tok in kept_texts:
            tri_sim = jaccard(tri, k_tri)
            tok_sim = jaccard(tok, k_tok)
            if max(tri_sim, tok_sim) >= threshold:
                is_dup = True
                break

        if not is_dup:
            kept.append(item)
            kept_texts.append((tri, tok))

    return kept


def cross_source_link(
    *source_lists,
    get_text_fn: Callable,
    threshold: float = 0.40,
) -> None:
    """Mutate cross_refs on items that appear similar across sources.

    For each pair of items from different source lists whose hybrid
    similarity exceeds `threshold`, each item gets the other's `.id`
    appended to its `.cross_refs` list.

    Args:
        *source_lists: Variable number of lists of schema items, each from
                       a different source (e.g. github_issues, stackoverflow, …).
        get_text_fn: Callable(item) -> str returning the comparison text.
        threshold: Minimum hybrid similarity to create a cross-reference.
                   Default 0.40 (lower than dedupe because cross-source
                   items are expected to be less textually identical).
    """
    # Flatten into (source_idx, item) pairs
    indexed: List[Tuple[int, object]] = []
    for src_idx, lst in enumerate(source_lists):
        for item in lst:
            indexed.append((src_idx, item))

    n = len(indexed)
    if n < 2:
        return

    # Pre-compute text representations once
    texts: List[Tuple[Set[str], Set[str]]] = []
    for _, item in indexed:
        text = get_text_fn(item)
        texts.append((char_trigrams(text), token_set(text)))

    # O(n²) pairwise comparison — acceptable for typical result set sizes (<200)
    for i in range(n):
        src_i, item_i = indexed[i]
        tri_i, tok_i = texts[i]
        id_i = getattr(item_i, "id", None)
        if not id_i:
            continue

        for j in range(i + 1, n):
            src_j, item_j = indexed[j]
            if src_i == src_j:
                continue  # only cross-source links

            tri_j, tok_j = texts[j]
            id_j = getattr(item_j, "id", None)
            if not id_j:
                continue

            tri_sim = jaccard(tri_i, tri_j)
            tok_sim = jaccard(tok_i, tok_j)
            sim = max(tri_sim, tok_sim)

            if sim >= threshold:
                cross_refs_i = getattr(item_i, "cross_refs", None)
                cross_refs_j = getattr(item_j, "cross_refs", None)
                if cross_refs_i is not None and id_j not in cross_refs_i:
                    cross_refs_i.append(id_j)
                if cross_refs_j is not None and id_i not in cross_refs_j:
                    cross_refs_j.append(id_i)
