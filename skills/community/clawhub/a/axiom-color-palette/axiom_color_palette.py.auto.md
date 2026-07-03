# 📄 `axiom_color_palette.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-color-palette/axiom_color_palette.py`  
**Size:** 6,889 bytes / 221 lines  
**Hash:** `99f7237bcac0e407`  
**Generated:** 2026-06-15T03:00:47.187212+00:00

## 📝 Module Docstring

```
🛠️ axiom-color-palette — Color Palette Generator
=================================================

Skill Axiome #14 (Phase 4 — Extraction)

⚠️ LIMITATIONS CONNUES :
- Pas d'extraction depuis image (utiliser PIL pour ça)
- Pas de gestion d'alpha (RGB seulement)
- Pas de WCAG accessibility scoring (à ajouter)

GÉNÈRE DES HARMONIES DE COULEURS À PARTIR D'UNE COULEUR DE BASE
```

## 📦 Imports (5)

```python
import colorsys
import re
import sys
import argparse
import json
```

## ⚡ Functions (16)

### `def parse_hex(hex_str):`
> Parse a hex color string to (r, g, b) tuple (0-255).

### `def to_hex(rgb):`
> Convert (r, g, b) tuple to #RRGGBB string.

### `def to_rgb_string(rgb):`
> Convert to 'rgb(r, g, b)' string.

### `def hsl(rgb):`
> Convert (r, g, b) to (h, s, l) where h is 0-360, s and l are 0-100.

### `def to_hsl_string(rgb):`
> Convert to 'hsl(h, s%, l%)' string.

### `def rotate_hue(rgb, degrees):`
> Rotate hue by N degrees.

### `def adjust_lightness(rgb, delta):`
> Adjust lightness by delta (positive = lighter, negative = darker).

### `def complementary(rgb):`
> Complementary color (opposite on color wheel).

### `def analogous(rgb):`
> Analogous colors (adjacent on color wheel).

### `def triadic(rgb):`
> Triadic colors (120° apart).

### `def tetradic(rgb):`
> Tetradic / square colors (90° apart).

### `def split_complementary(rgb):`
> Split-complementary (180° ± 30°).

### `def monochromatic(rgb, count):`
> Monochromatic palette (same hue, varying lightness).

### `def generate(base_color, harmony):`
> Generate a color palette from a base color.

Args:
    base_color: hex string like "#FF5500" or "FF5500"
    harmony: complementary, analogous, triadic, tetradic, split_complementary, monochromatic

R

### `def to_css(palette, format):`
> Format a palette as CSS custom properties.

### `def main():`
