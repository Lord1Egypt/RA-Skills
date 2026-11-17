"""Mechanical translation from frozen Phase 15 OCR results to Phase 12 locators."""
from __future__ import annotations

import re
from typing import Any, Mapping

from source_grounding import compute_source_digest, validate_locator
from ocr_providers import OCREvidence, validate_evidence
from pdf_ocr.models import PDFPageIdentity, PDFSourceIdentity
from pdf_ocr.orchestration import MixedPDFExecutionResult, OCRPageExecution, TextPageExecution
from image_ocr.models import ImagePreparationProvenance
from image_ocr.orchestration import StandaloneImageOCRResult

from .models import (
    ERROR_EVIDENCE_INVALID, ERROR_LOCATOR_INVALID, ERROR_SOURCE_MISMATCH,
    ERROR_TRANSACTION_INVALID, ERROR_UNSUPPORTED, GroundingDocument,
    GroundingPage, GroundingTranslationError,
)

_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_IMAGE_NATIVE = {"kind": "image", "ordinal": 1}
_IMAGE_PHASE12 = {"kind": "generic", "label": "image:1-of-1"}


def _checked_digest(raw: bytes, expected: str, label: str) -> None:
    if not isinstance(raw, bytes) or not _DIGEST.fullmatch(expected or "") or compute_source_digest(raw) != expected:
        raise GroundingTranslationError(f"{label} source digest mismatch", ERROR_SOURCE_MISMATCH)


def _validate_phase12(locator: Mapping[str, Any]) -> None:
    if not isinstance(locator, Mapping) or validate_locator(dict(locator)):
        raise GroundingTranslationError("translated locator is not accepted by Phase 12", ERROR_LOCATOR_INVALID)


def _validate_evidence(evidence: OCREvidence, source_id: str, source_digest: str, native_locator: Mapping[str, Any], text: str) -> None:
    try:
        validate_evidence(evidence)
    except Exception as exc:
        raise GroundingTranslationError("OCR evidence is invalid", ERROR_EVIDENCE_INVALID) from exc
    if evidence.source_id != source_id or evidence.source_digest != source_digest:
        raise GroundingTranslationError("OCR evidence source identity differs", ERROR_SOURCE_MISMATCH)
    if len(evidence.pages) != 1 or dict(evidence.pages[0].locator) != dict(native_locator):
        raise GroundingTranslationError("OCR evidence locator differs", ERROR_LOCATOR_INVALID)
    if evidence.pages[0].raw_text != text:
        raise GroundingTranslationError("OCR raw_text was changed", ERROR_EVIDENCE_INVALID)


def translate_pdf_ocr_page(
    source: PDFSourceIdentity,
    page: PDFPageIdentity,
    evidence: OCREvidence,
    raster_provenance: Any = None,
) -> GroundingPage:
    """Map one completed scanned PDF page without executing any OCR machinery."""
    if not isinstance(source, PDFSourceIdentity) or not isinstance(page, PDFPageIdentity):
        raise GroundingTranslationError("PDF identity is invalid", ERROR_TRANSACTION_INVALID)
    native = page.to_dict()
    if not isinstance(evidence, OCREvidence) or not evidence.pages:
        raise GroundingTranslationError("OCR evidence has no page", ERROR_EVIDENCE_INVALID)
    _validate_evidence(evidence, source.source_id, source.source_digest, native, evidence.pages[0].raw_text)
    locator = {"kind": "page", "start": page.page, "end": page.page}
    _validate_phase12(locator)
    return GroundingPage(source.source_id, source.source_digest, locator, evidence.pages[0].raw_text, "OCR", native, evidence, raster_provenance)


def translate_pdf_text_page(source: PDFSourceIdentity, page: PDFPageIdentity, raw_text: str) -> GroundingPage:
    """Retain an existing searchable page on the frozen Phase 13 path."""
    if not isinstance(source, PDFSourceIdentity) or not isinstance(page, PDFPageIdentity) or not isinstance(raw_text, str):
        raise GroundingTranslationError("PDF text page is invalid", ERROR_TRANSACTION_INVALID)
    locator = {"kind": "page", "start": page.page, "end": page.page}
    _validate_phase12(locator)
    return GroundingPage(source.source_id, source.source_digest, locator, raw_text, "TEXT", page.to_dict())


def translate_mixed_pdf(result: MixedPDFExecutionResult, raw_pdf_bytes: bytes | None = None) -> GroundingDocument:
    """Translate a complete Phase 15.2 result in source order; never partially."""
    if not isinstance(result, MixedPDFExecutionResult):
        raise GroundingTranslationError("mixed PDF result is invalid", ERROR_TRANSACTION_INVALID)
    if raw_pdf_bytes is not None:
        _checked_digest(raw_pdf_bytes, result.source.source_digest, "PDF")
    pages: list[GroundingPage] = []
    for item in result.pages:
        if isinstance(item, TextPageExecution):
            pages.append(translate_pdf_text_page(item.source, item.page, item.raw_text))
        elif isinstance(item, OCRPageExecution):
            pages.append(translate_pdf_ocr_page(item.source, item.page, item.evidence, item.raster_provenance))
        else:
            raise GroundingTranslationError("unknown PDF execution page", ERROR_TRANSACTION_INVALID)
    return GroundingDocument(result.source.source_id, result.source.source_digest, tuple(pages))


def translate_standalone_image(result: StandaloneImageOCRResult, raw_image_bytes: bytes | None = None) -> GroundingPage:
    """Map the one-image OCR-native locator to frozen generic/image:1-of-1."""
    if not isinstance(result, StandaloneImageOCRResult):
        raise GroundingTranslationError("standalone image result is invalid", ERROR_TRANSACTION_INVALID)
    if raw_image_bytes is not None:
        _checked_digest(raw_image_bytes, result.source.source_digest, "image")
    if not result.evidence.pages:
        raise GroundingTranslationError("OCR evidence has no image page", ERROR_EVIDENCE_INVALID)
    native = dict(_IMAGE_NATIVE)
    _validate_evidence(result.evidence, result.source.source_id, result.source.source_digest, native, result.evidence.pages[0].raw_text)
    _validate_phase12(_IMAGE_PHASE12)
    if not isinstance(result.preparation, ImagePreparationProvenance):
        raise GroundingTranslationError("image preparation provenance is invalid", ERROR_EVIDENCE_INVALID)
    return GroundingPage(result.source.source_id, result.source.source_digest, _IMAGE_PHASE12, result.evidence.pages[0].raw_text, "OCR", native, result.evidence, result.preparation)
