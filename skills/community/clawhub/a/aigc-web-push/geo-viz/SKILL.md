---
name: geo-viz
description: >-
  Geographic visualization for video: maps, routes, terrain, globe, buildings,
  basins. Parametric for any country/locale. Free-key open data. Load when a shot
  needs real geography. Remotion or HyperFrames.
version: 1.0.0
---

# geo-viz · Geographic visualization

Load when a primary shot needs real geography. Skip when the film has no map / terrain / globe / route shots.

## When to load

- Maps, route draw-on, borders, city pins, highways
- Terrain, profiles, basins, coasts / seafloor
- Globe flights, plate / geologic space
- Building footprints / extruded massing
- Historical geography with real coordinates (see history rule)

Skip for decorative backgrounds or non-geographic explainers.

## Read order

1. This `SKILL.md`
2. `references/props-contract.md` — universal inputs (any country)
3. `references/data.md` — free-key sources
4. `references/scenes.md` — shot → engine
5. Framework one of:
   - Remotion → `references/remotion.md`
   - HyperFrames → `references/hyperframes.md`
6. If cropping / CRS → `references/preprocessing.md`
7. Before delivery → `references/checklist.md`
8. Cache policy → `references/storage.md`

## Hard rules

1. **Free-key defaults.** No API Key / Token basemaps (天地图 / 星图 / MapTiler / 高德, etc.) as the default path.
2. **Parametric scenes.** Inputs: `bbox` / `center` / GeoJSON / `locale` / `assetsBase`. No per-country code forks.
3. **Fetch by extent.** Never download the whole planet “just in case.”
4. **Deterministic time.** Remotion = frame; HyperFrames = seek. No wall-clock map playback at render.
5. **HyperFrames basemaps: bake** (`bake-basemap`). No live tiles at render time.
6. **History.** Ancient roads / canals / channels need verified historical data; record sources in `manifest`. Do not use modern OSM as a stand-in.
7. **No AI fake geography.** No AI stills/video as fake satellite or terrain.
8. **Attribution.** Keep license / CRS / attribution with assets and on screen when required.

## Pipeline

1. Mark geographic shots and their `center` / `bbox` / routes in the storyboard.
2. Resolve data per `data.md` → work folder `geo/` (see `storage.md`).
3. Pick engine per `scenes.md`.
4. Implement against `props-contract.md`.
5. Pass `checklist.md`, then host QA.

## Hosts

| Host | Where |
| --- | --- |
| aigc-web-push | Bundled `geo-viz/`; open geo data is a programmatic whitelist, not stock B-roll |
| cursor-service (HyperFrames) | `.cursor/skills/geo-viz` |

## Engines

MapLibre, Three.js, and Cesium cover different shots. Prefer real data + code; Blender pre-render when real-time is unstable.
