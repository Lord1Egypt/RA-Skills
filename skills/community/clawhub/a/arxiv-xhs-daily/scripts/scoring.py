from __future__ import annotations

from typing import Any


def _keyword_hits(text: str, keywords: list[str]) -> int:
    return sum(1 for term in keywords if term.lower() in text)


def score_paper(paper: dict[str, Any], topic_config: dict[str, Any]) -> float:
    text = f"{paper.get('title', '')} {paper.get('summary', '')}".lower()
    score = 0.0
    positive_hits = _keyword_hits(text, topic_config.get("keywords", []))
    negative_hits = _keyword_hits(text, topic_config.get("negative_keywords", []))
    score += positive_hits * 3.0
    score -= negative_hits * 3.0
    if "reasoning" in text or "推理" in text:
        score += 0.8
    if "alignment" in text or "safety" in text:
        score += 0.5
    if "agent" in text and positive_hits > 0:
        score += 0.5
    return round(score, 3)


def matched(paper: dict[str, Any], topic_config: dict[str, Any]) -> bool:
    text = f"{paper.get('title', '')} {paper.get('summary', '')}".lower()
    positive_hits = _keyword_hits(text, topic_config.get("keywords", []))
    negative_hits = _keyword_hits(text, topic_config.get("negative_keywords", []))
    if negative_hits > 0:
        return False
    return positive_hits > 0 and score_paper(paper, topic_config) >= 3.0
