"""Stable Phase 15.3 standalone-image OCR errors."""

from __future__ import annotations

from enum import Enum


class ImageOCRErrorCode(str, Enum):
    FORMAT_UNSUPPORTED = "OCR_IMAGE_FORMAT_UNSUPPORTED"
    INPUT_INVALID = "OCR_IMAGE_INPUT_INVALID"
    RESOURCE_LIMIT_EXCEEDED = "OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED"
    DECODE_FAILED = "OCR_IMAGE_DECODE_FAILED"
    CLEANUP_FAILED = "OCR_IMAGE_CLEANUP_FAILED"


ERROR_CODES = frozenset(code.value for code in ImageOCRErrorCode)


class ImageOCRError(Exception):
    """A deterministic image-ingestion error outside provider fallback."""

    def __init__(self, message: str, error_code: ImageOCRErrorCode | str):
        try:
            code = ImageOCRErrorCode(error_code)
        except ValueError as exc:
            raise ValueError(f"unsupported Phase 15.3 error code: {error_code!r}") from exc
        super().__init__(message)
        self.error_code = code.value

    @property
    def provider_fallback_eligible(self) -> bool:
        return False
