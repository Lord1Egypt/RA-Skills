#!/usr/bin/env python3
"""Migrate legacy article-html-to-ppt style contracts to v2 token contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


GENERIC_FONT_STACK = ["Aptos", "Noto Sans CJK SC", "Microsoft YaHei", "sans-serif"]
EDITORIAL_FONT_STACK = ["Source Han Serif SC", "Noto Serif CJK SC", "SimSun", "serif"]
MONO_FONT_STACK = ["JetBrains Mono", "Consolas", "monospace"]


def color_value(colors: dict[str, Any], *keys: str, default: str) -> str:
    for key in keys:
        value = colors.get(key)
        if isinstance(value, str) and value.startswith("#"):
            return value
    return default


def migrate(data: dict[str, Any]) -> dict[str, Any]:
    colors = data.get("colors", {}) if isinstance(data.get("colors"), dict) else {}
    typography = data.get("typography", {}) if isinstance(data.get("typography"), dict) else {}
    old_grid = data.get("grid") or data.get("layout", {}).get("grid", {})
    if not isinstance(old_grid, dict):
        old_grid = {}
    spacing_scale = data.get("spacing_scale_in", [0.06, 0.1, 0.16, 0.24, 0.36, 0.52])
    if not isinstance(spacing_scale, list) or len(spacing_scale) < 3:
        spacing_scale = [0.06, 0.1, 0.16, 0.24, 0.36, 0.52]
    scale_names = ["xs", "sm", "md", "lg", "xl", "xxl"]
    spacing = {
        "unit": "in",
        "scale": {name: spacing_scale[idx] for idx, name in enumerate(scale_names[: len(spacing_scale)])},
        "rules": {
            "title_to_body": "lg",
            "card_gap": "md",
            "section_gap": "xl",
            "icon_to_label": "sm",
            "label_to_value": "xs",
            "paragraph_gap": "sm",
        },
    }

    primary = color_value(colors, "primary", default="#1B2A42")
    accent = color_value(colors, "accent", default="#C69749")
    background = color_value(colors, "background", default="#FAF9F5")
    surface_1 = color_value(colors, "surface_1", "surface", "secondary_surface", default="#F4F1EA")
    surface_2 = color_value(colors, "surface_2", "secondary", default="#ECE7DC")
    text_primary = color_value(colors, "text_primary", "text", default="#2D3340")
    text_secondary = color_value(colors, "text_secondary", "muted", default="#6E6A60")
    border = color_value(colors, "border", default="#E4E0D7")

    style_id = data.get("style_id") or data.get("style_system") or "custom-style"
    display_name = data.get("display_name") or str(style_id).replace("-", " ").title()
    aliases = []
    if data.get("palette_name"):
        aliases.append({"alias": data["palette_name"], "maps_to": style_id})

    default_card_tokens = {
        "default": {"fill": "surface_1", "text_color": "text_primary", "border_color": "border", "border_width_ref": "shape_tokens.border_width_pt", "radius_ref": "shape_tokens.card_radius_pt", "padding": {"horizontal": "md", "vertical": "md"}, "shadow_ref": "shadow_tokens.default"},
        "highlight": {"fill": "primary", "text_color": "background", "border_color": "primary"},
        "metric": {"fill": "background", "number_color": "primary", "label_color": "text_secondary", "trend_positive_color": "positive", "trend_negative_color": "negative"},
        "risk": {"fill": "surface_1", "border_color": "warning", "icon_color": "warning"},
        "quote": {"fill": "surface_1", "text_color": "text_primary", "border_color": "accent"},
        "comparison": {"fill": "background", "text_color": "text_primary", "border_color": "border"},
        "source": {"fill": "surface_2", "text_color": "text_secondary", "border_color": "border"},
    }
    legacy_cards = (data.get("component_variants") or {}).get("cards", {}) if isinstance(data.get("component_variants"), dict) else {}
    if not isinstance(legacy_cards, dict):
        legacy_cards = {}
    card_tokens = data.get("card_tokens", legacy_cards)
    if not isinstance(card_tokens, dict) or "default" not in card_tokens:
        card_tokens = default_card_tokens
    else:
        card_tokens = {**default_card_tokens, **card_tokens}

    migrated = {
        "schema_version": "2.0",
        "style_id": style_id,
        "display_name": display_name,
        "description": data.get("description", "Migrated style contract."),
        "audience": data.get("audience") if isinstance(data.get("audience"), list) else ["general"],
        "formality": data.get("formality", "professional"),
        "presentation_context": data.get("presentation_context", ["live", "review"]),
        "aspect_ratios": data.get("aspect_ratios", ["16:9"]),
        "colors": {
            "primary": primary,
            "accent": accent,
            "background": background,
            "surface_1": surface_1,
            "surface_2": surface_2,
            "text_primary": text_primary,
            "text_secondary": text_secondary,
            "border": border,
            "positive": color_value(colors, "positive", default="#4E7358"),
            "warning": color_value(colors, "warning", default="#A66A2C"),
            "negative": color_value(colors, "negative", default="#9C4A48"),
            "data_series": colors.get("data_series", [primary, accent, "#4E7358", text_secondary]),
            "allowed_opacity": colors.get("allowed_opacity", [0.08, 0.12, 0.18, 0.45, 1]),
        },
        "typography": {
            "font_primary": typography.get("font_primary", GENERIC_FONT_STACK),
            "font_editorial": typography.get("font_editorial", EDITORIAL_FONT_STACK),
            "font_mono": typography.get("font_mono", MONO_FONT_STACK),
            "title_sizes_pt": typography.get("title_sizes_pt", {"cover": 34, "section": 28, "slide": typography.get("title_size_pt", 22)}),
            "body_sizes_pt": typography.get("body_sizes_pt", {"large": 16, "normal": typography.get("body_size_pt", 13), "small": 10, "footnote": typography.get("caption_size_pt", 8.5)}),
            "metric_sizes_pt": typography.get("metric_sizes_pt", {"hero": 30, "normal": 22}),
            "minimum_body_size_pt": typography.get("minimum_body_size_pt", 10),
            "minimum_footnote_size_pt": typography.get("minimum_footnote_size_pt", 8),
            "line_height": typography.get("line_height", {"cover_title": 1.05, "slide_title": 1.1, "body": 1.35, "caption": 1.25}),
            "paragraph_spacing_pt": typography.get("paragraph_spacing_pt", {"body": 6, "list": 4}),
            "letter_spacing_pt": typography.get("letter_spacing_pt", {"cover_title": 0, "uppercase_label": 0.8}),
            "weights": typography.get("weights", {"regular": 400, "medium": 500, "semibold": 600, "bold": 700}),
        },
        "grid": {
            "columns": old_grid.get("columns", 12),
            "rows": old_grid.get("rows", 8),
            "margin_left_in": old_grid.get("margin_left_in", 0.55),
            "margin_right_in": old_grid.get("margin_right_in", 0.55),
            "margin_top_in": old_grid.get("margin_top_in", 0.38),
            "margin_bottom_in": old_grid.get("margin_bottom_in", 0.35),
            "gutter_horizontal_in": old_grid.get("gutter_horizontal_in", old_grid.get("gutter_in", 0.14)),
            "gutter_vertical_in": old_grid.get("gutter_vertical_in", 0.12),
            "title_zone_height_in": old_grid.get("title_zone_height_in", 0.72),
            "footer_zone_height_in": old_grid.get("footer_zone_height_in", 0.24),
            "safe_zone_in": old_grid.get("safe_zone_in", {"left": 0.08, "right": 0.08, "top": 0.06, "bottom": 0.06}),
        },
        "spacing": spacing,
        "shape_tokens": data.get("shape_tokens", {"card_radius_pt": 8, "border_width_pt": 0.8, "connector_width_pt": 1.2, "primary_connector_width_pt": 2.2}),
        "shadow_tokens": data.get("shadow_tokens", {"default": {"enabled": False}}),
        "card_tokens": card_tokens,
        "table_tokens": data.get("table_tokens", {"default": {"header_fill": "primary", "header_text": "background", "body_fill": "background", "alternate_row_fill": "surface_1", "text_color": "text_primary", "border_color": "border", "border_width_pt": 0.5, "cell_padding_in": {"horizontal": 0.08, "vertical": 0.06}, "header_font_weight": 600, "body_font_size_ref": "typography.body_sizes_pt.small"}}),
        "chart_tokens": data.get("chart_tokens", {"series_colors": ["primary", "accent", "positive"], "axis_color": "border", "highlight_color": "accent"}),
        "diagram_tokens": data.get("diagram_tokens", {"node": {"fill": "surface_1", "text_color": "text_primary", "border_color": "border"}, "connector": {"default_color": "text_secondary", "primary_color": "primary"}, "relation_styles": {"request": "orthogonal", "feedback": "curved", "optional": "dashed"}}),
        "image_tokens": data.get("image_tokens", {"default_crop_mode": "cover", "caption_position": "bottom", "caption_style_ref": "typography.body_sizes_pt.footnote"}),
        "icon_tokens": data.get("icon_tokens", {"stroke_width_pt": 1.4, "default_color": "text_secondary", "accent_color": "accent", "allowed_styles": ["outline"]}),
        "footer_tokens": data.get("footer_tokens", data.get("footer", {"enabled": True, "height_in": 0.24, "text_color": "text_secondary", "font_size_ref": "typography.body_sizes_pt.footnote", "divider_color": "border"})),
        "density_limits": data.get("density_limits", {"low": {"max_primary_objects": 2, "max_supporting_objects": 3, "max_body_characters_zh": 80}, "medium": {"max_primary_objects": 4, "max_supporting_objects": 5, "max_body_characters_zh": 180}, "high": {"max_primary_objects": 6, "max_supporting_objects": 8, "max_body_characters_zh": 320}}),
        "component_variants": data.get("component_variants", {}),
        "allowed_effects": data.get("allowed_effects", ["subtle_divider", "single_accent_rule"]),
        "forbidden_drift": data.get("forbidden_drift", ["invented colors", "unbounded raster components"]),
        "compatibility_aliases": data.get("compatibility_aliases", aliases),
    }
    return migrated


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate legacy style-contract JSON to v2.")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    migrated = migrate(data)
    output = json.dumps(migrated, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
