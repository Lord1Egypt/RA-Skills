---
name: d3js
description: D3.js (Data-Driven Documents) — A JavaScript library for data visualization. Covers installation, selections, data binding, scales, shapes, transitions, 30+ module reference, chart templates, React/Svelte integration. For custom SVG/Canvas visualizations.
---

# D3.js

> D3 v7 · Low-level toolbox · 30+ composable modules · Web standards (SVG/Canvas/DOM)

## Installation

```
ESM: import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm"
UMD: <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
npm: npm install d3 → import * as d3 from "d3"
Submodules: import {mean} from "d3-array"
```

## 1-Minute Bar Chart

```js
import * as d3 from "d3";
const data = [10, 20, 30, 40, 50];
const svg = d3.create("svg").attr("width", 400).attr("height", 200);
const x = d3.scaleBand().domain(data.map((d,i)=>i)).range([0,350]).padding(.2);
const y = d3.scaleLinear().domain([0, d3.max(data)]).range([150, 0]);
svg.selectAll("rect").data(data).join("rect")
  .attr("x", (d,i)=>x(i)).attr("y", d=>y(d))
  .attr("width", x.bandwidth()).attr("height", d=>150-y(d))
  .attr("fill", "steelblue");
document.getElementById("chart").append(svg.node());
```

## Module Index

| Module | Purpose | Location |
|--------|---------|----------|
| selection/scale/shape/axis/transition/path/ease | Selections·Scales·Shapes·Axes·Transitions·Path·Easing | essentials |
| array/format/interpolate/color/random/dispatch/timer | Array stats·Number format·Interpolation·Color·Random·Events·Timer | advanced |
| polygon/quadtree/delaunay/chord/contour | Polygons·Quadtree·Delaunay·Chord·Contour | advanced |
| force/hierarchy/geo/zoom/brush/drag | Force·Hierarchy·Geo·Zoom·Brush·Drag | advanced |
| dsv/fetch/time/time-format | CSV·Fetch·Time intervals·Time format | data |
| scale-chromatic | Color schemes (schemeCategory10/interpolateViridis) | essentials |

## Progressive Loading

| File | Content |
|------|---------|
| [essentials.md](references/essentials.md) | Selections·Data join·Scales·Axes·Shapes·Transitions·Easing·Path·5 chart templates·React/Svelte·Margin |
| [data.md](references/data.md) | CSV/JSON/TSV loading·Parsing·Formatting·Time intervals·Time formatting |
| [advanced.md](references/advanced.md) | Array stats·Interpolation·Color·Random·Events·Timer·Polygons·Quadtree·Chord·Contour·Delaunay·Force·Hierarchy·Geo·Zoom·Brush·Drag |

Usage principle: D3 has no "chart" abstraction. Visualizations are built by composing selections + scales + shapes + axes. No automatic chart generation — only component-level precise control. Use Canvas for 5000+ data points.