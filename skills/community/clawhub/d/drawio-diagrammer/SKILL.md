---
name: drawio-diagrammer-skill
description: Generate beautiful draw.io diagrams with a mandatory visual QA loop. Covers flowcharts, ERD, architecture, sequence, and class diagrams. Use when user requests any diagram or visualization.
---

# draw.io Diagrammer Skill

## When to use this skill
- User requests a flowchart, process map, or workflow diagram
- User requests an ERD, database diagram, or entity relationship model
- User requests an architecture, system, or component diagram
- User requests a class, sequence, or UML diagram
- User says "draw.io", "diagram", "flowchart", "visualize this process"
- User asks to update, fix, or extend an existing `.drawio` file

---

## MANDATORY — Read before generating anything

1. **Detect diagram type first** — see diagram-types/ references before writing XML
2. **Apply universal box style standards** — see `references/box-style-standards.md`
3. **All positions are hardcoded** — no auto-layout exists in draw.io XML
4. **Run the visual review loop after every export** — see `references/visual-review-protocol.md`
5. **Never declare done without a visual pass** — export PNG, read it, fix it, repeat

---

## Diagram type detection

| User says... | Reference file |
|---|---|
| "flowchart", "process", "steps", "workflow", "SOP" | `references/diagram-types/flowchart.md` |
| "ERD", "database", "tables", "entities", "foreign key" | `references/diagram-types/erd.md` |
| "architecture", "system", "components", "services" | `references/diagram-types/layout.md` |
| "class", "UML", "inheritance", "methods", "attributes" | `references/diagram-types/class.md` |
| "sequence", "interaction", "lifeline", "actor calls" | `references/diagram-types/sequence.md` |

---

## Standard generation workflow

### Step 1 — Load type reference
Read the correct `references/diagram-types/` file before writing any XML.

### Step 2 — Plan all elements
List every node, connection, and section before coding. Do not improvise layout mid-build.

### Step 3 — Apply universal box style
Every node must include the universal spacing attributes from `references/box-style-standards.md`.

### Step 4 — Create output folder and write XML
```bash
mkdir -p ./diagrams
```
Save to:
```
./diagrams/<diagram-name>.drawio
```

Pre-save checklist:
- [ ] All `mxCell` elements have unique sequential numeric IDs
- [ ] Universal box spacing applied to every node style: `spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;`
- [ ] Arrows use chained routing, not fan-out from single source to many targets
- [ ] Minimum 15–20px gap between any two boxes (verify sub-item list bottom vs next section top)
- [ ] Heights calculated with the formula in box-style-standards.md (×16px per line at fontSize=10)
- [ ] Wide-text panels (notes, descriptions) are 530px+ wide — not 460px or less
- [ ] No literal `\n` in value attributes — use `&#xa;` for line breaks
- [ ] `verticalAlign=top` on all multi-line content boxes

### Step 5 — Export PNG and run visual review loop
```bash
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format png --output ./diagrams/<name>.png --scale 2 --border 30 ./diagrams/<name>.drawio
```
Then follow the full protocol in `references/visual-review-protocol.md`.

### Step 6 — Deliver

Send the PNG to the user first. For larger diagrams, send section screenshots (top, middle, bottom) before the full image.

Then ask which additional formats they want:

```
The diagram is ready. Which format would you like?

1 — PNG image (ready to view)
2 — .drawio file (editable in draw.io)
3 — SVG (scalable vector)
4 — PDF
5 — All of the above

Reply with the number(s) of your choice.
```

For Drive delivery or custom output paths, follow `references/workflow-sop.md`.

---

## CLI reference

```bash
# macOS — Export PNG (standard)
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format png --output <out.png> --scale 2 --border 30 <file.drawio>

# macOS — Export high-res PNG
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format png --output <out.png> --scale 3 --border 30 <file.drawio>

# macOS — Export SVG
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format svg --output <out.svg> <file.drawio>

# macOS — Export PDF
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format pdf --output <out.pdf> <file.drawio>

# Linux / headless — Export PNG
xvfb-run -a drawio --export --format png --output <out.png> --scale 2 --border 30 <file.drawio>

# Linux / headless — Export SVG
xvfb-run -a drawio --export --format svg --output <out.svg> <file.drawio>
```
