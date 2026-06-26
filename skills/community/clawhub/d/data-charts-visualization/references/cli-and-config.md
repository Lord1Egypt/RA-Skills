# CLI And Config Contract

Read this file before calling the local `areslabs-data-charts` runtime.

## Audience

This document is written for OpenClaw-like agents.
It explains the public contract of the published `@areslabs/data-charts-visualization` CLI as installed into this skill directory.

## One Command To Use

Prefer:

```bash
{baseDir}/node_modules/.bin/areslabs-data-charts \
  --chart-type <chartType> \
  --config-file {baseDir}/config/<chart>_style.json \
  --data '<json>' \
  --out <output.png>
```

Run that command from the skill directory `{baseDir}`, or use the absolute `{baseDir}` paths directly.

Before first use, or whenever the local CLI may not be initialized yet, verify that `{baseDir}/node_modules/.bin/areslabs-data-charts` exists.
If it does not exist, initialize the local runtime with:

```bash
cd {baseDir} && npm install
```

This is the default entrypoint because it installs dependencies once and then executes the local CLI without a runtime network fetch.

CLI shape:

```bash
{baseDir}/node_modules/.bin/areslabs-data-charts --chart-type <type> (--data <json> | --data-file <file>) (--config <json> | --config-file <file>) [--variant <json>] [--width <px>] [--height <px>] [--out <dir|file>]
```

## Supported Top-Level Flags

- `--chart-type`: one of `line`, `bar`, `pie`, `gauge`, `area`, `dualAxis`, `scatter`, `radar`, `funnel`
- `--data`: inline JSON for raw chart data
- `--data-file`: JSON file for raw chart data
- `--config`: inline JSON for a complete chart config object
- `--config-file`: JSON file for a complete chart config object
- `--variant`: inline JSON for one-off render strategy
- `--width`: width in pixels, default `650`
- `--height`: height in pixels, default `360`
- `--out`: output file path or output directory

Rules:

- exactly one of `--data` or `--data-file`
- exactly one of `--config` or `--config-file`
- `--variant` must be an inline JSON object
- `config` must contain both `common` and `specific`
- if `config.chartType` exists, it must match `--chart-type`

Recommended priority:

- prefer `--config-file` for the base chart config
- prefer inline `--data`
- use `--data-file` only when the user already provided a data-file path or the payload is more practical as a file
- prefer inline `--variant`

## Data Payload

`data` is close to ECharts raw data structure.
It may include:

- `series`
- `xAxis`
- `yAxis`
- `dataset`
- `radar`
- chart-specific raw option fragments needed for the data layer
- `title.text` and `title.subtext` when title copy belongs to the input data

Typical usage:

- `line`, `bar`, `area`: `xAxis.data` plus `series[].data`
- `scatter`: numeric `xAxis` and `yAxis`, plus `series[].data` as point arrays
- `pie`: `series[0].data` with `{ name, value }`
- `gauge`: `series[0].data` with one KPI item
- `dualAxis`: shared `xAxis`, two `yAxis`, series with `yAxisIndex`; series typing comes from `variant` or defaults to left `bar` plus right `line`
- `radar`: `radar.indicator` plus `series[].data[].value`
- `funnel`: `series[0].data` in stage order

Use `dataset.source` plus `series.encode` when the user gives table-like data and shared tabular mapping is the cleanest fit.

## Config Payload

`config` is the chart config schema, not a raw ECharts option patch.

Base shape:

```json
{
  "chartType": "line",
  "common": {},
  "specific": {}
}
```

### `common`

`common` is shared across chart types and supports:

- `title.main.show`
- `title.main.align`
- `title.main.fontSize`
- `title.main.color`
- `title.main.bold`
- `title.subtitle.show`
- `title.subtitle.fontSize`
- `title.subtitle.color`
- `canvas.backgroundColor`
- `canvas.palette`
- `canvas.plotArea.left`
- `canvas.plotArea.right`
- `canvas.plotArea.top`
- `canvas.plotArea.bottom`
- `legend.show`
- `legend.position`
- `legend.orient`
- `legend.fontSize`
- `legend.color`
- `axes.x.lineShow`
- `axes.x.tickShow`
- `axes.x.rotate`
- `axes.x.labelFontSize`
- `axes.x.labelColor`
- `axes.x.lineColor`
- `axes.x.formatter`
- `axes.y.lineShow`
- `axes.y.tickShow`
- `axes.y.scale`
- `axes.y.labelFontSize`
- `axes.y.labelColor`
- `axes.y.lineColor`
- `axes.y.formatter`
- `splitLines.horizontal.show`
- `splitLines.horizontal.color`
- `splitLines.horizontal.type`
- `splitLines.horizontal.width`
- `splitLines.vertical.show`
- `splitLines.vertical.color`
- `splitLines.vertical.type`
- `splitLines.vertical.width`

`gauge`, `radar`, `funnel`, and `pie` may ignore some cartesian-only fields such as axes or split lines.

### `specific` By Chart Type

`line`:

- `specific.line.smooth`
- `specific.line.showSymbol`
- `specific.line.connectNulls`
- `specific.line.symbol`
- `specific.line.symbolSize`
- `specific.line.lineStyleType`
- `specific.line.lineWidth`
- `specific.dataLabels.show`
- `specific.dataLabels.fontSize`
- `specific.dataLabels.color`

`bar`:

- `specific.bar.barGap`
- `specific.bar.itemOpacity`
- `specific.bar.borderRadius`
- `specific.bar.borderWidth`
- `specific.bar.borderColor`
- `specific.dataLabels.show`
- `specific.dataLabels.position`
- `specific.dataLabels.fontSize`
- `specific.dataLabels.color`

`area`:

- `specific.area.smooth`
- `specific.area.showSymbol`
- `specific.area.symbol`
- `specific.area.symbolSize`
- `specific.area.connectNulls`
- `specific.area.areaOpacity`
- `specific.area.areaFillMode`
- `specific.area.lineStyleType`
- `specific.area.lineWidth`
- `specific.dataLabels.show`
- `specific.dataLabels.fontSize`
- `specific.dataLabels.color`

`scatter`:

- `specific.point.symbol`
- `specific.point.symbolSize`
- `specific.point.itemOpacity`
- `specific.point.borderWidth`
- `specific.point.borderColor`
- `specific.dataLabels.show`
- `specific.dataLabels.fontSize`
- `specific.dataLabels.color`

`pie`:

- `specific.labelPosition`
- `specific.startAngle`
- `specific.showLabel`
- `specific.labelFontSize`
- `specific.labelColor`
- `specific.labelFormatter`
- `specific.labelLineShow`
- `specific.labelLineColor`
- `specific.labelLineWidth`
- `specific.itemOpacity`
- `specific.borderWidth`
- `specific.borderColor`

`dualAxis`:

- `common.splitLines.horizontal.display`
- `specific.leftAxis.labelFontSize`
- `specific.leftAxis.labelColor`
- `specific.leftAxis.lineShow`
- `specific.leftAxis.lineColor`
- `specific.leftAxis.tickShow`
- `specific.leftAxis.scale`
- `specific.leftAxis.formatter`
- `specific.rightAxis.labelFontSize`
- `specific.rightAxis.labelColor`
- `specific.rightAxis.lineShow`
- `specific.rightAxis.lineColor`
- `specific.rightAxis.tickShow`
- `specific.rightAxis.scale`
- `specific.rightAxis.formatter`
- `specific.leftBar.showLabel`
- `specific.leftBar.labelPosition`
- `specific.leftBar.labelFontSize`
- `specific.leftBar.labelColor`
- `specific.leftBar.opacity`
- `specific.leftBar.barGap`
- `specific.leftBar.borderRadius`
- `specific.leftBar.borderWidth`
- `specific.leftBar.borderColor`
- `specific.leftBar.colors`
- `specific.rightBar.showLabel`
- `specific.rightBar.labelPosition`
- `specific.rightBar.labelFontSize`
- `specific.rightBar.labelColor`
- `specific.rightBar.opacity`
- `specific.rightBar.barGap`
- `specific.rightBar.borderRadius`
- `specific.rightBar.borderWidth`
- `specific.rightBar.borderColor`
- `specific.rightBar.colors`
- `specific.leftLine.smooth`
- `specific.leftLine.area`
- `specific.leftLine.showSymbol`
- `specific.leftLine.connectNulls`
- `specific.leftLine.showLabel`
- `specific.leftLine.colors`
- `specific.leftLine.lineStyleType`
- `specific.leftLine.lineWidth`
- `specific.leftLine.symbol`
- `specific.leftLine.symbolSize`
- `specific.leftLine.labelFontSize`
- `specific.leftLine.labelColor`
- `specific.rightLine.smooth`
- `specific.rightLine.area`
- `specific.rightLine.showSymbol`
- `specific.rightLine.connectNulls`
- `specific.rightLine.showLabel`
- `specific.rightLine.colors`
- `specific.rightLine.lineStyleType`
- `specific.rightLine.lineWidth`
- `specific.rightLine.symbol`
- `specific.rightLine.symbolSize`
- `specific.rightLine.labelFontSize`
- `specific.rightLine.labelColor`

For `dualAxis`, persistent `common.splitLines.horizontal.display` controls whether horizontal split lines render on the left axis or right axis. Set `common.splitLines.horizontal.show` to `false` to hide them. Left and right series typing is a render-time `variant` decision. Horizontal vs vertical dual-axis layout is also a render-time `variant.layout` decision.

`gauge`:

- `specific.startAngle`
- `specific.endAngle`
- `specific.progressShow`
- `specific.progressWidth`
- `specific.progressColor`
- `specific.axisWidth`
- `specific.bandStops`
- `specific.titleShow`
- `specific.titleFontSize`
- `specific.titleColor`
- `specific.detailShow`
- `specific.detailFormatter`
- `specific.detailFontSize`
- `specific.detailColor`
- `specific.axisLabelShow`
- `specific.axisLabelDistance`
- `specific.axisLabelFontSize`
- `specific.axisLabelColor`
- `specific.splitLineShow`
- `specific.splitLineLength`
- `specific.splitLineWidth`
- `specific.splitLineColor`
- `specific.axisTickShow`
- `specific.axisTickLength`
- `specific.axisTickWidth`
- `specific.axisTickColor`
- `specific.pointerShow`
- `specific.pointerWidth`
- `specific.pointerColor`
- `specific.anchorShow`
- `specific.anchorSize`
- `specific.anchorColor`

`radar`:

- `specific.shape`
- `specific.splitNumber`
- `specific.showSymbol`
- `specific.showLabel`
- `specific.labelFormatter`
- `specific.areaOpacity`
- `specific.splitLineColor`
- `specific.splitLineWidth`
- `specific.splitLineType`
- `specific.axisLineColor`
- `specific.axisLineWidth`
- `specific.axisLineType`
- `specific.axisNameFontSize`
- `specific.axisNameColor`
- `specific.axisNameBold`
- `specific.symbol`
- `specific.symbolSize`
- `specific.lineStyleType`
- `specific.lineWidth`
- `specific.labelFontSize`
- `specific.labelColor`

`funnel`:

- `specific.sort`
- `specific.gap`
- `specific.minSize`
- `specific.maxSize`
- `specific.itemOpacity`
- `specific.labelPosition`
- `specific.showLabel`
- `specific.labelFormatter`
- `specific.labelFontSize`
- `specific.labelColor`

## Style Override Workflow

When the user explicitly requests styles such as:

- “make the title dark blue”
- “increase the font size”
- “move the legend to the top right”
- “change label color to light gray”
- “set the background to white”

do not directly edit the persistent files under `{baseDir}/config/*.json` by default.

The correct workflow is:

1. read the persistent chart config file for the chosen chart type, such as `config/bar_style.json`
2. merge the user’s temporary style overrides into that config in memory
3. pass the merged full config to the CLI via `--config`
4. leave the persistent config file unchanged

That means:

- the persistent chart config is the base config
- the user’s style request is a temporary override
- the CLI must still receive one complete chart config object, not a loose patch

Only edit the persistent chart config file when the user explicitly asks for persistence, for example:

- “make this the default”
- “save this style”
- “update the default config”
- “persist this config”

If the user starts asking for many style changes, clearly enters iterative visual tuning, or keeps re-rendering the same underlying data with different presentation goals, guide them to the config page:

中文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.zh.html`
英文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html`

## Merge Rules

When merging styles:

- override only the fields the user actually mentioned
- leave all other fields inherited from the persistent chart config
- do not write temporary overrides back into the persistent chart config file unless the user explicitly asked for that
- if the user describes styles in raw ECharts terms, first map them back into chart config fields, then merge

Examples:

- if the user says “make the title red”, override only `common.title.main.color`
- if the user says “move the legend to top-right and make labels gray”, override only the corresponding legend position and chart-specific label color fields
- if the user says “blue title, font size 20, white background”, override only those fields and keep everything else from the base config

## Variant Contract

`variant` is intentionally small and agent-controlled.
Current supported keys are:

- `layout`: `"horizontal"` or `"vertical"` for bar layout, and for one-off dual-axis orientation
- `stack`: `true` or `false` for stacked bar mode
- `pieMode`: pie-family one-off mode such as donut or rose
- `leftSeriesType`: dual-axis left series type
- `rightSeriesType`: dual-axis right series type

Dual-axis guidance:

- if the user names only “dual-axis”, default to `leftSeriesType=bar` and `rightSeriesType=line`
- use `layout=horizontal` only when the current render needs a horizontal dual-axis layout
- use `leftSeriesType=bar` + `rightSeriesType=line` for volume-plus-rate combinations
- use `leftSeriesType=line` + `rightSeriesType=line` for two trend series with different units
- use `leftSeriesType=line` + `rightSeriesType=bar` only when the line is the primary story and the bar is support
- use `leftSeriesType=bar` + `rightSeriesType=bar` only when both series are truly discrete magnitude comparisons and both need separate axes

Examples:

```bash
--variant '{"layout":"horizontal","stack":true}'
```

```bash
--variant '{"pieMode":"donut"}'
```

```bash
--variant '{"leftSeriesType":"bar","rightSeriesType":"line"}'
```

```bash
--variant '{"layout":"horizontal","leftSeriesType":"bar","rightSeriesType":"line"}'
```

Do not treat `variant` as a generic ECharts patch channel.

## Important Behavioral Rules

- If the user gives raw ECharts `option`, extract or reuse the parts that belong in `data`.
- Do not tell the agent to pass full raw ECharts style blocks into `config`.
- Prefer stable style presets in `config` and ephemeral strategy in `variant`.
- For temporary style requests, merge overrides in memory on top of the persistent chart config before calling the CLI.
- When the user starts asking for more direct visual manipulation, route them toward the config page instead of inventing larger ad hoc JSON by hand.

## Config Source Of Truth

Default presets live under:

- `{baseDir}/config/`

The visual config page is available at:

中文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.zh.html`
英文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html`
ual config page is available at:

中文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.zh.html`
英文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html`
