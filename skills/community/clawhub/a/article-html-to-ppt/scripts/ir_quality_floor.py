"""Minimum semantic completeness checks for Path B PPT IR."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DATA_COMPONENTS = {"bar_chart", "line_chart", "pie_chart", "native_table", "heat_matrix", "kpi_dashboard", "metric_card"}
SUBSTANTIVE_SUPPORT_COMPONENTS = {"evidence_block", "metric_card", "comparison_card", "summary_action_card"}
NAVIGATION_ROLES = {"cover", "agenda", "section", "reference"}
PRIMARY_EVIDENCE_COMPONENTS = DATA_COMPONENTS | {"metric_card"}
GENERATED_SUPPORT_DERIVATION = "same_slide_evidence_augmenter"


def _content_tokens(value: str) -> set[str]:
    return {char for char in value.replace(" ", "") if char.strip()}


def _is_near_duplicate(value: str, baseline: str) -> bool:
    candidate, existing = _content_tokens(value), _content_tokens(baseline)
    if not candidate or not existing:
        return False
    return len(candidate & existing) / len(candidate | existing) >= 0.75


def _repeats_claim(value: str, claim: str) -> bool:
    candidate, baseline = _content_tokens(value), _content_tokens(claim)
    if not candidate or not baseline:
        return False
    overlap = len(candidate & baseline)
    return (
        overlap / len(candidate | baseline) >= 0.75
        or overlap / len(candidate) >= 0.9
    )


def _normalize_text(value: str) -> str:
    return " ".join(value.replace("\n", " ").split())


def _component_type(obj: dict[str, Any]) -> str:
    return str(obj.get("component_type") or obj.get("type") or "")


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return _normalize_text(content)
    if isinstance(content, dict):
        title = content.get("title")
        claim = content.get("claim")
        if isinstance(title, str) and title.strip() and isinstance(claim, str) and claim.strip():
            return _normalize_text(f"{title}\n{claim}")
        items = content.get("items")
        if isinstance(title, str) and title.strip() and isinstance(items, list):
            summaries = [
                _normalize_text(str(item.get("summary") or ""))
                for item in items
                if isinstance(item, dict) and str(item.get("summary") or "").strip()
            ]
            if summaries:
                return _normalize_text(f"{title}\n" + "\n".join(summaries))
        for key in ("title", "label", "claim", "text", "value"):
            value = content.get(key)
            if isinstance(value, str) and value.strip():
                return _normalize_text(value)
    return ""


def _source_ref_markers(source_refs: Any) -> set[str]:
    markers: set[str] = set()
    for ref in source_refs or []:
        if isinstance(ref, dict):
            markers.add(json.dumps(ref, ensure_ascii=False, sort_keys=True))
    return markers


def _looks_like_generated_same_slide_support(obj: dict[str, Any]) -> bool:
    provenance = obj.get("provenance")
    if isinstance(provenance, dict) and provenance.get("derivation") == GENERATED_SUPPORT_DERIVATION:
        return True
    if _component_type(obj) != "evidence_block" or obj.get("priority") == "primary":
        return False
    score = 0
    if str(obj.get("id") or "").endswith("-same-slide-evidence-comparison"):
        score += 2
    if _content_text(obj.get("content")).startswith("同页来源证据："):
        score += 2
    if str(obj.get("semantic_role") or "") == "interpretation":
        score += 1
    if str(obj.get("editability") or "") == "native_required":
        score += 1
    preferences = obj.get("delivery_preferences")
    if (
        isinstance(preferences, dict)
        and preferences.get("preferred_route") == "native_ppt"
        and list(preferences.get("allowed_fallbacks") or []) == []
    ):
        score += 1
    return score >= 4


def _generated_support_has_valid_provenance(obj: dict[str, Any], objects: list[dict[str, Any]]) -> bool:
    support_markers = _source_ref_markers(obj.get("source_refs"))
    if not support_markers:
        return False
    provenance = obj.get("provenance")
    if not isinstance(provenance, dict) or provenance.get("derivation") != GENERATED_SUPPORT_DERIVATION:
        return False
    if provenance.get("source_ref_scope") != "object_level_only":
        return False
    derived_ids = [item for item in provenance.get("derived_from_object_ids", []) if isinstance(item, str) and item.strip()]
    unique_ids = set(derived_ids)
    if len(unique_ids) < 2:
        return False
    by_id = {str(item.get("id") or ""): item for item in objects if isinstance(item, dict)}
    expected_markers: set[str] = set()
    for derived_id in unique_ids:
        source_obj = by_id.get(derived_id)
        if not isinstance(source_obj, dict):
            return False
        if source_obj.get("priority") != "primary" or _component_type(source_obj) not in PRIMARY_EVIDENCE_COMPONENTS:
            return False
        object_markers = _source_ref_markers(source_obj.get("source_refs"))
        if not object_markers or not (support_markers & object_markers):
            return False
        expected_markers.update(object_markers)
    return support_markers == expected_markers


def _support_has_independent_provenance(obj: dict[str, Any], objects: list[dict[str, Any]]) -> bool:
    if _looks_like_generated_same_slide_support(obj):
        return _generated_support_has_valid_provenance(obj, objects)
    return bool(_source_ref_markers(obj.get("source_refs")))


def assess_ir_quality_floor(ppt_ir: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    for slide in ppt_ir.get("slides", []) or []:
        if not isinstance(slide, dict):
            continue
        slide_id = str(slide.get("id") or "unknown-slide")
        role = str(slide.get("slide_role") or "")
        expression = str(slide.get("primary_expression") or "")
        objects = [obj for obj in slide.get("objects", []) or [] if isinstance(obj, dict)]
        kinds = {_component_type(obj) for obj in objects}
        support_objects = [obj for obj in objects if _component_type(obj) in SUBSTANTIVE_SUPPORT_COMPONENTS and obj.get("priority") != "primary"]
        support_count = len(support_objects)

        if role in NAVIGATION_ROLES:
            continue
        if role in {"data", "judgment"}:
            slide_claims = [str(slide.get(key) or "") for key in ("title", "judgment", "message")]
            for obj in support_objects:
                content = _content_text(obj.get("content"))
                if content and any(_repeats_claim(content, claim) for claim in slide_claims):
                    issues.append(_issue(slide_id, "IR_SUPPORTING_EVIDENCE_DUPLICATES_SLIDE_CLAIM", "Supporting evidence must add independently sourced information, not repeat the slide claim."))
        if role == "closing":

            actions = sum(1 for obj in objects if str(obj.get("component_type") or obj.get("type") or "") == "summary_action_card")
            if actions < 2:
                issues.append(_issue(slide_id, "IR_CLOSING_ACTIONS_INSUFFICIENT", "Closing slides require 2–4 actionable native objects."))
            continue
        if role == "data" or expression == "data_visual":
            data_objects = [obj for obj in objects if _component_type(obj) in DATA_COMPONENTS]
            if not data_objects:
                issues.append(_issue(slide_id, "IR_PRIMARY_DATA_OBJECT_REQUIRED", "Data slides require a source-backed native chart, table, matrix, or KPI dashboard."))
            for obj in data_objects:
                if not obj.get("source_refs"):
                    issues.append(_issue(slide_id, "IR_DATA_OBJECT_SOURCE_REQUIRED", "Each primary data object must carry its own source reference."))
                content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
                categories = content.get("categories") if isinstance(content.get("categories"), list) else []
                series = content.get("series") if isinstance(content.get("series"), list) else []
                if categories and any(not isinstance(item, dict) or not isinstance(item.get("values"), list) or len(item["values"]) != len(categories) for item in series):
                    issues.append(_issue(slide_id, "IR_CHART_SERIES_LENGTH_INVALID", "Each chart series must have exactly one value per category."))
            if support_count < 1:
                issues.append(_issue(slide_id, "IR_SUPPORTING_EVIDENCE_REQUIRED", "Data slides require at least one supporting interpretation or evidence object."))
            elif not any(_support_has_independent_provenance(obj, objects) for obj in support_objects):
                issues.append(_issue(slide_id, "IR_SUPPORTING_OBJECT_SOURCE_REQUIRED", "Supporting evidence must carry an independent source reference."))
        elif role == "judgment":
            if support_count < 1:
                issues.append(_issue(slide_id, "IR_SUPPORTING_EVIDENCE_REQUIRED", "Judgment slides require at least one supporting evidence or interpretation object."))
            elif not any(_support_has_independent_provenance(obj, objects) for obj in support_objects):
                issues.append(_issue(slide_id, "IR_SUPPORTING_OBJECT_SOURCE_REQUIRED", "Supporting evidence must carry an independent source reference."))
    return {"status": "blocked" if issues else "passed", "issues": issues}


def _issue(slide_id: str, code: str, message: str) -> dict[str, str]:
    return {"slide_id": slide_id, "code": code, "severity": "blocked", "message": message}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Assess Path B PPT IR semantic completeness.")
    parser.add_argument("--ppt-ir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.ppt_ir.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ValueError("ppt-ir must be a JSON object")
        report = assess_ir_quality_floor(document)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 2 if args.strict and report["status"] != "passed" else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ir_quality_floor: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
