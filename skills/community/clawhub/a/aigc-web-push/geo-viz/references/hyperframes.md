# HyperFrames

Workspace: cursor-service. Contract: no render-time network, seek-safe, assets under `assets/`.

## Flat maps / real places (default)

1. Read `hyperframes/references/film.md` → Maps.
2. Bake with `hyperframes/scripts/bake-basemap.mjs` → `assets/<name>.mp4` + `<name>-coords.json`.
3. Play the MP4; animate borders/routes/labels as SVG from coords while the camera holds.
4. On-screen attribution + `data-layout-ignore`.

### Preferred `STYLE` (free-key)

| Value | Meaning |
| --- | --- |
| `liberty` / `openfreemap` | OpenFreeMap liberty (**default**) |
| `positron` / `bright` | Other OpenFreeMap styles |
| `gibs-bluemarble` | NASA GIBS overview imagery |
| `dark` / `light` | Carto fallback |
| `satellite` | Esri fallback (credit ToS; not preferred) |
| custom URL | Self-hosted XYZ or style JSON |

```bash
NAME=route-a STYLE=liberty CENTER="116.4,39.9" ZSTART=3 ZEND=10 \
  FPS=30 DUR=6 HOLD=0.55 OUT=./assets \
  node .cursor/skills/hyperframes/scripts/bake-basemap.mjs
```

One bake at a time. Commit bake outputs into the project for offline renders.

## 3D

Three.js via `hf-seek` / `__hf.buildReady`. DEM and models must already be local under `assets/`. Heavy shots: Blender → MP4 clip.

## Data

Same `data.md` as Remotion. Prefer the work’s local `assets/geo/` copy for the current film only.
