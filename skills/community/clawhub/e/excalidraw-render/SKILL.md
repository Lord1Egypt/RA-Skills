---
name: excalidraw-diagram
description: Create professional Excalidraw diagrams — flowcharts, architecture diagrams, workflows, systems, processes, or concepts. Use when user asks to "create a diagram", "draw a flowchart", "visualize a process", "make a flow diagram", "architecture diagram", "excalidraw", "technical diagram", or discusses workflow/process visualization. Supports quick DSL-based flowcharts and comprehensive hand-crafted JSON diagrams. Built-in PNG rendering and PDF export.
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - uv
        - node
        - npm
    homepage: https://clawhub.ai/skills/excalidraw-render
---

# Excalidraw Diagram Creator

Generate `.excalidraw` files — from quick flowcharts to comprehensive technical diagrams.

## ⚠️ Golden Rule

**Every diagram MUST be rendered to PNG and visually inspected before delivery.** Look at the actual image — check that text fits inside boxes, no elements overlap, arrows connect correctly, and spacing is balanced. Fix the JSON and re-render until it looks professional. See the **Render & Validate** section. No exceptions.

---

## Depth Gate (Do This First)

| Need | Approach | Time |
|------|----------|------|
| Simple flowchart, decision tree, linear process | **Quick Path** — CLI DSL | ~1 min |
| Architecture, multi-zoom technical, evidence artifacts | **Full Path** — hand-crafted JSON | ~10 min |

---

## Quick Path: CLI DSL Flowcharts

For straightforward flows, use `@swiftlysingh/excalidraw-cli` (installed locally by `setup.sh`):

```bash
excalidraw-cli create --inline "DSL" -o output.excalidraw
```

> **Note:** If `excalidraw-cli` is not in your PATH after setup, use:
> `"$SKILL_DIR/.npm/node_modules/.bin/excalidraw-cli"` or re-run `setup.sh`.

### DSL Syntax

| Syntax | Shape | Use For |
|--------|-------|---------|
| `[Label]` | Rectangle | Process steps |
| `{Label?}` | Diamond | Decisions |
| `(Label)` | Ellipse | Start/End |
| `[[Label]]` | Database | Data storage |
| `->` | Arrow | Connection |
| `-> "text" ->` | Labeled arrow | Conditional |
| `-->` | Dashed arrow | Optional path |

Directives: `@direction LR|TB|RL|BT`, `@spacing 60`

### DSL Example

```bash
excalidraw-cli create --inline "$(cat <<'EOF'
@direction TB
(Start) -> [Receive Request] -> {Authenticated?}
{Authenticated?} -> "yes" -> [Process Request] -> (Success)
{Authenticated?} -> "no" -> [Return 401] -> (End)
EOF
)" -o auth-flow.excalidraw
```

CLI options: `-d LR` (direction), `-s 80` (spacing), `--format dot` (DOT/Graphviz input).

After generation, **always render and validate** (see Render section below). Fix overlaps or clipping in the JSON if needed.

---

## Full Path: Hand-Crafted JSON Diagrams

For comprehensive, professional diagrams. Read these references as needed:

- **`references/color-palette.md`** — All colors (read FIRST, every time)
- **`references/element-templates.md`** — Copy-paste JSON for each element type
- **`references/json-schema.md`** — Full property reference
- **`references/layout-rules.md`** — Anti-overlap spacing and text-sizing rules ⚠️ READ THIS

### Design Process

1. **Assess depth** — simple/conceptual vs. comprehensive/technical
2. **Research** (technical diagrams) — look up real specs, event names, API formats
3. **Map concepts to visual patterns** — see Pattern Library below
4. **Sketch mentally** — trace how the eye moves through the diagram
5. **Generate JSON section-by-section** — see Large Diagram Strategy
6. **Render & validate** — MANDATORY loop (see below)

### JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": 20 },
  "files": {}
}
```

### Core Rules

- `fontFamily: 3`, `roughness: 0`, `opacity: 100` on all elements
- `text` property = ONLY readable words (no markup)
- **Size containers to fit text** — see `references/layout-rules.md`
- **Minimum 40px gap** between elements — see `references/layout-rules.md`
- Default to free-floating text; use containers only when meaningful (<30% text in boxes)

### Visual Pattern Library

| Concept Behavior | Pattern |
|------------------|---------|
| One source → many outputs | **Fan-out** (radial arrows from center) |
| Many inputs → one output | **Convergence** (arrows merging) |
| Hierarchy/nesting | **Tree** (lines + free-floating text) |
| Sequence of steps | **Timeline** (line + dots + labels) |
| Feedback loop | **Spiral/Cycle** (arrow returning to start) |
| Abstract state | **Cloud** (overlapping ellipses) |
| Transformation | **Assembly line** (before → process → after) |
| Comparison | **Side-by-side** (parallel structures) |
| Phase changes | **Gap/Break** (visual whitespace) |

### Shape Meaning

| Concept | Shape |
|---------|-------|
| Labels, descriptions | Free-floating text (no container) |
| Timeline markers | Small ellipse (12px) |
| Start/trigger | Ellipse |
| End/output | Ellipse |
| Decision | Diamond |
| Process/action | Rectangle |

### Evidence Artifacts (Technical Diagrams)

| Artifact | Rendering |
|----------|-----------|
| Code snippets | Dark rect (`#1e293b`) + syntax-colored text |
| JSON/data | Dark rect (`#1e293b`) + green text (`#22c55e`) |
| Event sequences | Timeline (line + dots + labels) |
| UI mockups | Nested rectangles |

### Large Diagram Strategy

Build JSON **one section at a time** (Claude has ~32k token output limit):

1. Create base file + first section
2. Add one section per edit — use descriptive IDs (`"trigger_rect"`, `"auth_arrow"`)
3. Namespace seeds by section (100xxx, 200xxx, etc.)
4. Update cross-section bindings as you go
5. Review the whole before rendering

### Multi-Zoom (Comprehensive Diagrams)

- **Level 1** — Summary flow (simplified overview)
- **Level 2** — Section boundaries (labeled regions)
- **Level 3** — Detail (evidence artifacts, code snippets, real data)

---

## Render & Validate (MANDATORY)

**Every diagram must be rendered and visually inspected before delivery.** This catches overlap, text clipping, and spacing issues that are invisible in JSON.

### Render Command

```bash
cd ~/.openclaw/skills/excalidraw-diagram && uv run python render_excalidraw.py <path-to-file.excalidraw>
```

Outputs a PNG next to the `.excalidraw` file. Use the **Read tool** to view it.

### First-Time Setup

```bash
cd ~/.openclaw/skills/excalidraw-diagram
bash setup.sh                              # builds local Excalidraw bundle (requires node/npm)
uv sync && uv run playwright install chromium
```

### The Loop (repeat until professional)

1. **Render** the PNG
2. **View the image** with the Read tool — actually look at it
3. **Inspect systematically:**
   - Does every label fit cleanly inside its box? (no clipping, no overflow)
   - Are all boxes/shapes clearly separated? (no overlapping edges)
   - Are arrows connecting the right elements without crossing through others?
   - Is spacing even and consistent between similar elements?
   - Is text large enough to read?
   - Does the overall layout look balanced and professional?
4. **Fix the JSON** for every issue found — widen containers, adjust x/y, add arrow waypoints, increase gaps
5. **Re-render and re-view** — look at the new PNG
6. **Repeat** until every issue is resolved (typically 2-4 iterations, sometimes more)

**Do not skip this loop.** JSON coordinates are approximate — you will almost always find issues on the first render. The visual check IS the quality gate.

### Stop When

- No text overflow or overlapping
- Arrows route cleanly
- Consistent spacing, balanced composition
- You'd show it without caveats

---

## PNG & PDF Export

### PNG (for Word, presentations, sharing)

The render script outputs high-res PNG (2x scale by default):

```bash
cd ~/.openclaw/skills/excalidraw-diagram && uv run python render_excalidraw.py diagram.excalidraw --output diagram.png --scale 3
```

Options: `--scale 3` (3x for print), `--width 2560` (wider viewport).

### PDF (for documents, printing)

Convert PNG to PDF:

```bash
# ImageMagick (most common)
convert diagram.png -density 150 diagram.pdf

# Or with a white background and margins
convert diagram.png -gravity center -background white -extent 110%x110% -density 150 diagram.pdf
```

For multi-page or A4/Letter sizing:

```bash
convert diagram.png -resize 1800x -gravity center -background white \
  -extent 2100x2970 -units PixelsPerInch -density 254 diagram-a4.pdf
```

---

## Quality Checklist

### Layout & Overlap
- [ ] All text fits within containers (used layout-rules.md sizing formula)
- [ ] Minimum 40px gap between all elements
- [ ] Arrows don't cross through elements
- [ ] Even spacing between similar elements
- [ ] Balanced composition (no voids or overcrowding)

### Visual
- [ ] `roughness: 0`, `opacity: 100`, `fontFamily: 3` everywhere
- [ ] Colors from `references/color-palette.md`
- [ ] Text readable at export size
- [ ] Clear visual flow (eye path)

### Technical (if applicable)
- [ ] Real specs/event names/API formats (not placeholders)
- [ ] Evidence artifacts included
- [ ] Multi-zoom levels present

### Export
- [ ] Rendered to PNG and visually validated
- [ ] PNG/PDF delivered if user needs it
