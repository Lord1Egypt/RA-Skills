---
name: cesium
description: Build, debug, and optimize CesiumJS 3D globe apps, including viewer setup, terrain/imagery, 3D Tiles, GeoJSON/CZML loading, camera control, picking, entity styling, and performance tuning. Use when the user asks for Cesium code, Cesium architecture, Cesium bugs, or migration guidance in web projects.
homepage: https://cesium.com/platform/cesiumjs/
metadata:
  {
    "openclaw":
      {
        "emoji": "🌍",
        "homepage": "https://cesium.com/platform/cesiumjs/",
      },
  }
---

# Cesium

Implement CesiumJS solutions with minimal assumptions and production-safe defaults.

## Workflow

1. Confirm runtime assumptions first: framework (vanilla/Vite/React), CesiumJS version, and whether Cesium Ion is available.
2. Start with the smallest runnable viewer setup before adding terrain, 3D Tiles, or heavy data layers.
3. Keep token handling out of source code; use environment variables and project config wiring.
4. Add data layers incrementally and verify camera framing after each step.
5. For rendering/perf issues, reduce scene complexity first, then tune request/render settings.

## Implementation guardrails

- Prefer explicit imports from `cesium` and avoid hidden globals.
- Use `requestRenderMode` for mostly static scenes to reduce GPU/CPU usage.
- Dispose resources in teardown paths (`viewer.destroy()`) in SPA route changes/unmounts.
- For large datasets, prefer 3D Tiles over huge entity collections when possible.
- Keep picking logic resilient: handle `undefined` picks and mixed primitive/entity results.

## Debugging checklist

- Blank globe: verify CSS container height/width and render loop not blocked.
- Missing terrain/tiles: verify network access, token, and dataset permissions.
- Misplaced data: verify CRS and coordinate order (lon, lat, height).
- Memory/GPU pressure: profile number of entities/primitives and texture-heavy layers.

## Reference docs in this skill

- Read `{baseDir}/references/patterns.md` when generating or fixing Cesium code.
