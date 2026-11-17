"""Atomic standalone-image OCR orchestration for Phase 15.3."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from ocr_providers import OCRProvider, OCRRequest, OCREvidence, execute_with_fallback, validate_evidence
from ocr_providers.errors import OCRError
from source_grounding import compute_source_digest

from .errors import ImageOCRError, ImageOCRErrorCode
from .models import ImagePreparationConfiguration, ImagePreparationProvenance, ImageResourceLimits, ImageSourceIdentity
from .preparer import ImagePreparationRequest, ImagePreparer


_IMAGE_LOCATOR = {"kind": "image", "ordinal": 1}


@dataclass(frozen=True)
class StandaloneImageOCRResult:
    source: ImageSourceIdentity
    preparation: ImagePreparationProvenance
    evidence: OCREvidence

    def __post_init__(self) -> None:
        if not isinstance(self.source, ImageSourceIdentity) or not isinstance(self.preparation, ImagePreparationProvenance) or not isinstance(self.evidence, OCREvidence):
            raise OCRError("standalone image result contract is invalid", "OCR_PROVIDER_CONTRACT_INVALID")
        validate_evidence(self.evidence)
        if self.evidence.source_id != self.source.source_id or self.evidence.source_digest != self.source.source_digest:
            raise OCRError("OCR evidence source identity does not match original image", "OCR_PROVIDER_CONTRACT_INVALID")
        if len(self.evidence.pages) != 1 or dict(self.evidence.pages[0].locator) != _IMAGE_LOCATOR:
            raise OCRError("OCR evidence locator does not identify image 1 of 1", "OCR_PROVIDER_CONTRACT_INVALID")
        if not isinstance(self.evidence.pages, tuple) or not isinstance(self.evidence.model_manifest, tuple):
            raise OCRError("OCR evidence must be immutably materialized", "OCR_PROVIDER_CONTRACT_INVALID")

    @property
    def raw_text(self) -> str:
        return self.evidence.pages[0].raw_text

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source.to_dict(), "locator": dict(_IMAGE_LOCATOR), "preparation": self.preparation.to_dict(), "evidence": self.evidence.to_dict()}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def execute_standalone_image_ocr(
    raw_image_bytes: bytes,
    source_id: str,
    preparer: ImagePreparer,
    providers: Mapping[str, OCRProvider],
    *,
    configuration: ImagePreparationConfiguration | None = None,
    resource_limits: ImageResourceLimits | None = None,
    explicit: str | None = None,
    project: str | None = None,
    user: str | None = None,
    default: str = "tesseract",
    allow_fallback: bool = False,
    language_config: Mapping[str, Any] | None = None,
    execution_config: Mapping[str, Any] | None = None,
) -> StandaloneImageOCRResult:
    """Prepare one image, then execute frozen provider semantics atomically."""

    if not isinstance(raw_image_bytes, bytes) or not isinstance(source_id, str) or not source_id:
        raise ImageOCRError("standalone image transaction input is invalid", ImageOCRErrorCode.INPUT_INVALID)
    if not isinstance(preparer, ImagePreparer):
        raise ImageOCRError("image preparer boundary is invalid", ImageOCRErrorCode.DECODE_FAILED)
    source = ImageSourceIdentity(source_id, compute_source_digest(raw_image_bytes))
    prepared = preparer.prepare(ImagePreparationRequest(
        raw_image_bytes,
        source,
        configuration or ImagePreparationConfiguration(),
        resource_limits or ImageResourceLimits(),
    ))
    request = OCRRequest(
        image_bytes=prepared.png_bytes,
        source_id=source.source_id,
        source_digest=source.source_digest,
        locator=dict(_IMAGE_LOCATOR),
        language_config=dict(language_config or {}),
        execution_config=dict(execution_config or {}),
    )
    evidence = execute_with_fallback(
        providers,
        request,
        explicit=explicit,
        project=project,
        user=user,
        default=default,
        allow_fallback=allow_fallback,
    )
    return StandaloneImageOCRResult(source, prepared.provenance, evidence)
