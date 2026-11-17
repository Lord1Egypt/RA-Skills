#!/usr/bin/env python3
"""P9 — Template extractor: build a v4 style pack from a user's own PPTX.

User's end goal is "DIY a deck that carries MY design sense". This script is
the entry point: point it at any PPTX (their own deck, a brand template, a
client deck) and it extracts the palette and type system, then emits a
complete v4 style pack (v3 style-contract v2.0 schema — the format the engine
and `style-validate` natively consume).

What is extracted (from the actual PPTX, by frequency):
  - text run colors        -> text_primary / text_secondary
  - text run font names    -> font_primary / font_secondary
  - shape fills / lines    -> primary / accent / background / surface_*
  - first-slide background -> background

What is NOT extracted (engine-owned, inherited from a base pack):
  grid, spacing, shape/shadow/card/table/chart/diagram/image/icon/footer
  tokens, density limits, allowed effects. These keep the deck renderable and
  QA-able; the user's identity comes through palette + type, which is what a
  "design sense" mostly is at the token level.

Usage:
  python3 scripts/template_from_pptx.py --pptx user-deck.pptx \
      --style-id my-brand --display-name "My Brand" \
      --output styles/my-brand.json
  # then: python3 -m engine style-validate --style styles/my-brand.json
  # then: python3 -m engine compile --source doc:markdown:source.md \
  #        --style styles/my-brand.json --output-dir out/
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Base pack whose engine-owned tokens are inherited. consulting-light is the
# engine's default visual system for report/proposal contexts.
DEFAULT_BASE = ROOT / "styles" / "consulting-light.json"

# Severity tiers for color assignment.
_BG_CANDIDATES = {"FBFBF8", "FFFFFF", "F1EFEA", "F2EADF", "FBF8F1", "F7F7F5"}


def _hex(rgb) -> str:
    """python-pptx RGBColor -> '#RRGGBB'."""
    return f"#{str(rgb)}"


def extract_palette(pptx_path: Path) -> dict:
    """Scan a PPTX and return frequency counters of text/fill/line colors and fonts."""
    from pptx import Presentation

    prs = Presentation(str(pptx_path))
    text_colors: Counter[str] = Counter()
    fill_colors: Counter[str] = Counter()
    line_colors: Counter[str] = Counter()
    fonts: Counter[str] = Counter()
    slide_bg: Counter[str] = Counter()

    def rgb_of(color) -> str | None:
        try:
            if color and color.type is not None and getattr(color, "rgb", None):
                return _hex(color.rgb)
        except Exception:
            return None
        return None

    for slide in prs.slides:
        # slide-level background
        try:
            bg = slide.background
            if bg.fill.type is not None:
                try:
                    if str(bg.fill.type) == "MSO_FILL_TYPE.SOLID (1)":
                        slide_bg[rgb_of(bg.fill.fore_color)] += 1
                except Exception:
                    pass
        except Exception:
            pass

        for shape in slide.shapes:
            # text runs -> color + font
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        c = rgb_of(run.font.color)
                        if c:
                            text_colors[c] += 1
                        if run.font.name:
                            fonts[run.font.name] += 1
            # shape fill
            try:
                if shape.fill.type is not None and str(shape.fill.type) == "MSO_FILL_TYPE.SOLID (1)":
                    c = rgb_of(shape.fill.fore_color)
                    if c:
                        fill_colors[c] += 1
            except Exception:
                pass
            # shape line
            try:
                if shape.line and shape.line.fill.type is not None and \
                        str(shape.line.fill.type) == "MSO_FILL_TYPE.SOLID (1)":
                    c = rgb_of(shape.line.color)
                    if c:
                        line_colors[c] += 1
            except Exception:
                pass

    return {
        "text_colors": text_colors,
        "fill_colors": fill_colors,
        "line_colors": line_colors,
        "fonts": fonts,
        "slide_bg": slide_bg,
    }


def assign_colors(extracted: dict, base_colors: dict | None = None) -> dict:
    """Map frequency counters to v4 color tokens."""
    base_colors = base_colors or {}
    text = extracted["text_colors"]
    fill = extracted["fill_colors"]
    line = extracted["line_colors"]
    bg_counter = extracted["slide_bg"]

    # background: prefer the slide-level background, else the most common
    # near-white fill / text color that appears on background.
    background = None
    if bg_counter:
        background = bg_counter.most_common(1)[0][0]
    if not background:
        # most common fill that is light
        light_fills = [c for c, _ in fill.most_common(10) if _is_light(c)]
        background = light_fills[0] if light_fills else "#FFFFFF"

    # text_primary / text_secondary: the most common DARK text colors.
    # White runs are white-on-dark (labels on filled cards), not body text —
    # picking them as text_primary would set body copy to white on a white page.
    text_sorted = [c for c, _ in text.most_common()]
    dark_text = [c for c in text_sorted if not _is_light(c)]
    text_primary = dark_text[0] if dark_text else "#2A2E35"
    text_secondary = dark_text[1] if len(dark_text) > 1 else _darken(text_primary, 0.72)

    # primary = most common non-light fill (brand color), else a strong text color.
    dark_fills = [c for c, _ in fill.most_common(8) if not _is_light(c)]
    primary = dark_fills[0] if dark_fills else _darken(text_primary, 0.75)
    accent_candidates = [c for c, _ in fill.most_common(12) if c != primary and not _is_light(c)]
    accent = accent_candidates[0] if accent_candidates else _lighten(primary)

    # surfaces: light fills distinct from background.
    light_fills = [c for c, _ in fill.most_common(12) if _is_light(c) and c != background]
    surface_1 = light_fills[0] if light_fills else _lighten(background, 0.94)
    # surface_2 must be visibly distinct from surface_1 for the layered look;
    # if the template only used one light fill, derive a slightly darker tone.
    surface_2 = light_fills[1] if len(light_fills) > 1 else _darken(surface_1, 0.97)
    if surface_2 == surface_1:
        surface_2 = _darken(surface_1, 0.96)

    # semantic positive/warning/negative: keep base defaults (rarely in templates)
    border = _lighten(surface_1, 0.88) if light_fills else _lighten(text_primary, 0.25)

    # data_series: derive from the extracted palette so charts inherit the
    # user's identity rather than the base pack's.
    data_series = [
        primary, accent,
        base_colors.get("positive", "#4E7358"),
        base_colors.get("warning", "#A66A2C"),
    ]

    return {
        "primary": primary,
        "accent": accent,
        "background": background,
        "surface_1": surface_1,
        "surface_2": surface_2,
        "text_primary": text_primary,
        "text_secondary": text_secondary,
        "border": border,
        "data_series": data_series,
        # keep base semantic colors; user template rarely defines these
    }


def assign_fonts(extracted: dict) -> dict:
    """Map font frequency to font_primary/font_editorial stacks.

    The v3 style-contract schema declares `font_primary`, `font_editorial`
    and `font_mono` (no `font_secondary`). `font_editorial` is the engine's
    second font slot (used for cover/quote/editorial text).
    """
    fonts = extracted["fonts"]
    ordered = [f for f, _ in fonts.most_common() if f]
    primary = ordered[0] if ordered else "Calibri"
    editorial = ordered[1] if len(ordered) > 1 else primary
    # ensure a CJK-capable fallback is present so zh decks don't break
    cjk = ["PingFang SC", "Microsoft YaHei", "Source Han Sans SC", "Noto Sans CJK SC"]
    return {
        "font_primary": [primary, *cjk],
        "font_editorial": [editorial, *cjk],
        "font_mono": ["Menlo", "Consolas", "Courier New"],
    }


def _is_light(hex_color: str) -> bool:
    """Heuristic: is this color light (relative luminance > 0.55)?"""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return lum > 0.55
    except Exception:
        return False


def _darken(hex_color: str, factor: float = 0.7) -> str:
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f"#{r:02X}{g:02X}{b:02X}"
    except Exception:
        return "#2A2E35"


def _lighten(hex_color: str, factor: float = 0.75) -> str:
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r = int(r + (255 - r) * (1 - factor))
        g = int(g + (255 - g) * (1 - factor))
        b = int(b + (255 - b) * (1 - factor))
        return f"#{r:02X}{g:02X}{b:02X}"
    except Exception:
        return "#FFFFFF"


def build_pack(pptx_path: Path, style_id: str, display_name: str,
               base_path: Path = DEFAULT_BASE, description: str = "") -> dict:
    """Extract from PPTX and produce a complete v4 style pack."""
    extracted = extract_palette(pptx_path)

    base = json.loads(base_path.read_text(encoding="utf-8"))
    if base.get("schema_version") != "2.0":
        raise ValueError(f"base pack must be schema_version 2.0, got {base.get('schema_version')}")

    colors = assign_colors(extracted, base_colors=base.get("colors", {}))
    fonts = assign_fonts(extracted)

    pack = dict(base)  # deep-enough copy of engine-owned tokens
    pack.update({
        "style_id": style_id,
        "display_name": display_name,
        "description": description or f"Auto-extracted from {pptx_path.name}",
    })
    # override palette + type with user-derived values
    pack["colors"] = dict(base["colors"])
    pack["colors"].update(colors)
    pack["typography"] = dict(base["typography"])
    pack["typography"].update(fonts)

    # provenance so the pack is auditable
    pack.setdefault("extensions", {})["template_from_pptx"] = {
        "source_pptx": str(pptx_path),
        "extracted_colors": extracted["text_colors"].most_common(6),
        "extracted_fonts": fonts,
        "extractor_version": "0.1.0",
    }
    return pack


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pptx", required=True, help="User PPTX to extract template from")
    ap.add_argument("--style-id", required=True, help="style_id for the new pack (kebab-case)")
    ap.add_argument("--display-name", required=True, help="Human-readable pack name")
    ap.add_argument("--output", required=True, help="Output style pack path")
    ap.add_argument("--description", default="", help="Optional description")
    ap.add_argument("--base", default=str(DEFAULT_BASE), help="Base pack to inherit engine tokens from")
    args = ap.parse_args(argv)

    pptx_path = Path(args.pptx)
    if not pptx_path.exists():
        print(f"error: pptx not found: {pptx_path}", file=sys.stderr)
        return 2

    pack = build_pack(pptx_path, args.style_id, args.display_name,
                      base_path=Path(args.base), description=args.description)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {out}")
    print(f"  style_id:     {args.style_id}")
    print(f"  display_name: {args.display_name}")
    print(f"  colors:       primary={pack['colors']['primary']} background={pack['colors']['background']} "
          f"text={pack['colors']['text_primary']}")
    print(f"  fonts:        {pack['typography']['font_primary'][0]} / "
          f"{pack['typography']['font_editorial'][0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
