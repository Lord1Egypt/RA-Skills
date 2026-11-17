"""Stable OCR provider error taxonomy."""

class OCRError(Exception):
    def __init__(self, message: str, error_code: str, *, cause: "OCRError | None" = None):
        super().__init__(message)
        self.error_code = error_code
        self.cause = cause

ERROR_CODES = {
    "OCR_MODEL_UNAVAILABLE", "OCR_EXTRACTION_FAILED", "OCR_TEXT_UNAVAILABLE",
    "OCR_PROVIDER_NOT_FOUND", "OCR_PROVIDER_UNAVAILABLE", "OCR_PROVIDER_CONTRACT_INVALID",
    "OCR_PROVIDER_CAPABILITY_MISSING", "OCR_PROVIDER_VERSION_UNAVAILABLE",
    "OCR_PROVIDER_VERSION_UNSUPPORTED", "OCR_PROVIDER_OUTPUT_INVALID", "OCR_PROVIDER_FAILED",
    "OCR_FALLBACK_NOT_ALLOWED", "OCR_LANGUAGE_UNSUPPORTED", "OCR_SOURCE_CHANGED", "OCR_MODEL_CHANGED",
}
