"""Deterministic, source-bound supporting-object enrichment for Path B IR."""
from __future__ import annotations

from copy import deepcopy
import json
from typing import Any

DATA_COMPONENTS = {"bar_chart", "line_chart", "pie_chart", "native_table", "heat_matrix", "kpi_dashboard", "metric_card"}
SUBSTANTIVE_SUPPORT_COMPONENTS = {"evidence_block", "metric_card", "comparison_card", "summary_action_card"}
PRIMARY_EVIDENCE_COMPONENTS = DATA_COMPONENTS | {"metric_card"}
GENERATED_SUPPORT_DERIVATION = "same_slide_evidence_augmenter"


def _content_tokens(value: str) -> set[str]:
    """Use CJK characters and word tokens for conservative duplicate detection."""
    return {char for char in value.replace(" ", "") if char.strip()}


def _is_near_duplicate(value: str, existing: str) -> bool:
    candidate, baseline = _content_tokens(value), _content_tokens(existing)
    if not candidate or not baseline:
        return False
    return len(candidate & baseline) / len(candidate | baseline) >= 0.75


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


def _dedupe_source_refs(source_refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref in source_refs:
        if not isinstance(ref, dict):
            continue
        marker = json.dumps(ref, ensure_ascii=False, sort_keys=True)
        if marker in seen:
            continue
        seen.add(marker)
        unique.append(deepcopy(ref))
    return unique


def _extract_object_summary(obj: dict[str, Any]) -> str | None:
    component = _component_type(obj)
    content = obj.get("content")
    if component == "metric_card" and isinstance(content, str):
        return _normalize_text(content)
    if component in {"bar_chart", "line_chart", "pie_chart"} and isinstance(content, dict):
        categories = [str(item) for item in content.get("categories", []) if str(item).strip()]
        series = [item for item in content.get("series", []) if isinstance(item, dict)]
        if not categories or not series:
            return None
        series_summaries: list[str] = []
        for series_item in series[:2]:
            values = series_item.get("values")
            if not isinstance(values, list) or not values:
                continue
            points = ", ".join(f"{category}={value}" for category, value in zip(categories[:4], values[:4]))
            if not points:
                continue
            label = _normalize_text(str(series_item.get("name") or "series"))
            series_summaries.append(f"{label}: {points}")
        return " / ".join(series_summaries) or None
    if component == "native_table" and isinstance(content, dict):
        headers = [str(item) for item in content.get("headers", []) if str(item).strip()]
        body = [row for row in content.get("body", []) if isinstance(row, list) and len(row) >= 2]
        if not headers or not body:
            return None
        row_summaries: list[str] = []
        for row in body[:4]:
            key = _normalize_text(str(row[0]))
            values = " / ".join(_normalize_text(str(cell)) for cell in row[1:] if str(cell).strip())
            if key and values:
                row_summaries.append(f"{key}={values}")
        if not row_summaries:
            return None
        header_prefix = " / ".join(headers[: min(len(headers), 3)])
        return f"{header_prefix}: {'; '.join(row_summaries)}"
    if isinstance(content, str):
        normalized = _normalize_text(content)
        return normalized or None
    return None


def _slide_claims(slide: dict[str, Any]) -> list[str]:
    return [
        normalized
        for normalized in (_normalize_text(str(slide.get(key) or "")) for key in ("title", "judgment", "message"))
        if normalized
    ]


def _generated_support_text(items: list[dict[str, Any]]) -> str:
    return f"同页来源证据：{'；'.join(item['summary'] for item in items)}"


def _build_same_slide_support(slide: dict[str, Any], objects: list[dict[str, Any]]) -> dict[str, Any] | None:
    used_objects: list[dict[str, Any]] = []
    seen_summaries: list[str] = []
    slide_claims = _slide_claims(slide)
    for obj in objects:
        if obj.get("priority") != "primary" or not obj.get("source_refs"):
            continue
        if _component_type(obj) not in PRIMARY_EVIDENCE_COMPONENTS:
            continue
        summary = _extract_object_summary(obj)
        if not summary:
            continue
        if any(_repeats_claim(summary, claim) for claim in slide_claims):
            continue
        if any(_is_near_duplicate(summary, existing) for existing in seen_summaries):
            continue
        used_objects.append({"id": str(obj.get("id") or ""), "summary": summary, "source_refs": list(obj.get("source_refs") or [])})
        seen_summaries.append(summary)
        if len(used_objects) == 3:
            break

    if len(used_objects) < 2:
        return None

    content = _generated_support_text(used_objects)
    if any(_repeats_claim(content, claim) for claim in slide_claims):
        return None

    return {
        "id": f"{slide.get('id', 'slide')}-same-slide-evidence-comparison",
        "type": "shape",
        "component_type": "evidence_block",
        "semantic_role": "interpretation",
        "content": content,
        "source_refs": _dedupe_source_refs([ref for item in used_objects for ref in item["source_refs"] if isinstance(ref, dict)]),
        "editability": "native_required",
        "priority": "supporting",
        "delivery_preferences": {"preferred_route": "native_ppt", "allowed_fallbacks": []},
        "provenance": {
            "derivation": GENERATED_SUPPORT_DERIVATION,
            "derived_from_object_ids": [item["id"] for item in used_objects],
            "source_ref_scope": "object_level_only",
        },
    }


def enrich_ppt_ir(ppt_ir: dict[str, Any]) -> dict[str, Any]:
    enriched = deepcopy(ppt_ir)
    for slide in enriched.get("slides", []) or []:
        if not isinstance(slide, dict):
            continue
        objects = [obj for obj in slide.get("objects", []) or [] if isinstance(obj, dict)]
        slide["objects"] = objects
        kinds = {str(obj.get("component_type") or obj.get("type") or "") for obj in objects}
        has_support = any(
            str(obj.get("component_type") or obj.get("type") or "") in SUBSTANTIVE_SUPPORT_COMPONENTS
            and obj.get("priority") != "primary"
            for obj in objects
        )
        source_refs = list(slide.get("source_refs") or [])
        message = str(slide.get("judgment") or slide.get("message") or "").strip()
        title = str(slide.get("title") or "").strip()
        role = str(slide.get("slide_role") or "")
        evidence = [item for item in slide.get("supporting_evidence", []) or [] if isinstance(item, dict)]

        # A slide's message/judgment is a conclusion, never independent evidence.
        # Only an explicitly supplied, separately source-bound evidence item may be
        # compiled into a supporting native object; no data or claims are inferred.
        if role in {"data", "judgment"} and not has_support:
            has_primary_data = bool(kinds & DATA_COMPONENTS)
            candidate = next((item for item in evidence if str(item.get("content") or "").strip() and item.get("source_refs")), None)
            if candidate and (role == "judgment" or has_primary_data):
                content = str(candidate["content"]).strip()
                if not _repeats_claim(content, f"{title} {message}"):
                    objects.append({
                        "id": f"{slide.get('id', 'slide')}-source-bound-interpretation",
                        "type": "shape",
                        "component_type": "evidence_block",
                        "semantic_role": "interpretation",
                        "content": content,
                        "source_refs": list(candidate["source_refs"]),
                        "editability": "native_required",
                        "priority": "supporting",
                        "delivery_preferences": {"preferred_route": "native_ppt", "allowed_fallbacks": []},
                    })
                    has_support = True
        if role in {"data", "judgment"} and not has_support:
            generated = _build_same_slide_support(slide, objects)
            if generated and not any(str(obj.get("id") or "") == generated["id"] for obj in objects):
                objects.append(generated)
        if role == "closing":
            actions = [obj for obj in objects if str(obj.get("component_type") or obj.get("type") or "") == "summary_action_card"]
            for index, content in enumerate([title, message], start=1):
                if len(actions) >= 2 or not content:
                    break
                objects.append({
                    "id": f"{slide.get('id', 'slide')}-action-{index}",
                    "type": "shape",
                    "component_type": "summary_action_card",
                    "semantic_role": "next_action",
                    "content": content,
                    "source_refs": source_refs,
                    "editability": "native_required",
                    "priority": "primary" if index == 1 else "supporting",
                    "delivery_preferences": {"preferred_route": "native_ppt", "allowed_fallbacks": []},
                })
                actions.append(objects[-1])
    return enriched
