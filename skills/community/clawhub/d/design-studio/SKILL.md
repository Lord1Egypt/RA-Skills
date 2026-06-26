---
name: design-studio
description: Professional design studio for creating covers, banners, avatars, logos, mockups, portfolios and GIF animations. Use when you need to create designs for freelance platforms (Fiverr, Kwork, Upwork), generate social media banners, check design quality, add watermarks, batch-generate covers from CSV, or pick color palettes and font pairings.
version: 1.0.1
author: mosoonpi-ai
license: MIT
tags: design, graphics, banners, covers, logos, avatars, mockups, gif, pillow, imagemagick, svg
---

# Design Studio — Professional Design Skill for OpenClaw

## What You Get

- ⏱️ **30 seconds per cover** instead of 2 hours in Canva or Figma
- 📊 **Auto quality scoring** (1-10) — stop guessing if your design is good enough
- 📦 **Batch-generate 50+ covers** from a CSV in one command
- 🔄 **A/B test 4 variants** instantly — pick the winner by score, not gut feeling
- 🎬 **Animated GIF banners** — no After Effects needed
- 📱 **Device mockups** in seconds — laptop, phone, tablet, any device
- 💧 **Watermarking** — protect your work in tile, corner, or center mode

## When to Use

Activate this skill when you need to:
- Create **covers** for freelance profiles (Fiverr, Kwork, Upwork, Freelance.ru)
- Generate **banners** for social media, channels, repos
- Design **logos** (text-based, icon, combined)
- Build **portfolio cards** or presentations
- Create **avatars** (initials, abstract, brand)
- Prepare **UI mockups** or visual prototypes
- Check design quality with automated scoring

## Available Tools

| Tool | Purpose | Command |
|---|---|---|
| **Pillow** (Python) | Raster graphics, banners, avatars | `python3 -c "from PIL import Image"` |
| **ImageMagick** | Convert, effects, compositing | `convert`, `magick` |
| **svgwrite** (Python) | SVG generation | `python3 -c "import svgwrite"` |
| **CairoSVG** (Python) | SVG → PNG/PDF rendering | `python3 -c "import cairosvg"` |
| **Inkscape** | SVG editing (CLI) | `inkscape --export-type=png` |
| **GIMP** | Advanced raster processing (CLI) | `gimp -i -b '(script-fu ...)'` |
| **fonttools** (Python) | Font metrics and kerning | `python3 -c "from fontTools.ttLib import TTFont"` |

## Fonts

Find system fonts:
```bash
fc-list : family | grep -i "name"
fc-match --format="%{file}\n" "PT Sans:Bold"
```

Recommended Cyrillic: PT Sans/Serif, Roboto, Open Sans, Montserrat, DejaVu Sans.

## Scripts (12)

**Basic:**
- `scripts/generate_banner.py` — banners (size, palette, style, fonts)
- `scripts/generate_avatar.py` — avatars (gradient/flat/circle, 1024x1024)
- `scripts/check_design.py` — auto quality scoring (contrast, balance, palette → 1-10)

**Marketplace covers:**
- `scripts/generate_marketplace_cover.py` — Fiverr (1280×769), Kwork (1200×800), Freelance.ru, Upwork (1584×396)

**Advanced:**
- `scripts/mockup_generator.py` — device mockups (laptop/phone/tablet/monitor/hand_phone)
- `scripts/design_pipeline.py` — full pipeline: generate → check → auto-improve → final
- `scripts/generate_svg_library.py` — SVG library (23 elements: icons, badges, frames)

**Batch & effects:**
- `scripts/ab_variants.py` — A/B test: 4 cover variants with different palettes + score comparison
- `scripts/generate_gif_banner.py` — animated GIF banners (fade_in/slide/pulse/typewriter)
- `scripts/watermark.py` — watermarks (bottom_right/center/tile)
- `scripts/batch_generate.py` — mass cover generation from CSV file

**SVG library** (references/svg_elements/): 10 icons, 5 badges, 5 shapes, 3 frames — ready to embed.

## Print & Document Design

Also supports brochures, catalogs, and multi-page docs via Scribus, LaTeX, Typst, WeasyPrint, Pandoc, LibreOffice.

## Workflow

1. **Brief** — define task, audience, style
2. **Palette** — choose from `references/color-palettes.md` (20 curated palettes)
3. **Fonts** — pick a pair from `references/font-pairings.md` (15 tested pairs)
4. **Rules** — follow `references/design-rules.md`
5. **Create** — use scripts or tools directly
6. **Check** — run `scripts/check_design.py`
7. **Iterate** — fix by recommendations, re-check

## References

- `references/design-rules.md` — professional design rules
- `references/color-palettes.md` — 20 curated color palettes
- `references/font-pairings.md` — 15 tested font pairings
