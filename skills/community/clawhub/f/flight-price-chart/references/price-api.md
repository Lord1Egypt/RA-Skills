# Price Trend API Reference

## Overview

The Price Trend API provides historical price data for flight routes, enabling price analysis and visualization.

## Endpoint

```
GET /api/price/trend
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `origin` | string | Yes | Origin airport/city code (e.g., "SHA", "PVG") |
| `destination` | string | Yes | Destination airport/city code (e.g., "TYO", "BKK") |
| `days` | number | No | Number of days of history (default: 60, max: 180) |

## Request Example

```bash
curl "https://api.example.com/price/trend?origin=SHA&destination=TYO&days=60"
```

## Response Format

```json
{
  "success": true,
  "data": {
    "route": {
      "origin": "SHA",
      "destination": "TYO",
      "originName": "Shanghai",
      "destinationName": "Tokyo"
    },
    "priceHistory": [
      [1706227200, 1450],
      [1706313600, 1380],
      [1706400000, 1420]
    ],
    "lowestPrice": 1299,
    "priceLevel": "low",
    "analysis": {
      "min": 1199,
      "max": 1899,
      "average": 1450,
      "trend": "falling",
      "confidence": 0.85
    }
  }
}
```

## Response Fields

### priceHistory

Array of `[timestamp, price]` tuples:
- `timestamp`: Unix timestamp in seconds
- `price`: Price in local currency (CNY)

### priceLevel

String indicator of current price position:
- `"low"`: Below 33rd percentile
- `"typical"`: Between 33rd and 67th percentile
- `"high"`: Above 67th percentile

### analysis

| Field | Type | Description |
|-------|------|-------------|
| `min` | number | Minimum price in period |
| `max` | number | Maximum price in period |
| `average` | number | Average price (rounded) |
| `trend` | string | "falling" | "rising" | "stable" |
| `confidence` | number | Prediction confidence (0-1) |

## Error Responses

### 400 Bad Request

```json
{
  "success": false,
  "error": "MISSING_PARAMETER",
  "message": "Missing required parameter: destination"
}
```

### 404 Not Found

```json
{
  "success": false,
  "error": "ROUTE_NOT_FOUND",
  "message": "No price data available for SHA-TYO"
}
```

### 503 Service Unavailable

```json
{
  "success": false,
  "error": "DATA_UNAVAILABLE",
  "message": "Price data service temporarily unavailable"
}
```

## Data Coverage

### Supported Routes

- Domestic China routes: 100% coverage
- Major international routes from China: 90% coverage
- Emerging routes: 60% coverage

### Data Freshness

- Prices updated: Every 6 hours
- Historical data retention: 2 years
- Real-time availability: 99% uptime SLA

## Rate Limits

| Tier | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 10 | 500 |
| Pro | 60 | 10,000 |
| Enterprise | 300 | Unlimited |

## Integration Example

### JavaScript/Node.js

```javascript
async function getPriceTrend(origin, destination, days = 60) {
  const params = new URLSearchParams({ origin, destination, days: String(days) });
  const response = await fetch(`/api/price/trend?${params}`);

  if (!response.ok) {
    throw new Error(`Price API error: ${response.status}`);
  }

  const result = await response.json();
  return result.data;
}

// Usage
const trendData = await getPriceTrend('SHA', 'TYO');
console.log(`Current price: ¥${trendData.lowestPrice}`);
console.log(`Price level: ${trendData.priceLevel}`);
```

### Python

```python
import requests

def get_price_trend(origin, destination, days=60):
    params = {'origin': origin, 'destination': destination, 'days': days}
    response = requests.get('/api/price/trend', params=params)
    response.raise_for_status()
    return response.json()['data']

# Usage
trend = get_price_trend('SHA', 'TYO')
print(f"Current price: ¥{trend['lowestPrice']}")
print(f"Price level: {trend['priceLevel']}")
```

## Data Conversion for PriceChart

Convert API response to PriceChart component props:

```javascript
function convertApiToChart(apiData) {
  const { priceHistory, lowestPrice, analysis, route } = apiData;

  return {
    data: priceHistory.map(([timestamp, price]) => ({
      date: new Date(timestamp * 1000).toISOString().split('T')[0],
      price
    })),
    currentPrice: lowestPrice,
    analysis: {
      min: analysis.min,
      max: analysis.max,
      average: analysis.average,
      pctDiff: Math.round(((lowestPrice - analysis.average) / analysis.average) * 100),
      level: apiData.priceLevel === 'typical' ? 'mid' : apiData.priceLevel,
      trend: analysis.trend
    },
    destination: {
      code: route.destination,
      name: route.destinationName
    }
  };
}
```
