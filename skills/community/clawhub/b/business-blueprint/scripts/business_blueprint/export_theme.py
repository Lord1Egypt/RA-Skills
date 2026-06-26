from __future__ import annotations


# Light theme (default) — warm, professional, matches DESIGN.md
C_LIGHT = {
    "bg": "#F8FAFC",
    "canvas": "#FFFFFF",
    "border": "#CBD5E1",
    "text_main": "#0F172A",
    "text_sub": "#64748B",
    "layer_header_bg": "#F1F5F9",
    "layer_border": "#E2E8F0",
    "cap_fill": "#E8F5F5",
    "cap_stroke": "#0B6E6E",
    "sys_fill": "#EFF6FF",
    "sys_stroke": "#3B82F6",
    "actor_fill": "#FFF7ED",
    "actor_stroke": "#F97316",
    "flow_fill": "#FEFCE8",
    "flow_stroke": "#CA8A04",
    "arrow": "#0B6E6E",
    "arrow_muted": "#94A3B8",
    "arrow_label": "#475569",
    "arrow_label_bg": "#FFFFFF",
}

# Dark theme — deep slate with vibrant accent colors
C_DARK = {
    "bg": "#020617",
    "canvas": "#0F172A",
    "border": "#1E293B",
    "text_main": "#E2E8F0",
    "text_sub": "#94A3B8",
    "layer_header_bg": "#0F172A",
    "layer_border": "#1E293B",
    "cap_fill": "#064E3B",
    "cap_stroke": "#34D399",
    "sys_fill": "#1E3A5F",
    "sys_stroke": "#60A5FA",
    "actor_fill": "#451A03",
    "actor_stroke": "#FB923C",
    "flow_fill": "#422006",
    "flow_stroke": "#FBBF24",
    "arrow": "#34D399",
    "arrow_muted": "#6B7280",
    "arrow_label": "#CBD5E1",
    "arrow_label_bg": "#1E293B",
}

INDUSTRY_THEMES: dict[str, dict[str, str]] = {
    "retail": {
        "accent": "#F97316",
    },
    "finance": {
        "accent": "#3B82F6",
    },
    "manufacturing": {
        "accent": "#6B7280",
    },
}

SYSTEM_CATEGORY_COLORS: dict[str, dict[str, dict[str, str]]] = {
    "frontend": {
        "light": {"fill": "#ECFEFF", "stroke": "#0891B2"},
        "dark": {"fill": "#0E2A3D", "stroke": "#22D3EE"},
    },
    "backend": {
        "light": {"fill": "#ECFDF5", "stroke": "#10B981"},
        "dark": {"fill": "#0E2E1F", "stroke": "#34D399"},
    },
    "database": {
        "light": {"fill": "#F5F3FF", "stroke": "#8B5CF6"},
        "dark": {"fill": "#1E1535", "stroke": "#A78BFA"},
    },
    "message_bus": {
        "light": {"fill": "#F0FDF4", "stroke": "#22C55E"},
        "dark": {"fill": "#0F2518", "stroke": "#4ADE80"},
    },
    "cloud": {
        "light": {"fill": "#FFFBEB", "stroke": "#F59E0B"},
        "dark": {"fill": "#2A2010", "stroke": "#FBBF24"},
    },
    "security": {
        "light": {"fill": "#FFF1F2", "stroke": "#F43F5E"},
        "dark": {"fill": "#2A1018", "stroke": "#FB7185"},
    },
    "external": {
        "light": {"fill": "#F8FAFC", "stroke": "#64748B"},
        "dark": {"fill": "#1A2030", "stroke": "#94A3B8"},
    },
}

CATEGORY_ALIASES: dict[str, str] = {
    "web": "frontend",
    "mobile": "frontend",
    "ui": "frontend",
    "api": "backend",
    "service": "backend",
    "microservice": "backend",
    "storage": "database",
    "infra": "cloud",
    "infrastructure": "cloud",
    "devops": "cloud",
    "auth": "security",
    "third-party": "external",
    "third_party": "external",
    "saas": "external",
}

ARROW_STYLES: dict[str, dict[str, str | None]] = {
    "supports": {"color": "#34D399", "dash": None, "marker": "arrow-solid"},
    "depends-on": {"color": "#94A3B8", "dash": "6,4", "marker": "arrow-open"},
    "flows-to": {"color": "#60A5FA", "dash": None, "marker": "arrow-solid"},
    "owned-by": {"color": "#FBBF24", "dash": "3,3", "marker": "arrow-dot"},
}

_ARROW_STYLES_LIGHT: dict[str, dict[str, str]] = {
    "supports": {"color": "#0B6E6E"},
    "depends-on": {"color": "#94A3B8"},
    "flows-to": {"color": "#3B82F6"},
    "owned-by": {"color": "#D97706"},
}


def resolve_theme(name: str = "light", industry: str | None = None) -> dict:
    """Return the color palette for the given theme, with optional industry accent."""
    base = C_DARK if name == "dark" else C_LIGHT
    if not industry or industry == "common":
        return base
    overrides = INDUSTRY_THEMES.get(industry)
    if not overrides:
        return base
    result = dict(base)
    accent = overrides["accent"]
    result["cap_stroke"] = accent
    result["actor_stroke"] = accent
    result["arrow"] = accent
    return result


def resolve_system_colors(category: str | None, theme: str) -> tuple[str, str]:
    """Get (fill, stroke) for a system node based on its category."""
    canonical = CATEGORY_ALIASES.get(category, category) if category else None
    palette = SYSTEM_CATEGORY_COLORS.get(canonical)
    if palette:
        colors = palette.get(theme, palette.get("light", {}))
        return colors.get("fill", ""), colors.get("stroke", "")
    return "", ""


def resolve_arrow_style(relation_type: str, theme: str) -> dict[str, str | None]:
    """Get arrow style for a relation type, adjusted for theme."""
    style = ARROW_STYLES.get(relation_type, ARROW_STYLES["supports"]).copy()
    if theme == "light" and relation_type in _ARROW_STYLES_LIGHT:
        style["color"] = _ARROW_STYLES_LIGHT[relation_type]["color"]
    return style
