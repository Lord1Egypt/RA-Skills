# DESIGN.md — archviz-skills Design System

Plain-text design system for all visualizations, structured in the [Stitch DESIGN.md format](https://stitch.withgoogle.com/docs/design-md/format/) (9 sections + extended sections), following the VoltAgent/awesome-design-md pattern.

This file is the visual truth source. `SKILL.md` tells agents how to execute; this file tells them what the output should look and feel like. §9 is the copy-paste prompt layer. `preview.html` is the visual catalog.

---

## 1. Visual Theme & Atmosphere

archviz-skills diagrams read like figures in a well-set academic book — quiet, gridded, and deliberately under-decorated. The canvas is warm paper, not a whiteboard: every neutral carries a beige-stone undertone, lines are hairline-thin, and color appears only when it encodes meaning. Where typical AI-generated diagrams shout (purple gradients, rainbow nodes, centered symmetry), these diagrams state — structure carries the argument, decoration is absent by policy.

The signature move is **restraint as a dial, not a default**: every diagram starts from a brief read and three explicit dials (COMPLEXITY / DENSITY / RESTRAINT), so the same content can be set austere for a paper or looser for a teaching slide — but it is never shipped on an unexamined default theme. The second signature is **text-first survivability**: the primary artifact is plain text (.mmd, ASCII) that renders in Obsidian, GitHub, and a terminal; HTML, Python, and 3D are reserved for deliverables that earn them.

**Key characteristics:**
- Warm paper neutrals (`#f5f0eb`, `#f5f5f4`, `#a8a29e`) — no cool grays, no pure black/white surfaces
- One accent maximum per diagram set — International Klein Blue (`#002FA7`) or Lemon (`#FFD500`), never both
- Hairline discipline: 1px default strokes, 2px reserved for the single accent
- Typography weight inverts with size (越大越细，越小越粗) — large titles ExtraLight, small labels SemiBold
- Sharp corners, no emoji, no gradients, no shadows in diagram bodies
- Contrast is computed, not guessed: the luminance rule decides light vs dark text
- Anti-slop: no purple defaults, no rainbow nodes, no flowchart-for-everything, no pie

### Agent-Readable Contract

Every generated diagram should be understandable as a compact design system, not just a code block. Before output, the agent must be able to point to:

| Contract layer | Required decision | Failure mode if missing |
|---|---|---|
| Visual theme | restrained / academic / teaching / technical / spatial | Generic AI diagram |
| Tokens | surface, text, border, accent, line weight | Inconsistent color or low contrast |
| Component roles | node, group, edge, legend, annotation | Decorative shapes with no semantics |
| Layout behavior | direction, max nodes, split rule, fallback | Overflow and unreadable graphs |
| Validation | render target, contrast, overlap, fallback | Pretty source that fails in the user's viewer |

`awesome-design-md` works because each `DESIGN.md` captures a real visual language: overview, tokens, typography, components, layout, guardrails, responsive behavior, and agent guide. `archviz-skills` applies the same idea to information visualization: every chart family has tokens, semantics, constraints, and validation gates.

---

## 2. Color Palette & Roles

### Shared Neutrals (all systems)

| Name | Hex | Role |
|---|---|---|
| **Warm Paper** | `#f5f0eb` | Default surface — node fill in the Warm Paper system |
| **Paper Beige** | `#e8e4e0` | Legacy/secondary surface; 3D floor slab and ground plane |
| **Mist White** | `#f5f5f4` | Swiss surface; light text on accent/dark fills ONLY |
| **Stone Gray** | `#a8a29e` | Default border, line color, 3D wireframe |
| **Pebble** | `#d6d3d1` | Tertiary fill, Swiss border, hemisphere ground light |
| **Ink Navy** | `#1B365D` | Primary text on light warm surfaces |
| **Warm Ink** | `#44403c` | Secondary text, muted nodes |
| **Charcoal** | `#292524` | Stone Mono text |
| **Near Black** | `#0a0a0a` | Text on IKB/Lemon system surfaces |

### Accents (max 1 per diagram set)

| Name | Hex | Role |
|---|---|---|
| **International Klein Blue (IKB)** | `#002FA7` | Signature accent — core connections, sovereign node border, active floor (3D). Pair with Mist White text on solid fills. |
| **Lemon** | `#FFD500` | Tech-flavored accent alternative. Pair with Near Black text. |

### Palette Systems (one system per diagram set)

| System | surface | text | border | accent | Use |
|---|---|---|---|---|---|
| **Warm Paper** | `#f5f0eb` | `#1B365D` | `#a8a29e` | — | Default, academic |
| **Swiss Neutral** | `#f5f5f4` | `#1B365D` | `#d6d3d1` | — | Clean, print |
| **IKB Accent** | `#e4e8f0` | `#0a0a0a` | `#94a3b8` | `#002FA7` | guizang Swiss |
| **Lemon Accent** | `#f0f4e0` | `#0a0a0a` | `#a8b898` | `#FFD500` | Tech |
| **Stone Mono** | `#e7e5e4` | `#292524` | `#a8a29e` | — | Austerity |
| **Editorial Parchment** | `#f5f4ed` | `#141413` | `#e8e6dc` | `#c96442` Terracotta | Cards, covers, publishable HTML ([claude-design-card](https://github.com/geekjourneyx/claude-design-card) lineage) |

**Editorial Parchment notes** (full rules → `references/editorial-parchment-language.md`):
- Terracotta replaces IKB as the single accent when the brief is editorial / card / cover — never both in one set.
- Surfaces alternate: Parchment canvas → Ivory card → Dark-Surface band (`#30302e`) → optional Terracotta band (one per page).
- Typography: serif display at weight 400–500 (never 700) + system-ui body; book line-height 1.55–1.65.
- Elevation: hairline warm borders + optional ring shadow on card container only — not on chart marks.

**Contrast rule (mandatory, computed)**: `luminance = 0.299R + 0.587G + 0.114B`. Fill luminance < 128 → light text (Mist White); ≥ 128 → dark text (Ink Navy / Near Black / Charcoal).

**Token gate**: Any palette with surface luminance ≥128 must use dark text. All five system surfaces are light → they always take dark text. **Never pair warm light surfaces with near-white text.** Mist White as text is legal only on accent fills (IKB) or genuinely dark fills.

### Dark Mode Palettes

Mirror every light palette with a dark counterpart. Same accent, inverted surface/text.

| System | surface | text | border | accent | Use |
|---|---|---|---|---|---|
| **Warm Paper Dark** | `#1a1814` | `#e8e4e0` | `#44403c` | — | Default dark |
| **Swiss Neutral Dark** | `#0a0a0a` | `#d6d3d1` | `#333333` | — | Clean dark |
| **IKB Accent Dark** | `#0d1117` | `#c9d1d9` | `#30363d` | `#58a6ff` | guizang dark |
| **Lemon Accent Dark** | `#0d1117` | `#c9d1d9` | `#30363d` | `#e3b341` | Tech dark |
| **Stone Mono Dark** | `#1c1917` | `#d6d3d1` | `#44403c` | — | Austerity dark |

**Dark mode rules:**
- Same accent hue, lighter tint (IKB `#002FA7` → `#58a6ff`; Lemon `#FFD500` → `#e3b341`)
- Surface: near-black with warm undertone (never pure `#000000`)
- Text: light gray (never pure `#ffffff`)
- Border: 1-2 stops lighter than surface
- Diagram init: swap `primaryColor`/`primaryTextColor`/`primaryBorderColor` to dark values
- Auto-detect: use CSS `prefers-color-scheme: dark` for HTML templates; manual toggle for Mermaid

**Mermaid dark init:**
```
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a1814', 'primaryTextColor': '#e8e4e0', 'primaryBorderColor': '#44403c', 'lineColor': '#58a6ff', 'tertiaryColor': '#2a2520', 'fontSize': '13px'}}}%%
```

**Rules:** Max 1 accent family — vary lightness, never hue. No AI-purple. Same document = same palette. Gradient-free: emphasis comes from the single accent, border weight, and whitespace.

---

## 3. Typography Rules

**Principle: 越大越细，越小越粗** — the larger the text, the lighter the weight.

| Role | Size | Weight | Notes |
|---|---|---|---|
| Diagram title | 15–16px | 200 (ExtraLight) | One per diagram, sentence case |
| Node label / body | 13–14px | 300 (Light) | ≤6 words / ≤8 Chinese chars |
| Small label / caption / axis | 11–13px | 500–600 (SemiBold) | Legends, units, annotations |
| ASCII mode | monospace | — | Max 80 columns |

- Labels: ≤6 words / ≤8 Chinese chars / no ALL CAPS / no full sentences (detail goes in the caption)
- One language per diagram — never mix Chinese and English labels in the same diagram
- Caption = finding, not title: "Sales dropped 30% in Q3", not "Q3 Sales Chart"
- Numbers in HTML/Python outputs: tabular figures where the library allows

---

## 4. Component Stylings

### Nodes (shape = semantic role, never decoration)

| Role | Mermaid | ASCII | Styling |
|---|---|---|---|
| Process | `[]` | `[text]` | surface fill, 1px Stone border |
| Important / core | `(( ))` | `[[text]]` | surface fill, 2px accent border (the one emphasis) |
| Decision | `{}` | `{text}` | surface fill, 1px border |
| Data / artifact | `[[]]` | `<text>` | Pebble fill |
| Actor | `(( ))` | `o` | 1px border |

**ASCII rule**: No box-drawing characters (┌─┐╔═╗╰─╯等) — they garble in non-monospace contexts. Use plain `[text]`, `-->`, `|` only.

- Border radius: sharp (0) by default — never mix radii in one diagram
- Icons: max 1 per group; never emoji

### Edges

| Type | Style | Meaning |
|---|---|---|
| Primary | solid `─────►` | Main flow |
| Secondary | dashed `- - -►` | Optional / feedback path |
| Emphasized | 2px accent / `═════►` | The single highlighted relation |
| Labeled | text on edge | Explicit semantics (rituals, conditions) |

Legend mandatory if >2 edge types appear.

### Groups / Subgraphs

Max 4–5 per diagram. Short noun titles. Non-symmetric layout unless content demands symmetry. 1px Stone border, no fill or faint Pebble fill.

### Gantt bars (hard rules)

Codes only inside the block (V1.1, A1) · full names in a mandatory table immediately after · ASCII fallback always included · min bar 3w · 3–6 tasks per section.

### Tables

The preferred "chart" for ≤5 items or 2–3 way comparisons. Plain Markdown, no styling tricks.

### Mermaid init (the token carrier)

```
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#f5f0eb','primaryTextColor':'#1B365D','primaryBorderColor':'#a8a29e','lineColor':'#a8a29e','tertiaryColor':'#d6d3d1','fontSize':'13px'}}}%%
```

Never ship the default theme. If you change `primaryColor`, recompute `primaryTextColor` with the contrast rule.

---

## 5. Layout Principles

**Three dials** (baseline 4/3/8):

| Dial | Default | Range | Meaning |
|---|---|---|---|
| COMPLEXITY | 4 | 1–10 | ≤25–50 nodes at default; >50 → split |
| DENSITY | 3 | 1–10 | Generous whitespace at default |
| RESTRAINT | 8 | 1–10 | Monochrome + one accent at default |

Inference: "academic" → 3-5/2-3/9-10 · "playful" → 5-8/3-5/3-5 · "data report" → 6-8/6-8/5-7

**Preferred types (compatibility first):**
- System/layered → flowchart TD + subgraph (primary for .md source)
- Hierarchical → mindmap (strip `<br/>`, use `/` separators)
- Process → flowchart LR; hierarchy → TD
- Scoring → xychart-beta or mindmap
- Subgraphs max 4-5, labels ≤8 Chinese chars, non-symmetric

**Whitespace philosophy**: whitespace is the grid made visible. Never fill space; a sparse diagram with a sharp caption beats a dense one. Subgraphs breathe; labels never touch borders.

---

## 6. Depth & Elevation

Diagrams are **flat by doctrine**. Elevation is expressed through line weight and the single accent, not shadows:

| Level | Treatment | Use |
|---|---|---|
| Base | 1px Stone border | Every regular node and edge |
| Emphasis | 2px accent border / accent edge | The one core element per diagram |
| Grouping | subgraph hairline | Layer/zone containment |
| HTML charts | at most one whisper shadow on the chart card | Container only, never on data marks |
| 3D mode | light rig (max 3 lights), not shadow stacks | See §3D — bake lighting, hero-object shadow only |

Anti-elevation rules: no drop shadows on Mermaid/ASCII output, no 3D-effect bars/pies (depth = data dimension, never decoration), no glassmorphism, no gradients.

---

## 7. Do's and Don'ts

### Do
- Run the brief + set the three dials before generating anything
- Apply the custom Mermaid init — the default theme is a bug, not a baseline
- Compute contrast with the luminance rule for every fill/text pairing
- Keep one accent family per document; vary lightness, not hue
- Make the "why" visible in structure (ritual edges, sovereign core, labeled transitions)
- Match the palette already established in the host document
- Cite hex/px when describing or reviewing output; mark confidence ✅/⚠️/❓
- Prepare the ASCII fallback whenever the render environment is uncertain
- Vary the "shot" when the same concept recurs in one document — change type (flowchart → mindmap), emphasis, or perspective; serve content rhythm, not decoration

### Don't
- Don't pair light warm surfaces with Mist White / near-white text — light surfaces always take dark ink
- Don't use purple gradients, rainbow nodes, or the Mermaid default theme
- Don't force non-sequential data into flowcharts, or any data into pies (≤3 slices → table; else treemap/stacked bar)
- Don't exceed 1 accent, 4–5 subgraphs, 50 nodes, 7 legend items, or 8 Chinese chars per label
- Don't use emoji, ALL CAPS, mixed corner radii, or 3px+ borders
- Don't truncate bar-chart Y-axes or put unrelated metrics on a dual Y-axis
- Don't rely on color as the only channel — add pattern/shape/label for colorblind safety
- Don't combine >2 visualization types in one diagram — split instead
- Don't ship without validation (render test, overlap check, legend, caption)

---

## 8. Responsive Behavior

| Output | Behavior |
|---|---|
| Mermaid in .md | Narrow-first: short labels + TD orientation prevent horizontal overflow in Obsidian/GitHub mobile |
| ASCII | Hard cap 80 columns — survives any terminal, `cat`, and diff |
| Self-contained HTML | Fluid container, `max-width` + viewport meta; canvas resize listener mandatory |
| Python (Plotly) | `autosize=True`; export both interactive HTML and static for print |
| 3D (Three.js) | Resize listener mandatory; reduce geometry + disable shadows on mobile; camera distance/polar limits set |

Degradation strategy (when data is too complex): >50 nodes → split into 2–3 linked diagrams with shared legend · >7 categories → aggregate "Other" · mixed data types → primary relationship in the diagram, the rest in a table · preview fails → ASCII fallback · Mermaid syntax error → flowchart TD + subgraph.

---

## 9. Agent Prompt Guide

### Quick Color Reference
- Default surface: "Warm Paper (#f5f0eb)"
- Primary text on light: "Ink Navy (#1B365D)"
- Border / lines: "Stone Gray (#a8a29e)"
- Accent (one max): "International Klein Blue (#002FA7)" — pair with "Mist White (#f5f5f4)" text on solid fills
- Tertiary fill: "Pebble (#d6d3d1)"

### Ready-to-use prompts
- "Create a flowchart TD with subgraphs: Warm Paper (#f5f0eb) nodes, Ink Navy (#1B365D) text, Stone Gray (#a8a29e) 1px borders, using the Mermaid init from DESIGN.md §4. Mark the core node with a 2px International Klein Blue (#002FA7) border — it is the only accent. Labels ≤8 Chinese chars, dials 4/3/8."
- "Build an Editorial Parchment knowledge card (1080×1440): Parchment (#f5f4ed) canvas, Ivory (#faf9f5) card, judgment headline in Georgia 500, one promise line, one Terracotta (#c96442) evidence cue, dark band for secondary context. Caption states the finding. Use templates/html/editorial-card.html."
- "Build a Gantt with codes only inside the block (V1.1, A2…), a full-name table immediately after, and an 80-column ASCII fallback. Min bar 3 weeks, 3–6 tasks per section, Warm Paper init."
- "Render a comparison of 4 items as an xychart-beta bar chart, Warm Paper tokens, Y-axis starting at 0, caption stating the finding. If items ≤5 and exact values are the point, output a Markdown table instead."
- "Generate a self-contained Three.js HTML: building structure shell, procedural BoxGeometry, Stone Gray (#a8a29e) wireframe, Paper Beige (#e8e4e0) slabs, IKB (#002FA7) active floor, max 3 lights, OrbitControls with damping, animejs v4 camera tweens (`import { animate }`, render loop named `renderLoop`)."

### Iteration guide
1. One diagram at a time; state the brief reading first ("Reading this as: <type> for <audience>, <vibe>, <palette>")
2. Reference colors by name + hex — "use Ink Navy (#1B365D)", not "darker text"
3. To increase emphasis, say "move the accent to X" — never "add another color"
4. To fix crowding, lower DENSITY or split — never shrink the font below 11px
5. For render failures, follow the degradation strategy (§8), ending at ASCII

---

## Extended: Visualization Taxonomy

Based on Few's 7 relationships + Shneiderman's 6 data types + teaching/academic gaps:

| Category | Types | Anti-default | Template |
|---|---|---|---|
| Ranking/Comparison | Bar, Column, Radar (≤7), Bullet | ≤5 items → TABLE | `diverging-bar.mmd` |
| Temporal | Line, Area, Gantt, Calendar Heatmap | Gantt: codes+table+ASCII | `gantt.mmd` |
| Part-to-Whole | Stacked Bar, Treemap, Sunburst | **Avoid pie/donut** | `html/treemap.html` |
| Distribution | Histogram, Box Plot, Violin, Dot | — | `distribution.mmd` |
| Correlation | Scatter, Heatmap, Bubble, Network | — | `python/scatter-plot.py` |
| Hierarchical | Tree, Treemap, Circle Packing | — | — |
| Flow | Sankey, Chord, Flowchart | — | `sankey.mmd` |
| Funnel/Conversion | Funnel chart, Pipeline stages | Max 7 stages, label with % | `funnel.mmd` |
| Decision/Evaluation | Decision matrix, Weighted scorecard | Table-first, radar for ≤7 criteria | `decision-matrix.mmd` |
| State Transitions | State diagram, Lifecycle | Max 10 states, label transitions | `state-machine.mmd` |
| Dependencies | Dependency graph, Critical path | Cluster by layer, highlight blockers | `dependency-network.mmd` |
| Geospatial | Choropleth, Bubble Map | Use sparingly | — |

**Choosing by data shape** (quick heuristic):
- "Which is better?" → comparison (bar/radar/table)
- "How does it flow?" → sankey/flowchart
- "What converts/drops?" → funnel
- "What depends on what?" → dependency graph
- "What are the states?" → state diagram
- "How to decide?" → decision matrix + radar

---

## Extended: Editorial Format Families (HTML / card deliverables)

When the brief asks for **cards, covers, or publishable HTML** (not inline Mermaid), route by job contract. Full spec: `references/editorial-parchment-language.md`.

| Family | Job | archviz output | Template |
|---|---|---|---|
| **A — Attention** | Click / pause promise | Fixed-size cover HTML | `editorial-card.html` + aspect override |
| **B — Knowledge artifact** | Stop, understand, save | 1080×1440 card, hero + dark band | `editorial-card.html` |
| **C — Social square** | Quote / data hero | 1080×1080 single focal | `editorial-card.html` |
| **D — Long-form** | Reading depth | width-led auto-height HTML | `editorial-card.html` (strip min-height) |

**Compression rule (Family A)**: judgment headline + one promise + one evidence — never 4–6 summary bullets on a cover.

**Ambiguous brief**: state 1 primary family + 2 alternatives before generating (see SKILL.md §Editorial Mode).

---

## Extended: Signature Patterns (Aver domain)

> Synced 2026-06-11 with the Aver design system (cinnabar era). Aver's own UI tokens live in the Aver repo (`aver-design-system`); the patterns below are for **diagrams about Aver** rendered with archviz-skills tokens.

- Core = .md 数据主权 (sovereign, strongest border — the single accent)
- V1 loop as the spine: 物件 → 陪伴证据 → 告别归档 (object → evidence → farewell)
- Layers as groups: Money (量化刻度) / Evidence (陪伴证据) / Sentiment (告别归档) — the legacy Money / Knowledge / Sentiment trio appears only in archived diagrams
- Ritual edges labeled explicitly (购入仪式, 卖出告别, 里程碑)
- Accent: single IKB (#002FA7) when the diagram lives in neutral archviz documents; switch the accent slot to Aver cinnabar (#A24A2D) when the diagram is embedded in Aver-branded material — never both, still max 1
- Aver-embedded diagrams may adopt Aver paper surfaces (#FBF8F2 / #F5F1E9) to match the host document, per "match existing document palette"

---

## Extended: 3D Architectural Visualization (Three.js)

When the brief calls for building structure, interior walkthrough, or spatial analysis — switch from 2D diagram mode to 3D archviz mode.

**Stack**: Three.js (rendering) + animejs (UI transitions) + OrbitControls (navigation)

**3D Archviz Types**:

| Type | Use Case | Complexity |
|---|---|---|
| Structure shell | Building envelope, column grid, floor slabs | Low — wireframe + transparent surfaces |
| Floor plan extrusion | 2D plan → 3D floor with walls | Medium — ExtrudeGeometry from SVG/DXF paths |
| Interior walkthrough | Room layout, furniture, lighting | High — GLTF models + baked lighting |
| Structural overlay | Load paths, stress visualization on 3D model | Medium — color-mapped geometry |
| Section cut | Exploded axonometric, cutaway views | Medium — ClippingPlanes |
| Multi-floor navigation | Floor selector with camera animation | Medium — animejs camera tween |

**3D Tokens** (inherits 2D palette, adds spatial):

| Token | Value | Use |
|---|---|---|
| structure | `#a8a29e` (Stone Gray) | Wireframe, grid lines |
| floor | `#e8e4e0` (Paper Beige) | Slab fill, ground plane |
| accent-3d | `#002FA7` (IKB) | Highlighted structure, active floor |
| ambient | `0xf5f5f4` | Hemisphere light (sky) |
| ground | `0xd6d3d1` | Hemisphere light (ground) |

**3D Constraints**:
- Self-contained HTML only (no external model dependencies for templates)
- Procedural geometry preferred (BoxGeometry, PlaneGeometry) over loaded GLTF
- Max 3 light sources (1 ambient + 1 directional + 1 hemisphere)
- Camera: PerspectiveCamera, FOV 50-60, near 0.1, far 1000
- OrbitControls: enableDamping=true, dampingFactor=0.05
- animejs v4 for camera transitions (duration 800-1200ms, easeInOutCubic)
- **animejs v4 API**: `animate(target, props)` — NOT v3's `anime({targets})`. Use `tween()` wrapper.
- **animejs v4 CDN**: `dist/bundles/anime.esm.js` — NOT `lib/anime.es.js`
- **Render loop naming**: never name it `animate` (conflicts with animejs import). Use `renderLoop`.
- **Ground offset**: objects at y=0 bury into ground plane. Set `object.position.y = 2` or `ground.position.y = -0.5`.
- **CDN verification**: `curl -sI <URL>` must return 200 before committing template.
- Responsive: resize listener mandatory
- Performance: requestAnimationFrame loop, dispose geometry on teardown

**Anti-patterns (3D specific)**:
| Anti-pattern | Fix |
|---|---|
| Too many real-time shadows | Bake lighting, use shadow only for hero object |
| Unbounded camera | Set minDistance/maxDistance/polar angle limits |
| No loading state | Show progress bar for GLTF loads |
| Janky camera jump | Use animejs tween, never direct position set |
| No mobile fallback | Reduce geometry complexity, disable shadows on mobile |

**Future: HTML-in-Canvas annotation strategy** (watch — do not adopt until cross-browser stable):

Google/WICG [HTML-in-Canvas](https://github.com/WICG/html-in-canvas) renders real DOM (HTML + CSS) into 2D canvas, WebGL, or WebGPU textures while preserving accessibility, text selection, find-in-page, and DevTools inspection. Chrome Origin Trial: 148–150 (May 2026). Three.js experimental: `THREE.HTMLTexture`.

| Today | Future (when stable) |
|---|---|
| `createLabel()` → offscreen canvas `fillText` → `CanvasTexture` → `Sprite` | Hidden DOM label nodes → `HTMLTexture` / `texElementImage2D` on mesh or sprite |
| Crude CJK typography, blurry zoom | DESIGN.md typography tokens on real CSS |
| Labels not selectable / no a11y | Screen-reader + Cmd+F compatible room/floor names |

**Scope**: 3D templates only (`threejs-floorplan.html`, `threejs-archviz.html`). Default 2D mode (Mermaid, ASCII, HTML charts) stays DOM-native — no change needed.

**Adoption gate** (all must pass before rewriting templates):
1. Chrome Stable (no flag) OR documented progressive enhancement with Sprite fallback
2. Three.js `HTMLTexture` documented beyond experiment
3. Safari or Firefox signals implementation (avoid Chrome-only deliverables)
4. Self-contained HTML constraint preserved (labels as in-document `<div>`, not external assets)

**Pilot checklist** (post-gate): floor label (`#floor-label` pattern), per-room name + area badge, structural overlay legend on cut plane. Verify resize, camera tween, and mobile still pass §3D post-gen.

---

## Extended: Validation

**Pre-gen**: Brief done? Dials set? Tokens locked? Labels short? Contract layer complete? Gantt: codes+table+ASCII?

**Post-gen**: Render test? No overlaps? Legend present? Matches document style? Contrast gate pass? Caption states the finding?

**3D post-gen**: CDN imports resolve? Console clean? Resize works? Camera limits set? Touch/mobile tested?

**Error recovery**: Simplify → switch type → ASCII fallback. Never ship without validation.

---

See SKILL.md for execution workflow. See templates/ for concrete examples. See preview.html for the visual catalog.
