# 🌐 SkyRoute

**[🔴 Live Demo](https://chengcecho.github.io/skyroute/)**

**3D real-time global traffic visualization for [OpenClaw](https://github.com/openclaw/openclaw)**

A stunning WebGL globe that visualizes live user connections flowing from around the world to your AWS backend — like a network operations "war room" display.

> 💡 **Click the Live Demo link above** to see it running in your browser — no install needed!

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌍 **3D Globe** | Country polygons rendered in WebGL — no textures, no external assets |
| 🌈 **Latency Arcs** | Animated connections color-coded: 🟢 <100ms · 🟡 <300ms · 🔴 >300ms |
| 📡 **Edge Panel** | CloudFront PoP breakdown by request volume |
| 📊 **Live Metrics** | Active connections, RPS, P95/P99 latency, error rate |
| 🚨 **Alert Mode** | Header flashes red when error rate spikes |
| 📈 **Sparklines** | Inline trend charts for latency & throughput history |
| 🗺️ **i18n Names** | ISO country codes → localized display names |

## 🎯 Use Cases

- **NOC / War Room** — wall-mounted real-time traffic display
- **Executive Dashboard** — impressive overview of global reach
- **Incident Response** — visualize traffic shifts during outages
- **Presentations** — stunning backdrop for architecture talks
- **Demo Days** — show global scale to stakeholders

## 🚀 Quick Start

```bash
git clone https://github.com/chengcecho/skyroute
open skyroute/assets/globe.html
```

That's it. Single HTML file, zero dependencies, no build step.

## 🔌 Connect Real Data

The demo runs with simulated traffic. To use real data, modify `generateConnections()`:

```javascript
// Expected data format per connection:
{
  "lat": 51.5,        // Source latitude
  "lng": -0.12,       // Source longitude
  "latency": 85,      // RTT in milliseconds
  "country": "GB",    // ISO country code
  "requests": 1200    // Request count
}
```

### Integration Ideas

| Source | Method |
|--------|--------|
| ALB access logs | Parse IPs → GeoIP → aggregate by region |
| CloudFront real-time logs | Kinesis → Lambda → WebSocket push |
| Custom metrics API | Fetch every 5s from your monitoring backend |
| Nginx logs | Tail + GeoIP lookup → SSE stream |

## 🛠️ Customization

```javascript
// Target AWS region (arc destination)
const TARGET_REGION = { lat: 45.5, lng: -122.6 }; // us-west-2

// Latency color thresholds
function getArcColor(latency) { ... }

// Error rate alert trigger
const ERROR_THRESHOLD = 5; // percent

// Country name mapping
const CC_NAMES = { US: '美国', GB: '英国', ... };
```

## 🏗️ Tech Stack

- **Three.js** — WebGL 3D rendering
- **Vanilla JS** — zero framework dependencies
- **Self-contained** — single HTML file, CDN imports only
- **Responsive** — adapts to any screen size

## 📦 Deployment Options

| Method | Steps |
|--------|-------|
| **GitHub Pages** | Fork → Settings → Pages → Done |
| **Static hosting** | Upload `assets/globe.html` to S3/Nginx/Vercel |
| **Grafana embed** | iframe panel pointing to hosted URL |
| **TV display** | Full-screen kiosk mode on a wall monitor |

## License

MIT
