# Web Service API: Google → AMap Complete Parameter & Response Mapping

Every API below shows: Google request → AMap request (param-by-param), Google response → AMap response (field-by-field), and working code.

AMap Non-Mainland domain: `https://sg-restapi.opnavi.com` | Mainland: `https://restapi.amap.com`
Google domain: `https://maps.googleapis.com`

---

## 1. Autocomplete / Places Autocomplete → 输入提示

**Google:** `GET /maps/api/place/autocomplete/json`
**AMap:** `GET /v3/assistant/inputtips`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | Swap key value |
| `input` | `keywords` | Rename |
| `location` (lat,lng) | `location` (lng,lat) | Reversed |
| `radius` | *(use city/adcode)* | AMap uses city-based scoping |
| `types` | `type` | AMap uses its own POI typecodes |
| `language` | `langCode` | zh/en/ja/ko etc. |
| — | `city` | **Required for Non-Mainland**, adcode |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `predictions[]` | `tips[]` | Array name differs |
| `prediction.description` | `tip.name` + `tip.district` | Combine for full description |
| `prediction.place_id` | `tip.id` | Non-Mainland IDs start with `P` |
| `prediction.structured_formatting.main_text` | `tip.name` | Direct |
| — | `tip.location` | `"lng,lat"` string |
| — | `tip.adcode` | Region code |

### Example

```javascript
// Google
`https://maps.googleapis.com/maps/api/place/autocomplete/json?input=starbucks&key=${G_KEY}`

// AMap (Non-Mainland)
`https://sg-restapi.opnavi.com/v3/assistant/inputtips?keywords=starbucks&city=840000000&key=40ffec9172a0dd65b7e224bb252b7e0b&appname=amap-map-google-maps-migration`
```

---

## 2. Text Search / Keyword Search → 关键字搜索

**Google:** `GET /maps/api/place/textsearch/json`
**AMap:** `GET /v3/place/text`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `query` | `keywords` | Rename |
| `location` (lat,lng) | *(not used)* | AMap uses `city` scoping |
| `radius` | *(not used)* | — |
| `type` | `types` | AMap POI typecodes, `\|` separated |
| `pagetoken` | `page` + `offset` | AMap: `page`=page number, `offset`=per page (max 50) |
| `language` | `langCode` | — |
| — | `city` | **Required for Non-Mainland** |
| — | `extensions` | `base` or `all` |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `results[]` | `pois[]` | — |
| `result.name` | `poi.name` | Direct |
| `result.formatted_address` | `poi.address` | Direct |
| `result.geometry.location.lat` | `poi.location.split(',')[1]` | String parse |
| `result.geometry.location.lng` | `poi.location.split(',')[0]` | String parse |
| `result.place_id` | `poi.id` | `P`-prefix Non-Mainland |
| `result.types[]` | `poi.type` / `poi.typecode` | Different classification |
| `result.rating` | *(not available)* | — |
| `result.opening_hours` | *(not available)* | — |
| — | `poi.tel` | Phone number |
| — | `poi.pname` / `poi.cityname` / `poi.adname` | Region hierarchy |

---

## 3. Nearby Search → 周边搜索

**Google:** `GET /maps/api/place/nearbysearch/json`
**AMap:** `GET /v3/place/around`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `location` (lat,lng) | `location` (lng,lat) | **Reversed** |
| `radius` (meters) | `radius` (meters, 0-50000) | Same unit |
| `keyword` | `keywords` | Rename |
| `type` | `types` | AMap typecodes |
| `pagetoken` | `page` + `offset` | — |

### Response Fields

Same as Keyword Search (#2). Plus `poi.distance` (meters from center) is populated.

---

## 4. Place Details / ID Search → ID搜索

**Google:** `GET /maps/api/place/details/json`
**AMap:** `GET /v3/place/detail`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `place_id` | `id` | AMap Non-Mainland IDs: `P0JAK55X50` format |
| `fields` | *(not needed)* | AMap returns full POI |
| `language` | *(not available)* | — |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `result.name` | `pois[0].name` | AMap wraps in array |
| `result.formatted_address` | `pois[0].address` | — |
| `result.geometry.location` | `pois[0].location` | `"lng,lat"` string |
| `result.formatted_phone_number` | `pois[0].tel` | — |
| `result.types` | `pois[0].type` | — |
| `result.rating` | *(not available)* | — |
| `result.reviews` | *(not available)* | — |

---

## 5. Polygon Search → 多边形搜索

**Google:** *(No direct equivalent — Google requires Nearby Search with custom client-side filtering)*
**AMap:** `GET /v3/place/polygon`

AMap-specific. `polygon` param: `lng,lat|lng,lat|...` (first & last must match, or 2 corners for rectangle). Plus `keywords` or `types`.

---

## 6. Geocoding → 地理编码

**Google:** `GET /maps/api/geocode/json` (with `address=`)
**AMap:** `GET /v3/geocode/geo`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `address` | `address` | Non-Mainland: low-level first ("9 Madison Ave, NY, USA") |
| `components` | `city` | AMap uses adcode instead of component filtering |
| `language` | *(not available)* | — |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `results[]` | `geocodes[]` | — |
| `result.geometry.location.lat` | `geocode.location.split(',')[1]` | String parse |
| `result.geometry.location.lng` | `geocode.location.split(',')[0]` | String parse |
| `result.formatted_address` | Concat: `country+province+city+district+street+number` | AMap returns flat fields |
| `result.address_components[].long_name` | `geocode.country/province/city/district/street/number` | Flat, not array |
| `result.place_id` | *(not returned)* | — |

---

## 7. Reverse Geocoding → 逆地理编码

**Google:** `GET /maps/api/geocode/json` (with `latlng=`)
**AMap:** `GET /v3/geocode/regeo`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `latlng` (lat,lng) | `location` (lng,lat) | **Reversed** |
| `result_type` | `poitype` | Filter POI types (requires `extensions=all`) |
| `language` | `langCode` | 20+ languages |
| — | `radius` | 0-3000m, default 1000 |
| — | `extensions` | `base` or `all` (all includes nearby POIs, roads) |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `results[0].formatted_address` | `regeocode.formatted_address` | Direct |
| `results[0].address_components[]` | `regeocode.addressComponent` | Object with country/province/city/district/township |
| `results[0].geometry.location` | Request `location` param | Not re-returned |
| — | `regeocode.pois[]` | Nearby POIs (when extensions=all) |

---

## 8. Geolocation → 网络定位

**Google:** `POST https://www.googleapis.com/geolocation/v1/geolocate`
**AMap Non-Mainland:** `GET http://sg-apilocate.opnavi.com/position` ⚠️ HTTP only — use HTTPS in production where supported / 生产环境建议使用 HTTPS
**AMap Mainland:** `GET https://restapi.amap.com/v3/position`

| Google Param | AMap Param | Notes |
|---|---|---|
| `wifiAccessPoints[]` | `macs` | WiFi MAC addresses |
| `cellTowers[]` | `bts` / `nearbts` | Cell tower info |
| — | `accesstype` | 0=mobile, 1=wifi |
| — | `imei` | Device IMEI |

Both return lat/lng position. AMap for IoT hardware positioning.

---

## 9. Driving Directions → 驾车路径规划

**Google:** `GET /maps/api/directions/json` (mode=driving)
**AMap:** `GET /v3/direction/driving`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `origin` (lat,lng) | `origin` (lng,lat) | **Reversed** |
| `destination` (lat,lng) | `destination` (lng,lat) | **Reversed** |
| `waypoints` (lat,lng\|...) | `waypoints` (lng,lat;...) | Reversed + `;` separator, max 16 |
| `avoid=tolls` | `strategy=14` | Strategy number |
| `avoid=highways` | `strategy=13` | Strategy number |
| `alternatives=true` | `strategy=10` (or 11-20) | Multi-route strategies |
| `language` | `langCode` | zh / en |
| — | `origin_id` / `destination_id` | POI ID for accuracy |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `routes[].legs[].distance.value` | `route.paths[].distance` | Meters |
| `routes[].legs[].duration.value` | `route.paths[].duration` | Seconds |
| `routes[].legs[].steps[]` | `route.paths[].steps[]` | Turn-by-turn |
| `step.html_instructions` | `step.instruction` | Instruction text |
| `step.distance.value` | `step.distance` | Meters |
| `step.polyline.points` | `step.polyline` | Encoded polyline |

---

## 10. Walking Directions → 步行路径规划

**Google:** `GET /maps/api/directions/json` (mode=walking)
**AMap:** `GET /v3/direction/walking`

Same param pattern as Driving (#9) but without `strategy`/`waypoints`. Response structure matches driving.

---

## 11. Transit Directions → 公交路径规划

**Google:** `GET /maps/api/directions/json` (mode=transit)
**AMap Non-Mainland:** `GET /v5/direction/transit/integrated/abroad`
**AMap Mainland:** `GET /v3/direction/transit/integrated`

### Extra AMap Params (vs Google)

| Google Param | AMap Param | Notes |
|---|---|---|
| `departure_time` | `date` + `time` | AMap uses separate date (`YYYY-MM-DD`) and time (`HH:MM`) |
| `transit_mode` | `strategy` | 0=fastest, 1=cheapest, 2=fewest transfers, 3=least walking, 5=no subway |
| — | `city` / `cityd` | Required for cross-city transit |
| — | `nightflag` | 0=no night bus, 1=include |

Non-Mainland transit coverage: USA, Japan, South Korea, UK, Singapore, Canada + 11 more countries.

---

## 12. Distance Matrix → 矩阵距离测量

**Google:** `GET /maps/api/distancematrix/json`
**AMap:** `POST /v5/distance/matrix`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `origins` (lat,lng\|lat,lng) | `origins` (lng,lat;lng,lat) | **Reversed + `;` separator**, max 25 |
| `destinations` (lat,lng\|lat,lng) | `destinations` (lng,lat;lng,lat) | **Reversed + `;` separator**, max 25 |
| `mode` | `travelMode` | `Drive` (default) |
| `departure_time` | `departureTime` | Unix timestamp (seconds), future only, max 7 days |
| — | `routingPreference` | 1=speed priority |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `rows[i].elements[j].distance.value` | `routes[].route[].distanceMeters` | Meters |
| `rows[i].elements[j].duration.value` | `routes[].route[].duration` | Seconds |
| `rows[i].elements[j].status` | `routes[].route[].status` | 0=OK, 1=distance limit, 2=timeout |
| — | `routes[].route[].originIndex` | Origin index (1-25) |
| — | `routes[].route[].destinationIndex` | Destination index (1-25) |

---

## 13. Admin Division → 行政区划查询

**Google:** *(No equivalent)*
**AMap Non-Mainland:** `GET /v5/district/global`
**AMap Mainland:** `GET /v3/config/district`

Params: `keywords` (region name or adcode), `subdistrict` (0,1,2... sub-levels), `langCode`, `page`, `offset`.
Response: `districts[]` → `{adcode, name, center, level, districts[]}`. Levels: 1=country, 2=province/state, 3=city, 4=district.

---

## 14. Time Zone → 时区

**Google:** `GET /maps/api/timezone/json`
**AMap:** `GET /v5/timezone`

### Request Params

| Google Param | AMap Param | Notes |
|---|---|---|
| `key` | `key` | — |
| `location` (lat,lng) | `location` (lng,lat) | **Reversed** |
| `timestamp` (Unix seconds) | `time` (Unix when time_type=1) | Same value |
| — | `time_type` | 1=UTC input (default), 2=local time input |

### Response Fields

| Google Field | AMap Field | Notes |
|---|---|---|
| `timeZoneId` | `time_zone_id` | e.g. `America/New_York` |
| `timeZoneName` | *(not returned)* | — |
| `rawOffset` (seconds) | `rawoffset` (seconds) | Same |
| `dstOffset` (seconds) | `dstoffset` (seconds) | Same |
| — | `time` | Converted time output |
