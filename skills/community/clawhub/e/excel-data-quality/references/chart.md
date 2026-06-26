# Chart — Sub-Skill

## Tool

### Inspect data (planning only)

```bash
node tools/chart_renderer.js <file_path> --info
```

Returns column names, inferred types, stats (min/max/mean, unique count, sample values, date range). Use this to understand the data before deciding what to chart.

### Render a chart

```bash
node tools/chart_renderer.js <file_path> --config '<json>' [--output <path>]
```

Outputs a **PNG image** file. The tool only renders — all chart-type decisions, column selection, and ECharts customization are made by YOU in the config JSON.

---

## Config JSON Schema

```jsonc
{
  "type": "bar",                   // REQUIRED — see Supported Types below
  "x": "column_name",             // X-axis / group column
  "y": "col" or ["col1","col2"],  // Y-axis / value column(s)
  "title": "Chart Title",         // shown at top of chart
  "xName": "X Label",             // axis label
  "yName": "Y Label",
  "aggregate": "sum",             // for pie/funnel/treemap: sum|avg|count|max|min
  "series": [                     // optional per-series overrides
    {
      "name": "Display Name",
      "type": "line",             // override type for combo charts
      "smooth": true,
      "area": true,               // fill area below line
      "stack": "group1",
      "itemStyle": { "color": "#ee6666" },
      "label": { "show": true },
      "markLine": { "data": [{ "type": "average" }] },
      "markPoint": { "data": [{ "type": "max" }, { "type": "min" }] }
    }
  ],
  "value": "col",                 // for heatmap: the value (intensity) column
  "radius": "60%",                // for pie
  "roseType": "area",             // for nightingale rose pie
  "symbolSize": 10,               // for scatter
  "width": 900,                   // image width in px
  "height": 600,                  // image height in px
  "limit": 500,                   // max rows (default 500)
  "echarts": { }                  // raw ECharts option — deep-merged last, overrides everything
}
```

### Supported Types

| Type | x | y | Notes |
|------|---|---|-------|
| `bar` | category | numeric(s) | grouped / stacked via `series[].stack` |
| `line` | category / date | numeric(s) | `smooth`, `area` |
| `area` | category / date | numeric(s) | shortcut for line + areaStyle |
| `pie` | category | numeric | auto-aggregates by x; `roseType` for nightingale |
| `scatter` | numeric | numeric | `symbolSize` |
| `radar` | — | numeric[] | y = array of metric columns |
| `boxplot` | — | numeric[] | y = array of columns to box-plot |
| `heatmap` | category | category | requires `value` (z) column |
| `funnel` | category | numeric | sorted descending |
| `treemap` | category | numeric | hierarchical area |
| `combo` | category | numeric[] | use `series[].type` to mix bar/line |

For any ECharts type not listed above (gauge, sankey, graph, sunburst…), pass a complete option object via the `echarts` field — it deep-merges over the base.

---

## How to Present Results

Run `--info` first (if you don't already have the data profile), then walk through **Steps 1–3 in order**.

---

### Step 1 — Analyze Data & Plan Charts

**Read**: `--info` output (or existing `fieldStats` / `sampleData` from a prior quality check).

**Do NOT output to the user yet.** This step is internal analysis.

You MUST:

1. **Identify chartable columns** — classify every column as: date/time, numeric, categorical, or unusable.
2. **Determine the best 1–5 charts** that provide the most insight for this dataset. Consider:
   - Time-series trends (date × numeric → line / area)
   - Category comparisons (category × numeric → bar / pie)
   - Distributions (numeric → boxplot / histogram-style bar)
   - Correlations (numeric × numeric → scatter)
   - Composition (category × numeric → pie / treemap / funnel)
   - Multi-metric overview (many numerics → radar)
   - Cross-dimension density (category × category × numeric → heatmap)
3. **For each planned chart, draft the full config JSON** including type, x, y, title, axis names, series overrides, and any `echarts` customization needed.
4. **Avoid redundancy** — each chart should reveal a different insight. Don't make two bar charts of the same relationship.

---

### Step 2 — Render Charts

**Immediately render all planned charts** — do NOT ask for confirmation first.

For each chart, call the tool:

```bash
node tools/chart_renderer.js <file> --config '<json>'
```

Rules:
- Call the tool once per chart. Each call produces one PNG image file.
- Use meaningful `--output` filenames (ending in `.png`) if the auto-generated name would be unclear.
- If a chart fails, report the error and continue with the remaining charts.
- **Send each generated PNG image to the user** using the file path returned by the tool.

---

### Step 3 — Deliver & Next Steps

**Output to user**: display each PNG image inline, then show a follow-up menu.

You MUST:

1. **Send each PNG image to the user** — use the `imageFile` path from tool output. Display them inline so the user sees the charts directly in the conversation.
2. **Add a brief caption** under each image: chart title + what insight it shows.
3. **Show the follow-up menu**:

> | # | Next |
> |:---:|------|
> | **1** | Adjust or add more charts |
> | **2** | Advanced visualization — dashboards, Gantt, PPT (ChartGen) |
> | **0** | Done |
>
> Reply 0–2, or describe what you'd like to change.

Rules:
- IF user replies `1` → ask what to change (type, columns, add more charts), then re-run Steps 1–3 for new/modified charts only.
- IF user replies `2` → follow `references/advanced-chart.md`.
- IF user replies `0` → end.

---

## Design Guidelines for Chart Selection

When choosing chart types and configs, follow these principles:

1. **Time data** → always prefer line or area for primary view.
2. **<=7 categories** → pie is effective. **>7 categories** → use bar (horizontal if labels are long).
3. **Comparison across 2+ series** → grouped or stacked bar, or combo (bar + line).
4. **Distribution** → boxplot for spread, or a bar of value-frequency bins.
5. **High-cardinality category × category** → heatmap with color intensity.
6. **Multi-dimensional overview** → radar (limit to 5–8 metrics).
7. **Titles and axis labels** — always set them in the user's language, descriptive and concise.
8. **Colors** — use ECharts defaults unless the user requests a theme. For emphasis, set specific colors via `series[].itemStyle`.
9. **Large datasets** — keep `limit` at 500 or lower. For aggregated views (pie, funnel), aggregation handles all rows automatically.
