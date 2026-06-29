---
name: color-converter
description: "Convert colors between HEX, RGB, RGBA, HSL, HSLA, and CSS color formats. Use when working with colors for web development, design, or styling tasks. Triggers on requests like: convert this color, what is HEX in RGB, show HSL values, format this for CSS."
---

# Color Converter

Convert colors between HEX, RGB, RGBA, HSL, HSLA formats.

## Supported Formats

- `HEX` - #RRGGBB or #RGB
- `RGB` - rgb(R, G, B)
- `RGBA` - rgba(R, G, B, A)
- `HSL` - hsl(H, S%, L%)
- `HSLA` - hsla(H, S%, L%, A)

## Usage

```bash
python scripts/color_converter.py <color> [--output FORMAT]
```

## Examples

```bash
# HEX to RGB
python scripts/color_converter.py "#3B82F6"
# Output: rgb(59, 130, 246)

# RGB to HSL
python scripts/color_converter.py "rgb(255, 99, 71)" --output hsl
# Output: hsl(9, 100%, 62%)

# HEX with alpha to RGBA
python scripts/color_converter.py "#3B82F680" --output rgba
# Output: rgba(59, 130, 246, 0.5)

# Named color
python scripts/color_converter.py "tomato"
# Output: rgb(255, 99, 71)
```

## Conversion Table

Common conversions for quick reference:

| HEX | RGB | HSL |
|-----|-----|-----|
| #FF0000 | rgb(255, 0, 0) | hsl(0, 100%, 50%) |
| #00FF00 | rgb(0, 255, 0) | hsl(120, 100%, 50%) |
| #0000FF | rgb(0, 0, 255) | hsl(240, 100%, 50%) |
| #FFFFFF | rgb(255, 255, 255) | hsl(0, 0%, 100%) |
| #000000 | rgb(0, 0, 0) | hsl(0, 0%, 0%) |
