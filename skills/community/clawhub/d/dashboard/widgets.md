# Dashboard Widgets

## KPI Card

```html
<div class="kpi-card">
  <span class="value">$12,450</span>
  <span class="label">Monthly Revenue</span>
  <span class="delta positive">+12%</span>
</div>
```

## Line Chart

Best for: Trends over time
```json
{
  "type": "line",
  "data": "data.json#revenue",
  "xAxis": "date",
  "yAxis": "amount"
}
```

## Bar Chart

Best for: Comparisons
```json
{
  "type": "bar",
  "data": "data.json#categories",
  "xAxis": "name",
  "yAxis": "value"
}
```

## Status Indicator

```html
<div class="status">
  <span class="dot green"></span>
  <span class="label">API Healthy</span>
  <span class="time">Updated 2m ago</span>
</div>
```

## Table

Best for: Detailed data
```json
{
  "type": "table",
  "data": "data.json#transactions",
  "columns": ["date", "description", "amount"]
}
```

## Widget Sizing

| Size | Width | Use for |
|------|-------|---------|
| Small | 1/4 | KPIs |
| Medium | 1/2 | Charts |
| Large | Full | Tables, maps |
