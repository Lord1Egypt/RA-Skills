# Universal props contract

One scene implementation serves every region. Only inputs change.

## CRS and units

| Item | Convention |
| --- | --- |
| Horizontal | WGS84, GeoJSON RFC 7946 (`[lng, lat]`) |
| Elevation | meters; record vertical datum in `manifest` |
| Length | meters for analysis; 0–1 OK for screen progress |
| Time | Remotion: integer frame; HyperFrames: seconds |

## Shared inputs

```ts
type GeoLocale = {
  language: string; // BCP 47: "en" | "zh-CN" | "pt-BR" | ...
  labelsFrom?: "data" | "props" | "none";
};

type GeoAssets = {
  /** Local work folder root (preferred), no trailing slash */
  assetsBase: string;
  attribution: string[];
};

type GeoCamera = {
  center: [lng: number, lat: number];
  zoomStart: number;
  zoomEnd: number;
  pitch?: number;
  bearing?: number;
  from?: [lng: number, lat: number];
};

type GeoExtent = {
  /** [west, south, east, north] */
  bbox: [number, number, number, number];
  /** Optional ISO / Geofabrik id for cache keys only — never hardcode styling on this */
  regionCode?: string;
};
```

## Scene inputs

### Map / route (MapLibre)

```ts
type MapRouteSceneProps = GeoExtent & GeoCamera & GeoAssets & {
  locale: GeoLocale;
  /** OpenFreeMap style URL, GIBS, or self-hosted */
  style: "liberty" | "positron" | "bright" | "gibs-bluemarble" | string;
  route?: GeoJSON.FeatureCollection;
  points?: GeoJSON.FeatureCollection;
  borders?: GeoJSON.FeatureCollection;
  drawProgress: number; // 0–1 from frame / seek
};
```

### Terrain profile (Three.js)

```ts
type TerrainProfileProps = GeoExtent & GeoAssets & {
  demPath: string;
  profileLine: GeoJSON.Feature;
  exaggerateZ?: number;
  cutProgress: number;
};
```

### Globe flight

```ts
type GlobeFlightProps = GeoCamera & GeoAssets & {
  terrain: "mapterhorn" | "none" | "local-dem";
  imagery: "gibs-bluemarble" | "openfreemap" | "local";
  flyProgress: number;
};
```

## Forbidden

- `if (country === "…")` style or logic forks inside components
- Hardcoded single-language placename tables as the only label source
- Shipping global DEM / OSM inside the skill package or npm tarball

## Per-shot sidecar

```text
geo/
  manifest.json
  …
```

`manifest.json` minimum: `sources[]`, `license`, `crs`, `bbox`, `createdAt`, `attribution[]`.
