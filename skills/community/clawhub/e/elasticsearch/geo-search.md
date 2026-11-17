# Geo Search — Points, Shapes, Distance, and the Ordering Trap

## The Coordinate Order Trap

`geo_point` accepts several input formats and **they do not agree on order**:

| Format | Example | Order |
|---|---|---|
| Object | `{"lat": 41.38, "lon": 2.17}` | Named, unambiguous |
| String | `"41.38,2.17"` | **lat, lon** |
| Array | `[2.17, 41.38]` | **lon, lat** (GeoJSON convention) |
| WKT | `"POINT (2.17 41.38)"` | **lon, lat** |
| Geohash | `"sp3e3"` | n/a |

The array and string forms are reversed relative to each other, and both index without complaint. Symptom: every result is in the wrong hemisphere, or distance filters return nothing near the user. **Use the object form everywhere** — it is the only one nobody can get backwards, and the extra bytes are irrelevant next to a silent correctness bug.

## `geo_point` vs `geo_shape` vs `point`

- `geo_point` — a single location. Supports distance, bounding-box, polygon-containment queries, distance sorting, and geo aggregations. Cheapest by a wide margin.
- `geo_shape` — lines, polygons, multipolygons, circles, and collections. Indexed as BKD trees on `elasticsearch >=7.0`, so accuracy is exact rather than the old prefix-tree approximation, and `precision`/`tree_levels` settings no longer exist.
- `point` / `shape` — the same two types on a **Cartesian** plane rather than a globe. For floor plans, game maps, CAD, and chip layouts: no great-circle math, no coordinate range validation.
- A document may hold an array of `geo_point` values (a delivery route, several store locations). Distance queries match if *any* point qualifies, and distance sorting picks the closest by default — set `mode: "max"` if you need the farthest.

## Queries

```json
{"bool": {"filter": [
  {"geo_distance": {"distance": "5km", "location": {"lat": 41.38, "lon": 2.17}}},
  {"geo_bounding_box": {"location": {
      "top_left": {"lat": 41.5, "lon": 2.0}, "bottom_right": {"lat": 41.3, "lon": 2.3}}}}
]}}
```

- All geo queries are filters: they contribute no score. Ranking by proximity is a separate concern (below).
- `geo_bounding_box` is substantially cheaper than `geo_distance` — a box is two range comparisons. When a map viewport is the actual constraint, a box is also the *correct* shape, not an approximation.
- `geo_distance` supports `distance_type: "arc"` (default, accurate) and `"plane"` (faster, degrades over long distances and near the poles). Plane is fine for city-scale radii.
- `geo_shape` query `relation`: `intersects` (default), `within`, `contains`, `disjoint`. Choosing `intersects` when you meant `within` returns every polygon that merely touches the boundary.
- `geo_polygon` was deprecated in 7.12 — use a `geo_shape` query with a polygon instead.
- Bounding boxes crossing the antimeridian (±180° longitude) work if you let longitude wrap (left > right); a box computed naively by subtracting degrees will be empty or span the whole globe.

## Sorting and Scoring by Distance

```json
"sort": [ {"_geo_distance": {"location": {"lat": 41.38, "lon": 2.17},
                             "order": "asc", "unit": "km", "distance_type": "arc"}} ]
```

- Sorting by distance discards relevance entirely. For "relevant AND nearby", score it instead: `distance_feature` on a `geo_point` with a `pivot` (the distance at which the boost halves), or a `gauss` decay in `function_score`.
- `_geo_distance` sorting returns the distance in the hit's `sort` array — use it rather than recomputing client-side, since it already accounts for the chosen `distance_type`.

## Geo Aggregations

- `geo_distance` agg — ranged rings around a point ("within 1km / 1-5km / 5km+"). Bucket counts, not documents.
- `geohash_grid` — buckets by geohash cell. `precision` 1-12; each level splits a cell into 32. Precision 5 is roughly 5 km, precision 7 roughly 150 m. Cells are rectangular in lat/lon space, so they are visibly distorted at high latitudes.
- `geotile_grid` — buckets by web-map tile (the same z/x/y a slippy map uses). The right choice for anything rendered on a Mercator map, because the buckets align with the tiles.
- `geohex_grid` (`elasticsearch >=8.1`) — H3 hexagons. Equal-area cells with uniform neighbour distance, which matters for density comparison and clustering.
- `geo_bounds` and `geo_centroid` — extent and weighted centre of a bucket. `geo_centroid` inside a `terms` agg gives one marker per category; combining it with `geotile_grid` is the standard server-side map-clustering pattern.
- Always pair a grid aggregation with a `geo_bounding_box` filter for the current viewport. Aggregating the whole planet to render one city is the usual cause of a slow map.

## Ingest and Data Quality

- `ignore_malformed: true` on a `geo_point` field keeps a document with a broken coordinate instead of rejecting it — the right posture for third-party feeds, wrong for your own writers, where the rejection is the signal.
- The `geoip` ingest processor turns an IP into a `geo_point` plus country and city fields at index time.
- Out-of-range coordinates are **rejected, not normalised**: a latitude of 120 throws `illegal_argument_exception` and the whole document fails to index. `geo_point` has no `coerce` parameter; `ignore_malformed: true` is the only switch, and it drops the field rather than fixing it. That rejection is the lucky case. The swap that stays invisible is the one where both numbers are legal: 41.38/2.17 reversed indexes as lat 2.17, lon 41.38 — a valid point in East Africa instead of Barcelona, no error, wrong hemisphere.
- Polygons must follow the right-hand rule for orientation on `geo_shape` when ambiguous; a reversed outer ring can be interpreted as "everything except this shape". Validate with a small `within` query against a point you know is inside.

## Sizing Notes

- `geo_point` costs about the same as two numeric fields; adding one to an existing index is cheap.
- `geo_shape` with complex polygons (thousands of vertices) is expensive to index and to query. Simplify geometry to the tolerance the use case actually needs — administrative boundaries at street precision are usually 10× more detail than any query resolves.
- Precomputing a coarse `geohash` `keyword` field alongside the point lets you use an ordinary `terms` aggregation for coarse clustering, which is cheaper than a grid aggregation when the resolution is fixed.
