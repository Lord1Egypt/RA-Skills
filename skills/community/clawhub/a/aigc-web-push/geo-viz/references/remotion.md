# Remotion

Implement inside the aigc-web-push work folder. Host quality rules still apply.

## Dependencies (install in the work’s `remotion/` project as needed)

| Package | Use |
| --- | --- |
| `three` + `@remotion/three` | 3D terrain / science |
| `maplibre-gl` | 2D / 2.5D maps |
| `@turf/turf` | Routes / spatial ops |
| optional `cesium` | Globe (wire `delayRender`) |

Load Remotion official skills first. Prefer frame-driven `jumpTo` over map runtime clocks.

## Determinism

- Drive camera / `drawProgress` / cuts from `useCurrentFrame()`.
- Cache tiles / DEM under `geo/` before render; use `delayRender` / `continueRender`.

## Work layout

```text
works/<date>-<topic>/
  remotion/
  geo/
    manifest.json
    dem/…
    vectors/…
  audio/
  out/<topic>.mp4
```

`assetsBase` points at that `geo/` (or a local mirror). Never read planet-scale data from the skill package.

## Global reuse

Same Composition; swap `bbox` / `center` / route GeoJSON / `locale` / `style` / regional `geo/` cache. Do not fork per country.

## Material whitelist

Open geo data used for **programmatic drawing** is allowed. Still forbidden: AI fake satellite/terrain, unauthorized stock as hero, modern OSM as historical routes.
