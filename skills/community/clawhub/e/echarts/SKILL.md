---
name: echarts
description: Create Apache ECharts option JSON, standalone HTML chart pages, and export-ready chart artifacts from CSV, TSV, JSON tables, or existing option configs. Use when a user asks for ECharts charts, dashboards, chart configs, preview pages, PNG or SVG-ready chart deliverables, or help turning structured data into practical ECharts visuals.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "homepage": "https://echarts.apache.org/",
        "requires": { "anyBins": ["node", "bun"] },
      },
  }
---

# ECharts

Build ECharts artifacts that are easy to preview, revise, export, and share in OpenClaw workspaces. Prefer saving actual files over leaving the chart design only in chat.

## Workflow

1. If the user already has an ECharts option object, refine it and run `page`.
2. If the user has structured data in CSV, TSV, or JSON, run `table`.
3. If the user only has a small inline list, run `sample`.
4. If the user needs a static image, either add `--export-image png|svg` during build or run `node {baseDir}/scripts/render-image.mjs --input <artifact-dir> --type png|svg` afterward.

`bun` can be used anywhere below where `node` appears.

## Quick Start

Quick line or bar chart from inline data:

```bash
node {baseDir}/scripts/build.mjs sample --chart line --categories Jan,Feb,Mar,Apr --series Revenue:120,160,210,260 --series Profit:24,30,42,51 --title "Revenue and Profit" --subtitle "Sample series" --out ./artifacts/revenue-profit
```

Generate a chart from a CSV, TSV, or JSON table:

```bash
node {baseDir}/scripts/build.mjs table --input ./data/sales.csv --chart bar --x month --y revenue,profit --title "Monthly sales" --page-mode report --out ./artifacts/monthly-sales
```

Build and export a PNG in one step:

```bash
node {baseDir}/scripts/build.mjs sample --chart line --categories Jan,Feb,Mar,Apr --series Revenue:120,160,210,260 --title "Quarterly trend" --renderer svg --export-image png --out ./artifacts/quarterly-trend
```

Build and export both PNG and SVG in one run:

```bash
node {baseDir}/scripts/build.mjs sample --chart line --categories Jan,Feb,Mar,Apr --series Revenue:120,160,210,260 --title "Quarterly trend" --renderer svg --export-image png --export-image svg --out ./artifacts/quarterly-trend-both
```

Package an existing option file into a standalone preview page:

```bash
node {baseDir}/scripts/build.mjs page --option ./option.json --renderer svg --theme paper --title "Release dashboard" --out ./artifacts/release-dashboard
```

Lint an option file before handing it off:

```bash
node {baseDir}/scripts/lint-option.mjs ./artifacts/release-dashboard/chart.option.json
```

Export a static image from a generated artifact directory:

```bash
node {baseDir}/scripts/render-image.mjs --input ./artifacts/monthly-sales --type png
node {baseDir}/scripts/render-image.mjs --input ./artifacts/release-dashboard --type svg
```

## 中文示例

销售趋势折线图：

```bash
node {baseDir}/scripts/build.mjs sample --chart line --categories 1月,2月,3月,4月 --series 销售额:120,168,210,256 --series 毛利:32,45,58,73 --title "月度销售趋势" --subtitle "示例数据" --out ./artifacts/zh-sales-line
```

值班热力图：

```bash
node {baseDir}/scripts/build.mjs sample --chart heatmap --x-categories 周一,周二,周三,周四,周五 --y-categories 上午,下午,晚上 --matrix '4,6,7,5,3;7,8,9,6,5;3,4,6,5,4' --title "客服值班热力图" --out ./artifacts/zh-heatmap
```

渠道转化桑基图：

```bash
node {baseDir}/scripts/build.mjs sample --chart sankey --link "广告>注册:380" --link "自然流量>注册:240" --link "注册>激活:410" --link "激活>付费:126" --title "渠道转化流向" --out ./artifacts/zh-sankey
```

股票 K 线：

```bash
node {baseDir}/scripts/build.mjs sample --chart candlestick --categories 周一,周二,周三,周四 --ohlc '12,15,11,16;15,14,13,17;14,18,13,19;18,17,16,20' --title "示例 K 线" --out ./artifacts/zh-candlestick
```

团队协作关系图：

```bash
node {baseDir}/scripts/build.mjs sample --chart graph --link "产品>设计:8" --link "产品>前端:12" --link "前端>后端:10" --link "后端>运维:6" --node "产品:30:业务" --node "设计:24:设计" --node "前端:28:研发" --node "后端:28:研发" --node "运维:22:平台" --title "团队协作网络" --out ./artifacts/zh-graph
```

多指标平行坐标：

```bash
node {baseDir}/scripts/build.mjs sample --chart parallel --dimensions 响应时间,稳定性,成本,易用性 --series 方案A:88,93,52,74 --series 方案B:72,85,66,91 --series 方案C:64,90,80,69 --title "方案对比" --out ./artifacts/zh-parallel
```

日历热力图：

```bash
node {baseDir}/scripts/build.mjs sample --chart calendar --dates 2026-03-01,2026-03-02,2026-03-03,2026-03-04,2026-03-05,2026-03-06,2026-03-07 --values 12,18,9,20,16,24,14 --title "周活跃日历" --out ./artifacts/zh-calendar
```

时间流带图：

```bash
node {baseDir}/scripts/build.mjs sample --chart themeRiver --dates 2026-03-01,2026-03-02,2026-03-03,2026-03-04 --series 广告:120,140,130,150 --series 自然流量:90,105,115,118 --series 转介绍:30,42,40,46 --title "渠道流量流带图" --out ./artifacts/zh-theme-river
```

瀑布变化图：

```bash
node {baseDir}/scripts/build.mjs sample --chart waterfall --categories 新签,退款,扩容,流失 --values 120,-30,45,-10 --title "净变化瀑布图" --out ./artifacts/zh-waterfall
```

南北区极坐标柱状图：

```bash
node {baseDir}/scripts/build.mjs sample --chart polarBar --categories 华北,华东,华南,西南 --series 营收:120,98,140,110 --title "区域营收极坐标图" --out ./artifacts/zh-polar-bar
```

玫瑰饼图：

```bash
node {baseDir}/scripts/build.mjs sample --chart rosePie --labels 搜索,直接访问,社交,邮件 --values 420,310,180,90 --title "渠道结构玫瑰图" --out ./artifacts/zh-rose-pie
```

## Artifacts

The builder writes a stable file set:

- `chart.spec.json`: normalized build request and mappings
- `chart.option.json`: ECharts config kept as the source of truth
- `chart.data.json`: normalized input rows when source data was provided
- `chart.html`: standalone preview and export page
- `manifest.json`: small index of generated files and settings
- optional exported image such as `<fileBase>.png` or `<fileBase>.svg`

Keep `chart.option.json` even when the user only asked for a preview page. It is the easiest artifact to diff, review, and reuse later. Static image exports can be created on demand with `scripts/render-image.mjs` or directly during build with one or more `--export-image` flags, and default to `<fileBase>.png` or `<fileBase>.svg` inside the artifact directory. `manifest.json` keeps single-image compatibility in `files.image`, and records multi-format exports in `files.images`.

## Input Modes

### `sample`

Best for quick drafts from short lists.

- `bar`, `line`, `area`, `polarBar`: use `--categories` plus one or more `--series Name:1,2,3`
- `pictorialBar`: use `--categories` plus one or more `--series Name:1,2,3`
- `pie`: use `--labels` plus `--values`
- `rosePie`: use `--labels` plus `--values`
- `funnel`: use `--labels` plus `--values`
- `gauge`: use `--values`, optional `--labels`, optional `--maxes` or shared `--max-value`
- `heatmap`: use `--x-categories`, `--y-categories`, and `--matrix`
- `waterfall`: use `--categories` and `--values`
- `calendar`: use `--dates` and `--values`
- `themeRiver`: use `--dates` plus one or more `--series Name:1,2,3`
- `candlestick`: use `--categories` and `--ohlc open,close,low,high;...`
- `boxplot`: use `--categories` and `--boxes low,q1,median,q3,high;...`
- `sankey`: use repeated `--link Source>Target:Value` or a single `--links` list
- `graph`: use repeated `--link Source>Target:Value`, with optional repeated `--node Name[:Size[:Group]]`
- `tree`: use `--labels`, `--values`, and optional `--parents`
- `parallel`: use `--dimensions MetricA,MetricB,...` plus one or more `--series Name:1,2,3`
- `radar`: use `--indicators` plus one or more `--series Name:1,2,3`
- `treemap`: use `--labels`, `--values`, and optional `--parents`
- `sunburst`: use `--labels`, `--values`, and optional `--parents`

### `table`

Best for real data files.

- `bar`, `line`, `area`, `polarBar`: `--x <field>` and `--y field1,field2`
- `pictorialBar`: `--x <field>` and `--y field1,field2`
- `pie`: `--label <field>` and `--value <field>`
- `rosePie`: `--label <field>` and `--value <field>`
- `funnel`: `--label <field>` and `--value <field>`
- `gauge`: `--value <field>` plus optional `--label`, `--max-field`, or shared `--max-value`
- `heatmap`: `--x <field> --y <field> --value <field>`
- `waterfall`: `--x <field> --value <field>`
- `calendar`: `--date <field> --value <field>`
- `themeRiver`: `--date <field> --value <field> --series-field <field>`
- `candlestick`: `--x <field> --open <field> --close <field> --low <field> --high <field>`
- `boxplot`: `--x <field> --low <field> --q1 <field> --median <field> --q3 <field> --high <field>`
- `sankey`: `--source <field> --target <field> --value <field>`
- `graph`: `--source <field> --target <field>` plus optional `--value`, `--source-group`, `--target-group`, `--source-size`, `--target-size`
- `tree`: `--label <field> --value <field>` plus optional `--parent-field`
- `parallel`: `--name-field <field> --y metric1,metric2,metric3`
- `scatter`: `--x <field> --y <field>` plus optional `--series-field`, `--size-field`, `--label-field`
- `radar`: `--name-field <field> --y metric1,metric2,metric3`
- `treemap`: `--label <field> --value <field>` plus optional `--parent-field`
- `sunburst`: `--label <field> --value <field>` plus optional `--parent-field`

### `page`

Best when the option already exists and only needs a polished preview or export wrapper.

- Accepts JSON option files
- Preserves the option as JSON and wraps it in the standalone HTML template
- Use `--renderer svg` when the final deliverable should stay vector-friendly

## Export Guidance

- Use `--renderer svg` for vector exports, design reviews, and docs-friendly embeds.
- Use `--renderer canvas` for crisp PNG output and heavier charts.
- Use `--export-image png` or `--export-image svg` during `build.mjs` for one-step image output.
- Repeat `--export-image` to export multiple formats in one run, for example `--export-image png --export-image svg`.
- Use `node {baseDir}/scripts/render-image.mjs --input ./artifacts/chart-name --type png` for direct PNG export.
- Use `node {baseDir}/scripts/render-image.mjs --input ./artifacts/chart-name --type svg` for direct SVG export from SVG-rendered pages.
- `--export-image svg` requires `--renderer svg`.
- When exporting multiple formats, `--image-out` must point to a directory or a path without an extension.
- `render-image.mjs` auto-detects Chrome or Edge. If detection fails, pass `--browser-executable <path>` or set `ECHARTS_BROWSER_PATH`.
- `chart.html` still includes buttons for PNG download, SVG download when SVG renderer is active, JSON download, and clipboard copy.
- The generated page first tries the configured CDN and then common public mirrors. If the environment is fully offline, rerun with `--cdn <url>` pointing to a local or mirrored bundle.

## Authoring Rules

- Choose the simplest chart that answers the question. Do not default to dashboards when one chart is enough.
- Keep units in titles, axis names, or notes when the metric is ambiguous.
- Use `references/chart-selection.md` when deciding between bars, pictorial bars, polar bars, lines, pies, rose pies, scatters, heatmaps, calendars, theme rivers, waterfalls, funnels, gauges, treemaps, sunbursts, candlesticks, boxplots, sankeys, graphs, trees, parallels, and radar charts.
- Use `references/option-patterns.md` for JSON-safe option patterns such as data zoom, stacked series, donut layout, and mark lines.
- Prefer JSON-safe config over formatter functions when possible. If function-based formatting is unavoidable, treat `chart.option.json` as the base and edit `chart.html` intentionally afterward.

## OpenClaw And ClawHub Norms

- Write artifacts inside the current workspace, not into home-directory scratch paths.
- Keep examples, templates, and published artifacts generic. Sanitize client data before sharing anything on ClawHub.
- Do not hide key logic in chat-only prose. Save the option, page, and normalized data as files.
- Keep the skill reusable: data samples should be fake or clearly synthetic, and commands should use `{baseDir}` instead of machine-specific paths.

## References

- Read `references/chart-selection.md` for chart choice and data-shape guidance.
- Read `references/option-patterns.md` for advanced JSON-safe option patterns and cleanup rules.
