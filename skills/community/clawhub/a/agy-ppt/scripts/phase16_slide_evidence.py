#!/usr/bin/env python3
"""Phase 16.3 slide-level evidence planning and deterministic drift checks."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from phase16_claims import Claim, EvidenceBinding


ERROR_SLIDE_EVIDENCE_INVALID = "PHASE16_SLIDE_EVIDENCE_INVALID"
ERROR_FACTUAL_DRIFT = "PHASE16_EVIDENCE_BOUND_FACTUAL_DRIFT"
ERROR_UNSUPPORTED_EXPANSION = "PHASE16_UNSUPPORTED_FACTUAL_EXPANSION"

_FACT_TOKEN = re.compile(r"(?<![\w.])(?:\d{4}|\d+(?:\.\d+)?%?)(?!\w)")


class SlideEvidenceError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def factual_tokens(text: str) -> tuple[str, ...]:
    return tuple(sorted(set(_FACT_TOKEN.findall(text))))


@dataclass(frozen=True)
class MaterialClaim:
    claim: Claim
    material: bool = True
    protected_terms: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.claim, Claim) or not isinstance(self.material, bool):
            raise SlideEvidenceError(ERROR_SLIDE_EVIDENCE_INVALID, "material claim is invalid")
        terms = tuple(term.strip() for term in self.protected_terms if isinstance(term, str) and term.strip())
        object.__setattr__(self, "protected_terms", terms)

    @property
    def facts(self) -> tuple[str, ...]:
        return tuple(sorted(set(factual_tokens(self.claim.text) + self.protected_terms)))


@dataclass(frozen=True)
class WorkerInstruction:
    """Narrow renderer payload: approved copy, without evidence mechanics."""

    slide_id: str
    approved_content: tuple[str, ...]
    constraints: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"approved_content": list(self.approved_content), "constraints": list(self.constraints), "slide_id": self.slide_id}


@dataclass(frozen=True)
class SlideEvidencePlan:
    plan_id: str
    slide_id: str
    claims: tuple[MaterialClaim, ...]
    evidence_snapshot: Mapping[str, tuple[EvidenceBinding, ...]]

    @classmethod
    def create(cls, slide_id: str, claims: Iterable[MaterialClaim]) -> "SlideEvidencePlan":
        clean = tuple(claims)
        if not re.fullmatch(r"slide_\d+", slide_id or "") or not clean:
            raise SlideEvidenceError(ERROR_SLIDE_EVIDENCE_INVALID, "slide evidence plan is invalid")
        if any(not isinstance(item, MaterialClaim) for item in clean):
            raise SlideEvidenceError(ERROR_SLIDE_EVIDENCE_INVALID, "slide claims are invalid")
        ids = [item.claim.claim_id for item in clean]
        if len(ids) != len(set(ids)):
            raise SlideEvidenceError(ERROR_SLIDE_EVIDENCE_INVALID, "duplicate claim in slide plan")
        snapshot = {
            item.claim.claim_id: tuple(item.claim.evidence)
            for item in clean
        }
        payload = {
            "claims": [{"claim": item.claim.to_dict(), "material": item.material, "protected_terms": list(item.protected_terms)} for item in clean],
            "slide_id": slide_id,
        }
        plan_id = "sp:" + hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()[:16]
        return cls(plan_id, slide_id, clean, MappingProxyType(snapshot))

    def worker_instruction(self) -> WorkerInstruction:
        return WorkerInstruction(
            self.slide_id,
            tuple(item.claim.text for item in self.claims),
            (
                "Use only approved factual content.",
                "Do not change numbers, dates, names, or factual meaning.",
                "Do not add factual assertions.",
            ),
        )

    def validate_rendered_text(self, rendered_text: str) -> None:
        if not isinstance(rendered_text, str):
            raise SlideEvidenceError(ERROR_SLIDE_EVIDENCE_INVALID, "rendered text is invalid")
        required = {
            token for item in self.claims if item.material for token in item.facts
        }
        rendered_tokens = set(factual_tokens(rendered_text))
        missing = sorted(required - rendered_tokens)
        if missing:
            raise SlideEvidenceError(ERROR_FACTUAL_DRIFT, "protected factual tokens changed: " + ", ".join(missing))
        approved_numeric = {
            token for item in self.claims for token in factual_tokens(item.claim.text)
        }
        additions = sorted(rendered_tokens - approved_numeric)
        if additions:
            raise SlideEvidenceError(ERROR_UNSUPPORTED_EXPANSION, "rendered text added factual tokens: " + ", ".join(additions))


__all__ = [
    "ERROR_FACTUAL_DRIFT", "ERROR_SLIDE_EVIDENCE_INVALID", "ERROR_UNSUPPORTED_EXPANSION",
    "MaterialClaim", "SlideEvidenceError", "SlideEvidencePlan", "WorkerInstruction", "factual_tokens",
]
