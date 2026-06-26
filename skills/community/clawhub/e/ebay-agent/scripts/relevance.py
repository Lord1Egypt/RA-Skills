"""
Search relevance filtering for eBay results.

Filters out obvious accessories and junk from search results, and scores
title relevance so that comps used for valuation are trustworthy.
"""

import re

# Negative keywords — titles containing these (as whole words) are likely
# accessories, not the product itself.  Conservative list to avoid
# over-filtering.
ACCESSORY_KEYWORDS: set[str] = {
    # Keep this list conservative. Generic terms like "case" can cause
    # false positives for legitimate products that include a bundled case
    # (e.g. AirPods Pro with charging case).
    "cover",
    "protector",
    "charger",
    "cable",
    "skin",
    "decal",
    "sticker",
    "holster",
    "screen protector",
    "keyboard cover",
    "replacement strap",
    "empty box",
    "box only",
    "manual only",
    "adapter",
    "mount adapter",
    "lens cap",
    "lens hood",
    "body cap",
    "carrying bag",
    "pouch",
    "tripod",
    "cleaning kit",
    "tempered glass",
    "film",
    "silicone case",
    "hard case",
    "soft case",
    "wallet case",
    "bumper case",
    "case only",
    "charging case only",
    "replacement charging case",
    "replacement battery",
    "dock",
    "stand only",
}

# Multi-word patterns checked first, then single-word fallback
_MULTI_WORD = sorted(
    [kw for kw in ACCESSORY_KEYWORDS if " " in kw],
    key=len,
    reverse=True,
)
_SINGLE_WORD = {kw for kw in ACCESSORY_KEYWORDS if " " not in kw}


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())


def is_accessory(title: str) -> bool:
    """Return True if the title looks like an accessory, not the main product."""
    norm = _normalize(title)

    for phrase in _MULTI_WORD:
        if phrase in norm:
            return True

    # Word-boundary check for single keywords to avoid false positives
    # (e.g. "case" shouldn't match "showcase")
    words = set(re.findall(r"\b\w+\b", norm))
    return bool(words & _SINGLE_WORD)


def title_relevance_score(title: str, query: str) -> float:
    """
    Score how well a listing title matches the search query.

    Returns a float from 0.0 to 1.0.  Higher means more relevant.
    Checks what fraction of query tokens appear in the title, with a
    bonus for tokens appearing in order.
    """
    query_tokens = re.findall(r"\w+", query.lower())
    title_lower = title.lower()

    if not query_tokens:
        return 0.0

    # Token presence score
    matches = sum(1 for t in query_tokens if t in title_lower)
    presence = matches / len(query_tokens)

    # Order bonus: do the query tokens appear in sequence?
    order_bonus = 0.0
    if matches >= 2:
        # Check if matched tokens appear in title order
        positions = []
        for t in query_tokens:
            pos = title_lower.find(t)
            if pos >= 0:
                positions.append(pos)
        if positions == sorted(positions) and len(positions) == matches:
            order_bonus = 0.15

    return min(1.0, presence + order_bonus)


def filter_relevant(
    items: list[dict],
    query: str,
    min_relevance: float = 0.4,
) -> list[dict]:
    """
    Filter a list of search result items for relevance.

    Removes obvious accessories and items with low title relevance.
    Adds a 'relevance' key to each surviving item.

    Args:
        items: List of parsed item dicts (must have 'title').
        query: The original search query.
        min_relevance: Minimum title_relevance_score to keep (0.0-1.0).

    Returns:
        Filtered list with 'relevance' field added.
    """
    kept = []
    for item in items:
        title = item.get("title", "")
        if is_accessory(title):
            continue
        rel = title_relevance_score(title, query)
        if rel < min_relevance:
            continue
        item["relevance"] = round(rel, 3)
        kept.append(item)
    return kept
