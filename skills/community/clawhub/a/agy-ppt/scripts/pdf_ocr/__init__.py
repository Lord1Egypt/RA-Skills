"""Internal Phase 15.2 PDF OCR contract primitives."""

from .errors import ERROR_CODES, PDFOCRError, PDFOCRErrorCode
from .classification import classify_page_text
from .models import (
    PDFAdmissionResult,
    PDFPageIdentity,
    PDFSourceIdentity,
    PageClassification,
    RasterConfiguration,
    RasterProvenance,
    ResourceLimits,
    WorkerIsolationPolicy,
)
from .rasterizer import PDFRasterizer, RasterRequest, RasterResult
from .planning import MixedPDFPlan, PDFPageInput, PDFPagePlan, PageRoute, plan_pdf_pages
from .orchestration import (
    MixedPDFExecutionResult,
    OCRPageExecution,
    TextPageExecution,
    execute_mixed_pdf,
)

__all__ = [
    "ERROR_CODES",
    "MixedPDFPlan",
    "PDFAdmissionResult",
    "PDFOCRError",
    "PDFOCRErrorCode",
    "PDFPageIdentity",
    "PDFPageInput",
    "PDFPagePlan",
    "PDFRasterizer",
    "PDFSourceIdentity",
    "PageClassification",
    "PageRoute",
    "RasterConfiguration",
    "RasterProvenance",
    "RasterRequest",
    "RasterResult",
    "ResourceLimits",
    "WorkerIsolationPolicy",
    "classify_page_text",
    "plan_pdf_pages",
    "MixedPDFExecutionResult",
    "OCRPageExecution",
    "TextPageExecution",
    "execute_mixed_pdf",
]
