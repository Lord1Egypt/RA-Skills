"""Sequential mixed-PDF OCR execution for Phase 15.2-D.

This module is intentionally internal.  It coordinates the renderer-neutral
Phase 15.2 contracts and the frozen Phase 15.1 provider contract without
performing grounding, text repair, or semantic reconciliation.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping

from ocr_providers import (
    OCRProvider,
    OCRRequest,
    OCREvidence,
    execute_with_fallback,
    validate_evidence,
)
from ocr_providers.errors import OCRError

from .errors import PDFOCRError, PDFOCRErrorCode
from .models import (
    PDFAdmissionResult,
    PDFPageIdentity,
    PDFSourceIdentity,
    RasterConfiguration,
    RasterProvenance,
    ResourceLimits,
    WorkerIsolationPolicy,
)
from .planning import MixedPDFPlan, PDFPagePlan, PageRoute
from .rasterizer import PDFRasterizer, RasterRequest


@dataclass(frozen=True)
class TextPageExecution:
    """A searchable page retained exactly from deterministic extraction."""

    source: PDFSourceIdentity
    page: PDFPageIdentity
    raw_text: str

    @property
    def route(self) -> PageRoute:
        return PageRoute.TEXT

    def to_dict(self) -> dict[str, Any]:
        return {
            "route": self.route.value,
            "source": self.source.to_dict(),
            "locator": self.page.to_dict(),
            "raw_text": self.raw_text,
        }


@dataclass(frozen=True)
class OCRPageExecution:
    """A scanned page's provider evidence and derived raster provenance."""

    source: PDFSourceIdentity
    page: PDFPageIdentity
    evidence: OCREvidence
    raster_provenance: RasterProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.evidence, OCREvidence):
            raise PDFOCRError("OCR evidence must use the Phase 15.1 model", PDFOCRErrorCode.RASTERIZATION_FAILED)
        validate_evidence(self.evidence)
        expected_locator = self.page.to_dict()
        if self.evidence.source_id != self.source.source_id or self.evidence.source_digest != self.source.source_digest:
            raise OCRError("OCR evidence source identity does not match the original PDF", "OCR_PROVIDER_CONTRACT_INVALID")
        if len(self.evidence.pages) != 1 or dict(self.evidence.pages[0].locator) != expected_locator:
            raise OCRError("OCR evidence locator does not match the PDF page", "OCR_PROVIDER_CONTRACT_INVALID")
        if not isinstance(self.evidence.pages, tuple) or not isinstance(self.evidence.model_manifest, tuple):
            raise OCRError("OCR evidence must be immutably materialized", "OCR_PROVIDER_CONTRACT_INVALID")

    @property
    def route(self) -> PageRoute:
        return PageRoute.OCR

    @property
    def raw_text(self) -> str:
        return self.evidence.pages[0].raw_text

    def to_dict(self) -> dict[str, Any]:
        return {
            "route": self.route.value,
            "source": self.source.to_dict(),
            "locator": self.page.to_dict(),
            "evidence": self.evidence.to_dict(),
            "raster_provenance": self.raster_provenance.to_dict(),
        }


PageExecution = TextPageExecution | OCRPageExecution


@dataclass(frozen=True)
class MixedPDFExecutionResult:
    """Complete, source-ordered transaction output; never partial."""

    source: PDFSourceIdentity
    pages: tuple[PageExecution, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "pages", tuple(self.pages))
        if not isinstance(self.source, PDFSourceIdentity) or not self.pages:
            raise PDFOCRError("completed PDF transaction is incomplete", PDFOCRErrorCode.INPUT_INVALID)
        expected = tuple(range(1, self.pages[0].page.total_pages + 1))
        actual = tuple(item.page.page for item in self.pages)
        if actual != expected:
            raise PDFOCRError("completed PDF transaction is not source ordered", PDFOCRErrorCode.INPUT_INVALID)
        for item in self.pages:
            if item.source != self.source or item.page.total_pages != len(expected):
                raise PDFOCRError("completed PDF transaction has inconsistent page identity", PDFOCRErrorCode.INPUT_INVALID)

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source.to_dict(), "pages": [page.to_dict() for page in self.pages]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def execute_mixed_pdf(
    plan: MixedPDFPlan,
    raw_pdf_bytes: bytes,
    rasterizer: PDFRasterizer,
    providers: Mapping[str, OCRProvider],
    *,
    configuration: RasterConfiguration | None = None,
    resource_limits: ResourceLimits | None = None,
    isolation_policy: WorkerIsolationPolicy | None = None,
    explicit: str | None = None,
    project: str | None = None,
    user: str | None = None,
    default: str = "tesseract",
    allow_fallback: bool = False,
    language_config: Mapping[str, Any] | None = None,
    execution_config: Mapping[str, Any] | None = None,
) -> MixedPDFExecutionResult:
    """Execute a complete mixed-PDF plan sequentially and fail closed."""

    if not isinstance(plan, MixedPDFPlan) or not isinstance(raw_pdf_bytes, bytes):
        raise PDFOCRError("PDF transaction input is invalid", PDFOCRErrorCode.INPUT_INVALID)
    if plan.source.source_digest != hashlib.sha256(raw_pdf_bytes).hexdigest():
        raise PDFOCRError("source_digest does not identify original PDF bytes", PDFOCRErrorCode.INPUT_INVALID)
    if not isinstance(rasterizer, PDFRasterizer):
        raise PDFOCRError("PDF rasterizer boundary is invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)

    config = configuration or RasterConfiguration()
    limits = resource_limits or ResourceLimits()
    isolation = isolation_policy or WorkerIsolationPolicy()
    language = dict(language_config or {})
    execution = dict(execution_config or {})
    results: list[PageExecution] = []

    for planned in plan.pages:
        _validate_planned_page(plan, planned)
        if planned.route is PageRoute.TEXT:
            results.append(TextPageExecution(plan.source, planned.page, planned.extracted_text))
            continue

        request = RasterRequest(
            raw_pdf_bytes=raw_pdf_bytes,
            source=plan.source,
            page=planned.page,
            configuration=config,
            resource_limits=limits,
            isolation_policy=isolation,
            # Admission itself is performed by the restricted renderer worker;
            # this request marker cannot authorize a parent-side PDF parse.
            admission=PDFAdmissionResult(True, "pdf"),
        )
        raster = rasterizer.rasterize(request)
        ocr_request = OCRRequest(
            image_bytes=raster.raster_bytes,
            source_id=plan.source.source_id,
            source_digest=plan.source.source_digest,
            locator=planned.page.to_dict(),
            language_config=language,
            execution_config=execution,
        )
        evidence = execute_with_fallback(
            providers,
            ocr_request,
            explicit=explicit,
            project=project,
            user=user,
            default=default,
            allow_fallback=allow_fallback,
        )
        results.append(OCRPageExecution(plan.source, planned.page, evidence, raster.provenance))

    return MixedPDFExecutionResult(plan.source, tuple(results))


def _validate_planned_page(plan: MixedPDFPlan, planned: PDFPagePlan) -> None:
    if planned.source != plan.source or planned.page.page < 1 or planned.page.total_pages != len(plan.pages):
        raise PDFOCRError("PDF page identity does not match complete plan", PDFOCRErrorCode.PAGE_INVALID)
