"""Independent Bespoke authoring-plan assembly.

This route does not compile a Standard deck and does not choose layouts.
It packages locked content, page-budget decisions, optional uploaded-template
evidence and delivery gates for a high-capability narrative/visual author.
"""
from __future__ import annotations

import hashlib
import json

from .production_request import resolve_page_budget, validate_production_request


def _canonical_sha256(payload: dict) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _required_bindings(slide: dict) -> list[str]:
    slide_id = slide["id"]
    bindings = [f"slide:{slide_id}:title"]
    if slide.get("message"):
        bindings.append(f"slide:{slide_id}:message")
    if isinstance(slide.get("chart"), dict):
        bindings.append(f"chart:{slide_id}")
    for block in slide.get("blocks", []):
        block_id = block.get("id")
        if not block_id:
            continue
        if block.get("role") == "table":
            bindings.append(f"table:{slide_id}:{block_id}")
        for field in ("text", "label", "value", "detail"):
            if block.get(field) not in (None, ""):
                bindings.append(f"block:{slide_id}:{block_id}:{field}")
        for index, item in enumerate(block.get("items", []) or []):
            if item.get("text"):
                bindings.append(f"block:{slide_id}:{block_id}:item:{index}")
            if item.get("detail"):
                bindings.append(f"block:{slide_id}:{block_id}:detail:{index}")
    return bindings


def build_authoring_manifest(request: dict, ir: dict, content_assessment: dict,
                             template_context: dict | None = None,
                             narrative_contract: dict | None = None) -> dict:
    """Build a source-locked, layout-unconstrained Bespoke authoring manifest."""
    findings = validate_production_request(request)
    if findings:
        return {"status": "rejected", "code": "PRODUCTION_REQUEST_INVALID", "findings": findings}
    if request["route"] != "bespoke":
        return {"status": "rejected", "code": "BESPOKE_ROUTE_REQUIRED"}
    if request.get("delivery_scope") == "complete_deck" and narrative_contract is None:
        return {"status": "rejected", "code": "NARRATIVE_CONTRACT_REQUIRED"}
    if narrative_contract is not None:
        from .narrative_contract import validate_narrative_contract

        narrative_findings = validate_narrative_contract(narrative_contract, ir)
        if narrative_findings:
            return {
                "status": "rejected",
                "code": "NARRATIVE_CONTRACT_INVALID",
                "findings": narrative_findings,
            }

    page_budget = resolve_page_budget(request["page_contract"], content_assessment)
    if page_budget["status"] == "conflict":
        return {
            "status": "page_contract_conflict", "route": "bespoke",
            "page_budget": page_budget,
        }

    slides = ir.get("slides", [])
    planned_pages = page_budget["planned_pages"]
    if len(slides) != planned_pages:
        return {
            "status": "rejected", "code": "STORYBOARD_PAGE_COUNT_MISMATCH",
            "planned_pages": planned_pages, "ir_slide_count": len(slides),
            "page_budget": page_budget,
        }

    if request.get("template"):
        if template_context is None:
            return {"status": "rejected", "code": "TEMPLATE_CONTEXT_REQUIRED"}
        if template_context.get("status") != "ready_for_visual_interpretation":
            return {
                "status": "rejected", "code": "TEMPLATE_CONTEXT_REJECTED",
                "template_context": template_context,
            }

    pages = [
        {
            "slide_id": slide["id"],
            "required_bindings": _required_bindings(slide),
            "layout_freedom": "unrestricted_within_delivery_gates",
        }
        for slide in slides
    ]
    manifest = {
        "schema_version": "1.0.0",
        "status": "ready_for_authoring",
        "request_id": request["request_id"],
        "route": "bespoke",
        "delivery_scope": request.get("delivery_scope", "chapter"),
        "source_ir_sha256": _canonical_sha256(ir),
        "page_budget": page_budget,
        "ownership": {
            "narrative": "high_capability_model",
            "visual_design": "high_capability_model",
            "geometry": "high_capability_model",
            "verification": "ppt_smith_engine",
        },
        "requires_standard_base_deck": False,
        "pages": pages,
        "delivery_gates": {
            "source_binding": "required",
            "native_editability": "required",
            "real_render": "required",
            "visual_review": "required",
            "max_refinement_rounds": 2,
        },
    }
    if narrative_contract is not None:
        manifest["narrative_contract"] = {
            **narrative_contract,
            "sha256": _canonical_sha256(narrative_contract),
        }
    if template_context is not None:
        manifest["template"] = {
            "use_mode": template_context["use_mode"],
            "source": template_context["source"],
            "preferred_slide_indices": template_context["preferred_slide_indices"],
            "generation_policy": template_context["generation_policy"],
            "review": template_context["review"],
            "evidence": template_context["evidence"],
        }
    return manifest
