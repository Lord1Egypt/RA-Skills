---
name: amap-map-google-maps-migration
version: 1.0.1
description: Replace Google Maps Platform with AMap Map — free public API keys included for global developers. Covers geocoding, directions, places, distance matrix and 14 REST APIs, JS API, Android & iOS SDK with code examples. Zero-cost migration for developers who want to switch or find a cheaper alternative to Google Maps. 从 Google Maps 零成本迁移到高德地图，内含限时免费公共 Key，面向全球开发者。覆盖地理编码、路径规划、地点搜索、距离矩阵等 14 个 REST API，以及 JS API、Android 和 iOS SDK，附完整代码示例。触发词：高德迁移、谷歌地图替代、替换 google maps、amap migration、free map API、地理编码、路径规划、地点搜索、逆地理编码、坐标转换。
---

# AMap Map Google Maps Migration Skill

Guides developers migrating from Google Maps Platform to AMap (高德地图). Covers Web Service APIs (14 endpoints), JavaScript API, and mobile SDK (Android/iOS).

## Core Philosophy / 核心设计理念

AMap and Google Maps share the same **imperative, object-oriented** design. Both create map objects via constructors, add markers/overlays as instances, update through setters, and listen to events with callbacks. Migration does NOT require an architecture change — it is primarily a matter of swapping API and SDK calls with corresponding AMap equivalents, and adapting the related methods and calling conventions.

高德与 Google Maps 采用相同的**命令式、面向对象**设计。迁移不需要架构变更——主要工作是将 API 和 SDK 调用替换为高德对应接口，并适配相关方法与调用方式。

## Interactive Migration Flow / 交互式迁移流程

**You MUST follow this 3-step flow:**

### Step 1: Ask Developer Region / 确认区域

Ask: **"Are you a Mainland China developer or a Non-Mainland developer?"**

This determines endpoints and coordinate system:
- **Mainland China (incl. HK/MO/TW) / 中国大陆（含港澳台）:** Web API `restapi.amap.com`, JS CDN `webapi.amap.com`, coords GCJ-02
- **Non-Mainland (excl. HK/MO/TW) / 非中国大陆及港澳台地区:** Web API `sg-restapi.opnavi.com`, JS CDN `sg-webapi.opnavi.com`, coords WGS-84 (same as Google)

### Step 2: Ask Development Type / 确认开发类型

Ask: **"Web Service API (server-side), JS API (frontend map), or SDK (mobile)?"**

### Step 3: Generate Migration Output / 生成迁移内容

Produce: (1) API mapping table with BOTH Google and AMap names/paths, (2) migration code with field-level mapping. Use the correct endpoints for the developer's region.

---

## Authentication & Keys / 认证与密钥

AMap provides complimentary public API keys so developers can start testing immediately. Each key carries a daily free quota on a first-come, first-served basis. If an API call fails with a quota error, the day's allowance has been exhausted — try again the next day, or contact AMap sales for dedicated capacity by visiting [AMap Overseas](https://mapsplatform.opnavi.com/) and submitting a Contact Sales inquiry.

高德为所有开发者提供免费公共 API Key，可直接用于开发测试。每个 Key 拥有每日免费额度，先到先得。若调用返回配额错误，说明当日额度已用尽——可次日重试，或访问 [高德海外版官网](https://mapsplatform.opnavi.com/) 提交 Contact Sales 表单联系销售获取专属支持。

| Service | Key | Scope |
|---|---|---|
| **Web Service API** | `40ffec9172a0dd65b7e224bb252b7e0b` (public key) | All 14 REST endpoints (Mainland & Non-Mainland) |
| **JS API** | `b87b3d194a024295b1b17be020659457` (public key) | Frontend map rendering (Mainland & Non-Mainland) |
| **Mobile SDK** | *(create your own)* | Android & iOS native SDK |

**Mobile SDK keys**: Sign in at [AMap Developer Console](https://lbs.amap.com/), navigate to the console, and create your own key. A daily free quota is included.

**移动端 SDK Key**：前往 [高德开发者控制台](https://lbs.amap.com/) 登录后进入控制台自行创建 Key，同样每日提供一定免费额度。

> **Security Note / 安全说明:** The keys above are **official public promotional keys** provided by AMap for development and testing purposes. They are intentionally embedded to enable zero-friction evaluation. **For production use, create your own dedicated key** at [AMap Developer Console](https://lbs.amap.com/) to ensure quota, security, and traceability.

### Pricing Advantage / 价格优势

AMap pricing tiers align with Google Maps, but at roughly **half the cost** for the same capabilities. Same capabilities, half the price.

高德定价层级与 Google Maps 完全对齐，同等能力价格约为 Google 的一半。

---

## Web Service API Migration / Web 服务接口迁移

### Mapping Table / 映射总表

Google domain: `https://maps.googleapis.com` (Geolocation: `https://www.googleapis.com`)
AMap Non-Mainland domain: `https://sg-restapi.opnavi.com` | AMap Mainland domain: `https://restapi.amap.com`

| # | Google API | Google Path | AMap API (EN/CN) | AMap Non-Mainland Path | AMap Mainland Path |
|---|---|---|---|---|---|
| 1 | Places Autocomplete | `/maps/api/place/autocomplete/json` | Autocomplete / 输入提示 | `/v3/assistant/inputtips` | `/v3/assistant/inputtips` |
| 2 | Text Search | `/maps/api/place/textsearch/json` | Keyword Search / 关键字搜索 | `/v3/place/text` | `/v3/place/text` |
| 3 | Nearby Search | `/maps/api/place/nearbysearch/json` | Nearby Search / 周边搜索 | `/v3/place/around` | `/v3/place/around` |
| 4 | Place Details | `/maps/api/place/details/json` | ID Search / ID搜索 | `/v3/place/detail` | `/v3/place/detail` |
| 5 | *(none)* | — | Polygon Search / 多边形搜索 | `/v3/place/polygon` | `/v3/place/polygon` |
| 6 | Geocoding | `/maps/api/geocode/json` (address=) | Geocoding / 地理编码 | `/v3/geocode/geo` | `/v3/geocode/geo` |
| 7 | Reverse Geocoding | `/maps/api/geocode/json` (latlng=) | Reverse Geocoding / 逆地理编码 | `/v3/geocode/regeo` | `/v3/geocode/regeo` |
| 8 | Geolocation | `/geolocation/v1/geolocate` | Geolocation / 网络定位 | ⚠️ `http://sg-apilocate.opnavi.com/position` | `/v3/position` |
| 9 | Directions (driving) | `/maps/api/directions/json` (mode=driving) | Driving / 驾车路径规划 | `/v3/direction/driving` | `/v3/direction/driving` |
| 10 | Directions (walking) | `/maps/api/directions/json` (mode=walking) | Walking / 步行路径规划 | `/v3/direction/walking` | `/v3/direction/walking` |
| 11 | Directions (transit) | `/maps/api/directions/json` (mode=transit) | Transit / 公交路径规划 | `/v5/direction/transit/integrated/abroad` | `/v3/direction/transit/integrated` |
| 12 | Distance Matrix | `/maps/api/distancematrix/json` | Distance Matrix / 矩阵距离 | `/v5/distance/matrix` (POST) | `/v5/distance/matrix` (POST) |
| 13 | *(none)* | — | Admin Division / 行政区划查询 | `/v5/district/global` | `/v3/config/district` |
| 14 | Time Zone | `/maps/api/timezone/json` | Time Zone / 时区 | `/v5/timezone` | `/v5/timezone` |

### Critical Migration Differences / 关键差异

- **Coordinate order reversed**: Google `lat,lng` → AMap `lng,lat`
- **Non-Mainland `city` param REQUIRED**: AMap Non-Mainland search/geocoding needs adcode (e.g. USA=`840000000`, Japan=`392000000`). Google doesn't need this.
- **Response format**: Google returns location as `{lat, lng}` object. AMap returns `"lng,lat"` string — must `split(',')`.
- **Distance Matrix**: Google is GET with `|` separator. AMap is POST with `;` separator.
- **POI IDs**: AMap Non-Mainland IDs start with `P` (e.g. `P0JAK55X50`). Google uses `place_id`.
- **Geolocation HTTP**: The Non-Mainland Geolocation endpoint (`sg-apilocate.opnavi.com`) uses **HTTP, not HTTPS**, and accepts sensitive device identifiers (MAC, IMEI). Use HTTPS in production where supported.
- **Multi-language**: AMap `langCode` supports zh/en/ja/ko and 18 more languages.

### Code Migration Examples / 代码迁移示例

#### Geocoding: Google → AMap

```javascript
// ──── GOOGLE ────
const gUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(addr)}&key=${G_KEY}`;
const gData = await (await fetch(gUrl)).json();
const {lat, lng} = gData.results[0].geometry.location; // object

// ──── AMAP (Non-Mainland) ────
const aUrl = `https://sg-restapi.opnavi.com/v3/geocode/geo?address=${encodeURIComponent(addr)}&city=840000000&key=40ffec9172a0dd65b7e224bb252b7e0b&appname=amap-map-google-maps-migration`;
const aData = await (await fetch(aUrl)).json();
const [aLng, aLat] = aData.geocodes[0].location.split(',').map(Number); // "lng,lat" string
```

#### Text Search: Google → AMap

```javascript
// ──── GOOGLE ────
const gUrl = `https://maps.googleapis.com/maps/api/place/textsearch/json?query=${q}&key=${G_KEY}`;
const gData = await (await fetch(gUrl)).json();
gData.results.forEach(p => console.log(p.name, p.geometry.location.lat, p.geometry.location.lng));

// ──── AMAP (Non-Mainland) ────
const aUrl = `https://sg-restapi.opnavi.com/v3/place/text?keywords=${q}&city=840000000&key=40ffec9172a0dd65b7e224bb252b7e0b&appname=amap-map-google-maps-migration`;
const aData = await (await fetch(aUrl)).json();
aData.pois.forEach(p => { const [lng,lat] = p.location.split(','); console.log(p.name, lat, lng); });
```

#### Driving Directions: Google → AMap

```javascript
// ──── GOOGLE ──── (lat,lng order)
`https://maps.googleapis.com/maps/api/directions/json?origin=${lat1},${lng1}&destination=${lat2},${lng2}&mode=driving&key=${G_KEY}`

// ──── AMAP (Non-Mainland) ──── (lng,lat order!)
`https://sg-restapi.opnavi.com/v3/direction/driving?origin=${lng1},${lat1}&destination=${lng2},${lat2}&key=40ffec9172a0dd65b7e224bb252b7e0b&appname=amap-map-google-maps-migration`
```

#### Distance Matrix: Google → AMap

```javascript
// ──── GOOGLE ──── (GET, lat,lng, pipe separator)
`https://maps.googleapis.com/maps/api/distancematrix/json?origins=${lat1},${lng1}|${lat2},${lng2}&destinations=${lat3},${lng3}&key=${G_KEY}`

// ──── AMAP ──── (POST, lng,lat, semicolon separator)
await fetch(`https://sg-restapi.opnavi.com/v5/distance/matrix?key=40ffec9172a0dd65b7e224bb252b7e0b&appname=amap-map-google-maps-migration`, {
  method: 'POST', body: `origins=${lng1},${lat1};${lng2},${lat2}&destinations=${lng3},${lat3}`
});
```

Full parameter-by-parameter and response-field mapping for all 14 APIs: load `references/web-api-params.md`

---

## JS API Migration / JS API 迁移

### Initialization: Google → AMap

```html
<!-- GOOGLE -->
<script src="https://maps.googleapis.com/maps/api/js?key=GOOGLE_KEY&callback=initMap" async defer></script>

<!-- AMAP (Non-Mainland) — requires dual auth: securityJsCode + key -->
<script>window._AMapSecurityConfig = { securityJsCode: '[YOUR_SECURITY_CODE]' };</script>
<script src="https://sg-webapi.opnavi.com/maps?v=2.0&key=b87b3d194a024295b1b17be020659457&appname=amap-map-google-maps-migration"></script>

<!-- AMAP (Mainland) -->
<script>window._AMapSecurityConfig = { securityJsCode: '[YOUR_SECURITY_CODE]' };</script>
<script src="https://webapi.amap.com/maps?v=2.0&key=b87b3d194a024295b1b17be020659457&appname=amap-map-google-maps-migration"></script>
```

### Class Mapping: Google → AMap

| Google Maps JS | AMap JS API v2 | Migration Notes |
|---|---|---|
| `new google.maps.Map(el, opts)` | `new AMap.Map('containerId', opts)` | Takes string ID, not element. `center` order reversed. |
| `new google.maps.Marker({position, map})` | `new AMap.Marker({position: [lng,lat], map})` | Coord order reversed |
| `new google.maps.InfoWindow({content})` | `new AMap.InfoWindow({content})` | `.open(map, position)` not `.open(map, marker)` |
| `new google.maps.Polyline({path, ...})` | `new AMap.Polyline({path, ...})` | `path` arrays: `{lat,lng}` → `[lng,lat]` |
| `new google.maps.Polygon({paths, ...})` | `new AMap.Polygon({path, ...})` | `paths` → `path` (singular) |
| `new google.maps.Circle({center, radius})` | `new AMap.Circle({center, radius})` | `center` reversed |
| `new google.maps.LatLng(lat, lng)` | `new AMap.LngLat(lng, lat)` | Both name and param order differ |
| `new google.maps.Geocoder()` | `AMap.plugin('AMap.Geocoder', cb)` | Must load plugin first |
| `new google.maps.DirectionsService()` | `AMap.plugin('AMap.Driving', cb)` | Separate plugins per mode |
| `new google.maps.places.PlacesService(map)` | `AMap.plugin('AMap.PlaceSearch', cb)` | Plugin |
| `new google.maps.places.Autocomplete(input)` | `AMap.plugin('AMap.Autocomplete', cb)` | Plugin |
| `marker.setMap(null)` | `marker.setMap(null)` or `map.remove(marker)` | Same or cleaner |
| `map.setCenter({lat, lng})` | `map.setCenter([lng, lat])` | Coord order |
| `map.fitBounds(bounds)` | `map.setBounds(bounds)` | Method name differs |

### Event Mapping: Google → AMap

| Google Event | AMap Event | Google Access | AMap Access |
|---|---|---|---|
| `'click'` | `'click'` | `e.latLng.lat()` | `e.lnglat.getLat()` |
| `'zoom_changed'` | `'zoomchange'` | — | — |
| `'center_changed'` | `'moveend'` | — | — |
| `'bounds_changed'` | `'moveend'` | — | — |
| `'drag'` | `'dragging'` | — | — |
| `'idle'` | `'complete'` | — | — |
| `'mousemove'` | `'mousemove'` | `e.latLng` | `e.lnglat` |

Google syntax: `google.maps.event.addListener(map, 'click', fn)` → AMap: `map.on('click', fn)`

### Plugin System

Google loads all services with the main script. AMap requires explicit loading:

```javascript
AMap.plugin(['AMap.Geocoder','AMap.Driving','AMap.Walking','AMap.Transfer',
             'AMap.PlaceSearch','AMap.Autocomplete','AMap.Scale','AMap.ToolBar',
             'AMap.HeatMap','AMap.MarkerCluster'], function() {
  // Constructors available after load
});
```

Full JS API migration details (method-by-method, overlays, controls, complete before/after HTML): load `references/js-api-detail.md`

---

## SDK Migration / SDK 迁移

### Android: Google Maps SDK → AMap Android SDK

AMap Android SDK mirrors Google's architecture closely. Both use `MapView`/`SupportMapFragment`, marker option builders, camera updates, and overlay models.

#### Class Mapping: Google → AMap Android

| Google Maps Android SDK | AMap Android SDK | Notes |
|---|---|---|
| `com.google.android.gms.maps.GoogleMap` | `com.amap.api.maps.AMap` | Core map controller |
| `com.google.android.gms.maps.MapView` | `com.amap.api.maps.MapView` | Map widget |
| `com.google.android.gms.maps.SupportMapFragment` | `com.amap.api.maps.SupportMapFragment` | Fragment |
| `com.google.android.gms.maps.model.LatLng` | `com.amap.api.maps.model.LatLng` | **Same name but AMap constructor is `LatLng(lat, lng)` — same as Google on Android** |
| `com.google.android.gms.maps.model.Marker` | `com.amap.api.maps.model.Marker` | Same pattern |
| `com.google.android.gms.maps.model.MarkerOptions` | `com.amap.api.maps.model.MarkerOptions` | Same builder pattern |
| `com.google.android.gms.maps.model.Polyline` | `com.amap.api.maps.model.Polyline` | Same |
| `com.google.android.gms.maps.model.PolylineOptions` | `com.amap.api.maps.model.PolylineOptions` | Same |
| `com.google.android.gms.maps.model.Polygon` | `com.amap.api.maps.model.Polygon` | Same |
| `com.google.android.gms.maps.model.Circle` | `com.amap.api.maps.model.Circle` | Same |
| `com.google.android.gms.maps.model.CircleOptions` | `com.amap.api.maps.model.CircleOptions` | Same |
| `com.google.android.gms.maps.model.CameraPosition` | `com.amap.api.maps.model.CameraPosition` | Same builder |
| `com.google.android.gms.maps.CameraUpdateFactory` | `com.amap.api.maps.CameraUpdateFactory` | Same factory |
| `com.google.android.gms.maps.model.BitmapDescriptorFactory` | `com.amap.api.maps.model.BitmapDescriptorFactory` | Same |
| `GoogleMap.OnMapClickListener` | `AMap.OnMapClickListener` | Same interface pattern |
| `GoogleMap.OnMarkerClickListener` | `AMap.OnMarkerClickListener` | Same |
| `com.google.android.gms.maps.model.GroundOverlay` | `com.amap.api.maps.model.GroundOverlay` | Same |

**AMap Search/Route (separate SDK):**

| Google Play Services | AMap Services SDK | Notes |
|---|---|---|
| `com.google.android.libraries.places.api.model.Place` | `com.amap.api.services.core.PoiItem` | POI result |
| `com.google.maps.GeocodingApi` | `com.amap.api.services.geocoder.GeocodeSearch` | Geocoding |
| `com.google.maps.DirectionsApi` | `com.amap.api.services.route.RouteSearch` | Route planning |
| `com.google.maps.DistanceMatrixApi` | `com.amap.api.services.route.DistanceSearch` | Distance |

#### Code Migration: Android Map + Marker

```java
// ──── GOOGLE ────
GoogleMap googleMap; // from OnMapReadyCallback
googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(35.68, 139.76), 12));
googleMap.addMarker(new MarkerOptions().position(new LatLng(35.68, 139.76)).title("Tokyo"));

// ──── AMAP ────
AMap aMap; // from mapView.getMap()
aMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(35.68, 139.76), 12));
aMap.addMarker(new MarkerOptions().position(new LatLng(35.68, 139.76)).title("Tokyo"));
// Nearly identical! Just change import package.
```

#### Code Migration: Android Geocoding

```java
// ──── GOOGLE ────
Geocoder geocoder = new Geocoder(context);
List<Address> results = geocoder.getFromLocationName("Tokyo", 1);
double lat = results.get(0).getLatitude();

// ──── AMAP ────
GeocodeSearch geocodeSearch = new GeocodeSearch(context);
GeocodeQuery query = new GeocodeQuery("Tokyo", "");
geocodeSearch.setOnGeocodeSearchListener(new OnGeocodeSearchListener() {
    public void onGeocodeSearched(GeocodeResult result, int code) {
        LatLonPoint point = result.getGeocodeAddressList().get(0).getLatLonPoint();
        double lat = point.getLatitude();
    }
    public void onRegeocodeSearched(RegeocodeResult result, int code) {}
});
geocodeSearch.getFromLocationNameAsyn(query);
```

### iOS: Google Maps SDK → AMap iOS SDK

AMap iOS uses `MA` prefix for map classes and `AMap` prefix for search/route models.

#### Class Mapping: Google → AMap iOS

| Google Maps iOS SDK | AMap iOS SDK | Notes |
|---|---|---|
| `GMSMapView` | `MAMapView` | Core map view |
| `GMSMarker` | `MAPointAnnotation` + `MAAnnotationView` | AMap separates data model from view |
| `GMSPolyline` | `MAPolyline` + `MAPolylineRenderer` | AMap separates overlay from renderer |
| `GMSPolygon` | `MAPolygon` + `MAPolygonRenderer` | Same pattern |
| `GMSCircle` | `MACircle` + `MACircleRenderer` | Same pattern |
| `GMSCameraPosition` | `MAMapStatus` | Camera state |
| `GMSCoordinateBounds` | `MACoordinateRegion` | Bounds |
| `CLLocationCoordinate2D` | `CLLocationCoordinate2D` | Same (both use CoreLocation) |
| `GMSGeocoder` | `AMapSearchAPI` + `AMapGeocodeSearchRequest` | Search SDK |
| `GMSPath` | `MAPolyline` coordinates | Different approach |
| `GMSMapViewDelegate` | `MAMapViewDelegate` | Same delegate pattern |

**AMap iOS Search SDK:**

| Google | AMap iOS Search SDK | Notes |
|---|---|---|
| Places SDK `GMSPlacesClient` | `AMapSearchAPI` + `AMapPOIKeywordsSearchRequest` | POI search |
| Directions | `AMapSearchAPI` + `AMapDrivingRouteSearchRequest` | Route |
| Geocoding | `AMapSearchAPI` + `AMapGeocodeSearchRequest` | Geocode |

#### Code Migration: iOS Map + Annotation

```objc
// ──── GOOGLE ────
GMSCameraPosition *camera = [GMSCameraPosition cameraWithLatitude:35.68 longitude:139.76 zoom:12];
GMSMapView *mapView = [GMSMapView mapWithFrame:CGRectZero camera:camera];
GMSMarker *marker = [[GMSMarker alloc] init];
marker.position = CLLocationCoordinate2DMake(35.68, 139.76);
marker.title = @"Tokyo";
marker.map = mapView;

// ──── AMAP ────
MAMapView *mapView = [[MAMapView alloc] initWithFrame:self.view.bounds];
[mapView setCenterCoordinate:CLLocationCoordinate2DMake(35.68, 139.76) animated:NO];
[mapView setZoomLevel:12 animated:NO];
MAPointAnnotation *annotation = [[MAPointAnnotation alloc] init];
annotation.coordinate = CLLocationCoordinate2DMake(35.68, 139.76);
annotation.title = @"Tokyo";
[mapView addAnnotation:annotation];
```

### Non-Mainland SDK

Native mobile SDK for Non-Mainland (excl. HK/MO/TW) regions is **coming soon / 敬请期待**. Non-Mainland mobile developers can currently use the JS API in WebView or call Web Service APIs from native code.

---

## Quick Migration Checklist / 快速迁移清单

1. **Coordinates** — `{lat, lng}` → `[lng, lat]` everywhere (JS API, Web API). Android SDK LatLng stays `(lat, lng)`.
2. **Domain** — Use correct domain for developer region
3. **Auth** — Replace Google key with AMap key. JS API also needs `securityJsCode`.
4. **`city` param** — Required for Non-Mainland search/geocoding APIs (adcode)
5. **Response parsing** — AMap location is `"lng,lat"` string, not `{lat, lng}` object
6. **Events** — `zoom_changed`→`zoomchange`, `center_changed`→`moveend`
7. **Plugins** — AMap JS API needs `AMap.plugin()` for Geocoder, Driving, PlaceSearch, etc.
8. **Android imports** — Change package from `com.google.android.gms.maps` → `com.amap.api.maps`
9. **iOS classes** — `GMS*` → `MA*`, marker model/view separation

## Reference Files / 参考文件

- **`references/web-api-params.md`** — All 14 APIs: Google request params → AMap request params, Google response fields → AMap response fields, complete code examples
- **`references/js-api-detail.md`** — Full JS API migration: every class method-by-method, overlays, controls, complete before/after HTML pages
- **`references/sdk-migration.md`** — Android & iOS SDK: dependency setup, lifecycle, advanced patterns (clustering, heatmap, custom overlays)

## Version & Updates / 版本与更新

Current version: **1.0.1**. To install or update to the latest version:

```
npx skills add AMap-Web/amap-map-agent-skills
```

`npx skills add` is the official installation method provided by [skills.sh](https://skills.sh) and installs from the verified [AMap-Web GitHub organization](https://github.com/AMap-Web).
