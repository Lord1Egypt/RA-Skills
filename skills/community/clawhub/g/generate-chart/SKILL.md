---
name: generate-chart
description: "Generate a chart image using Chart.js. Supports line, bar, pie, doughnut, radar, polarArea, bubble, and scatter chart types."
---

# Generate Chart

## What It Does
Creates a chart image using the Chart.js library. Supports bar, line, pie, doughnut, radar, polarArea, bubble, and scatter chart types with full Chart.js data and options configuration.

## When to Use
- Generate data visualization charts programmatically
- Create chart images for reports, dashboards, or emails
- Produce charts without a browser or frontend

## Required Inputs
- `chart_type` — one of: `line`, `bar`, `pie`, `doughnut`, `radar`, `polarArea`, `bubble`, `scatter`
- `data` — Chart.js data object with `labels` and `datasets`

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Dashboard Reports** — Generate chart images for PDF/email reports without a browser
- **Sales Analytics** — Create bar/line charts showing revenue, growth, or conversion trends
- **Survey Results** — Visualize poll or survey data as pie/doughnut charts
- **Financial Reports** — Produce stock performance or budget allocation charts
- **Project Metrics** — Generate sprint velocity, burn-down, or team performance charts
- **Newsletter Content** — Embed data visualizations directly in email newsletters
- **Slack/Discord Bots** — Generate chart images on-the-fly for chatbot responses

## Key Options
| Parameter | Description |
|-----------|-------------|
| `chart_type` | Type of chart (bar, line, pie, etc.) |
| `data` | Chart.js data config (labels + datasets) |
| `options` | Chart.js options (title, legend, scales) |
| `width` / `height` | Chart dimensions in pixels |
| `output_format` | `url` (default), `base64`, `both`, `image` |

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/generateChart \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "chart_type": "bar",
    "data": {
      "labels": ["Q1", "Q2", "Q3", "Q4"],
      "datasets": [{
        "label": "Revenue",
        "data": [120000, 150000, 180000, 200000],
        "backgroundColor": "rgba(54, 162, 235, 0.6)"
      }]
    },
    "options": { "plugins": { "title": { "display": true, "text": "Quarterly Revenue" } } },
    "width": 800,
    "height": 500,
    "output_format": "url"
  }'
```
