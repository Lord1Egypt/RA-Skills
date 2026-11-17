<!-- Copyright (c) 2026 Yang Pengfei / Forklift Veteran. MIT License; see LICENSE.md. -->
# Static SVG Charts

Provide SVG and a copyable numeric table for comparisons, rankings, shares and trends. Use ASCII only on request or where SVG cannot render. Limit the main report to three charts; place additional detail in an appendix.

## Accessibility and appearance
Use standalone SVG with `viewBox`, responsive width, system fonts and no external dependencies. Include unique title and description IDs, `role="img"` and `aria-labelledby`. Show units, geography, period, exact labels and sources. Normal text needs contrast of at least 4.5:1; use dark labels outside orange bars. Do not rely on colour alone.

Suggested palette: navy #1a2a4a, orange #ff6b35, green #2e7d32, blue #1565c0, background #f5f7fa.

| Chart | Geometry and rules |
|---|---|
| Horizontal bars | width = plotWidth * value / maximumValue; zero baseline |
| Grouped bars | Common scale and baseline; identify categories and series |
| Line | Map actual time to x and value to y; disclose axis limits |
| Donut | C = 2*pi*r; segment = C*share; start angle = cumulativeShare*360-90 |

Handle all-zero series without dividing by zero. Use signed bars for negative values. Donuts require a complete meaningful total; do not normalize incomplete shares silently. Label logarithmic scales, axis breaks, estimates and forecasts.

## Example
All values below are fictional teaching data, not market statistics.

| Category | Example units |
|---|---:|
| A | 80 |
| B | 50 |

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 230" width="100%" role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Fictional comparison</title>
  <desc id="chart-desc">Teaching data only: A has 80 units and B has 50. Bars start at zero.</desc>
  <rect width="640" height="230" fill="#f5f7fa"/>
  <g font-family="Arial, sans-serif" fill="#1a2a4a" font-size="16">
    <text x="24" y="30">Fictional example (units)</text>
    <text x="24" y="82">A</text><text x="24" y="132">B</text>
    <rect x="70" y="60" width="400" height="30" fill="#1565c0"/>
    <rect x="70" y="110" width="250" height="30" fill="#ff6b35"/>
    <text x="480" y="82">80</text><text x="330" y="132">50</text>
    <text x="70" y="165">0</text><text x="450" y="165">80</text>
    <text x="24" y="205" font-size="13">Source: fictional teaching data; no market claim.</text>
  </g>
</svg>
```

Check arithmetic against the source table, chronology, legends, clipping and narrow-screen readability. Never invent URLs or fill missing observations to improve appearance.
