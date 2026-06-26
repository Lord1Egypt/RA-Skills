---
name: skyroute
description: 3D globe visualization of global traffic flowing to AWS regions. Shows real-time user connections with latency-colored arcs, CloudFront edge node panels, P95/P99 metrics, error rate alerts, and sparkline trends. Use when building a global traffic monitoring dashboard, visualizing CDN/user distribution, or creating a "war room" real-time traffic display for web applications served via CloudFront/ALB.
---

# SkyRoute — 3D Global Traffic Monitor

A self-contained HTML/WebGL dashboard that renders a 3D globe showing real-time traffic connections from users worldwide to your AWS backend region.

## Features

- **3D Globe** with country polygons (no external textures — pure geometry)
- **Animated arcs** from user locations to target region, color-coded by latency (green < 100ms, yellow < 300ms, red > 300ms)
- **CloudFront edge panel** showing top PoPs by request volume
- **Metrics panel**: active connections, RPS, P95/P99 latency, error rate
- **Alert mode**: header flashes red when error rate spikes, with alert badge
- **Sparkline trends** for latency/RPS history
- **Country name mapping** (CC → Chinese name)

## Files

- `assets/globe.html` — Complete standalone dashboard (Three.js + custom shaders via CDN)

## Usage

### Static demo

Open `assets/globe.html` directly in a browser. It includes a mock data generator that simulates global traffic.

### With real data

To connect real data, modify the `generateConnections()` function in the HTML to fetch from your data source. Expected data format per connection:

```json
{
  "lat": 51.5,
  "lng": -0.12,
  "latency": 85,
  "country": "GB",
  "requests": 1200
}
```

### Data sources (integration ideas)

1. **ALB access logs** → parse source IPs → GeoIP lookup → aggregate by region
2. **CloudFront real-time logs** → Kinesis → Lambda → WebSocket push
3. **Custom metrics API** → poll every 5s from your monitoring backend

### GeoIP Setup

For production use, obtain MaxMind GeoLite2-City database:
1. Register at https://www.maxmind.com/en/geolite2/signup
2. Download GeoLite2-City.mmdb
3. Use with a backend service to resolve IP → lat/lng

## Customization

| Config | Location | Description |
|--------|----------|-------------|
| Target region | `TARGET_REGION` const | AWS region coordinates (default: us-west-2) |
| Color thresholds | `getArcColor()` | Latency → color mapping |
| Alert threshold | `ERROR_THRESHOLD` | Error rate % to trigger alert mode |
| Panel layout | CSS `.panel` classes | Reposition info panels |
| Country names | `CC_NAMES` object | ISO code → display name mapping |

## Deployment

Serve as a static file behind any web server or embed in an internal dashboard (Grafana iframe, TV display, etc.). No backend required for the visualization itself — all rendering is client-side WebGL.
