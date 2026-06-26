# Chart Splat API Reference

## Endpoint

```
POST https://api.chartsplat.com/chart
```

## Authentication

Include your API key using one of these headers:

```
X-Api-Key: YOUR_API_KEY
Authorization: Bearer YOUR_API_KEY
```

API keys start with `cs_` and are managed at [chartsplat.com/dashboard/api-keys](https://chartsplat.com/dashboard/api-keys).

## Request Body

```json
{
  "type": "bar",
  "data": {
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [
      {
        "label": "Revenue",
        "data": [12, 19, 3],
        "backgroundColor": "#8b5cf6",
        "borderColor": "#6366f1",
        "borderWidth": 1,
        "fill": false
      }
    ]
  },
  "options": {
    "width": 800,
    "height": 600,
    "plugins": {
      "title": { "display": true, "text": "Monthly Revenue" }
    },
    "scales": {
      "y": { "beginAtZero": true }
    }
  }
}
```

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `type` | string | No | `line` | Chart type: `line`, `bar`, `pie`, `doughnut`, `radar`, `polarArea`, `candlestick`, `ohlc` |
| `data.labels` | string[] | Yes* | - | Labels for X-axis or chart segments (*optional for candlestick/ohlc) |
| `data.datasets` | object[] | Yes | - | Array of datasets (see below) |
| `options.width` | integer | No | 800 | Image width in pixels (100-4000) |
| `options.height` | integer | No | 600 | Image height in pixels (100-4000) |
| `options.plugins` | object | No | - | Chart.js plugin configuration |
| `options.scales` | object | No | - | Chart.js scale configuration |

### Dataset Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `data` | number[] or OhlcDataPoint[] | Yes | Numeric data points, or OHLC objects for candlestick/ohlc charts |
| `label` | string | No | Dataset label shown in legend |
| `backgroundColor` | string or string[] | No | Fill color(s) in hex or rgba |
| `borderColor` | string or string[] | No | Border/line color(s) |
| `borderWidth` | number | No | Border width in pixels |
| `fill` | boolean | No | Fill area under line charts |

### OHLC Data Point (for candlestick/ohlc charts)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `x` | number or string | Yes | Timestamp (ms) or date string (e.g., `"2025-02-25"`) |
| `o` | number | Yes | Open price |
| `h` | number | Yes | High price |
| `l` | number | Yes | Low price |
| `c` | number | Yes | Close price |

## Response

### Success (200)

```json
{
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "format": "png",
  "width": 800,
  "height": 600
}
```

### Rate Limit Headers

All responses include:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Monthly request limit |
| `X-RateLimit-Remaining` | Requests remaining this month |
| `X-RateLimit-Reset` | When the limit resets (ISO 8601) |

### Errors

| Status | Error | Description |
|--------|-------|-------------|
| 400 | `Request body is required` | Empty request |
| 400 | `Invalid JSON in request body` | Malformed JSON |
| 400 | `Invalid chart configuration` | Missing `data.labels` or `data.datasets` (candlestick/ohlc only require `data.datasets`) |
| 401 | `API key required` | No API key provided |
| 401 | `Invalid API key` | Key not found or revoked |
| 429 | `Rate limit exceeded` | Monthly quota reached |
| 500 | `Chart generation failed` | Server-side rendering error |

### Rate Limit Error Response

```json
{
  "error": "Rate limit exceeded",
  "message": "You have used 100 of 100 requests this month.",
  "limit": 100,
  "used": 100,
  "plan": "free"
}
```

## Rate Limits by Plan

| Plan | Requests/Month | API Keys |
|------|----------------|----------|
| Free | 100 | 1 |
| Pro | 10,000 | 5 |
| Enterprise | Unlimited | Unlimited |

## Multi-Dataset Example

```json
{
  "type": "bar",
  "data": {
    "labels": ["Q1", "Q2", "Q3", "Q4"],
    "datasets": [
      {
        "label": "2024",
        "data": [50, 75, 60, 90],
        "backgroundColor": "#8b5cf6"
      },
      {
        "label": "2025",
        "data": [65, 80, 70, 95],
        "backgroundColor": "#3b82f6"
      }
    ]
  },
  "options": {
    "plugins": {
      "title": { "display": true, "text": "Year-over-Year Revenue" }
    }
  }
}
```

## Candlestick Chart Example

```json
{
  "type": "candlestick",
  "data": {
    "datasets": [
      {
        "label": "Price",
        "data": [
          { "x": 1740441600000, "o": 4.23, "h": 4.80, "l": 4.10, "c": 4.45 },
          { "x": 1740528000000, "o": 4.45, "h": 5.50, "l": 4.30, "c": 5.34 },
          { "x": 1740614400000, "o": 5.34, "h": 6.20, "l": 5.10, "c": 5.97 }
        ]
      }
    ]
  },
  "options": {
    "plugins": {
      "title": { "display": true, "text": "Price History" }
    }
  }
}
```

Use `"type": "ohlc"` for bar-style OHLC rendering. The `x` field accepts numeric timestamps (recommended) or date strings like `"2025-02-25"`.

## Color Suggestions

| Color | Hex | Good For |
|-------|-----|----------|
| Purple | `#8b5cf6` | Primary data |
| Blue | `#3b82f6` | Secondary data |
| Green | `#10b981` | Positive/growth |
| Red | `#ef4444` | Negative/decline |
| Amber | `#f59e0b` | Warning/neutral |
| Indigo | `#6366f1` | Accent |

For pie/doughnut charts, pass an array of colors:

```json
"backgroundColor": ["#8b5cf6", "#3b82f6", "#10b981", "#ef4444", "#f59e0b"]
```
