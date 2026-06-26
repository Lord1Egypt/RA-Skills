---
name: chart-renderer-open
version: 1.0.0
description: Render structured data into polished, self-contained HTML pages with heatmaps, trend lines, category cards, styled tables, and more. Screenshot/download ready. Suitable for any data visualization scenario — reports, dashboards, comparisons, and analyses.
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://github.com/dachunggan/chart-renderer-open
trigger_keywords:
  - chart
  - render chart
  - visualize
  - visualization
  - generate report
  - render table
  - heatmap
  - line chart
  - radar chart
  - export image
  - export report
  - 生成图表
  - 可视化
  - 渲染表格
  - 导出图片
  - 生成报告
---

# Chart Renderer Open

A modular, registry-driven chart generator for AI agents. Produces self-contained HTML pages with styled charts and tables — no backend required.

**Design philosophy:** Only load the CSS/JS/docs for chart types actually used, minimizing token waste. All information is statically readable with no hover dependency.

## Available Chart Types

| type | Name | Description |
|------|------|-------------|
| `heatmap` | Matrix Heatmap Table | Multi-row x multi-column numeric matrix with color-coded cells, change arrows, and trend badges |
| `layered` | Tiered Category Cards | Three-tier color-coded cards (green/blue/red) for categorizing items by performance level |
| `direction` | Recommendation Cards | Dual-column cards with auto-matched icons and color themes |
| `line` | Multi-series Line Chart | Chart.js multi-line chart with optional data labels |
| `dualAxis` | Dual-axis Line Chart | Chart.js dual Y-axis: primary series (area fill) + secondary series (dashed line) |
| `table` | Styled Table | Clean white-background table with auto-coloring for ↑/↓ prefixed cells |
| `text` | Text Block | Colored callout blocks: success (green) / warning (yellow) / danger (red) |

Full data format specs are in `templates/types/{type}.md` — read on demand.

## Execution Steps

### Step 1: Determine required types
Based on the user's request, select the needed chart types from the table above.

### Step 2: Read on demand
1. Read `skills/chart-renderer-open/templates/registry.json` for file mappings
2. Read `skills/chart-renderer-open/templates/chart_page.html` for the page skeleton
3. Read `skills/chart-renderer-open/templates/types/core.css` for shared styles
4. **For each needed type**, read its `.md` file for data format, its `.css` and `.js` for rendering code
   - When multiple types share a file (e.g., `line` and `dualAxis` share `chart.css`/`chart.js`), do not re-read

### Step 3: Assemble data
Build the CFG and SECTIONS data structures per the `.md` format specs.

**Data injection uses JSON.** The skeleton template loads data via `<script type="application/json">` + `JSON.parse`. Both data placeholders must contain valid JSON strings (output of `JSON.stringify()`). This means:
- Double quotes `"` in string values must be escaped as `\"`
- Newlines must be escaped as `\n`
- Do not manually concatenate JS strings — construct JS objects then use `JSON.stringify()` to output

### Step 4: Assemble HTML and replace placeholders

| Placeholder | Fill with |
|-------------|-----------|
| `{{PAGE_TITLE}}` | Page title |
| `<!--__CDN_LIBS__*/` | CDN scripts (include Chart.js + datalabels when line/dualAxis used; always include html2canvas) |
| `/*__CORE_CSS__*/` | core.css content |
| `/*__TYPE_CSS__*/` | Concatenated CSS for needed types |
| `/*__TYPE_JS__*/` | Concatenated JS for needed types |
| `/*__CFG__*/{}/*__END__*/` | JSON string of CFG object |
| `/*__SECTIONS__*/[]/*__END__*/` | JSON string of SECTIONS array |

### Step 5: Write and deliver
1. Write to `docs/{chart_types}_report_{year}_{month}_{day}_{hour}_{minute}_{second}.html` (no zero-padding)
2. Write to canvas hosted directory `/home/admin/.openclaw/canvas/documents/report_{id}/index.html`
3. Include `[embed ref="report_{id}" title="Report Preview" height="600" /]` in reply for inline preview

## Adding New Chart Types
1. Create `{typeName}.css`, `{typeName}.js`, `{typeName}.md` under `types/`
2. In the JS file, call `registerRenderer('typeName', renderFn)` or `registerRenderer('typeName', renderFn, afterRenderFn)`
3. Add a mapping entry in `registry.json`
4. Add a row to the "Available Chart Types" table in this file

## Notes
- Do not fabricate data the user has not provided
- Heatmap: requires at least 2 rows + 2 columns
- Line charts: require at least 2 data points
- Color scale: <30% dark red / 30-45% light red / 45-55% yellow / 55-70% light green / >=70% dark green
