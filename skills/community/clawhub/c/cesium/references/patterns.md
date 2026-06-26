# Cesium Patterns

Use this file as a quick reference for common CesiumJS implementation patterns.

## 1. Minimal viewer bootstrap

```ts
import { Viewer } from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";

const viewer = new Viewer("cesiumContainer", {
  animation: false,
  timeline: false,
  requestRenderMode: true,
});
```

Notes:
- Ensure `#cesiumContainer` has explicit width/height in CSS.
- In SPA teardown, call `viewer.destroy()`.

## 2. Environment token wiring

```ts
import { Ion } from "cesium";

Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ION_TOKEN ?? "";
```

Notes:
- Do not hardcode real tokens in repo files.
- Fail fast with a clear error if required token is missing.

## 3. Load GeoJSON and frame camera

```ts
import { GeoJsonDataSource } from "cesium";

const ds = await GeoJsonDataSource.load("/data/boundaries.geojson", {
  stroke: undefined,
});
viewer.dataSources.add(ds);
await viewer.zoomTo(ds);
```

## 4. Screen picking safety

```ts
const picked = viewer.scene.pick(click.position);
if (!picked) return;

const entity = (picked as { id?: unknown }).id;
if (!entity) return;
```

Notes:
- Picking may return primitives without `.id`.
- Guard all casts and branch by object shape.

## 5. Performance baseline toggles

Start with:
- `requestRenderMode: true`
- `maximumRenderTimeChange: Infinity`
- hide heavy UI widgets unless needed

Then profile before adding custom optimizations.
