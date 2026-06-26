---
name: geojson
description: Inspect, validate, summarize, and troubleshoot GeoJSON files and payloads, including FeatureCollection checks, geometry counting, bbox generation, coordinate range review, and CRS-related safety guidance. Use when the user asks about GeoJSON, FeatureCollection, geometry validity, 坐标范围检查, bbox, GeoJSON summary, or GeoJSON debugging.
metadata:
  openclaw:
    emoji: "🗂️"
    requires:
      bins: ["python3"]
    install:
      - id: "brew"
        kind: "brew"
        formula: "python"
        bins: ["python3"]
        label: "Install Python 3 (brew)"
---

# GeoJSON

Use this skill for practical GeoJSON inspection and validation.

This skill focuses on safe read-only analysis of GeoJSON structure and coordinates. For deterministic GIS conversion, reprojection, clipping, or raster/vector processing on files, hand off to `qgis`.

## What This Skill Does

- Validate whether a JSON file or payload is plausible GeoJSON.
- Summarize top-level type, feature count, geometry types, and bbox.
- Flag obvious coordinate-range issues for longitude/latitude style data.
- Explain common GeoJSON mistakes such as malformed `FeatureCollection`, missing `geometry`, or wrong coordinate nesting.
- Recommend when `EPSG:4326` assumptions are safe and when CRS clarification is required.

## Standard Workflow

1. Confirm whether the input is a file path or inline JSON.
2. Parse the JSON and identify the top-level GeoJSON type.
3. Count features and geometry types.
4. Compute bbox from coordinates when possible.
5. Flag likely coordinate problems:
   - out-of-range longitude/latitude
   - swapped `lat,lon` vs `lon,lat`
   - mixed geometry structures
6. If the user needs file transformation, reprojection, or editing, switch to `qgis`.

## Practical Commands

### Summarize a GeoJSON file

```bash
python3 {baseDir}/scripts/geojson_tool.py summary --file ./data/sample.geojson
```

### Validate a GeoJSON file

```bash
python3 {baseDir}/scripts/geojson_tool.py validate --file ./data/sample.geojson
```

### Summarize inline GeoJSON

```bash
python3 {baseDir}/scripts/geojson_tool.py summary --json '{"type":"Point","coordinates":[116.4074,39.9042]}'
```

## Decision Rules

- Assume GeoJSON coordinates are `lon,lat` when they represent geographic positions unless the source clearly says otherwise.
- Do not assume every GeoJSON file is WGS84 just because it is GeoJSON; verify source context if precision matters.
- GeoJSON CRS metadata is effectively absent in modern practice; prefer explicit prose in the answer when CRS is uncertain.
- If distance or area analysis is needed, recommend reprojection to a projected CRS before measurement.
- Treat malformed but parseable data as suspect; report the issue instead of silently guessing.

## What To Return

- Top-level GeoJSON type.
- Feature count when applicable.
- Geometry type counts.
- Bounding box when coordinates are present.
- A short note about likely CRS/coordinate-order assumptions.
- Specific validation errors or suspicious patterns when found.

## When Not To Use

- Reverse geocoding or coordinates-to-address lookup: use `geocode`.
- WGS84-specific CRS reasoning: use `wgs84`.
- Deterministic GIS processing, conversion, reprojection, or clipping: use `qgis`.
- CesiumJS rendering logic: use `cesium`.

## OpenClaw + ClawHub Notes

- Keep examples generic and portable.
- Do not hardcode private datasets, machine paths, or secrets.
- For clawhub.ai publication, keep examples standards-based and version/changelog updates semver-driven.

## Reference Docs In This Skill

- Read `{baseDir}/references/geojson-notes.md` for common structures, nesting rules, and failure cases.
