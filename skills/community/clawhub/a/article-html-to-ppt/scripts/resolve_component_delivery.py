#!/usr/bin/env python3
"""Resolve PPT IR objects to delivery routes using Component Registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from builders.selector import select_builder as select_report_builder
from diagram_ir_tools import analyze_diagram

ORDINARY_COMPONENTS = {
    "judgment_title",
    "section_title",
    "body_argument",
    "evidence_block",
    "quote_block",
    "source_note",
    "metric_card",
    "comparison_card",
    "risk_card",
    "capability_card",
    "summary_action_card",
    "native_table",
    "comparison_matrix",
    "decision_matrix",
    "feature_matrix",
    "risk_matrix",
    "bar_chart",
    "line_chart",
    "pie_chart",
    "kpi_dashboard",
}
NATIVE_ROUTES = {"native_ppt", "native_chart", "native_table", "native_diagram"}
ROUTE_REQUIRED_LEVEL = {
    "native_ppt": {"full"},
    "native_chart": {"full"},
    "native_table": {"full"},
    "native_diagram": {"full", "partial"},
    "hybrid_overlay": {"full", "partial", "visual_only"},
    "svg_component": {"full", "partial", "visual_only"},
    "raster_component": {"full", "partial", "visual_only"},
    "generated_image": {"full", "partial", "visual_only"},
    "background_image": {"full", "partial", "visual_only"},
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def registry_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {component["component_type"]: component for component in registry.get("components", [])}


def infer_component_type(obj: dict[str, Any]) -> str:
    if obj.get("component_type"):
        explicit = str(obj["component_type"])
        aliases = {"card": "comparison_card", "process": "process_flow"}
        return aliases.get(explicit, explicit)
    plan = obj.get("visual_component_plan") if isinstance(obj.get("visual_component_plan"), dict) else {}
    if plan.get("component_type"):
        return plan["component_type"]
    obj_type = obj.get("type")
    role = obj.get("semantic_role", "")
    if obj_type == "table":
        return "native_table"
    if obj_type == "chart":
        return "bar_chart"
    if obj_type == "diagram":
        return plan.get("diagram", {}).get("component_type", "process_flow") if isinstance(plan.get("diagram"), dict) else "process_flow"
    if obj_type == "image":
        return "conceptual_scene"
    if obj_type == "text" and "source" in role:
        return "source_note"
    if obj_type == "text" and "title" in role:
        return "judgment_title"
    if obj_type == "text":
        return "body_argument"
    return role or "body_argument"


def builder_level(component: dict[str, Any], builder: str, capabilities: dict[str, Any] | None) -> str:
    if capabilities:
        cap = (capabilities.get("builders", {}) or {}).get(builder, {})
        if not isinstance(cap, dict) or cap.get("available") is not True:
            return "unsupported"
        component_levels = cap.get("components", {}) if isinstance(cap, dict) else {}
        probe_level = component_levels.get(component.get("component_type"))
        # Trust the probe if it returns a positive result; fall back to registry for "unsupported"/missing
        if probe_level and probe_level != "unsupported":
            return probe_level
    # Registry fallback: use builder_support declared in the component registry
    support = component.get("builder_support", {})
    if builder in support:
        return support[builder].get("level", "unknown")
    return "unknown"


def select_builder(component: dict[str, Any], requested: str, capabilities: dict[str, Any] | None) -> str:
    if requested and requested != "auto":
        return requested
    preferred = ["pptxgenjs", "officecli", "python_pptx", "html_svg"]
    for builder in preferred:
        if builder_level(component, builder, capabilities) in {"full", "partial", "visual_only"}:
            return builder
    return "unknown"


def complexity_exceeds(obj: dict[str, Any], component: dict[str, Any]) -> bool:
    complexity = obj.get("complexity", {}) if isinstance(obj.get("complexity"), dict) else {}
    limits = (component.get("complexity_limits", {}) or {}).get("native", {})
    mapping = {
        "node_count": "max_nodes",
        "edge_count": "max_edges",
        "series_count": "max_series",
        "category_count": "max_categories",
        "row_count": "max_rows",
        "column_count": "max_columns",
    }
    for actual_key, limit_key in mapping.items():
        if actual_key in complexity and limit_key in limits and complexity[actual_key] > limits[limit_key]:
            return True
    return False


def load_diagram_for_object(obj: dict[str, Any], ppt_ir_base: Path) -> dict[str, Any] | None:
    if isinstance(obj.get("diagram_ir"), dict):
        return obj["diagram_ir"]
    ref = obj.get("diagram_ir_ref") or obj.get("diagram_ref")
    if not ref:
        return None
    path = Path(ref)
    if not path.is_absolute():
        path = ppt_ir_base / path
    if not path.exists():
        return None
    return load_json(path)


def route_allowed_by_builder(route: str, level: str) -> bool:
    if route == "unsupported":
        return False
    allowed = ROUTE_REQUIRED_LEVEL.get(route, {"full", "partial", "visual_only"})
    if route in NATIVE_ROUTES and level == "partial":
        return True
    return level in allowed


def route_allowed_by_policy(route: str, obj: dict[str, Any], component: dict[str, Any], profile: str) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    component_type = component.get("component_type")
    raster_policy = component.get("raster_policy", {})
    editability = obj.get("editability")
    if route in {"raster_component", "generated_image", "background_image"}:
        if component_type in ORDINARY_COMPONENTS:
            reasons.append("DELIVERY_ORDINARY_COMPONENT_RASTERIZED")
        if not raster_policy.get("allowed"):
            reasons.append("DELIVERY_RASTER_FORBIDDEN")
        if obj.get("whole_slide_raster") and raster_policy.get("whole_slide_forbidden", True):
            reasons.append("DELIVERY_WHOLE_SLIDE_RASTER_FORBIDDEN")
    if route in {"svg_component", "raster_component", "generated_image", "background_image", "hybrid_overlay"} and editability == "native_required":
        reasons.append("DELIVERY_NATIVE_REQUIRED_UNAVAILABLE")
    if profile == "premium":
        if route == "raster_component":
            reasons.append("DELIVERY_PROFILE_RESTRICTION")
        if obj.get("whole_slide_raster"):
            reasons.append("DELIVERY_WHOLE_SLIDE_RASTER_FORBIDDEN")
    return (not reasons, reasons)


def route_allowed_by_support(route: str, level: str, obj: dict[str, Any], profile: str) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if level == "unknown" and profile == "premium":
        reasons.append("BUILDER_UNKNOWN_SUPPORT_REJECTED")
    if obj.get("editability") == "native_required":
        if route not in NATIVE_ROUTES:
            reasons.append("BUILDER_NATIVE_REQUIRED_UNSUPPORTED")
        if level not in {"full", "partial"} or (profile == "premium" and level != "full"):
            reasons.append("BUILDER_NATIVE_REQUIRED_UNSUPPORTED")
        if level == "visual_only":
            reasons.append("BUILDER_VISUAL_ONLY_FOR_NATIVE_REQUIRED")
    if route in NATIVE_ROUTES and level == "visual_only":
        reasons.append("BUILDER_VISUAL_ONLY_FOR_NATIVE_ROUTE")
    return (not reasons, reasons)


def object_plan(slide: dict[str, Any], obj: dict[str, Any], registry: dict[str, dict[str, Any]], capabilities: dict[str, Any] | None, profile: str, requested_builder: str, ppt_ir_base: Path | None = None) -> tuple[dict[str, Any], str]:
    component_type = infer_component_type(obj)
    component = registry.get(component_type)
    slide_id = slide.get("id", "unknown-slide")
    object_id = obj.get("id", "unknown-object")
    diagram_analysis = None
    if obj.get("type") == "diagram":
        diagram = load_diagram_for_object(obj, ppt_ir_base or Path("."))
        if diagram:
            diagram_analysis = analyze_diagram(diagram)
            obj = dict(obj)
            obj.setdefault("complexity", {})
            obj["complexity"] = {
                **obj["complexity"],
                "node_count": diagram_analysis["node_count"],
                "edge_count": diagram_analysis["edge_count"],
            }
    if component is None:
        return {
            "slide_id": slide_id,
            "object_id": object_id,
            "component_type": component_type,
            "preferred_route": "unsupported",
            "selected_route": "unsupported",
            "decision": "unsupported",
            "reason_codes": ["DELIVERY_COMPONENT_NOT_REGISTERED"],
            "editable_core": [],
            "rasterized_parts": [],
            "svg_parts": [],
            "native_overlay_parts": [],
            "qa_checks": [],
            "fallback_chain": [],
        }, "unknown"

    builder = select_builder(component, requested_builder, capabilities)
    level = builder_level(component, builder, capabilities)
    preferred = (obj.get("delivery_preferences", {}) or {}).get("preferred_route") or component.get("preferred_delivery_route")
    allowed_fallbacks = (obj.get("delivery_preferences", {}) or {}).get("allowed_fallbacks")
    fallback_chain = allowed_fallbacks if isinstance(allowed_fallbacks, list) else component.get("fallback_chain", [])
    candidate_routes = [preferred] + [route for route in fallback_chain if route != preferred]
    reason_codes: list[str] = []
    if level in {"unsupported", "unknown"}:
        reason_codes.append("DELIVERY_BUILDER_UNSUPPORTED" if level == "unsupported" else "DELIVERY_BUILDER_UNAVAILABLE")
    if level == "partial":
        reason_codes.append("DELIVERY_BUILDER_PARTIAL_SUPPORT")
    if complexity_exceeds(obj, component):
        reason_codes.append("DELIVERY_COMPLEXITY_EXCEEDS_NATIVE_LIMIT")

    selected = "unsupported"
    decision = "unsupported"
    route_reasons = list(reason_codes)
    for idx, route in enumerate(candidate_routes):
        policy_ok, policy_reasons = route_allowed_by_policy(route, obj, component, profile)
        support_ok, support_reasons = route_allowed_by_support(route, level, obj, profile)
        route_reasons = list(dict.fromkeys(reason_codes + policy_reasons + support_reasons))
        if route in NATIVE_ROUTES and complexity_exceeds(obj, component):
            continue
        if not policy_ok or not support_ok:
            continue
        if route_allowed_by_builder(route, level):
            selected = route
            decision = "selected" if idx == 0 and not route_reasons else "fallback"
            if idx > 0 or route_reasons:
                route_reasons.append("DELIVERY_FALLBACK_SELECTED")
            break
    if selected == "unsupported":
        route_reasons.append("DELIVERY_NO_VALID_ROUTE")

    editable_core = component.get("editable_core", [])
    native_overlay = editable_core if selected in {"hybrid_overlay", "generated_image", "background_image"} else []
    plan = {
        "slide_id": slide_id,
        "object_id": object_id,
        "component_type": component_type,
        "preferred_route": preferred if preferred else "unsupported",
        "selected_route": selected,
        "decision": decision,
        "reason_codes": list(dict.fromkeys(route_reasons)),
        "editable_core": editable_core,
        "rasterized_parts": [object_id] if selected in {"raster_component", "generated_image", "background_image"} else [],
        "svg_parts": [object_id] if selected == "svg_component" else [],
        "native_overlay_parts": native_overlay,
        "qa_checks": component.get("required_qa_checks", []),
        "fallback_chain": fallback_chain,
    }
    if diagram_analysis:
        plan["diagram_analysis"] = {
            "node_count": diagram_analysis["node_count"],
            "edge_count": diagram_analysis["edge_count"],
            "group_count": diagram_analysis["group_count"],
            "boundary_count": diagram_analysis["boundary_count"],
            "connector_web_risk": diagram_analysis["connector_web_risk"],
            "layout_recommendation": diagram_analysis["recommended_layout"],
            "recommended_delivery_route": diagram_analysis["recommended_delivery_route"],
            "split_recommended": diagram_analysis["split_recommended"],
        }
    return plan, builder


def resolve(ppt_ir: dict[str, Any], style_ref: str, registry_ref: str, registry: dict[str, Any], capabilities: dict[str, Any] | None, profile: str, requested_builder: str, ppt_ir_ref: str, capability_ref: str | None) -> dict[str, Any]:
    reg = registry_map(registry)
    slides_out: list[dict[str, Any]] = []
    risk_codes: list[str] = []
    selected_builders: list[str] = []
    total = fallback_count = unsupported_count = 0
    ppt_ir_base = Path(ppt_ir_ref).parent
    selection = select_report_builder(
        ppt_ir=ppt_ir,
        delivery_plan=None,
        component_registry=registry,
        capability_report=capabilities,
        profile=profile,
        requested_builder=requested_builder,
    )
    if selection.selected == "unknown" and requested_builder != "auto":
        # User explicitly requested a builder; trust it over the auto-selector
        effective_builder = requested_builder
        # Clear auto-selector errors since user override is in effect
        selection.errors.clear()
    else:
        effective_builder = selection.selected
    if selection.errors and effective_builder == "unknown":
        risk_codes.extend(selection.errors)
    for slide in ppt_ir.get("slides", []):
        objects = slide.get("objects", []) or []
        object_plans = []
        for obj in objects:
            plan, builder = object_plan(slide, obj, reg, capabilities, profile, effective_builder, ppt_ir_base)
            selected_builders.append(builder)
            total += 1
            if plan["decision"] == "fallback":
                fallback_count += 1
            if plan["decision"] == "unsupported":
                unsupported_count += 1
            risk_codes.extend(plan["reason_codes"])
            object_plans.append(plan)
        slides_out.append({"slide_id": slide.get("id", "unknown-slide"), "objects": object_plans})
    selected_builder = effective_builder
    return {
        "schema_version": "1.0",
        "ppt_ir_ref": ppt_ir_ref,
        "style_contract_ref": style_ref,
        "component_registry_ref": registry_ref,
        "capability_report_ref": capability_ref,
        "profile": profile,
        "builder": {
            **selection.to_dict(),
            "selected": selected_builder,
        },
        "slides": slides_out,
        "summary": {
            "total_objects": total,
            "fallback_count": fallback_count,
            "unsupported_count": unsupported_count,
            "risk_codes": sorted(set(risk_codes)),
        },
    }


def explain(plan: dict[str, Any]) -> str:
    lines: list[str] = []
    for slide in plan.get("slides", []):
        for obj in slide.get("objects", []):
            lines.append(f"{obj['slide_id']} / {obj['object_id']} / {obj['component_type']}")
            lines.append(f"Preferred route: {obj['preferred_route']}")
            lines.append(f"Selected route: {obj['selected_route']}")
            if obj["reason_codes"]:
                lines.append("Reasons:")
                lines.extend(f"- {code}" for code in obj["reason_codes"])
            lines.append("")
    return "\n".join(lines).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve component delivery routes.")
    parser.add_argument("--ppt-ir", type=Path, required=True)
    parser.add_argument("--style", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--capabilities", type=Path)
    parser.add_argument("--profile", choices=["fast", "standard", "premium"], default="standard")
    parser.add_argument("--builder", default="auto")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--explain", action="store_true")
    parser.add_argument("--json-output", action="store_true")
    args = parser.parse_args()

    ppt_ir = load_json(args.ppt_ir)
    registry = load_json(args.registry)
    capabilities = load_json(args.capabilities) if args.capabilities and args.capabilities.exists() else None
    plan = resolve(
        ppt_ir=ppt_ir,
        style_ref=str(args.style),
        registry_ref=str(args.registry),
        registry=registry,
        capabilities=capabilities,
        profile=args.profile,
        requested_builder=args.builder,
        ppt_ir_ref=str(args.ppt_ir),
        capability_ref=str(args.capabilities) if args.capabilities else None,
    )
    write_json(args.output, plan)
    if args.explain:
        print(explain(plan))
    elif args.json_output:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"delivery plan written: {args.output}")
    strict_errors = [str(item) for item in plan.get("builder", {}).get("errors", [])]
    if plan.get("builder", {}).get("selected") == "unknown" and not strict_errors:
        strict_errors.append("BUILDER_SELECTION_UNKNOWN")
    if plan["summary"]["unsupported_count"]:
        strict_errors.append("DELIVERY_PLAN_UNSUPPORTED")
    if args.strict and strict_errors:
        print(", ".join(sorted(set(strict_errors))), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
