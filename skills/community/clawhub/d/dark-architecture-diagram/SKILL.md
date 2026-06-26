---
name: dark-architecture-diagram
description: Create professional, dark-themed SVG architecture diagrams as standalone HTML files matching a specific design system with precise color tokens, typography, and component patterns. Use when the user asks for system architecture diagrams, infrastructure diagrams, technical diagrams showing system components, layer diagrams, or any diagram that should use the dark "cyberpunk-engineering" aesthetic with colored layer boundaries, numbered step circles, and card-based component layouts. Also use when the user says "用全景图风格", "暗色架构图", "dark architecture", or references this diagram style.
---

# Dark Architecture Diagram

Create standalone HTML files containing SVG architecture diagrams in a dark, technical aesthetic. The style is "cyberpunk-engineering" — dark slate backgrounds, colored layer boundaries, monospace typography, and glowing accents. Every diagram produced with this skill should look like it belongs in the same design system.

## When to Use

This skill applies when creating technical architecture diagrams that need:

- Multi-layer system visualization (e.g., presentation → logic → data)
- Component relationship mapping with flow arrows
- Numbered execution step sequences
- Dark theme with high contrast and color-coded layers

## Core Design Philosophy

The design language communicates hierarchy through color temperature and opacity rather than size alone. Each architectural layer gets a unique hue. Cards within layers use the layer's color at low opacity for fills and full saturation for strokes. Text hierarchy is maintained through a strict 5-level grayscale system. The overall feeling should be "a well-lit control room at night" — dark but highly readable.

## File Structure

Always produce a single standalone HTML file with embedded `<style>` and inline SVG. No external dependencies except the Google Fonts link for JetBrains Mono. The SVG uses a `viewBox` for responsive scaling.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Diagram Title]</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* See references/design-tokens.md for full token list */
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'JetBrains Mono', 'PingFang SC', monospace;
  background: #020617;
  color: #e2e8f0;
  min-height: 100vh;
}
</style>
</head>
<body>
<!-- Header, SVG diagram, optional summary cards, footer -->
</body>
</html>
```

## Design Token Summary

Read `references/design-tokens.md` for the complete token specification. Key tokens:

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#020617` | Page and SVG background |
| Card Fill | `#0f172a` | All card/box backgrounds |
| Grid/Border | `#1e293b` | Subtle grid lines, card borders |
| Text L1 (title) | `#f8fafc` | Main titles only |
| Text L2 (heading) | `#e2e8f0` | Section headings, step labels |
| Text L3 (body) | `#94a3b8` | Body text, descriptions |
| Text L4 (muted) | `#64748b` | Secondary info, captions |
| Text L5 (ghost) | `#475569` | Footnotes, de-emphasized |

## Layer Color System

Each architectural layer is assigned a dedicated hue. When creating a new diagram, map your layers to these colors in order of visual priority:

| Role | Color | Hex | Typical Use |
|------|-------|-----|-------------|
| Product/Presentation | Pink | `#f472b6` | Top-level user-facing layer |
| Channel/Access | Cyan | `#22d3ee` | Entry points, routing |
| Orchestrator/Core | Orange | `#fb923c` | Central coordination |
| Domain/Service | Purple | `#a78bfa` | Business domain modules |
| Capability/Tools | Green | `#34d399` | Infrastructure capabilities |
| Memory/State | Yellow | `#fbbf24` | State, caching, memory |
| Platform/Cross-cut | Rose | `#fb7185` | Cross-cutting concerns |
| Safety/Security | Red | `#ef4444` | Security boundaries |
| Steps/Flow | Sky Blue | `#0ea5e9` | Numbered execution steps |
| Gateway | Light Blue | `#38bdf8` | API gateways, auth |

## Component Patterns

Read `references/component-patterns.md` for the full component library. Key patterns:

### Layer Boundary
```svg
<rect x="40" y="30" width="1120" height="130" rx="12" fill="none" stroke="{layer-color}" stroke-width="1.5" stroke-opacity="0.3"/>
<rect x="40" y="30" width="1120" height="130" rx="12" fill="rgba({layer-rgb},0.08)"/>
<text x="60" y="55" fill="{layer-color}" font-size="11" font-weight="700">{emoji} {Layer Name}</text>
<text x="{offset}" y="55" fill="#64748b" font-size="9">{description}</text>
```

### Card Component
```svg
<rect x="60" y="70" width="160" height="72" rx="8" fill="#0f172a"/>
<rect x="60" y="70" width="160" height="72" rx="8" fill="rgba({layer-rgb},0.3)" stroke="{layer-color}" stroke-width="1"/>
<text ... fill="{layer-color}" font-size="11" font-weight="600">{emoji} {Title}</text>
<text ... fill="#94a3b8" font-size="8">{description}</text>
<text ... fill="#64748b" font-size="7">{metadata}</text>
```

### Numbered Step Circle
```svg
<circle cx="100" cy="380" r="14" fill="#0ea5e9" stroke="none"/>
<text x="100" y="384" fill="#fff" font-size="10" font-weight="700" text-anchor="middle">{N}</text>
<text x="100" y="405" fill="#e2e8f0" font-size="9" font-weight="600" text-anchor="middle">{Step Name}</text>
```

### Flow Arrows
```svg
<!-- Standard arrow -->
<line x1="..." y1="..." x2="..." y2="..." stroke="#64748b" stroke-width="1" marker-end="url(#arrowhead)"/>

<!-- Colored semantic arrow -->
<line ... stroke="#a78bfa" stroke-width="1.2" marker-end="url(#arrowhead)"/>

<!-- Dashed async/optional arrow -->
<line ... stroke="#fbbf24" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#arrowhead)"/>
```

### LLM Execution Zone (Dashed Boundary)
```svg
<rect ... rx="10" fill="url(#llmGrad)" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="6,3" stroke-opacity="0.6"/>
```

## Typography Rules

- **Font stack**: `'JetBrains Mono', 'PingFang SC', monospace`
- **Title** (page header): 22px, weight 700, color `#f8fafc`
- **Layer label**: 11px, weight 700, layer color
- **Card title**: 10-11px, weight 600, layer color
- **Body text**: 8-9px, weight 400, `#94a3b8`
- **Caption/metadata**: 7-8px, weight 400, `#64748b`
- **Ghost text**: 6-7px, weight 400-600, `#475569`

## SVG Conventions

- **viewBox**: Use a large viewBox (e.g., `0 0 1420 1400`) for detail; the SVG scales responsively via `width: 100%; height: auto`
- **Grid pattern**: 40×40 grid with `#1e293b` stroke at 0.5 opacity
- **Border radius**: `rx="12"` for layer boundaries, `rx="8"` for cards, `rx="6"` for small items, `rx="4"` for tags/chips
- **Arrow markers**: Define in `<defs>` — neutral (`#64748b`), orange, cyan variants
- **Gradients**: Use `linearGradient` for special zones (orchestrator, LLM domain) — always subtle (0.02–0.15 opacity)
- **Stroke patterns**: solid for primary boundaries, `stroke-dasharray="6,3"` for LLM zones, `stroke-dasharray="4,3"` for placeholder/expandable areas
- **Spacing**: 15-25px between layers, 10-15px between cards within a layer
- **L-shape routing**: Route arrows with right-angle bends to avoid crossing content — never diagonal through other components

## Summary Cards (Below Diagram)

Include a grid of summary cards below the SVG for key architectural decisions:

```css
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 24px; }
.card { background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 18px 20px; }
```

Each card has a colored dot matching its layer, a title, and bullet points.

## Header Pattern

Always include a header with a pulsing cyan dot and subtitle:

```css
.header h1::before {
  content: '';
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #22d3ee;
  animation: pulse 2s infinite;
}
```

## Checklist

Before finalizing any diagram, verify:

- [ ] Background is `#020617`, not black or dark gray
- [ ] All cards use `#0f172a` fill with colored overlay
- [ ] Text hierarchy follows the 5-level system
- [ ] Each layer has a unique color from the palette
- [ ] Numbered steps use `#0ea5e9` filled circles with white text
- [ ] Arrows use L-shape routing, no diagonal crossing
- [ ] Font is JetBrains Mono + PingFang SC
- [ ] Grid pattern is defined and applied to background rect
- [ ] All `rx` values follow the size convention (12/8/6/4)
- [ ] Footer text uses `#475569` at 10px
