# Component Patterns — Dark Architecture Diagram

Complete component library for the dark architecture diagram design system. Each pattern includes the exact SVG markup with placeholder values in `{curly braces}`.

## Table of Contents

1. [Layer Boundary](#layer-boundary)
2. [Card Component](#card-component)
3. [Channel Card (Compact)](#channel-card-compact)
4. [Numbered Step Circle](#numbered-step-circle)
5. [Execution Flow Box](#execution-flow-box)
6. [LLM Execution Zone](#llm-execution-zone)
7. [Fork/Branch Pattern](#forkbranch-pattern)
8. [Flow Arrows](#flow-arrows)
9. [Tag/Chip Grid](#tagchip-grid)
10. [Placeholder/Expandable](#placeholderexpandable)
11. [Security Zone](#security-zone)
12. [Memory/State Card](#memorystate-card)
13. [Platform Sidebar](#platform-sidebar)
14. [Legend Bar](#legend-bar)
15. [Summary Cards (HTML)](#summary-cards-html)
16. [Header (HTML)](#header-html)

---

## Layer Boundary

The primary structural element. Each architectural layer gets a boundary rect with its accent color.

```svg
<!-- Layer boundary: two overlapping rects for stroke + fill -->
<rect x="40" y="{y}" width="1120" height="{h}" rx="12"
      fill="none" stroke="{layer-color}" stroke-width="1.5" stroke-opacity="0.3"/>
<rect x="40" y="{y}" width="1120" height="{h}" rx="12"
      fill="rgba({layer-rgb},{fill-opacity})"/>

<!-- Layer label (positioned inside, top-left) -->
<text x="60" y="{y+25}" fill="{layer-color}" font-size="11" font-weight="700">
  {emoji} {Layer Name}
</text>
<!-- Optional description (same line, offset right) -->
<text x="{label-end + 20}" y="{y+25}" fill="#64748b" font-size="9">
  {description text}
</text>
```

**Parameters:**
- `fill-opacity`: `0.05` for subtle (platform), `0.08` for standard layers
- Layer label uses emoji prefix for visual scanning
- Description text is always `#64748b` at 9px

---

## Card Component

Used for individual services, agents, or modules within a layer.

```svg
<!-- Base card (dark fill) -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#0f172a"/>
<!-- Color overlay -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="rgba({layer-rgb},0.2-0.4)" stroke="{layer-color}" stroke-width="1"/>

<!-- Card title (centered or left-aligned) -->
<text x="{cx}" y="{y+22}" fill="{layer-color}" font-size="10-11"
      font-weight="600" text-anchor="middle">{emoji} {Title}</text>

<!-- Description lines (8px, #94a3b8) -->
<text x="{cx}" y="{y+38}" fill="#94a3b8" font-size="8"
      text-anchor="middle">{description line}</text>

<!-- Metadata (7px, #64748b) -->
<text x="{cx}" y="{y+52}" fill="#64748b" font-size="7"
      text-anchor="middle">{metadata}</text>

<!-- Deep metadata (7px, #475569) -->
<text x="{cx}" y="{y+64}" fill="#475569" font-size="7"
      text-anchor="middle">{deep metadata}</text>
```

**Typical sizes:**
- Standard card: 160-170w × 70-72h
- Wide card: 200-220w × 90h
- Compact card: 120-150w × 42-50h

**Fill opacity guide:**
- `0.2`: standard (domain agents)
- `0.25`: medium emphasis (execution paths)
- `0.3`: high emphasis (capabilities, active state)
- `0.4`: channel cards (maximum contrast)

---

## Channel Card (Compact)

For entry-point items like message channels, APIs, or triggers.

```svg
<rect x="{x}" y="{y}" width="220" height="36" rx="6" fill="#0f172a"/>
<rect x="{x}" y="{y}" width="220" height="36" rx="6"
      fill="rgba({layer-rgb},0.4)" stroke="{layer-color}" stroke-width="1"/>
<text x="{cx}" y="{y+23}" fill="{layer-color}" font-size="10"
      font-weight="600" text-anchor="middle">{emoji} {Channel Name}</text>
```

---

## Numbered Step Circle

For showing execution sequence (main flow or sub-flow).

### Large Step (Orchestrator level)
```svg
<circle cx="{x}" cy="{y}" r="14" fill="#0ea5e9" stroke="none"/>
<text x="{x}" y="{y+4}" fill="#fff" font-size="10" font-weight="700"
      text-anchor="middle">{N}</text>
<!-- Label below circle -->
<text x="{x}" y="{y+25}" fill="#e2e8f0" font-size="9" font-weight="600"
      text-anchor="middle">{Step Name}</text>
<!-- Optional sub-label -->
<text x="{x}" y="{y+38}" fill="#64748b" font-size="7"
      text-anchor="middle">{detail}</text>
```

### Small Step (Sub-agent level)
```svg
<circle cx="{x}" cy="{y}" r="12" fill="#a78bfa" stroke="none"/>
<text x="{x}" y="{y+4}" fill="#fff" font-size="9" font-weight="700"
      text-anchor="middle">{N}</text>
<text x="{x}" y="{y+25}" fill="#e2e8f0" font-size="8" font-weight="500"
      text-anchor="middle">{Step Name}</text>
```

### Tiny Step (Inline)
```svg
<circle cx="{x}" cy="{y}" r="10" fill="#0ea5e9" stroke="none"/>
<text x="{x}" y="{y+4}" fill="#fff" font-size="8" font-weight="700"
      text-anchor="middle">{N}</text>
```

---

## Execution Flow Box

A bounded region containing multiple steps with a labeled header.

```svg
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="#0f172a" stroke="#334155" stroke-width="1"/>
<text x="{x+20}" y="{y+20}" fill="#94a3b8" font-size="9" font-weight="600">
  {Flow Title}
</text>
<!-- Steps placed inside -->
```

---

## LLM Execution Zone

A dashed boundary indicating an LLM reasoning region that may loop.

```svg
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"
      fill="url(#llmGrad)" stroke="#f59e0b" stroke-width="1.5"
      stroke-dasharray="6,3" stroke-opacity="0.6"/>
<text x="{x+20}" y="{y+10}" fill="#f59e0b" font-size="10" font-weight="700">
  ⚡ LLM 推理域
</text>
<text x="{x+150}" y="{y+10}" fill="#64748b" font-size="8">
  （可能多轮循环）
</text>
```

---

## Fork/Branch Pattern

When a flow splits into two or more paths.

```svg
<!-- Path A: labeled line going one direction -->
<line x1="{fork-x}" y1="{fork-y}" x2="{target-x}" y2="{target-y}"
      stroke="{color-a}" stroke-width="1.2" marker-end="url(#arrowhead)"/>
<text x="{mid-x}" y="{mid-y - 7}" fill="{color-a}" font-size="7"
      font-weight="600">{Label A}</text>

<!-- Path B: labeled line going another direction -->
<line x1="{fork-x}" y1="{fork-y+15}" x2="{target-x}" y2="{target-y}"
      stroke="{color-b}" stroke-width="1.2" marker-end="url(#arrowhead)"/>
<text x="{mid-x}" y="{mid-y}" fill="{color-b}" font-size="7"
      font-weight="600">{Label B}</text>
```

---

## Flow Arrows

### Standard (neutral)
```svg
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
      stroke="#64748b" stroke-width="1" marker-end="url(#arrowhead)"/>
```

### Semantic (colored, slightly thicker)
```svg
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
      stroke="{semantic-color}" stroke-width="1.2" marker-end="url(#arrowhead)"/>
```

### Async/Optional (dashed)
```svg
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
      stroke="{color}" stroke-width="1" stroke-dasharray="3,2"
      marker-end="url(#arrowhead)"/>
```

### L-Shape Route (avoid crossing)
```svg
<!-- Horizontal first, then vertical, then horizontal -->
<line x1="{start-x}" y1="{start-y}" x2="{corner1-x}" y2="{start-y}"
      stroke="{color}" stroke-width="1.2" stroke-opacity="0.5" stroke-dasharray="5,3"/>
<line x1="{corner1-x}" y1="{start-y}" x2="{corner1-x}" y2="{corner2-y}"
      stroke="{color}" stroke-width="1.2" stroke-opacity="0.5" stroke-dasharray="5,3"/>
<line x1="{corner1-x}" y1="{corner2-y}" x2="{end-x}" y2="{corner2-y}"
      stroke="{color}" stroke-width="1.2" marker-end="url(#arrowhead)"/>
```

### Vertical Return Arrow (with label)
```svg
<line x1="{x}" y1="{start-y}" x2="{x}" y2="{end-y}"
      stroke="{color}" stroke-width="1" marker-end="url(#arrowhead)"/>
<text x="{x+12}" y="{mid-y}" fill="{color}" font-size="7"
      writing-mode="tb">{label text}</text>
```

---

## Tag/Chip Grid

For listing capabilities, tools, or features in a compact grid.

```svg
<!-- Single chip -->
<rect x="{x}" y="{y}" width="68" height="22" rx="4"
      fill="rgba({layer-rgb},0.3)" stroke="{layer-color}" stroke-width="0.5"/>
<text x="{cx}" y="{y+14}" fill="{layer-color}" font-size="7"
      text-anchor="middle">{Chip Label}</text>
```

**Layout:** 2-column grid with 6px gap between columns, 6px gap between rows. Typical chip width: 68px, height: 22px.

---

## Placeholder/Expandable

For "more items" or future expansion slots.

```svg
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="4,3"/>
<text x="{cx}" y="{cy-10}" fill="#64748b" font-size="14-18"
      text-anchor="middle">···</text>
<text x="{cx}" y="{cy+10}" fill="#475569" font-size="8"
      text-anchor="middle">{placeholder text}</text>
```

---

## Security Zone

For security-related execution boundaries (SafeRoom, auth gates).

```svg
<!-- Security box -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#0f172a"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"
      fill="rgba(239,68,68,0.08)" stroke="#ef4444" stroke-width="1"
      stroke-opacity="0.6"/>

<!-- Title with lock emoji -->
<text x="{cx}" y="{y+14}" fill="#ef4444" font-size="8" font-weight="700"
      text-anchor="middle">🔒 {Security Zone Name}</text>

<!-- Steps listed vertically -->
<text x="{x+10}" y="{y+29}" fill="#94a3b8" font-size="7">
  ① {step description}
</text>
```

### Security Flow Arrow (dashed red with loop-back)
```svg
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
      stroke="#ef4444" stroke-width="1.2" stroke-dasharray="4,2"
      stroke-opacity="0.8"/>
```

---

## Memory/State Card

For memory system sub-components with capacity indicators.

```svg
<rect x="{x}" y="{y}" width="95" height="68" rx="6"
      fill="rgba({memory-rgb},0.25-0.3)" stroke="{memory-color}" stroke-width="1"/>
<text x="{cx}" y="{y+16}" fill="{memory-color}" font-size="7-8"
      font-weight="600" text-anchor="middle">{Memory Type}</text>
<text x="{cx}" y="{y+29}" fill="#94a3b8" font-size="6"
      text-anchor="middle">{description}</text>
<text x="{cx}" y="{y+40}" fill="#64748b" font-size="6"
      text-anchor="middle">{scope/isolation info}</text>
<!-- Capacity bar (text-based) -->
<text x="{cx}" y="{y+62}" fill="#475569" font-size="6"
      text-anchor="middle">Token: ████ {level}</text>
```

### Privacy Isolation Indicator
```svg
<rect x="{x}" y="{y}" width="{w}" height="16" rx="4"
      fill="rgba(239,68,68,0.1)" stroke="#ef4444" stroke-width="0.8"
      stroke-opacity="0.5"/>
<text x="{cx}" y="{y+11}" fill="#ef4444" font-size="6" font-weight="600"
      text-anchor="middle">🔒 {isolation policy text}</text>
```

---

## Platform Sidebar

A tall vertical panel on the right side for cross-cutting platform capabilities.

```svg
<!-- Outer boundary -->
<rect x="1185" y="30" width="210" height="{total-h}" rx="12"
      fill="none" stroke="#fb7185" stroke-width="1.5" stroke-opacity="0.3"/>
<rect x="1185" y="30" width="210" height="{total-h}" rx="12"
      fill="rgba(136,19,55,0.05)"/>

<!-- Vertical title -->
<text x="1290" y="55" fill="#fb7185" font-size="11" font-weight="700"
      text-anchor="middle">🏗️ {Platform Title}</text>
<text x="1290" y="72" fill="#64748b" font-size="8"
      text-anchor="middle">{subtitle}</text>

<!-- Platform item (major, with sub-grid) -->
<rect x="1200" y="{y}" width="180" height="{h}" rx="6"
      fill="#0f172a" stroke="#fb7185" stroke-width="1.2" stroke-opacity="0.7"/>
<text x="1290" y="{y+18}" fill="#fb7185" font-size="9" font-weight="700"
      text-anchor="middle">{emoji} {Item Title}</text>
<!-- Sub-items in 2-column grid -->
<rect x="1208" y="{y+26}" width="82" height="24" rx="4"
      fill="rgba(251,113,133,0.1)" stroke="#fb7185" stroke-width="0.5"
      stroke-opacity="0.4"/>
<text x="1249" y="{y+42}" fill="#94a3b8" font-size="7"
      text-anchor="middle">{sub-item}</text>

<!-- Platform item (minor, no sub-grid) -->
<rect x="1200" y="{y}" width="180" height="42" rx="6"
      fill="#0f172a" stroke="#fb7185" stroke-width="0.8" stroke-opacity="0.5"/>
<text x="1290" y="{y+18}" fill="#fb7185" font-size="9" font-weight="600"
      text-anchor="middle">{emoji} {Item Title}</text>
<text x="1290" y="{y+35}" fill="#64748b" font-size="7"
      text-anchor="middle">{description}</text>
```

**Platform item stroke weight hierarchy:**
- Major items (with sub-grid): `stroke-width="1.2"` `stroke-opacity="0.7"`
- Minor items: `stroke-width="0.8"` `stroke-opacity="0.5"`

---

## Legend Bar

Placed at the bottom of the SVG to explain color coding.

```svg
<rect x="40" y="{y}" width="1355" height="50" rx="8"
      fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
<text x="60" y="{y+20}" fill="#64748b" font-size="8" font-weight="600">
  LEGEND
</text>

<!-- Legend items (circle + label pairs) -->
<circle cx="{x}" cy="{y+27}" r="4" fill="{color}"/>
<text x="{x+10}" y="{y+30}" fill="#94a3b8" font-size="8">{label}</text>

<!-- Special legend items -->
<!-- Dashed rect for zones -->
<rect x="{x}" y="{y+22}" width="20" height="10" rx="2"
      fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="3,2"/>
<text x="{x+26}" y="{y+30}" fill="#94a3b8" font-size="8">{zone label}</text>

<!-- Step circle mini -->
<circle cx="{x}" cy="{y+27}" r="8" fill="#0ea5e9"/>
<text x="{x}" y="{y+30}" fill="#fff" font-size="6" font-weight="700"
      text-anchor="middle">N</text>
<text x="{x+14}" y="{y+30}" fill="#94a3b8" font-size="8">执行步骤</text>
```

---

## Summary Cards (HTML)

```html
<div class="cards">
  <div class="card">
    <div class="card-header">
      <div class="card-dot" style="background:{layer-color}"></div>
      <h3>{Card Title}</h3>
    </div>
    <ul>
      <li>• {point 1}</li>
      <li>• {point 2}</li>
      <li>• {point 3}</li>
    </ul>
  </div>
  <!-- Repeat for each card (typically 4) -->
</div>
```

---

## Header (HTML)

```html
<div class="header">
  <h1>{Diagram Title}</h1>
  <div class="subtitle">{Technical subtitle in English}</div>
</div>
```

The `h1::before` pseudo-element creates the pulsing cyan dot automatically via CSS.

---

## Composition Rules

When assembling a full diagram:

1. **Top to bottom**: Layers stack vertically with ~20px gaps
2. **Left main + right sidebar**: Main content in 1120px width, optional platform sidebar at x=1185 with 210px width
3. **Flow direction**: Primary flow goes left→right within layers, top→bottom between layers
4. **Step numbering**: Main flow uses `#0ea5e9` large circles; sub-flows use layer-colored smaller circles
5. **Cross-layer arrows**: Use L-shape routing along the left margin (x=55) to avoid crossing content
6. **Return arrows**: Vertical lines with `writing-mode="tb"` labels on the right side
7. **Legend**: Always at the SVG bottom, spanning full width
8. **Summary cards**: HTML below the SVG, 4-column grid
