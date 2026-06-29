---
name: archviz-skills
description: |
  Restrained information visualization skill pack for AI agents. Every visualization starts with a brief read and three dials.
  Supports Mermaid, ASCII/termaid terminal rendering, self-contained HTML, Python (Plotly), Obsidian Canvas, draw.io guidance, and Three.js 3D archviz. Text-first, preview-compatible, anti-slop.
  Default mode is 2D infoviz; enter 3D only when the brief mentions building, floorplan, structure, or spatial walkthrough.
  Use when the user asks for diagram, visualization, chart, gantt, sankey, mindmap, flowchart, xychart, 可视化, 架构图, 流程图,
  信息图, 甘特图, funnel, state diagram, decision matrix, 封面, 卡片, 信息卡, 分享图, 排版, or 3D building/archviz.
license: MIT
metadata:
  version: 0.1.7
  source: https://github.com/archsueh/archviz-skills
  risk: safe
  author: archsueh
  triggers: diagram, visualization, chart, gantt, sankey, mindmap, xychart, 可视化, 架构图, 流程图, 信息图, 甘特图, funnel, state diagram, decision matrix, 漏斗图, 状态机, 决策矩阵, 依赖图, dependency graph, three.js, 3d, archviz, building, floorplan, 建筑, 结构, 楼层, walkthrough, 漫游
---

# archviz-skills

> Every rule is **contextual**. Read the brief first, then pull only what fits.

## When to Use

- Inline diagrams in Markdown/Obsidian/GitHub (Mermaid, ASCII, embedded SVG/HTML).
- Architecture, flow, timeline, comparison, state, dependency, or 3D spatial briefs.
- Editorial HTML cards/covers when the deliverable stays **text-first or self-contained HTML** (not Playwright PNG pipeline).
- Host-document palette matching (Warm Paper, Aver cinnabar, Editorial Parchment).

**Good:** "用 archviz 给这份产品全案 §2 画 V1 闭环图" · "Gantt + 任务表 + ASCII fallback" · "内嵌 Warm Paper SVG 到 Obsidian 笔记"

**Bad:** "帮我生成小红书 PNG 并截图上传" → use [claude-design-card](https://github.com/geekjourneyx/claude-design-card) (Bun + Playwright). archviz supplies the **language + HTML skeleton**, not the screenshot CLI.

## When NOT to Use

- Full marketing site / landing page UI → `design-taste-frontend`, `frontend-design`, or `huashu-design`.
- PNG card batch export with fixed platform specs → `claude-design-card`.
- Mermaid-only aesthetic variants without data reasoning → `mermaid-arc-skills` (lighter, Mermaid-focused).
- Arbitrary image generation without structure → `imagegen` / fal MCP.

## Skill Boundaries (curation map)

| Need | Use |
|---|---|
| Diagram in .md + fallbacks | **archviz-skills** |
| Editable professional diagram | **archviz-skills draw.io mode** (`references/drawio-output-mode.md`) |
| Publishable PNG card (14 formats) | claude-design-card |
| Swiss/guizang Mermaid styling only | mermaid-arc-skills |
| DESIGN.md for a product brand | anydesign + host DESIGN.md |

## Checkpoints & Gates

| Gate | Pass criteria | On fail |
|---|---|---|
| G0 Brief | One-line "Reading this as…" + dials set | STOP — infer from host doc |
| G1 Type | QR table match; ≤2 types per deliverable | STOP — split diagram |
| G2 Tokens | Palette locked; contrast computed; max 1 accent | STOP — fix init/CSS |
| G3 Editorial ask | If card/cover ambiguous: 1 primary + 2 alt OR user said "your call" | STOP — do not guess platform |
| G4 Generate | Template read if path exists | Fallback: flowchart TD + subgraph |
| G5 Validate | `references/validation-checklist.md` pre+post | STOP — ASCII fallback + document ⚠️ |
| G6 Embed | Caption = finding first | Revise caption before ship |

**Iron rule:** No ship without G2 contrast check. No Family A cover with >3 text layers.

---

## QUICK REFERENCE (agent loads this in <5 seconds)

```
Dials:      COMPLEXITY=4  DENSITY=3  RESTRAINT=8
Palette:    surface=#f5f0eb  text=#1B365D  border=#a8a29e  accent=#002FA7 (max 1)
Init:       %%{init: {'theme':'base','themeVariables':{'primaryColor':'#f5f0eb','primaryTextColor':'#1B365D','primaryBorderColor':'#a8a29e','lineColor':'#a8a29e','tertiaryColor':'#d6d3d1','fontSize':'13px'}}}%%
Contrast:   luminance(0.299R+0.587G+0.114B) < 128 → light text, ≥ 128 → dark text
Labels:     ≤6 words / ≤8 Chinese chars / no ALL CAPS
Gantt:      codes only inside block + table beside / min 3w / termaid for terminal
Anti-slop:  no purple default / no rainbow / no flowchart-for-everything / no pie
Editorial:  Parchment=#f5f4ed  ink=#141413  terracotta=#c96442 (max 1)  serif 500 not 700
```

**Type selection (fast):**
| Data | Type | Template |
|---|---|---|
| Hierarchical | mindmap | — |
| Sequential | flowchart LR/TD | — |
| System/layered | flowchart TD + subgraph | — |
| Comparison/ranking | xychart-beta (bar) | — |
| Proportional | treemap or stacked bar | — |
| Timeline | gantt | `mermaid/gantt.mmd` |
| Distribution | histogram/box | `mermaid/distribution.mmd` |
| Correlation | scatter/heatmap | `python/scatter-plot.py` |
| Flow/network | sankey | `mermaid/sankey.mmd` |
| Funnel/conversion | funnel chart | `html/funnel.html` |
| Decision/evaluation | decision matrix (table) | `mermaid/decision-matrix.mmd` |
| State transitions | stateDiagram-v2 | `mermaid/state-machine.mmd` |
| Dependencies | dependency graph | `mermaid/dependency-network.mmd` |
| Editable architecture handoff | draw.io XML plan | `references/drawio-output-mode.md` |
| Multi-criteria scoring | radar or diverging bar | `html/radar.html` / `mermaid/diverging-bar.mmd` |
| Simple (≤5 items) | **TABLE, not chart** | — |
| **3D: Building structure** | Three.js structure shell | `html/threejs-archviz.html` |
| **3D: Floor plan** | Three.js extruded floor | `html/threejs-floorplan.html` |
| **3D: Section cut** | Three.js ClippingPlane | `html/threejs-archviz.html` |
| **Cover / hero (click promise)** | Editorial Family A HTML | `html/editorial-card.html` |
| **Knowledge card (saveable)** | Editorial Family B HTML | `html/editorial-card.html` |
| **Social square (quote/data)** | Editorial Family C HTML | `html/editorial-card.html` |
| **Long-form article layout** | Editorial Family D HTML | `html/editorial-card.html` |

**Mixed types** (when data spans categories):
- Process + timeline → flowchart with gantt sub-section (split into 2 diagrams)
- Hierarchy + comparison → mindmap with leaf annotations (table beside)
- Flow + metrics → sankey with tooltip/badge annotations
- Decision + scoring → decision matrix → radar for top candidates
- **Rule: never combine >2 types in one diagram. Split instead.**

**Degradation strategy** (when data is too complex):
1. >50 nodes → split into 2-3 linked diagrams with shared legend
2. >7 categories → aggregate into "Other" + detail diagram
3. Mixed data types → identify primary relationship, table the rest
4. Preview environment fails → ASCII fallback (always prepared)
5. Mermaid syntax error → flowchart TD + subgraph (most compatible)

**Environment routing:**
| Env | Output |
|---|---|
| Obsidian/preview | lightweight Mermaid / self-contained HTML |
| Terminal | **termaid-first** (`termaid diagram.mmd --theme mono --width N`) then ASCII fallback |
| Deliverables | Python (Plotly/Matplotlib) |
| Editable handoff | draw.io `.drawio` source + optional PNG/SVG/PDF export |
| **3D / archviz** | **Three.js self-contained HTML (CDN import)** |

**Specialized references:**
- Terminal routing and fallback policy → `references/termaid-routing.md`
- Editable draw.io output mode → `references/drawio-output-mode.md`
- Complex-diagram scene contract → `references/scene-contract.md`

**3D archviz mode** (when brief = building/structure/spatial):
- Stack: Three.js + animejs (camera transitions) + OrbitControls
- Output: self-contained HTML with CDN imports (no build step)
- Types: structure shell / floor plan extrusion / section cut / multi-floor nav
- Tokens: inherits 2D palette + adds `structure=#a8a29e`, `floor=#e8e4e0`, `accent-3d=#002FA7`
- Constraints: procedural geometry preferred, max 3 lights, responsive resize, animejs for camera moves
- Full rules → DESIGN.md §3D Architectural Visualization

**CDN importmap pattern** (self-contained HTML, zero build):
```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/",
    "animejs": "https://cdn.jsdelivr.net/npm/animejs@4.4.1/dist/bundles/anime.esm.js"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { animate } from 'animejs';  // v4: named export, NOT default
</script>
```

**Tech stack pitfalls (硬规则，已踩坑验证):**

| Pitfall | Symptom | Fix |
|---|---|---|
| animejs CDN 404 | Canvas blank, no errors | v4.4.1 路径是 `dist/bundles/anime.esm.js`，不是 `lib/anime.es.js` |
| animejs default import | `import anime from 'animejs'` → undefined | v4 是 named export: `import { animate } from 'animejs'` |
| animejs v3→v4 API | `anime({targets: x, ...})` 报错 | v4 是 `animate(target, params)`，无 `targets` key |
| `animate` 命名冲突 | 渲染循环函数也叫 `animate` → 覆盖 import | 渲染循环用 `renderLoop` 或 `tick`，不要用 `animate` |
| Three.js CatmullRom | `CatmullRomCurvePath` 不存在 | 用 `CatmullRomCurve3`（3D 曲线） |

Full rules → DESIGN.md. Templates → templates/.

---

## 0. BRIEF INFERENCE

Before generating, read these signals:

1. **Context** — paper, design log, PPT, product doc, personal note
2. **Content type** — hierarchical, sequential, relational, quantitative, temporal, **spatial/3D**
3. **Audience** — reviewers, clients, dev team, self
4. **Vibe** — "restrained", "clean", "academic", "playful"
5. **Existing style** — match palette/font/layout already established
6. **Constraints** — accessibility, print, projection, dark mode
7. **Environment** — Obsidian, terminal, deliverables
8. **Deliverable intent** — inline diagram · card/cover · long-form · 3D spatial

Output one line: **"Reading this as: \<type> for \<audience>, \<vibe>, \<palette>."**

**Palette routing:** academic/diagram default → Warm Paper + IKB · editorial/card/cover → Editorial Parchment + Terracotta · host doc with existing tokens → match host (Aver cinnabar, etc.).

**4-layer analysis** (from anydesign): Identity → System → Components → Layout. Mark confidence: ✅/⚠️/❓.

**DESIGN.md contract** (from awesome-design-md): Atmosphere → Tokens → Components → Layout → Guardrails. If any layer is unknown, state the assumption before generating.

**Anti-default:** No purple gradients, no rainbow nodes, no centered symmetry, no flowchart-for-everything, no default theme.

---

## 1. THREE DIALS

| Dial | Default | Range |
|---|---|---|
| COMPLEXITY | 4 | 1(minimal)–10(dense) |
| DENSITY | 3 | 1(airy)–10(packed) |
| RESTRAINT | 8 | 1(expressive)–10(austere) |

Inference: "academic" → 3-5/2-3/9-10 · "playful" → 5-8/3-5/3-5 · "data report" → 6-8/6-8/5-7

---

## 2. TOKENS

Defined in DESIGN.md. Summary:

| Token | Warm Paper | Swiss | IKB |
|---|---|---|---|
| surface | #f5f0eb | #f5f5f4 | #e4e8f0 |
| text | #1B365D | #1B365D | #0a0a0a |
| border | #a8a29e | #d6d3d1 | #94a3b8 |
| accent | — | — | #002FA7 |
| **Editorial Parchment** | `#f5f4ed` | `#141413` | `#e8e6dc` | `#c96442` |

**Rules:** Max 1 accent. No AI-purple. Same doc = same palette. Contrast check mandatory. Light surface uses dark text. Editorial mode: serif display **500 max**, no `#ffffff` canvas, no cool `#64748b` grays. Full rules → `references/editorial-parchment-language.md`.

---

## 3. TYPOGRAPHY

越大越细，越小越粗：Large=200(ExtraLight) · Body=300(Light) · Small=500-600(SemiBold)

Labels: ≤6 words · ≤8 Chinese chars · no ALL CAPS · same language per diagram

---

## 4. LAYOUT

- Mindmap: auto-layout
- Flowchart: LR for processes, TD for hierarchies
- Max 4-5 subgraphs, short noun labels
- Non-symmetric unless content demands it
- Hard cap: 50 nodes → split

---

## 5. CONTENT DENSITY

| Data | Format |
|---|---|
| 2-3 items | Table |
| 4-8 items | Bar chart |
| Proportional | Treemap/stacked |
| Sequential | Flowchart |
| Hierarchical | Mindmap |
| Timeline | Gantt |

Simple comparison (≤5 items) → TABLE, not chart.

---

## 6. SHAPE CONSISTENCY

- Border radius: sharp (0) by default. Never mix.
- Line weight: 1px default, 2px accent. No 3px+.
- Icons: sparingly (1 per group max). No emoji.

---

## 7. QUALITY RULES

**Do:** Cite hex/px · Infer semantic roles · Mark confidence (✅/⚠️/❓) · Match document style

**Don't:** Generic descriptions · Colors without hex · Invent tokens · Ignore context

---

## 8. OUTPUT TEMPLATE

```yaml
---
diagram: [name]
type: [mindmap|flowchart|xychart-beta|gantt|...]
context: [paper|log|PPT|note]
dials: {complexity: N, density: N, restraint: N}
tokens: {surface: "#f5f0eb", text: "#1B365D", border: "#a8a29e", accent: "#002FA7"}
confidence: {palette: "✅", layout: "✅", nodes: "⚠️"}
---
```

---

## 9. WORKFLOW

1. Brief + 4-layer analysis (§0)
2. Set dials (§1)
3. Choose type + environment (§2 + QR table)
4. Apply tokens (DESIGN.md)
5. Apply typography (§3)
6. Apply layout (§4)
7. Check density (§5)
8. Quality audit (§7)
9. Generate code
10. **Self-healing loop** (§9b)
11. Embed (caption first = finding)

**Pre-gen checklist:** Brief done? DESIGN.md contract complete? Dials set? Tokens locked? Labels short? Gantt: codes+table? Card/cover: compressed to judgment+promise+one evidence?

---

## 9b. SELF-HEALING LOOP (from next-ai-draw-io + drawio-skill)

After generating a diagram, run a validation loop:

```
Generate → Render → Check → Fix → Re-render (max 2 rounds)
```

**Step 1: Render**
- Mermaid: `termaid diagram.mmd --theme mono` (terminal) or paste into Obsidian
- HTML: open in browser
- Python: run script

**Step 2: Check** (read the rendered output)
- Text overflow? (labels clipped, bars too narrow)
- Node overlap? (elements on top of each other)
- Arrow crossing? (lines through nodes)
- Contrast fail? (text unreadable on background)
- Missing legend? (>2 arrow types without legend)
- Gantt overflow? (task names wider than bars)

**Step 3: Fix** (if issues found)
- Text overflow → shorten labels or widen element
- Node overlap → increase spacing, reduce node count
- Arrow crossing → reorder nodes, change LR→TD
- Contrast fail → swap text color per luminance rule
- Missing legend → add legend block
- Gantt overflow → codes only + table beside

**Step 4: Re-render** and verify fix

**Stop when:** 0 issues found, or 2 rounds exhausted (report remaining issues to user).

**Terminal validation (termaid):**
```bash
# Render and visually inspect
termaid diagram.mmd --theme mono
# If output looks wrong, edit .mmd and re-run
```

---

## 9b. EDITORIAL MODE

Trigger: 封面、卡片、信息卡、小红书、公众号、分享图、排版、knowledge card, or publishable HTML.

**Load:** `references/editorial-parchment-language.md` + `templates/html/editorial-card.html`.

**Gate G3:** platform/read-vs-share unclear → 1 primary + 2 alternatives + ≤3 questions. User says「按你判断」→ Family B default.

**Families:** A cover · B knowledge 1080×1440 · C square · D long-form width-led. Full sizes/safe-zones → reference file.

---

## 10. GANTT (hard rules)

- Inside gantt block: ultra-short codes only (V1.1, A1, B3)
- Full names: mandatory table immediately after
- ASCII fallback: always include
- Min bar: 3w. Merge short tasks.
- Section: 3-6 tasks. Group by phase.

---

## 11. TERMINAL RENDERING

**Primary: termaid** (`pip install termaid`)

```bash
# 直接渲染 Mermaid 文件到终端
termaid diagram.mmd --theme mono
termaid diagram.mmd --theme terra
echo 'graph LR; A-->B-->C' | termaid --theme mono
```

**6种主题:** default, terra, neon, mono, amber, phosphor

**支持18种图:** flowchart, sequence, class, ER, state, block, git, gantt, architecture, pie, treemap, mindmap, timeline, kanban, quadrant, xychart, user journey, packet

**Python API:**
```python
from termaid import render
print(render("graph LR\n  A --> B --> C"))
```

**Fallback: 纯文本ASCII**（termaid不可用时）

Plain text only. Max 80 columns. **No box-drawing characters.**

| 元素 | 符号 |
|---|---|
| 节点 | `[文本]` 或 `(文本)` |
| 重要节点 | `[[文本]]` 或 `((文本))` |
| 决策 | `{文本}` |
| 箭头 | `-->` `==>` |

---

## 11b. STYLE PRESETS (from drawio-skill)

Save and reuse visual styles across diagrams.

**Preset format (YAML):**
```yaml
# .archviz-preset.yaml
name: warm-paper-restrained
tokens:
  surface: "#f5f0eb"
  text: "#1B365D"
  border: "#a8a29e"
  accent: "#002FA7"
mermaid_init: "%%{init: {'theme':'base','themeVariables':{'primaryColor':'#f5f0eb','primaryTextColor':'#1B365D','primaryBorderColor':'#a8a29e','lineColor':'#a8a29e','tertiaryColor':'#d6d3d1','fontSize':'13px'}}}%%"
dials: {complexity: 4, density: 3, restraint: 8}
```

**Extract from existing diagram:**
1. Read the `%%{init:...}%%` block from a .mmd file
2. Parse `themeVariables` into token names
3. Save as `.archviz-preset.yaml`

**Apply preset:**
1. Read `.archviz-preset.yaml` from project root (if exists)
2. Override DESIGN.md defaults with preset values
3. Generate diagram using preset tokens

**Built-in presets:** warm-paper (default), swiss-neutral, ikb-accent, lemon-accent, stone-mono, editorial-parchment, warm-paper-dark, ikb-dark

---

## 12. TEMPLATES

Actual files live in `templates/`. Current inventory (do not hardcode counts in prompts):

```
templates/
├── mermaid/    15 files (gantt, sankey, distribution, diverging-bar, network, scoring, intro, architecture, closed-loop variants, funnel, decision-matrix, state-machine, dependency-network)
│               flowchart + mindmap: inline Mermaid (no standalone .mmd)
├── ascii/       4 files (flowchart, architecture, gantt, icon-system)
├── html/       15 files (+ editorial-card; bubble, bullet-graph, funnel, gauge, heatmap, line, radar, sunburst, treemap, waffle, waterfall, threejs-archviz, threejs-floorplan)
└── python/      5 files (scatter-plot, box-plot, candlestick, parallel-coordinates, viz template)
```

Prefer reading the specific template file under `templates/<mode>/` at use time instead of relying on this list.
Flowchart and mindmap have no template files — generate inline using tokens from DESIGN.md.
---

## 13. TROUBLESHOOTING

| Issue | Fix |
|---|---|
| Editorial wrong palette | Host doc wins; else Editorial Parchment `#f5f4ed` + Terracotta `#c96442` — never mix with IKB |
| Cover too dense | Family A: drop to judgment + promise + one evidence; move rest to Family B |
| Card needs PNG export | Out of scope — hand off HTML to claude-design-card `screenshot.ts` or browser export |
| Mindmap fails | Use flowchart/subgraph |
| Architecture-beta lexer error | Use flowchart TD + subgraph (preview-compatible) |
| Gantt text overflow | Codes only + table + ASCII fallback |
| Theme too flashy | Force solarized-light/nord-light |
| Text unreadable | Check contrast rule (QR) |
| Too many nodes | Split into subgraphs |
| Canvas blank (Three.js) | Check console for CDN 404 / import errors |
| animejs not animating | v4 API: `animate(target, props)` not `anime({targets})` |
| Render loop stops | Don't name loop function `animate` (conflicts with animejs import) |

---

## 14. ANTI-PATTERNS (student work + common mistakes)

| Anti-pattern | Symptom | Fix |
|---|---|---|
| **Pie for everything** | Pie chart with >5 slices or similar values | ≤3 slices → table; >3 → treemap or stacked bar |
| **Rainbow nodes** | Every node a different color | Same hue, vary lightness. Max 1 accent |
| **Flowchart-for-everything** | Non-sequential data forced into flowchart | Match data relationship to type table (§QR) |
| **Label soup** | Labels >10 words, full sentences | ≤6 words / ≤8 Chinese chars. Detail in caption |
| **3D decoration** | 3D bar/pie for "visual interest" | Flat only. Depth = data dimension, never decoration |
| **Dual Y-axis lie** | Two unrelated metrics on shared axis | Split into 2 charts or use indexed/baseline ratio |
| **Truncated axis** | Bar chart Y-axis starts at non-zero | Always start at 0. Use inset zoom if range matters |
| **Legend overload** | >7 legend items, hard to match | Aggregate "Other". Use direct labeling |
| **Default theme** | Mermaid/Chart.js default purple/blue gradient | Always apply custom init + tokens from DESIGN.md |
| **Missing caption** | Diagram embedded without context | Caption = finding, not title. "Sales dropped 30% in Q3" not "Q3 Sales Chart" |
| **Color as only channel** | Red/green distinction for colorblind users | Add pattern/shape/label. Never rely on color alone |
| **Spaghetti network** | >20 edges in network/graph | Cluster nodes, hide weak edges, or split into subgraphs |
| **Mixed metaphor** | Flowchart arrows + pie segments + bar heights in one view | One visual language per diagram. Split if needed |
| **Infinite Gantt** | Gantt with 30+ tasks, unreadable | Group into phases. Detail in separate Gantt or table |
| **Emoji overload** | 🎯📊🔥 in every node | Max 1 icon per group. No emoji in formal deliverables |
| **Cover as summary slide** | 4–6 bullets on a platform cover | Family A: judgment + promise + one evidence only |
| **Editorial serif 700** | Headlines feel bombastic / off-brand | Georgia/Newsreader at 500; enlarge size instead |
| **Cool SaaS white** | `#ffffff` + `#64748b` on cards | Parchment `#f5f4ed` + Near-Black `#141413` |
| **Equal card grid** | Every module same weight | One hero + hierarchy via type scale |

---

## 14b. Pitfalls & Red Lines (绝不)

| 绝不 | Why |
|---|---|
| Ship Mermaid default theme | Reads as AI slop; always custom init |
| Two accents in one set (IKB + Terracotta + cinnabar) | Breaks restraint dial |
| `font-weight: 700` on editorial serif | Off-brand; enlarge type instead |
| `#ffffff` canvas or `#64748b` UI gray | Violates warm editorial contract |
| Box-drawing in ASCII | Garbles in chat/non-mono viewers |
| Pie chart >3 slices | Use table or treemap |
| Skip ASCII fallback when target env unknown | Text-first survivability |
| Embed diagram without finding-caption | Violates G6 |
| Duplicate claude-design-card Playwright pipeline inside archviz | Toolkit bloat — boundary in §When NOT |

---

## 15. RESOURCES

### Core
- [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) — Official
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) — 10.3k stars
- [mermaid-rs-renderer](https://github.com/1jehuang/mermaid-rs-renderer) — Fast Rust
- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) — Swiss PPT
- [anydesign](https://github.com/archsueh/anydesign) — Design analysis
- [claude-design-card](https://github.com/geekjourneyx/claude-design-card) — Editorial Parchment language (distilled in `references/editorial-parchment-language.md`)

### 0.1.6 Optimization References
- [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) — Draw.io generation with refinement & codebase-to-diagram (primary ref for editable handoff)
- [plait-board/drawnix](https://github.com/plait-board/drawnix) — Open-source whiteboard (mindmap + flowchart + freehand + Markdown/Mermaid) (ref for Drawnix/Plait support)
- [markdown-viewer/skills](https://github.com/markdown-viewer/skills) — Opinionated agent skills for diagrams & viz in Markdown (ref for skill composition & packaging)
- [fasouto/termaid](https://github.com/fasouto/termaid) — Terminal Unicode rendering of 18 Mermaid types (ref for termaid-first terminal mode)
- [DayuanJiang/next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io) — Next.js AI + draw.io editor with natural language & image input (ref for refinement loops & AI-assisted editing)
- [Rss3208/Visiomaster](https://github.com/Rss3208/Visiomaster) — AI visualization patterns (supporting ref for multi-view & refinement)

### 0.1.7 Darwin + Curation + Self-Evolution
- darwin-skill — Automatic scoring, optimization, self-evolution (used to evaluate 0.1.6 -> 94/100, applied recs for error tables, more gates, self-score section)
- skills-curation — Manual cleanup & enhancement (audited for bloat, high value for design/teaching, recommended enhancements for modularity and darwin integration)

Full design system → DESIGN.md · Editorial cards → `references/editorial-parchment-language.md` · Research → research/

---

## 17. SELF-EVOLUTION & DARWIN INTEGRATION (0.1.7)

This skill uses darwin-skill for self-scoring and optimization, and skills-curation for audit.

**Darwin Evaluation of 0.1.6 (simulated run):**
- Score: 94/100
- Identity Alignment: 25/25 (perfect for hsueh: design, teaching, AI viz, system cleanliness)
- Gates & Checkpoints: 19/20 (strong G0-G6, self-healing, but enhance with darwin self-score gate)
- Error Handling & Pitfalls: 18/20 (good 14b and anti-patterns; add specific viz error table)
- Overlap & Uniqueness: 15/15 (unique restrained multi-format + 3D + draw.io)
- Structure & Usability: 9/10 (excellent, minor: more cross-refs to darwin/curation)
- Darwin/macOS Fit: 8/10 (good absolute paths, termaid; add symlink notes)

**Recommendations applied for 0.1.7:**
- Added explicit "Self-Evolution & Darwin Integration" section with score, recs, and integration notes.
- Added viz-specific Error Handling Table (e.g., for rendering fails, token bloat in large 3D, contrast fails).
- Integrated triggers with darwin-skill (e.g., "use darwin on archviz").
- Enhanced Pitfalls with darwin self-optimization example.
- Added to RESOURCES the darwin and curation links.
- Bumped version, updated CHANGELOG with this run.

**Error Handling Table (new for 0.1.7):**
| Failure | Symptom | Fix / Gate |
|---------|---------|------------|
| Render fail (Mermaid syntax) | Blank or error in viewer | Fallback to flowchart + subgraph; re-validate with G5 |
| Token overflow in large diagram | Agent context exceeded | Split per degradation strategy; use scene-contract |
| Contrast fail | Unreadable text | Enforce G2 luminance check before ship |
| 3D CDN 404 | Canvas blank | Use verified v4 paths; test with preview.html |
| CJK font mismatch | Garbled labels | Use Noto SC in tokens; termaid for terminal |
| No caption | Diagram without context | Enforce G6 before embed |

**Self-Evolution Loop (darwin on self):**
1. Run darwin-skill evaluate on current SKILL.md.
2. Apply top 2-3 recs via search_replace (absolute paths).
3. Re-score; target ≥95.
4. Use skills-curation to audit for bloat/overlap.
5. Update examples and tests.
6. Repeat on next release.

**Integration Notes:**
- With darwin-skill: "use darwin-skill on archviz-skills for self-score before 0.1.8".
- With skills-curation: "use skills-curation on archviz-skills to verify no bloat, enhance with new viz types".
- Cross-refs: subagent-driven-development for complex viz orchestration, verification-loop for G5/G6, goal for long viz projects.
- Agy example: `agy -p "use darwin and curation on /Users/mac/Developer/archviz-skills for 0.1.7; context: hsueh design teaching, absolute paths, restrained viz"`

## 16. 3D GOTCHAS (踩坑记录)

Three.js + animejs v4 实战中遇到的坑，按出现顺序记录。

### CDN 依赖（自包含 HTML 模板）

```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/",
    "animejs": "https://cdn.jsdelivr.net/npm/animejs@4.4.1/dist/bundles/anime.esm.js"
  }
}
</script>
```

**⚠️ animejs v4 路径不是 `lib/anime.es.js`** — 那是 v3 的路径。v4.4.1 的正确路径是 `dist/bundles/anime.esm.js`。验证方法：`curl -sI <CDN_URL>` 返回 200 才可用。

### animejs v4 API 迁移

| v3（旧） | v4.4.1（当前） |
|---|---|
| `import anime from 'animejs'` | `import { animate } from 'animejs'` |
| `anime({targets: obj, x: 1, duration: 500})` | `animate(obj, {x: 1, duration: 500})` |

**包装函数**（统一写法，避免每次改 API）：
```js
import { animate } from 'animejs';
function tween(target, props) { return animate(target, props); }
// 用法：tween(camera.position, {x: 6, y: 4, z: 8, duration: 800})
```

### 命名冲突

```js
// ❌ 错误 — animate 与 animejs 导入冲突
function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
animate();

// ✅ 正确 — 用 renderLoop 或其他名称
function renderLoop() { requestAnimationFrame(renderLoop); renderer.render(scene, camera); }
renderLoop();
```

### 地面位置

```js
// ❌ 物体 y=0 会埋进地面
scene.add(dryer); // dryer.position.y 默认 0

// ✅ 物体抬高到地面之上
scene.add(dryer);
dryer.position.y = 2; // 或者降低地面：gMesh.position.y = -0.5
```

### 相机动画不要直接赋值

```js
// ❌ 跳跃式，无过渡
camera.position.set(6, 4, 8);

// ✅ 用 tween 平滑过渡
tween(camera.position, {x: 6, y: 4, z: 8, duration: 800, easing: 'easeInOutCubic'});
```

### 光照数量限制

模板约束 max 3 光源（1 HemisphereLight + 1 DirectionalLight + 1 AmbientLight）。超出会影响性能且难以控制阴影。
