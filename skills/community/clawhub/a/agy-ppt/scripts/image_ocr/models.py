"""Immutable internal contracts for Phase 15.3 image preparation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import re
from typing import Any

from source_grounding import compute_source_digest

from .errors import ImageOCRError, ImageOCRErrorCode


_MIB = 1024 * 1024
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_PATH_MARKERS = ("/Users/", "/home/", "C:\\Users\\", "/tmp/", "/private/tmp/")


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ImageOCRError(f"{name} must be a positive integer", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    return value


def _positive_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ImageOCRError(f"{name} must be a positive number", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)
    return float(value)


def _nonempty_path_free(value: object, name: str) -> str:
    if not isinstance(value, str) or not value or any(marker in value for marker in _PATH_MARKERS):
        raise ImageOCRError(f"{name} must be non-empty and path-free", ImageOCRErrorCode.DECODE_FAILED)
    return value


@dataclass(frozen=True)
class ImageSourceIdentity:
    source_id: str
    source_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not self.source_id:
            raise ImageOCRError("source_id is required", ImageOCRErrorCode.INPUT_INVALID)
        if not isinstance(self.source_digest, str) or not _DIGEST.fullmatch(self.source_digest):
            raise ImageOCRError("source_digest must be lowercase SHA-256 of original image bytes", ImageOCRErrorCode.INPUT_INVALID)

    @classmethod
    def from_bytes(cls, source_id: str, raw_image_bytes: bytes) -> "ImageSourceIdentity":
        if not isinstance(raw_image_bytes, bytes):
            raise ImageOCRError("raw image input must be immutable bytes", ImageOCRErrorCode.INPUT_INVALID)
        return cls(source_id, compute_source_digest(raw_image_bytes))

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ImagePreparationConfiguration:
    target_format: str = "PNG"
    target_mode: str = "RGB"
    alpha_policy: str = "composite_on_white"
    exif_orientation_policy: str = "apply_display_orientation"
    icc_policy: str = "detect_without_transform_and_drop"
    semantic_preprocessing: str = "none"

    def __post_init__(self) -> None:
        expected = {
            "target_format": "PNG",
            "target_mode": "RGB",
            "alpha_policy": "composite_on_white",
            "exif_orientation_policy": "apply_display_orientation",
            "icc_policy": "detect_without_transform_and_drop",
            "semantic_preprocessing": "none",
        }
        if any(type(getattr(self, key)) is not str or getattr(self, key) != value for key, value in expected.items()):
            raise ImageOCRError("image preparation configuration cannot be changed", ImageOCRErrorCode.DECODE_FAILED)

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ImageResourceLimits:
    max_raw_image_bytes: int = 100 * _MIB
    max_width: int = 10_000
    max_height: int = 10_000
    max_pixels: int = 25_000_000
    max_tiff_frames: int = 1
    max_decoded_packed_bytes: int = 100 * _MIB
    max_prepared_png_bytes: int = 100 * _MIB
    preparation_timeout_seconds: float = 30.0
    worker_memory_limit_bytes: int = 512 * _MIB
    max_temporary_storage_bytes: int = 256 * _MIB

    def __post_init__(self) -> None:
        for name, ceiling in self.committed_ceilings().items():
            value = getattr(self, name)
            checked = _positive_number(value, name) if isinstance(ceiling, float) else _positive_int(value, name)
            if checked > ceiling:
                raise ImageOCRError(f"{name} exceeds committed ceiling", ImageOCRErrorCode.RESOURCE_LIMIT_EXCEEDED)

    @staticmethod
    def committed_ceilings() -> dict[str, int | float]:
        return {
            "max_raw_image_bytes": 100 * _MIB,
            "max_width": 10_000,
            "max_height": 10_000,
            "max_pixels": 25_000_000,
            "max_tiff_frames": 1,
            "max_decoded_packed_bytes": 100 * _MIB,
            "max_prepared_png_bytes": 100 * _MIB,
            "preparation_timeout_seconds": 30.0,
            "worker_memory_limit_bytes": 512 * _MIB,
            "max_temporary_storage_bytes": 256 * _MIB,
        }

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


@dataclass(frozen=True)
class ImagePreparationProvenance:
    decoder_id: str
    decoder_version: str
    source_format: str
    original_width: int
    original_height: int
    original_mode: str
    exif_orientation: int | None
    orientation_transform_applied: bool
    icc_profile_present: bool
    alpha_policy: str
    color_conversion_policy: str
    target_format: str
    target_mode: str
    prepared_width: int
    prepared_height: int
    prepared_image_digest: str

    def __post_init__(self) -> None:
        _nonempty_path_free(self.decoder_id, "decoder_id")
        _nonempty_path_free(self.decoder_version, "decoder_version")
        if self.source_format not in ("PNG", "JPEG", "TIFF"):
            raise ImageOCRError("source format is not admitted", ImageOCRErrorCode.DECODE_FAILED)
        for name in ("original_width", "original_height", "prepared_width", "prepared_height"):
            _positive_int(getattr(self, name), name)
        _nonempty_path_free(self.original_mode, "original_mode")
        if self.exif_orientation is not None and (isinstance(self.exif_orientation, bool) or not isinstance(self.exif_orientation, int) or self.exif_orientation not in range(1, 9)):
            raise ImageOCRError("EXIF orientation must be 1 through 8", ImageOCRErrorCode.DECODE_FAILED)
        for name in ("orientation_transform_applied", "icc_profile_present"):
            if type(getattr(self, name)) is not bool:
                raise ImageOCRError(f"{name} must be boolean", ImageOCRErrorCode.DECODE_FAILED)
        expected_transform = self.exif_orientation in range(2, 9) if self.exif_orientation is not None else False
        if self.orientation_transform_applied is not expected_transform:
            raise ImageOCRError("EXIF orientation provenance is inconsistent", ImageOCRErrorCode.DECODE_FAILED)
        for name in ("alpha_policy", "color_conversion_policy"):
            _nonempty_path_free(getattr(self, name), name)
        if self.target_format != "PNG" or self.target_mode != "RGB":
            raise ImageOCRError("prepared image must be RGB PNG", ImageOCRErrorCode.DECODE_FAILED)
        if not isinstance(self.prepared_image_digest, str) or not _DIGEST.fullmatch(self.prepared_image_digest):
            raise ImageOCRError("prepared image digest must be lowercase SHA-256", ImageOCRErrorCode.DECODE_FAILED)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())


@dataclass(frozen=True)
class PreparedImage:
    png_bytes: bytes
    provenance: ImagePreparationProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.png_bytes, bytes) or not self.png_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ImageOCRError("prepared payload is not PNG bytes", ImageOCRErrorCode.DECODE_FAILED)
        if compute_source_digest(self.png_bytes) != self.provenance.prepared_image_digest:
            raise ImageOCRError("prepared digest does not identify PNG bytes", ImageOCRErrorCode.DECODE_FAILED)
