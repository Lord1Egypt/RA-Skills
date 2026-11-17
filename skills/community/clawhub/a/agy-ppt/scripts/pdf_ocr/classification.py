"""Mechanical Phase 15.2 PDF page classification."""

from __future__ import annotations

from .errors import PDFOCRError, PDFOCRErrorCode
from .models import PageClassification


def classify_page_text(extracted_text: str) -> PageClassification:
    """Classify by Unicode whitespace presence without changing the input text."""

    if not isinstance(extracted_text, str):
        raise PDFOCRError(
            "extracted page text must be a string",
            PDFOCRErrorCode.INPUT_INVALID,
        )
    if extracted_text.strip() != "":
        return PageClassification.SEARCHABLE
    return PageClassification.SCANNED
