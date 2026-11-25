---
name: chartatelier
display_name: ChartAtelier — Business Diagram Studio
display_name_en: ChartAtelier — Business Diagram Studio
description: Turn one sentence of intent into a presentation-grade business diagram, delivered as a high-resolution PNG plus an editable SVG.
description_en: Turn one sentence of intent into a presentation-grade business diagram, delivered as a high-resolution PNG plus an editable SVG.
version: 1.0.0
category: design-media
sub_categories:
  - key: pro-design
    name: Professional Design Delivery
tags: [business diagrams, architecture diagram, flowchart, infographic, SVG delivery]
tags_en: [business diagrams, architecture diagram, flowchart, infographic, SVG delivery]
icon: 📊
platforms: [WorkBuddy, QClaw, ima, Claude Code, Codex]
trigger_keywords: [architecture diagram, business chart, topology map, flowchart, timeline, infographic, comparison matrix, deck visual, tender exhibit, white paper figure, export SVG, high-res PNG]
author: DeepCraft Studio
license: Commercial
pay_skill: true
price_cny: "1.99"
---

# ChartAtelier — Business Diagram Studio

Turn one sentence of intent into a diagram that drops straight into a slide deck, a tender document or a white paper: a high-resolution PNG plus an editable SVG, in a light professional palette, with Chinese typography that stays sharp and never crowds.

## What This Is

- It closes the gap between "the structure is clear in my head" and "I cannot draw it": you get a finished diagram file, not a paragraph describing one you still have to lay out yourself.
- Every run ships five artifacts: `diagram.html` (single-file CSS and SVG), `diagram.svg` (editable vector), `diagram@2x.png` (long edge at least 3000 px), `qa-report.json` (five measured values) and a hand-off note of 80 to 200 words.
- Six families are covered: architecture, flow, topology, timeline, infographic and comparison matrix; each has a fixed skeleton, an element ceiling and a split rule, so output does not depend on improvisation.
- What separates it from asking a general model: palette, type scale, stroke weights, margins, export multiplier and acceptance thresholds are executable parameters, verified by script. Nothing ships before the self-check passes.

## When to Use It

- "I have to explain this system overhaul in one slide for the weekly meeting."
- "The tender needs an overall architecture diagram that still reads when printed in black and white."
- "Chapter three of the white paper needs a process diagram, seven or eight steps, and it cannot look crammed."
- "Two options, six dimensions, four alternatives each: make me a matrix."
- "A horizontal timeline for eight milestones, plus how these racks and links connect."

## When NOT to Use

- Illustrations, 3D renders, brand VI or poster art: this skill only builds structured diagrams.
- Accurate geographic maps: it shows relative position, not navigation-grade geography.
- More than 40 nodes on one canvas: split the diagram instead of squeezing text.
- No trustworthy data source: only `XX%` placeholders are allowed, never invented numbers.

## Quick Reference

| Situation | Use |
|---|---|
| Unsure which diagram type fits | `references/diagram-selection.md` |
| Color, type scale, spacing | `references/visual-spec.md` |
| Export PNG / target DPI | `references/render-pipeline.md` + `scripts/render_diagram.py` |
| Final defect pass | `references/qa-checklist.md` |

## Inputs and Outputs

| Field | Required | Notes |
|---|---|---|
| `requirement` | Yes | One sentence naming the subject and its relationship. Under 12 characters, go back to clarification instead of drawing |
| `diagram_type` | No | `architecture`, `flow`, `topology`, `timeline`, `infographic`, `matrix`, `swimlane` or `sequence`; empty means the rules in step 2 decide |
| `nodes` | No | Comma-separated list. Extracted from `requirement` when omitted; fewer than three after extraction means ask, never invent business nouns |
| `canvas` | No | `16:9` (default, logical 1520x856), `4:3` (1280x960) or `a4p` (1240x1754 portrait) |
| `scale` | No | Export multiplier, `2` (default) or `3` for print, large format or stage screens |
| `tokens`, `lang` | No | Brand accent and forbidden colours, which may override stroke and title colours only; `zh` (default), `en` or `bi` for bilingual pairs |

| File | Format | Specification |
|---|---|---|
| `diagram.html` | Single HTML | Inline CSS and SVG, no external assets, opens by double click |
| `diagram.svg` | SVG 1.1 | `width` and `height` in explicit pixels matching the viewBox; text stays as editable `<text>` |
| `diagram@2x.png` | PNG | 3040x1712 for 16:9; 2480x3508 for A4 portrait at about 300 DPI; long edge at least 3000 px |
| `diagram@3x.png` | PNG | Long edge at least 4500 px; produced only when `scale=3` |
| `qa-report.json` | JSON | Measured margins, crossings, text overflow, contrast and export size |

Minimum viable input is `requirement` alone, optionally plus `nodes`; every other field falls back to a default declared on the first line of the hand-off note. A run is complete only when it can be pasted (size and margins pass), edited (SVG text is still live) and audited (`qa-report.json` carries all five measurements).

## Workflow

### Step 1 - Clarify with five questions

Ask all five at once rather than trickling them out. Anything unanswered proceeds on the default, which is then declared in the hand-off note.

| Question | What it decides | Default when unanswered |
|---|---|---|
| Where will this appear: one slide, a Word tender, a full white-paper page, or a phone preview? | Canvas ratio and minimum type size | 16:9 single page, body 12 px |
| Who reads it, and from how far? | Density and type ceiling | Read at two metres, body 12 px, annotation 10 px |
| Which nouns must appear: system, module or metric names? | Node list and naming discipline | Extracted from the request; ask again below three |
| What is the dominant relationship: hierarchy, sequence, connection or quantity? | Diagram family | Decided by the rules in step 2 |
| What must stay consistent: palette, legend, numbering, units, version? | Reusable tokens and legend | This skill's default token table |

Pass condition: "where it goes", "dominant relationship" and "the nouns" are answered before drawing starts, then stop asking and fold anything extra into the node list. Failure handling: after two rounds of "just decide for me", run the full default set and open the hand-off note with "delivered to default specification".

### Step 2 - Choose the structure

Pick the family from signal words in the request, never from taste. The full table and split thresholds live in `references/diagram-selection.md`.

| Signal in the request | Family | Skeleton | Ceiling | Not for |
|---|---|---|---|---|
| Layers, upper tier, lower tier, access layer | Architecture | Horizontal layer bands with parallel cards | 5 cards per layer, 18 total | Expressing sequence |
| First, then, after that, if so, where it stalls | Flow | Vertical spine with decision branches | 8 spine steps, 3 decisions | Parallel data flows |
| How it connects, links, cabling, which path | Topology | Zone frames, nodes, orthogonal links | 14 nodes, 8 inter-zone links | Approval workflows |
| Who does what and when, across roles | Swimlane or sequence | Role lanes over stages, or message rows | 5 lanes and 6 stages; 6 participants and 12 messages | Capacity comparison |
| Phase one, milestones, from X to Y | Timeline | Single axis with alternating labels | 8 nodes | Hierarchy |
| One idea or three numbers on a page | Infographic | Hero visual plus data blocks | 5 data blocks | More than ten concepts |
| How A and B differ, which to pick | Comparison matrix | Rows are options, columns are dimensions | 6 dimensions, 4 options | Process flow |

Three hard rules: "connect, link, cabling" means topology; "first, then, if" means flow; "layer, upper, lower" means architecture. If all three fire, the subject of the sentence decides the primary family and the rest become legend entries.

Failure handling: never shrink type to force an oversized set into one frame. Split into a primary figure for the conclusion and a secondary figure for detail, and each must still pass the full self-check.

### Step 3 - Layout and palette

The complete token table, spacing scale and legend rules are in `references/visual-spec.md`. These are the non-negotiable points.

- Canvas logical 1520x856 for 16:9 with a 32 px safe margin, everything snapping to an 8 px grid (4, 8, 16, 24, 32, 48); page `#f1f5f9`, card `#ffffff` with a 1 px `#e2e8f0` border and 16 px radius.
- Semantic colours are fixed and may not drift inside one deliverable: blue for access or channel, green for core business, violet for data or reconciliation, rose for risk or error, amber for settlement or contract, slate for external or regulator, dashed yellow for a container boundary.
- Titles `#0f172a` at weight 600, body `#475569`, annotations `#64748b`; body and annotation contrast against white reaches at least 4.5 to 1.
- Primary connectors 1.2 to 1.5 px, auxiliary dashes 1.1 px; arrowheads 10 by 7 with `refX=9` and `refY=3.5`; dash rhythm 5 to 7 px on, 4 to 5 px off; `rx=10` for nodes and `rx=14` for containers.
- Node titles 14 to 15 px at weight 600, body 12 px, annotations 10 to 11 px, nothing below 10 px in the final file; line height 1.5 to 1.6, and never add positive tracking to Chinese text, because anything above 0.02 em pulls the characters apart.
- Legend horizontal, bottom right, outside any container frame, six entries at most, swatches 10 by 10 px; one numbering scheme only, and units follow the value inside parentheses.

### Step 4 - Plan coordinates, then draw

Produce a coordinate table before writing any SVG: every node's `x`, `y`, `w`, `h`, every connector's start, end and elbows, and the vertical band each row occupies.

- Write arrows and connectors before the node rectangles so they render underneath and are never hidden by a fill.
- Orthogonal routes may only travel through gaps between rows: `M x1 y1 L x1 gapY L x2 gapY L x2 y2`. A horizontal segment at a y value occupied by a node is forbidden.
- Centre text with `text-anchor="middle"` and a hand-computed offset (`dy="0.35em"`); renderers disagree about `dominant-baseline`.
- Wrap on semantic boundaries, not by character count: 14 CJK characters or 28 Latin characters per line, then wrap or widen the box. Bilingual pairs put Chinese on top, English below at line height 1.3 and two pixels smaller, each in its own `<text>` node.

Pass condition: every shape traces back to a row in the coordinate table, and a dashed container frame enclosing its own children is expected rather than an overlap defect. Failure handling: when a connector cuts through a box, move the elbow instead of hiding it behind z-order, then re-run step 5.

### Step 5 - Self-check, five items, all scripted

| Check | Pass condition | On failure |
|---|---|---|
| Margins | Saturated content box covers at least 95 percent of the width and 93 percent of the height, 1 to 3 percent per side | Tighten the viewBox to content plus 10 to 20 px and remove default page padding |
| Crossings | Zero intersections between orthogonal routes; a bridge with a legend note if one is unavoidable | Re-route through row gaps, or bring one side around as a dashed detour |
| Text overflow | Every `<text>` box sits inside its parent rectangle within 2 px | Shorten, then raise the box, then wrap. Never reduce type size |
| Contrast | Body and annotation at least 4.5 to 1, large titles at least 3 to 1 | Step the title colour one shade darker in the same family |
| Export size | PNG width equals logical width times multiplier within 2 px, and the long edge is at least 3000 px | Reset the window size or device scale factor; never upscale afterwards |

Commands are in `references/qa-checklist.md`. All five green is the gate for export, and the order is fixed: geometry, typography, colour, export, because a colour change forces the geometry to be re-tested.

### Step 6 - Render and export

Extract a standalone SVG with explicit pixel `width` and `height` first, then screenshot. Skipping that step yields content squeezed into the top-left corner with white everywhere else. Full parameters and fallbacks are in `references/render-pipeline.md`.

```bash
python scripts/render_diagram.py diagram.html --out diagram@2x.png --scale 2   # preferred: Playwright
chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1520,856 \
  --force-device-scale-factor=2 --screenshot=diagram@2x.png file:///ABS/PATH/diagram.html
```

- Font stack is fixed: `'Inter', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif`; on Linux without PingFang or YaHei it falls back to Noto Sans SC or Source Han Sans, and never to `monospace`, which forces uniform widths and destroys alignment.
- Wait for `document.fonts.ready` plus 300 ms before capturing, and for `networkidle` whenever a web font loads, or the capture picks up the fallback face.
- DPI arithmetic: pixels equal millimetres divided by 25.4, times DPI, so an A4 page 210 mm wide at 300 DPI needs 2480 px, which is logical 1240 at 2x. Verify every PNG afterwards, because "the file was written" does not mean "the size is right".

### Step 7 - Deliver

Fixed folder, fixed naming: lowercase letters, digits and hyphens only, with a version suffix, never a client name or project code. The folder is `chartatelier-<topic>/` and holds `diagram.html`, `diagram.svg`, `diagram@2x.png`, `qa-report.json` and `handoff.md`.

Delivery order: PNG preview first, then a file list with path, dimensions and byte size, then three to five bullets covering family, palette basis, type scale and reproduction command. Five items are mandatory: the PNG (no clipping, no blur, no empty field), the SVG (change one character in a vector editor to prove text is not outlined), the HTML (opens by double click, console clean), the QA report (all five values inside threshold) and the hand-off note. Final pass: view the PNG at 25 percent for hierarchy, then at 100 percent for blurry text and broken arrowheads.

## Output Format

```
Canvas: 16:9 (1520x856) | 4:3 (1280x960) | A4 portrait
Margins: 64px frame, >= 48px between nodes
Type: title 28-34px, node 16-18px, note 12-14px
Legend: top-right, <= 6 items, colors matched to nodes
Export: PNG at 2x
```

## Quality Gate

- [ ] The PNG long edge is at least 3000 px, its width equals logical width times multiplier within 2 px, and it reaches 4500 px when `scale=3`.
- [ ] Saturated content box covers at least 95 percent of the width and 93 percent of the height, with 1 to 3 percent margin per side.
- [ ] Text overflow count is zero: every `<text>` box stays inside its parent rectangle within 2 px.
- [ ] Sibling overlap count is zero; container frames overlapping their own children do not count.
- [ ] Orthogonal route intersections are zero, or every bridge is documented in the legend.
- [ ] Nothing extends beyond the viewBox, rotated labels included, and the export shows no clipping.
- [ ] Body and annotation contrast is at least 4.5 to 1; large titles at least 3 to 1.
- [ ] The smallest type in the final image is at least 10 px, which is 20 device pixels at 2x.
- [ ] SVG text is real `<text>`, and `width` and `height` are explicit pixels, so words stay editable.
- [ ] Legend, numbering, units and footer version agree with the body text, with no page-count contradictions.

## Scope and Limits

- No photo-realistic illustration, 3D rendering, skeuomorphic icons or brand identity redesign; palette stays tied to the tokens supplied.
- No accurate map that needs real geographic coordinates, only schematic zone blocks and logical links.
- When a set exceeds the ceiling for its family the figure is split; compressing type below 10 px to fit everything into one frame is refused.
- Business figures are never invented: for unpublished operating data the diagram carries structure and placeholders such as `XX%` for the caller to fill.
- No promise of approval by a review board or of visual taste, only that size, margins, overflow and contrast are measurable and pass.

## Common Traps

- **Text touching borders**: size node boxes from content plus a 16px inner padding.
- **Low contrast on light themes**: keep body text at >= 4.5:1 against its background.
- **Arrows crossing nodes**: route connectors so they never pass through another node.
- **Legend out of sync**: re-check legend colors against node colors before export.

## Delivery Example

Input:

```
One-line request: show how an inbound request moves through triage, manual review and follow-up filing, for one slide
Nodes: intake, automated triage, manual review, follow-up filing, exception hold
Constraints: 16:9, light palette, readable at two metres
```

Output skeleton:

```
chartatelier-inbound-flow/
  diagram.html            inline CSS and SVG, double click to open
  diagram.svg             viewBox 1520 856, explicit pixel width and height
  diagram@2x.png          3040 x 1712, 1.1 MB
  qa-report.json          cover 96.4/94.1 percent, overflow 0, siblingOverlap 0, crossings 0, contrast 7.1
  handoff.md
    - Family: vertical flow, four-step spine plus one rejection loop
    - Palette: access #f0f9ff / #38bdf8, core #f0fdf4 / #4ade80, exception #fff1f2 / #fda4af
    - Type: node titles 14 px, detail 12 px, caption 11 px
    - Reproduce: python scripts/render_diagram.py diagram.html --out diagram@2x.png --scale 2
```

## Related Skills

- **TableScribe (paid)**: clean the source table before drawing.
- **PolicyForge (paid)**: write the conclusion there, draw the figure here.

## Reference Files

- `references/diagram-selection.md`: signal words, skeleton, element ceiling, misuse and split thresholds for eight families.
- `references/visual-spec.md`: light-theme tokens, type scale, spacing grid, stroke and arrowhead values, legend and bilingual rules.
- `references/render-pipeline.md`: HTML and SVG to PNG parameters, DPI arithmetic, fallback chain and recurring failure modes.
- `references/qa-checklist.md`: executable criteria for the five checks, verification snippets and the pre-delivery tick list.
