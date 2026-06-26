# Cesium.js Basics

## Setup

```html
<script src="https://cesium.com/downloads/cesiumjs/releases/1.114/Build/Cesium/Cesium.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.114/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="cesiumContainer"></div>
<script>
  Cesium.Ion.defaultAccessToken = 'YOUR_TOKEN';
  const viewer = new Cesium.Viewer('cesiumContainer');
</script>
```

## Key Concepts

### Entities

```javascript
// Add a point
viewer.entities.add({
  position: Cesium.Cartesian3.fromDegrees(-75.59777, 40.03883),
  point: {
    pixelSize: 10,
    color: Cesium.Color.RED
  }
});

// Add a line
viewer.entities.add({
  polyline: {
    positions: Cesium.Cartesian3.fromDegreesArray([
      -75, 40,
      -80, 45
    ]),
    width: 2,
    material: Cesium.Color.YELLOW
  }
});
```

### Time-Dynamic Data (CZML)

For animated flights, use CZML:

```json
[
  {
    "id": "document",
    "name": "Flight",
    "version": "1.0"
  },
  {
    "id": "aircraft",
    "position": {
      "epoch": "2026-03-05T18:00:00Z",
      "cartographicDegrees": [
        0, -75, 40, 1000,
        3600, -80, 45, 10000
      ]
    }
  }
]
```

Load with:
```javascript
const czml = [...];
viewer.dataSources.add(Cesium.CzmlDataSource.load(czml));
```

### Clock & Timeline

```javascript
viewer.clock.startTime = Cesium.JulianDate.fromIso8601('2026-03-05T18:00:00Z');
viewer.clock.stopTime = Cesium.JulianDate.fromIso8601('2026-03-05T20:00:00Z');
viewer.clock.currentTime = viewer.clock.startTime;
viewer.clock.multiplier = 60; // Play at 60x speed
viewer.timeline.zoomTo(viewer.clock.startTime, viewer.clock.stopTime);
```

### 3D Tiles

Load 3D building data:
```javascript
viewer.scene.primitives.add(Cesium.createOsmBuildings());
```

Load terrain:
```javascript
viewer.terrainProvider = Cesium.createWorldTerrain();
```

## Free Tilesets

- **OpenStreetMap 3D buildings**: `Cesium.createOsmBuildings()`
- **Terrain**: `Cesium.createWorldTerrain()`
- **Bing Maps**: Requires Ion token (free tier available)

## Performance Tips

- Use `viewer.scene.alwaysSelectCurrentFrame = false` for static views
- Limit entity count; use `PointPrimitiveCollection` for 1000s of points
- Disable unused widgets: `viewer.scene.globe.enableLighting = false`
