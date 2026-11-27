# Storage (local-first)

## Default (required for the published skill)

1. Download **only what this film needs** (bbox / region).
2. Keep it under the **work folder**:
   - Remotion: `works/<id>/geo/`
   - HyperFrames: project `assets/geo/` (+ bake MP4s in `assets/`)
3. Write `manifest.json` (source, license, CRS, bbox, time, attribution).
4. Skill package and Git: **instructions only** — never ship global DEM/OSM.

No cloud account, no upload API, and no shared bucket are required for geo-viz to work for global users.

## Optional: platform shared cache (lazy fill)

If a host product (e.g. Design) later provides authenticated geo cache:

```text
need asset for key K
  → cache hit? use it
  → miss? download from open source → process → upload to cache → use
  → cache/upload failure? continue with local file; do not block render
```

Rules for that product feature (not this skill’s publish gate):

- Cache **processed** crops / extracts, not every transient tile screenshot
- Key by extent / region (`dem/…`, `osm/<region>/`, `vectors/…`)
- Keep manifests; respect licenses; quota + auth against abuse
- Never make the open-source skill hard-depend on one vendor bucket

## What not to do now

- Pre-mirror the whole planet
- Require an HTTP upload API before shipping the skill
- Force every third-party installer to write into your cloud
