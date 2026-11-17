"""Exact, renderer-independent PDF point geometry for Phase 15.2-C."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable

from .errors import PDFOCRError, PDFOCRErrorCode


def exact_fraction(value: object) -> Fraction:
    """Convert PDF numeric text without inheriting binary-float error."""

    if isinstance(value, bool):
        raise PDFOCRError("PDF geometry must be numeric", PDFOCRErrorCode.INPUT_INVALID)
    try:
        candidate = Fraction(str(value))
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise PDFOCRError("PDF geometry must be finite", PDFOCRErrorCode.INPUT_INVALID) from exc
    try:
        finite = math.isfinite(float(candidate))
    except OverflowError as exc:
        raise PDFOCRError("PDF geometry must be finite", PDFOCRErrorCode.INPUT_INVALID) from exc
    if not finite:
        raise PDFOCRError("PDF geometry must be finite", PDFOCRErrorCode.INPUT_INVALID)
    return candidate


def outward_pixels(point_extent: object, dpi: int = 300) -> int:
    """Return ceil(exact(point_extent) * dpi / 72)."""

    extent = exact_fraction(point_extent)
    if isinstance(dpi, bool) or not isinstance(dpi, int) or dpi < 1 or extent <= 0:
        raise PDFOCRError("PDF point extent and DPI must be positive", PDFOCRErrorCode.INPUT_INVALID)
    scaled = extent * dpi / 72
    return -(-scaled.numerator // scaled.denominator)


@dataclass(frozen=True)
class EffectivePageGeometry:
    selected_box: str
    exact_coordinates: tuple[Fraction, Fraction, Fraction, Fraction]
    provenance_coordinates: tuple[float, float, float, float]
    effective_rotation: int
    width: int
    height: int


def build_geometry(
    media_values: Iterable[object],
    crop_values: Iterable[object] | None,
    rotation_value: object,
    *,
    dpi: int = 300,
) -> EffectivePageGeometry:
    """Validate effective boxes and derive exact, rotation-aware pixels."""

    media = tuple(exact_fraction(value) for value in media_values)
    if len(media) != 4:
        raise PDFOCRError("MediaBox must contain four values", PDFOCRErrorCode.INPUT_INVALID)
    mx0, my0, mx1, my1 = media
    if mx1 <= mx0 or my1 <= my0:
        raise PDFOCRError("MediaBox must have positive area", PDFOCRErrorCode.INPUT_INVALID)

    selected_box = "MediaBox"
    selected = media
    if crop_values is not None:
        try:
            crop = tuple(exact_fraction(value) for value in crop_values)
        except PDFOCRError:
            crop = ()
        if len(crop) == 4:
            cx0, cy0, cx1, cy1 = crop
            if cx1 > cx0 and cy1 > cy0 and mx0 <= cx0 <= cx1 <= mx1 and my0 <= cy0 <= cy1 <= my1:
                selected_box = "CropBox"
                selected = crop

    try:
        rotation_number = int(rotation_value)
    except (TypeError, ValueError) as exc:
        raise PDFOCRError("effective page rotation is invalid", PDFOCRErrorCode.INPUT_INVALID) from exc
    if isinstance(rotation_value, bool) or exact_fraction(rotation_value).denominator != 1 or rotation_number % 90 != 0:
        raise PDFOCRError("effective page rotation is invalid", PDFOCRErrorCode.INPUT_INVALID)
    rotation = rotation_number % 360

    x0, y0, x1, y1 = selected
    point_width, point_height = x1 - x0, y1 - y0
    if rotation in (90, 270):
        point_width, point_height = point_height, point_width
    width = outward_pixels(point_width, dpi)
    height = outward_pixels(point_height, dpi)
    return EffectivePageGeometry(
        selected_box=selected_box,
        exact_coordinates=selected,
        provenance_coordinates=tuple(float(value) for value in selected),
        effective_rotation=rotation,
        width=width,
        height=height,
    )
