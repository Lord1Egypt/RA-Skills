"""Stable Phase 15.2 PDF OCR orchestration errors."""

from __future__ import annotations

from enum import Enum


class PDFOCRErrorCode(str, Enum):
    """Public/internal error identities committed by the Phase 15.2 contract."""

    PASSWORD_REQUIRED = "OCR_PDF_PASSWORD_REQUIRED"
    INPUT_INVALID = "OCR_PDF_INPUT_INVALID"
    PAGE_INVALID = "OCR_PDF_PAGE_INVALID"
    RESOURCE_LIMIT_EXCEEDED = "OCR_PDF_RESOURCE_LIMIT_EXCEEDED"
    CLEANUP_FAILED = "OCR_PDF_CLEANUP_FAILED"
    RASTERIZATION_FAILED = "OCR_RASTERIZATION_FAILED"


ERROR_CODES = frozenset(code.value for code in PDFOCRErrorCode)


class PDFOCRError(Exception):
    """A deterministic Phase 15.2 error outside provider fallback semantics."""

    def __init__(self, message: str, error_code: PDFOCRErrorCode | str):
        try:
            code = PDFOCRErrorCode(error_code)
        except ValueError as exc:
            raise ValueError(f"unsupported Phase 15.2 error code: {error_code!r}") from exc
        super().__init__(message)
        self.error_code = code.value

    @property
    def provider_fallback_eligible(self) -> bool:
        """PDF admission/resource/raster errors never enter provider fallback."""

        return False
