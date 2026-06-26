---
name: amap-maps
description: Amap LBS services. Call Amap services via Streamable HTTP MCP, supporting geocoding, route planning, POI search, weather query, distance measurement, and more.
license: MIT
compatibility: Requires Node.js 18+ and AMAP_KEY environment variable
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":["node"],"env":["AMAP_KEY"]},"primaryEnv":"AMAP_KEY"}}
---

# Amap Maps Skill

Call Amap services via Streamable HTTP MCP.

## Quick Start

### 1. Install Dependencies

```bash
cd amap-maps
npm install
```

### 2. Set Environment Variables

```bash
export AMAP_KEY="Your Amap Key"
```

Get Key: https://lbs.amap.com/api/javascript-api-v2/guide/abc/register

### 3. Use Command Line Tool

```bash
# View all commands
node scripts/amap.js help

# Query weather
node scripts/amap.js weather 北京

# Address to coordinates
node scripts/amap.js geo encode "北京市朝阳区望京 SOHO" 北京

# Coordinates to address
node scripts/amap.js geo decode "116.482384,39.998383"

# Search POI
node scripts/amap.js search text 麦当劳 北京

# Nearby search
node scripts/amap.js search around "116.48,39.99" 餐厅 1000

# Route planning
node scripts/amap.js route driving "116.48,39.99" "116.40,39.91"
node scripts/amap.js route walking "116.48,39.99" "116.40,39.91"
node scripts/amap.js route bicycling "116.48,39.99" "116.40,39.91"
node scripts/amap.js route transit "116.48,39.99" "116.40,39.91" "北京" "北京"

# Distance measurement
node scripts/amap.js distance "116.48,39.99" "116.40,39.91" 1

# IP location
node scripts/amap.js ip-location "114.114.114.114"

# Navigation Schema (generate Amap URI)
node scripts/amap.js navi "116.397428" "39.90923"

# Taxi Schema
node scripts/amap.js taxi "116.397428" "39.90923" "天安门"
```

---

## Tool List (15 tools)

| Category | Command | Description |
|----------|---------|-------------|
| **Weather** | `weather <city>` | Query city weather |
| **Geocoding** | `geo encode <address> [city]` | Address → Coordinates |
| | `geo decode <coordinates>` | Coordinates → Address |
| **Search** | `search text <keyword> [city]` | Keyword search POI |
| | `search around <coordinates> <keyword> [radius]` | Nearby search |
| | `search detail <POI_ID>` | POI details |
| **Routes** | `route driving <origin> <destination>` | Driving route planning |
| | `route walking <origin> <destination>` | Walking route planning |
| | `route bicycling <origin> <destination>` | Cycling route planning |
| | `route transit <origin> <destination> <city> <cityd>` | Transit route planning |
| **Distance** | `distance <origin> <destination> [type]` | Distance measurement (0=linear, 1=driving, 3=walking) |
| **Location** | `ip-location <IP>` | IP location |
| **Schema** | `navi <lon> <lat>` | Generate navigation URI |
| | `taxi <lon> <lat> <name>` | Generate taxi URI |

---

## Common Workflows

### Workflow 1: Search Place → Plan Route

```bash
# 1. Search destination
node scripts/amap.js search text 天安门 北京

# 2. Get location (coordinates) from results

# 3. Plan driving route
node scripts/amap.js route driving "116.48,39.99" "116.397428,39.90923"
```

### Workflow 2: Current Location Weather

```bash
# 1. Get city via IP location
node scripts/amap.js ip-location "114.114.114.114"

# 2. Query weather for that city
node scripts/amap.js weather 南京
```

### Workflow 3: Nearby Exploration

```bash
# 1. Address to coordinates
node scripts/amap.js geo encode "北京市朝阳区望京 SOHO"

# 2. Search nearby restaurants
node scripts/amap.js search around "116.47,39.99" 餐厅 1000
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `AMAP_KEY not set` | Missing environment variable | Run `export AMAP_KEY="..."` |
| `Invalid API Key` | Key is invalid or expired | Check if Key is correct |
| `Missing parameters` | Missing required parameters | Check command format |
| `Rate limit exceeded` | Request rate limit exceeded | Reduce request frequency |

---

## References

- [Amap MCP Server Official Documentation](https://lbs.amap.com/api/mcp-server/summary)
