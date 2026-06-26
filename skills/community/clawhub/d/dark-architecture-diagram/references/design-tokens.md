# Design Tokens — Dark Architecture Diagram

Complete design token specification for the dark architecture diagram style system. All values are derived from the Tailwind CSS Slate scale with custom accent overlays.

## Color Palette

### Base Colors (Slate Scale)

| Token Name | Hex | RGB | Usage |
|-----------|-----|-----|-------|
| `bg-base` | `#020617` | `2, 6, 23` | Page background, SVG background |
| `bg-card` | `#0f172a` | `15, 23, 42` | Card fills, box backgrounds, inner panels |
| `border-subtle` | `#1e293b` | `30, 41, 59` | Grid lines, card borders, separator lines |
| `border-medium` | `#334155` | `51, 65, 85` | Inner box strokes, secondary borders |
| `text-title` | `#f8fafc` | `248, 250, 252` | Page title only |
| `text-heading` | `#e2e8f0` | `226, 232, 240` | Step names, card headings, emphasis |
| `text-body` | `#94a3b8` | `148, 163, 184` | Primary body text, descriptions |
| `text-muted` | `#64748b` | `100, 116, 139` | Captions, metadata, secondary labels |
| `text-ghost` | `#475569` | `71, 85, 105` | Footnotes, version info, de-emphasized |

### Layer Accent Colors

Each color is used at multiple opacity levels:
- **Stroke**: full hex value, `stroke-opacity="0.3"` for boundary, `1.0` for cards
- **Fill overlay**: `rgba(r,g,b, 0.05–0.08)` for layer boundary, `rgba(r,g,b, 0.2–0.4)` for cards
- **Text**: full hex value for titles within that layer

| Layer Role | Hex | RGB (for rgba) | Example |
|-----------|-----|----------------|---------|
| Product/Presentation | `#f472b6` | `244, 114, 182` | `rgba(136,19,55,0.08)` boundary fill |
| Channel/Access | `#22d3ee` | `34, 211, 238` | `rgba(8,51,68,0.08)` boundary fill |
| Orchestrator/Core | `#fb923c` | `251, 146, 60` | `rgba(120,53,15,0.15)` card overlay |
| Domain/Service | `#a78bfa` | `167, 139, 250` | `rgba(76,29,149,0.25)` card overlay |
| Capability/Tools | `#34d399` | `52, 211, 153` | `rgba(6,78,59,0.3)` chip fill |
| Memory/State | `#fbbf24` | `251, 191, 36` | `rgba(120,53,15,0.25)` card overlay |
| Platform/Cross-cut | `#fb7185` | `251, 113, 133` | `rgba(136,19,55,0.05)` boundary fill |
| Safety/Security | `#ef4444` | `239, 68, 68` | `rgba(239,68,68,0.08)` box fill |
| Steps/Flow | `#0ea5e9` | `14, 165, 233` | Solid fill for step circles |
| Gateway | `#38bdf8` | `56, 189, 248` | `rgba(8,51,68,0.08)` boundary fill |
| LLM Zone | `#f59e0b` | `245, 158, 11` | Gradient + dashed border |

### Semantic Colors

| Purpose | Hex | Usage |
|---------|-----|-------|
| Arrow default | `#64748b` | Standard connection arrows |
| Arrow semantic | Layer color | Arrows that carry meaning (dispatch, return) |
| Arrow async | `#fbbf24` | Dashed arrows for async operations |
| Arrow danger | `#ef4444` | Security-related flow |
| Step circle fill | `#0ea5e9` | Numbered step indicators |
| Step circle text | `#ffffff` | Number inside step circle |

## Typography

### Font Stack

```css
font-family: 'JetBrains Mono', 'PingFang SC', monospace;
```

Load via Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Type Scale (SVG `font-size` attribute)

| Level | Size | Weight | Color | Use |
|-------|------|--------|-------|-----|
| Page Title | 22px | 700 | `#f8fafc` | Single page header |
| Subtitle | 11px | 400 | `#64748b` | Below page title |
| Layer Label | 11px | 700 | Layer color | Layer boundary name |
| Layer Description | 9px | 400 | `#64748b` | Inline after layer label |
| Card Title | 10-11px | 600 | Layer color | Card heading |
| Body | 8-9px | 400 | `#94a3b8` | Card content, flow descriptions |
| Caption | 7-8px | 400 | `#64748b` | Metadata, secondary info |
| Footnote | 6-7px | 400-600 | `#475569` | Bottom notes, version stamps |

### Letter Spacing

- Page title: `letter-spacing: 1px`
- Subtitle/footer: `letter-spacing: 0.5px`
- All other: default (0)

## Spacing & Layout

### SVG Canvas

| Property | Value |
|----------|-------|
| Typical viewBox | `0 0 1420 1400` (adjust height as needed) |
| Page padding | `padding: 0 24px 60px` |
| Max content width | `1600px` |
| Grid cell size | 40×40px |

### Layer Spacing

| Between | Gap |
|---------|-----|
| Layer boundaries | 15-25px vertical |
| Cards within layer | 10-15px horizontal |
| Layer label to content | 20-25px |
| Card padding (internal) | 10-12px |

### Border Radius Scale

| Element | `rx` value |
|---------|-----------|
| Layer boundary | 12 |
| Cards, major boxes | 8 |
| Small boxes, sub-panels | 6 |
| Tags, chips, small items | 4 |

## Gradients

### Orchestrator Gradient
```svg
<linearGradient id="orchGrad" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" style="stop-color:#fb923c;stop-opacity:0.15"/>
  <stop offset="100%" style="stop-color:#fb923c;stop-opacity:0.02"/>
</linearGradient>
```

### LLM Zone Gradient
```svg
<linearGradient id="llmGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" style="stop-color:#f59e0b;stop-opacity:0.08"/>
  <stop offset="100%" style="stop-color:#f59e0b;stop-opacity:0.02"/>
</linearGradient>
```

## Arrow Markers

```svg
<defs>
  <!-- Default gray arrow -->
  <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
  </marker>
  <!-- Orange (orchestrator) arrow -->
  <marker id="arrowOrange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#fb923c"/>
  </marker>
  <!-- Cyan (channel) arrow -->
  <marker id="arrowCyan" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#22d3ee"/>
  </marker>
</defs>
```

## Stroke Patterns

| Pattern | `stroke-dasharray` | Usage |
|---------|-------------------|-------|
| Solid | (none) | Primary boundaries, standard connections |
| LLM zone | `6,3` | Dashed boundary for LLM execution regions |
| Placeholder | `4,3` | Expandable/future components |
| Async flow | `3,2` | Async operations, optional paths |
| Security reroute | `4,2` | Security flow redirections |

## Animation

### Pulse Animation (Header Dot)
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
```
Applied to: header cyan dot, duration 2s infinite.

## CSS Tokens for HTML Elements

### Page Wrapper
```css
.page { padding: 0 24px 60px; max-width: 1600px; margin: 0 auto; }
```

### Diagram Container
```css
.diagram-wrap {
  border: 1px solid #1e293b;
  border-radius: 12px;
  overflow: hidden;
  background: #020617;
}
.diagram-wrap svg { width: 100%; height: auto; display: block; }
```

### Cards Grid
```css
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 24px; }
.card {
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 10px;
  padding: 18px 20px;
}
.card h3 { font-size: 12px; font-weight: 600; color: #e2e8f0; }
.card ul { list-style: none; font-size: 11px; color: #94a3b8; line-height: 1.8; }
```

### Card Header
```css
.card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.card-dot { width: 8px; height: 8px; border-radius: 50%; }
```

### Footer
```css
.footer {
  text-align: center;
  padding: 32px 20px;
  font-size: 10px;
  color: #475569;
  letter-spacing: 0.5px;
}
```
