"""Template-neutral component adaptation contracts.

The contract is derived from the reviewed objects of the *current* uploaded
template.  It never relies on a component id, source page number, colour, or
brand-specific convention.  Reviewers may override conservative defaults, but
the geometry and referenced native shapes remain machine-verifiable.
"""

from __future__ import annotations

from copy import deepcopy


BACKGROUND_POLICIES = frozenset({
    "none", "retain_component", "reflow_to_content", "strip_on_reuse",
})
RESPONSIVE_MODES = frozenset({
    "scale_uniform", "stretch", "reflow_grid", "resize_text_container",
    "resize_chart_plot", "reflow_background",
})
SERIES_ROLES = frozenset({"independent", "comparison_anchor", "sequence", "appendix"})


def _union_frames(frames: list[dict]) -> dict | None:
    if not frames:
        return None
    left = min(frame["x"] for frame in frames)
    top = min(frame["y"] for frame in frames)
    right = max(frame["x"] + frame["w"] for frame in frames)
    bottom = max(frame["y"] + frame["h"] for frame in frames)
    return {
        "x": round(left, 6), "y": round(top, 6),
        "w": round(right - left, 6), "h": round(bottom - top, 6),
    }


def _area(frame: dict | None) -> float:
    return float(frame["w"] * frame["h"]) if frame else 0.0


def _background_role(role: object) -> bool:
    if not isinstance(role, str):
        return False
    normalized = role.lower().replace("-", "_").replace(" ", "_")
    return "background" in normalized or "backdrop" in normalized


def _content_role(role: object) -> bool:
    if not isinstance(role, str):
        return False
    normalized = role.lower().replace("-", "_").replace(" ", "_")
    if _background_role(normalized):
        return False
    return normalized not in {
        "decoration", "shadow", "connector", "attachment", "ornament",
    }


def _shape_names(groups: list[dict], predicate) -> list[str]:
    return [
        member["shape_name"]
        for group in groups if predicate(group.get("role"))
        for member in group.get("members", [])
        if isinstance(member.get("shape_name"), str)
    ]


def _frames(groups: list[dict], predicate) -> list[dict]:
    return [
        member["frame"]
        for group in groups if predicate(group.get("role"))
        for member in group.get("members", [])
        if isinstance(member.get("frame"), dict)
    ]


def _positive_number(value: object, *, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{context} must be a positive number")
    return float(value)


def build_adaptation_contract(
    declaration: dict,
    resolved_groups: list[dict],
) -> dict:
    """Derive and validate a portable component adaptation contract."""
    override = declaration.get("adaptation_contract", {})
    if not isinstance(override, dict):
        raise ValueError(
            f"component {declaration.get('component_id')!r} adaptation_contract must be an object"
        )

    content_bbox = _union_frames(_frames(resolved_groups, _content_role))
    all_bbox = _union_frames(_frames(resolved_groups, lambda _role: True))
    decoration_bbox = _union_frames(_frames(
        resolved_groups, lambda role: not _content_role(role),
    ))
    background_names = _shape_names(resolved_groups, _background_role)
    background_bbox = _union_frames(_frames(resolved_groups, _background_role))
    if content_bbox is None:
        content_bbox = all_bbox
    if content_bbox is None:
        # Composite recipes can consist entirely of child components.
        content_bbox = {"x": 0.0, "y": 0.0, "w": 1.0, "h": 1.0}

    source_aspect = content_bbox["w"] / max(content_bbox["h"], 1e-6)
    background_area_ratio = (
        _area(background_bbox) / max(_area(content_bbox), 1e-6)
        if background_bbox else 0.0
    )
    inferred_background_policy = "none"
    if background_names:
        inferred_background_policy = (
            "strip_on_reuse"
            if background_area_ratio > 1.35
            or background_bbox["w"] > 0.88
            or background_bbox["h"] > 0.78
            or (
                background_area_ratio > 1.15
                and background_bbox["w"] > 0.70
                and background_bbox["h"] > 0.65
            )
            else "reflow_to_content"
        )

    background = override.get("background", {})
    if not isinstance(background, dict):
        raise ValueError("adaptation background must be an object")
    background_policy = background.get("policy", inferred_background_policy)
    if background_policy not in BACKGROUND_POLICIES:
        raise ValueError(f"invalid adaptation background policy {background_policy!r}")

    renderer = declaration.get("renderer")
    group_roles = {group.get("role") for group in resolved_groups}
    default_modes = ["scale_uniform"]
    if renderer in {"card_grid", "icon_card_grid"}:
        default_modes.extend(["reflow_grid", "resize_text_container"])
    elif renderer in {"native_group", "two_sided_contrast"}:
        default_modes.append("resize_text_container")
    if "chart" in group_roles:
        default_modes.append("resize_chart_plot")
    if background_names:
        default_modes.append("reflow_background")

    responsive = override.get("responsive", {})
    if not isinstance(responsive, dict):
        raise ValueError("adaptation responsive must be an object")
    modes = responsive.get("modes", default_modes)
    if (
        not isinstance(modes, list) or not modes
        or any(mode not in RESPONSIVE_MODES for mode in modes)
    ):
        raise ValueError("adaptation responsive modes are invalid")
    aspect_range = responsive.get("supported_aspect_ratio", {})
    if not isinstance(aspect_range, dict):
        raise ValueError("supported_aspect_ratio must be an object")
    flexible = bool(set(modes) & {"stretch", "reflow_grid", "resize_chart_plot"})
    default_factor = 0.5 if flexible else 0.75
    minimum_aspect = _positive_number(
        aspect_range.get("minimum", source_aspect * default_factor),
        context="minimum supported aspect ratio",
    )
    maximum_aspect = _positive_number(
        aspect_range.get("maximum", source_aspect / default_factor),
        context="maximum supported aspect ratio",
    )
    if minimum_aspect > maximum_aspect:
        raise ValueError("minimum supported aspect ratio exceeds maximum")

    density_override = override.get("density", {})
    if not isinstance(density_override, dict):
        raise ValueError("adaptation density must be an object")
    guidance = declaration.get("page_guidance", {})
    minimum_units = density_override.get(
        "minimum_information_units", guidance.get("minimum_information_units", 1),
    )
    if isinstance(minimum_units, bool) or not isinstance(minimum_units, int) or minimum_units < 1:
        raise ValueError("adaptation minimum_information_units must be positive")
    minimum_label_chars = density_override.get("minimum_label_chars", 1)
    if (
        isinstance(minimum_label_chars, bool)
        or not isinstance(minimum_label_chars, int)
        or minimum_label_chars < 1
    ):
        raise ValueError("adaptation minimum_label_chars must be positive")
    minimum_numeric_annotations = density_override.get("minimum_numeric_annotations", 0)
    if (
        isinstance(minimum_numeric_annotations, bool)
        or not isinstance(minimum_numeric_annotations, int)
        or minimum_numeric_annotations < 0
    ):
        raise ValueError("adaptation minimum_numeric_annotations cannot be negative")

    preferred_aspects = override.get("preferred_aspect_ratios", [round(source_aspect, 4)])
    if (
        not isinstance(preferred_aspects, list) or not preferred_aspects
        or any(isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0
               for value in preferred_aspects)
    ):
        raise ValueError("preferred_aspect_ratios must contain positive numbers")
    series_role = override.get("series_role", "independent")
    if series_role not in SERIES_ROLES:
        raise ValueError(f"invalid adaptation series role {series_role!r}")

    return {
        "schema_version": "1.0.0",
        "content_bbox": deepcopy(content_bbox),
        "decoration_bbox": deepcopy(decoration_bbox),
        "background": {
            "policy": background_policy,
            "shape_names": background_names,
            "bbox": deepcopy(background_bbox),
            "area_ratio_to_content": round(background_area_ratio, 4),
            "rationale": background.get(
                "rationale",
                "derived from reviewed background-role geometry in the uploaded template",
            ),
        },
        "responsive": {
            "modes": list(dict.fromkeys(modes)),
            "source_aspect_ratio": round(source_aspect, 4),
            "supported_aspect_ratio": {
                "minimum": round(minimum_aspect, 4),
                "maximum": round(maximum_aspect, 4),
            },
        },
        "density": {
            "minimum_information_units": minimum_units,
            "minimum_label_chars": minimum_label_chars,
            "minimum_numeric_annotations": minimum_numeric_annotations,
        },
        "preferred_aspect_ratios": [round(float(value), 4) for value in preferred_aspects],
        "series_role": series_role,
    }


def evaluate_component_target_fit(component: dict, placement: dict) -> dict:
    """Check whether a reviewed component can adapt to a planned target box."""
    contract = component.get("adaptation_contract", {})
    responsive = contract.get("responsive", {}) if isinstance(contract, dict) else {}
    supported = responsive.get("supported_aspect_ratio", {})
    if not isinstance(placement, dict):
        return {"status": "fail", "code": "TEMPLATE_COMPONENT_PLACEMENT_REQUIRED"}
    width, height = placement.get("w"), placement.get("h")
    if (
        isinstance(width, bool) or not isinstance(width, (int, float)) or width <= 0
        or isinstance(height, bool) or not isinstance(height, (int, float)) or height <= 0
    ):
        return {"status": "fail", "code": "TEMPLATE_COMPONENT_PLACEMENT_INVALID"}
    target_aspect = float(width) / float(height)
    minimum, maximum = supported.get("minimum"), supported.get("maximum")
    if not isinstance(minimum, (int, float)) or not isinstance(maximum, (int, float)):
        return {"status": "fail", "code": "TEMPLATE_COMPONENT_ADAPTATION_MISSING"}
    if not float(minimum) <= target_aspect <= float(maximum):
        # A contain placement remains safe: it preserves the native geometry
        # and may leave deliberate whitespace.  Only a plan that explicitly
        # requires the component to fill the target is allowed to claim that
        # this is responsive; otherwise report the mismatch as evidence for
        # the page-composition layer without breaking legacy contain layouts.
        if placement.get("require_fill") is not True:
            return {
                "status": "pass",
                "fit_warning": "target_aspect_outside_responsive_range",
                "target_aspect_ratio": round(target_aspect, 4),
                "supported_aspect_ratio": {"minimum": minimum, "maximum": maximum},
                "responsive_modes": responsive.get("modes", []),
                "background_policy": contract.get("background", {}).get("policy", "none"),
            }
        return {
            "status": "fail",
            "code": "TEMPLATE_COMPONENT_TARGET_ASPECT_UNSUPPORTED",
            "target_aspect_ratio": round(target_aspect, 4),
            "supported_aspect_ratio": {"minimum": minimum, "maximum": maximum},
        }
    return {
        "status": "pass",
        "target_aspect_ratio": round(target_aspect, 4),
        "responsive_modes": responsive.get("modes", []),
        "background_policy": contract.get("background", {}).get("policy", "none"),
    }
