# Preprocessing (GDAL / QGIS)

Do heavy GIS **before** Remotion / bake / Three — not inside the render loop.

| Tool | Use |
| --- | --- |
| GDAL (`gdalwarp`, `gdal_translate`) | DEM crop, resample, format |
| PROJ | CRS |
| QGIS | Inspect, extract |
| osmium / osmconvert (optional) | OSM PBF by bbox |
| Tippecanoe (optional) | Vector tiles |

## DEM

1. Fetch Copernicus DEM for the shot `bbox` (or local cache hit).
2. Crop / resample with `gdalwarp`.
3. Export what Three / terrain needs; record Z scale in `manifest`.

## Vectors

1. Subset Natural Earth / Hydro* / Geofabrik for the extent.
2. Emit WGS84 GeoJSON (or project format).
3. Simplify routes with Turf when needed; record tolerance in `manifest`.

## Forbidden

- Heavy GIS inside Remotion / HF frame loops
- Mixing CRS without recording them
- Dropping uncropped national PBFs into the work repo
