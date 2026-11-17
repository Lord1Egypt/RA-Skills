# Graphic & Print Design Color Guide

> This guide establishes engineering color standards for **graphic design, editorial posters, packaging, brand collateral, and physical prepress printing** within the `color-system` skill.

---

## 1. Color Models & Cross-Medium Conversion

### 1.1 RGB ➜ CMYK Gamut Clipping (The Out-of-Gamut Problem)

- **Physical Nature**: Screen emissions operate via the additive RGB color model (wide gamut). Physical ink on paper operates via the subtractive CMYK color model (narrower gamut).
- **High-Risk Gamut Clipping Zones**:
  - High-chroma fluorescent greens and vibrant limes (RGB greens collapse into dull olive/moss greens in CMYK).
  - High-purity electric blues and cyans (`#0066FF` shifts to dark purplish navy in standard four-color printing).
  - Fluorescent magentas, bright neon pinks, and ultra-saturated oranges.
- **Engineering Rules**:
  1. Print materials must be designed from inception in **CMYK color space** (`FOGRA39` or `Japan Color 2001 Coated`).
  2. For visual identity marks or key packaging brand moments that demand ultra-high saturation, **always specify a Pantone Spot Color** instead of four-color CMYK process simulation.

### 1.2 Pantone Matching System (PMS) Standards

| Color Category | Example Code | Ideal Application | Prepress & Finishing Notes |
|---|---|---|---|
| **Solid Coated (C)** | `PANTONE 186 C` | Coated art paper, cast-coated paper, glossy packaging | Glossy surface, maximum fidelity to standard swatch book |
| **Solid Uncoated (U)** | `PANTONE 186 U` | Offset woodfree paper, kraft paper, textured stationery | Fiber absorption dulls ink; always check against U swatch book |
| **Metallic (Silver/Gold)** | `PANTONE 877 C` (Silver) / `871 C` (Gold) | Luxury packaging, annual reports, premium certificates | High opacity metallic flakes; matte/gloss lamination slightly reduces sheen |
| **Fluorescent / Neons** | `PANTONE 801 C` (Neon Blue) / `805 C` (Neon Orange) | Streetwear posters, event collateral, youth packaging | Physically unachievable with 4-color CMYK; requires dedicated fifth plate |

---

## 2. Prepress Standards & Ink Formulations

### 2.1 Black Ink Standards (Prepress Rule #1)

| Black Formulation | Recommended CMYK Values | Target Usage | Failure Modes to Avoid |
|---|---|---|---|
| **Standard Black (Pure Black)** | `C:0 M:0 Y:0 K:100` | Body copy text (≤24pt), fine rules (≤1pt), barcodes, QR codes | **NEVER** use Pure Black for large solid background fills (will appear washed out, greyish, or translucent). |
| **Rich Black (Four-Color Black)** | `C:30 M:20 Y:20 K:100` or `C:40 M:30 Y:0 K:100` | Large background blocks, poster fields, deep solid borders | **NEVER** use Rich Black on small typography (press registration variance causes fuzzy multi-color halos). |
| **Cool Rich Black** | `C:40 M:10 Y:0 K:100` | Tech/industrial branding, stark contemporary posters | Deep midnight tone with subtle cold elegance. |
| **Warm Rich Black** | `C:10 M:30 Y:30 K:100` | Editorial publications, luxury, retro/heritage pieces | Deep velvety tone with warm organic depth. |
| **Total Ink Limit (TIC / TAC)** | **Sum must NEVER exceed 300%** (e.g., `C:100 M:100 Y:100 K:100 = 400%` is an absolute failure) | — | Excessive ink thickness causes drying failure, smearing, offset marking on reverse sheets, and paper warping. |

### 2.2 Paper Substrate & Dot Gain Compensation

| Substrate Category | Typical Examples | Physical Characteristics | Prepress Compensation Rules |
|---|---|---|---|
| **Coated Art Paper (铜版纸)** | Gloss/Silk Art paper (157g/200g/250g), Coated Ivory cardstock | Smooth non-porous coating; low ink absorption; small dot gain (~10%-15%). | High sharpness and dynamic range. Output artwork at default profiles without artificial brightness boosts. |
| **Uncoated Woodfree (双胶纸/道林纸)** | Bond paper, letterhead stock, offset book paper (80g-140g) | Porous plant fibers; rapid absorption; high dot gain (~20%-25%). | Inks darken and soften. Shadows tend to clog into muddy blocks. Prepress compensation: lift overall curve brightness by +5%~10% and expand shadow detail. |
| **Specialty & Textured Paper (特种纸)** | Laid paper, cotton rag, metallic pearl, tracing paper | Natural warm/cream tinted base or textured surface reflections. | Paper tint shows through light areas. For pure white or vibrant solid coverage, **print a dedicated opaque white ink underprint (`白墨打底`) first**. |
| **Kraft & Corrugated (牛皮纸/瓦楞纸)** | Brown kraft, recycled cardboard | Dark earthy base; very low contrast. | Avoid fine photographic halftones. Best paired with **solid single black, opaque spot white, or high-saturation warm spot inks (Gold, Red)**. |

---

## 3. Graphic Layout Harmony & Emotion Matrix

### 3.1 The 60-30-10 Golden Composition Rule

For posters, editorial covers, brochures, and packaging, allocate surface visual weight across three distinct tiers:

```
┌─────────────────────────────────────────────────────────────┐
│ 60% Dominant Base (Canvas & Negative Space)                 │
│ - Overall background tint, broad structural negative space  │
│ - Sets emotional temperature, provides optical breathing room│
├──────────────────────────────┬──────────────────────────────┤
│ 30% Secondary Structure      │ 10% Visual Accent Hook       │
│ - Major illustration, headline│ - Call-to-action seal, focal │
│   typography, modular cards   │   emblem, spot foil, break   │
└──────────────────────────────┴──────────────────────────────┘
```

### 3.2 Industry & Category Palette Matrix

| Industry / Sector | Dominant Chromatic Tone | Classic 60-30-10 Formula | Psychological Signaling |
|---|---|---|---|
| **Food & Beverage (食品餐饮)** | Warm tones, appetite reds, warm ambers, fresh greens | Base: Creamy Linen (60%) + Subject: Warm Terracotta (30%) + Accent: Golden Mustard (10%) | Stimulates digestive response, warmth, freshness, artisanal care. |
| **Technology & Industrial (科技工业)** | Deep space graphite, cold slate, precision cyan/cobalt | Base: Deep Slate / Pure White (60%) + Structure: Technical Navy (30%) + Accent: Electric Cyan (10%) | Rationality, engineering precision, reliability, forward momentum. |
| **Luxury & Heritage (高端奢品)** | Deep forest, charcoal, sand, metallic bronze/gold | Base: Obsidian Black / Jade (60%) + Structure: Muted Sand (30%) + Accent: Metallic Foil Gold (10%) | Restraint, mystique, heritage value, timeless pricing power. |
| **Wellness & Care (健康母婴)** | Calming pastels, low-contrast sage, soft oatmeal | Base: Soft Oatmeal (60%) + Structure: Dusty Rose / Mist Blue (30%) + Accent: Sage Green (10%) | Non-aggressive, biological safety, gentleness, therapeutic calm. |
| **Urban & Cultural (先锋文创/国潮)** | High-contrast clashes, mineral tones, lacquer black | Base: Mineral Black / Raw Xuan White (60%) + Structure: Vermilion Red / Azurite (30%) + Accent: Lemon Yellow / Gold (10%) | Cultural pride, visual tension, bold avant-garde memory hook. |

---

## 4. Graphic Color Deliverable Specification Format

When outputting color systems for print collateral or brand identity manuals, generate the specification using the standard table below:

```markdown
### [System / Palette Name] Print & Graphic Color Specification

| Role | Color Name | HEX / RGB | CMYK (FOGRA39) | Pantone Spot | Substrate & Application Notes |
|---|---|---|---|---|---|
| Dominant (60%) | [Name] | `#HEX` / `R,G,B` | `C:__ M:__ Y:__ K:__` | `PANTONE ___ C/U` | Canvas / background cardstock; check paper tone |
| Secondary (30%) | [Name] | `#HEX` / `R,G,B` | `C:__ M:__ Y:__ K:__` | `PANTONE ___ C/U` | Primary headline typography & structural graphics |
| Accent (10%) | [Name] | `#HEX` / `R,G,B` | `C:__ M:__ Y:__ K:__` | `PANTONE ___ C/U` | Focal hook, brand badge, hot foil / spot UV plate |
| Body Text Black | Standard Black | `#000000` / `0,0,0` | `C:0 M:0 Y:0 K:100` | — | Text ≤24pt, barcodes; strictly no rich black mixing |
```
