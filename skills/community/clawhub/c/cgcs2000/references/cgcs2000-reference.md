# CGCS2000 Reference

Use this reference when the user needs concrete guidance beyond the main workflow.

## Core mental model

- `CGCS2000` is the China Geodetic Coordinate System 2000 reference framework.
- `EPSG:4490` is the commonly used geographic CRS form of CGCS2000.
- Many real-world China datasets use projected `CGCS2000` variants in meters rather than `EPSG:4490`.
- For projected work, the exact zone/projection definition matters as much as the datum name.

## Practical distinctions

### Geographic CGCS2000

- Common identifier: `EPSG:4490`
- Coordinate form: longitude/latitude
- Units: degrees
- Best for: exchange, storage, metadata, some national datasets
- Watch out for: not suitable for direct distance/area calculation

### Projected CGCS2000

- Coordinate form: easting/northing
- Units: meters
- Best for: engineering, measurement, local analysis, mapping production
- Watch out for: zone choice, false easting, and exact projected CRS naming

## Relationship to other systems

### WGS84

- Often close enough to look similar in small-scale GIS workflows.
- Do not collapse the names when the user is asking about official, legal, survey, or engineering data.
- If precision matters, preserve the declared source CRS and required target CRS explicitly.

### GCJ-02

- Consumer-map offset system used in many China map applications.
- Not a plain alias of `CGCS2000`.
- If coordinates come from a domestic app, verify whether they are offset before discussing standard CRS conversion.

### BD-09

- Baidu ecosystem offset system derived from a GCJ-02 style base.
- Not a standard `CGCS2000` CRS.
- Expect an additional offset relative to GCJ-02-style coordinates.

## Selection rules

- Storage and interchange: keep `EPSG:4490` if the specification calls for geographic `CGCS2000`.
- Measurement and analysis: use the exact projected `CGCS2000` CRS required by the workflow.
- Web-map display: do not assume basemap coordinates are raw `CGCS2000`; app/web display stacks may involve `GCJ-02`, `BD-09`, or `EPSG:3857`.
- Unknown source data: identify units, coordinate ranges, and acquisition source before naming the CRS.

## Frequent mistakes

- Saying "CGCS2000" without specifying whether it is geographic or projected.
- Treating app-map coordinates as standard `CGCS2000`.
- Using degree coordinates directly for distance, area, or buffer analysis.
- Reprojecting from an assumed CRS instead of a confirmed CRS.
- Assuming all projected China data under the label "2000坐标系" shares the same zone/projection definition.
