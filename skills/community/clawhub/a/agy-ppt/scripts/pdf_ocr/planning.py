"""Pure deterministic mixed-PDF planning for Phase 15.2-B."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Iterable

from .classification import classify_page_text
from .errors import PDFOCRError, PDFOCRErrorCode
from .models import PDFPageIdentity, PDFSourceIdentity, PageClassification


class PageRoute(str, Enum):
    TEXT = "TEXT"
    OCR = "OCR"


@dataclass(frozen=True)
class PDFPageInput:
    """Internal input derived from deterministic per-page text extraction."""

    source: PDFSourceIdentity
    page: PDFPageIdentity
    extracted_text: str

    def __post_init__(self) -> None:
        if not isinstance(self.source, PDFSourceIdentity):
            raise PDFOCRError("page source identity is invalid", PDFOCRErrorCode.INPUT_INVALID)
        if not isinstance(self.page, PDFPageIdentity):
            raise PDFOCRError("page identity is invalid", PDFOCRErrorCode.PAGE_INVALID)
        if not isinstance(self.extracted_text, str):
            raise PDFOCRError("extracted page text must be a string", PDFOCRErrorCode.INPUT_INVALID)


@dataclass(frozen=True)
class PDFPagePlan:
    """One planned route; no text, raster, or OCR execution occurs here."""

    source: PDFSourceIdentity
    page: PDFPageIdentity
    extracted_text: str
    classification: PageClassification
    route: PageRoute

    def __post_init__(self) -> None:
        if not isinstance(self.source, PDFSourceIdentity):
            raise PDFOCRError("planned source identity is invalid", PDFOCRErrorCode.INPUT_INVALID)
        if not isinstance(self.page, PDFPageIdentity):
            raise PDFOCRError("planned page identity is invalid", PDFOCRErrorCode.PAGE_INVALID)
        if not isinstance(self.extracted_text, str):
            raise PDFOCRError("planned extracted text must be a string", PDFOCRErrorCode.INPUT_INVALID)
        expected_route = (
            PageRoute.TEXT
            if self.classification is PageClassification.SEARCHABLE
            else PageRoute.OCR
            if self.classification is PageClassification.SCANNED
            else None
        )
        if expected_route is None or self.route is not expected_route:
            raise PDFOCRError("classification and route are inconsistent", PDFOCRErrorCode.INPUT_INVALID)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.to_dict(),
            "locator": self.page.to_dict(),
            "extracted_text": self.extracted_text,
            "classification": self.classification.value,
            "route": self.route.value,
        }


@dataclass(frozen=True)
class MixedPDFPlan:
    """Complete source-ordered route plan for one original PDF."""

    source: PDFSourceIdentity
    pages: tuple[PDFPagePlan, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "pages", tuple(self.pages))
        if not isinstance(self.source, PDFSourceIdentity):
            raise PDFOCRError("plan source identity is invalid", PDFOCRErrorCode.INPUT_INVALID)
        if not self.pages:
            raise PDFOCRError("complete PDF plan requires pages", PDFOCRErrorCode.INPUT_INVALID)
        if any(not isinstance(item, PDFPagePlan) for item in self.pages):
            raise PDFOCRError("plan entries must be PDFPagePlan values", PDFOCRErrorCode.INPUT_INVALID)
        total_pages = self.pages[0].page.total_pages
        expected_pages = tuple(range(1, total_pages + 1))
        actual_pages = tuple(item.page.page for item in self.pages)
        if actual_pages != expected_pages:
            raise PDFOCRError(
                "PDF plan must contain each source page exactly once in ascending order",
                PDFOCRErrorCode.INPUT_INVALID,
            )
        for item in self.pages:
            if item.source != self.source:
                raise PDFOCRError("all plan pages must share one source identity", PDFOCRErrorCode.INPUT_INVALID)
            if item.page.total_pages != total_pages:
                raise PDFOCRError("all page identities must share total_pages", PDFOCRErrorCode.INPUT_INVALID)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.to_dict(),
            "pages": [page.to_dict() for page in self.pages],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )


def plan_pdf_pages(pages: Iterable[PDFPageInput]) -> MixedPDFPlan:
    """Build a complete source-ordered plan without executing any route."""

    inputs = tuple(pages)
    if not inputs:
        raise PDFOCRError("complete PDF plan requires pages", PDFOCRErrorCode.INPUT_INVALID)
    if any(not isinstance(item, PDFPageInput) for item in inputs):
        raise PDFOCRError("planner inputs must be PDFPageInput values", PDFOCRErrorCode.INPUT_INVALID)

    source = inputs[0].source
    total_pages = inputs[0].page.total_pages
    for item in inputs:
        if item.source != source:
            raise PDFOCRError("planner cannot mix source identities", PDFOCRErrorCode.INPUT_INVALID)
        if item.page.total_pages != total_pages:
            raise PDFOCRError("planner cannot mix total_pages values", PDFOCRErrorCode.INPUT_INVALID)

    actual_pages = tuple(item.page.page for item in inputs)
    expected_pages = tuple(range(1, total_pages + 1))
    if tuple(sorted(actual_pages)) != expected_pages:
        raise PDFOCRError(
            "planner requires each page in 1..total_pages exactly once",
            PDFOCRErrorCode.INPUT_INVALID,
        )

    planned: list[PDFPagePlan] = []
    for item in sorted(inputs, key=lambda value: value.page.page):
        classification = classify_page_text(item.extracted_text)
        route = PageRoute.TEXT if classification is PageClassification.SEARCHABLE else PageRoute.OCR
        planned.append(
            PDFPagePlan(
                source=item.source,
                page=item.page,
                extracted_text=item.extracted_text,
                classification=classification,
                route=route,
            )
        )
    return MixedPDFPlan(source=source, pages=tuple(planned))
