# Ant Design — Visual Language (exact specs)

Values are **v5 defaults**; nearly all are exposed as **design tokens** (so customize via tokens, not
hardcoded values — see `design-tokens.md`). Each spec ends with its design rationale.

---

## Color

### Brand & functional (seed) colors

| Role | Token | Hex | Palette name |
| --- | --- | --- | --- |
| Primary / brand | `colorPrimary` | `#1677FF` | Daybreak Blue (blue-6) |
| Success | `colorSuccess` | `#52C41A` | Polar Green (green-6) |
| Warning | `colorWarning` | `#FAAD14` | Calendula Gold (gold-6) |
| Error | `colorError` | `#FF4D4F` | Dust Red (red-6) |
| Info | `colorInfo` | `#1677FF` | (same as primary) |

> v4 brand was `#1890FF`; v5 shifted to `#1677FF` for better contrast/accessibility. Don't mix.

### The palette-generation algorithm (颜色梯度算法)

From **one** brand color, antd's algorithm (`@ant-design/colors` `generate()`) derives a **10-step**
palette (index **1–10**, the input sits at **index 6**). Lighter steps (1–5) blend toward white,
darker steps (7–10) toward black, via tuned **HSV** rotations — not naive lightness math — so hues
stay vivid and perceptually even. Example (Daybreak Blue):

```
blue-1 #E6F4FF  blue-2 #BAE0FF  blue-3 #91CAFF  blue-4 #69B1FF  blue-5 #4096FF
blue-6 #1677FF  blue-7 #0958D9  blue-8 #003EB3  blue-9 #002C8C  blue-10 #001D66
```

Use **6** for the main color, **5** for hover, **7** for active/pressed, **1–2** for backgrounds,
**3** for borders. There are 13 preset palettes: red, volcano, orange, gold, yellow, lime, green,
cyan, blue, geekblue, purple, magenta, + grey.

*Why an algorithm:* it guarantees **Repetition/consistency** (every status color has matching
hover/active/bg steps) and **accessible contrast** at each step — the system, not the designer,
enforces it (the **Certainty** value).

### Neutrals & text (light theme)

Text is **layered black at decreasing opacity** (so it composites correctly on any background):

| Use | Value |
| --- | --- |
| Text primary | `rgba(0,0,0,0.88)` (`#000000E0`) |
| Text secondary | `rgba(0,0,0,0.65)` |
| Text tertiary / placeholder | `rgba(0,0,0,0.45)` |
| Text disabled | `rgba(0,0,0,0.25)` (`#00000040`) |
| Border | `rgba(0,0,0,0.15)`; split border `rgba(0,0,0,0.06)` |
| Bg container | `#FFFFFF` · Bg layout | `#F5F5F5` |

*Why opacity, not fixed greys:* opacity-based neutrals adapt to colored/dark backgrounds and keep a
consistent **contrast hierarchy** (primary > secondary > disabled) — supporting **Contrast** and
WCAG legibility.

### Data-viz color

Defer to **AntV** (ant.design's sister viz system): palettes built from the base + neutral palettes,
optimized to be "effective, clear, accurate, beautiful." Don't reuse UI status colors as categorical
series colors (they carry semantic meaning).

---

## Typography

### Font family (system stack — no webfont by default)

```css
-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans',
sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
```

*Why system fonts:* zero load time, native feel per OS, and they render CJK well — the **Natural**
value (look like the user's environment). Set `font-variant-numeric: tabular-nums` so columns of
figures align.

### Type scale

Base **14px / line-height 22px** (`lineHeight ≈ 1.5714`). 14 (not 12) was chosen for legibility at a
~50 cm viewing distance / ~0.3° reading angle on standard monitors. Heading tokens:

| Token | px |
| --- | --- |
| `fontSizeHeading1` | 38 |
| `fontSizeHeading2` | 30 |
| `fontSizeHeading3` | 24 |
| `fontSizeHeading4` | 20 |
| `fontSizeHeading5` | 16 |
| `fontSize` (body) | 14 |
| `fontSizeLG` / `fontSizeSM` | 16 / 12 |

The 10-size system is "inspired by pentatonic scales and natural logarithm." **Use only 3–5 sizes in
one product.** *Why:* restraint = clear **hierarchy (Contrast)** and lower load; too many sizes
destroy the scale's signal.

### Weight

`400` (regular) and `500` (medium) cover almost everything; `600` only for short English emphasis.
*Why:* "order, stability, restraint" — weight is a **Contrast** tool; overusing bold flattens
hierarchy.

---

## Layout, grid & spacing

### 8px base unit

The grid base is **8** ("matches even-number thinking and most mainstream displays"). **All spacing
is a multiple of 8** (4 for fine adjustments). v5 size tokens:

```
sizeXXS 4 · sizeXS 8 · sizeSM 12 · size 16 · sizeMD 20 · sizeLG 24 · sizeXL 32 · sizeXXL 48
seed: sizeUnit 4, sizeStep 4   (Map tokens derive the scale from these)
```

*Why 8px rhythm:* a consistent spatial cadence leverages **Proximity / Common Region** to group
controls and creates "a dynamic sense of rhythm." It's **Repetition** made measurable, and it kills
the pixel-pushing that breeds **collaboration entropy**.

### 24-column grid

Antd uses a **24-column** grid (`<Row gutter>` / `<Col span>`), divisible by 2/3/4/6/8/12 → flexible
without fractions. Responsive breakpoints:

```
xs <576 · sm ≥576 · md ≥768 · lg ≥992 · xl ≥1200 · xxl ≥1600
```

Standard **design canvas 1440px**, content area ~1168px. *Why 24 (vs 12):* enterprise screens are
data-dense; 24 columns give finer, still-aligned partitions — serving **Alignment** without ad-hoc
widths.

---

## Corner radius

`borderRadiusXS 2 · borderRadiusSM 4 · borderRadius 6 (default) · borderRadiusLG 8`. *Why moderate
radius:* a soft 6px reads friendly/modern yet stays **certain** and businesslike — not playful (large
radius) nor harsh (0). Radius is a **Repetition** token: every surface shares it.

## Shadow / elevation

Antd uses **subtle, layered shadows** (3 levels via `boxShadow` / `boxShadowSecondary`) to lift
**transient** surfaces (dropdowns, popovers, modals, cards on hover) off the page — *not* the heavy,
ever-present elevation of Material. *Why restrained:* enterprise screens are dense; loud shadows add
visual noise and false hierarchy. Shadow signals "temporary/floating," reinforcing **figure–ground**
and the **Stay-on-the-Page** pattern (overlays, not new pages).

## Iconography

`@ant-design/icons` — ~700+ icons in three themes: **Outlined** (default), **Filled**, **TwoTone**.
Designed on a **1024×1024** grid with consistent stroke width, optical balance, and a shared visual
language with components. *Why a unified set:* icons are **signifiers**; consistent metaphor + stroke
makes them recognizable at a glance (**recognition over recall**) and visually **repetitive** with
the UI.

## Motion

Ant Design's motion is **natural & purposeful** — it obeys physical intuition (easing like
acceleration/friction) and always *explains a state change*, never decorates. Tokens:

```
durations: motionDurationFast 0.1s · motionDurationMid 0.2s · motionDurationSlow 0.3s
easing:    motionEaseInOut  cubic-bezier(0.645, 0.045, 0.355, 1)
           motionEaseOut    cubic-bezier(0.215, 0.61, 0.355, 1)
           motionEaseInOutCirc, motionEaseInBack, … (full set in the token table)
```

*Why fast + eased:* keep responses well under the **Doherty Threshold (≈400 ms)** so the UI feels
instant (**React Immediately**); easing gives **object constancy** (**Use Transition**) so users
track elements rather than seeing them pop. Respect `prefers-reduced-motion`.

## Dark mode

Generated by `theme.darkAlgorithm`: `colorBgBase` flips to dark and the whole token tree re-derives
(text opacities, palette steps, borders, shadows) — you don't hand-pick dark colors. Backgrounds are
**near-black, not pure #000**, to reduce halation/glare. *Why algorithmic:* dark mode "for free" from
the same seeds embodies **Growing** (one source, many themes) and **Certainty** (dark = light, just
re-derived).

---

## One-screen cheat sheet

```
Primary #1677FF · Success #52C41A · Warning #FAAD14 · Error #FF4D4F
Text 88/65/45/25% black · Bg #FFF / layout #F5F5F5
Body 14/22 · Headings 38/30/24/20/16 · weights 400/500 · 3–5 sizes max · tabular-nums
Spacing ×8 (4 8 12 16 24 32 48) · 24-col grid · radius 6 · subtle 3-level shadow
Motion 0.1/0.2/0.3s eased · <400ms feedback · dark via darkAlgorithm
```
