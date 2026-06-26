---
name: architecture-diagram
description: Create professional, dark-themed architecture diagrams as standalone HTML files with inline SVG graphics. Use when the user asks for system architecture diagrams, infrastructure diagrams, cloud architecture visualizations, security diagrams, network topology diagrams, or any technical diagram showing system components and their relationships. Based on Cocoon-AI/architecture-diagram-generator.
license: MIT
metadata:
  version: "1.0"
  author: Cocoon AI (hello@cocoon-ai.com)
  source: https://github.com/Cocoon-AI/architecture-diagram-generator
---

# Architecture Diagram Skill

Create professional technical architecture diagrams as self-contained HTML files with inline SVG graphics and CSS styling.

## When to Use

- User asks for "architecture diagram", "system diagram", "技术架构图"
- User wants to visualize system components and relationships
- User needs cloud architecture (AWS/GCP/Azure), network topology, or security diagrams
- User asks to "生成架构图", "画一个系统图", "可视化XXX架构"

## Design System

### Color Palette

Use these semantic colors for component types:

| Component Type | Fill (rgba) | Stroke |
|---------------|-------------|--------|
| Frontend | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) |
| Backend | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) |
| Database | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) |
| AWS/Cloud | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) |
| Security | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) |
| Message Bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400) |
| External/Generic | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) |

### Typography

Use JetBrains Mono for all text:
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Font sizes: 12px for component names, 9px for sublabels, 8px for annotations, 7px for tiny labels.

### Visual Elements

**Background:** `#020617` (slate-950) with subtle grid pattern:
```svg
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
</pattern>
```

**Component boxes:** Rounded rectangles (`rx="6"`) with 1.5px stroke, semi-transparent fills.

**Security groups:** Dashed stroke (`stroke-dasharray="4,4"`), transparent fill, rose color.

**Region boundaries:** Larger dashed stroke (`stroke-dasharray="8,4"`), amber color, `rx="12"`.

**Arrows:** Use SVG marker for arrowheads:
```svg
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />
</marker>
```

**Arrow z-order:** Draw connection arrows early in the SVG (after the background grid) so they render behind component boxes.

**Masking arrows behind transparent fills:** Since component boxes use semi-transparent fills, draw an opaque background rect first:
```svg
<!-- Opaque background to mask arrows -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#0f172a"/>
<!-- Styled component on top -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="rgba(76, 29, 149, 0.4)" stroke="#a78bfa" stroke-width="1.5"/>
```

### Spacing Rules

- **Standard component height:** 60px for services, 80-120px for larger components
- **Minimum vertical gap between components:** 40px
- Place inline connectors (message buses) IN the gap between components, not overlapping

### Legend Placement

Place legends OUTSIDE all boundary boxes. Place at least 20px below the lowest boundary. Expand SVG viewBox height if needed.

## Layout Structure

1. **Header** - Title with pulsing dot indicator, subtitle
2. **Main SVG diagram** - Contained in rounded border card
3. **Summary cards** - Grid of 3-4 cards below diagram with key details
4. **Footer** - Minimal metadata line

## Output

Always produce a single self-contained `.html` file with:
- Embedded CSS (no external stylesheets except Google Fonts)
- Inline SVG (no external images)
- No JavaScript required (pure CSS animations)

Deploy with the `deploy` tool to a `/tmp/xxx/index.html` directory.

## Example: Component Box

```svg
<rect x="100" y="100" width="160" height="70" rx="6" fill="#0f172a"/>
<rect x="100" y="100" width="160" height="70" rx="6"
      fill="rgba(8, 51, 68, 0.4)" stroke="#22d3ee" stroke-width="1.5"/>
<text x="180" y="126" fill="white" font-size="11" font-weight="600" text-anchor="middle">Frontend</text>
<text x="180" y="142" fill="#94a3b8" font-size="9" text-anchor="middle">React + TypeScript</text>
```
