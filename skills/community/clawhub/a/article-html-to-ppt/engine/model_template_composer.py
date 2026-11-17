"""Compile a model-authored Template composition into strict component slots."""

from __future__ import annotations

from copy import deepcopy

from .component_atlas import select_component
from .component_intent import evaluate_component_intents
from .deck_diversity import evaluate_family_diversity
from .template_page_composition import evaluate_template_page_compositions


def build_model_template_composition(
    ir: dict,
    atlas: dict,
    model_plan: dict,
    *,
    enforce_intent_audit: bool = True,
    enforce_page_composition: bool | None = None,
) -> dict:
    """Honor explicit model composition while proving reviewed-component reuse."""
    if (
        not isinstance(model_plan, dict)
        or model_plan.get("schema_version") not in {"1.0.0", "1.1.0"}
    ):
        raise ValueError("model template plan schema_version must be 1.0.0 or 1.1.0")
    planned_slides = model_plan.get("slides")
    if not isinstance(planned_slides, list) or not planned_slides:
        raise ValueError("model template plan requires slides")
    if enforce_page_composition is None:
        enforce_page_composition = enforce_intent_audit
    template_slide_count = atlas.get("source", {}).get("slide_count")
    if not isinstance(template_slide_count, int) or template_slide_count < 1:
        raise ValueError("reviewed atlas requires source slide_count")
    intent_audit = evaluate_component_intents(
        ir, atlas, require_all_content_slides=enforce_intent_audit,
    )
    if enforce_intent_audit and intent_audit["status"] != "pass":
        codes = sorted({issue["code"] for issue in intent_audit["issues"]})
        raise ValueError(f"COMPONENT_INTENT_FAILED: {','.join(codes)}")
    page_composition = evaluate_template_page_compositions(ir, atlas, model_plan)
    if enforce_page_composition and page_composition["status"] != "pass":
        codes = sorted({issue["code"] for issue in page_composition["issues"]})
        raise ValueError(f"TEMPLATE_PAGE_COMPOSITION_FAILED: {','.join(codes)}")

    ir_by_id = {
        slide.get("id"): slide
        for slide in ir.get("slides", [])
        if isinstance(slide, dict) and isinstance(slide.get("id"), str)
    }
    pages: list[dict] = []
    planned_ids: set[str] = set()
    for page_index, page in enumerate(planned_slides, 1):
        if not isinstance(page, dict):
            raise ValueError(f"model template page {page_index} must be an object")
        slide_id = page.get("slide_id")
        if not isinstance(slide_id, str) or slide_id not in ir_by_id:
            raise ValueError(f"model template page {page_index} references unknown slide")
        if slide_id in planned_ids:
            raise ValueError(f"model template slide {slide_id!r} is planned twice")
        planned_ids.add(slide_id)
        slide = ir_by_id[slide_id]
        intent = slide.get("component_intent", {})
        components = page.get("components")
        if not isinstance(components, list) or not components:
            raise ValueError(f"model template slide {slide_id!r} requires components")
        selected_ids: list[str] = []
        resolved_components: list[dict] = []
        for component_index, component in enumerate(components, 1):
            if not isinstance(component, dict):
                raise ValueError(
                    f"model template slide {slide_id!r} component {component_index} is invalid"
                )
            component_id = component.get("component_id")
            if not isinstance(component_id, str) or not component_id:
                raise ValueError("model template components require component_id")
            is_model_authored = (
                component.get("model_authored") is True
                or (
                    isinstance(component.get("author_script"), str)
                    and component_id == intent.get("new_component_id")
                )
            )
            if is_model_authored:
                if intent.get("mode") == "model_authored" and len(components) != 1:
                    raise ValueError(
                        f"MODEL_AUTHORED_COMPONENT_COUNT_INVALID: slide={slide_id}"
                    )
                if component_id != intent.get("new_component_id"):
                    raise ValueError(
                        f"MODEL_AUTHORED_COMPONENT_ID_MISMATCH: slide={slide_id}"
                    )
                author_script = component.get("author_script")
                if not isinstance(author_script, str) or not author_script:
                    raise ValueError(
                        f"MODEL_AUTHORED_COMPONENT_SCRIPT_REQUIRED: slide={slide_id}"
                    )
                placement = component.get("placement")
                if not isinstance(placement, dict):
                    raise ValueError(
                        f"MODEL_AUTHORED_COMPONENT_PLACEMENT_REQUIRED: slide={slide_id}"
                    )
                required_binding_names = component.get("required_binding_names", [])
                if not isinstance(required_binding_names, list) or any(
                    not isinstance(name, str) or not name
                    for name in required_binding_names
                ):
                    raise ValueError(
                        f"MODEL_AUTHORED_COMPONENT_BINDINGS_INVALID: slide={slide_id}"
                    )
                asset_bindings = component.get("asset_bindings", [])
                if not isinstance(asset_bindings, list) or any(
                    not isinstance(asset, dict) for asset in asset_bindings
                ):
                    raise ValueError(
                        f"MODEL_AUTHORED_COMPONENT_ASSETS_INVALID: slide={slide_id}"
                    )
                author_context = component.get("author_context", {})
                if not isinstance(author_context, dict):
                    raise ValueError(
                        f"MODEL_AUTHORED_COMPONENT_CONTEXT_INVALID: slide={slide_id}"
                    )
                resolved_components.append({
                    "component_id": component_id,
                    "model_authored": True,
                    "author_script": author_script,
                    "slide_id": slide_id,
                    "required_binding_names": deepcopy(required_binding_names),
                    "asset_bindings": deepcopy(asset_bindings),
                    "author_context": deepcopy(author_context),
                    "placement": deepcopy(placement),
                })
                continue
            if intent.get("mode") == "model_authored":
                raise ValueError(
                    f"MODEL_AUTHORED_COMPONENT_SCRIPT_REQUIRED: slide={slide_id}"
                )
            payload = component.get("payload")
            if not isinstance(payload, dict):
                raise ValueError(f"component {component_id!r} requires payload")
            element_count = payload.get("element_count")
            if element_count is None and isinstance(payload.get("elements"), list):
                element_count = len(payload["elements"])
            requirement = {
                "component_id": component_id,
                "semantic_use": payload.get("semantic_use", intent.get("semantic_use")),
                "element_count": element_count,
                "topology": payload.get("topology", intent.get("topology")),
                "required_slots": payload.get("required_slots", intent.get("required_slots", [])),
            }
            for field in (
                "family", "archetype", "composition_role",
                "text_requirements", "data_shape",
            ):
                value = payload.get(field, intent.get(field))
                if value is not None:
                    requirement[field] = value
            selection = select_component(atlas, requirement)
            if selection.get("status") != "selected":
                raise ValueError(
                    f"MODEL_TEMPLATE_COMPONENT_INFEASIBLE: slide={slide_id} "
                    f"component={component_id}: {selection.get('reason')}"
                )
            selected_ids.append(component_id)
            resolved = deepcopy(payload)
            resolved["component_id"] = component_id
            resolved["placement"] = deepcopy(component.get("placement"))
            resolved_components.append(resolved)
        declared_selected = intent.get("selected_component_ids", [])
        if set(selected_ids) != set(declared_selected):
            raise ValueError(
                f"MODEL_TEMPLATE_SELECTION_MISMATCH: slide={slide_id} "
                f"declared={declared_selected} planned={selected_ids}"
            )
        output_page_index = page.get("output_page_index", page_index)
        if not isinstance(output_page_index, int) or output_page_index < 1:
            raise ValueError("output_page_index must be positive")
        pages.append({
            "output_page_index": output_page_index,
            "purpose": slide_id,
            "destination_slide_index": template_slide_count + output_page_index,
            "components": resolved_components,
            "page_composition": deepcopy(page.get("page_composition")),
        })
    content_ids = {
        slide_id for slide_id, slide in ir_by_id.items()
        if slide.get("slide_role", "content") not in {"cover", "section", "closing"}
    }
    missing = sorted(content_ids - planned_ids)
    if missing:
        raise ValueError(f"MODEL_TEMPLATE_PAGES_MISSING: {missing}")
    atlas_by_id = {
        component.get("component_id"): component
        for component in atlas.get("components", [])
        if isinstance(component, dict)
    }
    family_diversity = evaluate_family_diversity([
        {
            "families": [
                (
                    f"model_authored:{component.get('component_id')}"
                    if component.get("model_authored") is True
                    else atlas_by_id.get(component.get("component_id"), {}).get("family")
                )
                for component in page.get("components", [])
            ],
            "archetype": (
                "body"
                if ir_by_id.get(page.get("purpose"), {}).get("slide_role", "content") == "content"
                else ir_by_id.get(page.get("purpose"), {}).get("slide_role", "body")
            ),
        }
        for page in pages
    ])
    if enforce_intent_audit and family_diversity["status"] != "pass":
        codes = sorted({issue["code"] for issue in family_diversity["issues"]})
        raise ValueError(f"COMPONENT_DIVERSITY_FAILED: {','.join(codes)}")
    return {
        "schema_version": "1.0.0",
        "source_page_count": len(pages),
        "template_slide_count": template_slide_count,
        "pages": sorted(pages, key=lambda page: page["output_page_index"]),
        "unsupported_pages": [],
        "component_intent": intent_audit,
        "page_composition": page_composition,
        "family_diversity": family_diversity,
        "coverage": {
            "status": "complete",
            "total_pages": len(content_ids),
            "planned_pages": len(content_ids),
            "unsupported_pages": 0,
            "coverage_ratio": 1.0,
        },
    }
