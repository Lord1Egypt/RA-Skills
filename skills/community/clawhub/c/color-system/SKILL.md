---
name: color-system
version: "0.2.0"
license: Apache-2.0
description: "Comprehensive multi-domain color design system — covering both digital product UI (semantic CSS color tokens, dark/light mode, WCAG AA contrast) and graphic/print design (CMYK/Pantone specs, print paper absorption & spot colors, 60-30-10 harmony rules, emotional poster & packaging palettes). Use when: configuring color tokens, generating tokens.css, designing dark/light mode palettes, or determining CMYK/Pantone colors for graphic, poster, and packaging print materials. Keywords: color system, 色彩系统, 配色方案, color tokens, dark mode, light mode, 平面设计配色, 印刷色彩, CMYK, Pantone, 包装配色, 海报配色."
metadata:
  openclaw:
    emoji: 🎨
---

# Color System — Multi-Domain Color Architecture

> Comprehensive color design system governing both digital product interfaces (Web/App tokens & theming) and graphic/print media (CMYK/Pantone & prepress standards).

---

## Architecture Overview

This skill operates across two specialized domains depending on the user's medium:

```
                      ┌─────────────────────────┐
                      │      color-system       │
                      │ Multi-Domain Color Core │
                      └────────────┬────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ Domain 1: Digital UI & Tokens   │ │ Domain 2: Graphic & Print Media │
│ • Semantic CSS vars (tokens.css)│ │ • CMYK (FOGRA39) & Pantone Spot │
│ • Auto Light/Dark mode switching│ │ • 60-30-10 Rule & Emotion Matrix│
│ • WCAG AA (≥4.5:1 / ≥3:1) check │ │ • Pure K100 vs Rich Black (TIC) │
│ • 7 Curated Palettes + Custom   │ │ • Substrate dot gain absorption │
└─────────────────────────────────┘ └─────────────────────────────────┘
```

---

## Domain 1: Digital Product & UI Color Tokens

This track produces production-ready CSS token blocks (`tokens.css`) containing semantic variables with automatic dark-mode adaptation.

### Side Files
- `assets/tokens-template.css` — base CSS template with light/dark scaffolding.
- `references/palettes.md` — curated digital palette catalog with all 7 systems' light and dark values.

### Available Digital Palettes
| Keyword   | Name               | Vibe                               | Best for                                  |
| --------- | ------------------ | ---------------------------------- | ----------------------------------------- |
| `neutral` | **Neutral Modern** | Clean, safe, neutral               | General products, dashboards, B2B tools   |
| `linear`  | **Linear Dark**    | Dark-native, precision engineering | Developer tools, SaaS, data-dense UIs     |
| `claude` / `anthropic` | **Anthropic Editorial Warm** | Warm ivory, slate ink, literary & academic | AI products, research hubs, editorial & docs |
| `openai`  | **OpenAI Swiss Modern** | True white, obsidian ink, pearl surfaces & horizon gradients | Generative AI apps, conversational UIs, media galleries |
| `artcraft`| **ArtCraft Studio Blueprint** | Drafting paper, sunken darkroom viewports, blueprint cobalt & 13-app spectrum | Creative software, desktop studio tools, CAD/3D & pro workflows |
| `cursor`  | **Cursor Code**    | Warm light, code-editor aesthetic  | Developer tools, IDEs, technical products |
| `lovable` | **Lovable Pop**    | Creamy, playful, low-barrier       | No-code tools, creative apps, onboarding  |
| `custom`  | **Custom**         | Derived from your base color       | Brand-specific needs, experiments         |

### Digital Workflow
1. **Determine palette**: Ask user for keyword or derive from a base hex color + mood (`warm` / `cool` / `neutral`).
2. **Consult reference**: Read `references/palettes.md` for curated palettes.
3. **Generate `:root` block** for default light-mode values.
4. **Generate `@media (prefers-color-scheme: dark)` and `.dark` block** for dark-mode overrides.
5. **Validate WCAG AA contrast ratios**:
   - Body text (≤16px): **≥ 4.5:1**
   - Large text (>18px or 14px bold): **≥ 3:1**
   - UI components / borders: **≥ 3:1**
6. **Emit CSS block** and enforce accent discipline (max 2 visible accent uses per screen).

### Standard Token Set
| Token | Role |
| --- | --- |
| `--bg` | Page canvas |
| `--surface` | Elevated cards, panels |
| `--surface-warm` | Tertiary surface tier (buttons, prominent interactive) |
| `--fg` | Primary text |
| `--fg-2` | Secondary emphasis text |
| `--muted` | Placeholders, metadata |
| `--meta` | Tertiary text, footnotes |
| `--border` | Standard borders |
| `--border-soft` | Subtle dividers |
| `--accent` | Primary CTA, links, brand moments |
| `--accent-on` | Text on accent background |
| `--accent-hover` | Hover state for accent elements |
| `--accent-active` | Active/pressed state |
| `--success` / `--warn` / `--danger` | Semantic state feedback |

---

## Domain 2: Graphic & Print Design Color System

This track provides physical media color standards, converting visual concepts into accurate CMYK formulas, Pantone spot colors, and print prepress parameters.

### Reference Manual
- `references/graphic-print-color.md` — deep-dive guide on gamut conversion, black ink rules, paper substrates, and industry mood matrices.

### Core Graphic Color Rules
1. **60-30-10 Golden Ratio**:
   - **60% Dominant Base**: Canvas, background paper tone, dominant negative space.
   - **30% Secondary Structure**: Layout elements, secondary blocks, major headline typography.
   - **10% Visual Accent Hook**: Focal hook, CTA sticker, key emblem, spot foil/varnish.
2. **RGB ➜ CMYK Gamut Protection**:
   - For physical print, never rely on unmanaged RGB conversions (especially vibrant greens, cyan blues, and fluorescent pinks).
   - High-chroma branding elements must be assigned a dedicated **Pantone Spot Color** (`Formula Guide Coated/Uncoated`).
3. **Black Ink Prepress Rules**:
   - **Body text (≤24pt) & barcodes**: Strictly single black `C:0 M:0 Y:0 K:100`. Never use four-color rich black for fine text.
   - **Large dark backgrounds**: Rich black (`C:30 M:20 Y:20 K:100` or `C:40 M:30 Y:0 K:100`). Total Ink Coverage (TIC) must remain **≤ 300%** to prevent drying defects and offset smearing.
4. **Substrate & Paper Absorption Compensation**:
   - **Coated art paper**: High color fidelity, small dot gain (~10%-15%).
   - **Uncoated paper**: High dot gain (~20%-25%), colors darken and desaturate; increase pre-press curve brightness by +5%~10%.
   - **Specialty/Kraft paper**: Dark or tinted base; white elements require an opaque spot white underprint (`白墨打底`).

### Graphic Color Deliverable Format
When delivering a color system for posters, brochures, packaging, or brand VI collateral, output the following structured specification:

```markdown
### [Palette Name] Print & Graphic Color Specification

| Role | Color Name | HEX / RGB | CMYK (FOGRA39) | Pantone Spot | Substrate & Application Notes |
|---|---|---|---|---|---|
| Dominant (60%) | [Name] | `#HEX` / `R,G,B` | `C:__ M:__ Y:__ K:__` | `PANTONE ___ C/U` | Canvas / background cardstock; check paper tone |
| Secondary (30%) | [Name] | `#HEX` / `R,G,B` | `C:__ M:__ Y:__ K:__` | `PANTONE ___ C/U` | Primary headline typography & structural graphics |
| Accent (10%) | [Name] | `#HEX` / `R,G,B` | `C:__ M:__ Y:__ K:__` | `PANTONE ___ C/U` | Focal hook, brand badge, hot foil / spot UV plate |
| Body Text Black | Standard Black | `#000000` / `0,0,0` | `C:0 M:0 Y:0 K:100` | — | Text ≤24pt, barcodes; strictly no rich black mixing |
```
