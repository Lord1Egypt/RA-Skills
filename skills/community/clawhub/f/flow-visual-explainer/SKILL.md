---
name: FlowVisualExplainer
description: Generate beautiful, self-contained HTML pages that visually explain systems, code, plans, and data. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, slide deck, or any visual explanation of technical concepts. Also triggers automatically when about to render a complex table (4+ rows or 3+ columns) — render HTML instead of ASCII. Supports --slides flag for magazine-quality slide decks. Outputs to ~/clawd/output/diagrams/ and opens in browser.
homepage: https://github.com/nicobailon/visual-explainer
metadata:
  openclaw:
    emoji: "🎨"
    version: "1.0.0"
    author: "nicobailon (adapted for OpenClaw by Flo)"
---

# Flow Visual Explainer

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Always open the result in the browser. **Never fall back to ASCII art when this skill is loaded.**

**Output directory:** `~/clawd/output/diagrams/`
**Open in browser:** `exec: open ~/clawd/output/diagrams/filename.html`

---

## Trigger Conditions

Use this skill when:
- User asks to "draw", "diagram", "visualize", "chart", "map out", or "explain" something visually
- User asks for architecture overview, system diagram, flow diagram, sequence diagram, ER diagram
- User asks for a diff review, plan review, project recap, or fact-check
- User asks for a slide deck or presentation
- You are about to render a table with **4+ rows or 3+ columns** — render HTML instead automatically
- User asks to compare N things against M criteria (always a table → always HTML)

Do not wait for the user to ask for HTML. If the output would be a complex table or diagram, render it visually.

---

## Commands (Natural Language Triggers)

| What user says | What to generate |
|---|---|
| "draw a diagram of X" / "visualize X" | `generate-web-diagram` — HTML diagram for any topic |
| "visual plan for X" / "implementation plan" | `generate-visual-plan` — visual feature/build plan |
| "slide deck for X" / "slides on X" | `generate-slides` — magazine-quality slide deck |
| "review this diff" / "/diff-review" | `diff-review` — visual diff with architecture comparison |
| "review this plan" / "/plan-review" | `plan-review` — plan vs codebase with risk assessment |
| "project recap" / "catch me up on X" | `project-recap` — mental model snapshot for context switching |
| "fact-check this doc" | `fact-check` — verify document accuracy against actual code |
| "share this" / "deploy this" | `share` — deploy HTML to Vercel, return live URL |

Any command that produces a scrollable page also supports `--slides` flag:
```
"review this diff as slides"
→ generates slide deck version instead of scrollable page
```

---

## Workflow

### Step 1: Think First (30 seconds)

Before writing HTML, commit to a direction. Answer three questions:

**Who is looking?** Developer? PM? Investor? Shapes density and complexity.

**What type of content?**
- Architecture (text-heavy cards) → CSS Grid
- Architecture (topology, connections matter) → Mermaid
- Flowchart / pipeline / state machine → Mermaid
- Sequence diagram → Mermaid
- ER / schema → Mermaid
- Data table / comparison / matrix → HTML `<table>`
- Dashboard / metrics → Chart.js
- Slide deck → scroll-snap sections

**What aesthetic?** Pick one. Commit. Read `references/css-patterns.md` for patterns.

**Constrained aesthetics (prefer these — harder to make generic):**
- Blueprint: technical drawing, dot/grid background, slate/blue palette, monospace labels
- Editorial: serif headlines (Instrument Serif, Crimson Pro), generous whitespace, muted earth tones or navy + gold
- Paper/ink: warm cream `#faf7f5` background, terracotta/sage accents, informal
- Monochrome terminal: green/amber on near-black, monospace, CRT glow optional

**Flexible aesthetics (use with discipline):**
- IDE-inspired: commit to a real named scheme (Dracula, Nord, Catppuccin Mocha, Gruvbox, One Dark) — use the actual palette
- Data-dense: small type, tight spacing, maximum info, muted colors

**Forbidden forever:**
- Neon dashboard (cyan + magenta + purple on dark) — AI slop
- Gradient mesh (pink/purple/cyan blobs) — too generic
- Inter font + violet/indigo accents + gradient text combination

Vary each time. If the last diagram was dark and technical, make the next one light and editorial.

---

### Step 2: Read Reference Material

Before generating, read the relevant references:

**For architecture (text-heavy cards):** read `references/css-patterns.md` + `templates/architecture.html`
**For flowcharts / diagrams:** read `references/libraries.md` + `templates/mermaid-flowchart.html`
**For data tables / comparisons:** read `templates/data-table.html`
**For slide decks:** read `templates/slide-deck.html` + `references/slide-patterns.md`
**For CSS/layout patterns:** read `references/css-patterns.md`
**For 4+ sections (reviews, recaps, dashboards):** also read `references/responsive-nav.md`

---

### Step 3: Choose Rendering Approach

| Content type | Approach |
|---|---|
| Architecture (text-heavy) | CSS Grid cards + flow arrows |
| Architecture (topology) | Mermaid graph |
| Flowchart / pipeline | Mermaid flowchart |
| Sequence diagram | Mermaid sequence |
| Data flow | Mermaid with edge labels |
| ER / schema | Mermaid ER |
| State machine | Mermaid stateDiagram |
| Mind map | Mermaid mindmap |
| Class diagram | Mermaid classDiagram |
| C4 architecture | Mermaid graph TD with subgraphs |
| Data table / comparison | HTML `<table>` with styled CSS |
| Dashboard / KPIs | CSS Grid cards + Chart.js |
| Slide deck | Scroll-snap `<section>` elements |

---

### Step 4: Generate HTML

**File naming:** `~/clawd/output/diagrams/YYYY-MM-DD-{slug}.html`
Example: `~/clawd/output/diagrams/2026-03-10-nexus-architecture.html`

**All HTML must be:**
- Self-contained (no external dependencies except CDN libs)
- Single file
- Dark/light theme support via `@media (prefers-color-scheme: dark)`
- Responsive (mobile-friendly)
- Real typography — Google Fonts or system font stack, never just `sans-serif`

**Boilerplate structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties for theme */
    /* Layout */
    /* Components */
  </style>
</head>
<body>
  <!-- Content -->
  <script>
    /* JS only if needed (Mermaid, Chart.js, interactivity) */
  </script>
</body>
</html>
```

---

### Step 5: Open in Browser

After writing the file:
```bash
open ~/clawd/output/diagrams/YYYY-MM-DD-{slug}.html
```

Tell the user the file path and that it's opened in their browser.

---

## Diagram-Specific Notes

### Mermaid Integration
- Always use `theme: 'base'` — only theme where all themeVariables are customizable
- Never use violet/indigo/fuchsia colors in themeVariables
- Always add CSS overrides for `.mermaid .nodeLabel` and `.mermaid .edgeLabel` to respect page color scheme
- Never use `.node` as a CSS class (conflicts with Mermaid internals) — use `.ve-card` instead
- Add zoom/pan controls for complex diagrams (see css-patterns.md)
- Import ELK layout engine only when needed — adds significant bundle weight

### Slide Decks
- Use scroll-snap: each slide is `100dvh`, `scroll-snap-align: start`
- Add keyboard navigation (ArrowLeft/ArrowRight/Space)
- Add slide counter (e.g., "3 / 12")
- Add progress bar
- Inventory ALL source content before assigning to slides — never silently drop content
- A source doc with 7 sections typically → 18–25 slides, not 10–13

### Data Tables
- Sticky header
- Alternating row colors
- Sortable columns if >8 rows (add click handlers)
- Status badges for status columns (color-coded)
- Export to CSV button for data tables

---

## Share to Web

To deploy any generated HTML page to a live URL:

```bash
~/clawd/skills/flow-visual-explainer/scripts/share.sh ~/clawd/output/diagrams/filename.html
```

Requires Vercel CLI: `npm i -g vercel`. Returns a live URL that can be shared.

---

## Flowverse Design System

When generating diagrams for FlowStay / FlowVue / FlowTron / any Flowverse product, use the official brand palette:

```css
:root {
  --flow-hero: #008FFF;
  --flow-hero-light: #33A5FF;
  --flow-hero-dark: #0070CC;
  --flow-glow: rgba(0, 143, 255, 0.25);
  --flow-bg: #0a0a0f;        /* FlowVue dark bg */
  --flow-surface: #13131a;
  --flow-border: rgba(255,255,255,0.08);
  --flow-text: #e8e8f0;
}
```

FlowVue is **dark-only**. FlowStay and FlowTron support both themes.

---

## Examples

**"Draw me a diagram of the API gateway architecture"**
→ Mermaid architecture diagram, Blueprint aesthetic, shows Client → Gateway → Auth → Services → Database

**"Make a comparison table of all our third-party integrations"**
→ HTML table, data-dense aesthetic, columns: Service | Category | Auth | Rate Limit | Status | Cost

**"Give me a project recap on the checkout refactor"**
→ Scrollable HTML page, sections: Status, Recent Commits, Active Work, Blockers, Next Steps

**"Slide deck on our Q2 go-to-market plan"**
→ 15–20 slide deck, editorial aesthetic, covers ICP, target pipeline, GTM channels, urgency argument

**"Review the Phase 9 routing diff"**
→ Visual diff review: before/after architecture, code quality assessment, risk flags

---

*Adapted from nicobailon/visual-explainer (MIT) for OpenClaw — March 2026*
