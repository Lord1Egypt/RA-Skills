from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .package_inspector import inspect_package
from .render_report import build_render_report
from .renderers.base import RenderResult, select_renderer
from .report import inspection_to_dict
from .slide_inspector import inspect_slides
from engine.route_policy import require_production_route


QA_SCHEMA_VERSION = "2.1"
SEVERITY_COMPATIBILITY = {
    "info": "review",
    "warning": "review",
    "error": "fail",
    "fatal": "blocked",
}


class VerificationInputError(ValueError):
    pass


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Optional[Path]) -> Optional[dict[str, Any]]:
    if path is None:
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise VerificationInputError(f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise VerificationInputError(f"{path} must contain a JSON object")
    return data


def write_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def run_structural_inspection(
    pptx_path: Path,
    *,
    ppt_ir: Optional[dict[str, Any]] = None,
    style: Optional[dict[str, Any]] = None,
    delivery: Optional[dict[str, Any]] = None,
    build_manifest: Optional[dict[str, Any]] = None,
    include_raw_xml: bool = False,
    route: str = "standard",
) -> dict[str, Any]:
    route = require_production_route(route)
    inspection = inspect_package(pptx_path, ppt_ir=ppt_ir, build_manifest=build_manifest)
    if not any(issue.severity == "fatal" for issue in inspection.issues):
        inspection = inspect_slides(
            pptx_path,
            inspection,
            ppt_ir=ppt_ir,
            style=style,
            delivery=delivery,
            include_raw_xml=include_raw_xml,
            route=route,
        )
    report = inspection_to_dict(inspection, include_raw_xml=include_raw_xml)
    report["qa_route"] = route
    return report


def run_render_report(
    pptx_path: Path,
    output_dir: Path,
    *,
    engine: str = "auto",
    expected_slides: Optional[int] = None,
    expected_aspect: float = 16 / 9,
    timeout: int = 300,
    dpi: int = 144,
) -> dict[str, Any]:
    started_at = iso_now()
    renderer = (
        None
        if os.environ.get("PPTSMITH_TEST_RENDERER_UNAVAILABLE") == "1"
        else select_renderer(engine)
    )
    if renderer is None:
        result = RenderResult(
            status="unavailable",
            engine=None,
            engine_version=None,
            pdf_path=None,
            errors=["RENDER_ENGINE_UNAVAILABLE"],
            duration_seconds=0.0,
            slide_count_rendered=0,
        )
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        for generated_name in ("deck.pdf", "slides", "logs"):
            generated_path = output_dir / generated_name
            if generated_path.is_dir():
                shutil.rmtree(generated_path)
            elif generated_path.exists():
                generated_path.unlink()
        result = renderer.render(pptx_path, output_dir, timeout_seconds=timeout, dpi=dpi)  # type: ignore[call-arg]
    return build_render_report(
        pptx_path,
        result,
        started_at=started_at,
        expected_slides=expected_slides,
        expected_aspect=expected_aspect,
    )


def build_verification_report(
    pptx_path: Path,
    *,
    ppt_ir: Optional[dict[str, Any]] = None,
    style: Optional[dict[str, Any]] = None,
    delivery: Optional[dict[str, Any]] = None,
    build_manifest: Optional[dict[str, Any]] = None,
    inspection_report: Optional[dict[str, Any]] = None,
    render_report: Optional[dict[str, Any]] = None,
    ppt_ir_ref: Optional[str] = None,
    style_ref: Optional[str] = None,
    delivery_ref: Optional[str] = None,
    build_ref: Optional[str] = None,
    render_required: bool = False,
    profile: Optional[str] = None,
) -> dict[str, Any]:
    if inspection_report is None:
        inspection_report = run_structural_inspection(
            pptx_path,
            ppt_ir=ppt_ir,
            style=style,
            delivery=delivery,
            build_manifest=build_manifest,
        )
    issues = _normalize_inspection_issues(inspection_report)
    render_available = False
    render_status = "not_run"
    if render_report is not None:
        render_status = str(render_report.get("status", "unknown"))
        render_available = render_status not in {"unavailable", "not_run"}
        issues.extend(_normalize_render_issues(render_report))
        if render_status == "unavailable":
            issues.append(
                _issue(
                    "RENDER_ENGINE_UNAVAILABLE",
                    "warning" if not render_required else "error",
                    "render",
                    "No PowerPoint, Keynote, LibreOffice, or other configured render engine is available.",
                    evidence={"render_status": "unavailable", "render_required": render_required},
                    repair_action={"type": "configure_renderer", "description": "Install or configure a real renderer before claiming visual QA."},
                    repair_status="not_applicable",
                )
            )
    elif render_required:
        issues.append(
            _issue(
                "RENDER_NOT_RUN",
                "error",
                "render",
                "Render verification is required but no render report was supplied or generated.",
                evidence={"render_required": True},
                repair_action={"type": "run_render", "description": "Run verify_deck.py with --render or provide --render-report."},
            )
        )

    status = _status_from_issues(issues, render_status=render_status, render_required=render_required)
    deck_id = _deck_id(ppt_ir, build_manifest, pptx_path)
    logical_count = _json_int(ppt_ir, ["deck", "logical_slide_count"])
    physical_count = _json_int(ppt_ir, ["deck", "physical_slide_count"])
    metrics = _metrics(inspection_report, render_report, issues, logical_count, physical_count)
    build_status_cap = _build_status_cap(status, render_status, render_available)
    return {
        "schema_version": QA_SCHEMA_VERSION,
        "generated_at": iso_now(),
        "deck_id": deck_id,
        "pptx": str(pptx_path),
        "ppt_ir_ref": ppt_ir_ref or "",
        "style_ref": style_ref,
        "delivery_ref": delivery_ref,
        "build_ref": build_ref,
        "profile": profile or _profile(ppt_ir, build_manifest),
        "status": status,
        "build_status_cap": build_status_cap,
        "render_required": render_required,
        "compatibility": {
            "severity_aliases": SEVERITY_COMPATIBILITY,
            "legacy_severities": ["review", "fail", "blocked"],
        },
        "inputs": {
            "inspection_report": "embedded",
            "render_report": "embedded" if render_report is not None else None,
        },
        "evidence": {
            "structural_inspection": inspection_report,
            "render_report": render_report,
        },
        "issues": issues,
        "metrics": metrics,
    }


def verification_exit_code(report: dict[str, Any]) -> int:
    if report.get("status") == "pass":
        return 0
    issues = report.get("issues", [])
    if any(isinstance(issue, dict) and issue.get("issue_code") == "RENDER_ENGINE_UNAVAILABLE" for issue in issues):
        return 2
    return 1


def _normalize_inspection_issues(inspection: dict[str, Any]) -> list[dict[str, Any]]:
    return [_normalize_issue(issue, source="inspection") for issue in inspection.get("issues", []) if isinstance(issue, dict)]


def _normalize_render_issues(render_report: dict[str, Any]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in render_report.get("warnings", []) or []:
        if isinstance(item, dict):
            normalized.append(_render_issue(item, "warning"))
    for item in render_report.get("errors", []) or []:
        if isinstance(item, dict) and item.get("code") != "RENDER_ENGINE_UNAVAILABLE":
            normalized.append(_render_issue(item, "error"))
    return normalized


def _normalize_issue(issue: dict[str, Any], *, source: str) -> dict[str, Any]:
    severity = _canonical_severity(str(issue.get("severity", "warning")))
    return {
        "issue_id": issue.get("issue_id"),
        "issue_code": str(issue.get("issue_code", "QA_UNKNOWN")),
        "slide_id": issue.get("slide_id"),
        "object_id": issue.get("object_id"),
        "ppt_shape_id": issue.get("ppt_shape_id"),
        "severity": severity,
        "compatibility_severity": SEVERITY_COMPATIBILITY[severity],
        "category": str(issue.get("category", source)),
        "detector": str(issue.get("detector", source)),
        "evidence": issue.get("evidence") if isinstance(issue.get("evidence"), dict) else {},
        "message": str(issue.get("message", "")),
        "repair_action": issue.get("repair_action"),
        "repair_status": str(issue.get("repair_status", "pending")),
        "recheck_status": "not_run",
        "source_report": source,
    }


def _render_issue(item: dict[str, Any], severity: str) -> dict[str, Any]:
    slide_index = item.get("slide_index")
    slide_id = "S%02d" % slide_index if isinstance(slide_index, int) else None
    return _issue(
        str(item.get("code", "RENDER_UNKNOWN")),
        severity,
        "render",
        str(item.get("message", "")),
        slide_id=slide_id,
        evidence={key: value for key, value in item.items() if key not in {"code", "message"}},
        repair_action={"type": "manual_visual_repair", "description": "Requires rendered output and authoring-tool review."},
    )


def _issue(
    issue_code: str,
    severity: str,
    category: str,
    message: str,
    *,
    slide_id: Optional[str] = None,
    object_id: Optional[str] = None,
    evidence: Optional[dict[str, Any]] = None,
    repair_action: Optional[dict[str, Any]] = None,
    repair_status: str = "pending",
) -> dict[str, Any]:
    canonical = _canonical_severity(severity)
    return {
        "issue_id": None,
        "issue_code": issue_code,
        "slide_id": slide_id,
        "object_id": object_id,
        "ppt_shape_id": None,
        "severity": canonical,
        "compatibility_severity": SEVERITY_COMPATIBILITY[canonical],
        "category": category,
        "detector": "verify-deck",
        "evidence": evidence or {},
        "message": message,
        "repair_action": repair_action,
        "repair_status": repair_status,
        "recheck_status": "not_run",
        "source_report": "verification",
    }


def _canonical_severity(severity: str) -> str:
    if severity in {"info", "warning", "error", "fatal"}:
        return severity
    if severity == "review":
        return "warning"
    if severity == "fail":
        return "error"
    if severity == "blocked":
        return "fatal"
    return "warning"


def _status_from_issues(issues: list[dict[str, Any]], *, render_status: str, render_required: bool) -> str:
    severities = {str(issue.get("severity")) for issue in issues}
    if "fatal" in severities:
        return "blocked"
    if "error" in severities:
        return "fail"
    if "warning" in severities:
        return "warning"
    if render_required and render_status not in {"passed"}:
        return "blocked"
    return "pass"


def _build_status_cap(status: str, render_status: str, render_available: bool) -> str:
    if status in {"fail", "blocked"}:
        return "failed"
    if render_available:
        return "verified" if status == "pass" else "read_back"
    if render_status == "unavailable":
        return "created"
    return "read_back" if status == "pass" else "created"


def _metrics(
    inspection: dict[str, Any],
    render_report: Optional[dict[str, Any]],
    issues: list[dict[str, Any]],
    logical_count: Optional[int],
    physical_count: Optional[int],
) -> dict[str, Any]:
    inspection_metrics = inspection.get("metrics", {}) if isinstance(inspection.get("metrics"), dict) else {}
    rendered = 0
    expected = None
    if render_report is not None:
        rendered = int(render_report.get("slide_count_rendered") or 0)
        expected_value = render_report.get("slide_count_expected")
        expected = expected_value if isinstance(expected_value, int) else inspection.get("slide_count")
    render_success_ratio = None
    if isinstance(expected, int) and expected > 0:
        render_success_ratio = round(rendered / expected, 4)
    return {
        "logical_slide_count": logical_count,
        "physical_slide_count": physical_count if physical_count is not None else inspection.get("slide_count"),
        "native_text_ratio": inspection_metrics.get("native_text_ratio"),
        "editable_core_ratio": inspection_metrics.get("native_text_ratio"),
        "rasterized_area_ratio": inspection_metrics.get("rasterized_area_ratio"),
        "whole_slide_raster_count": inspection_metrics.get("whole_slide_raster_count"),
        "native_table_count": inspection_metrics.get("native_table_count"),
        "native_chart_count": inspection_metrics.get("native_chart_count"),
        "native_connector_count": inspection_metrics.get("native_connector_count"),
        "media_count": _media_count(inspection),
        "average_object_count": inspection_metrics.get("average_object_count"),
        "render_success_ratio": render_success_ratio,
        "qa_info_count": _count_severity(issues, "info"),
        "qa_warning_count": _count_severity(issues, "warning"),
        "qa_error_count": _count_severity(issues, "error"),
        "qa_fatal_count": _count_severity(issues, "fatal"),
    }


def _media_count(inspection: dict[str, Any]) -> int:
    count = 0
    for slide in inspection.get("slides", []) or []:
        if not isinstance(slide, dict):
            continue
        for obj in slide.get("objects", []) or []:
            if isinstance(obj, dict) and obj.get("shape_type") in {"picture", "svg", "media", "ole"}:
                count += 1
    return count


def _count_severity(issues: list[dict[str, Any]], severity: str) -> int:
    return len([issue for issue in issues if issue.get("severity") == severity])


def _json_int(data: Optional[dict[str, Any]], keys: list[str]) -> Optional[int]:
    cursor: Any = data
    for key in keys:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(key)
    return cursor if isinstance(cursor, int) else None


def _deck_id(ppt_ir: Optional[dict[str, Any]], build_manifest: Optional[dict[str, Any]], pptx_path: Path) -> str:
    if isinstance(build_manifest, dict) and isinstance(build_manifest.get("deck_id"), str):
        return build_manifest["deck_id"]
    if isinstance(ppt_ir, dict):
        deck = ppt_ir.get("deck")
        if isinstance(deck, dict) and isinstance(deck.get("id"), str):
            return deck["id"]
    return pptx_path.stem


def _profile(ppt_ir: Optional[dict[str, Any]], build_manifest: Optional[dict[str, Any]]) -> str:
    if isinstance(build_manifest, dict) and build_manifest.get("profile") in {"fast", "standard", "premium"}:
        return str(build_manifest["profile"])
    if isinstance(ppt_ir, dict):
        deck = ppt_ir.get("deck")
        if isinstance(deck, dict) and deck.get("production_profile") in {"fast", "standard", "premium"}:
            return str(deck["production_profile"])
    return "standard"
