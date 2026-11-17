#!/usr/bin/env python3
"""Offline development records and confidence routing for Jev decisions.

No network client is present by design.  Live Jev calls are optional engineering
experiments; their sanitized typed results can be parsed here and reviewed by
Codex.  Runtime and CI remain independent of TypeSafe credentials and service.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence


class ConfidenceDisposition(str, Enum):
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    ESCALATE = "ESCALATE"


_SECRET_KEYS = re.compile(r"(?i)(api[_-]?key|authorization|bearer|access[_-]?token|secret|credential)")


def confidence_disposition(
    confidence: float,
    *,
    probabilities: Mapping[str, float] | None = None,
    contradictory: bool = False,
) -> ConfidenceDisposition:
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= float(confidence) <= 1:
        raise ValueError("confidence must be between 0 and 1")
    if contradictory:
        return ConfidenceDisposition.ESCALATE
    if probabilities:
        clean = sorted((float(value) for value in probabilities.values()), reverse=True)
        if any(value < 0 or value > 1 for value in clean):
            raise ValueError("probabilities must be between 0 and 1")
        if len(clean) > 1 and clean[0] - clean[1] < 0.15:
            return ConfidenceDisposition.ESCALATE
    if confidence >= 0.85:
        return ConfidenceDisposition.HIGH_CONFIDENCE
    if confidence >= 0.65:
        return ConfidenceDisposition.REVIEW_REQUIRED
    return ConfidenceDisposition.ESCALATE


@dataclass(frozen=True)
class JevChoiceResult:
    choice: str
    probabilities: tuple[tuple[str, float], ...]
    confidence: float
    disposition: ConfidenceDisposition

    @classmethod
    def parse(cls, payload: Mapping[str, Any], answers: Sequence[str]) -> "JevChoiceResult":
        if not isinstance(payload, Mapping):
            raise ValueError("Jev result must be an object")
        allowed = tuple(str(answer) for answer in answers)
        choice = str(payload.get("choice") or "")
        if choice not in allowed:
            raise ValueError("Jev choice is outside the bounded answer schema")
        raw_probabilities = payload.get("probabilities")
        if not isinstance(raw_probabilities, Mapping) or set(raw_probabilities) != set(allowed):
            raise ValueError("Jev probabilities must cover the bounded answer schema exactly")
        probabilities = tuple(sorted((str(key), float(value)) for key, value in raw_probabilities.items()))
        probability_map = dict(probabilities)
        if abs(sum(probability_map.values()) - 1.0) > 0.02:
            raise ValueError("Jev probabilities must sum to one")
        confidence = float(payload.get("confidence"))
        contradictory = max(probability_map, key=probability_map.get) != choice
        disposition = confidence_disposition(
            confidence, probabilities=probability_map, contradictory=contradictory
        )
        return cls(choice, probabilities, confidence, disposition)


def _sanitize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): "[REDACTED]" if _SECRET_KEYS.search(str(key)) else _sanitize(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_sanitize(item) for item in value]
    if isinstance(value, str):
        value = re.sub(r"(?i)bearer\s+[A-Za-z0-9._-]+", "Bearer [REDACTED]", value)
        value = re.sub(r"\b(?:sk|ts)-[A-Za-z0-9._-]{8,}\b", "[REDACTED]", value)
    return value


@dataclass(frozen=True)
class JevDecisionRecord:
    decision_id: str
    task: str
    answer_schema: tuple[str, ...]
    evidence_references: tuple[str, ...]
    result: str
    confidence: float
    codex_action: str
    escalated: bool
    final_engineering_disposition: str
    repository_capture: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.decision_id.strip() or not self.task.strip():
            raise ValueError("decision id and task are required")
        if self.result not in self.answer_schema:
            raise ValueError("result must belong to the bounded answer schema")
        confidence_disposition(self.confidence)
        if not self.repository_capture:
            raise ValueError("adopted decisions require a repository-owned capture")

    def sanitized_dict(self) -> dict[str, Any]:
        return _sanitize({
            "decision_id": self.decision_id,
            "task": self.task,
            "bounded_answer_schema": list(self.answer_schema),
            "evidence_fixture_references": list(self.evidence_references),
            "jev_result": self.result,
            "confidence": self.confidence,
            "codex_action": self.codex_action,
            "escalated": self.escalated,
            "final_engineering_disposition": self.final_engineering_disposition,
            "repository_capture": list(self.repository_capture),
        })

    def canonical_json(self) -> str:
        return json.dumps(self.sanitized_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


__all__ = [
    "ConfidenceDisposition", "JevChoiceResult", "JevDecisionRecord",
    "confidence_disposition",
]
