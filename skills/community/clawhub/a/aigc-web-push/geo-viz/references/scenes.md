# Scenes → engines

Pick by narrative need. Inputs must follow `props-contract.md`.

| Scene | Look | Engine | Remotion | HyperFrames |
| --- | --- | --- | --- | --- |
| Locate on map | Basemap, pins, borders | MapLibre | Frame-driven camera | bake-basemap + SVG |
| Route growth | Line draw-on, follow | MapLibre + Turf | `drawProgress` | bake + SVG |
| Globe flight | Spin, dive, land | Cesium or MapLibre globe bake | Adapter / pre-render | `PROJECTION=globe` bake |
| Mountain terrain | Ridges, orbit | Cesium / Three | Components | Pre-render or `hf-seek` |
| Terrain profile | Cut, Z exaggerate | Three / Blender | `@remotion/three` | `hf-seek` / clip |
| Rivers / basins | Network grow | MapLibre + Hydro* | Frame | bake + SVG |
| City massing | Extrude footprints | Three / Cesium | Components | `hf-seek` |
| Geology / plates | Section, motion | Three | Components | `hf-seek` |
| Hazards | Epicenter, ripples | MapLibre + Three | Mix | bake + overlay |
| Population / economy | Heat, charts | MapLibre + D3 | Mix | catalog chart + bake |
| Historical borders | Then/now | MapLibre + curated GeoJSON | Frame | bake + SVG |
| Science machinery | Structure, particles | Three / Blender | Components | `hf-seek` / clip |

## Order of choice

1. Real place / route / border → MapLibre (HF: bake).
2. Browseable terrain → Cesium or terrain tiles; heavy → pre-render.
3. Profiles / abstract science → Three.js.
4. Cinematic weight that breaks real-time → Blender, then composite.
