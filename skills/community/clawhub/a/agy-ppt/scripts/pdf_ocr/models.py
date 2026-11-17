"""Immutable, deterministic internal contracts for Phase 15.2 PDF OCR."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
import math
import re
from typing import Any

from ocr_providers.errors import OCRError
from ocr_providers.models import validate_locator

from .errors import PDFOCRError, PDFOCRErrorCode


_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_MIB = 1024 * 1024


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _require_nonempty(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or value.lower() == "unknown":
        raise PDFOCRError(f"{field_name} must be a stable non-empty identifier", PDFOCRErrorCode.RASTERIZATION_FAILED)
    if "/" in value or "\\" in value:
        raise PDFOCRError(f"{field_name} must not contain a filesystem path", PDFOCRErrorCode.RASTERIZATION_FAILED)
    return value


def _require_positive_int(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise PDFOCRError(f"{field_name} must be a positive integer", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    return value


def _require_positive_number(value: object, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise PDFOCRError(f"{field_name} must be a positive finite number", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    return float(value)


class PageClassification(str, Enum):
    SEARCHABLE = "SEARCHABLE"
    SCANNED = "SCANNED"


@dataclass(frozen=True)
class PDFPageIdentity:
    """OCR-native, source-relative PDF page identity."""

    page: int
    total_pages: int

    def __post_init__(self) -> None:
        locator = {"kind": "page", "page": self.page, "total_pages": self.total_pages}
        try:
            validate_locator(locator)
        except OCRError as exc:
            raise PDFOCRError(str(exc), PDFOCRErrorCode.PAGE_INVALID) from exc

    def to_dict(self) -> dict[str, int | str]:
        return {"kind": "page", "page": self.page, "total_pages": self.total_pages}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())


@dataclass(frozen=True)
class PDFSourceIdentity:
    """Identity of the original raw PDF; no derived raster identity is accepted."""

    source_id: str
    source_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not self.source_id:
            raise PDFOCRError("source_id is required", PDFOCRErrorCode.INPUT_INVALID)
        if not isinstance(self.source_digest, str) or not _DIGEST.fullmatch(self.source_digest):
            raise PDFOCRError("source_digest must be lowercase SHA-256 of original raw PDF bytes", PDFOCRErrorCode.INPUT_INVALID)

    def to_dict(self) -> dict[str, str]:
        return {"source_id": self.source_id, "source_digest": self.source_digest}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())


@dataclass(frozen=True)
class RasterConfiguration:
    """Renderer-independent mechanical raster settings."""

    dpi: int = 300
    output_format: str = "PNG"
    colorspace: str = "RGB"
    alpha: bool = False
    rotation_policy: str = "respect_effective_pdf_page_rotation"
    box_policy: str = "valid_explicit_cropbox_else_mediabox"
    semantic_preprocessing: str = "none"
    render_annotations: bool = False

    def __post_init__(self) -> None:
        expected = {
            "dpi": 300,
            "output_format": "PNG",
            "colorspace": "RGB",
            "alpha": False,
            "rotation_policy": "respect_effective_pdf_page_rotation",
            "box_policy": "valid_explicit_cropbox_else_mediabox",
            "semantic_preprocessing": "none",
            "render_annotations": False,
        }
        for name, value in expected.items():
            actual = getattr(self, name)
            if actual != value or type(actual) is not type(value):
                raise PDFOCRError(f"unsupported raster configuration: {name}", PDFOCRErrorCode.RASTERIZATION_FAILED)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())


@dataclass(frozen=True)
class ResourceLimits:
    """Configured Phase 15.2 ceilings; this model does not enforce resources."""

    max_raw_pdf_bytes: int = 100 * _MIB
    max_page_count: int = 500
    max_raster_width: int = 10_000
    max_raster_height: int = 10_000
    max_pixels_per_page: int = 25_000_000
    max_raster_output_bytes_per_page: int = 100 * _MIB
    renderer_timeout_seconds_per_page: float = 30.0
    document_open_timeout_seconds: float = 30.0
    text_extraction_timeout_seconds_per_page: float = 30.0
    max_temporary_storage_bytes: int = 256 * _MIB
    worker_memory_limit_bytes: int = 512 * _MIB

    def __post_init__(self) -> None:
        ceilings = ResourceLimits.committed_ceilings()
        for name, ceiling in ceilings.items():
            value = getattr(self, name)
            checked = _require_positive_number(value, name) if isinstance(ceiling, float) else _require_positive_int(value, name)
            if checked > ceiling:
                raise PDFOCRError(f"{name} exceeds the committed ceiling", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)

    @staticmethod
    def committed_ceilings() -> dict[str, int | float]:
        return {
            "max_raw_pdf_bytes": 100 * _MIB,
            "max_page_count": 500,
            "max_raster_width": 10_000,
            "max_raster_height": 10_000,
            "max_pixels_per_page": 25_000_000,
            "max_raster_output_bytes_per_page": 100 * _MIB,
            "renderer_timeout_seconds_per_page": 30.0,
            "document_open_timeout_seconds": 30.0,
            "text_extraction_timeout_seconds_per_page": 30.0,
            "max_temporary_storage_bytes": 256 * _MIB,
            "worker_memory_limit_bytes": 512 * _MIB,
        }

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @property
    def enforced(self) -> bool:
        """A policy value alone is never evidence of worker enforcement."""

        return False


@dataclass(frozen=True)
class WorkerIsolationPolicy:
    """Requirements for the later worker implementation; this does not enforce them."""

    dedicated_worker: bool = True
    restricted_before_open: bool = True
    parent_monotonic_watchdog: bool = True
    bounded_ipc: bool = True
    resource_limits_required: bool = True
    temporary_storage_bounded: bool = True
    network_enabled: bool = False
    minimal_filesystem_visibility: bool = True
    credentials_available: bool = False
    cleanup_required: bool = True
    native_crash_isolated: bool = True

    def __post_init__(self) -> None:
        required = {
            "dedicated_worker": True,
            "restricted_before_open": True,
            "parent_monotonic_watchdog": True,
            "bounded_ipc": True,
            "resource_limits_required": True,
            "temporary_storage_bounded": True,
            "network_enabled": False,
            "minimal_filesystem_visibility": True,
            "credentials_available": False,
            "cleanup_required": True,
            "native_crash_isolated": True,
        }
        if any(type(getattr(self, name)) is not bool or getattr(self, name) is not value for name, value in required.items()):
            raise PDFOCRError("worker isolation policy cannot be weakened", PDFOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @property
    def enforced(self) -> bool:
        """The worker and platform enforcement are deferred to Phase 15.2-C."""

        return False


@dataclass(frozen=True)
class PDFAdmissionResult:
    """Structural result for the future admission boundary, not proof by itself.

    Direct construction is intended for internal contract tests. Production
    orchestration must only trust a result emitted by the future controlled PDF
    admission implementation.
    """

    accepted: bool
    detected_format: str | None
    error_code: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.accepted, bool):
            raise PDFOCRError("admission accepted must be boolean", PDFOCRErrorCode.INPUT_INVALID)
        if self.accepted:
            if self.detected_format != "pdf" or self.error_code is not None:
                raise PDFOCRError("accepted input must be deterministically admitted as PDF", PDFOCRErrorCode.INPUT_INVALID)
        elif self.error_code != PDFOCRErrorCode.INPUT_INVALID.value:
            raise PDFOCRError("rejected admission must use OCR_PDF_INPUT_INVALID", PDFOCRErrorCode.INPUT_INVALID)

    def to_dict(self) -> dict[str, bool | str | None]:
        return asdict(self)

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())


@dataclass(frozen=True)
class RasterProvenance:
    renderer_id: str
    renderer_version: str
    renderer_engine_version: str
    approved_build_identity: str
    dpi: int
    output_format: str
    colorspace: str
    alpha: bool
    rotation_policy: str
    effective_rotation: int
    box_policy: str
    selected_box: str
    box_coordinates: tuple[float, float, float, float]
    render_annotations: bool
    semantic_preprocessing: str
    width: int
    height: int
    raster_digest: str

    def __post_init__(self) -> None:
        for name in ("renderer_id", "renderer_version", "renderer_engine_version", "approved_build_identity"):
            _require_nonempty(getattr(self, name), name)
        RasterConfiguration(
            dpi=self.dpi,
            output_format=self.output_format,
            colorspace=self.colorspace,
            alpha=self.alpha,
            rotation_policy=self.rotation_policy,
            box_policy=self.box_policy,
            semantic_preprocessing=self.semantic_preprocessing,
            render_annotations=self.render_annotations,
        )
        if isinstance(self.effective_rotation, bool) or self.effective_rotation not in (0, 90, 180, 270):
            raise PDFOCRError("effective_rotation must be 0, 90, 180, or 270", PDFOCRErrorCode.RASTERIZATION_FAILED)
        if self.selected_box not in ("CropBox", "MediaBox"):
            raise PDFOCRError("selected_box must be CropBox or MediaBox", PDFOCRErrorCode.RASTERIZATION_FAILED)
        if not isinstance(self.box_coordinates, tuple) or len(self.box_coordinates) != 4:
            raise PDFOCRError("box_coordinates must contain four values", PDFOCRErrorCode.RASTERIZATION_FAILED)
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in self.box_coordinates):
            raise PDFOCRError("box_coordinates must be finite numbers", PDFOCRErrorCode.RASTERIZATION_FAILED)
        x0, y0, x1, y1 = self.box_coordinates
        if x1 <= x0 or y1 <= y0:
            raise PDFOCRError("selected page box must have positive area", PDFOCRErrorCode.RASTERIZATION_FAILED)
        _require_positive_int(self.width, "width")
        _require_positive_int(self.height, "height")
        if not isinstance(self.raster_digest, str) or not _DIGEST.fullmatch(self.raster_digest):
            raise PDFOCRError("raster_digest must be lowercase SHA-256", PDFOCRErrorCode.RASTERIZATION_FAILED)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["box_coordinates"] = list(self.box_coordinates)
        return value

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())
