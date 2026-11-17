#!/usr/bin/env python3
"""Migrate a v3 style contract to a Style Contract v4 data pack (P5).

Best-effort mechanical mapping: token values copy over, geometry fields
(grid/density_limits/safe zones) are dropped by design (engine-owned in
v4), numeric values are clamped into the v4 hard floors, and skin color
references that are not valid palette token names are dropped rather
than guessed. The result is validated against the frozen v4 schema
before it is written — an invalid migration never lands on disk.

Usage:
  python3 scripts/migrate_style_v3_to_v4.py --input v3.json --output pack.json
  python3 scripts/migrate_style_v3_to_v4.py --builtin   # migrate shipped fixtures
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_contracts  # noqa: E402

TOKEN_NAMES = {"primary", "accent", "background", "surface_1", "surface_2", "surface_3",
               "text_primary", "text_secondary", "text_muted", "border",
               "positive", "warning", "negative"}

BUILTIN_KNOBS = {
    "editorial-knowledge": {"density": "airy", "margin_scale": 1.1, "alignment": "left"},
    "consulting-light": {"density": "regular", "margin_scale": 1.0, "alignment": "left"},
    "technical-blueprint": {"density": "compact", "margin_scale": 0.95, "alignment": "left"},
    "product-report": {"density": "regular", "margin_scale": 1.0, "alignment": "left"},
    "consulting-blueprint-hybrid": {"density": "regular", "margin_scale": 1.0,
                                    "alignment": "left"},
}


def _clamp(value, lo, hi, default):
    try:
        return min(max(float(value), lo), hi)
    except (TypeError, ValueError):
        return default


def _token_ref(value):
    return value if value in TOKEN_NAMES else None


def migrate(v3: dict) -> dict:
    colors_in = v3.get("colors", {})
    colors = {k: v for k, v in colors_in.items()
              if k in TOKEN_NAMES | {"data_series", "allowed_opacity"}}

    typo_in = v3.get("typography", {})
    titles = typo_in.get("title_sizes_pt", {})
    bodies = typo_in.get("body_sizes_pt", {})
    metrics = typo_in.get("metric_sizes_pt", {})
    line_h = typo_in.get("line_height", {})
    typography = {
        "font_primary": (typo_in.get("font_primary") or ["Calibri"])[:8],
        "title_sizes_pt": {
            "cover": _clamp(titles.get("cover"), 24, 60, 34),
            "section": _clamp(titles.get("section"), 20, 48, 28),
            "slide": _clamp(titles.get("slide"), 16, 36, 22),
        },
        "body_sizes_pt": {
            "large": _clamp(bodies.get("large"), 13, 24, 16),
            "normal": _clamp(bodies.get("normal"), 11, 18, 13),
            "small": _clamp(bodies.get("small"), 9.5, 14, 10),
            "footnote": _clamp(bodies.get("footnote"), 8, 11, 8.5),
        },
        "metric_sizes_pt": {
            "hero": _clamp(metrics.get("hero"), 22, 64, 30),
            "normal": _clamp(metrics.get("normal"), 16, 40, 22),
        },
        "line_height": {
            "title": _clamp(line_h.get("slide_title"), 0.95, 1.4, 1.1),
            "body": _clamp(line_h.get("body"), 1.15, 1.8, 1.35),
            "caption": _clamp(line_h.get("caption"), 1.1, 1.6, 1.25),
        },
    }
    for key in ("font_editorial", "font_mono"):
        if typo_in.get(key):
            typography[key] = typo_in[key][:8]
    weights = typo_in.get("weights", {})
    if weights:
        typography["weights"] = {
            k: int(_clamp(round(weights.get(k, d) / 100) * 100, 100, 900, d))
            for k, d in (("regular", 400), ("medium", 500),
                         ("semibold", 600), ("bold", 700)) if k in weights}

    shape_in = v3.get("shape_tokens", {})
    shape = {"card_radius_pt": _clamp(shape_in.get("card_radius_pt"), 0, 24, 8),
             "border_width_pt": _clamp(shape_in.get("border_width_pt"), 0.25, 3, 0.8)}
    for key, lo, hi, default in (("small_radius_pt", 0, 16, 4),
                                 ("pill_radius_pt", 0, 999, 999),
                                 ("emphasis_border_width_pt", 0.5, 4, 1.5),
                                 ("divider_width_pt", 0.25, 2, 0.6),
                                 ("connector_width_pt", 0.75, 3, 1.2)):
        if key in shape_in:
            shape[key] = _clamp(shape_in.get(key), lo, hi, default)

    tokens = {"colors": colors, "typography": typography, "shape": shape}

    shadow_in = (v3.get("shadow_tokens") or {}).get("floating_panel") or {}
    if shadow_in.get("enabled"):
        tokens["shadow"] = {"levels": [{
            "blur_pt": _clamp(shadow_in.get("blur_pt"), 0, 24, 4),
            "offset_pt": _clamp(shadow_in.get("distance_pt"), 0, 12, 2),
            "opacity": _clamp(shadow_in.get("opacity"), 0, 0.35, 0.12),
        }]}

    skins: dict = {}
    card_in = (v3.get("card_tokens") or {}).get("default") or {}
    card = {k: v for k, v in (("fill", _token_ref(card_in.get("fill"))),
                              ("text_color", _token_ref(card_in.get("text_color"))),
                              ("border_color", _token_ref(card_in.get("border_color"))))
            if v}
    if card:
        card["variant"] = "tinted" if card.get("fill", "").startswith("surface") else "flat"
        skins["card"] = card
    table_in = v3.get("table_tokens") or {}
    table = {}
    if _token_ref(table_in.get("header_fill")):
        table["header_fill"] = table_in["header_fill"]
        table["header_style"] = "filled"
    if isinstance(table_in.get("zebra"), bool):
        table["zebra"] = table_in["zebra"]
    if table:
        skins["table"] = table
    skins.setdefault("kpi", {"variant": "plain", "value_color": "primary"})
    skins["footer"] = {"show_source": True, "show_page_number": True,
                       "text_color": "text_secondary"}

    style_id = v3.get("style_id", "migrated-style")
    pack = {
        "schema_version": "4.0.0",
        "pack": {
            "pack_id": style_id,
            "version": "4.0.0",
            "display_name": v3.get("display_name", style_id),
            "description": (v3.get("description") or "")[:500],
            "publisher": "MeowClaw PPT Smith",
            "license": {"type": "open", "spdx": "Apache-2.0"},
            "engine_compat": ">=4.0 <5",
            "compatibility_aliases": [style_id],
        },
        "tokens": tokens,
        "skins": skins,
        "layout_knobs": BUILTIN_KNOBS.get(
            style_id, {"density": "regular", "margin_scale": 1.0, "alignment": "left"}),
    }
    return pack


def migrate_file(input_path: Path, output_path: Path) -> list:
    pack = migrate(json.loads(input_path.read_text(encoding="utf-8")))
    schema = json.loads(
        (ROOT / "schemas/v4/style-contract-v4.schema.json").read_text(encoding="utf-8"))
    errors = validate_contracts.validate_schema_subset(pack, schema, output_path, True)
    if errors:
        for e in errors[:10]:
            print(f"  {e['pointer']}: {e['code']}", file=sys.stderr)
        return errors
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--builtin", action="store_true")
    args = parser.parse_args()

    if args.builtin:
        failed = False
        for fixture in sorted((ROOT / "tests/fixtures/styles").glob("*.json")):
            out = ROOT / "styles" / fixture.name
            errors = migrate_file(fixture, out)
            print(f"{fixture.stem}: {'FAIL' if errors else 'ok -> ' + str(out.relative_to(ROOT))}")
            failed = failed or bool(errors)
        return 1 if failed else 0

    if not args.input or not args.output:
        parser.error("--input/--output or --builtin required")
    errors = migrate_file(Path(args.input), Path(args.output))
    print("FAIL" if errors else "ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
