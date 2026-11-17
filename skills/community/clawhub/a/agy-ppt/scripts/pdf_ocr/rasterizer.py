"""Renderer-neutral Phase 15.2 rasterization boundary."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import hashlib

from source_grounding import compute_source_digest

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


@dataclass(frozen=True)
class RasterRequest:
    """Immutable worker request; admission authority is supplied by future orchestration."""

    raw_pdf_bytes: bytes
    source: PDFSourceIdentity
    page: PDFPageIdentity
    configuration: RasterConfiguration
    resource_limits: ResourceLimits
    isolation_policy: WorkerIsolationPolicy
    admission: PDFAdmissionResult

    def __post_init__(self) -> None:
        if not isinstance(self.raw_pdf_bytes, bytes):
            raise PDFOCRError("raw_pdf_bytes must be immutable bytes", PDFOCRErrorCode.INPUT_INVALID)
        if len(self.raw_pdf_bytes) > self.resource_limits.max_raw_pdf_bytes:
            raise PDFOCRError("raw PDF exceeds configured byte limit", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
        if compute_source_digest(self.raw_pdf_bytes) != self.source.source_digest:
            raise PDFOCRError(
                "source_digest must identify the original raw PDF bytes",
                PDFOCRErrorCode.INPUT_INVALID,
            )
        if not self.admission.accepted or self.admission.detected_format != "pdf":
            raise PDFOCRError("input has not passed strict PDF admission", PDFOCRErrorCode.INPUT_INVALID)


@dataclass(frozen=True)
class RasterResult:
    raster_bytes: bytes
    provenance: RasterProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.raster_bytes, bytes):
            raise PDFOCRError("raster_bytes must be immutable bytes", PDFOCRErrorCode.RASTERIZATION_FAILED)
        digest = hashlib.sha256(self.raster_bytes).hexdigest()
        if digest != self.provenance.raster_digest:
            raise PDFOCRError("raster digest does not identify prepared raster bytes", PDFOCRErrorCode.RASTERIZATION_FAILED)


class PDFRasterizer(ABC):
    """Minimal boundary implemented by deterministic fakes and future adapters."""

    @abstractmethod
    def rasterize(self, request: RasterRequest) -> RasterResult:
        """Return prepared raster bytes and canonical raster provenance."""
