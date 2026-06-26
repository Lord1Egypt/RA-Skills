# HTML Visualization Page Template

Generate standalone HTML file (Chart.js CDN) with KPI cards + charts + analysis insights.

## Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{report title}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  body { font-family: -apple-system, sans-serif; max-width: 960px; margin: 0 auto; padding: 40px 24px; background: #f8fafc; }
  .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 32px; }
  .kpi-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }
  .kpi-card .value { font-size: 28px; font-weight: 700; margin-top: 4px; }
  .kpi-card .label { font-size: 13px; color: #64748b; }
  .chart-box { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; margin-bottom: 24px; }
  .chart-box canvas { max-height: 340px; }
  .chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .insights { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }
  .insights li { margin-bottom: 10px; line-height: 1.6; }
  @media (max-width: 640px) { .chart-row { grid-template-columns: 1fr; } }
</style>
</head>
<body>
  <h1>📊 {report title}</h1>
  <p class="subtitle">{time range} | Mock Data</p>
  <div class="kpi-grid">
    <div class="kpi-card"><div class="label">Total Orders</div><div class="value">{value}</div></div>
    <div class="kpi-card"><div class="label">Total Revenue</div><div class="value">{value}</div></div>
    <div class="kpi-card"><div class="label">Daily Avg</div><div class="value">{value}</div></div>
    <div class="kpi-card"><div class="label">YoY Growth</div><div class="value">{value}</div></div>
  </div>
  <div class="chart-box"><h3>📈 Trend</h3><canvas id="trendChart"></canvas></div>
  <div class="chart-row">
    <div class="chart-box"><h3>Category Distribution</h3><canvas id="pieChart"></canvas></div>
    <div class="chart-box"><h3>Region Comparison</h3><canvas id="barChart"></canvas></div>
  </div>
  <div class="insights"><h3>📋 Insights</h3><ul>{insights}</ul></div>
  <script>
  new Chart(document.getElementById('trendChart'), { type: 'line', data: { labels: [...], datasets: [{ data: [...] }] }, options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' } } } } });
  new Chart(document.getElementById('pieChart'), { type: 'doughnut', data: { labels: [...], datasets: [{ data: [...] }] }, options: { responsive: true, plugins: { legend: { position: 'bottom' } } } });
  new Chart(document.getElementById('barChart'), { type: 'bar', data: { labels: [...], datasets: [{ data: [...] }] }, options: { responsive: true, plugins: { legend: { display: false } } } });
  </script>
</body>
</html>
```

## Chart Type Reference

| Type | Chart.js type | Use Case |
|------|---------------|----------|
| Line | `line` | Trends, time series |
| Bar | `bar` | Category comparison, ranking |
| Pie | `doughnut` / `pie` | Distribution |
| Scatter | `scatter` | Correlation |
| Radar | `radar` | Multi-dimensional comparison |

## Notes

- File written to `{domain}_chart.html`, report path only in chat
- Primary color indigo (#6366f1), accent colors amber/emerald/rose/slate
- Mobile chart-row collapses to single column