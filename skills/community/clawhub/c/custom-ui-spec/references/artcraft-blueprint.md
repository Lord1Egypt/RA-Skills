# ArtCraft Studio Blueprint Design Specification

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Color System & 3-Tier Surface Elevation](#2-color-system--3-tier-surface-elevation)
3. [Typography (Wide Grotesque + Italic Serif Hybrid)](#3-typography-wide-grotesque--italic-serif-hybrid)
4. [Spacing and Exposed 1px Blueprint Grid](#4-spacing-and-exposed-1px-blueprint-grid)
5. [Corner Radius and Shape (Strict 0px Zero-Radius)](#5-corner-radius-and-shape-strict-0px-zero-radius)
6. [HUD Registration Marks & Sunken Viewports](#6-hud-registration-marks--sunken-viewports)
7. [Motion & Hard-Cut Inversion Specifications](#7-motion--hard-cut-inversion-specifications)
8. [Component Specifications](#8-component-specifications)
9. [Tailwind CSS & shadcn/ui Integration](#9-tailwind-css--shadcnui-integration)
10. [Token Reference Table](#10-token-reference-table)

---

## 1. Design Principles

### 1.1 Industrial Blueprint & Camera HUD Precision
- Treat the interface as a precision engineering instrument (inspired by CAD drafting tables, camera viewfinders, and darkroom workbenches).
- Replace floating rounded cards with **full-bleed exposed `1px` blueprint grid cells** (`border-b` and `border-r` in `var(--line)`), millimeter-precise `11px` crosshair registration ticks (`.tick`), and wide-tracked monospace HUD labels (`.hud-label`).

### 1.2 Sunken Viewport Realism
- Instead of elevating cards above the canvas with drop shadows, **sink interactive media, canvas previews, and code wells into the page** using `--bg-sunken` (`#E9E8E4` in light mode, `#060607` in dark mode).

### 1.3 Mechanical-meets-Human Typographic Tension
- Pair ultra-wide variable grotesque display headlines (**Archivo**, `font-weight: 620; font-stretch: 118%`) with expressive **Instrument Serif Italic** inline accent words to bridge technical control and artistic expression.

### 1.4 Instantaneous Tactile Feedback
- Interactive controls use **hard-cut binary inversion** (`.invert-block`: `120ms linear` background/text swap between `--invert-bg` and `--invert-fg`) rather than soft opacity fades.

---

## 2. Color System & 3-Tier Surface Elevation

### 2.1 Core Foundation & Surface Tokens

| Token Name | CSS Variable | Light Mode (Drafting Paper) | Dark Mode (Studio Darkroom) | Usage |
|---|---|---|---|---|
| Base Canvas | `--bg` | `#F2F1EE` | `#121316` | Primary page & grid cell canvas |
| Raised Surface | `--bg-raised` | `#FAF9F7` | `#101014` | Floating toolbars, active tabs, modals |
| Sunken Viewport | `--bg-sunken` | `#E9E8E4` | `#060607` | Recessed 16:9 media wells, canvas stages, code blocks |
| Primary Ink | `--ink` | `#101014` | `#F2F1EE` | Standard body text, icons, borders |
| Strong Ink | `--ink-strong` | `#000000` | `#FFFFFF` | Display headlines, high-contrast labels |
| Muted Ink | `--muted` | `rgba(16, 16, 20, 0.62)` | `rgba(242, 241, 238, 0.60)` | Secondary descriptions, HUD category names |
| Faint Ink | `--faint` | `rgba(16, 16, 20, 0.42)` | `rgba(242, 241, 238, 0.38)` | Index numbers (`01`, `02`), ruler ticks |
| Grid Line | `--line` | `rgba(16, 16, 20, 0.16)` | `rgba(242, 241, 238, 0.15)` | Exposed 1px structural grid borders |
| Strong Line | `--line-strong` | `rgba(16, 16, 20, 0.40)` | `rgba(242, 241, 238, 0.40)` | Crosshair `.tick` marks, active cell borders |
| Invert Block BG | `--invert-bg` | `#101014` | `#FFFFFF` | Primary CTA fill & `.invert-block:hover` background |
| Invert Block FG | `--invert-fg` | `#F2F1EE` | `#0B0B0C` | Primary CTA text & `.invert-block:hover` text |
| Blueprint Cobalt | `--accent` | `#2D81FF` | `#2D81FF` | Selection highlight, active indicator |
| Readable Cobalt | `--accent-ink` | `#1659C4` | `#74AAFF` | Focus rings, interactive text links |

### 2.2 Multi-Product Suite Spectrum (`--app` & `--app-ink`)

When building multi-tool suites or categorized feature matrices, assign each tool a dedicated accent pair (`--app` for badges/dots, `--app-ink` for WCAG-compliant text in Light/Dark mode):

| Tool / Domain | Base `--app` | Light `--app-ink` | Dark `--app-ink` |
|---|---|---|---|
| PhotoCraft (Imaging) | `#2F7BF5` | `#1A5BC4` | `#7FB0FF` |
| VectorCraft (Vector) | `#E8573F` | `#B83A24` | `#FF8A70` |
| FilmCraft (Video) | `#8B5CF6` | `#6A3FD6` | `#B69CFF` |
| LightCraft (RAW/Color)| `#F2A516` | `#8A5800` | `#FFC14D` |
| DesignCraft (Layout) | `#7BB51C` | `#457008` | `#A6E04A` |
| FigCraft (UI/UX) | `#02DA96` | `#017A54` | `#3FE6AE` |
| DeckCraft (Slides) | `#F26B1D` | `#AD4306` | `#FF9657` |
| CADCraft (3D/CAD) | `#14A3C7` | `#09596D` | `#4CC7E6` |

---

## 3. Typography (Wide Grotesque + Italic Serif Hybrid)

### 3.1 Four-Font Open-Source Stack
ArtCraft uses 100% open-source Google/Vercel fonts with zero commercial licensing friction:

```css
:root {
  /* 1. Wide Industrial Display Headlines */
  --font-display: 'Archivo', system-ui, sans-serif;

  /* 2. Inline Dramatic Serif Emphasis */
  --font-serif: 'Instrument Serif', Georgia, 'Times New Roman', serif;

  /* 3. Clean UI & Body Copy */
  --font-body: 'Inter', system-ui, sans-serif;

  /* 4. HUD Labels, Coordinates & Indices */
  --font-mono: 'Geist Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
}

.font-display {
  font-family: var(--font-display);
  font-weight: 620;
  font-stretch: 118%; /* Signature wide mechanical stance */
  letter-spacing: -0.025em;
}

.font-display em, .serif-accent {
  font-family: var(--font-serif);
  font-style: italic;
  font-weight: 400;
  font-stretch: 100%;
  font-size: 1.08em;
}

.hud-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem; /* 11px */
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  line-height: 1.2;
}
```

### 3.2 Type Scale

| Role | Class / Font | Size (Desktop / Mobile) | Line Height | Tracking | Usage |
|---|---|---|---|---|---|
| Hero Statement | `.font-display` | `60px–72px` / `40px` | `1.0` | `-0.025em` | Hero headline with 1–2 `Instrument Serif Italic` keywords |
| Section Display (H2)| `.font-display` | `36px–48px` / `28px` | `1.08` | `-0.02em` | Chapter headers |
| Feature Cell Title (H3)| `.font-display` | `24px` (`1.5rem`) | `1.25` | `-0.02em` | Feature cell & card headings |
| Body Copy | `--font-body` | `16px` (`1rem`) | `1.625` | `0` | Descriptions (`max-width: 56ch`, `color: var(--muted)`) |
| HUD Telemetry Label | `.hud-label` | `11px` (`0.6875rem`) | `1.2` | `0.15em` | Cell headers, index numbers (`01 / CRAFTING FEATURES`) |

---

## 4. Spacing and Exposed 1px Blueprint Grid

- **Base Unit**: `4px` (`0.25rem`).
- **Exposed Structural Grid**:
  - Instead of floating cards with margins between them, use a contiguous CSS Grid where cells share `1px solid var(--line)` borders (`border-b border-line`, `border-r border-line`).
  - Outer container is bounded by `max-width: 1440px` with full-bleed horizontal rules extending to viewport edges.

---

## 5. Corner Radius and Shape (Strict 0px Zero-Radius)

- **Global Rule**: `border-radius: 0px !important` across all buttons, inputs, feature cells, media viewports, and badges.
- Crisp 90-degree corners reinforce the architectural blueprint and precision pixel-grid identity.

---

## 6. HUD Registration Marks & Sunken Viewports

### 6.1 Crosshair Registration Ticks (`.tick`)
Place `11px × 11px` crosshair ticks in the corners of sunken media viewports or hero stages:

```css
.tick {
  pointer-events: none;
  width: 11px;
  height: 11px;
  position: absolute;
}
.tick::before, .tick::after {
  content: "";
  background: var(--line-strong);
  position: absolute;
}
.tick::before { width: 1px; top: 0; bottom: 0; left: 5px; }
.tick::after  { height: 1px; top: 5px; left: 0; right: 0; }
```

---

## 7. Motion & Hard-Cut Inversion Specifications

- **Hard-Cut Inversion (`.invert-block`)**:
  ```css
  .invert-block {
    transition: background-color 120ms linear, color 120ms linear;
  }
  .invert-block:hover, .invert-block[data-active="true"] {
    background-color: var(--invert-bg);
    color: var(--invert-fg);
  }
  ```
- **Smooth Theme Interpolation (`@property`)**:
  - Register color variables with CSS `@property` (`syntax: "<color>"`) and transition them over `400ms` on `html.theme-anim` while freezing child transitions (`transition-duration: 0s !important`) to eliminate lag.
- **Infinite Capability Marquee**:
  - Continuous `36s linear infinite` horizontal ticker separating capability keywords with small square bullets (`▪`).

---

## 8. Component Specifications

### 8.1 3-Tier Feature Cell Anatomy
Every feature showcase cell in the blueprint grid follows a strict 3-part vertical anatomy:
1. **Top HUD Bar**: `display: flex; justify-content: space-between; padding: 10px 24px; border-bottom: 1px solid var(--line);`
   - Left: `.hud-label` category name in `var(--muted)` (e.g., `3D COMPOSITING`)
   - Right: `.hud-label` two-digit index in `var(--faint)` (e.g., `02`)
2. **Middle Sunken Viewport**: `aspect-ratio: 16 / 9; background: var(--bg-sunken); position: relative; overflow: hidden;`
   - Contains corner `.tick` crosshairs (`top-2 left-2`, `bottom-2 right-2`) and interactive canvas/video preview.
3. **Bottom Spec Copy**: `padding: 24px 32px;`
   - Heading: `.font-display` (`24px`, `var(--ink-strong)`)
   - Description: `16px`, `var(--muted)`, `line-height: 1.625`, `margin-top: 8px`.

### 8.2 Buttons
- **Primary Invert Block Button**:
  - Background: `var(--invert-bg)` (`#101014` in light, `#FFFFFF` in dark)
  - Text: `var(--invert-fg)` (`#F2F1EE` in light, `#0B0B0C` in dark)
  - Border: `1px solid var(--invert-bg)`
  - Radius: `0px`
  - Hover: Swaps to `background: var(--bg); color: var(--ink-strong); border-color: var(--line-strong)`
- **Secondary Blueprint Cell Button**:
  - Background: `transparent`
  - Border: `1px solid var(--line-strong)`
  - Text: `var(--ink)`
  - Hover (`.invert-block`): Instantly fills with `var(--invert-bg)` and text `var(--invert-fg)` in `120ms linear`.

---

## 9. Tailwind CSS & shadcn/ui Integration

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Geist+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## 10. Token Reference Table

| Token | Light Value | Dark Value | Description |
|---|---|---|---|
| `--bg` | `#F2F1EE` | `#121316` | Primary drafting paper / darkroom canvas |
| `--bg-raised` | `#FAF9F7` | `#101014` | Elevated bar / header surface |
| `--bg-sunken` | `#E9E8E4` | `#060607` | Recessed 16:9 viewport well |
| `--ink` | `#101014` | `#F2F1EE` | Standard body & UI ink |
| `--ink-strong` | `#000000` | `#FFFFFF` | High-contrast display ink |
| `--line` | `#10101429` | `#F2F1EE26` | 1px exposed blueprint grid line |
| `--line-strong` | `#10101466` | `#F2F1EE66` | Crosshair ticks & strong borders |
| `--accent` | `#2D81FF` | `#2D81FF` | Blueprint Cobalt highlight |
| `--accent-ink` | `#1659C4` | `#74AAFF` | WCAG-readable cobalt ink |
| `--radius` | `0px` | `0px` | Strict zero-radius geometry |

