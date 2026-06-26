# dualAxis — Dual-axis Line Chart

Chart.js dual Y-axis line chart: left axis primary series (area fill), right axis secondary series (dashed line).

```javascript
{
  type: "dualAxis",
  title: "Revenue & Growth Rate Trend",
  data: {
    labels: ["Jan","Feb","Mar","Apr","May","Jun"],
    primary: [410,354,381,354,365,399],
    secondary: [54.7,47.2,50.9,47.3,48.7,53.2],
    yMin: 300, yMax: 450,      // primary axis range
    rMin: 40, rMax: 65          // secondary axis range
  }
}
```

**Field descriptions:**
- `labels` X-axis labels / `primary` primary values array / `secondary` secondary values array
- `yMin`/`yMax` primary axis range / `rMin`/`rMax` secondary axis range (all optional)

**Rendering:** Data points labeled with values, dual Y-axes, primary as area fill + secondary as dashed line.

**Data requirements:** At least 2 data points.

**Note:** Shares `chart.css` / `chart.js` with `line`. Do not re-read if already loaded.
