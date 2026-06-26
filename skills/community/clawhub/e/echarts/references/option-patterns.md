# Option Patterns

These patterns stay JSON-safe so they can live inside `chart.option.json` without requiring function serialization.

## Baseline Checklist

- Keep `backgroundColor` transparent unless the export itself needs a fixed fill.
- Add `aria.enabled: true`.
- Add `tooltip`.
- Keep color palettes explicit for predictable rerenders.
- Save the final option separately from the page wrapper.

## Stacked Category Comparison

```json
{
  "tooltip": { "trigger": "axis" },
  "legend": { "top": 60 },
  "series": [
    { "name": "North", "type": "bar", "stack": "total", "data": [12, 19, 15] },
    { "name": "South", "type": "bar", "stack": "total", "data": [9, 14, 11] }
  ]
}
```

## Area Trend

```json
{
  "series": [
    {
      "name": "Revenue",
      "type": "line",
      "smooth": true,
      "areaStyle": { "opacity": 0.18 },
      "data": [120, 160, 210, 260]
    }
  ]
}
```

## Donut Breakdown

```json
{
  "legend": { "bottom": 0, "type": "scroll" },
  "series": [
    {
      "type": "pie",
      "radius": ["42%", "70%"],
      "center": ["50%", "42%"],
      "label": { "formatter": "{b}: {d}%" }
    }
  ]
}
```

## Rose Pie Breakdown

```json
{
  "legend": { "bottom": 0, "type": "scroll" },
  "series": [
    {
      "type": "pie",
      "roseType": "area",
      "radius": ["18%", "78%"],
      "center": ["50%", "44%"],
      "label": { "formatter": "{b}: {c}" }
    }
  ]
}
```

## Large Category Lists

```json
{
  "dataZoom": [
    { "type": "inside", "xAxisIndex": 0, "start": 0, "end": 40 },
    { "type": "slider", "xAxisIndex": 0, "start": 0, "end": 40, "height": 16 }
  ]
}
```

Use the `yAxisIndex` form when the chart is a horizontal bar chart.

## Target Or Benchmark Line

```json
{
  "series": [
    {
      "type": "line",
      "markLine": {
        "symbol": "none",
        "data": [{ "yAxis": 80, "name": "Target" }]
      }
    }
  ]
}
```

## Notes On Functions

- Prefer string formatters like `"{value}%"` before reaching for JavaScript formatter functions.
- If you truly need formatter functions, keep `chart.option.json` as the JSON baseline and make the function-aware edit in `chart.html` afterward.
- Lint the JSON baseline first so the structural issues are resolved before adding custom JavaScript.

## Heatmap With Visual Scale

```json
{
  "visualMap": {
    "min": 0,
    "max": 100,
    "calculable": true,
    "orient": "horizontal",
    "left": "center",
    "bottom": 18
  },
  "series": [
    {
      "type": "heatmap",
      "data": [
        [0, 0, 12],
        [1, 0, 18],
        [0, 1, 7],
        [1, 1, 21]
      ]
    }
  ]
}
```

## Funnel Drop Off

```json
{
  "series": [
    {
      "type": "funnel",
      "sort": "desc",
      "gap": 4,
      "data": [
        { "name": "Visited", "value": 1200 },
        { "name": "Signed Up", "value": 420 },
        { "name": "Purchased", "value": 95 }
      ]
    }
  ]
}
```

## Waterfall Deltas

```json
{
  "xAxis": { "type": "category", "data": ["New", "Refund", "Expansion", "Churn"] },
  "series": [
    {
      "type": "bar",
      "stack": "total",
      "silent": true,
      "itemStyle": { "color": "transparent", "borderColor": "transparent" },
      "data": [0, 120, 90, 135]
    },
    {
      "type": "bar",
      "stack": "total",
      "data": [120, 30, 45, 10]
    }
  ]
}
```

## KPI Gauge

```json
{
  "series": [
    {
      "type": "gauge",
      "min": 0,
      "max": 100,
      "progress": { "show": true, "width": 14 },
      "data": [{ "value": 72, "name": "Availability" }]
    }
  ]
}
```

## Treemap Hierarchy

```json
{
  "series": [
    {
      "type": "treemap",
      "breadcrumb": { "show": true },
      "data": [
        {
          "name": "Infrastructure",
          "children": [
            { "name": "API", "value": 42 },
            { "name": "Workers", "value": 18 }
          ]
        }
      ]
    }
  ]
}
```

## Candlestick OHLC

```json
{
  "series": [
    {
      "type": "candlestick",
      "data": [
        [12, 15, 11, 16],
        [15, 14, 13, 17],
        [14, 18, 13, 19]
      ]
    }
  ]
}
```

## Boxplot Distribution

```json
{
  "series": [
    {
      "type": "boxplot",
      "data": [
        [5, 9, 12, 16, 22],
        [7, 10, 13, 19, 25]
      ]
    }
  ]
}
```

## Sankey Flow

```json
{
  "series": [
    {
      "type": "sankey",
      "data": [{ "name": "Ads" }, { "name": "Signup" }, { "name": "Paid" }],
      "links": [
        { "source": "Ads", "target": "Signup", "value": 320 },
        { "source": "Signup", "target": "Paid", "value": 88 }
      ]
    }
  ]
}
```

## Sunburst Hierarchy

```json
{
  "series": [
    {
      "type": "sunburst",
      "data": [
        {
          "name": "Infrastructure",
          "children": [
            { "name": "API", "value": 42 },
            { "name": "Workers", "value": 18 }
          ]
        }
      ]
    }
  ]
}
```

## Tree Hierarchy

```json
{
  "series": [
    {
      "type": "tree",
      "data": [
        {
          "name": "Platform",
          "children": [
            { "name": "Web", "value": 24 },
            { "name": "Gateway", "value": 18 }
          ]
        }
      ]
    }
  ]
}
```

## Graph Network

```json
{
  "series": [
    {
      "type": "graph",
      "layout": "force",
      "data": [
        { "name": "Product", "symbolSize": 30, "category": 0 },
        { "name": "Frontend", "symbolSize": 26, "category": 1 },
        { "name": "Backend", "symbolSize": 28, "category": 1 }
      ],
      "links": [
        { "source": "Product", "target": "Frontend", "value": 12 },
        { "source": "Frontend", "target": "Backend", "value": 10 }
      ]
    }
  ]
}
```

## Parallel Coordinates

```json
{
  "parallelAxis": [
    { "dim": 0, "name": "Latency" },
    { "dim": 1, "name": "Reliability" },
    { "dim": 2, "name": "Cost" },
    { "dim": 3, "name": "Usability" }
  ],
  "series": [
    {
      "type": "parallel",
      "data": [
        { "name": "Option A", "value": [88, 93, 52, 74] },
        { "name": "Option B", "value": [72, 85, 66, 91] }
      ]
    }
  ]
}
```

## Calendar Heatmap

```json
{
  "calendar": { "range": ["2026-03-01", "2026-03-31"] },
  "visualMap": { "min": 0, "max": 30, "calculable": true },
  "series": [
    {
      "type": "heatmap",
      "coordinateSystem": "calendar",
      "data": [
        ["2026-03-01", 12],
        ["2026-03-02", 18],
        ["2026-03-03", 9]
      ]
    }
  ]
}
```

## ThemeRiver Flow

```json
{
  "singleAxis": { "type": "time" },
  "series": [
    {
      "type": "themeRiver",
      "data": [
        ["2026-03-01", 120, "Ads"],
        ["2026-03-01", 90, "Organic"],
        ["2026-03-02", 140, "Ads"]
      ]
    }
  ]
}
```

## Pictorial Bar Ranking

```json
{
  "series": [
    {
      "type": "pictorialBar",
      "symbol": "roundRect",
      "symbolRepeat": "fixed",
      "symbolClip": true,
      "data": [24, 18, 15, 11]
    }
  ]
}
```

## Polar Bar Ranking

```json
{
  "polar": { "radius": "72%" },
  "angleAxis": { "type": "category", "data": ["North", "South", "East", "West"] },
  "radiusAxis": { "type": "value" },
  "series": [
    {
      "type": "bar",
      "coordinateSystem": "polar",
      "roundCap": true,
      "data": [120, 98, 140, 110]
    }
  ]
}
```
