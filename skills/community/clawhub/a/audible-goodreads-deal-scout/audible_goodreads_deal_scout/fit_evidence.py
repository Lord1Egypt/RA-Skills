from __future__ import annotations

from typing import Any

from .goodreads_csv import effective_shelf
from .shared import normalize_author_key, normalize_review_text, normalize_space, normalized_key, truncate_text


MAX_FIT_EVIDENCE_ENTRIES = 12
MAX_FIT_EVIDENCE_REVIEWS = 6
MAX_FIT_EVIDENCE_REVIEW_CHARS = 2_000
MAX_RELATED_ENTRIES = 8

STOP_WORDS = {
    "and",
    "about",
    "after",
    "again",
    "against",
    "also",
    "among",
    "another",
    "because",
    "before",
    "being",
    "between",
    "book",
    "from",
    "has",
    "have",
    "her",
    "his",
    "into",
    "more",
    "most",
    "novel",
    "only",
    "our",
    "other",
    "over",
    "story",
    "than",
    "that",
    "the",
    "their",
    "them",
    "there",
    "these",
    "they",
    "this",
    "too",
    "through",
    "under",
    "very",
    "what",
    "when",
    "where",
    "which",
    "while",
    "with",
    "you",
    "your",
    "would",
}


def meaningful_terms(value: Any) -> set[str]:
    normalized = normalized_key(str(value or ""), ascii_only=True)
    return {
        token
        for token in normalized.split()
        if len(token) >= 3 and token not in STOP_WORDS and not token.isdigit()
    }


def _candidate_terms(candidate: dict[str, Any]) -> dict[str, set[str]]:
    genres = " ".join(normalize_space(str(item)) for item in candidate.get("genres") or [])
    return {
        "title": meaningful_terms(candidate.get("title")),
        "genres": meaningful_terms(genres),
        "summary": meaningful_terms(candidate.get("summary")),
    }


def _rank_entry(candidate: dict[str, Any], row: dict[str, Any], entry_id: int) -> dict[str, Any]:
    candidate_title = normalized_key(str(candidate.get("title") or ""), ascii_only=True)
    row_title = normalized_key(str(row.get("title") or ""), ascii_only=True)
    candidate_author = normalize_author_key(str(candidate.get("author") or ""), ascii_only=True)
    row_author = normalize_author_key(str(row.get("author") or ""), ascii_only=True)
    terms = _candidate_terms(candidate)
    row_title_terms = meaningful_terms(row.get("title"))
    row_review_terms = meaningful_terms(row.get("myReview"))
    title_overlap = terms["title"] & row_title_terms
    row_terms = row_title_terms | row_review_terms
    genre_overlap = terms["genres"] & row_terms
    summary_overlap = terms["summary"] & row_terms
    context_overlap = genre_overlap | (summary_overlap if len(summary_overlap) >= 2 else set())

    reasons: list[str] = []
    score = 0
    if candidate_title and row_title == candidate_title:
        score += 120
        reasons.append("same_title")
    if candidate_author and row_author == candidate_author:
        score += 80
        reasons.append("same_author")
    if title_overlap:
        score += len(title_overlap) * 12
        reasons.append("title_overlap")
    if context_overlap:
        score += len(context_overlap) * 4
        reasons.append("candidate_context_overlap")
    return {
        "entryId": entry_id,
        "row": row,
        "score": score,
        "reasons": reasons,
        "matchedTerms": sorted(title_overlap | context_overlap)[:8],
    }


def _general_anchors(ranked: list[dict[str, Any]], *, positive: bool) -> list[dict[str, Any]]:
    def is_candidate(item: dict[str, Any]) -> bool:
        rating = int(item["row"].get("myRating") or 0)
        review = normalize_review_text(str(item["row"].get("myReview") or ""))
        return bool(review) and (rating >= 4 if positive else 0 < rating <= 3)

    candidates = [item for item in ranked if is_candidate(item)]
    if positive:
        candidates.sort(
            key=lambda item: (
                -int(item["row"].get("myRating") or 0),
                -len(normalize_review_text(str(item["row"].get("myReview") or ""))),
                item["entryId"],
            )
        )
    else:
        candidates.sort(
            key=lambda item: (
                int(item["row"].get("myRating") or 0),
                -len(normalize_review_text(str(item["row"].get("myReview") or ""))),
                item["entryId"],
            )
        )
    return candidates


def _select_ranked_entries(ranked: list[dict[str, Any]]) -> list[dict[str, Any]]:
    related = [item for item in ranked if item["score"] > 0]
    related.sort(key=lambda item: (-item["score"], item["entryId"]))

    selected: list[dict[str, Any]] = []
    selected_ids: set[int] = set()

    def add(item: dict[str, Any], fallback_reason: str | None = None) -> None:
        if len(selected) >= MAX_FIT_EVIDENCE_ENTRIES or item["entryId"] in selected_ids:
            return
        copied = dict(item)
        if not copied["reasons"] and fallback_reason:
            copied["reasons"] = [fallback_reason]
        selected.append(copied)
        selected_ids.add(item["entryId"])

    for item in related[:MAX_RELATED_ENTRIES]:
        add(item)
    for item in _general_anchors(ranked, positive=True)[:2]:
        add(item, "positive_review_anchor")
    for item in _general_anchors(ranked, positive=False)[:2]:
        add(item, "critical_review_anchor")
    for item in related[MAX_RELATED_ENTRIES:]:
        add(item)
    return selected


def build_fit_evidence(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    ranked = [_rank_entry(candidate, row, index) for index, row in enumerate(rows)]
    selected = _select_ranked_entries(ranked)
    reviews_included = 0
    entries: list[dict[str, Any]] = []
    for item in selected:
        row = item["row"]
        review = normalize_review_text(str(row.get("myReview") or ""))
        include_review = bool(review) and reviews_included < MAX_FIT_EVIDENCE_REVIEWS
        if include_review:
            reviews_included += 1
        entry = {
            "entryId": item["entryId"],
            "title": normalize_space(str(row.get("title") or "")),
            "author": normalize_space(str(row.get("author") or "")),
            "rating": int(row.get("myRating") or 0),
            "shelf": effective_shelf(row) or normalize_space(str(row.get("exclusiveShelf") or "")),
            "selectionReasons": item["reasons"],
            "matchedTerms": item["matchedTerms"],
            "evidenceStrength": "review_backed" if include_review else "rating_only",
        }
        if include_review:
            review_text = truncate_text(review, MAX_FIT_EVIDENCE_REVIEW_CHARS)
            entry["reviewText"] = review_text
            entry["reviewTruncated"] = review_text != review
        entries.append(entry)

    return {
        "schemaVersion": 1,
        "candidate": {
            "title": normalize_space(str(candidate.get("title") or "")),
            "author": normalize_space(str(candidate.get("author") or "")),
            "genres": [normalize_space(str(item)) for item in candidate.get("genres") or [] if normalize_space(str(item))],
        },
        "selection": {
            "totalEligibleEntries": len(rows),
            "selectedEntryCount": len(entries),
            "selectedReviewCount": reviews_included,
            "maxEntries": MAX_FIT_EVIDENCE_ENTRIES,
            "maxReviews": MAX_FIT_EVIDENCE_REVIEWS,
            "maxReviewChars": MAX_FIT_EVIDENCE_REVIEW_CHARS,
        },
        "entries": entries,
    }
