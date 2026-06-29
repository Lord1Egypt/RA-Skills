---
name: apple-viz
description: Generate beautiful Apple HIG-inspired HTML visualizations (bar, line, donut, progress, stat-card) and screenshot them as PNG images. Use when user asks to visualize, chart, plot, graph, or make a viz — or explicitly says "apple-viz".
---

# Apple Viz

Generates beautiful, minimal, Apple-inspired data visualizations and saves them as PNG screenshots.

## When to use

- User asks to "visualize", "chart", "plot", "graph", or "make a viz"
- User explicitly says "apple-viz"
- User wants a stat card, progress ring, donut chart, bar chart, or line chart

## How to invoke

```bash
python3 {baseDir}/generate.py \
  --type <bar|line|donut|progress|stat-card> \
  --title "Chart Title" \
  --data '<JSON string>' \
  --output /tmp/apple-viz-output.png \
  [--width 800] [--height 500] [--dark]
```

## Chart types and data schemas

### `bar`
Vertical bars with rounded ends.
```json
{"labels": ["Mon", "Tue", "Wed"], "values": [42, 67, 55], "unit": "steps"}
```

### `line`
Smooth bezier line chart with filled gradient area.
```json
{"labels": ["Jan", "Feb", "Mar"], "values": [100, 150, 130], "unit": "ms"}
```

### `donut`
Donut/ring chart, single or multi-segment.
```json
{"segments": [{"label": "Sleep", "value": 7.5, "color": "#007AFF"}, {"label": "Awake", "value": 16.5}]}
```

### `progress`
Circular or linear progress rings.
```json
{"items": [{"label": "Steps", "value": 8200, "max": 10000, "color": "#34C759"}, {"label": "Calories", "value": 420, "max": 600, "color": "#FF9500"}]}
```

### `stat-card`
Grid of stat cards, like Apple Health summary.
```json
{"stats": [{"label": "Heart Rate", "value": "72", "unit": "BPM", "trend": "+3 BPM", "color": "#FF3B30"}, {"label": "Steps", "value": "8,241", "unit": "steps", "trend": "↑12%", "color": "#34C759"}]}
```

## Flags

- `--dark` — dark mode (black background, #F5F5F7 text)
- `--width N` — canvas width (default: 800)
- `--height N` — canvas height (default: 500)
- `--output PATH` — output PNG path (default: /tmp/apple-viz-output.png)

## Dependencies

Playwright (via npx) for screenshots. Falls back to pyppeteer if npx is unavailable.

```bash
pip3 install -r {baseDir}/requirements.txt
```
