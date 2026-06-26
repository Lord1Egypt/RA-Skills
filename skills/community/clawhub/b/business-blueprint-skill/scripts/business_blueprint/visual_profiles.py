from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class VisualProfile:
    profile_id: str
    label: str
    description: str
    preferred_theme: str
    best_for: tuple[str, ...]
    palette: Mapping[str, Mapping[str, str]]


VISUAL_PROFILES: dict[str, VisualProfile] = {
    "executive-clean": VisualProfile(
        profile_id="executive-clean",
        label="Executive Clean",
        description="Low-noise boardroom style for strategy, capability, and finance blueprints.",
        preferred_theme="light",
        best_for=("finance", "common"),
        palette={
            "light": {
                "bg": "#F7F8F5",
                "canvas": "#FFFFFF",
                "border": "#D8DED2",
                "text_main": "#17211B",
                "text_sub": "#667064",
                "layer_header_bg": "#EEF2E6",
                "layer_border": "#D8DED2",
                "cap_fill": "#EEF7F3",
                "cap_stroke": "#1F6F68",
                "actor_fill": "#F7F1E7",
                "actor_stroke": "#9A6A2F",
                "flow_fill": "#F4F0FF",
                "flow_stroke": "#6D5BD0",
                "arrow": "#1F6F68",
                "arrow_label_bg": "#FFFFFF",
            },
            "dark": {
                "bg": "#111827",
                "canvas": "#182235",
                "border": "#2F3B4F",
                "text_main": "#F8FAFC",
                "text_sub": "#CBD5E1",
                "arrow": "#5EEAD4",
            },
        },
    ),
    "blueprint-technical": VisualProfile(
        profile_id="blueprint-technical",
        label="Blueprint Technical",
        description="Engineering blueprint style with cyan grid energy for architecture-heavy outputs.",
        preferred_theme="dark",
        best_for=("manufacturing", "common"),
        palette={
            "dark": {
                "bg": "#071827",
                "canvas": "#0B2239",
                "border": "#164E63",
                "text_main": "#E0F2FE",
                "text_sub": "#7DD3FC",
                "layer_header_bg": "#082F49",
                "layer_border": "#155E75",
                "cap_fill": "#083344",
                "cap_stroke": "#22D3EE",
                "sys_fill": "#0C2D48",
                "sys_stroke": "#38BDF8",
                "actor_fill": "#172554",
                "actor_stroke": "#60A5FA",
                "flow_fill": "#1E293B",
                "flow_stroke": "#FDE047",
                "arrow": "#38BDF8",
                "arrow_label_bg": "#082F49",
            },
            "light": {
                "bg": "#EFF6FF",
                "canvas": "#FFFFFF",
                "border": "#BAE6FD",
                "text_main": "#0C4A6E",
                "arrow": "#0284C7",
            },
        },
    ),
    "dark-ops": VisualProfile(
        profile_id="dark-ops",
        label="Dark Ops",
        description="High-contrast operations style for dense system and runtime maps.",
        preferred_theme="dark",
        best_for=("retail", "manufacturing", "common"),
        palette={
            "dark": {
                "bg": "#050A12",
                "canvas": "#0B1220",
                "border": "#243244",
                "text_main": "#E5F0FF",
                "text_sub": "#8EA3B8",
                "layer_header_bg": "#101827",
                "layer_border": "#243244",
                "cap_fill": "#092F2A",
                "cap_stroke": "#2DD4BF",
                "sys_fill": "#10233F",
                "sys_stroke": "#38BDF8",
                "actor_fill": "#3B1B05",
                "actor_stroke": "#F59E0B",
                "flow_fill": "#301A3D",
                "flow_stroke": "#C084FC",
                "arrow": "#2DD4BF",
                "arrow_label_bg": "#101827",
            },
            "light": {
                "bg": "#F8FAFC",
                "canvas": "#FFFFFF",
                "arrow": "#0F766E",
            },
        },
    ),
    "warm-consulting": VisualProfile(
        profile_id="warm-consulting",
        label="Warm Consulting",
        description="Warm advisory style for presales workshops and retail/operations storytelling.",
        preferred_theme="light",
        best_for=("retail", "cross-border-ecommerce"),
        palette={
            "light": {
                "bg": "#FBF4EA",
                "canvas": "#FFFDF7",
                "border": "#E7D5BE",
                "text_main": "#2D1B0E",
                "text_sub": "#7C6048",
                "layer_header_bg": "#F8E8D4",
                "layer_border": "#E7D5BE",
                "cap_fill": "#FFF7ED",
                "cap_stroke": "#C2410C",
                "sys_fill": "#FFF1E6",
                "sys_stroke": "#EA580C",
                "actor_fill": "#FEF3C7",
                "actor_stroke": "#D97706",
                "flow_fill": "#FDE68A",
                "flow_stroke": "#B45309",
                "arrow": "#C2410C",
                "arrow_label_bg": "#FFFDF7",
            },
            "dark": {
                "bg": "#1C120A",
                "canvas": "#2A1B10",
                "border": "#5B3B24",
                "text_main": "#FFF7ED",
                "text_sub": "#FDBA74",
                "arrow": "#FB923C",
            },
        },
    ),
    "knowledge-canvas": VisualProfile(
        profile_id="knowledge-canvas",
        label="Knowledge Canvas",
        description="Consulting canvas style for pain-strategy-metric knowledge graphs.",
        preferred_theme="light",
        best_for=("cross-border-ecommerce",),
        palette={
            "light": {
                "bg": "#FAFAF4",
                "canvas": "#FFFFFA",
                "border": "#DDD6C7",
                "text_main": "#1F2933",
                "text_sub": "#6B705C",
                "layer_header_bg": "#F1F3E8",
                "layer_border": "#DDD6C7",
                "cap_fill": "#F0FDF4",
                "cap_stroke": "#15803D",
                "sys_fill": "#EFF6FF",
                "sys_stroke": "#2563EB",
                "actor_fill": "#FEF3C7",
                "actor_stroke": "#B45309",
                "flow_fill": "#FCE7F3",
                "flow_stroke": "#BE185D",
                "arrow": "#15803D",
                "arrow_label_bg": "#FFFFFA",
            },
            "dark": {
                "bg": "#11140F",
                "canvas": "#182016",
                "border": "#33412D",
                "text_main": "#F7FEE7",
                "text_sub": "#C7D2A5",
                "arrow": "#A3E635",
            },
        },
    ),
}

VISUAL_PROFILE_IDS: tuple[str, ...] = tuple(VISUAL_PROFILES)


def resolve_visual_profile(
    visual_profile: str | None,
    *,
    industry: str | None = None,
    blueprint_type: str | None = None,
    theme: str = "dark",
) -> VisualProfile | None:
    if not visual_profile or visual_profile == "base":
        return None
    if visual_profile == "auto":
        return VISUAL_PROFILES[_auto_profile_id(industry=industry, blueprint_type=blueprint_type, theme=theme)]
    try:
        return VISUAL_PROFILES[visual_profile]
    except KeyError as exc:
        valid = ", ".join(("auto", "base", *VISUAL_PROFILE_IDS))
        raise ValueError(f"Unknown visual profile: {visual_profile}. Valid: {valid}") from exc


def apply_visual_profile(
    base_palette: Mapping[str, str],
    visual_profile: str | None,
    *,
    theme: str,
    industry: str | None = None,
    blueprint_type: str | None = None,
) -> dict[str, str]:
    result = dict(base_palette)
    profile = resolve_visual_profile(
        visual_profile,
        industry=industry,
        blueprint_type=blueprint_type,
        theme=theme,
    )
    if profile is None:
        return result
    result.update(profile.palette.get(theme, {}))
    result["profile_id"] = profile.profile_id
    result["profile_label"] = profile.label
    return result


def _auto_profile_id(*, industry: str | None, blueprint_type: str | None, theme: str) -> str:
    if blueprint_type == "domain-knowledge" or industry == "cross-border-ecommerce":
        return "knowledge-canvas"
    if industry == "manufacturing":
        return "blueprint-technical"
    if industry == "finance":
        return "executive-clean"
    if industry == "retail":
        return "warm-consulting"
    return "dark-ops" if theme == "dark" else "executive-clean"
