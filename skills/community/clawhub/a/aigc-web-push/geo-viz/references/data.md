# Free-key data directory (global defaults)

No API Key / Token required for the default stack. Free-key ≠ unlimited: obey each license and ToS. Always fetch by bbox / region.

**Do not default to:** 天地图, 星图地球, MapTiler commercial keys, 高德 JS/Web keys.

## Basemap, imagery, terrain

| Need | Source | URL | How | Priority |
| --- | --- | --- | --- | --- |
| Global vector basemap | OpenFreeMap | https://openfreemap.org | Style URL / self-host | P0 |
| OSM extracts | Geofabrik | https://download.geofabrik.de | By country/region | P0 |
| OSM project | OpenStreetMap | https://www.openstreetmap.org | By extent | P0 |
| Overview imagery | NASA GIBS | https://earthdata.nasa.gov | Online tiles (not commercial HD substitute) | P1 |
| Terrain tiles | Mapterhorn | https://mapterhorn.com | Online / extract | P0 |
| DEM | Copernicus DEM GLO-30 | AWS Open Data | By bbox | P0 |
| DEM fallback | NASA SRTM | Earthdata Search | On demand (account may be required) | P2 |
| Bathymetry | GEBCO | https://www.gebco.net | By extent | P1 |
| Tools | GDAL / QGIS | gdal.org / qgis.org | Local | P0 |

Starter set: **OpenFreeMap + Mapterhorn + Copernicus DEM + Geofabrik (target region) + Natural Earth**.

OpenFreeMap MapLibre styles:

- `https://tiles.openfreemap.org/styles/liberty`
- `https://tiles.openfreemap.org/styles/positron`
- `https://tiles.openfreemap.org/styles/bright`

## Borders, roads, water, buildings

| Need | Source | URL | Priority |
| --- | --- | --- | --- |
| Borders / coasts | Natural Earth | https://www.naturalearthdata.com | P0 |
| Roads / rail | OSM / Geofabrik | download.geofabrik.de | P0 |
| Buildings | Overture Maps | https://overturemaps.org | P1 |
| Rivers | HydroRIVERS | https://www.hydrosheds.org | P0 |
| Basins | HydroBASINS | hydrosheds.org | P0 |
| Lakes | HydroLAKES | hydrosheds.org | P1 |
| Historical routes | Curated / verified | literature + public historical maps | P1 |

## Thematic (per film)

| Topic | Source | Priority |
| --- | --- | --- |
| Earthquakes | USGS | P1 |
| Climate | ERA5 / Copernicus CDS | P1 |
| Fires | NASA FIRMS public products | P1 |
| Population | WorldPop | P1 |
| Economy | World Bank Open Data | P1 |
| Weather / ocean | NOAA public | P1–P2 |

## 3D assets

| Need | Source | Note |
| --- | --- | --- |
| HDRI / materials | Poly Haven | Check license |
| Simple kits | Kenney | Check license |
| Format | glTF / GLB | Three / Cesium |
| Buildings | Extrude Overture / OSM | Prefer over random downloads |

Sketchfab is not a default dependency.
