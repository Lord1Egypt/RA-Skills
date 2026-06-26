"""Lightweight semantic review helpers for fact-check style digests."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

_POSITIVE_MARKERS = (
    "works",
    "working",
    "real",
    "reliable",
    "helpful",
    "profitable",
    "earned",
    "earning",
    "success",
    "good",
    "增长",
    "真实",
    "可行",
    "赚钱",
    "有效",
)

_NEGATIVE_MARKERS = (
    "scam",
    "fraud",
    "malware",
    "fake",
    "not real",
    "unreliable",
    "failure",
    "failed",
    "risk",
    "bad",
    "misleading",
    "骗局",
    "夸大",
    "误导",
    "风险",
    "恶意",
    "失败",
)

_TOPIC_MARKERS: dict[str, tuple[str, ...]] = {
    "revenue": ("revenue", "mrr", "earning", "income", "$", "赚钱", "收入"),
    "security": ("security", "malware", "phishing", "漏洞", "恶意"),
    "adoption": ("users", "download", "growth", "活跃", "下载", "增长"),
}

_CLAIM_HINTS = (
    "is",
    "are",
    "was",
    "were",
    "will",
    "can",
    "should",
    ">= ",
    "<= ",
    "=",
    "达到",
    "实现",
    "支持",
    "返回",
)


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def classify_stance(text: str) -> str:
    normalized = _normalize(text)
    if not normalized:
        return "neutral"
    positive_hits = sum(1 for marker in _POSITIVE_MARKERS if marker in normalized)
    negative_hits = sum(1 for marker in _NEGATIVE_MARKERS if marker in normalized)
    if positive_hits > negative_hits:
        return "positive"
    if negative_hits > positive_hits:
        return "negative"
    return "neutral"


def extract_claim_candidates(text: str, *, max_claims: int = 3) -> list[str]:
    normalized = (text or "").strip()
    if not normalized:
        return []

    sentences = [
        chunk.strip()
        for chunk in re.split(r"(?<=[。！？.!?])\s+", normalized)
        if chunk.strip()
    ]
    selected: list[str] = []
    for sentence in sentences:
        lower = sentence.lower()
        has_number = bool(re.search(r"[$¥€]?\d+(?:[.,]\d+)?%?", sentence))
        has_hint = any(hint in lower for hint in _CLAIM_HINTS)
        if has_number or has_hint:
            selected.append(sentence)
        if len(selected) >= max_claims:
            break
    return selected


def build_semantic_review(items: list[Any]) -> dict[str, Any]:
    stance_counts: Counter[str] = Counter()
    topic_stances: dict[str, Counter[str]] = {}
    rows: list[dict[str, Any]] = []
    claim_pool: list[str] = []

    for item in items:
        title = str(getattr(item, "title", "") or "")
        content = str(getattr(item, "content", "") or "")
        text = f"{title}\n{content[:4000]}"
        stance = classify_stance(text)
        stance_counts[stance] += 1

        claims = extract_claim_candidates(text, max_claims=3)
        claim_pool.extend(claims)
        rows.append({
            "id": str(getattr(item, "id", "") or ""),
            "title": title[:160],
            "source": str(getattr(item, "source_name", "") or ""),
            "stance": stance,
            "claim_candidates": claims,
        })

        lowered = _normalize(text)
        for topic, markers in _TOPIC_MARKERS.items():
            if any(marker in lowered for marker in markers):
                topic_stances.setdefault(topic, Counter())[stance] += 1

    contradictions: list[dict[str, Any]] = []
    for topic, counts in topic_stances.items():
        if counts.get("positive", 0) > 0 and counts.get("negative", 0) > 0:
            contradictions.append({
                "topic": topic,
                "positive": counts.get("positive", 0),
                "negative": counts.get("negative", 0),
                "neutral": counts.get("neutral", 0),
            })

    return {
        "version": "heuristic-v1",
        "items_analyzed": len(items),
        "stance_counts": {
            "positive": stance_counts.get("positive", 0),
            "negative": stance_counts.get("negative", 0),
            "neutral": stance_counts.get("neutral", 0),
        },
        "contradictions": contradictions,
        "claim_candidates": claim_pool[:20],
        "items": rows,
        "note": "Heuristic semantic pass for claim extraction/stance/contradiction hints.",
    }
