---
name: cgcs2000
description: Explain and work with the CGCS2000 coordinate reference system for China geospatial workflows, including EPSG:4490 interpretation, projected CRS selection, Gauss-Kruger zoning, axis/unit checks, and comparison with WGS84, GCJ-02, and BD-09. Use when the user asks about CGCS2000, 中国大地2000, EPSG:4490, 国家2000坐标系, 高斯-克吕格分带, 坐标系选择, or CGCS2000 conversion guidance.
metadata:
  openclaw:
    emoji: "🇨🇳"
---

# CGCS2000

Use this skill for practical reasoning about the China Geodetic Coordinate System 2000.

CGCS2000 is a China-centered geodetic reference framework used widely in surveying, mapping, and domestic GIS workflows. In many GIS tools, the geographic form is commonly represented as `EPSG:4490`, but real work often also involves projected CGCS2000 variants, especially Gauss-Kruger zone systems.

## What This Skill Does

- Explain what CGCS2000 is and when it is the right source or target CRS.
- Distinguish geographic `CGCS2000` from projected `CGCS2000` variants.
- Identify whether the user likely means `EPSG:4490` or a projected China CRS in meters.
- Check for common mistakes involving axis order, units, and false assumptions about "same as WGS84".
- Compare `CGCS2000` with `WGS84`, `GCJ-02`, and `BD-09`.
- Recommend whether to keep the data in geographic coordinates or move to a projected CRS for analysis.
- Hand off file-based conversion and batch reprojection steps to `qgis` when execution is needed.

## Standard Workflow

1. Confirm the actual input form:
   - longitude/latitude in degrees
   - projected easting/northing in meters
   - map-app coordinates that may actually be `GCJ-02` or `BD-09`
2. Ask whether the user needs:
   - storage or exchange
   - web display
   - engineering, surveying, or measurement
   - file-based reprojection
3. State the exact CRS level being discussed:
   - `CGCS2000` datum/reference frame
   - `EPSG:4490` geographic CRS
   - projected `CGCS2000` CRS with zone/projection details
4. Validate units and order before recommending conversion.
5. If the task needs meters, recommend the exact projected CRS rather than only saying "CGCS2000".

## Decision Rules

- Use `EPSG:4490` when the data is truly geographic `CGCS2000` longitude/latitude in degrees.
- For engineering, cadastral, measurement, or local analysis work, prefer the correct projected `CGCS2000` CRS in meters.
- Do not say "CGCS2000" alone when the task requires a projected CRS; include zone/projection details.
- Do not treat `GCJ-02` or `BD-09` as standard `CGCS2000` coordinates.
- Do not assume consumer-map coordinates in China are raw `CGCS2000` or raw `WGS84`.
- If the source is unknown, explicitly call out datum/projection uncertainty before suggesting a transformation.

## Common Cases

### The user says "CGCS2000 coordinates"

Interpret carefully:

- It may mean `EPSG:4490` longitude/latitude in degrees.
- It may mean a projected `CGCS2000` coordinate system in meters.
- It may be shorthand from a local data specification that still requires the exact EPSG or projection name.

### The user wants to compare CGCS2000 and WGS84

- They are close for many practical GIS use cases, but they are not interchangeable by definition in every precise workflow.
- If regulatory, survey, or engineering accuracy matters, keep the stated source datum and use the required official CRS.
- If the task is generic storage or API exchange, explain whether the downstream system expects `CGCS2000` or `WGS84` explicitly.

### The user has China map coordinates from an app

- First check whether the source is actually `GCJ-02` or `BD-09`.
- Do not label app-map coordinates as `CGCS2000` without evidence.
- If the request is about web maps or app SDKs, mention offset-system ambiguity early.

### The user wants projected analysis

- Ask for the area of use and the current CRS.
- Recommend the exact projected `CGCS2000` CRS with units in meters.
- If the user only has files and wants execution, use `qgis`.

## What To Return

- The interpreted source CRS, with exact name or EPSG when possible.
- Whether the coordinates are likely geographic degrees or projected meters.
- Whether `EPSG:4490` is appropriate, or whether a projected `CGCS2000` CRS is needed instead.
- Any risk that the data is actually `GCJ-02` or `BD-09`.
- A concrete next step for reprojection, exchange, or validation.

## When Not To Use

- Reverse geocoding or address lookup: use `geocode`.
- QGIS file-based processing or batch reprojection: use `qgis`.
- General CRS comparison across many systems when CGCS2000 is not the focus: use `project`.
- GPS-only WGS84 validation with no China-specific CRS question: use `wgs84`.

## OpenClaw + ClawHub Notes

- Keep examples generic and standards-based.
- Do not hardcode private datasets, machine paths, credentials, or proprietary basemap assumptions.
- For clawhub.ai publication, keep examples reproducible and version/changelog updates semver-driven.

## Reference Docs In This Skill

- Read `{baseDir}/references/cgcs2000-reference.md` for quick comparison points, projected-workflow guidance, and common failure cases.
