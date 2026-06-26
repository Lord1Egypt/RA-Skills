"""
Simple heuristic-based helper for the geo-hallucination-checker skill.

This script is not a full fact-checking engine. Instead, it:
- Splits text into rough sentences.
- Scores each sentence for hallucination risk based on lexical patterns.
- Returns a list of sentences with basic risk scores and matched patterns.

It is intended as an optional helper for deterministic workflows or
batch pre-screening, not as a replacement for careful reasoning in the skill.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class SentenceRisk:
    sentence: str
    risk_score: int
    matched_patterns: List[str]


SUSPICIOUS_PATTERNS = [
    r"\b\d{2,3}%\b",  # very specific percentages
    r"\bclinical(ly)? proven\b",
    r"\bguaranteed\b",
    r"\bno risk\b",
    r"\bzero risk\b",
    r"\bthe only\b",
    r"\bworld(-|\s)?class\b",
    r"\bnumber one\b",
    r"\b#1\b",
    r"\baccording to (a|an|the)?\s*(study|report|research)\b",
    r"\b(in|from)\s+\d{4}\s+(study|trial|paper)\b",
    r"\b(randomized|double-blind|placebo-controlled)\b",
    r"\b(guarantee|warranty) of\b",
]


SUSPICIOUS_INSTITUTION_PATTERNS = [
    r"\bHarvard\b",
    r"\bMIT\b",
    r"\bStanford\b",
    r"\bOxford\b",
    r"\bCambridge\b",
    r"\bYale\b",
    r"\bWorld Health Organization\b",
    r"\bWHO\b",
    r"\bFDA\b",
    r"\bEMA\b",
    r"\bNobel\b",
]


def split_into_sentences(text: str) -> List[str]:
    """Very naive sentence splitter. Good enough for heuristic scanning."""
    # Replace newlines with spaces and collapse multiple spaces.
    cleaned = re.sub(r"\s+", " ", text.strip())
    if not cleaned:
        return []

    # Split on sentence-ending punctuation while keeping things simple.
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    sentences = [p.strip() for p in parts if p.strip()]
    return sentences


def score_sentence(sentence: str) -> SentenceRisk:
    """
    Score a single sentence for hallucination risk.

    Higher scores indicate more potential hallucination risk.
    """
    matched: List[str] = []
    score = 0

    lower = sentence.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, sentence, flags=re.IGNORECASE):
            matched.append(pattern)
            score += 2

    for pattern in SUSPICIOUS_INSTITUTION_PATTERNS:
        if re.search(pattern, sentence, flags=re.IGNORECASE):
            matched.append(pattern)
            score += 1

    # Extra penalty for mixture of strong claims and institutions.
    if score >= 3 and ("study" in lower or "trial" in lower or "proven" in lower):
        score += 1

    return SentenceRisk(sentence=sentence, risk_score=score, matched_patterns=matched)


def analyze_text(text: str, min_score: int = 2) -> List[Dict[str, Any]]:
    """
    Analyze a block of text and return potentially risky sentences.

    :param text: Input content to scan.
    :param min_score: Minimum risk_score to include in the output.
    :return: List of dicts with sentence, risk_score, and matched_patterns.
    """
    sentences = split_into_sentences(text)
    results: List[Dict[str, Any]] = []

    for sent in sentences:
        risk = score_sentence(sent)
        if risk.risk_score >= min_score:
            results.append(asdict(risk))

    return results


def main() -> None:
    import sys
    import json

    if sys.stdin.isatty():
        print("Paste text on stdin to analyze hallucination risk.", file=sys.stderr)
        print("Example: python hallucination_checker.py < input.txt", file=sys.stderr)
        sys.exit(1)

    text = sys.stdin.read()
    data = analyze_text(text)
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()


