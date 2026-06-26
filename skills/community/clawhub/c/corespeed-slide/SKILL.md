---
name: corespeed-slide
description: Generate professional PowerPoint (.pptx) presentations using JSX/TSX with Deno. Supports slides, text, shapes, tables, charts (bar, line, pie, donut), images, gradients, shadows, and flexible layouts. Use when a user asks to create presentations, slide decks, pitch decks, reports, or any PPTX file.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["deno"] },
        "install":
          [
            {
              "id": "deno-install",
              "kind": "shell",
              "command": "curl -fsSL https://deno.land/install.sh | sh",
              "bins": ["deno"],
              "label": "Install Deno (https://deno.land)",
            },
          ],
      },
  }
---

# Corespeed PPTX — PowerPoint Generation with JSX

Generate professional `.pptx` files using TypeScript JSX via [`@pixel/pptx`](https://jsr.io/@pixel/pptx).

## Workflow

1. Write a `.tsx` file that exports a `deck` variable
2. Run the generator to produce the `.pptx`

## Usage

```bash
deno run --allow-read --allow-write --config {baseDir}/scripts/deno.json {baseDir}/scripts/generate.ts slides.tsx output.pptx [--json]
```

- First arg: path to your `.tsx` slide file (must `export const deck = ...`)
- Second arg: output `.pptx` filename
- `--json` — structured JSON output for agent consumption

## Design Principles

These rules are distilled from the three masters of presentation design:

- **Edward Tufte** (Yale professor, *The Visual Display of Quantitative Information*) — maximize data-ink ratio, remove chartjunk, every pixel must earn its place
- **Nancy Duarte** (designed Al Gore's *An Inconvenient Truth*, author of *Slide:ology*) — one idea per slide, visual contrast creates meaning, the audience is the hero
- **Garr Reynolds** (author of *Presentation Zen*) — restraint, whitespace, signal over noise, simplicity is the ultimate sophistication

Follow these rules for every deck:

1. **One idea per slide** (Duarte). If you need a second point, make a second slide.
2. **Font ≥ 24pt body, ≥ 32pt titles.** If the audience can't read it from the back row, it's too small.
3. **Max 3 colors** (Reynolds). One primary, one accent, one neutral. Derive the rest as tints/shades.
4. **Whitespace is design** (Reynolds). Generous padding (≥ 0.5in slide margins, ≥ 0.2in element padding). Never fill every inch.
5. **Contrast over decoration** (Duarte). No drop shadows unless essential. No gradients for ornament. Use contrast (size, weight, color) to create hierarchy.
6. **Data-ink ratio** (Tufte). Every pixel should convey information. Remove gridlines, borders, and labels that don't add meaning.
7. **Visual hierarchy.** Title → Key number/chart → Supporting text. The eye should know where to go instantly.
8. **Consistent rhythm.** Same gaps, same padding, same font sizes across all slides. Use `layout` defaults on `<Presentation>`.
9. **16:9 widescreen.** Always set `slideWidth={u.in(13.33)} slideHeight={u.in(7.5)}` on `<Presentation>`. The library defaults to 4:3 which looks wrong on modern screens.

### Preventing Text Overflow (critical)

The library uses fixed-size containers. Text that exceeds the container **will overflow and be clipped**. Follow these rules strictly:

1. **Use `grow` instead of fixed `h` whenever possible.** Inside `<Row>` or `<Column>`, prefer `grow={1}` over explicit `h={u.in(X)}`. The layout engine will calculate the correct size.
2. **Budget height for text.** Each line of 14pt text needs ~0.3in. A card with title + 4 bullet points needs at minimum: `0.3 (title) + 4×0.3 (bullets) + 0.6 (padding) = 1.8in`. Always round up.
3. **Fewer words, never more containers.** If text doesn't fit, shorten the text — don't shrink the font or the container.
4. **Max 5 bullet points per card.** If you need more, split into two cards or two slides.
5. **Test the math.** For `<Align>` with explicit `h`: count lines × 0.3in + padding × 2. If the result > h, increase h or cut text.
6. **Leave 20% headroom.** If you calculate 2.0in needed, set h to at least 2.4in.
7. **Never nest `<Align>` with tight heights inside `<Stack>`.** Use `<Column>` with `grow` instead — it flexes to fit content.
8. **Safe card pattern:**
   ```tsx
   {/* ✅ GOOD: grow handles height automatically */}
   <Column>
     <Shape preset="roundRect" style={cardStyle} grow={1}>
       <Text.P style={titleStyle}>Title</Text.P>
       <Text.P style={bodyStyle}>Body text here</Text.P>
     </Shape>
   </Column>

   {/* ❌ BAD: fixed h too small, text will overflow */}
   <Align x="center" y="center" w={u.in(3)} h={u.in(1.5)}>
     <Text>
       <Text.P>Title</Text.P>
       <Text.P>Line 1</Text.P>
       <Text.P>Line 2</Text.P>
       <Text.P>Line 3</Text.P>
       <Text.P>Line 4</Text.P>  {/* overflows! */}
     </Text>
   </Align>
   ```

### Table Overflow Prevention (critical)

Tables are the most common source of overflow. Follow these rules:

1. **Column widths must sum to ≤ content width.** For 16:9 slide with 1in padding each side: content width = 11.33in. All `cols` values must sum to ≤ 11.33in.
   ```tsx
   // ✅ GOOD: 2.5 + 4.0 + 4.0 = 10.5in < 11.33in
   <Table cols={[u.in(2.5), u.in(4.0), u.in(4.0)]}>

   // ❌ BAD: 3.0 + 5.0 + 5.0 = 13.0in > 11.33in → overflows right
   <Table cols={[u.in(3.0), u.in(5.0), u.in(5.0)]}>
   ```

2. **Give tables `grow` weight in `<Column>`.** `<Column>` distributes height equally by default. A table with 5 rows needs more space than a title. Use `grow` to allocate proportionally:
   ```tsx
   // ✅ GOOD: table gets 4x the space of title
   <Column>
     <Text.P style={titleStyle}>Title</Text.P>       {/* grow=1 default */}
     <Table cols={[...]} grow={4}>                    {/* gets 4x height */}
       <Table.Row>...</Table.Row>
       ...
     </Table>
   </Column>

   // ❌ BAD: Column splits equally, table gets squeezed
   <Column>
     <Text.P>Label</Text.P>
     <Text.P>Title</Text.P>
     <Table cols={[...]}>    {/* gets only 1/3 of height → rows overflow */}
       ...5 rows...
     </Table>
   </Column>
   ```

3. **Budget row height.** Each row of 12pt text needs ~0.45in (text + padding). Header row: 0.45in. A 5-row table needs: `0.45 + 4×0.45 = 2.25in` minimum.

4. **Keep cell text short.** Max ~40 chars per cell. If text wraps to 2 lines, the row needs 0.65in instead of 0.45in.

5. **Prefer fewer rows.** Max 5-6 data rows per slide. If you need more, split into two slides.

### Color Palettes (reference)

| Style | Background | Primary | Accent | Text |
|-------|-----------|---------|--------|------|
| **Dark (OpenAI)** | `0D0D0D` | `10A37F` | `6E42D3` | `FFFFFF` |
| **Warm (Anthropic)** | `FDF6EE` | `D97706` | `1F4E79` | `1C1917` |
| **Clean (Apple)** | `FFFFFF` | `007AFF` | `FF3B30` | `1D1D1F` |
| **Academic (Stanford)** | `FFFFFF` | `8C1515` | `2E2D29` | `2E2D29` |
| **Neutral (Stripe)** | `F6F9FC` | `635BFF` | `0A2540` | `0A2540` |

Pick one palette. Don't mix.

### Page Numbers

The library has no built-in page numbers. Use `<Positioned>` on every slide:

```tsx
// Helper — put at top of every .tsx file
const TOTAL = 10; // update to actual slide count

// ⚠️ CRITICAL: <Positioned> coordinates are RELATIVE TO CONTENT AREA (after slide padding).
// For 16:9 slide (13.33 x 7.5in) with padding 0.8/1.0/0.7/1.0:
//   Content area = (13.33 - 1.0 - 1.0) x (7.5 - 0.8 - 0.7) = 11.33 x 6.0in
//   Bottom-right page number: x = contentWidth - 1.0, y = contentHeight - 0.4
const PageNum = ({ n }: { n: number }) => (
  <Positioned x={u.in(10.33)} y={u.in(5.6)} w={u.in(1)} h={u.in(0.4)}>
    <Text.P style={{ fontSize: u.font(12), fontColor: textColor, align: "right" }}>
      {n} / {TOTAL}
    </Text.P>
  </Positioned>
);

// Use on every slide — LAST child of <Slide> (renders on top, never occluded)
<Slide background={bg}>
  <Column>
    {/* ...slide content... */}
  </Column>
  <PageNum n={1} />  {/* ← MUST be last child for highest z-order */}
</Slide>
```

Rules:
- **Always add page numbers.** They help the audience track progress and reference slides.
- **`<Positioned>` is relative to content area**, NOT the slide origin. Calculate: `slideWidth - leftPadding - rightPadding = contentWidth`. Position within those bounds.
- Use the **main text color** (not muted) — at 12pt it must be readable.
- Place `<PageNum>` as the **last child of `<Slide>`** — PPTX has no z-index, rendering order = declaration order. Last element renders on top, so page numbers are never occluded by other content.

## Writing Slides

Create a `.tsx` file. It must export a `deck` variable:

```tsx
/** @jsxImportSource @pixel/pptx */
import { Align, clr, Presentation, Slide, Text, u } from "@pixel/pptx";

export const deck = (
  <Presentation title="My Deck" slideWidth={u.in(13.33)} slideHeight={u.in(7.5)}>
    <Slide background={{ kind: "solid", color: clr.hex("F7F4EE") }}>
      <Align x="center" y="center" w={u.in(8)} h={u.in(1.5)}>
        <Text.P style={{ fontSize: u.font(32), bold: true }}>
          Hello, World!
        </Text.P>
      </Align>
    </Slide>
  </Presentation>
);
```

## Components

### Layout

| Component | Purpose |
|-----------|---------|
| `<Presentation>` | Root container. Props: `title`, `layout` |
| `<Slide>` | Single slide. Props: `background`, `layout` |
| `<Row>` | Horizontal flex layout. Has `<Row.Start>`, `<Row.End>` |
| `<Column>` | Vertical flex layout. Has `<Column.Start>`, `<Column.End>` |
| `<Stack>` | Overlapping layers |
| `<Align x y w h>` | Center/align a single child |
| `<Positioned x y w h>` | Absolute positioning |

### Content

| Component | Purpose |
|-----------|---------|
| `<Text>` | Multi-paragraph text body. Props: `gap`, `style` |
| `<Text.P>` | Single paragraph |
| `<Text.Span>` | Inline text run |
| `<Text.Bold>`, `<Text.Italic>`, `<Text.Underline>` | Inline formatting |
| `<Text.Link href="...">` | Hyperlink |
| `<Shape preset="...">` | Shape: `rect`, `roundRect`, `ellipse`, etc. |
| `<Image src={bytes} w={...} h={...} />` | Embed image (Uint8Array) |
| `<Table cols=[...]>` | Table with `<Table.Row>` and `<Table.Cell>` |

### Charts

| Component | Purpose |
|-----------|---------|
| `<Chart.Bar data={[...]} category="key" series={[...]} />` | Bar chart |
| `<Chart.Line data={[...]} category="key" series={[...]} />` | Line chart |
| `<Chart.Pie data={[...]} category="key" series={[...]} />` | Pie chart |
| `<Chart.Donut data={[...]} category="key" series={[...]} />` | Donut chart |

## Units & Colors

```tsx
import { u, clr } from "@pixel/pptx";

u.in(1)       // inches
u.cm(2.5)     // centimeters
u.pt(12)      // points
u.pct(50)     // percentage
u.font(24)    // font size (hundredths of a point)

clr.hex("1F4E79")  // hex color (no #)
```

## Styling

Style props are plain objects. Use `style` on any component:

```tsx
const style = {
  fill: { kind: "solid", color: clr.hex("1F4E79") },
  fontSize: u.font(24),
  fontColor: clr.hex("FFFFFF"),
  bold: true,
  italic: false,
  align: "center",
  verticalAlign: "middle",
  padding: u.in(0.2),
  shadow: {
    color: clr.hex("000000"),
    blur: u.emu(12000),
    distance: u.emu(4000),
    angle: 50,
    alpha: u.pct(18),
  },
  bullet: { kind: "char", char: "•" },
};
```

Backgrounds support `solid`, `linear-gradient`, and image.

## Example: Professional Multi-Slide Deck (Anthropic-warm style)

```tsx
/** @jsxImportSource @pixel/pptx */
import {
  Align, Chart, clr, Column, Presentation, Row, Shape, Slide,
  Stack, Table, Text, u, type Style,
} from "@pixel/pptx";

// --- Design tokens (pick ONE palette, use everywhere) ---
const bg     = clr.hex("FDF6EE");  // warm cream
const card   = clr.hex("FFFFFF");
const primary = clr.hex("D97706"); // amber
const dark   = clr.hex("1C1917");  // near-black
const muted  = clr.hex("78716C");  // warm gray
const accent = clr.hex("1F4E79");  // deep blue for charts

// --- Reusable styles ---
const s = {
  heroBar: {
    fill: { kind: "solid", color: primary },
    verticalAlign: "middle",
    padding: { top: u.in(0.3), right: u.in(0.5), bottom: u.in(0.3), left: u.in(0.5) },
  } satisfies Style,
  h1: { fontSize: u.font(36), fontColor: card, bold: true } satisfies Style,
  subtitle: { fontSize: u.font(16), fontColor: clr.hex("FEF3C7") } satisfies Style,
  h2: { fontSize: u.font(24), fontColor: dark, bold: true } satisfies Style,
  body: { fontSize: u.font(14), fontColor: muted } satisfies Style,
  bigNum: { fontSize: u.font(48), fontColor: primary, bold: true, align: "center" } satisfies Style,
  bigLabel: { fontSize: u.font(14), fontColor: muted, align: "center" } satisfies Style,
  cardBox: {
    fill: { kind: "solid", color: card },
    padding: u.in(0.3),
    shadow: { color: clr.hex("000000"), blur: u.emu(8000), distance: u.emu(2000), angle: 90, alpha: u.pct(8) },
  } satisfies Style,
};

export const deck = (
  <Presentation title="Q2 Review" slideWidth={u.in(13.33)} slideHeight={u.in(7.5)} layout={{
    slidePadding: u.in(0.6),
    rowGap: u.in(0.35),
    columnGap: u.in(0.35),
  }}>

    {/* Slide 1: Title — one idea only */}
    <Slide background={{ kind: "solid", color: bg }}>
      <Column>
        <Shape preset="roundRect" h={u.in(1.6)} style={s.heroBar}>
          <Text.P style={s.h1}>Q2 2025 Review</Text.P>
          <Text.P style={s.subtitle}>Growth ahead of plan · 15% QoQ</Text.P>
        </Shape>
        <Row>
          {/* Big number cards — Tufte: let the data speak */}
          {[
            { num: "$1.2M", label: "Revenue" },
            { num: "15%", label: "Growth" },
            { num: "61", label: "NPS" },
          ].map(({ num, label }) => (
            <Stack grow={1}>
              <Shape preset="roundRect" style={s.cardBox} />
              <Align x="center" y="center" w={u.in(2.5)} h={u.in(2.5)}>
                <Text gap={u.in(0.1)}>
                  <Text.P style={s.bigNum}>{num}</Text.P>
                  <Text.P style={s.bigLabel}>{label}</Text.P>
                </Text>
              </Align>
            </Stack>
          ))}
        </Row>
      </Column>
    </Slide>

    {/* Slide 2: Chart — one chart, full focus */}
    <Slide background={{ kind: "solid", color: bg }}>
      <Column>
        <Text.P style={s.h2}>Revenue by Quarter</Text.P>
        <Stack grow={1}>
          <Shape preset="roundRect" style={s.cardBox} />
          <Align x="center" y="center" w={u.in(8)} h={u.in(4)}>
            <Chart.Bar
              data={[
                { q: "Q1", rev: 0.8 }, { q: "Q2", rev: 1.2 },
                { q: "Q3", rev: 1.0 }, { q: "Q4", rev: 1.5 },
              ]}
              category="q"
              series={[{ name: "Revenue ($M)", value: "rev", color: accent }]}
              labels
              valueAxis={{ min: 0, max: 2 }}
            />
          </Align>
        </Stack>
      </Column>
    </Slide>

  </Presentation>
);
```

## Notes

- **No manual setup required.** Deno auto-downloads `@pixel/pptx` from JSR on first run.
- The `.tsx` file must `export const deck = ...` (the JSX Presentation element).
- Use `--json` for structured output: `{"ok": true, "file": "...", "size": 1234}`
- Output opens in PowerPoint, Google Slides, LibreOffice Impress, and Keynote.
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.pptx`.

## Support

Built by [Corespeed](https://corespeed.io). If you need help or run into issues:

- 💬 Discord: [discord.gg/mAfhakVRnJ](https://discord.gg/mAfhakVRnJ)
- 🐦 X/Twitter: [@CoreSpeed_io](https://x.com/CoreSpeed_io)
- 🐙 GitHub: [github.com/corespeed-io/skills](https://github.com/corespeed-io/skills/issues)
