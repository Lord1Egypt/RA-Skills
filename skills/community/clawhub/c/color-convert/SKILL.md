---
name: color-toolkit
description: Color conversion (HEX/RGB/HSL/HSV/CMYK), palette generation (complementary, analogous, triadic, split-complementary, shades), WCAG contrast ratio checking, and CSS variable export. Pure Python, zero dependencies. GitHub: https://github.com/darbling/clawhub-skills 当用户需要颜色转换、配色方案、对比度检查、调色板生成时触发。
---

# 🎨 Color Toolkit

**Author: Lin Hui** | [GitHub](https://github.com/darbling/clawhub-skills) | MIT License | v1.0.0

Every color tool you need. Convert between formats, generate harmonious palettes, check accessibility contrast, and export CSS variables.

## ✨ Features

- **Convert** — HEX ↔ RGB ↔ HSL ↔ HSV ↔ CMYK
- **Palettes** — Complementary, analogous, triadic, split-complementary, shades/tints
- **Contrast** — WCAG 2.1 contrast ratio and AA/AAA compliance
- **Named colors** — 148 CSS named colors lookup
- **CSS export** — Generate CSS custom properties from any palette
- **Random** — Generate random harmonious palettes

## 🚀 Usage

```
Convert #FF5733 to HSL
```
```
Generate a complementary palette for #3498DB
```
```
Check WCAG contrast ratio between #FFFFFF and #333333
```
```
Show me 5 shades of #E74C3C from light to dark
```
```
Generate a triadic color scheme and export as CSS variables
```

## ⚙️ Technical Details

- **Runtime**: Python 3.6+
- **Dependencies**: Zero (stdlib only: math, random, colorsys)
- **Formats**: HEX, RGB, HSL, HSV, CMYK
- **Standards**: WCAG 2.1 contrast ratio (AA 4.5:1, AAA 7:1)
