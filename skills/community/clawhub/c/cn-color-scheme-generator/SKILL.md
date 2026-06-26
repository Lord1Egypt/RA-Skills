---
slug: cn-color-scheme-generator
name: Color Scheme Generator
version: "1.0.0"
description: "Generate color schemes from a base color. Support complementary, triadic, analogous schemes. Pure Python standard library, no API key required."
keywords: color, scheme, palette, design, complementary
license: MIT-0
tags:
  - tools
---

# Color Scheme Generator

Generate beautiful color palettes from a base color.

## Features

- Complementary color scheme (opposite on color wheel)
- Triadic color scheme (3 evenly spaced colors)
- Analogous color scheme (adjacent colors)
- Pure Python, no external dependencies

## Color Theory

- **Complementary**: Colors opposite each other on the color wheel. High contrast, vibrant combinations.
- **Triadic**: Three colors evenly spaced. Balanced and visually appealing.
- **Analogous**: Colors next to each other. Harmonious and natural-looking.

## Usage

```
python3 scripts/color_scheme.py --base "#ff5733"
```

## Example Output

```json
{
  "base": "#ff5733",
  "schemes": {
    "complementary": ["#ff5733", "#33d6ff"],
    "triadic": ["#ff5733", "#33ff57", "#5733ff"],
    "analogous": ["#ff5733", "#ffa033", "#ff3357"]
  }
}
```

## Use Cases

- UI/UX design
- Brand color palette creation
- Data visualization color schemes

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
