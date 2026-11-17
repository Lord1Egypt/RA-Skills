"""Audit model-directed Template component reuse decisions."""

from __future__ import annotations

from .component_atlas import find_feasible_components


def evaluate_component_intents(
    ir: dict,
    atlas: dict,
    *,
    require_all_content_slides: bool = True,
) -> dict:
    """Prove that feasible template components were considered and reused."""
    issues: list[dict] = []
    audits: list[dict] = []
    eligible_pages = 0
    reused_pages = 0
    justified_authored_pages = 0
    content_pages = 0
    for index, slide in enumerate(ir.get("slides", []), 1):
        if not isinstance(slide, dict):
            continue
        slide_id = str(slide.get("id") or index)
        if slide.get("slide_role", "content") in {"cover", "section", "closing"}:
            continue
        content_pages += 1
        intent = slide.get("component_intent")
        if not isinstance(intent, dict):
            if require_all_content_slides:
                issues.append({"code": "COMPONENT_INTENT_MISSING", "slide_id": slide_id})
            continue
        requirement = {
            "semantic_use": intent.get("semantic_use"),
            "element_count": intent.get("element_count"),
            "topology": intent.get("topology"),
            "required_slots": intent.get("required_slots", []),
        }
        if intent.get("family") is not None:
            requirement["family"] = intent["family"]
        for field in ("archetype", "composition_role", "text_requirements", "data_shape"):
            if intent.get(field) is not None:
                requirement[field] = intent[field]
        try:
            feasible = find_feasible_components(atlas, requirement)
        except ValueError as exc:
            issues.append({
                "code": "COMPONENT_INTENT_INVALID",
                "slide_id": slide_id,
                "message": str(exc),
            })
            continue
        feasible_ids = [item["component_id"] for item in feasible]
        declared_candidates = intent.get("candidate_component_ids", [])
        selected = intent.get("selected_component_ids", [])
        rejected = intent.get("rejected_candidates", [])
        style_references = intent.get("style_reference_component_ids", [])
        if not isinstance(declared_candidates, list):
            declared_candidates = []
        if not isinstance(selected, list):
            selected = []
        if not isinstance(style_references, list):
            style_references = []
        if intent.get("mode") == "model_authored" or intent.get("new_component_id"):
            known_ids = {
                component.get("component_id") for component in atlas.get("components", [])
                if isinstance(component, dict)
            }
            if not style_references:
                issues.append({"code": "MODEL_AUTHORED_STYLE_REFERENCE_REQUIRED", "slide_id": slide_id})
            elif not set(style_references) <= known_ids:
                issues.append({
                    "code": "MODEL_AUTHORED_STYLE_REFERENCE_UNKNOWN",
                    "slide_id": slide_id,
                    "unknown_component_ids": sorted(set(style_references) - known_ids),
                })
        if set(declared_candidates) != set(feasible_ids):
            issues.append({
                "code": "COMPONENT_CANDIDATE_AUDIT_INCOMPLETE",
                "slide_id": slide_id,
                "expected_component_ids": feasible_ids,
                "declared_component_ids": declared_candidates,
            })
        if feasible_ids:
            eligible_pages += 1
            if intent.get("mode") == "model_authored" or not selected:
                rejected_by_id = {
                    item.get("component_id"): item
                    for item in rejected
                    if isinstance(item, dict) and isinstance(item.get("component_id"), str)
                } if isinstance(rejected, list) else {}
                missing_rejections = sorted(set(feasible_ids) - set(rejected_by_id))
                invalid_rejections = sorted(
                    component_id for component_id in feasible_ids
                    if component_id in rejected_by_id and (
                        rejected_by_id[component_id].get("reason_code") not in {
                            "page_fit_incompatible", "component_contract_incomplete",
                            "visual_density_mismatch", "data_topology_mismatch",
                        }
                        or not isinstance(rejected_by_id[component_id].get("reason"), str)
                        or not rejected_by_id[component_id]["reason"].strip()
                    )
                )
                if missing_rejections or invalid_rejections:
                    issues.append({
                        "code": "FEASIBLE_TEMPLATE_COMPONENT_UNUSED",
                        "slide_id": slide_id,
                        "feasible_component_ids": feasible_ids,
                        "missing_rejections": missing_rejections,
                        "invalid_rejections": invalid_rejections,
                    })
                else:
                    justified_authored_pages += 1
            elif not set(selected) <= set(feasible_ids):
                issues.append({
                    "code": "SELECTED_COMPONENT_NOT_FEASIBLE",
                    "slide_id": slide_id,
                    "selected_component_ids": selected,
                    "feasible_component_ids": feasible_ids,
                })
            else:
                reused_pages += 1
        elif intent.get("mode") != "model_authored":
            issues.append({
                "code": "MODEL_AUTHORED_COMPONENT_REQUIRED",
                "slide_id": slide_id,
            })
        audits.append({
            "slide_id": slide_id,
            "requirement": requirement,
            "feasible_components": feasible,
            "declared_candidate_component_ids": declared_candidates,
            "selected_component_ids": selected,
            "mode": intent.get("mode"),
            "new_component_id": intent.get("new_component_id"),
            "style_reference_component_ids": style_references,
            "rejected_candidates": rejected,
        })
    return {
        "status": "pass" if not issues else "fail",
        "content_page_count": content_pages,
        "eligible_page_count": eligible_pages,
        "reused_eligible_page_count": reused_pages,
        "justified_model_authored_page_count": justified_authored_pages,
        "eligible_component_coverage": (
            round(reused_pages / eligible_pages, 4) if eligible_pages else 1.0
        ),
        "pages": audits,
        "issues": issues,
    }
