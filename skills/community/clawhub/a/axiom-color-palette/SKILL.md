---
name: axiom-color-palette
description: Color palette extractor — extract dominant colors from an image (PNG/JPEG/GIF). Use when you need a color palette for design or analysis. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-color-palette

**Version:** 0.1.2
**Axioma Tools**

Extracts the dominant color palette from an image using frequency analysis.

## What this skill does

- Frequency-based color extraction
- Configurable palette size (3-16 colors)
- Optional K-means clustering
- Outputs hex codes + RGB tuples
- JSON output for design tools

## When to use this skill

- ✅ Generate palette for website redesign
- ✅ Find dominant brand colors in an image
- ✅ Analyze color trends in design portfolios
- ❌ Convert color spaces (use colormath)
- ❌ Render images (use Pillow)

## Usage

```bash
python3 axiom_color_palette.py logo.png --colors 5
python3 axiom_color_palette.py photo.jpg --json > palette.json
```

```python
from axiom_color_palette import extract_palette
colors = extract_palette('image.png', n_colors=5)
# [('#FF5733', 42), ('#33FF57', 28), ...]
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 15+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
