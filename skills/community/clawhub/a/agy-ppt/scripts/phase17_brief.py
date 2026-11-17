#!/usr/bin/env python3
"""Phase 17.1 deterministic Presentation Brief and audience boundary."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from phase16_editorial import PresentationMode


ERROR_BRIEF_INVALID = "PHASE17_BRIEF_INVALID"


class PresentationBriefError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class ContextProvenance(str, Enum):
    USER_PROVIDED = "USER_PROVIDED"
    SAFELY_DERIVED = "SAFELY_DERIVED"


class DesiredOutcome(str, Enum):
    KNOW = "KNOW"
    UNDERSTAND = "UNDERSTAND"
    REMEMBER = "REMEMBER"
    DECIDE = "DECIDE"
    ACT = "ACT"


_OUTCOME_ORDER = {outcome: index for index, outcome in enumerate(DesiredOutcome)}


@dataclass(frozen=True)
class BriefValue:
    value: str
    provenance: ContextProvenance = ContextProvenance.USER_PROVIDED

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "brief value must be non-empty text")
        if not isinstance(self.provenance, ContextProvenance):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "brief provenance is invalid")
        object.__setattr__(self, "value", self.value.strip())

    def internal_dict(self) -> dict[str, str]:
        return {"value": self.value, "provenance": self.provenance.value}


@dataclass(frozen=True)
class OutcomeIntent:
    outcome: DesiredOutcome
    provenance: ContextProvenance = ContextProvenance.USER_PROVIDED

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, DesiredOutcome) or not isinstance(self.provenance, ContextProvenance):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "desired outcome is invalid")

    def internal_dict(self) -> dict[str, str]:
        return {"outcome": self.outcome.value, "provenance": self.provenance.value}


@dataclass(frozen=True)
class BriefConstraint:
    name: str
    value: str
    provenance: ContextProvenance = ContextProvenance.USER_PROVIDED

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "constraint name is required")
        if not isinstance(self.value, str) or not self.value.strip():
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "constraint value is required")
        if not isinstance(self.provenance, ContextProvenance):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "constraint provenance is invalid")
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "value", self.value.strip())

    def internal_dict(self) -> dict[str, str]:
        return {"name": self.name, "value": self.value, "provenance": self.provenance.value}


@dataclass(frozen=True)
class PresentationBrief:
    audience: BriefValue
    purpose: BriefValue
    desired_outcomes: tuple[OutcomeIntent, ...]
    mode: PresentationMode
    context: BriefValue | None = None
    duration_seconds: int | None = None
    audience_knowledge: BriefValue | None = None
    constraints: tuple[BriefConstraint, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.audience, BriefValue) or not isinstance(self.purpose, BriefValue):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "audience and purpose are required")
        if not isinstance(self.mode, PresentationMode):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "Phase 16 presentation mode is required")
        if self.context is not None and not isinstance(self.context, BriefValue):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "presentation context is invalid")
        if self.audience_knowledge is not None and not isinstance(self.audience_knowledge, BriefValue):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "audience knowledge is invalid")
        if self.duration_seconds is not None and (
            not isinstance(self.duration_seconds, int)
            or isinstance(self.duration_seconds, bool)
            or self.duration_seconds <= 0
        ):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "duration must be positive whole seconds")

        outcomes = tuple(self.desired_outcomes)
        if not outcomes or any(not isinstance(item, OutcomeIntent) for item in outcomes):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "at least one desired outcome is required")
        by_outcome: dict[DesiredOutcome, OutcomeIntent] = {}
        for item in outcomes:
            existing = by_outcome.get(item.outcome)
            if existing is not None and existing != item:
                raise PresentationBriefError(ERROR_BRIEF_INVALID, "outcome provenance is ambiguous")
            by_outcome[item.outcome] = item
        object.__setattr__(
            self,
            "desired_outcomes",
            tuple(sorted(by_outcome.values(), key=lambda item: _OUTCOME_ORDER[item.outcome])),
        )

        constraints = tuple(self.constraints)
        if any(not isinstance(item, BriefConstraint) for item in constraints):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "brief constraint is invalid")
        keys = [(item.name, item.value, item.provenance.value) for item in constraints]
        if len(keys) != len(set(keys)):
            raise PresentationBriefError(ERROR_BRIEF_INVALID, "duplicate constraints are invalid")
        object.__setattr__(self, "constraints", tuple(sorted(constraints, key=lambda item: (item.name, item.value, item.provenance.value))))

    def internal_dict(self) -> dict[str, object]:
        return {
            "audience": self.audience.internal_dict(),
            "purpose": self.purpose.internal_dict(),
            "desired_outcomes": [item.internal_dict() for item in self.desired_outcomes],
            "presentation_mode": self.mode.value,
            "context": self.context.internal_dict() if self.context else None,
            "duration_seconds": self.duration_seconds,
            "audience_knowledge": self.audience_knowledge.internal_dict() if self.audience_knowledge else None,
            "constraints": [item.internal_dict() for item in self.constraints],
        }

    def canonical_json(self) -> str:
        return json.dumps(self.internal_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


@dataclass(frozen=True)
class SafeContextInference:
    audience: BriefValue | None = None
    context: BriefValue | None = None


_SAFE_CONTEXT_RULES = (
    (("BNI", "商務夥伴", "商務交流"), "business-networking participants", "business networking presentation"),
    (("董事會", "board review", "executive review"), "organizational decision-makers", "executive review"),
    (("新進人員", "training participants", "學員"), "training participants", "training session"),
)


def infer_obvious_context(request: str) -> SafeContextInference:
    """Derive only allowlisted, non-sensitive communication context from a request."""
    if not isinstance(request, str) or not request.strip():
        raise PresentationBriefError(ERROR_BRIEF_INVALID, "request text is required")
    folded = request.casefold()
    for markers, audience, context in _SAFE_CONTEXT_RULES:
        if any(marker.casefold() in folded for marker in markers):
            return SafeContextInference(
                BriefValue(audience, ContextProvenance.SAFELY_DERIVED),
                BriefValue(context, ContextProvenance.SAFELY_DERIVED),
            )
    return SafeContextInference()


def normalize_outcomes(
    outcomes: Iterable[DesiredOutcome],
    provenance: ContextProvenance = ContextProvenance.USER_PROVIDED,
) -> tuple[OutcomeIntent, ...]:
    return tuple(OutcomeIntent(outcome, provenance) for outcome in outcomes)


def user_facing_brief_message() -> str:
    return "我會依您的對象、目的與場合規劃大綱，先請您確認內容方向。"


__all__ = [
    "ERROR_BRIEF_INVALID", "BriefConstraint", "BriefValue", "ContextProvenance",
    "DesiredOutcome", "OutcomeIntent", "PresentationBrief", "PresentationBriefError",
    "SafeContextInference", "infer_obvious_context", "normalize_outcomes",
    "user_facing_brief_message",
]
