from __future__ import annotations

from typing import Any

from .base import BuilderSelection, SupportLevel

SUPPORT_ORDER = {"unsupported": 0, "unknown": 0, "visual_only": 1, "partial": 2, "full": 3}
NATIVE_ROUTES = {"native_ppt", "native_chart", "native_table", "native_diagram"}
VISUAL_ROUTES = {"svg_component", "raster_component", "generated_image", "background_image", "hybrid_overlay"}


def registry_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {component["component_type"]: component for component in registry.get("components", []) if isinstance(component, dict) and component.get("component_type")}


def infer_component_type(obj: dict[str, Any]) -> str:
    if obj.get("component_type"):
        explicit = str(obj["component_type"])
        aliases = {"card": "comparison_card", "process": "process_flow"}
        return aliases.get(explicit, explicit)
    plan = obj.get("visual_component_plan") if isinstance(obj.get("visual_component_plan"), dict) else {}
    if plan.get("component_type"):
        return str(plan["component_type"])
    obj_type = obj.get("type")
    role = str(obj.get("semantic_role", ""))
    if obj_type == "table":
        return "native_table"
    if obj_type == "chart":
        return "bar_chart"
    if obj_type == "diagram":
        return "process_flow"
    if obj_type == "image":
        return "conceptual_scene"
    if obj_type == "text" and "source" in role:
        return "source_note"
    if obj_type == "text" and "title" in role:
        return "judgment_title"
    if obj_type == "text":
        return "body_argument"
    return role or "body_argument"


def iter_objects(ppt_ir: dict[str, Any], delivery_plan: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if delivery_plan:
        objects: list[dict[str, Any]] = []
        for slide in delivery_plan.get("slides", []) or []:
            for obj in slide.get("objects", []) or []:
                if isinstance(obj, dict):
                    objects.append(
                        {
                            "component_type": obj.get("component_type"),
                            "selected_route": obj.get("selected_route"),
                            "editability": obj.get("editability"),
                        }
                    )
        if objects:
            return objects
    return [obj for slide in ppt_ir.get("slides", []) or [] for obj in (slide.get("objects", []) or []) if isinstance(obj, dict)]


def available_renderers(capabilities: dict[str, Any] | None) -> list[str]:
    if not capabilities:
        return []
    return [
        name
        for name, renderer in (capabilities.get("renderers", {}) or {}).items()
        if isinstance(renderer, dict) and renderer.get("available") is True
    ]


def builder_names(registry: dict[str, Any], capabilities: dict[str, Any] | None) -> list[str]:
    names: set[str] = set()
    if capabilities:
        names.update((capabilities.get("builders", {}) or {}).keys())
    for component in registry.get("components", []) or []:
        if isinstance(component, dict):
            names.update((component.get("builder_support", {}) or {}).keys())
    ordered = ["pptxgenjs", "officecli", "python_pptx", "html_svg", "custom"]
    return [name for name in ordered if name in names] + sorted(names - set(ordered))


def builder_available(builder: str, capabilities: dict[str, Any] | None, profile: str) -> bool:
    if not capabilities:
        return profile == "fast"
    data = (capabilities.get("builders", {}) or {}).get(builder)
    return isinstance(data, dict) and data.get("available") is True


def support_level(component: dict[str, Any] | None, builder: str, capabilities: dict[str, Any] | None) -> SupportLevel:
    if capabilities:
        cap = (capabilities.get("builders", {}) or {}).get(builder, {})
        if isinstance(cap, dict):
            components = cap.get("components", {}) if isinstance(cap.get("components"), dict) else {}
            component_type = component.get("component_type") if component else None
            if component_type in components:
                return components[component_type]
    if component:
        support = component.get("builder_support", {})
        if builder in support:
            return support[builder].get("level", "unknown")
    return "unknown"


def route_for_object(obj: dict[str, Any], component: dict[str, Any] | None) -> str:
    selected = obj.get("selected_route")
    if selected:
        return str(selected)
    preferred = (obj.get("delivery_preferences", {}) or {}).get("preferred_route") if isinstance(obj.get("delivery_preferences"), dict) else None
    return str(preferred or (component or {}).get("preferred_delivery_route") or "unsupported")


def route_support_ok(route: str, level: SupportLevel, editability: str | None, profile: str) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if profile == "premium" and level == "unknown":
        reasons.append("BUILDER_UNKNOWN_SUPPORT_REJECTED")
    if level in {"unsupported", "unknown"}:
        reasons.append("BUILDER_COMPONENT_UNSUPPORTED")
        reasons.append("BUILDER_ROUTE_UNSUPPORTED")
    if editability == "native_required":
        if route not in NATIVE_ROUTES:
            reasons.append("BUILDER_NATIVE_REQUIRED_UNSUPPORTED")
        if level not in {"full", "partial"} or (profile == "premium" and level != "full"):
            reasons.append("BUILDER_NATIVE_REQUIRED_UNSUPPORTED")
        if level == "visual_only":
            reasons.append("BUILDER_VISUAL_ONLY_FOR_NATIVE_REQUIRED")
    if route in NATIVE_ROUTES and level == "visual_only":
        reasons.append("BUILDER_VISUAL_ONLY_FOR_NATIVE_ROUTE")
    if route in VISUAL_ROUTES and editability == "native_required":
        reasons.append("BUILDER_VISUAL_ONLY_FOR_NATIVE_REQUIRED")
    return not reasons, reasons


def score_builder(
    builder: str,
    ppt_ir: dict[str, Any],
    registry: dict[str, Any],
    capabilities: dict[str, Any] | None,
    profile: str,
    delivery_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    reg = registry_map(registry)
    objects = iter_objects(ppt_ir, delivery_plan)
    total = max(len(objects), 1)
    native_hits = 0
    editable_hits = 0
    fallback_count = 0
    errors: list[str] = []
    reasons: list[str] = []
    for obj in objects:
        component = reg.get(infer_component_type(obj))
        route = route_for_object(obj, component)
        level = support_level(component, builder, capabilities)
        editability = obj.get("editability")
        ok, route_errors = route_support_ok(route, level, editability, profile)
        if not ok:
            errors.extend(route_errors)
        if route in NATIVE_ROUTES and level in {"full", "partial"}:
            native_hits += 1 if level == "full" else 0.5
        if level in {"full", "partial"}:
            editable_hits += 1 if level == "full" else 0.6
        elif level == "visual_only" and route in VISUAL_ROUTES and editability != "native_required":
            editable_hits += 0.25
        if level in {"partial", "visual_only"} or route not in NATIVE_ROUTES:
            fallback_count += 1
    renderer_score = 1.0 if available_renderers(capabilities) else (0.4 if profile == "fast" else 0.0)
    font_score = 1.0
    if capabilities:
        missing = ((capabilities.get("fonts", {}) or {}).get("required_missing") or [])
        fallback_map = ((capabilities.get("fonts", {}) or {}).get("fallback_map") or {})
        uncovered = [font for font in missing if font not in fallback_map]
        font_score = 0.2 if uncovered else (0.75 if missing else 1.0)
        if uncovered and profile == "premium":
            errors.append("CAPABILITY_REQUIRED_FONT_MISSING")
    profile_score = 1.0
    if profile == "premium" and not available_renderers(capabilities):
        reasons.append("CAPABILITY_RENDERER_NOT_FOUND")
        profile_score = 0.7
    normalized_fallback = fallback_count / total
    score = (
        0.35 * (native_hits / total)
        + 0.25 * (editable_hits / total)
        + 0.15 * renderer_score
        + 0.10 * font_score
        + 0.10 * profile_score
        - 0.05 * normalized_fallback
    )
    available = builder_available(builder, capabilities, profile)
    if not available:
        errors.append("CAPABILITY_BUILDER_NOT_FOUND")
    if builder == "python_pptx" and profile in {"standard", "premium"}:
        relationship_components = {
            "layered_architecture", "capability_landscape",
            "comparison_matrix", "timeline", "flywheel", "causal_chain",
            "stakeholder_network", "ecosystem_map",
        }
        has_complex_relationship = any(
            any(infer_component_type(obj) in relationship_components for obj in (slide.get("objects", []) or []) if isinstance(obj, dict))
            for slide in ppt_ir.get("slides", []) or []
            if isinstance(slide, dict)
        )
        if has_complex_relationship:
            errors.append("BUILDER_STANDARD_RELATIONSHIP_VISUAL_UNQUALIFIED")
    version = None
    if capabilities:
        cap = (capabilities.get("builders", {}) or {}).get(builder, {})
        version = cap.get("version") if isinstance(cap, dict) else None
    return {
        "builder": builder,
        "available": available,
        "version": version,
        "score": round(max(score, 0.0), 4),
        "native_component_coverage": round(native_hits / total, 4),
        "editable_core_coverage": round(editable_hits / total, 4),
        "fallback_count": fallback_count,
        "reasons": sorted(set(reasons)) or ["BUILDER_CANDIDATE_SCORED"],
        "errors": sorted(set(errors)),
    }


def select_builder(
    ppt_ir: dict[str, Any],
    delivery_plan: dict[str, Any] | None,
    component_registry: dict[str, Any],
    capability_report: dict[str, Any] | None,
    profile: str,
    requested_builder: str = "auto",
) -> BuilderSelection:
    warnings: list[str] = []
    errors: list[str] = []
    if capability_report is None and profile != "fast":
        return BuilderSelection(
            requested=requested_builder,
            selected="unknown",
            version=None,
            selection_score=0.0,
            selection_reasons=[],
            warnings=[],
            errors=["CAPABILITY_REPORT_REQUIRED"],
        )
    if capability_report is None:
        warnings.append("CAPABILITY_REPORT_MISSING_STATIC_DEFAULTS_USED")

    candidates = [
        score_builder(builder, ppt_ir, component_registry, capability_report, profile, delivery_plan)
        for builder in builder_names(component_registry, capability_report)
    ]
    if requested_builder != "auto":
        candidates = [candidate for candidate in candidates if candidate["builder"] == requested_builder]
        if not candidates:
            return BuilderSelection(
                requested=requested_builder,
                selected="unknown",
                version=None,
                selection_score=0.0,
                selection_reasons=[],
                warnings=warnings,
                errors=["CAPABILITY_BUILDER_NOT_FOUND"],
            )

    valid = [candidate for candidate in candidates if not candidate["errors"]]
    if requested_builder != "auto" and valid:
        selected = valid[0]
        reasons = ["BUILDER_USER_REQUEST_VALID"]
    elif valid:
        selected = sorted(valid, key=lambda item: (item["score"], -item["fallback_count"], item["native_component_coverage"]), reverse=True)[0]
        reasons = ["BUILDER_SELECTED_BY_SCORE", *selected["reasons"]]
    else:
        reasons = ["BUILDER_SELECTION_NO_VALID_CANDIDATE"]
        selected = {"builder": "unknown", "version": None, "score": 0.0, "errors": []}
        if requested_builder != "auto" and candidates:
            errors.extend(candidates[0]["errors"])
        errors.append("BUILDER_SELECTION_NO_VALID_CANDIDATE")

    return BuilderSelection(
        requested=requested_builder,
        selected=selected["builder"],
        version=selected.get("version"),
        selection_score=selected["score"],
        selection_reasons=sorted(set(reasons)),
        candidates=candidates,
        warnings=warnings,
        errors=sorted(set(errors)),
    )
