# Echarts-AI-Skill

<div align="center">

**Give your AI agent a charting skill.**

Turn requests like **"use my data and generate a pie chart"** into deterministic ECharts options and exportable `HTML` / `SVG` chart artifacts.

[![Release](https://img.shields.io/github/v/release/davaded/Echarts-AI-Skill)](https://github.com/davaded/Echarts-AI-Skill/releases)
[![License](https://img.shields.io/github/license/davaded/Echarts-AI-Skill)](./LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![ECharts](https://img.shields.io/badge/ECharts-5.x-AA344D)](https://echarts.apache.org/)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111111)](./SKILL.md)

English | [简体中文](./README.zh-CN.md)

</div>

---

## Why This Skill Exists

AI agents are already good at writing code, editing docs, and running workflows.
But when a user says:

- "Use my sales data and generate a pie chart."
- "Compare these weekly metrics and give me a bar chart."
- "Pick the right chart from this table and export it to my Desktop."
- "Render this chart as SVG so I can drop it into a report."

most agents still need a stable chart execution layer underneath.

`Echarts-AI-Skill` is that layer.

It gives your agent a deterministic path from **data request -> chart recommendation -> ECharts option -> exportable artifact**.

## What Your Agent Can Do Today

### Built-in recommendation

For generic table-shaped input, the skill currently auto-recommends:

- `line`
- `bar`
- `pie`
- `scatter`

### Explicit chart generation

If the request explicitly sets `chartType`, the current builder supports:

- `line`
- `bar`
- `pie`
- `scatter`
- `effectScatter`
- `radar`
- `funnel`
- `gauge`
- `heatmap`
- `treemap`
- `sunburst`
- `sankey`
- `graph`
- `candlestick`
- `boxplot`
- `parallel`
- `map`
- `lines`

### Chart Type Reference

| Type | Chinese |
| --- | --- |
| `line` | 折线图 |
| `bar` | 柱状图 / 条形图 |
| `pie` | 饼图 |
| `scatter` | 散点图 |
| `effectScatter` | 涟漪散点图 |
| `radar` | 雷达图 |
| `funnel` | 漏斗图 |
| `gauge` | 仪表盘 |
| `heatmap` | 热力图 |
| `treemap` | 矩形树图 |
| `sunburst` | 旭日图 |
| `sankey` | 桑基图 |
| `graph` | 关系图 |
| `candlestick` | K 线图 |
| `boxplot` | 箱线图 |
| `parallel` | 平行坐标图 |
| `map` | 地图 |
| `lines` | 线路图 / 迁徙线图 |

Also supported:

- interactive `HTML` preview export
- server-rendered `SVG` export
- explicit friendly output paths like `desktop`, `home`, and `~`
- Codex workflow instructions in [`SKILL.md`](./SKILL.md)

## Use Cases

### 1. Turn category totals into a pie chart

User intent:

> Use my category totals and generate a pie chart.

What the skill does:

- maps category/value fields
- builds a valid pie-chart option
- exports an HTML preview or SVG artifact

### 2. Compare weekly metrics with a bar chart

User intent:

> Compare these weekly performance numbers and give me a bar chart.

What the skill does:

- recognizes comparison-oriented data
- recommends `bar`
- produces a deterministic ECharts option

### 3. Generate a trend view from time-series data

User intent:

> Use this progress dataset and generate a line chart.

What the skill does:

- detects the time-like field
- recommends `line`
- exports a preview for quick review

### 4. Render richer charts when the request is explicit

User intent:

> Use these nodes and links and generate a sankey chart.

What the skill does:

- accepts chart-specific request fields
- builds richer ECharts series such as `radar`, `sankey`, `graph`, `gauge`, and `heatmap`
- keeps the generation path deterministic instead of free-form

### 5. Save chart artifacts where the user expects

User intent:

> Export the result to my Desktop.

What the skill does:

- supports `desktop`, `home`, and `~`
- writes to a friendly path without forcing users to manage exact file names

## Quick Start

```powershell
npm install
```

Typical workflow:

```powershell
node dist/cli/recommend-chart.js --input examples\study-progress.request.json
node dist/cli/generate-chart.js --input examples\study-progress.request.json
node dist/cli/render-chart.js --input option.json --format html
node dist/cli/render-chart.js --input option.json --format svg
```

## Demo

- Product-style showcase page: [`examples/product-demo.html`](./examples/product-demo.html)
- Study trend request: [`examples/study-progress.request.json`](./examples/study-progress.request.json)
- Pie chart request: [`examples/pie-chart.request.json`](./examples/pie-chart.request.json)
- Radar request: [`examples/radar.request.json`](./examples/radar.request.json)
- Gauge request: [`examples/gauge.request.json`](./examples/gauge.request.json)
- Heatmap request: [`examples/heatmap.request.json`](./examples/heatmap.request.json)
- Sankey request: [`examples/sankey.request.json`](./examples/sankey.request.json)
- Graph request: [`examples/graph.request.json`](./examples/graph.request.json)

If you want a more product-like local preview, open `examples/product-demo.html` in a browser.

## Publishing Metadata

This repo now includes cross-ecosystem packaging metadata:

- [`SKILL.md`](./SKILL.md) for Codex/OpenClaw-style skill instructions
- [`manifest.yaml`](./manifest.yaml) for publish-oriented metadata
- [`agents/openai.yaml`](./agents/openai.yaml) for OpenAI-style skill metadata

For ClawHub/OpenClaw publishing, the remaining step is running the platform CLI from this repository after login.

## Example Agent-Oriented Request

```json
{
  "title": "Category sales share",
  "chartType": "pie",
  "dataset": [
    { "category": "Books", "amount": 3200 },
    { "category": "Courses", "amount": 5100 },
    { "category": "Templates", "amount": 1700 }
  ],
  "categoryField": "category",
  "valueField": "amount"
}
```

This maps naturally to a user request like:

> Use my category totals and generate a pie chart.

## Output Rules

- `--out` writes to an exact file path
- `--out-dir` writes to a directory using the default output filename
- `desktop`, `home`, and `~` are supported in path resolution when the user explicitly asks for those locations
- If no path is provided, output defaults to the current working directory

Default filenames:

- `recommend` -> `spec.json`
- `generate` -> `option.json`
- `render --format html` -> `preview.html`
- `render --format svg` -> `preview.svg`

## Project Structure

```text
src/
  cli/      command entrypoints
  core/     recommendation, option building, rendering
  types/    request/spec types
examples/   sample inputs and demo pages
agents/     cross-platform skill metadata
SKILL.md    Codex skill instructions
manifest.yaml publish-oriented metadata
```

## Scope

### Current

- Structured chart input
- Common chart recommendation
- Broad explicit `chartType` support
- HTML and SVG export
- Codex skill workflow
- Universal packaging metadata for skill ecosystems

### Next

- Natural language to `ChartRequest`
- More chart-family-specific validation rules
- Chart explanation and refinement workflows
- MCP server packaging

## License

Released under the [MIT License](./LICENSE).
