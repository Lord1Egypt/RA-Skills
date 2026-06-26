# Chart Config

This directory stores helper-schema config presets for each chart type.

These files are not raw ECharts style fragments. They are helper-facing configs consumed by the shared helper option builder, which then produces the final ECharts option used by both helper preview and CLI rendering.
They should be treated as complete helper config payloads for CLI rendering, not as partial patches.
Title copy does not live here. Put chart title text in the data payload, for example `data.title.text` and `data.title.subtext`.

One-off render choices such as bar layout, stack mode, pie mode, or dual-axis type selection should not be stored here. Pass those through CLI `--variant` instead.
Long-lived axis behavior such as `common.axes.y.scale` belongs in config.

## Files

- `line_style.json`
- `bar_style.json`
- `pie_style.json`
- `gauge_style.json`
- `area_style.json`
- `dual_axis_style.json`
- `scatter_style.json`
- `radar_style.json`
- `funnel_style.json`

## Usage

```bash
./node_modules/.bin/areslabs-data-charts \
  --chart-type line \
  --config-file ./config/line_style.json \
  --data-file /tmp/line_basic_single_series.json \
  --out ../../skills-scripts/data-charts-visualization/test/manual
```

Run that command in the skill directory.
If the current working directory is the repository root, the equivalent command is:

```bash
cd skills/data-charts-visualization && ./node_modules/.bin/areslabs-data-charts \
  --chart-type line \
  --config-file ./config/line_style.json \
  --data-file /tmp/line_basic_single_series.json \
  --out ../../skills-scripts/data-charts-visualization/test/manual
```

Default demo data should come from:

- `skills-helpler/data-charts-visualization/shared/charts-default-data.js`

Default config files can be regenerated with:

```bash
node skills-helpler/data-charts-visualization/scripts/export_default_configs.js
```
