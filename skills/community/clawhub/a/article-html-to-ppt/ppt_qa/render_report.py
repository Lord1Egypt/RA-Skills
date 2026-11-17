from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .renderers.analysis import image_metrics
from .renderers.base import RenderResult


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _as_string(path: Optional[Path]) -> Optional[str]:
    return str(path) if path else None


def analyze_slides(
    result: RenderResult,
    *,
    expected_aspect: float = 16 / 9,
    blank_threshold: float = 0.995,
    near_blank_threshold: float = 0.98,
    aspect_tolerance: float = 0.03,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    slides: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    baseline_size: Optional[tuple[int, int]] = None
    for index, image in enumerate(result.slide_images, start=1):
        if not image.exists():
            errors.append({"code": "RENDER_IMAGE_MISSING", "message": f"Slide image missing: {image}", "slide_index": index})
            slides.append({"slide_index": index, "image": str(image), "width_px": None, "height_px": None, "blank_score": None, "status": "failed"})
            continue
        metrics = image_metrics(image)
        width = int(metrics["width_px"])
        height = int(metrics["height_px"])
        score = float(metrics["blank_score"])
        slide_status = "passed"
        if baseline_size is None:
            baseline_size = (width, height)
        elif baseline_size != (width, height):
            errors.append({"code": "RENDER_SIZE_MISMATCH", "message": f"Slide {index} size {width}x{height} differs from {baseline_size[0]}x{baseline_size[1]}.", "slide_index": index})
            slide_status = "failed"
        aspect = width / height if height else 0.0
        if height == 0 or abs(aspect - expected_aspect) > aspect_tolerance:
            errors.append({"code": "RENDER_ASPECT_RATIO_MISMATCH", "message": f"Slide {index} aspect ratio {aspect:.3f} differs from expected {expected_aspect:.3f}.", "slide_index": index})
            slide_status = "failed"
        # Minimal cover slides need PPTX object-count context; the render layer
        # exposes the score and only emits warnings/errors for the verifier to combine.
        if score >= blank_threshold:
            errors.append({"code": "RENDER_BLANK_SLIDE", "message": f"Slide {index} appears blank.", "slide_index": index, "blank_score": score})
            slide_status = "failed"
        elif score >= near_blank_threshold:
            warnings.append({"code": "RENDER_NEAR_BLANK_SLIDE", "message": f"Slide {index} appears near blank.", "slide_index": index, "blank_score": score})
            if slide_status == "passed":
                slide_status = "warning"
        slides.append({"slide_index": index, "image": str(image), "width_px": width, "height_px": height, "blank_score": score, "status": slide_status})
    return slides, warnings, errors


def build_render_report(
    pptx_path: Path,
    result: RenderResult,
    *,
    started_at: str,
    finished_at: Optional[str] = None,
    expected_slides: Optional[int] = None,
    expected_aspect: float = 16 / 9,
) -> dict[str, Any]:
    finished = finished_at or iso_now()
    slides, warnings, errors = analyze_slides(result, expected_aspect=expected_aspect)
    warnings.extend({"code": "RENDER_WARNING", "message": item} for item in result.logs)
    errors.extend({"code": _error_code(item), "message": item} for item in result.errors)
    if result.pdf_path is None:
        if result.status != "unavailable":
            errors.append({"code": "RENDER_PDF_MISSING", "message": "Renderer did not produce deck.pdf."})
    elif not result.pdf_path.exists():
        errors.append({"code": "RENDER_PDF_MISSING", "message": f"PDF missing: {result.pdf_path}"})
    if result.status != "unavailable" and expected_slides is not None and result.slide_count_rendered != expected_slides:
        errors.append(
            {
                "code": "RENDER_SLIDE_COUNT_MISMATCH",
                "message": f"Expected {expected_slides} slides, rendered {result.slide_count_rendered}.",
                "expected": expected_slides,
                "actual": result.slide_count_rendered,
            }
        )
    status = _status_from_result(result, errors)
    return {
        "schema_version": "1.0",
        "pptx": str(pptx_path),
        "engine": result.engine,
        "engine_version": result.engine_version,
        "started_at": started_at,
        "finished_at": finished,
        "duration_seconds": result.duration_seconds,
        "status": status,
        "slide_count_expected": expected_slides,
        "slide_count_rendered": result.slide_count_rendered,
        "pdf": _as_string(result.pdf_path),
        "slides": slides,
        "warnings": warnings,
        "errors": errors,
    }


def _error_code(message: str) -> str:
    prefix = message.split(":", 1)[0].strip()
    return prefix if prefix.startswith("RENDER_") else "RENDER_EXPORT_FAILED"


def _status_from_result(result: RenderResult, errors: list[dict[str, Any]]) -> str:
    if result.status == "unavailable" or any(error["code"] == "RENDER_ENGINE_UNAVAILABLE" for error in errors):
        return "unavailable"
    if errors:
        if result.slide_count_rendered > 0:
            return "partial"
        return "failed"
    return "passed"


def write_render_report(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
