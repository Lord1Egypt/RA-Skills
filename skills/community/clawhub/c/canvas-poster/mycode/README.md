# canvas-poster

[中文文档](./README.zh-CN.md)

Declarative server-side poster & dashboard image generator powered by [@napi-rs/canvas](https://github.com/nicknisi/napi-rs-canvas). Define your layout with a simple JSON DSL, get a pixel-perfect PNG — no browser, no headless Chrome.

## Install

```bash
npm install canvas-poster
```

## Quick Start

```js
const { buildPoster } = require('canvas-poster');

buildPoster({
  width: 800,
  header: { title: '📊 Monthly Report', subtitle: 'March 2026' },
  sections: [
    {
      type: 'kpi-cards',
      cards: [
        { label: 'Revenue', value: '$1.2M', color: 'green' },
        { label: 'Users', value: '45,200' },
        { label: 'Avg Order', value: '$89' },
        { label: 'Growth', value: '+12.5%', color: 'green' },
      ],
    },
    {
      type: 'bar-chart',
      title: '💼 Breakdown',
      bars: [
        { name: 'Product A', value: 580000 },
        { name: 'Product B', value: 340000 },
        { name: 'Product C', value: 280000 },
      ],
    },
    {
      type: 'tips',
      title: '💡 Insights',
      items: ['Product A grew 23% MoM', 'Consider expanding Product C'],
    },
  ],
  footer: 'Auto-generated report',
  output: './report.png',
});
```

## Section Types

| Type | Description | Fields |
|------|-------------|--------|
| `kpi-cards` | KPI card grid (2-column) | `cards: [{label, value, color?, sub?}]` |
| `bar-chart` | Horizontal bar chart | `bars: [{name, value, color?, pct?}]` |
| `pie-chart` | Pie chart with legend | `slices: [{name, value, pct?}]` |
| `line-chart` | Line chart (multi-series) | `lines: [{name, data: number[], color?}]`, `xLabels?: string[]` |
| `area-chart` | Area chart | `areas: [{name, data: number[], color?}]`, `xLabels?: string[]`, `opacity?: number` |
| `scatter-chart` | Scatter plot | `points: [{x, y, color?}]`, `dotRadius?: number` |
| `table` | Data table | `headers: string[], rows: string[][]` |
| `tips` | Tip/suggestion box | `items: string[]` |
| `divider` | Horizontal divider | No data needed |

All section types also accept a `title` field.

## API

### `buildPoster(config)`

Returns `{ canvas, width, height, buffer?, output? }`.

**Config fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `width` | number | 800 | Canvas width in pixels |
| `height` | number | auto | Canvas height (auto-calculated if omitted) |
| `bg` | string | `'#0f172a'` | Background color |
| `header` | object | — | `{ title, subtitle?, bg?, bgEnd? }` |
| `sections` | array | `[]` | Array of section objects |
| `footer` | string | — | Footer text |
| `output` | string | — | If set, writes PNG to this path |

### `buildDashboard(data, output)`

Pre-built dashboard template (expense/travel reports). See `templates/dashboard.js`.

## As a Claude Code Skill

This package also works as a [Claude Code](https://claude.ai/claude-code) Skill. Place it under `skills/canvas-poster` and Claude will use it when you ask to "generate a poster", "create a dashboard", or "make an infographic".

See [SKILL.md](./SKILL.md) for Skill-specific documentation.

## Font Support

CJK fonts are auto-detected on Windows (Microsoft YaHei), macOS (PingFang), and Linux (WenQuanYi Zen Hei). You can also place a `.ttc`/`.ttf` file in `lib/fonts/` as a fallback.

## License

[MIT](./LICENSE)
