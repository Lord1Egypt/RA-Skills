#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DIMENSIONS = [
    "title_role_and_message_quality",
    "content_fidelity",
    "expression_architecture",
    "page_composition",
    "component_craft",
    "editability_hygiene",
]

METRIC_DIMENSION_MAP = {
    "title_role_and_message_quality": [
        "judgment_role_slide_count",
        "generic_judgment_title_count",
        "title_role_invalid_count",
        "unsupported_judgment_count",
    ],
    "content_fidelity": [
        "source_coverage_ratio",
        "unknown_source_ref_count",
        "assumption_count",
        "missing_required_section_count",
    ],
    "expression_architecture": [
        "primary_expression_missing_count",
        "supporting_expression_overload_count",
        "multiple_primary_anchor_count",
        "relationship_to_cards_regression_count",
    ],
    "page_composition": [
        "text_overflow_issue_count",
        "object_out_of_bounds_count",
        "blank_slide_count",
        "average_object_count",
    ],
    "component_craft": [
        "style_color_drift_count",
        "tiny_object_overload_count",
        "rasterized_table_count",
        "rasterized_chart_count",
    ],
    "editability_hygiene": [
        "native_text_ratio",
        "editable_core_ratio",
        "rasterized_area_ratio",
        "whole_slide_raster_count",
        "render_success_ratio",
        "qa_error_count",
        "qa_fatal_count",
    ],
}

HARD_GATE_SEVERITIES = {"error", "fatal"}
WARNING_SEVERITIES = {"warning"}
TRUSTED_SCORER_TYPES = {"human_reference", "model"}
ABSOLUTE_PATH = re.compile(r"(?:/Users/|/home/|/tmp/|[A-Za-z]:\\)")


class ScoreInputError(ValueError):
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
        raise ScoreInputError(f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ScoreInputError(f"{path} must contain a JSON object")
    return data


def write_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def resolve_case_path(case_path: Path, ref: Optional[str]) -> Optional[Path]:
    if not ref:
        return None
    candidate = Path(ref)
    if candidate.is_absolute():
        return candidate
    return case_path.parent / candidate


def build_rubric_score(
    *,
    case: dict[str, Any],
    case_path: Path,
    ppt_ir: Optional[dict[str, Any]],
    qa_report: Optional[dict[str, Any]],
    build_manifest: Optional[dict[str, Any]],
    scorer_name: str = "automatic-metrics",
    scorer_version: str = "1.0",
    use_reference_rubric: bool = False,
    pptx_path: Optional[Path] = None,
) -> dict[str, Any]:
    case_id = str(case.get("case_id") or "")
    if not case_id:
        raise ScoreInputError("case.case_id is required")
    build_id = _build_id(case_id, build_manifest)
    qa_metrics = qa_report.get("metrics", {}) if isinstance(qa_report, dict) and isinstance(qa_report.get("metrics"), dict) else {}
    case_metrics = case.get("expected_metrics", {}) if isinstance(case.get("expected_metrics"), dict) else {}
    metrics = dict(case_metrics)
    metrics.update(qa_metrics)
    issues = qa_report.get("issues", []) if isinstance(qa_report, dict) and isinstance(qa_report.get("issues"), list) else []
    issue_counts = _issue_counts(issues)
    automatic_evidence = build_automatic_evidence(metrics, issue_counts, ppt_ir)
    reference_score = _load_reference_score(case, case_path) if use_reference_rubric else None
    if reference_score:
        render_report = _render_report(qa_report)
        if pptx_path is None:
            pptx_path = _manifest_pptx_path(build_manifest, case_path)
        validate_reference_rubric(
            reference_score,
            case_id=case_id,
            build_id=build_id,
            deck_id=_deck_id(case_id, ppt_ir, build_manifest, qa_report),
            pptx_path=pptx_path,
            render_report=render_report,
        )
        dimensions = _dimensions_from_reference(reference_score, automatic_evidence)
        manual_review_required = False
        scorer = reference_score.get("scorer") if isinstance(reference_score.get("scorer"), dict) else {
            "type": "human_reference",
            "name": "fixture-reference",
            "version": "1.0",
        }
        notes = list(reference_score.get("notes", [])) if isinstance(reference_score.get("notes"), list) else []
        notes.append("Final rubric values came from the case reference rubric, not model self-judgment.")
    else:
        dimensions = _provisional_dimensions(automatic_evidence)
        manual_review_required = True
        scorer = {
            "type": "automatic_metrics",
            "name": scorer_name,
            "version": scorer_version,
        }
        notes = [
            "No model or human scorer was configured; dimension scores are provisional automatic evidence only.",
            "manual_review_required is true because automatic metrics do not replace human judgment.",
        ]
    total_score = _total_score(dimensions)
    hard_gate_status = hard_gate_status_from_qa(qa_report)
    rubric_status = rubric_quality_status(total_score, dimensions, manual_review_required)
    overall_status = overall_status_from_parts(hard_gate_status, rubric_status)
    return {
        "schema_version": "1.0",
        "generated_at": iso_now(),
        "case_id": case_id,
        "build_id": build_id,
        "deck_id": _deck_id(case_id, ppt_ir, build_manifest, qa_report),
        "scorer": scorer,
        "dimensions": dimensions,
        "automatic_evidence": automatic_evidence,
        "total_score": total_score,
        "hard_gate_status": hard_gate_status,
        "rubric_quality_status": rubric_status,
        "overall_status": overall_status,
        "manual_review_required": manual_review_required,
        "evidence_binding": dict(reference_score["bindings"]) if reference_score else None,
        "decoupling": {
            "fatal_or_error_prevents_pass": hard_gate_status == "failed",
            "score_below_14_fails_quality": total_score is not None and total_score < 14,
            "zero_dimension_fails_quality": any(item.get("score") == 0 for item in dimensions),
        },
        "notes": notes,
    }


def build_automatic_evidence(
    metrics: dict[str, Any],
    issue_counts: dict[str, int],
    ppt_ir: Optional[dict[str, Any]],
) -> dict[str, Any]:
    enriched = dict(metrics)
    enriched.update(issue_counts)
    enriched.update(_ppt_ir_metrics(ppt_ir))
    evidence: dict[str, Any] = {}
    for dimension, keys in METRIC_DIMENSION_MAP.items():
        values = {key: enriched.get(key) for key in keys if key in enriched}
        evidence[dimension] = {
            "metrics": values,
            "provisional_score": provisional_score_for_dimension(dimension, enriched),
            "limits": "Automatic metrics are calibration evidence, not a final rubric judgment.",
        }
    return evidence


def provisional_score_for_dimension(dimension: str, metrics: dict[str, Any]) -> int:
    score = 3
    if dimension == "title_role_and_message_quality":
        score -= min(3, _int(metrics, "generic_judgment_title_count") + _int(metrics, "title_role_invalid_count") + _int(metrics, "unsupported_judgment_count"))
    elif dimension == "content_fidelity":
        coverage = _float(metrics, "source_coverage_ratio")
        if coverage is not None and coverage < 0.8:
            score -= 1
        score -= min(2, _int(metrics, "unknown_source_ref_count") + _int(metrics, "missing_required_section_count"))
    elif dimension == "expression_architecture":
        score -= min(
            3,
            _int(metrics, "primary_expression_missing_count")
            + _int(metrics, "multiple_primary_anchor_count")
            + _int(metrics, "relationship_to_cards_regression_count"),
        )
    elif dimension == "page_composition":
        score -= min(3, _int(metrics, "text_overflow_issue_count") + _int(metrics, "object_out_of_bounds_count") + _int(metrics, "blank_slide_count"))
        average_objects = _float(metrics, "average_object_count")
        if average_objects is not None and average_objects > 55:
            score -= 1
    elif dimension == "component_craft":
        score -= min(
            3,
            _int(metrics, "style_color_drift_count")
            + _int(metrics, "tiny_object_overload_count")
            + _int(metrics, "rasterized_table_count")
            + _int(metrics, "rasterized_chart_count"),
        )
    elif dimension == "editability_hygiene":
        score -= min(3, _int(metrics, "qa_fatal_count") * 2 + _int(metrics, "qa_error_count") + _int(metrics, "whole_slide_raster_count"))
        native_text_ratio = _float(metrics, "native_text_ratio")
        if native_text_ratio is not None and native_text_ratio < 0.75:
            score -= 1
        render_success_ratio = _float(metrics, "render_success_ratio")
        if render_success_ratio is not None and render_success_ratio < 1.0:
            score -= 1
    return max(0, min(3, score))


def hard_gate_status_from_qa(qa_report: Optional[dict[str, Any]]) -> str:
    if not isinstance(qa_report, dict):
        return "manual_review_required"
    status = qa_report.get("status")
    issues = qa_report.get("issues", []) if isinstance(qa_report.get("issues"), list) else []
    severities = {str(issue.get("severity")) for issue in issues if isinstance(issue, dict)}
    if status in {"fail", "blocked"} or severities & HARD_GATE_SEVERITIES:
        return "failed"
    if status == "warning" or severities & WARNING_SEVERITIES:
        return "warning"
    if status == "pass":
        return "passed"
    return "manual_review_required"


def rubric_quality_status(total_score: Optional[int], dimensions: list[dict[str, Any]], manual_review_required: bool) -> str:
    if manual_review_required or total_score is None:
        return "manual_review_required"
    if total_score < 14:
        return "failed"
    if any(item.get("score") == 0 for item in dimensions):
        return "failed"
    return "passed"


def overall_status_from_parts(hard_gate_status: str, rubric_status: str) -> str:
    if "failed" in {hard_gate_status, rubric_status}:
        return "failed"
    if "manual_review_required" in {hard_gate_status, rubric_status}:
        return "manual_review_required"
    if "warning" in {hard_gate_status, rubric_status}:
        return "warning"
    return "passed"


def _provisional_dimensions(automatic_evidence: dict[str, Any]) -> list[dict[str, Any]]:
    dimensions = []
    for dimension in DIMENSIONS:
        item = automatic_evidence.get(dimension, {})
        dimensions.append(
            {
                "dimension": dimension,
                "score": None,
                "provisional_score": item.get("provisional_score"),
                "evidence": ["Automatic evidence collected; final rubric judgment not available."],
                "automatic_metrics": item.get("metrics", {}),
                "confidence": 0.0,
                "manual_review_required": True,
            }
        )
    return dimensions


def _dimensions_from_reference(reference_score: dict[str, Any], automatic_evidence: dict[str, Any]) -> list[dict[str, Any]]:
    by_dimension = {
        str(item.get("dimension")): item
        for item in reference_score.get("dimensions", [])
        if isinstance(item, dict)
    }
    dimensions = []
    for dimension in DIMENSIONS:
        ref_item = by_dimension.get(dimension, {})
        score = ref_item.get("score")
        if not isinstance(score, int) or score < 0 or score > 3:
            raise ScoreInputError(f"reference rubric for {dimension} must contain integer score 0-3")
        evidence = ref_item.get("evidence")
        if not isinstance(evidence, list) or not evidence or any(not isinstance(item, str) or not item.strip() for item in evidence):
            raise ScoreInputError(f"reference rubric for {dimension} must contain non-empty evidence")
        if any(ABSOLUTE_PATH.search(item) for item in evidence):
            raise ScoreInputError(f"reference rubric for {dimension} evidence contains an absolute local path")
        auto = automatic_evidence.get(dimension, {})
        dimensions.append(
            {
                "dimension": dimension,
                "score": score,
                "provisional_score": auto.get("provisional_score"),
                "evidence": evidence,
                "automatic_metrics": auto.get("metrics", {}),
                "confidence": ref_item.get("confidence") if isinstance(ref_item.get("confidence"), (int, float)) else 1.0,
                "manual_review_required": False,
            }
        )
    return dimensions


def _load_reference_score(case: dict[str, Any], case_path: Path) -> Optional[dict[str, Any]]:
    ref_path = resolve_case_path(case_path, case.get("reference_rubric") if isinstance(case.get("reference_rubric"), str) else None)
    if ref_path is None or not ref_path.exists():
        return None
    return load_json(ref_path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _canonical_render_report(report: dict[str, Any]) -> dict[str, Any]:
    def clean(value: Any, key: str = "") -> Any:
        if isinstance(value, dict):
            return {name: clean(item, name) for name, item in sorted(value.items())}
        if isinstance(value, list):
            return [clean(item, key) for item in value]
        if isinstance(value, str) and key in {"pptx", "pdf", "pdf_path", "image"}:
            # Bind report semantics, not transient/renamed package paths. PPTX
            # bytes and rendered image bytes are bound separately below.
            return f"<{key}>"
        return value
    return clean(report)


def _json_sha256(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def render_evidence_sha256(report: dict[str, Any]) -> str:
    slides = report.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ScoreInputError("render report must contain rendered slide evidence")
    digest = hashlib.sha256()
    for item in sorted((item for item in slides if isinstance(item, dict)), key=lambda item: int(item.get("slide_index") or 0)):
        image = item.get("image")
        if not isinstance(image, str) or not Path(image).is_file():
            raise ScoreInputError("render report slide image evidence is missing")
        digest.update(str(item.get("slide_index")).encode("ascii"))
        digest.update(bytes.fromhex(sha256_file(Path(image)).split(":", 1)[1]))
    return "sha256:" + digest.hexdigest()


def build_evidence_binding(pptx_path: Path, render_report: dict[str, Any]) -> dict[str, str]:
    if not pptx_path.is_file():
        raise ScoreInputError("current PPTX is missing")
    if render_report.get("status") != "passed":
        raise ScoreInputError("render report must be passed")
    return {
        "pptx_sha256": sha256_file(pptx_path),
        "render_report_sha256": _json_sha256(_canonical_render_report(render_report)),
        "render_evidence_sha256": render_evidence_sha256(render_report),
    }


def validate_reference_rubric(
    reference: dict[str, Any], *, case_id: str, build_id: str, deck_id: str,
    pptx_path: Optional[Path], render_report: Optional[dict[str, Any]],
) -> None:
    bindings = reference.get("bindings")
    if not isinstance(bindings, dict):
        raise ScoreInputError("reference rubric bindings are required")
    expected_ids = {"case_id": case_id, "build_id": build_id, "deck_id": deck_id}
    for field, expected in expected_ids.items():
        if reference.get(field) != expected or bindings.get(field) != expected:
            raise ScoreInputError(f"reference rubric {field} does not match current evidence")
    scorer = reference.get("scorer")
    provenance = scorer.get("provenance") if isinstance(scorer, dict) else None
    if (
        not isinstance(scorer, dict)
        or scorer.get("type") not in TRUSTED_SCORER_TYPES
        or not all(isinstance(scorer.get(field), str) and scorer[field].strip() for field in ("name", "version"))
        or not isinstance(provenance, dict)
        or not all(isinstance(provenance.get(field), str) and provenance[field].strip() for field in ("review_id", "reviewed_at", "method"))
    ):
        raise ScoreInputError("reference rubric scorer provenance is not trusted")
    if pptx_path is None or render_report is None:
        raise ScoreInputError("reference rubric requires current PPTX and render evidence")
    actual = build_evidence_binding(pptx_path, render_report)
    for field, digest in actual.items():
        if bindings.get(field) != digest:
            raise ScoreInputError(f"reference rubric {field} does not match current evidence")


def _render_report(qa_report: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
    evidence = qa_report.get("evidence") if isinstance(qa_report, dict) else None
    report = evidence.get("render_report") if isinstance(evidence, dict) else None
    return report if isinstance(report, dict) else None


def _manifest_pptx_path(build_manifest: Optional[dict[str, Any]], case_path: Path) -> Optional[Path]:
    raw = build_manifest.get("outputs", {}).get("deck") if isinstance(build_manifest, dict) and isinstance(build_manifest.get("outputs"), dict) else None
    if not isinstance(raw, str) or not raw:
        return None
    path = Path(raw)
    return path if path.is_absolute() else case_path.parent / path


def _total_score(dimensions: list[dict[str, Any]]) -> Optional[int]:
    scores = [item.get("score") for item in dimensions]
    if not all(isinstance(score, int) for score in scores):
        return None
    return int(sum(scores))


def _issue_counts(issues: list[Any]) -> dict[str, int]:
    counts = {
        "text_overflow_issue_count": 0,
        "object_out_of_bounds_count": 0,
        "blank_slide_count": 0,
        "style_color_drift_count": 0,
        "tiny_object_overload_count": 0,
        "rasterized_table_count": 0,
        "rasterized_chart_count": 0,
    }
    code_map = {
        "TEXT_OVERFLOW_RISK": "text_overflow_issue_count",
        "PPTX_TEXT_OUT_OF_BOUNDS": "object_out_of_bounds_count",
        "PPTX_BLANK_SLIDE": "blank_slide_count",
        "STYLE_COLOR_DRIFT": "style_color_drift_count",
        "PPTX_TINY_OBJECT_OVERLOAD": "tiny_object_overload_count",
        "PPTX_TABLE_NOT_NATIVE": "rasterized_table_count",
        "PPTX_CHART_NOT_NATIVE": "rasterized_chart_count",
    }
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        key = code_map.get(str(issue.get("issue_code")))
        if key:
            counts[key] += 1
    return counts


def _ppt_ir_metrics(ppt_ir: Optional[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(ppt_ir, dict):
        return {}
    slides = ppt_ir.get("slides", [])
    if not isinstance(slides, list):
        return {}
    metrics = {
        "judgment_role_slide_count": 0,
        "generic_judgment_title_count": 0,
        "title_role_invalid_count": 0,
        "unsupported_judgment_count": 0,
        "primary_expression_missing_count": 0,
        "supporting_expression_overload_count": 0,
        "multiple_primary_anchor_count": 0,
        "relationship_to_cards_regression_count": 0,
        "unknown_source_ref_count": 0,
    }
    generic_titles = {"overview", "summary", "introduction", "background", "next steps", "key points"}
    valid_title_roles = {"judgment", "navigation", "section", "instruction", "reference", "closing"}
    valid_primary = {"textual_argument", "structured_cards", "table_matrix", "data_visual", "relationship_visual", "conceptual_scene"}
    for slide in slides:
        if not isinstance(slide, dict):
            continue
        title_role = slide.get("title_role")
        if title_role == "judgment":
            metrics["judgment_role_slide_count"] += 1
            title = str(slide.get("title", "")).strip().lower()
            if title in generic_titles or len(title.split()) <= 2:
                metrics["generic_judgment_title_count"] += 1
            if not slide.get("judgment") and not slide.get("message"):
                metrics["unsupported_judgment_count"] += 1
        if title_role not in valid_title_roles:
            metrics["title_role_invalid_count"] += 1
        if slide.get("primary_expression") not in valid_primary:
            metrics["primary_expression_missing_count"] += 1
        supporting = slide.get("supporting_expressions", [])
        if isinstance(supporting, list) and len(supporting) > 3:
            metrics["supporting_expression_overload_count"] += 1
        anchor = slide.get("primary_anchor")
        if isinstance(anchor, list) and len(anchor) != 1:
            metrics["multiple_primary_anchor_count"] += 1
        if slide.get("relationship_expected") is True and slide.get("primary_expression") == "structured_cards":
            metrics["relationship_to_cards_regression_count"] += 1
        for source_ref in slide.get("source_refs", []) or []:
            if isinstance(source_ref, dict) and str(source_ref.get("source_id", "")).startswith("unknown"):
                metrics["unknown_source_ref_count"] += 1
    return metrics


def _int(metrics: dict[str, Any], key: str) -> int:
    value = metrics.get(key)
    return value if isinstance(value, int) else 0


def _float(metrics: dict[str, Any], key: str) -> Optional[float]:
    value = metrics.get(key)
    return float(value) if isinstance(value, (int, float)) else None


def _build_id(case_id: str, build_manifest: Optional[dict[str, Any]]) -> str:
    if isinstance(build_manifest, dict) and isinstance(build_manifest.get("build_id"), str):
        return build_manifest["build_id"]
    return f"{case_id}-unknown-build"


def _deck_id(
    case_id: str,
    ppt_ir: Optional[dict[str, Any]],
    build_manifest: Optional[dict[str, Any]],
    qa_report: Optional[dict[str, Any]],
) -> str:
    for data, keys in [
        (build_manifest, ["deck_id"]),
        (qa_report, ["deck_id"]),
        (ppt_ir, ["deck", "id"]),
    ]:
        cursor: Any = data
        for key in keys:
            if not isinstance(cursor, dict):
                cursor = None
                break
            cursor = cursor.get(key)
        if isinstance(cursor, str) and cursor:
            return cursor
    return case_id


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a calibrated rubric scorecard from benchmark inputs and QA evidence.")
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--ppt-ir", type=Path)
    parser.add_argument("--qa-report", type=Path)
    parser.add_argument("--build-manifest", type=Path)
    parser.add_argument("--pptx", type=Path, help="Current PPTX whose bytes the reference rubric must bind.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--use-reference-rubric", action="store_true", help="Use the case's human/reference rubric as final scores.")
    parser.add_argument("--scorer-name", default="automatic-metrics")
    parser.add_argument("--scorer-version", default="1.0")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        case = load_json(args.case)
        assert case is not None
        score = build_rubric_score(
            case=case,
            case_path=args.case,
            ppt_ir=load_json(args.ppt_ir),
            qa_report=load_json(args.qa_report),
            build_manifest=load_json(args.build_manifest),
            scorer_name=args.scorer_name,
            scorer_version=args.scorer_version,
            use_reference_rubric=args.use_reference_rubric,
            pptx_path=args.pptx,
        )
        write_json(score, args.output)
        return 0 if score["overall_status"] in {"passed", "warning", "manual_review_required"} else 1
    except ScoreInputError as exc:
        print(str(exc), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
