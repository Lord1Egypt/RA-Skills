"""Immutable Phase 15.5 OCR-to-Phase-12 grounding envelopes."""
from __future__ import annotations

from dataclasses import dataclass
import json
import re
from types import MappingProxyType
from typing import Any, Mapping

from ocr_providers import OCREvidence

_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_SOURCE_ID = re.compile(r"^src_[A-Za-z0-9._-]+$")


class GroundingTranslationError(Exception):
    """Stable additive translation error; never a provider or Phase 12 error."""

    def __init__(self, message: str, error_code: str):
        super().__init__(message)
        self.error_code = error_code


ERROR_SOURCE_MISMATCH = "OCR_GROUNDING_SOURCE_MISMATCH"
ERROR_LOCATOR_INVALID = "OCR_GROUNDING_LOCATOR_INVALID"
ERROR_EVIDENCE_INVALID = "OCR_GROUNDING_EVIDENCE_INVALID"
ERROR_UNSUPPORTED = "OCR_GROUNDING_TRANSLATION_UNSUPPORTED"
ERROR_TRANSACTION_INVALID = "OCR_GROUNDING_TRANSACTION_INVALID"
ERROR_CODES = frozenset({
    ERROR_SOURCE_MISMATCH, ERROR_LOCATOR_INVALID, ERROR_EVIDENCE_INVALID,
    ERROR_UNSUPPORTED, ERROR_TRANSACTION_INVALID,
})


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    return value


def _canonical(value: Any) -> str:
    return json.dumps(_plain(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


@dataclass(frozen=True)
class GroundingPage:
    """One source-ordered Phase 12-compatible grounding input page."""

    source_id: str
    source_digest: str
    locator: Mapping[str, Any]
    text: str
    route: str
    native_locator: Mapping[str, Any]
    ocr_evidence: OCREvidence | None = None
    derived_provenance: Any = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not _SOURCE_ID.fullmatch(self.source_id):
            raise GroundingTranslationError("source_id is invalid", ERROR_SOURCE_MISMATCH)
        if not isinstance(self.source_digest, str) or not _DIGEST.fullmatch(self.source_digest):
            raise GroundingTranslationError("source_digest is invalid", ERROR_SOURCE_MISMATCH)
        if self.route not in ("TEXT", "OCR"):
            raise GroundingTranslationError("route is invalid", ERROR_TRANSACTION_INVALID)
        if not isinstance(self.text, str):
            raise GroundingTranslationError("grounding text must be a string", ERROR_EVIDENCE_INVALID)
        if not isinstance(self.locator, Mapping) or not isinstance(self.native_locator, Mapping):
            raise GroundingTranslationError("locators must be mappings", ERROR_LOCATOR_INVALID)
        object.__setattr__(self, "locator", _freeze(self.locator))
        object.__setattr__(self, "native_locator", _freeze(self.native_locator))
        if self.derived_provenance is not None and not hasattr(self.derived_provenance, "to_dict"):
            raise GroundingTranslationError("derived provenance is not serializable", ERROR_EVIDENCE_INVALID)
        if self.route == "TEXT" and self.ocr_evidence is not None:
            raise GroundingTranslationError("TEXT pages cannot carry OCR evidence", ERROR_EVIDENCE_INVALID)
        if self.route == "OCR" and not isinstance(self.ocr_evidence, OCREvidence):
            raise GroundingTranslationError("OCR pages require OCREvidence", ERROR_EVIDENCE_INVALID)

    def to_dict(self) -> dict[str, Any]:
        result = {
            "locator": _plain(self.locator),
            "native_locator": _plain(self.native_locator),
            "route": self.route,
            "source_digest": self.source_digest,
            "source_id": self.source_id,
            "text": self.text,
        }
        if self.ocr_evidence is not None:
            result["ocr_evidence"] = self.ocr_evidence.to_dict()
        if self.derived_provenance is not None:
            result["derived_provenance"] = self.derived_provenance.to_dict()
        return result


@dataclass(frozen=True)
class GroundingDocument:
    """Complete source-ordered translation; no partial document is valid."""

    source_id: str
    source_digest: str
    pages: tuple[GroundingPage, ...]

    def __post_init__(self) -> None:
        if not _SOURCE_ID.fullmatch(self.source_id or "") or not _DIGEST.fullmatch(self.source_digest or "") or not self.pages:
            raise GroundingTranslationError("grounding document identity is invalid", ERROR_TRANSACTION_INVALID)
        object.__setattr__(self, "pages", tuple(self.pages))
        for page in self.pages:
            if page.source_id != self.source_id or page.source_digest != self.source_digest:
                raise GroundingTranslationError("grounding page source identity differs", ERROR_SOURCE_MISMATCH)
        pdf_pages = [p.locator.get("start") for p in self.pages if p.locator.get("kind") == "page"]
        if (pdf_pages and pdf_pages != sorted(pdf_pages)) or len(pdf_pages) != len(set(pdf_pages)):
            raise GroundingTranslationError("grounding pages are not source ordered", ERROR_TRANSACTION_INVALID)

    def to_dict(self) -> dict[str, Any]:
        return {"pages": [page.to_dict() for page in self.pages], "source_digest": self.source_digest, "source_id": self.source_id}

    def to_json(self) -> str:
        return _canonical(self.to_dict())
