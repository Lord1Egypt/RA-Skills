# line — Multi-series Line Chart

Chart.js multi-line chart. Each series is a separate colored line.

```javascript
{
  type: "line",
  title: "Trend Analysis",
  data: {
    labels: ["Jan","Feb","Mar","Apr","May","Jun"],
    datasets: [
      { label:"Series A", data:[81,92,81,102,98,88], color:"#1a73e8" },
      { label:"Series B", data:[53,60,51,72,82,90], color:"#ea4335" }
    ],
    showDataLabels: true,   // default true
    yMin: 0, yMax: 120      // optional Y-axis range
  }
}
```

**Field descriptions:**
- `labels` X-axis labels / `datasets[].label` series name / `data` values array / `color` line color (optional, auto-assigned if omitted)
- `showDataLabels` show data point labels / `yMin` / `yMax` Y-axis range

**Rendering:** Bottom legend, optional data labels above points, multiple colored lines.

**Data requirements:** At least 2 data points.
