---
name: color-toolkit
description: Convert, analyze, and generate colors from the CLI. Supports HEX, RGB, HSL, HSV, CMYK conversion, WCAG contrast ratio checking (AA/AAA compliance), palette generation (complementary, analogous, triadic, split-complementary, monochromatic), color manipulation (lighten/darken/saturate/desaturate), mixing, random generation, and CSS named color lookup. Use when the user needs color conversions, accessibility contrast checks, palette generation, or color manipulation. Zero external dependencies.
---

# Color Toolkit

Convert colors, check WCAG contrast, generate palettes, and manipulate colors. Pure Python, no dependencies.

## Quick Start

```bash
# Convert between formats (accepts #hex, rgb(), hsl(), CSS names, or r,g,b)
python3 scripts/color_toolkit.py convert '#ff6347'
python3 scripts/color_toolkit.py convert tomato
python3 scripts/color_toolkit.py convert 'rgb(52, 152, 219)'

# WCAG contrast check
python3 scripts/color_toolkit.py contrast '#333333' '#ffffff'

# Generate palettes
python3 scripts/color_toolkit.py palette '#3498db' -s triadic
python3 scripts/color_toolkit.py palette '#e74c3c' -s monochromatic -n 7

# Modify colors
python3 scripts/color_toolkit.py modify '#3498db' --op lighten --amount 20
python3 scripts/color_toolkit.py modify coral --op darken --amount 15

# Mix colors
python3 scripts/color_toolkit.py mix '#ff0000' '#0000ff' --weight 0.5

# Random colors
python3 scripts/color_toolkit.py random -n 5

# Search CSS named colors
python3 scripts/color_toolkit.py lookup green
```

## Commands

| Command | Description |
|---------|-------------|
| `convert` | Convert any color to HEX, RGB, HSL, HSV, and CMYK. |
| `contrast` | WCAG contrast ratio between foreground and background. Reports AA/AAA compliance. |
| `palette` | Generate palettes: `complementary`, `analogous`, `triadic`, `split-complementary`, `monochromatic`. |
| `modify` | Adjust color: `lighten`, `darken`, `saturate`, `desaturate`. `--amount 0-100`. |
| `mix` | Blend two colors. `--weight` controls the ratio (0.0 = all color1, 1.0 = all color2). |
| `random` | Generate random colors. `-n` sets count. |
| `lookup` | Search CSS named colors by partial name. |

All commands support `--json` for structured output.

## Accepted Color Formats

`#hex` (3 or 6 digit), `rgb(r, g, b)`, `hsl(h, s%, l%)`, `r,g,b`, or any CSS color name (e.g., `tomato`, `steelblue`, `coral`).
