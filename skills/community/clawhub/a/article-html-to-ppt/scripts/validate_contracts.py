#!/usr/bin/env python3
"""Validate article-html-to-ppt contract files against formal v2 schemas.

The validator intentionally uses only the Python standard library so it can
ship inside a skill. It performs a practical JSON Schema subset check, then
adds cross-file contract checks for PPT production: title/judgment semantics,
source references, color references, and raster declarations.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from diagram_ir_tools import validate_diagram_semantics as validate_diagram_ir_semantics
from visual_narrative.intent import validate_page_design_intent

TITLE_ROLES = {"judgment", "navigation", "section", "instruction", "reference", "closing"}
NON_JUDGMENT_SLIDE_ROLES = {"cover", "agenda", "section", "reference", "closing", "instruction"}
PRIMARY_EXPRESSIONS = {
    "textual_argument",
    "structured_cards",
    "table_matrix",
    "data_visual",
    "relationship_visual",
    "conceptual_scene",
}
PROFILES = {"fast", "standard", "premium"}
SCHEMA_FILES = {
    "ppt-ir": "ppt-ir.schema.json",
    "style": "style-contract.schema.json",
    "assets": "asset-manifest.schema.json",
    "build": "build-manifest.schema.json",
    "qa": "qa-report.schema.json",
    "diagram": "diagram-ir.schema.json",
    "component-registry": "component-registry.schema.json",
    "delivery": "delivery-plan.schema.json",
    "page-design-intent": "page-design-intent.schema.json",
    "task-route": "task-route.schema.json",
    "visual-plan": "visual-plan.schema.json",
    "visual-revision-request": "visual-revision-request.schema.json",
    # v4 contracts (schemas/v4/); see schemas/v4/README.md
    "presentation-ir": "v4/presentation-ir.schema.json",
    "style-v4": "v4/style-contract-v4.schema.json",
    "decision-trace": "v4/decision-trace.schema.json",
    "render-plan": "v4/render-plan.schema.json",
}
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


def pointer_escape(part: str) -> str:
    return part.replace("~", "~0").replace("/", "~1")


def issue(file: Path | str, pointer: str, code: str, actual: Any, allowed: Any, suggestion: str) -> dict[str, Any]:
    return {
        "file": str(file),
        "pointer": pointer or "/",
        "code": code,
        "actual_value": actual,
        "allowed_values": allowed,
        "repair_suggestion": suggestion,
    }


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def load_schema(schema_dir: Path, name: str) -> dict[str, Any]:
    return load_json(schema_dir / SCHEMA_FILES[name])


def type_ok(value: Any, expected: str | list[str]) -> bool:
    if isinstance(expected, list):
        return any(type_ok(value, item) for item in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_schema_subset(
    data: Any,
    schema: dict[str, Any],
    file: Path,
    strict: bool,
    pointer: str = "",
    root: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    root = root or schema
    errors: list[dict[str, Any]] = []

    if "oneOf" in schema:
        matches = []
        for option in schema["oneOf"]:
            option_errors = validate_schema_subset(data, option, file, strict, pointer, root)
            if not option_errors:
                matches.append(option)
        if len(matches) != 1:
            return [issue(file, pointer, "ONE_OF_INVALID", data, "exactly one matching schema", "Satisfy exactly one of the allowed schema alternatives.")]

    if "anyOf" in schema:
        matched = False
        for option in schema["anyOf"]:
            option_errors = validate_schema_subset(data, option, file, strict, pointer, root)
            if not option_errors:
                matched = True
                break
        if not matched:
            return [issue(file, pointer, "ANY_OF_INVALID", data, "at least one matching schema", "Satisfy one of the allowed schema alternatives.")]

    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/$defs/"):
            name = ref.rsplit("/", 1)[-1]
            return validate_schema_subset(data, root.get("$defs", {}).get(name, {}), file, strict, pointer, root)

    if "const" in schema and data != schema["const"]:
        return [issue(file, pointer, "CONST_INVALID", data, schema["const"], f"Use constant value {schema['const']!r}.")]

    if "enum" in schema and data not in schema["enum"]:
        return [issue(file, pointer, "ENUM_INVALID", data, schema["enum"], "Use one of the allowed enum values.")]

    expected_type = schema.get("type")
    if expected_type and not type_ok(data, expected_type):
        return [issue(file, pointer, "TYPE_INVALID", data, expected_type, "Use the required JSON type.")]

    if isinstance(data, str) and schema.get("minLength") is not None and len(data) < schema["minLength"]:
        errors.append(issue(file, pointer, "MIN_LENGTH_INVALID", data, f">= {schema['minLength']}", "Use a non-empty value."))

    if isinstance(data, str) and schema.get("maxLength") is not None and len(data) > schema["maxLength"]:
        errors.append(issue(file, pointer, "MAX_LENGTH_INVALID", data, f"<= {schema['maxLength']}", "Shorten the string value."))

    if isinstance(data, str) and schema.get("pattern") and not re.match(schema["pattern"], data):
        errors.append(issue(file, pointer, "PATTERN_INVALID", data, schema["pattern"], "Match the required string pattern."))

    if isinstance(data, (int, float)) and schema.get("minimum") is not None and data < schema["minimum"]:
        errors.append(issue(file, pointer, "MINIMUM_INVALID", data, f">= {schema['minimum']}", "Increase the numeric value."))

    if isinstance(data, (int, float)) and schema.get("maximum") is not None and data > schema["maximum"]:
        errors.append(issue(file, pointer, "MAXIMUM_INVALID", data, f"<= {schema['maximum']}", "Decrease the numeric value."))

    if isinstance(data, (int, float)) and schema.get("exclusiveMinimum") is not None and data <= schema["exclusiveMinimum"]:
        errors.append(issue(file, pointer, "EXCLUSIVE_MINIMUM_INVALID", data, f"> {schema['exclusiveMinimum']}", "Increase the numeric value."))

    if isinstance(data, (int, float)) and schema.get("exclusiveMaximum") is not None and data >= schema["exclusiveMaximum"]:
        errors.append(issue(file, pointer, "EXCLUSIVE_MAXIMUM_INVALID", data, f"< {schema['exclusiveMaximum']}", "Decrease the numeric value."))

    if isinstance(data, (int, float)) and schema.get("multipleOf") and not isinstance(data, bool) and (data % schema["multipleOf"]) != 0:
        errors.append(issue(file, pointer, "MULTIPLE_OF_INVALID", data, f"multiple of {schema['multipleOf']}", "Use a permitted step value."))

    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(issue(file, pointer, "MIN_ITEMS_INVALID", len(data), f">= {schema['minItems']}", "Add required items."))
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append(issue(file, pointer, "MAX_ITEMS_INVALID", len(data), f"<= {schema['maxItems']}", "Remove extra items."))
        if schema.get("uniqueItems") and len(data) != len({json.dumps(item, sort_keys=True) for item in data}):
            errors.append(issue(file, pointer, "UNIQUE_ITEMS_INVALID", data, "unique items", "Remove duplicate array items."))
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(data):
                errors.extend(validate_schema_subset(item, item_schema, file, strict, f"{pointer}/{idx}", root))

    if isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(issue(file, f"{pointer}/{pointer_escape(key)}", "REQUIRED_FIELD_MISSING", None, key, f"Add required field `{key}`."))
        properties = schema.get("properties", {})
        for key, value in data.items():
            next_pointer = f"{pointer}/{pointer_escape(key)}"
            if key in properties:
                errors.extend(validate_schema_subset(value, properties[key], file, strict, next_pointer, root))
            elif strict and schema.get("additionalProperties") is False:
                errors.append(issue(file, next_pointer, "ADDITIONAL_PROPERTY", value, sorted(properties), "Remove undeclared property or update the schema."))
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(validate_schema_subset(value, schema["additionalProperties"], file, strict, next_pointer, root))
    return errors


def source_ids(ppt_ir: dict[str, Any]) -> set[str]:
    return {src.get("source_id") for src in ppt_ir.get("sources", []) if isinstance(src, dict) and src.get("source_id")}


def validate_source_refs(file: Path, pointer: str, refs: Any, declared_sources: set[str]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not isinstance(refs, list):
        return errors
    for idx, ref in enumerate(refs):
        source_id = ref.get("source_id") if isinstance(ref, dict) else ref
        if source_id and source_id not in declared_sources:
            errors.append(issue(file, f"{pointer}/{idx}/source_id", "SOURCE_REF_NOT_FOUND", source_id, sorted(declared_sources), "Use a declared source_id from /sources."))
    return errors


def collect_style_refs(style: dict[str, Any] | None) -> set[str]:
    if not isinstance(style, dict):
        return set()
    refs: set[str] = set()

    def walk(value: Any, prefix: str) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                path = f"{prefix}.{key}" if prefix else key
                refs.add(path)
                walk(item, path)
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                path = f"{prefix}.{idx}" if prefix else str(idx)
                refs.add(path)
                walk(item, path)

    for top_key in [
        "colors",
        "typography",
        "grid",
        "spacing",
        "shape_tokens",
        "shadow_tokens",
        "card_tokens",
        "table_tokens",
        "chart_tokens",
        "diagram_tokens",
        "image_tokens",
        "icon_tokens",
        "component_variants",
        "footer_tokens",
        "density_limits",
    ]:
        walk(style.get(top_key), top_key)
    return refs


def validate_diagram_semantics(file: Path, diagram: dict[str, Any], pointer: str, declared_sources: set[str] | None = None) -> list[dict[str, Any]]:
    if not isinstance(diagram, dict):
        return []
    return validate_diagram_ir_semantics(diagram, issue, file, pointer, declared_sources)


def validate_ppt_ir_semantics(file: Path, ppt_ir: dict[str, Any], assets: dict[str, Any] | None, style: dict[str, Any] | None) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    declared_sources = source_ids(ppt_ir)
    declared_style_refs = collect_style_refs(style)
    declared_assets = {
        asset.get("asset_id")
        for asset in (assets or {}).get("assets", [])
        if isinstance(asset, dict) and asset.get("asset_id")
    }
    raster_assets = {
        asset.get("asset_id")
        for asset in (assets or {}).get("assets", [])
        if isinstance(asset, dict) and asset.get("raster_declared")
    }

    for idx, slide in enumerate(ppt_ir.get("slides", []) or []):
        if not isinstance(slide, dict):
            continue
        ptr = f"/slides/{idx}"
        title_role = slide.get("title_role")
        slide_role = slide.get("slide_role")
        judgment = slide.get("judgment")
        if title_role == "judgment" and not judgment:
            errors.append(issue(file, ptr + "/judgment", "JUDGMENT_REQUIRED", judgment, "non-empty string", "Judgment slides must include an answer-first judgment."))
        if title_role != "judgment" and slide_role in NON_JUDGMENT_SLIDE_ROLES and judgment:
            errors.append(issue(file, ptr + "/judgment", "JUDGMENT_FOR_NON_JUDGMENT_ROLE", judgment, None, "Remove invented judgment or change title_role to judgment only when evidence supports it."))
        if slide.get("primary_expression") == "hybrid_panel":
            errors.append(issue(file, ptr + "/primary_expression", "HYBRID_PANEL_DEPRECATED", "hybrid_panel", sorted(PRIMARY_EXPRESSIONS), "Migrate to a true primary expression plus supporting_expressions."))
        errors.extend(validate_source_refs(file, ptr + "/source_refs", slide.get("source_refs"), declared_sources))
        for evidence_idx, evidence in enumerate(slide.get("supporting_evidence", []) or []):
            if isinstance(evidence, dict):
                errors.extend(validate_source_refs(
                    file,
                    f"{ptr}/supporting_evidence/{evidence_idx}/source_refs",
                    evidence.get("source_refs"),
                    declared_sources,
                ))

        delivery = slide.get("delivery_contract") if isinstance(slide.get("delivery_contract"), dict) else {}
        allowance = set(delivery.get("raster_allowance", []) or [])
        for obj_idx, obj in enumerate(slide.get("objects", []) or []):
            if not isinstance(obj, dict):
                continue
            obj_ptr = f"{ptr}/objects/{obj_idx}"
            errors.extend(validate_source_refs(file, obj_ptr + "/source_refs", obj.get("source_refs"), declared_sources))
            style_ref = obj.get("style_ref")
            if style_ref and declared_style_refs and style_ref not in declared_style_refs:
                errors.append(issue(file, obj_ptr + "/style_ref", "STYLE_REF_NOT_FOUND", style_ref, sorted(declared_style_refs), "Use a token path declared in style-contract.json."))
            asset_ref = obj.get("asset_ref")
            if asset_ref and assets is not None and asset_ref not in declared_assets:
                errors.append(issue(file, obj_ptr + "/asset_ref", "ASSET_REF_NOT_FOUND", asset_ref, sorted(declared_assets), "Use an asset_id declared in asset-manifest.json."))
            if obj.get("type") == "diagram":
                has_inline = isinstance(obj.get("diagram_ir"), dict)
                has_ref = bool(obj.get("diagram_ir_ref") or obj.get("diagram_ref"))
                if has_inline and has_ref:
                    errors.append(issue(file, obj_ptr, "DIAGRAM_IR_REFERENCE_CONFLICT", {"diagram_ir": True, "diagram_ir_ref": obj.get("diagram_ir_ref") or obj.get("diagram_ref")}, "exactly one diagram_ir or diagram_ir_ref", "Use either inline Diagram IR or an external reference, not both."))
                if not has_inline and not has_ref:
                    errors.append(issue(file, obj_ptr, "DIAGRAM_IR_MISSING", None, "diagram_ir or diagram_ir_ref", "Diagram objects must reference or inline a Diagram IR."))
                if has_ref:
                    rel = obj.get("diagram_ir_ref") or obj.get("diagram_ref")
                    path = Path(rel)
                    if not path.is_absolute():
                        path = file.parent / path
                    if not path.exists():
                        errors.append(issue(file, obj_ptr + "/diagram_ir_ref", "DIAGRAM_IR_REF_NOT_FOUND", rel, "existing Diagram IR file", "Create the referenced Diagram IR file or inline diagram_ir."))
            if isinstance(obj.get("diagram_ir"), dict):
                errors.extend(validate_diagram_semantics(file, obj["diagram_ir"], obj_ptr + "/diagram_ir", declared_sources))
            if obj.get("editability") in {"raster_allowed", "raster_only"}:
                if asset_ref not in raster_assets and obj.get("id") not in allowance and asset_ref not in allowance:
                    errors.append(issue(file, obj_ptr + "/asset_ref", "RASTER_UNDECLARED", asset_ref, sorted(raster_assets | allowance), "Declare raster use in asset-manifest or slide delivery_contract.raster_allowance."))
    return errors


def token_exists(style: dict[str, Any], token_ref: str) -> bool:
    current: Any = style
    for part in token_ref.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False
    return True


def color_token_errors(file: Path, style: dict[str, Any], section: str, value: Any, pointer: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    colors = style.get("colors", {}) if isinstance(style.get("colors"), dict) else {}
    declared = set(colors) - {"data_series", "allowed_opacity"}
    color_keys = {
        "fill",
        "text_color",
        "border_color",
        "number_color",
        "label_color",
        "trend_positive_color",
        "trend_negative_color",
        "icon_color",
        "header_fill",
        "header_text",
        "body_fill",
        "alternate_row_fill",
        "row_header_fill",
        "column_header_fill",
        "highlight_fill",
        "highlight_text",
        "series_colors",
        "axis_color",
        "axis_label_color",
        "gridline_color",
        "data_label_color",
        "highlight_color",
        "default_color",
        "primary_color",
        "accent_color",
        "divider_color",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            next_pointer = f"{pointer}/{pointer_escape(str(key))}"
            if key in color_keys:
                refs = item if isinstance(item, list) else [item]
                for ref_idx, ref in enumerate(refs):
                    if isinstance(ref, str) and ref not in declared and not ref.startswith("#"):
                        suffix = f"/{ref_idx}" if isinstance(item, list) else ""
                        errors.append(issue(file, next_pointer + suffix, "STYLE_UNKNOWN_TOKEN_REFERENCE", ref, sorted(declared), f"Reference a declared color token in /colors for {section}."))
            errors.extend(color_token_errors(file, style, section, item, next_pointer))
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            errors.extend(color_token_errors(file, style, section, item, f"{pointer}/{idx}"))
    return errors


def validate_style_semantics(file: Path, style: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    colors = style.get("colors", {}) if isinstance(style.get("colors"), dict) else {}
    semantic_color_keys = [
        "primary",
        "accent",
        "background",
        "surface_1",
        "surface_2",
        "text_primary",
        "text_secondary",
        "border",
        "positive",
        "warning",
        "negative",
    ]
    for key in semantic_color_keys:
        if key not in colors:
            errors.append(issue(file, f"/colors/{key}", "STYLE_REQUIRED_COLOR_MISSING", None, key, f"Add semantic color `{key}`."))
        elif not isinstance(colors[key], str) or not re.match(r"^#[0-9A-Fa-f]{6}$", colors[key]):
            errors.append(issue(file, f"/colors/{key}", "STYLE_INVALID_HEX", colors.get(key), "#RRGGBB", "Use a six-digit hex color."))
    data_series = colors.get("data_series", [])
    if isinstance(data_series, list) and len(data_series) < 3:
        errors.append(issue(file, "/colors/data_series", "STYLE_DATA_SERIES_TOO_SHORT", len(data_series), ">= 3", "Provide at least three data series colors."))

    typography = style.get("typography", {}) if isinstance(style.get("typography"), dict) else {}
    generic_families = {"sans-serif", "serif", "monospace", "cursive", "fantasy", "system-ui"}
    for key in ["font_primary", "font_editorial", "font_mono"]:
        stack = typography.get(key)
        if not isinstance(stack, list) or not stack:
            errors.append(issue(file, f"/typography/{key}", "STYLE_FONT_STACK_EMPTY", stack, "non-empty font stack", "Provide an ordered font fallback stack."))
        elif stack[-1] not in generic_families:
            errors.append(issue(file, f"/typography/{key}", "STYLE_FONT_GENERIC_FAMILY_MISSING", stack[-1], sorted(generic_families), "End the stack with a generic CSS font family."))
    body_sizes = typography.get("body_sizes_pt", {}) if isinstance(typography.get("body_sizes_pt"), dict) else {}
    minimum_body = typography.get("minimum_body_size_pt")
    if isinstance(minimum_body, (int, float)):
        for key, size in body_sizes.items():
            if isinstance(size, (int, float)) and key != "footnote" and size < minimum_body:
                errors.append(issue(file, f"/typography/body_sizes_pt/{pointer_escape(key)}", "STYLE_BODY_SIZE_BELOW_MINIMUM", size, f">= {minimum_body}", "Raise body size or lower the documented minimum."))
    minimum_footnote = typography.get("minimum_footnote_size_pt")
    footnote = body_sizes.get("footnote")
    if isinstance(minimum_footnote, (int, float)) and isinstance(footnote, (int, float)) and footnote < minimum_footnote:
        errors.append(issue(file, "/typography/body_sizes_pt/footnote", "STYLE_FOOTNOTE_SIZE_BELOW_MINIMUM", footnote, f">= {minimum_footnote}", "Raise footnote size or lower the documented minimum."))
    for key, value in (typography.get("line_height", {}) or {}).items():
        if isinstance(value, (int, float)) and not 1 <= value <= 2:
            errors.append(issue(file, f"/typography/line_height/{pointer_escape(key)}", "STYLE_INVALID_LINE_HEIGHT", value, "1.0-2.0", "Use a readable line-height ratio."))
    for key, value in (typography.get("weights", {}) or {}).items():
        if isinstance(value, int) and value not in {100, 200, 300, 400, 500, 600, 700, 800, 900}:
            errors.append(issue(file, f"/typography/weights/{pointer_escape(key)}", "STYLE_INVALID_FONT_WEIGHT", value, "100..900 step 100", "Use a standard OpenType weight."))

    grid = style.get("grid", {}) if isinstance(style.get("grid"), dict) else {}
    if grid.get("margin_top_in", 0) + grid.get("margin_bottom_in", 0) + grid.get("title_zone_height_in", 0) + grid.get("footer_zone_height_in", 0) >= 7.5:
        errors.append(issue(file, "/grid", "STYLE_GRID_OVERFLOW", grid, "content space remains on 16:9 slide", "Reduce margins, title zone, or footer zone."))

    spacing = style.get("spacing", {}) if isinstance(style.get("spacing"), dict) else {}
    spacing_scale = set((spacing.get("scale") or {}).keys()) if isinstance(spacing.get("scale"), dict) else set()
    for key, ref in (spacing.get("rules") or {}).items():
        if ref not in spacing_scale:
            errors.append(issue(file, f"/spacing/rules/{pointer_escape(key)}", "STYLE_SPACING_REFERENCE_MISSING", ref, sorted(spacing_scale), "Reference a spacing token declared under /spacing/scale."))

    for section in ["card_tokens", "table_tokens", "chart_tokens", "diagram_tokens", "image_tokens", "icon_tokens", "footer_tokens"]:
        errors.extend(color_token_errors(file, style, section, style.get(section), f"/{section}"))

    card_tokens = style.get("card_tokens", {}) if isinstance(style.get("card_tokens"), dict) else {}
    required_cards = {"default", "highlight", "metric", "risk", "quote", "comparison", "source"}
    missing_cards = sorted(required_cards - set(card_tokens))
    if missing_cards:
        errors.append(issue(file, "/card_tokens", "STYLE_CARD_VARIANT_INVALID", missing_cards, sorted(required_cards), "Define the required card token variants."))

    for section in ["card_tokens", "diagram_tokens", "image_tokens", "footer_tokens"]:
        value = style.get(section)
        if not isinstance(value, dict):
            continue
        refs: list[tuple[str, str]] = []

        def collect_refs(node: Any, ptr: str) -> None:
            if isinstance(node, dict):
                for key, item in node.items():
                    next_ptr = f"{ptr}/{pointer_escape(str(key))}"
                    if key.endswith("_ref") and isinstance(item, str):
                        refs.append((next_ptr, item))
                    collect_refs(item, next_ptr)
            elif isinstance(node, list):
                for idx, item in enumerate(node):
                    collect_refs(item, f"{ptr}/{idx}")

        collect_refs(value, f"/{section}")
        for ptr, ref in refs:
            if not token_exists(style, ref):
                errors.append(issue(file, ptr, "STYLE_UNKNOWN_TOKEN_REFERENCE", ref, "existing style token path", "Reference a token path declared in the style contract."))

    relation_styles = ((style.get("diagram_tokens") or {}).get("relation_styles") or {})
    allowed_relation_routes = {"straight", "orthogonal", "curved", "dashed"}
    if isinstance(relation_styles, dict):
        for key, value in relation_styles.items():
            if value not in allowed_relation_routes:
                errors.append(issue(file, f"/diagram_tokens/relation_styles/{pointer_escape(key)}", "STYLE_DIAGRAM_RELATION_UNKNOWN", value, sorted(allowed_relation_routes), "Use a supported diagram relation style."))

    density = style.get("density_limits", {}) if isinstance(style.get("density_limits"), dict) else {}
    for tier in ["low", "medium", "high"]:
        tier_value = density.get(tier, {})
        if not isinstance(tier_value, dict):
            continue
        for key, value in tier_value.items():
            if isinstance(value, (int, float)) and value < 0:
                errors.append(issue(file, f"/density_limits/{tier}/{pointer_escape(key)}", "STYLE_DENSITY_LIMIT_INVALID", value, ">= 0", "Use non-negative diagnostic limits."))

    drift = style.get("forbidden_drift", [])
    if isinstance(drift, list) and len(drift) != len(set(drift)):
        errors.append(issue(file, "/forbidden_drift", "STYLE_FORBIDDEN_DRIFT_DUPLICATE", drift, "unique items", "Remove duplicate forbidden drift entries."))
    aliases = style.get("compatibility_aliases", [])
    alias_map: dict[str, str] = {}
    if isinstance(aliases, list):
        for idx, alias in enumerate(aliases):
            if not isinstance(alias, dict):
                continue
            name = alias.get("alias")
            target = alias.get("maps_to")
            if name in alias_map and alias_map[name] != target:
                errors.append(issue(file, f"/compatibility_aliases/{idx}", "STYLE_ALIAS_CONFLICT", alias, alias_map[name], "Map each alias to exactly one style_id."))
            if name:
                alias_map[name] = target
    return errors


def validate_asset_semantics(file: Path, assets: dict[str, Any], declared_sources: set[str]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for idx, asset in enumerate(assets.get("assets", []) or []):
        if not isinstance(asset, dict):
            continue
        for ref_idx, source_id in enumerate(asset.get("source_refs", []) or []):
            if declared_sources and source_id not in declared_sources:
                errors.append(issue(file, f"/assets/{idx}/source_refs/{ref_idx}", "SOURCE_REF_NOT_FOUND", source_id, sorted(declared_sources), "Use a source_id declared in ppt-ir.json /sources."))
    return errors


def output_paths(outputs: Any) -> list[str]:
    paths: list[str] = []
    if not isinstance(outputs, dict):
        return paths
    for value in outputs.values():
        if isinstance(value, str):
            paths.append(value)
        elif isinstance(value, list):
            paths.extend(item for item in value if isinstance(item, str))
    return paths


def validate_build_semantics(file: Path, build: dict[str, Any], base_dir: Path) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    status = build.get("status")
    stages = build.get("stages", {}) if isinstance(build.get("stages"), dict) else {}
    required_stage_by_status = {
        "created": "built",
        "rendered": "rendered",
        "read_back": "read_back",
        "verified": "qa_passed",
        "final": "qa_passed",
    }
    stage_key = required_stage_by_status.get(status)
    if stage_key and stages.get(stage_key) is not True:
        errors.append(issue(file, f"/stages/{stage_key}", "BUILD_STAGE_STATUS_MISMATCH", stages.get(stage_key), True, f"Set stages.{stage_key}=true or lower build status."))
    for rel_path in output_paths(build.get("outputs")):
        path = Path(rel_path)
        if not path.is_absolute():
            path = base_dir / path
        if not path.exists():
            errors.append(issue(file, "/outputs", "BUILD_OUTPUT_NOT_FOUND", rel_path, "existing file path", "Create the output file or remove it from build-manifest.json until it exists."))
    return errors


def validate_qa_semantics(file: Path, qa: dict[str, Any], ppt_ir: dict[str, Any] | None) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not isinstance(ppt_ir, dict):
        return errors
    slide_ids = {slide.get("id") for slide in ppt_ir.get("slides", []) if isinstance(slide, dict)}
    object_ids: set[str] = set()
    for slide in ppt_ir.get("slides", []) or []:
        if not isinstance(slide, dict):
            continue
        for obj in slide.get("objects", []) or []:
            if isinstance(obj, dict) and obj.get("id"):
                object_ids.add(obj["id"])
    for idx, issue_item in enumerate(qa.get("issues", []) or []):
        if not isinstance(issue_item, dict):
            continue
        slide_id = issue_item.get("slide_id")
        object_id = issue_item.get("object_id")
        if slide_id and slide_id not in slide_ids:
            errors.append(issue(file, f"/issues/{idx}/slide_id", "QA_SLIDE_REF_NOT_FOUND", slide_id, sorted(slide_ids), "Reference a slide id from ppt-ir.json."))
        if object_id and object_id not in object_ids:
            errors.append(issue(file, f"/issues/{idx}/object_id", "QA_OBJECT_REF_NOT_FOUND", object_id, sorted(object_ids), "Reference an object id from ppt-ir.json."))
    return errors


def validate_component_registry_semantics(file: Path, registry: dict[str, Any], style: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    seen: set[str] = set()
    style_refs = collect_style_refs(style) if isinstance(style, dict) else set()
    for idx, component in enumerate(registry.get("components", []) or []):
        if not isinstance(component, dict):
            continue
        component_type = component.get("component_type")
        if component_type in seen:
            errors.append(issue(file, f"/components/{idx}/component_type", "COMPONENT_DUPLICATE", component_type, "unique component_type", "Keep one registry entry per component type."))
        seen.add(component_type)
        allowed = set(component.get("allowed_delivery_routes", []) or [])
        preferred = component.get("preferred_delivery_route")
        if preferred and preferred not in allowed:
            errors.append(issue(file, f"/components/{idx}/preferred_delivery_route", "DELIVERY_ROUTE_NOT_ALLOWED", preferred, sorted(allowed), "Set preferred route to one of allowed_delivery_routes."))
        for f_idx, route in enumerate(component.get("fallback_chain", []) or []):
            if route not in allowed:
                errors.append(issue(file, f"/components/{idx}/fallback_chain/{f_idx}", "DELIVERY_ROUTE_NOT_ALLOWED", route, sorted(allowed), "Fallback routes must be allowed routes."))
        if style_refs:
            for d_idx, dep in enumerate(component.get("style_dependencies", []) or []):
                if dep not in style_refs and not any(ref.startswith(dep + ".") for ref in style_refs):
                    errors.append(issue(file, f"/components/{idx}/style_dependencies/{d_idx}", "STYLE_REF_NOT_FOUND", dep, sorted(style_refs), "Reference a token path declared in style-contract.json."))
    return errors


def collect_ppt_objects(ppt_ir: dict[str, Any] | None) -> tuple[set[str], set[tuple[str, str]], dict[tuple[str, str], dict[str, Any]]]:
    if not isinstance(ppt_ir, dict):
        return set(), set(), {}
    slide_ids: set[str] = set()
    object_pairs: set[tuple[str, str]] = set()
    object_map: dict[tuple[str, str], dict[str, Any]] = {}
    for slide in ppt_ir.get("slides", []) or []:
        if not isinstance(slide, dict):
            continue
        slide_id = slide.get("id")
        if slide_id:
            slide_ids.add(slide_id)
        for obj in slide.get("objects", []) or []:
            if isinstance(obj, dict) and slide_id and obj.get("id"):
                key = (slide_id, obj["id"])
                object_pairs.add(key)
                object_map[key] = obj
    return slide_ids, object_pairs, object_map


def validate_delivery_semantics(file: Path, delivery: dict[str, Any], ppt_ir: dict[str, Any] | None) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    slide_ids, object_pairs, object_map = collect_ppt_objects(ppt_ir)
    for s_idx, slide in enumerate(delivery.get("slides", []) or []):
        if not isinstance(slide, dict):
            continue
        slide_id = slide.get("slide_id")
        if slide_ids and slide_id not in slide_ids:
            errors.append(issue(file, f"/slides/{s_idx}/slide_id", "DELIVERY_SLIDE_REF_NOT_FOUND", slide_id, sorted(slide_ids), "Reference a slide id from ppt-ir.json."))
        for o_idx, obj in enumerate(slide.get("objects", []) or []):
            if not isinstance(obj, dict):
                continue
            object_id = obj.get("object_id")
            key = (slide_id, object_id)
            if object_pairs and key not in object_pairs:
                errors.append(issue(file, f"/slides/{s_idx}/objects/{o_idx}/object_id", "DELIVERY_OBJECT_REF_NOT_FOUND", object_id, sorted(object_pairs), "Reference an object id from ppt-ir.json."))
            component_type = obj.get("component_type")
            selected = obj.get("selected_route")
            source_obj = object_map.get(key, {})
            if component_type in ORDINARY_COMPONENTS and selected in {"raster_component", "generated_image", "background_image"}:
                errors.append(issue(file, f"/slides/{s_idx}/objects/{o_idx}/selected_route", "DELIVERY_ORDINARY_COMPONENT_RASTERIZED", selected, "native route", "Ordinary components must remain native/editable."))
            if source_obj.get("editability") == "native_required" and selected not in {"native_ppt", "native_chart", "native_table", "native_diagram", "unsupported"}:
                errors.append(issue(file, f"/slides/{s_idx}/objects/{o_idx}/selected_route", "DELIVERY_NATIVE_REQUIRED_UNAVAILABLE", selected, "native route or unsupported", "Do not silently downgrade native_required objects."))
            if selected == "unsupported" and "DELIVERY_NO_VALID_ROUTE" not in (obj.get("reason_codes") or []) and "DELIVERY_COMPONENT_NOT_REGISTERED" not in (obj.get("reason_codes") or []):
                errors.append(issue(file, f"/slides/{s_idx}/objects/{o_idx}/reason_codes", "DELIVERY_NO_VALID_ROUTE", obj.get("reason_codes"), "reason code present", "Explain why the object is unsupported."))
    return errors


def validate_build_delivery_semantics(file: Path, build: dict[str, Any], delivery: dict[str, Any] | None) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not isinstance(delivery, dict):
        return errors
    planned: dict[tuple[str, str], str] = {}
    for slide in delivery.get("slides", []) or []:
        for obj in slide.get("objects", []) or []:
            if isinstance(obj, dict):
                planned[(obj.get("slide_id"), obj.get("object_id"))] = obj.get("selected_route")
    for idx, fallback in enumerate(build.get("fallbacks", []) or []):
        if not isinstance(fallback, dict):
            continue
        key = (fallback.get("slide_id"), fallback.get("object_id"))
        authoritative_route = planned.get(key)
        if authoritative_route and fallback.get("planned_route") != authoritative_route:
            errors.append(issue(file, f"/fallbacks/{idx}/planned_route", "BUILD_ROUTE_DEVIATION", fallback.get("planned_route"), authoritative_route, "Use the route selected in delivery-plan.json or record a new delivery plan."))
        if authoritative_route and fallback.get("actual_route") != authoritative_route:
            errors.append(issue(file, f"/fallbacks/{idx}/actual_route", "BUILD_ROUTE_DEVIATION", fallback.get("actual_route"), authoritative_route, "Build the route selected in delivery-plan.json; any permitted fallback must be selected and disclosed in a new authoritative delivery plan before building."))
    return errors


def validate_page_design_intent_semantics(file: Path, document: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for intent_issue in validate_page_design_intent(document):
        errors.append(
            issue(
                file,
                "/",
                intent_issue["code"],
                document,
                "valid page design intent contract",
                "Complete the required intent fields and remove forbidden native_required fallbacks.",
            )
        )
    return errors


def detect_v1(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    text = json.dumps(data, ensure_ascii=False)
    return (
        "judgment_title" in text
        or "expression_mode" in text
        or "hybrid_panel" in text
        or data.get("schema_version") in {"1.0", "1.1", "1.2"}
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate article-html-to-ppt contract files.")
    parser.add_argument("--ppt-ir", type=Path)
    parser.add_argument("--style", type=Path)
    parser.add_argument("--assets", type=Path)
    parser.add_argument("--build", type=Path)
    parser.add_argument("--qa", type=Path)
    parser.add_argument("--diagram", type=Path)
    parser.add_argument("--component-registry", type=Path)
    parser.add_argument("--delivery", type=Path)
    parser.add_argument("--task-route", type=Path)
    parser.add_argument("--visual-plan", type=Path)
    parser.add_argument("--visual-revision", type=Path)
    parser.add_argument("--page-design-intent", type=Path, action="append", default=[])
    parser.add_argument("--presentation-ir", type=Path, help="v4 Presentation IR document")
    parser.add_argument("--style-v4", type=Path, help="v4 style contract (visual-system data pack)")
    parser.add_argument("--decision-trace", type=Path, help="v4 decision trace document")
    parser.add_argument("--render-plan", type=Path, help="v4 render plan document")
    parser.add_argument("--schema-dir", type=Path, default=Path(__file__).resolve().parents[1] / "schemas")
    parser.add_argument("--allow-v1", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json-output", action="store_true")
    args = parser.parse_args()

    errors: list[dict[str, Any]] = []
    loaded: dict[str, tuple[Path, dict[str, Any]]] = {}
    inputs = {
        "ppt-ir": args.ppt_ir,
        "style": args.style,
        "assets": args.assets,
        "build": args.build,
        "qa": args.qa,
        "diagram": args.diagram,
        "component-registry": args.component_registry,
        "delivery": args.delivery,
        "task-route": args.task_route,
        "visual-plan": args.visual_plan,
        "visual-revision-request": args.visual_revision,
        "presentation-ir": args.presentation_ir,
        "style-v4": args.style_v4,
        "decision-trace": args.decision_trace,
        "render-plan": args.render_plan,
    }
    page_design_intent_inputs = args.page_design_intent or []

    try:
        for name, path in inputs.items():
            if not path:
                continue
            data = load_json(path)
            is_v1 = name not in {
                "component-registry",
                "delivery",
                "diagram",
                "task-route",
                "visual-plan",
                "visual-revision-request",
                "presentation-ir",
                "style-v4",
                "decision-trace",
                "render-plan",
            } and detect_v1(data)
            if is_v1 and not args.allow_v1:
                errors.append(issue(path, "/", "V1_CONTRACT_DEPRECATED", data.get("schema_version"), "2.0", "Run scripts/migrate_manifest_v1_to_v2.py or pass --allow-v1 for a transition-only check."))
            if is_v1 and args.allow_v1:
                continue
            schema = load_schema(args.schema_dir, name)
            errors.extend(validate_schema_subset(data, schema, path, args.strict))
            if isinstance(data, dict):
                loaded[name] = (path, data)
        page_design_intents: list[tuple[Path, dict[str, Any]]] = []
        for path in page_design_intent_inputs:
            data = load_json(path)
            schema = load_schema(args.schema_dir, "page-design-intent")
            errors.extend(validate_schema_subset(data, schema, path, args.strict))
            if isinstance(data, dict):
                page_design_intents.append((path, data))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    ppt_ir = loaded.get("ppt-ir", (None, None))[1]
    if "ppt-ir" in loaded:
        assets = loaded.get("assets", (None, None))[1]
        style = loaded.get("style", (None, None))[1]
        errors.extend(validate_ppt_ir_semantics(loaded["ppt-ir"][0], loaded["ppt-ir"][1], assets, style))
    if "style" in loaded:
        errors.extend(validate_style_semantics(loaded["style"][0], loaded["style"][1]))
    if "assets" in loaded:
        errors.extend(validate_asset_semantics(loaded["assets"][0], loaded["assets"][1], source_ids(ppt_ir or {})))
    if "diagram" in loaded:
        errors.extend(validate_diagram_semantics(loaded["diagram"][0], loaded["diagram"][1], "/", source_ids(ppt_ir or {})))
    if "build" in loaded:
        errors.extend(validate_build_semantics(loaded["build"][0], loaded["build"][1], loaded["build"][0].parent))
    if "qa" in loaded:
        errors.extend(validate_qa_semantics(loaded["qa"][0], loaded["qa"][1], ppt_ir))
    if "component-registry" in loaded:
        style = loaded.get("style", (None, None))[1]
        errors.extend(validate_component_registry_semantics(loaded["component-registry"][0], loaded["component-registry"][1], style))
    if "delivery" in loaded:
        errors.extend(validate_delivery_semantics(loaded["delivery"][0], loaded["delivery"][1], ppt_ir))
    if "build" in loaded and "delivery" in loaded:
        errors.extend(validate_build_delivery_semantics(loaded["build"][0], loaded["build"][1], loaded["delivery"][1]))
    for path, document in page_design_intents:
        errors.extend(validate_page_design_intent_semantics(path, document))

    if args.json_output:
        print(json.dumps({"ok": not errors, "issues": errors}, ensure_ascii=False, indent=2))
    elif errors:
        for item in errors:
            print(
                f"{item['file']} {item['pointer']} {item['code']}: "
                f"actual={item['actual_value']!r}; allowed={item['allowed_values']!r}; "
                f"repair={item['repair_suggestion']}",
                file=sys.stderr,
            )
    else:
        print("contract validation passed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
