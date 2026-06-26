---
name: corespeed-pptx
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

## Writing Slides

Create a `.tsx` file. It must export a `deck` variable:

```tsx
/** @jsxImportSource @pixel/pptx */
import { Align, clr, Presentation, Slide, Text, u } from "@pixel/pptx";

export const deck = (
  <Presentation title="My Deck">
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

## Example: Multi-Slide Deck

```tsx
/** @jsxImportSource @pixel/pptx */
import {
  Align, Chart, clr, Column, Presentation, Row, Shape, Slide,
  Stack, Table, Text, u, type Style,
} from "@pixel/pptx";

const title: Style = {
  fill: { kind: "solid", color: clr.hex("1F4E79") },
  fontSize: u.font(28), fontColor: clr.hex("FFFFFF"), bold: true,
  verticalAlign: "middle", padding: u.in(0.2),
};

export const deck = (
  <Presentation title="Q2 Report" layout={{ rowGap: u.in(0.3), columnGap: u.in(0.3) }}>
    <Slide background={{ kind: "solid", color: clr.hex("F7F4EE") }}>
      <Column>
        <Shape preset="roundRect" h={u.in(1.2)} style={title}>
          <Text.P>Q2 Report</Text.P>
        </Shape>
        <Row>
          <Stack grow={1}>
            <Shape preset="roundRect" style={{ fill: { kind: "solid", color: clr.hex("FFFFFF") } }} />
            <Align x="center" y="center" w={u.in(4)} h={u.in(3)}>
              <Chart.Bar
                data={[
                  { q: "Q1", rev: 8 }, { q: "Q2", rev: 12 },
                  { q: "Q3", rev: 10 }, { q: "Q4", rev: 15 },
                ]}
                category="q"
                series={[{ name: "Revenue", value: "rev", color: clr.hex("2678B4") }]}
                labels
              />
            </Align>
          </Stack>
          <Table cols={[u.in(1.5), u.in(1)]} grow={1}>
            <Table.Row height={u.in(0.4)}>
              <Table.Cell style={{ bold: true }}>Metric</Table.Cell>
              <Table.Cell style={{ bold: true }}>Value</Table.Cell>
            </Table.Row>
            <Table.Row height={u.in(0.4)}>
              <Table.Cell>Revenue</Table.Cell>
              <Table.Cell>$1.2M</Table.Cell>
            </Table.Row>
          </Table>
        </Row>
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
