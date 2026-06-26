# Rendering Stack Deep Dive

## Overview

Worldview runs entirely in the browser using WebGL. No desktop apps, no Unity/Unreal — just vanilla web tech + Cesium.js.

## Core Technology

### Cesium.js — 3D Globe

```javascript
// CDN import
<script src="https://cesium.com/downloads/cesiumjs/releases/1.114/Build/Cesium/Cesium.js"></script>
```

- **What it provides**: Full 3D globe with terrain, 3D tiles, time-dynamic data
- **Why Cesium**: Handles the hard stuff (geographic math, 3D tiling, streaming)
- **Free tier**: Works with OpenStreetMap + limited Bing Maps

```javascript
const viewer = new Cesium.Viewer('cesiumContainer', {
  terrainProvider: Cesium.createWorldTerrain(),
  baseLayerPicker: false,
  animation: true,
  timeline: true,
  sceneMode: Cesium.SceneMode.SCENE3D
});

// 3D buildings (free)
viewer.scene.primitives.add(Cesium.createOsmBuildings());
```

### WebGL / Three.js — Effects Layer

For custom post-processing (CRT, NVG, thermal), you can either:

1. **Use Cesium's PostProcessStage** (easier, already integrated)
2. **Layer Three.js on top** (more control)

```javascript
// Option 1: Cesium post-processing
const crtEffect = new Cesium.PostProcessStage({
  name: 'crt',
  fragmentShader: `...` // Custom GLSL
});
viewer.scene.postProcessStages.add(crtEffect);
```

### HTML/CSS — UI Overlay

The controls (mode switching, sensitivity sliders) are just HTML elements positioned over the canvas:

```html
<div id="controls">
  <button onclick="setMode('crt')">CRT</button>
  <button onclick="setMode('nvg')">NVG</button>
  <button onclick="setMode('thermal')">Thermal</button>
  <input type="range" id="sensitivity" />
</div>

<style>
#controls {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 100;
  background: rgba(0,0,0,0.8);
  color: #0f0; /* Terminal green */
  font-family: monospace;
}
</style>
```

## Rendering Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER RENDER LOOP                       │
├─────────────────────────────────────────────────────────────┤
│  1. Cesium fetches 3D tiles + terrain                      │
│  2. WebGL renders globe to framebuffer                      │
│  3. Post-process stages apply effects (CRT/NVG/etc)         │
│  4. HTML UI overlay composited on top                        │
│  5. RequestAnimationFrame → next frame                       │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
API Polling (JS) → JSON Parse → Cesium Entities → WebGL Render
       ↓
  ~5 sec intervals (ADS-B)
  ~1 min intervals (CCTV, Marine)
```

## Why Browser?

| Advantage | Explanation |
|-----------|-------------|
| No install | URL = app |
| Cross-platform | Works on Mac/Windows/Linux |
| WebGL fast enough | Cesium uses level-of-detail streaming |
| Easy AI coding | Standard JS, no compilation |
| Real-time updates | Just refresh data, not rebuild |

## Performance Considerations

### Browser Limits

- **WebGL context**: One per tab
- **Memory**: ~2GB before crash
- **Entities**: Cesium handles ~10k well with clustering

### Optimization Techniques

```javascript
// 1. Sequential loading (prevents freeze)
async function loadData() {
  for (let chunk of chunks) {
    process(chunk);
    await new Promise(r => setTimeout(r, 50)); // Yield to UI
  }
}

// 2. Level of detail
viewer.scene.globe.maximumScreenSpaceError = 2; // Higher = faster

// 3. Frustum culling
viewer.scene.globe.enableFrustumCulling = true;

// 4. Point primitives (faster than entities)
const points = viewer.scene.primitives.add(
  new Cesium.PointPrimitiveCollection()
);
```

## Alternatives to Cesium

| Library | Pros | Cons |
|---------|------|------|
| Mapbox GL JS | Beautiful 2D/2.5D | Less 3D flexibility |
| Deck.gl | Fast big data | Less globe-focused |
| Globe.gl | Easier Three.js integration | Less mature |
| MapLibre | Free Mapbox alternative | Similar to Mapbox |

## Minimal Starting Code

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cesium.com/downloads/cesiumjs/releases/1.114/Build/Cesium/Cesium.js"></script>
  <link href="https://cesium.com/downloads/cesiumjs/releases/1.114/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
  <style>
    html, body, #cesiumContainer { margin: 0; height: 100%; overflow: hidden; }
  </style>
</head>
<body>
  <div id="cesiumContainer"></div>
  <script>
    Cesium.Ion.defaultAccessToken = 'FREE_TOKEN_FROM_CESIUM_ION';
    const viewer = new Cesium.Viewer('cesiumContainer');
  </script>
</body>
</html>
```

## Development Workflow

```
1. Write prompt to AI agent
2. AI generates HTML/JS
3. Open in browser
4. Iterate: "make it more like CRT mode"
5. Screen capture → content
```

This is exactly what Bilawal did — vibe coded the whole thing with AI agents, no manual WebGL expertise needed.
