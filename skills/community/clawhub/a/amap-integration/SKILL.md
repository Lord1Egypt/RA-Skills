---
name: amap-integration
description: Map and location services for search, routing, and visualization. Provides geocoding, POI search, route planning, and heatmap generation capabilities.
credentials:
  - name: AMAP_WEBSERVICE_KEY
    description: Map service API key for geocoding, routing, and POI search features
    optional: true
    source: env
config:
  - path: ~/.openclaw/.env
    description: Environment file for API keys
  - path: ~/.openclaw/credentials/.env
    description: Alternative credentials location
---

# Map Integration Service

This skill provides map-based services including location search, routing, and data visualization.

## Features

### 1. Location Search

For general searches without API key:
- Generate search URL: `https://www.amap.com/search?query={keywords}`
- Returns clickable link for user

### 2. Nearby Search (Requires API Key)

For "search near X" queries:
1. Use geocoding API to get coordinates
2. Generate nearby search link

**API Key Required**: Users must provide their own map service API key.

### 3. Route Planning (Requires API Key)

For directions queries:
1. Get coordinates for origin and destination
2. Use routing API for walking/driving/cycling routes

**API Key Required**: Standard Web Service API key needed.

### 4. Heatmap Visualization

For data visualization requests:
1. Accept data URL (JSON format)
2. Generate visualization link

**Data Format**:
```json
[{"lng": 116.397428, "lat": 39.90923}]
```

### 5. Travel Planning (Requires API Key)

For trip planning queries:
1. Extract city and interest types
2. Search POI data
3. Generate travel map

**API Key Required**

## API Key Configuration

When API key is needed:

1. Get API key from your map service provider
2. Add to OpenClaw config:
   ```
   AMAP_WEBSERVICE_KEY=your_key
   ```
3. Location: `~/.openclaw/.env` or `~/.openclaw/credentials/.env`

## Quick Reference

| Feature | API Key Needed |
|---------|---------------|
| General Search | No |
| Nearby Search | Yes |
| Route Planning | Yes |
| Heatmap | No |
| Travel Planning | Yes |

## Security Notes

- API keys are user-provided credentials
- Keys are stored in user's local environment
- No external data transmission except to map service provider APIs
- Use HTTPS for all production connections

## Disclaimer

This skill is for educational/demonstration purposes. Users should ensure compliance with map service provider terms of service.
