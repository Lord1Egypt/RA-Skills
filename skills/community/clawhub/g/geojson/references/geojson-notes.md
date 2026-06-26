# GeoJSON Notes

Use this reference when the user needs concise reminders about GeoJSON structure or error patterns.

## Common top-level types

- `FeatureCollection`
- `Feature`
- Geometry objects such as `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`, `MultiPolygon`, `GeometryCollection`

## Common expectations

- `FeatureCollection.features` should be an array.
- `Feature.geometry` may be `null`, but that should be called out.
- Coordinates are arrays whose nesting depth depends on geometry type.
- Geographic coordinates are typically interpreted as `lon,lat`.

## Frequent mistakes

- Using `lat,lon` instead of `lon,lat`
- Invalid coordinate nesting for `Polygon` or `MultiPolygon`
- Missing `features` on a `FeatureCollection`
- Missing `type`
- Mixing geometry arrays and feature objects in the same array
- Assuming GeoJSON always carries a reliable CRS declaration

## CRS guidance

- In modern usage, GeoJSON is commonly exchanged as WGS84-style longitude/latitude.
- If the source CRS is uncertain, say so explicitly instead of inventing a CRS.
- If measurement accuracy matters, recommend reprojection before analysis.
