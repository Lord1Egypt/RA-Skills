#!/usr/bin/env python3
"""Cross-validation module for multi-source data verification."""

from enum import Enum
from dataclasses import dataclass
from typing import List


class ConfidenceLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ValidationResult:
    score: float
    confidence: ConfidenceLevel
    warnings: List[str]
    sources_used: List[str]


def cross_validate(sources: List[dict]) -> ValidationResult:
    """Cross-validate data from multiple sources.

    Args:
        sources: List of dicts with 'source', 'data', 'score' keys

    Returns:
        ValidationResult with consensus score and confidence level
    """
    if not sources:
        return ValidationResult(
            score=0.0,
            confidence=ConfidenceLevel.LOW,
            warnings=["No sources provided"],
            sources_used=[]
        )

    scores = [s.get("score", 0.5) for s in sources]
    avg_score = sum(scores) / len(scores)

    # Check variance - low variance = high confidence
    variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)

    if len(sources) >= 3 and variance < 0.05:
        confidence = ConfidenceLevel.HIGH
    elif len(sources) >= 2 and variance < 0.1:
        confidence = ConfidenceLevel.MEDIUM
    else:
        confidence = ConfidenceLevel.LOW

    warnings = []
    if variance >= 0.1:
        warnings.append("High variance between sources")

    return ValidationResult(
        score=avg_score,
        confidence=confidence,
        warnings=warnings,
        sources_used=[s.get("source", "unknown") for s in sources]
    )
