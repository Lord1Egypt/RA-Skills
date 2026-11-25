# Anthropic Editorial Design Specification

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Spacing and Grid](#4-spacing-and-grid)
5. [Corner Radius and Shape](#5-corner-radius-and-shape)
6. [Shadow and Depth (Zero-Shadow Rule)](#6-shadow-and-depth-zero-shadow-rule)
7. [Motion Specifications](#7-motion-specifications)
8. [Component Specifications](#8-component-specifications)
9. [Tailwind CSS & shadcn/ui Integration](#9-tailwind-css--shadcnui-integration)
10. [Token Reference Table](#10-token-reference-table)

---

## 1. Design Principles

### 1.1 Editorial Authority
- Treat digital interfaces like a printed literary journal or academic monograph rather than a glossy SaaS marketing page.
- Pair high-contrast authoritative serif headlines with crisp grotesque body copy and monospace metadata labels.
- Let typographic hierarchy, negative space, and structural rules carry the visual weight.

### 1.2 Tactile Warmth
- Reject sterile pure white (`#FFFFFF`) and cold tech blue-grays (`#F8FAFC`).
- Anchor the canvas in warm parchment ivory (`#FAF9F5`) and deep slate ink (`#141413`) to reduce ocular fatigue during long-form reading.
- Use organic, earth-derived accents (Clay, Cactus, Sky, Fig, Oat) sparingly for categorization, data visualization, and research highlights.

### 1.3 Structural Honesty (Zero-Shadow Discipline)
- **No diffuse drop shadows** on cards, containers, or buttons.
- Define hierarchy through `1px solid` hairline borders (`#C6C4BA` in light mode, `rgba(250, 249, 245, 0.14)` in dark mode) and warm surface tone steps (`#FAF9F5` → `#F5F4ED` → `#E8E6DC`).

### 1.4 Utilitarian Restraint
- Primary actions use solid Slate Ink (`#141413`) rather than saturated neon or gradient fills.
- Motion is strictly functional (`150ms–200ms` tone or border transitions), never decorative or bouncy.

---

## 2. Color System

### 2.1 Core Foundation & Neutral Tokens

| Token Name | CSS Variable | Light Mode (Ivory Canvas) | Dark Mode (Slate Ink Canvas) | Usage |
|---|---|---|---|---|
| Canvas Background | `--bg` | `#FAF9F5` | `#141413` | Primary page canvas |
| Elevated Surface | `--surface` | `#F5F4ED` | `#1E1E1C` | Cards, code blocks, table headers |
| Secondary Surface | `--surface-warm` | `#E8E6DC` | `#2A2A27` | Secondary buttons, active pills, callouts |
| Oat Surface | `--surface-oat` | `#E3DACC` | `#33312B` | Highlighted banners, featured paper cards |
| Primary Ink | `--fg` | `#141413` | `#FAF9F5` | Headlines, body text, primary CTA fill |
| Secondary Ink | `--fg-2` | `#3D3D3A` | `#D8D6CC` | Subtitles, lead paragraphs |
| Muted Text | `--muted` | `#5E5D59` | `#B0AEA5` | Captions, secondary descriptions |
| Meta / Inactive | `--meta` | `#87867F` | `#7A786F` | Timestamps, middle-dot separators |
| Hairline Border | `--border` | `#C6C4BA` | `rgba(250, 249, 245, 0.14)` | Structural grid lines, card borders, inputs |
| Subtle Divider | `--border-soft` | `#E8E6DC` | `rgba(250, 249, 245, 0.07)` | Table row dividers, internal separators |

### 2.2 Domain & Editorial Accents

| Accent Name | CSS Variable | Light Hex | Dark Hex | Semantic Role |
|---|---|---|---|---|
| Clay (Terracotta) | `--accent-clay` | `#D97757` | `#E08568` | Brand focal hook, active indicator, primary chart series |
| Clay Hover | `--accent-hover` | `#C6613F` | `#E38C70` | Hover state for terracotta accents |
| Cactus (Sage) | `--accent-cactus` | `#788C5D` | `#8FA372` | Safety research, alignment status, positive/success metric |
| Sky (Slate Blue) | `--accent-sky` | `#6A9BCC` | `#82B0DE` | Economic index, technical benchmarks, info state |
| Fig (Mauve) | `--accent-fig` | `#C46686` | `#D47A98` | Policy papers, societal impact, tertiary chart series |
| Coral Tint | `--accent-coral` | `#EBCECE` | `#4A3535` | Soft badge fill, editorial callout background |
| Seafoam Tint | `--accent-seafoam` | `#BCD1CA` | `#2D3D38` | Soft technical callout background |

---

## 3. Typography

### 3.1 Tripartite Font Stack

Anthropic's typography pairs literary serif headings with clean geometric/grotesque body text and monospace metadata labels. When proprietary `Anthropic Serif` / `Anthropic Sans` fonts are unavailable, use the following open-source Google Fonts stack:

```css
:root {
  /* Display & Section Headings */
  --font-serif: 'Newsreader', 'Lora', 'Instrument Serif', Georgia, Cambria, serif;
  
  /* Body Copy, Navigation & UI Controls */
  --font-sans: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  
  /* Eyebrow Labels, Category Tags, Metrics & Code */
  --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace;
}
```

### 3.2 Type Scale & Hierarchy

| Role | Font Family | Size (Desktop / Mobile) | Weight | Line Height | Letter Spacing | Usage Rules |
|---|---|---|---|---|---|---|
| Display Hero | `--font-serif` | `56px` / `38px` (`3.5rem` / `2.375rem`) | `400`–`500` | `1.08` | `-0.025em` | Page hero statement; never bold (`700`) |
| Section Title (H1/H2) | `--font-serif` | `36px` / `28px` (`2.25rem` / `1.75rem`) | `400`–`500` | `1.15` | `-0.02em` | Major chapter headings |
| Card / Article Title (H3) | `--font-serif` | `22px` / `20px` (`1.375rem` / `1.25rem`) | `500` | `1.30` | `-0.01em` | Research cards, feature titles |
| Subheading (H4) | `--font-sans` | `17px` (`1.0625rem`) | `600` | `1.40` | `-0.01em` | UI panel headers, table titles |
| Body Large (Lead) | `--font-sans` | `18px` (`1.125rem`) | `400` | `1.65` | `0` | Introductory prose, article abstracts |
| Body Standard | `--font-sans` | `16px` (`1rem`) | `400` | `1.62` | `0` | Long-form essays, documentation (`60ch–70ch` max) |
| UI Control / Button | `--font-sans` | `14px` (`0.875rem`) | `500` | `1.20` | `0` | Buttons, inputs, navigation links |
| Eyebrow / Meta Tag | `--font-mono` | `12px` (`0.75rem`) | `500` | `1.20` | `0.08em` | `UPPERCASE` category labels, dates (`RESEARCH · OCT 2026`) |

---

## 4. Spacing and Grid

### 4.1 8px Structural Spacing Scale
- Base unit: `4px` / `8px`
- Scale: `4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`, `64px`, `96px`, `128px`

### 4.2 Broadsheet Asymmetric Grid
- **Max Container Width**: `1280px` (`80rem`) with `24px` (mobile) to `48px` (desktop) horizontal padding.
- **Asymmetric 12-Column Split**:
  - **Left Column (3 to 4 cols)**: Sticky eyebrow label, section title, or table-of-contents wayfinding.
  - **Right Column (8 to 9 cols)**: Primary narrative prose, research index list, or interactive component grid.
- **Reading Measure Constraint**: Long-form body text must be constrained to `60ch–70ch` (`max-width: 680px`) to prevent eye strain.
- **Cream & Ink Band Pacing**: For long landing or research pages, alternate full-bleed Ivory Cream (`#FAF9F5`) sections with full-bleed Slate Ink (`#141413`) chapters separated by `1px solid var(--border)` rules.

---

## 5. Corner Radius and Shape

Anthropic avoids bubbly consumer rounding (`16px–24px` on buttons) in favor of crisp, book-like geometry:

| Token | Value | Application |
|---|---|---|
| `--radius-none` | `0px` | Full-bleed bands, Hairline index tables, dividers |
| `--radius-sm` | `4px` | Inline code badges, checkboxes, keyboard kbd tags |
| `--radius-md` | `6px` | Primary/Secondary Buttons, Text Inputs, Selects |
| `--radius-lg` | `12px` | Editorial Cards, Callout Panels, Code Containers, Modals |
| `--radius-full` | `9999px` | Category filter pills, status dots |

---

## 6. Shadow and Depth (Zero-Shadow Rule)

- **Cards, Buttons, Inputs, Panels**: `box-shadow: none !important;`
- **Elevation Strategy**:
  - **Level 0 (Canvas)**: `--bg` (`#FAF9F5`)
  - **Level 1 (Bounded Card)**: `--surface` (`#F5F4ED`) + `1px solid var(--border)` (`#C6C4BA`)
  - **Level 2 (Featured / Interactive Surface)**: `--surface-warm` (`#E8E6DC`) or `--surface-oat` (`#E3DACC`) + `1px solid var(--fg)` on hover
  - **Level 3 (Modal / Popover)**: `--bg` + `1px solid var(--fg)` + subtle backdrop dim (`rgba(20, 20, 19, 0.45)` with `backdrop-filter: blur(4px)`)

---

## 7. Motion Specifications

- **Duration**: `150ms` for color/border state changes; `200ms` for layout disclosures (accordions/tabs).
- **Easing**: `cubic-bezier(0.16, 1, 0.3, 1)` (clean exponential ease-out).
- **Forbidden Motion**: No spring physics, no scale-up hover zoom (`transform: scale(1.05)` is prohibited on cards), no parallax scrolling.
- **Permitted Micro-interactions**:
  - Card hover: border transitions from `--border` (`#C6C4BA`) to `--fg` (`#141413`), or background shifts from `--surface` to `--surface-warm`.
  - Link hover: `text-underline-offset` shifts from `3px` to `5px` with `1px` thickness.

---

## 8. Component Specifications

### 8.1 Buttons
- **Primary Button**:
  - Background: `var(--fg)` (`#141413` in light mode, `#FAF9F5` in dark mode)
  - Text: `var(--bg)` (`#FAF9F5` in light mode, `#141413` in dark mode)
  - Height: `40px` (standard), `36px` (compact), `44px` (hero CTA)
  - Padding: `0 18px`
  - Border Radius: `6px` (`--radius-md`)
  - Hover: Background shifts to `#3D3D3A` (light mode) or `#D8D6CC` (dark mode)
- **Secondary (Outline) Button**:
  - Background: `transparent`
  - Border: `1px solid var(--border)`
  - Text: `var(--fg)`
  - Hover: Background fills with `var(--surface-warm)` (`#E8E6DC`), border sharpens to `var(--fg)`
- **Accent (Clay) Button** *(use sparingly, max 1 per view for special product launches)*:
  - Background: `var(--accent-clay)` (`#D97757`)
  - Text: `#FAF9F5`
  - Hover: `#C6613F`

### 8.2 Editorial Cards
- **Anatomy**:
  1. Top Eyebrow Row: `--font-mono`, `12px`, `UPPERCASE`, `var(--muted)`, formatted as `CATEGORY · DATE` (e.g., `ALIGNMENT · OCT 2026`).
  2. Title: `--font-serif`, `22px`, `var(--fg)`, line-height `1.3`.
  3. Summary: `--font-sans`, `15px`, `var(--muted)`, line-height `1.6`.
  4. Footer Action: Bottom-aligned link (`Read paper →`) in `14px` `--font-sans` medium weight.
- **Styling**: `background: var(--surface)`, `border: 1px solid var(--border)`, `border-radius: 12px`, `padding: 24px`, `box-shadow: none`.

### 8.3 Archive Index List (Publication Rows)
- Used for research directories, changelogs, and documentation lists.
- Structure: Full-width horizontal rows separated by `1px solid var(--border-soft)`, with top and bottom container borders in `1px solid var(--border)`.
- Columns: `Date /Mono (140px)` | `Category Tag (160px)` | `Title /Serif (1fr)` | `Arrow Indicator (32px)`.
- Hover state: Row background transitions to `var(--surface-warm)`, arrow translates `translateX(3px)`.

### 8.4 Form Controls (Inputs, Selects, Textareas)
- Height: `40px`
- Background: `var(--bg)`
- Border: `1px solid var(--border)`
- Border Radius: `6px`
- Focus State: `outline: none; border-color: var(--fg); box-shadow: 0 0 0 1px var(--fg);` (crisp 2px ink ring, no blurry glow).

---

## 9. Tailwind CSS & shadcn/ui Integration

Add the following to your Tailwind setup to use Anthropic Editorial tokens seamlessly with `shadcn/ui`:

```html
<!-- Google Fonts Import -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## 10. Token Reference Table

| Token | Light Value | Dark Value | Description |
|---|---|---|---|
| `--bg` | `#FAF9F5` | `#141413` | Primary page canvas |
| `--surface` | `#F5F4ED` | `#1E1E1C` | Card & module background |
| `--surface-warm` | `#E8E6DC` | `#2A2A27` | Hover & secondary surface |
| `--surface-oat` | `#E3DACC` | `#33312B` | Featured callout surface |
| `--fg` | `#141413` | `#FAF9F5` | Primary ink & CTA fill |
| `--muted` | `#5E5D59` | `#B0AEA5` | Secondary body & captions |
| `--border` | `#C6C4BA` | `rgba(250,249,245,0.14)` | 1px structural hairline |
| `--accent-clay` | `#D97757` | `#E08568` | Terracotta brand highlight |
| `--accent-cactus` | `#788C5D` | `#8FA372` | Safety / positive accent |
| `--accent-sky` | `#6A9BCC` | `#82B0DE` | Data / informational accent |
| `--accent-fig` | `#C46686` | `#D47A98` | Policy / editorial accent |
| `--radius-md` | `6px` | `6px` | Control & button radius |
| `--radius-lg` | `12px` | `12px` | Card & panel radius |

