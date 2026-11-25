# OpenAI Swiss Modernist Design Specification

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Color System & Atmospheric Gradients](#2-color-system--atmospheric-gradients)
3. [Typography (OpenAI Sans System)](#3-typography-openai-sans-system)
4. [Spacing and Grid](#4-spacing-and-grid)
5. [Corner Radius and Shape (Pills & Soft Tiles)](#5-corner-radius-and-shape-pills--soft-tiles)
6. [Surface Elevation (Borderless Soft Fills)](#6-surface-elevation-borderless-soft-fills)
7. [Motion Specifications](#7-motion-specifications)
8. [Component Specifications](#8-component-specifications)
9. [Tailwind CSS & shadcn/ui Integration](#9-tailwind-css--shadcnui-integration)
10. [Token Reference Table](#10-token-reference-table)

---

## 1. Design Principles

### 1.1 Swiss Geometric Clarity
- Inspired by Swiss International Style and contemporary art galleries: stark true-white (`#FFFFFF`) and obsidian (`#000000` / `#0D0D0D`) foundations paired with disciplined neo-grotesque typography (**OpenAI Sans**).
- The interface frame recedes completely so multimodal model outputs (video, voice, code, reasoning) command 100% of visual attention.

### 1.2 Borderless Soft Surfaces
- Unlike Anthropic's `1px` hairline grid, OpenAI minimizes visible borders on content cards.
- Hierarchy is created through **borderless Pearl Gray surface fills** (`#F5F5F5` on `#FFFFFF` in light mode; `#171717` on `#000000` in dark mode) separated by generous whitespace (`16px–24px` gaps, `64px–128px` section margins).

### 1.3 Atmospheric Horizon Warmth
- While UI chrome is strictly monochrome, media tiles, audio visualizers, and featured research cards use soft **Atmospheric Horizon Gradients** (sky blue melting into warm sunrise amber, or aurora teal into soft violet) to evoke human presence and organic intelligence.

### 1.4 The Prompt Box as Primary Architecture
- The conversational input bar ("Ask anything...") is treated as the centerpiece of navigation and interaction — floating with subtle translucent blur (`backdrop-filter: blur(16px)`), stadium-pill starter chips (`9999px`), and a circular icon action button.

---

## 2. Color System & Atmospheric Gradients

### 2.1 Core Monochrome & Neutral Tokens

| Token Name | CSS Variable | Light Mode (Gallery White) | Dark Mode (Obsidian Theater) | Usage |
|---|---|---|---|---|
| Canvas Background | `--bg` | `#FFFFFF` | `#000000` | Primary page canvas |
| Card / Tile Surface | `--surface` | `#F5F5F5` | `#171717` | Borderless bento cards, prompt bar, sidebar |
| Interactive Surface | `--surface-warm` | `#ECECEC` | `#212121` | Card hover state, secondary pill fill |
| Subtle Section Mist | `--surface-mist` | `#FAFAFA` | `#0D0D0D` | Alternating section background |
| Primary Ink | `--fg` | `#0D0D0D` | `#FFFFFF` | Headlines, body copy, primary pill CTA |
| Secondary Text | `--fg-2` | `#1A1A1A` | `#ECECEC` | Subheadings, active navigation links |
| Muted Text | `--muted` | `#6E6E6E` | `#9B9B9B` | Descriptions, metadata, timestamps |
| Placeholder / Meta | `--meta` | `#8E8EA0` | `#6E6E80` | Prompt placeholders, disabled labels |
| Subtle Hairline | `--border` | `#E5E5E5` | `rgba(255, 255, 255, 0.10)` | Prompt box border, table dividers |

### 2.2 Brand Accent & Atmospheric Gradients

| Token Name | CSS Variable | Light Mode Value | Dark Mode Value | Semantic Role |
|---|---|---|---|---|
| OpenAI Teal | `--accent` | `#10A37F` | `#10A37F` | Links, status indicators, active voice orb |
| Teal Hover | `--accent-hover` | `#0A7A5E` | `#1ABC94` | Hover state for teal interactive elements |
| Horizon Gradient | `--gradient-horizon` | `linear-gradient(135deg, #DBEAFE 0%, #FEF3C7 55%, #FDE68A 100%)` | `linear-gradient(135deg, #1E3A8A 0%, #4C1D95 55%, #7C2D12 100%)` | Featured model cards, audio/voice backdrops |
| Aurora Gradient | `--gradient-aurora` | `linear-gradient(135deg, #D1FAE5 0%, #E0F2FE 50%, #EDE9FE 100%)` | `linear-gradient(135deg, #064E3B 0%, #0C4A6E 50%, #312E81 100%)` | Research & reasoning showcase tiles |
| Dusk Gradient | `--gradient-dusk` | `linear-gradient(135deg, #FCE7F3 0%, #EDE9FE 50%, #DBEAFE 100%)` | `linear-gradient(135deg, #831843 0%, #4C1D95 50%, #1E3A8A 100%)` | Creative & multimodal (Sora/Image) tiles |

---

## 3. Typography (OpenAI Sans System)

### 3.1 Font Family Stack
OpenAI's unified brand system centers on **OpenAI Sans** (a geometric grotesque with circular dot details), paired optionally with **Signifier** for long-form literary quotes and **Söhne Mono** for code. Use the following open-source Google Fonts stack:

```css
:root {
  /* Primary UI, Display Headlines & Body Copy (OpenAI Sans / Söhne equivalent) */
  --font-sans: 'Inter', 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Optional Editorial Pull-Quotes & Essays (Signifier equivalent) */
  --font-serif: 'Newsreader', 'Source Serif 4', Georgia, serif;

  /* Code Blocks, Token Counts & API Specs (Söhne Mono equivalent) */
  --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace;
}
```

### 3.2 Type Scale & Hierarchy

| Role | Font Family | Size (Desktop / Mobile) | Weight | Line Height | Letter Spacing | Usage Rules |
|---|---|---|---|---|---|---|
| Display Hero | `--font-sans` | `52px` / `36px` (`3.25rem` / `2.25rem`) | `500` | `1.08` | `-0.03em` | Centered hero title; clean medium weight, never heavy `800` |
| Section Heading (H2) | `--font-sans` | `32px` / `24px` (`2rem` / `1.5rem`) | `500` | `1.18` | `-0.02em` | Carousel section headers |
| Card Title (H3) | `--font-sans` | `20px` (`1.25rem`) | `500` | `1.30` | `-0.015em` | Media tile & feature card headlines |
| Body Copy | `--font-sans` | `17px` (`1.0625rem`) | `400` | `1.60` | `-0.005em` | Standard reading text (`max-width: 65ch`) |
| UI Label / Pill | `--font-sans` | `14px` (`0.875rem`) | `500` | `1.20` | `0` | Pill buttons, sidebar nav links, starter chips |
| Caption / Meta | `--font-sans` | `13px` (`0.8125rem`) | `400` | `1.40` | `0` | Card category + date (`Research · Oct 2026`) |

---

## 4. Spacing and Grid

- **Base Grid**: `8px` increments (`8px`, `16px`, `24px`, `32px`, `48px`, `64px`, `96px`, `128px`).
- **Persistent Left Sidebar + Theater Canvas**:
  - **Left Navigation Rail**: `220px` fixed width on desktop (collapsible), housing clean vertical text links (`Research`, `Safety`, `ChatGPT`, `Sora`, `API`, `Company`).
  - **Main Content Canvas**: Max width `1360px` centered inside the remaining viewport with `32px–64px` horizontal padding.
- **Horizontal Snap Bento Grid**:
  - Content showcases use 3-column or 4-column grids (`gap: 20px`) with aspect-ratio locked tiles (`1:1` square or `4:5` portrait for research/stories, `16:9` for video demos).

---

## 5. Corner Radius and Shape (Pills & Soft Tiles)

OpenAI pairs **100% circular stadium pills** for interactive controls with **softly rounded rectangles** for media containers:

| Token | Value | Application |
|---|---|---|
| `--radius-sm` | `6px` | Inline code tags, small tooltips |
| `--radius-md` | `12px` | Standard info cards, dropdown menus |
| `--radius-lg` | `16px` | Media showcase tiles, bento cards, code blocks |
| `--radius-xl` | `24px` | Floating Prompt Input Bar container |
| `--radius-full` | `9999px` | **All Primary/Secondary Buttons**, starter prompt chips, circular icon buttons |

---

## 6. Surface Elevation (Borderless Soft Fills)

- **Cards & Bento Tiles**: Do **not** use borders (`border: none`) or drop shadows (`box-shadow: none`). Distinguish cards purely by filling them with `--surface` (`#F5F5F5` in light, `#171717` in dark) against the `--bg` (`#FFFFFF` / `#000000`) canvas.
- **Floating Prompt Bar (Exception)**: The central/bottom Prompt Input Box uses `--surface` (`#F5F5F5` / `#171717`) with a `1px solid var(--border)` hairline and a soft ambient float shadow (`0 8px 30px rgba(0, 0, 0, 0.06)` in light mode, `0 8px 30px rgba(0, 0, 0, 0.45)` in dark mode).

---

## 7. Motion Specifications

- **Easing**: `cubic-bezier(0.22, 1, 0.36, 1)` (smooth quintic ease-out).
- **Duration**: `200ms` for surface fills and button states; `350ms` for media card hover zoom.
- **Media Tile Zoom**: On hover, the inner image or atmospheric gradient canvas scales smoothly (`transform: scale(1.025)`) inside an `overflow: hidden; border-radius: 16px` container.

---

## 8. Component Specifications

### 8.1 Stadium Pill Buttons (`border-radius: 9999px`)
- **Primary Pill Button**:
  - Background: `var(--fg)` (`#0D0D0D` in light mode, `#FFFFFF` in dark mode)
  - Text: `var(--bg)` (`#FFFFFF` in light mode, `#0D0D0D` in dark mode)
  - Height: `40px` (standard), `44px` (hero CTA), `34px` (compact chip)
  - Padding: `0 20px`
  - Border Radius: `9999px` (`--radius-full`)
  - Hover: Opacity `0.85` or `#333333`
- **Secondary / Starter Chip Button**:
  - Background: `var(--surface)` (`#F5F5F5` in light, `#171717` in dark)
  - Border: `1px solid transparent` (or `1px solid var(--border)` for floating prompt chips)
  - Text: `var(--fg)`
  - Border Radius: `9999px`
  - Hover: Background shifts to `var(--surface-warm)` (`#ECECEC` / `#212121`)

### 8.2 The Prompt Input Bar (Core Interaction Component)
- **Container**: `max-width: 760px`, `background: var(--surface)`, `border: 1px solid var(--border)`, `border-radius: 24px`, `padding: 14px 18px`, `box-shadow: 0 8px 30px rgba(0,0,0,0.06)`.
- **Anatomy**:
  1. Top/Main Input Area: Auto-expanding textarea or input (`16px`, `--fg`, placeholder in `--meta`).
  2. Bottom Action Row: Left-aligned attachment/mode pills (`Search`, `Reason`, `Voice`) + Right-aligned circular submit button (`36px × 36px`, `border-radius: 9999px`, `background: var(--fg)`, `color: var(--bg)` with upward arrow `↑`).
  3. Below-Bar Starter Pills: Row of `9999px` pill chips offering 3–4 instant example prompts.

### 8.3 Atmospheric Media Cards
- **Anatomy**:
  1. Visual Aspect Box (`aspect-ratio: 1 / 1` or `16 / 10`): `border-radius: 16px`, `overflow: hidden`, filled with an atmospheric gradient (`--gradient-horizon`, `--gradient-aurora`, `--gradient-dusk`) or full-bleed media, with an optional top-left category pill (`rgba(255,255,255,0.75)`, `backdrop-filter: blur(8px)`).
  2. Below-Card Caption Block (`padding-top: 12px`): Meta line (`Research · Oct 2026` in `13px var(--muted)`) + Title (`20px` medium weight `var(--fg)`).

---

## 9. Tailwind CSS & shadcn/ui Integration

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 10. Token Reference Table

| Token | Light Value | Dark Value | Description |
|---|---|---|---|
| `--bg` | `#FFFFFF` | `#000000` | Pure gallery canvas |
| `--surface` | `#F5F5F5` | `#171717` | Borderless card & prompt surface |
| `--surface-warm` | `#ECECEC` | `#212121` | Hover & active surface |
| `--fg` | `#0D0D0D` | `#FFFFFF` | Primary obsidian ink |
| `--muted` | `#6E6E6E` | `#9B9B9B` | Secondary captions & meta |
| `--border` | `#E5E5E5` | `rgba(255,255,255,0.10)` | Subtle hairline divider |
| `--accent` | `#10A37F` | `#10A37F` | OpenAI Emerald Teal |
| `--radius-lg` | `16px` | `16px` | Media tile & bento card radius |
| `--radius-xl` | `24px` | `24px` | Prompt bar container radius |
| `--radius-full` | `9999px` | `9999px` | Stadium pill buttons & chips |

