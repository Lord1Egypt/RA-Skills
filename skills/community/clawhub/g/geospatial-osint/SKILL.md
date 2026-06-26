---
name: geospatial-osint
description: Open-source geospatial intelligence gathering and visualization dashboard. Use when building Worldview-style spy thriller dashboards, monitoring geopolitical events, or analyzing multi-source OSINT. Covers satellite tracking, live flights (commercial + military), maritime traffic, street cameras, seismic data, and real-time visualization with post-processing effects. Supports 3D globe rendering with CRT/NVG/thermal modes, time-based replay, and multi-agent development workflows.
---

# Geospatial OSINT / Worldview Dashboard

This skill covers building real-time geospatial intelligence dashboards inspired by Bilawal Sidhu's Worldview project.

## Quick Start

### Core Data Sources (Free)

| Source | API/URL | Use Case |
|--------|---------|----------|
| [ADS-B Exchange](https://www.adsbexchange.com/) | API, free key | Commercial flights |
| [ADS-B Exchange Military](https://www.adsbexchange.com/api/military/) | API | Military aircraft |
| [OpenSky Network](https://opensky-network.org/) | Free API | Flight data |
| [MarineTraffic](https://www.marinetraffic.com/) | Free tier | Ship positions |
| [CelesTrak](https://celestrak.org/) | TLE files | Satellite orbits |
| [n2yo.com](https://www.n2yo.com/) | Free API | Satellite passes |
| [GPSJam](https://gpsjam.org/) | Static | GPS jamming heatmaps |
| [Earthquakes](https://earthquake.usgs.gov/earthquakes/feed/) | GeoJSON | Seismic data |
| [Insecam](https://www.insecam.org/) | Public cams | CCTV cameras |
| [OpenStreetMap](https://www.openstreetmap.org/) | Overpass API | Road networks |

### Paid Options (Optional)

- Planet Labs (daily imagery)
- Maxar (high-res)
- Capella Space (SAR)
- MarineTraffic Pro

## Architecture

### Stack

```
Frontend:      Cesium.js (3D globe) + Three.js (effects)
Data Layer:    Polling APIs → WebSocket → Entity updates
Visual:        Post-processing (bloom, CRT, NVG, thermal)
Development:   Multi-agent CLI (OpenClaw, Claude, etc.)
```

### Visual Modes

Worldview supports multiple rendering modes:

```javascript
// Effect pipeline examples
const effects = {
  // Night Vision Goggles (green tint + scanlines)
  nvg: {
    colorMatrix: [0,1,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1],
    scanlines: true,
    vignette: 0.3
  },
  
  // Thermal (heat map coloring)
  thermal: {
    colorMap: 'inferno',
    threshold: true
  },
  
  // CRT (scanlines + curvature + glow)
  crt: {
    scanlines: 0.5,
    curvature: 0.02,
    bloom: 0.5
  },
  
  // Fluor (high contrast military green)
  fluor: {
    colorMatrix: [0,0.5,0,0, 0,1,0,0, 0,0.5,0,0, 0,0,0,1],
    contrast: 1.5
  }
};
```

### Data Layers

| Layer | Source | Update Freq |
|-------|--------|-------------|
| Satellites | CelesTrak TLE | Periodic refresh |
| Commercial flights | ADS-B / OpenSky | ~5 sec |
| Military flights | ADS-B Exchange military | ~5 sec |
| Ships | MarineTraffic | ~1 min |
| CCTV | Insecam | ~1 min |
| Road traffic | OSM + simulation | Static + particles |
| Earthquakes | USGS | Real-time |
| GPS jamming | GPSJam | Static/daily |

## Dashboard Template

### Basic Cesium Setup

```javascript
import * as Cesium from 'cesium';

const viewer = new Cesium.Viewer('container', {
  terrainProvider: Cesium.createWorldTerrain(),
  baseLayerPicker: false,
  timeline: true,
  animation: true,
  sceneMode: Cesium.SceneMode.SCENE3D
});

// Enable 3D buildings
viewer.scene.primitives.add(Cesium.createOsmBuildings());

// Clock settings for replay
viewer.clock.shouldAnimate = true;
viewer.clock.multiplier = 60; // 60x speed
```

### Loading Flight Data

```javascript
async function loadFlights(bounds) {
  const response = await fetch(
    `https://opensky-network.org/api/states/all?lamin=${bounds.minLat}&lomin=${bounds.minLon}&lamax=${bounds.maxLat}&lomax=${bounds.maxLon}`
  );
  const data = await response.json();
  
  data.states.forEach(flight => {
    const [icao, callsign, .., lat, lon, alt, .., velocity, heading] = flight;
    // Add entity to viewer
    viewer.entities.add({
      id: icao,
      position: Cesium.Cartesian3.fromDegrees(lon, lat, alt),
      point: { pixelSize: 5, color: getFlightColor(callsign) },
      label: { text: callsign, font: '10px monospace' }
    });
  });
}
```

### Satellite Tracking

```javascript
// Load TLE and calculate positions
const satellites = await fetch('https://celestrak.org/NORAD/elements/gp.php?GROUP=visual&FORMAT=tle')
  .then(r => r.text());

// Use satellite.js to propagate
import { propagate, eciToEcf } from 'satellite.js';

function updateSatellite(satrec, time) {
  const position = propagate(satrec, time);
  const gmst = satellite.gstime(time);
  const positionEcf = eciToEcf(position.position, gmst);
  
  return {
    x: positionEcf.x * 1000,
    y: positionEcf.y * 1000,
    z: positionEcf.z * 1000
  };
}
```

### CCTV Camera Overlay

```javascript
// Insecam - public cameras
async function loadCameras(bounds) {
  const response = await fetch(
    `https://www.insecam.org/en/by-country/XX/?page=1` // Filter by country
  );
  // Parse camera list, add as entities with video texture
}

// Project camera onto 3D geometry
cameraEntities.forEach(cam => {
  viewer.entities.add({
    position: cam.location,
    billboard: {
      image: cam.snapshot,
      width: 320,
      height: 240,
      pixelOffset: new Cesium.Cartesian2(0, -120)
    }
  });
});
```

## Post-Processing Effects

```javascript
// Using Cesium's PostProcessStage
const bloom = viewer.scene.postProcessStages.bloom;
bloom.enabled = true;
bloom.threshold = 0.5;
bloom.strength = 0.5;

// Custom shader for CRT effect
const crtEffect = new Cesium.PostProcessStage({
  name: 'crt',
  fragmentShader: `
    uniform sampler2D colorTexture;
    varying vec2 v_textureCoord;
    void main() {
      vec4 color = texture2D(colorTexture, v_textureCoord);
      // Scanlines
      float scanline = sin(v_textureCoord.y * 800.0) * 0.04;
      // Vignette
      float vignette = 1.0 - length(v_textureCoord - 0.5) * 0.5;
      gl_FragColor = vec4(color.rgb * (1.0 - scanline) * vignette, 1.0);
    }
  `
});
```

## Workflow: Building with AI Agents

### Multi-Agent Setup

Run multiple terminals in parallel:

```
Terminal 1: Core 3D globe + Cesium setup
Terminal 2: Data integration (flights, satellites)  
Terminal 3: Visual effects (shaders, post-processing)
Terminal 4: UI controls + camera systems
```

### Prompt Template

```
Build a [feature] for my Cesium.js geospatial dashboard.
Requirements:
- [specific behavior]
- Integration with existing data layer
- Performance: handle [N] entities without lag
- Visual style: [CRT/NVG/thermal/none]
```

### Performance Tips

```javascript
// Sequential loading for large datasets
async function loadSequential(data, chunkSize = 1000) {
  for (let i = 0; i < data.length; i += chunkSize) {
    const chunk = data.slice(i, i + chunkSize);
    chunk.forEach(addEntity);
    await new Promise(r => setTimeout(r, 100)); // Yield to UI
  }
}

// Use PointPrimitiveCollection for 10k+ points
const points = viewer.scene.primitives.add(new Cesium.PointPrimitiveCollection());
points.add({ position: ..., color: ... });
```

## Region Monitoring

### Automated Polling

```python
import requests
import schedule
from datetime import datetime

REGIONS = {
  'iran': {'lat': 32.0, 'lon': 52.0, 'radius': 500},
  'gulf': {'lat': 26.0, 'lon': 52.0, 'radius': 300},
}

def monitor():
    for name, bounds in REGIONS.items():
        flights = get_flights(bounds)
        military = get_military(bounds)
        if detect_anomaly(flights, military):
            alert(f"Anomaly in {name}: {details}")

schedule.every(5).minutes.do(monitor)
```

### Alert Conditions

- Sudden flight rerouting
- New no-fly zones
- Unusual military activity
- Satellite coverage of area of interest

## References

- [Cesium.js](references/cesium-basics.md)
- [Rendering Stack](references/rendering-stack.md)
- [ADS-B API](references/adsb-api.md)
- [Satellite Passes](references/satellite-passes.md)
- [Post-Processing](references/effects.md)
