#!/usr/bin/env python3
"""Migrate article-html-to-ppt v1 slide manifests to v2 PPT IR."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

TITLE_ROLE_BY_SLIDE_ROLE = {
    "cover": "navigation",
    "agenda": "navigation",
    "section": "section",
    "reference": "reference",
    "closing": "closing",
    "instruction": "instruction",
}
PRIMARY_MAP = {
    "textual_argument": "textual_argument",
    "structured_cards": "structured_cards",
    "table_matrix": "table_matrix",
    "data_visual": "data_visual",
    "relationship_visual": "relationship_visual",
    "conceptual_scene": "conceptual_scene",
    "hybrid_panel": "structured_cards",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_refs_from_labels(labels: Any) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for label in labels or []:
        refs.append({
            "source_id": "src-001",
            "locator": str(label),
            "claim_type": "direct",
            "note": "Migrated from source_labels.",
        })
    return refs


def object_from_visual_plan(plan: Any, slide_id: str) -> list[dict[str, Any]]:
    if not plan:
        return []
    if isinstance(plan, str):
        lowered = plan.lower()
        obj_type = "diagram" if any(word in lowered for word in ["flow", "relationship", "architecture", "diagram", "map"]) else "chart" if "chart" in lowered else "image" if "image" in lowered else "shape"
        return [{
            "id": f"{slide_id}-visual-1",
            "type": obj_type,
            "semantic_role": "primary_visual",
            "content": plan,
            "source_refs": [],
            "editability": "native_preferred",
            "priority": "primary",
        }]
    if isinstance(plan, dict):
        obj_type = plan.get("type") or plan.get("component_type") or "diagram"
        return [{
            "id": plan.get("id", f"{slide_id}-visual-1"),
            "type": obj_type,
            "semantic_role": plan.get("semantic_role", "primary_visual"),
            "content": plan,
            "source_refs": plan.get("source_refs", []),
            "editability": plan.get("editability", "native_preferred"),
            "priority": plan.get("priority", "primary"),
        }]
    if isinstance(plan, list):
        objects: list[dict[str, Any]] = []
        for idx, item in enumerate(plan, 1):
            objects.extend(object_from_visual_plan(item, f"{slide_id}-visual-{idx}"))
        return objects
    return []


def migrate_slide(raw: dict[str, Any], index: int) -> dict[str, Any]:
    slide_id = raw.get("id") or raw.get("slide_id") or f"S{index:02d}"
    slide_role = raw.get("slide_role") or raw.get("role") or "judgment"
    expression = raw.get("expression_mode") or raw.get("primary_expression") or "textual_argument"
    primary_expression = PRIMARY_MAP.get(expression, "textual_argument")
    supporting = list(raw.get("supporting_expressions") or [])
    if expression == "hybrid_panel" and "interpretation" not in supporting:
        supporting.append("interpretation")
    title = raw.get("title") or raw.get("judgment_title") or f"Slide {index}"
    title_role = raw.get("title_role") or TITLE_ROLE_BY_SLIDE_ROLE.get(slide_role, "judgment")
    judgment = raw.get("judgment")
    if not judgment and raw.get("judgment_title") and title_role == "judgment":
        judgment = raw.get("judgment_title")
    source_refs = raw.get("source_refs") or source_refs_from_labels(raw.get("source_labels"))
    objects = raw.get("objects") or object_from_visual_plan(raw.get("visual_component_plan"), slide_id)
    return {
        "id": slide_id,
        "index": raw.get("index") or index,
        "slide_role": slide_role,
        "title_role": title_role,
        "title": title,
        "judgment": judgment if title_role == "judgment" else None,
        "message": raw.get("message") or raw.get("audience_action") or raw.get("claim") or "",
        "audience_question": raw.get("audience_question") or "",
        "source_refs": source_refs,
        "primary_expression": primary_expression,
        "primary_expression_reason": raw.get("primary_expression_reason") or raw.get("expression_mode_reason") or "Migrated from v1 manifest.",
        "supporting_expressions": supporting,
        "page_archetype": raw.get("page_archetype") or raw.get("layout_family") or "unspecified",
        "layout_intent": raw.get("layout_intent") or raw.get("visual_job") or "unspecified",
        "primary_anchor": raw.get("primary_anchor") or "primary visual group",
        "density": raw.get("density") if isinstance(raw.get("density"), dict) else {
            "level": raw.get("density_label", "medium"),
            "reason": raw.get("density_reason", "Migrated from v1 manifest."),
        },
        "objects": objects,
        "delivery_contract": {
            "preferred_route": raw.get("visual_component_delivery") or raw.get("preferred_route") or "native_ppt",
            "editable_core": raw.get("editable_core") or [],
            "raster_allowance": raw.get("raster_allowance") or [],
            "forbidden_raster": raw.get("forbidden_raster") or ["title", "judgment", "data_labels"],
        },
        "qa_expectations": raw.get("qa_expectations") or [],
    }


def migrate(data: dict[str, Any]) -> dict[str, Any]:
    slides_raw = data.get("slides") or data.get("slide_manifest") or []
    sources = data.get("sources") or [{
        "source_id": "src-001",
        "type": data.get("source_type", "article"),
        "title": data.get("source_title", "source"),
        "path": data.get("source_path", ""),
    }]
    return {
        "schema_version": "2.0",
        "deck": {
            "id": data.get("deck_id", "deck-migrated"),
            "title": data.get("title", "Migrated Deck"),
            "source_type": data.get("source_type", "article"),
            "audience": data.get("audience", ""),
            "purpose": data.get("purpose", ""),
            "language": data.get("language", "zh-CN"),
            "formality": data.get("formality", "internal"),
            "presentation_context": data.get("presentation_context", "document"),
            "aspect_ratio": data.get("aspect_ratio", "16:9"),
            "production_profile": data.get("production_profile", "standard"),
            "target_builder": data.get("target_builder", "auto"),
            "logical_slide_count": len(slides_raw),
        },
        "sources": sources,
        "style_contract_ref": data.get("style_contract_ref", "style-contract.json"),
        "asset_manifest_ref": data.get("asset_manifest_ref", "asset-manifest.json"),
        "slides": [migrate_slide(slide, idx + 1) for idx, slide in enumerate(slides_raw)],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate v1 slide manifest to v2 PPT IR.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    migrated = migrate(load_json(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(migrated, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
