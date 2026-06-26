# Data Charts Visualization
A lightweight charting skill built on ECharts that outputs static images directly. Browser-independent and designed for fast, reliable agent workflows without a browser stack, it supports a rich set of chart types—including line, bar, pie, donut, rose, gauge, area, dual-axis, scatter, bubble, radar, 
and funnel—while providing flexible configuration, abundant styling options, and [a dedicated styling configuration page](https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html)

## Install

Install this skill from GitHub with the Skills CLI:

```bash
npx skills add ykforerlang/awesome-skills --skill data-charts-visualization
```

or

```bash
npx skills add ykforerlang/awesome-skills --skill data-charts-visualization  -g --copy -y
```

For OpenClaw users, install directly into the OpenClaw global skills directory:

```bash
npx clawhub@latest install data-charts-visualization
```

After the skill files are present, install the local chart runtime in the skill directory:

```bash
npm install
```

If the current working directory is the repository root, the equivalent command is:

```bash
cd skills/data-charts-visualization && npm install
```

## Quick start 

1. Ask your agent to generate or refine a chart.
2. Fine-tune the chart style in natural language first, such as palette, layout, typography, legend position, or overall visual tone.
3. For more precise visual tuning, open the config page:
   `https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html`
4. After adjusting the style in the config page, copy the generated config and paste it back into the current chat.

## Why This Skill

- **Rich chart support**: line, bar, pie, donut, rose, gauge, area, dual-axis, scatter, bubble, radar, and funnel.
- **Lightweight runtime**: render static images without Chromium, Playwright, or browser automation.
- **Convenient styling configuration**: Convenient style fine-tuning and configuration, plus a dedicated [configuration page](https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html).
- **Agent-friendly contract**: keep business data in `data`, reusable style rules in `config`, and one-off render choices in `variant`.

## Showcase

<table>
  <tr>
    <td align="center" width="33%">
      <strong>Line</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/line-series-2.png" alt="Two-series line chart" width="260"/>
    </td>
    <td align="center" width="33%">
      <strong>Bar</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/bar-series-2.png" alt="Two-series bar chart" width="260"/>
    </td>
    <td align="center" width="33%">
      <strong>Area</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/area-series-2.png" alt="Two-series area chart" width="260"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>Dual-Axis</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/dual-axis-series-2.png" alt="Two-series dual-axis bar-line chart" width="260"/>
    </td>
    <td align="center">
      <strong>Dual-Axis Horizontal Style</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/dual-axis-horizontal-style.png" alt="Two-series horizontal-style dual-axis bar-line chart" width="260"/>
    </td>
    <td align="center">
      <strong>Scatter</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/scatter-series-2.png" alt="Two-series scatter chart" width="260"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>Pie</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/pie-showcase.png" alt="Pie chart" width="260"/>
    </td>
    <td align="center">
      <strong>Donut</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/donut-showcase.png" alt="Donut chart" width="260"/>
    </td>
    <td align="center">
      <strong>Rose</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/rose-showcase.png" alt="Rose chart" width="260"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>Gauge</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/gauge-showcase.png" alt="Gauge chart" width="260"/>
    </td>
    <td align="center">
      <strong>Radar</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/radar-showcase.png" alt="Radar chart" width="260"/>
    </td>
    <td align="center">
      <strong>Funnel</strong><br/>
      <img src="https://raw.githubusercontent.com/ykforerlang/awesome-skills/main/static/data-charts-visualization/funnel-showcase.png" alt="Funnel chart" width="260"/>
    </td>
  </tr>
</table>

## Built For Agents

This skill is aimed at OpenClaw-like agents and other automation flows that need deterministic chart rendering instead of interactive BI sessions.

- One local CLI for all supported chart families after setup: `./node_modules/.bin/areslabs-data-charts` from the skill directory
- Runtime installation is explicit and happens once through the skill-local `package.json`
- Avoid documenting runtime `npx -y @areslabs/data-charts-visualization...` as the default entrypoint
- Static image output by default, ideal for reports, dashboards, tickets, and generated assets
- No browser dependency, which keeps environments simpler and cheaper to run
- A small, explicit contract that makes chart generation easier to reason about than passing arbitrary raw styling blocks

## Configuration Power

This is where the skill separates itself from a thin chart wrapper.

- Persistent chart presets: each chart type owns its default config under `config/<chart>_style.json`
- Temporary style overrides: merge one-off changes and pass them inline with `--config`
- Render variants: use `--variant` for choices such as horizontal bar, stacked bar, donut, rose, or dual-axis series typing
- Structured style schema: the config model is built for chart styling, not as a dump of raw browser-only options
- Visual tuning path: when you want hands-on style exploration, use the config page and then bring the generated config back into the render flow

Config page addresses:
- addresses：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html`


## Best Fit

Use this skill when you want to:

- render production-friendly static charts from agent-generated data
- keep chart syntax close to ECharts without depending on a browser runtime
- standardize report visuals through persistent chart presets
- support both quick default rendering and deep style customization
- cover most business chart requests with one consistent toolchain

## License
MIT-0
