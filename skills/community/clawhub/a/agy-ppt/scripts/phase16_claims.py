#!/usr/bin/env python3
"""Internal Phase 16.1 claim and evidence contracts.

This module is additive to frozen Phase 12.  Evidence bindings reference the
existing SourceInventory identities and locators exactly; they never create a
second locator system or persist a public schema.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from source_grounding import SourceInventory, validate_locator


ERROR_CLAIM_INVALID = "PHASE16_CLAIM_INVALID"
ERROR_EVIDENCE_REQUIRED = "PHASE16_EVIDENCE_REQUIRED"
ERROR_EVIDENCE_REFERENCE_INVALID = "PHASE16_EVIDENCE_REFERENCE_INVALID"
ERROR_SOURCE_MISMATCH = "PHASE16_EVIDENCE_SOURCE_MISMATCH"
ERROR_LOCATOR_MISMATCH = "PHASE16_EVIDENCE_LOCATOR_MISMATCH"


class ClaimContractError(Exception):
    """Stable machine-readable Phase 16 contract failure."""

    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class ContentOrigin(str, Enum):
    SOURCE_GROUNDED = "SOURCE_GROUNDED"
    USER_PROVIDED = "USER_PROVIDED"
    AGY_SYNTHESIS = "AGY_SYNTHESIS"


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _freeze(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType({key: _freeze(item) if isinstance(item, Mapping) else item for key, item in value.items()})


def _canonical(value: Any) -> str:
    try:
        return json.dumps(_plain(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ClaimContractError(ERROR_CLAIM_INVALID, "claim data must be deterministic JSON") from exc


@dataclass(frozen=True)
class EvidenceBinding:
    """Exact reference to one existing Phase 12 source unit."""

    source_id: str
    source_digest: str | None
    unit_id: str
    locator: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not all(isinstance(value, str) and value for value in (self.source_id, self.unit_id)):
            raise ClaimContractError(ERROR_EVIDENCE_REFERENCE_INVALID, "evidence identity is invalid")
        if self.source_digest is not None and (
            not isinstance(self.source_digest, str)
            or len(self.source_digest) != 64
            or any(char not in "0123456789abcdef" for char in self.source_digest)
        ):
            raise ClaimContractError(ERROR_SOURCE_MISMATCH, "source digest is invalid")
        locator = dict(self.locator) if isinstance(self.locator, Mapping) else None
        if locator is None or validate_locator(locator):
            raise ClaimContractError(ERROR_LOCATOR_MISMATCH, "evidence locator is invalid")
        object.__setattr__(self, "locator", _freeze(locator))

    def to_dict(self) -> dict[str, Any]:
        return {
            "locator": _plain(self.locator),
            "source_digest": self.source_digest,
            "source_id": self.source_id,
            "unit_id": self.unit_id,
        }


def resolve_binding(inventory: SourceInventory, binding: EvidenceBinding) -> Mapping[str, Any]:
    """Resolve a binding exactly; no fuzzy correction or fallback is allowed."""
    unit = next((item for item in inventory.data["units"] if item["unit_id"] == binding.unit_id), None)
    if unit is None:
        raise ClaimContractError(ERROR_EVIDENCE_REFERENCE_INVALID, "evidence unit does not exist")
    if unit["source_id"] != binding.source_id:
        raise ClaimContractError(ERROR_SOURCE_MISMATCH, "evidence unit belongs to another source")
    source = next((item for item in inventory.data["sources"] if item["source_id"] == binding.source_id), None)
    if source is None or source.get("source_digest") != binding.source_digest:
        raise ClaimContractError(ERROR_SOURCE_MISMATCH, "evidence source identity differs")
    if _canonical(unit["locator"]) != _canonical(binding.locator):
        raise ClaimContractError(ERROR_LOCATOR_MISMATCH, "evidence locator differs from Phase 12")
    return MappingProxyType(dict(unit))


def binding_from_unit(inventory: SourceInventory, unit_id: str) -> EvidenceBinding:
    unit = next((item for item in inventory.data["units"] if item["unit_id"] == unit_id), None)
    if unit is None:
        raise ClaimContractError(ERROR_EVIDENCE_REFERENCE_INVALID, "evidence unit does not exist")
    source = next((item for item in inventory.data["sources"] if item["source_id"] == unit["source_id"]), None)
    if source is None:
        raise ClaimContractError(ERROR_SOURCE_MISMATCH, "evidence source does not exist")
    binding = EvidenceBinding(unit["source_id"], source.get("source_digest"), unit["unit_id"], unit["locator"])
    resolve_binding(inventory, binding)
    return binding


def binding_from_grounding_page(inventory: SourceInventory, page: Any) -> EvidenceBinding:
    """Reuse a Phase 15.5 translated page through its Phase 12 locator."""
    candidates = [
        unit for unit in inventory.data["units"]
        if unit["source_id"] == getattr(page, "source_id", None)
        and _canonical(unit["locator"]) == _canonical(getattr(page, "locator", {}))
    ]
    if len(candidates) != 1:
        raise ClaimContractError(ERROR_EVIDENCE_REFERENCE_INVALID, "translated evidence does not resolve exactly")
    binding = EvidenceBinding(
        page.source_id,
        page.source_digest,
        candidates[0]["unit_id"],
        page.locator,
    )
    resolve_binding(inventory, binding)
    return binding


@dataclass(frozen=True)
class Claim:
    """Immutable claim whose origin can never be silently promoted."""

    claim_id: str
    text: str
    origin: ContentOrigin
    evidence: tuple[EvidenceBinding, ...]

    @classmethod
    def create(
        cls,
        inventory: SourceInventory,
        text: str,
        origin: ContentOrigin,
        evidence: Iterable[EvidenceBinding] = (),
    ) -> "Claim":
        if not isinstance(origin, ContentOrigin):
            raise ClaimContractError(ERROR_CLAIM_INVALID, "claim origin is invalid")
        clean_text = text.strip() if isinstance(text, str) else ""
        if not clean_text:
            raise ClaimContractError(ERROR_CLAIM_INVALID, "claim text is required")
        bindings = tuple(evidence)
        if any(not isinstance(binding, EvidenceBinding) for binding in bindings):
            raise ClaimContractError(ERROR_EVIDENCE_REFERENCE_INVALID, "evidence binding is invalid")
        if origin is ContentOrigin.SOURCE_GROUNDED and not bindings:
            raise ClaimContractError(ERROR_EVIDENCE_REQUIRED, "source-grounded claims require evidence")
        for binding in bindings:
            resolve_binding(inventory, binding)
        ordered = tuple(sorted(bindings, key=lambda item: _canonical(item.to_dict())))
        payload = {"evidence": [item.to_dict() for item in ordered], "origin": origin.value, "text": clean_text}
        claim_id = "pc:" + hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()[:16]
        return cls(claim_id, clean_text, origin, ordered)

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "evidence": [item.to_dict() for item in self.evidence],
            "origin": self.origin.value,
            "text": self.text,
        }

    def to_json(self) -> str:
        return _canonical(self.to_dict())


__all__ = [
    "Claim", "ClaimContractError", "ContentOrigin", "EvidenceBinding",
    "ERROR_CLAIM_INVALID", "ERROR_EVIDENCE_REQUIRED", "ERROR_EVIDENCE_REFERENCE_INVALID",
    "ERROR_SOURCE_MISMATCH", "ERROR_LOCATOR_MISMATCH", "binding_from_grounding_page",
    "binding_from_unit", "resolve_binding",
]
