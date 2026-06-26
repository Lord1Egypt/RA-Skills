# SDK Migration: Google Maps → AMap — Android & iOS

## API Key / 获取 Key

The public Web/JS API keys in the main guide do not cover mobile SDK. To get an SDK key, sign in at [AMap Developer Console](https://lbs.amap.com/) (Chinese site), go to the console, and create your own key — a daily free quota is included. If the quota runs out, retry the next day or contact sales at [AMap Overseas](https://mapsplatform.opnavi.com/) for dedicated capacity.

主文档中的公共 Web/JS API Key 不适用于移动端 SDK。请前往 [高德开发者控制台](https://lbs.amap.com/) 登录后自行创建 Key，每日提供一定免费额度。若额度用尽可次日重试，或访问 [高德海外版官网](https://mapsplatform.opnavi.com/) 联系销售获取专属支持。

## Android SDK: Google → AMap

### Dependencies

```groovy
// ── GOOGLE (build.gradle) ──
implementation 'com.google.android.gms:play-services-maps:18.2.0'
implementation 'com.google.android.gms:play-services-location:21.0.1'

// ── AMAP (build.gradle) ──
implementation 'com.amap.api:3dmap:latest.integration'        // Map SDK
implementation 'com.amap.api:search:latest.integration'        // Search/Geocode/Route SDK
implementation 'com.amap.api:location:latest.integration'      // Location SDK
```

### Package Mapping

| Google Package | AMap Package |
|---|---|
| `com.google.android.gms.maps` | `com.amap.api.maps` |
| `com.google.android.gms.maps.model` | `com.amap.api.maps.model` |
| `com.google.android.gms.location` | `com.amap.api.location` |
| `com.google.android.libraries.places.api` | `com.amap.api.services.poisearch` |
| `com.google.maps` (server SDK) | `com.amap.api.services` |

### Core Class Mapping

| Google Class | AMap Class |
|---|---|
| `GoogleMap` | `AMap` |
| `MapView` | `MapView` |
| `SupportMapFragment` | `SupportMapFragment` |
| `OnMapReadyCallback` | `OnMapReadyCallback` |
| `LatLng(lat, lng)` | `LatLng(lat, lng)` — **Same order on Android!** |
| `LatLngBounds` | `LatLngBounds` |
| `CameraPosition` | `CameraPosition` |
| `CameraPosition.Builder` | `CameraPosition.Builder` |
| `CameraUpdateFactory` | `CameraUpdateFactory` |
| `CameraUpdate` | `CameraUpdate` |
| `BitmapDescriptorFactory` | `BitmapDescriptorFactory` |
| `Marker` | `Marker` |
| `MarkerOptions` | `MarkerOptions` |
| `Polyline` | `Polyline` |
| `PolylineOptions` | `PolylineOptions` |
| `Polygon` | `Polygon` |
| `PolygonOptions` | `PolygonOptions` |
| `Circle` | `Circle` |
| `CircleOptions` | `CircleOptions` |
| `GroundOverlay` | `GroundOverlay` |
| `TileOverlay` | `TileOverlay` |

### Listener Mapping

| Google Listener | AMap Listener |
|---|---|
| `GoogleMap.OnMapClickListener` | `AMap.OnMapClickListener` |
| `GoogleMap.OnMarkerClickListener` | `AMap.OnMarkerClickListener` |
| `GoogleMap.OnCameraIdleListener` | `AMap.OnCameraChangeListener` |
| `GoogleMap.OnMyLocationClickListener` | `AMap.OnMyLocationChangeListener` |
| `GoogleMap.InfoWindowAdapter` | `AMap.InfoWindowAdapter` |

### Search/Route Class Mapping

| Google | AMap | Notes |
|---|---|---|
| `Geocoder` | `GeocodeSearch` | `com.amap.api.services.geocoder` |
| `Address` | `GeocodeAddress` / `RegeocodeAddress` | — |
| *(Directions SDK)* | `RouteSearch` | `com.amap.api.services.route` |
| *(Directions result)* | `DriveRouteResult` / `WalkRouteResult` / `BusRouteResult` | Per mode |
| `PlacesClient` | `PoiSearch` | `com.amap.api.services.poisearch` |
| `Place` | `PoiItem` | — |
| *(Distance Matrix)* | `DistanceSearch` | `com.amap.api.services.route` |

### Code: Map Init

```java
// ── GOOGLE ──
public class MapsActivity extends AppCompatActivity implements OnMapReadyCallback {
    private GoogleMap mMap;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
            .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(35.68, 139.76), 12));
    }
}

// ── AMAP ──
public class MapsActivity extends AppCompatActivity implements OnMapReadyCallback {
    private AMap aMap;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
            .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }
    public void onMapReady(AMap map) {
        aMap = map;
        aMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(35.68, 139.76), 12));
        // Nearly identical! Just change GoogleMap→AMap, change imports.
    }
}
```

### Code: Markers

```java
// ── GOOGLE ──
mMap.addMarker(new MarkerOptions()
    .position(new LatLng(35.68, 139.76))
    .title("Tokyo")
    .snippet("Capital of Japan")
    .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED)));

// ── AMAP ──
aMap.addMarker(new MarkerOptions()
    .position(new LatLng(35.68, 139.76))
    .title("Tokyo")
    .snippet("Capital of Japan")
    .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED)));
// Identical code — just change imports!
```

### Code: Polyline

```java
// ── GOOGLE ──
mMap.addPolyline(new PolylineOptions()
    .add(new LatLng(35.68, 139.76), new LatLng(35.65, 139.69))
    .width(5).color(Color.RED));

// ── AMAP ──
aMap.addPolyline(new PolylineOptions()
    .add(new LatLng(35.68, 139.76), new LatLng(35.65, 139.69))
    .width(5).color(Color.RED));
// Identical!
```

### Code: Geocoding

```java
// ── GOOGLE ──
Geocoder geocoder = new Geocoder(context, Locale.getDefault());
List<Address> addresses = geocoder.getFromLocationName("Tokyo", 1);
LatLng location = new LatLng(addresses.get(0).getLatitude(), addresses.get(0).getLongitude());

// ── AMAP ── (async pattern)
GeocodeSearch geocodeSearch = new GeocodeSearch(context);
geocodeSearch.setOnGeocodeSearchListener(new GeocodeSearch.OnGeocodeSearchListener() {
    public void onGeocodeSearched(GeocodeResult result, int rCode) {
        if (rCode == 1000) {
            GeocodeAddress addr = result.getGeocodeAddressList().get(0);
            LatLonPoint point = addr.getLatLonPoint();
            LatLng location = new LatLng(point.getLatitude(), point.getLongitude());
        }
    }
    public void onRegeocodeSearched(RegeocodeResult result, int rCode) {}
});
GeocodeQuery query = new GeocodeQuery("Tokyo", "");
geocodeSearch.getFromLocationNameAsyn(query);
```

### Code: Route Search

```java
// ── GOOGLE ── (typically uses REST API or Directions SDK)
// Most Android apps call the Directions REST API directly

// ── AMAP ──
RouteSearch routeSearch = new RouteSearch(context);
routeSearch.setRouteSearchListener(new RouteSearch.OnRouteSearchListener() {
    public void onDriveRouteSearched(DriveRouteResult result, int errorCode) {
        if (errorCode == 1000) {
            DrivePath path = result.getPaths().get(0);
            float distance = path.getDistance(); // meters
            long duration = path.getDuration();   // seconds
        }
    }
    // ... other mode callbacks
});
RouteSearch.FromAndTo fromAndTo = new RouteSearch.FromAndTo(
    new LatLonPoint(35.68, 139.76),  // start
    new LatLonPoint(35.65, 139.69)   // end
);
RouteSearch.DriveRouteQuery query = new RouteSearch.DriveRouteQuery(fromAndTo, 0, null, null, "");
routeSearch.calculateDriveRouteAsyn(query);
```

### Android Lifecycle

AMap MapView requires lifecycle calls (same pattern as Google):

```java
protected void onResume() { super.onResume(); mapView.onResume(); }
protected void onPause() { super.onPause(); mapView.onPause(); }
protected void onDestroy() { super.onDestroy(); mapView.onDestroy(); }
protected void onSaveInstanceState(Bundle outState) {
    super.onSaveInstanceState(outState);
    mapView.onSaveInstanceState(outState);
}
```

---

## iOS SDK: Google → AMap

### Dependencies

```ruby
# ── GOOGLE (Podfile) ──
pod 'GoogleMaps', '~> 8.0'
pod 'GooglePlaces', '~> 8.0'

# ── AMAP (Podfile) ──
pod 'AMap3DMap'          # 3D Map SDK
pod 'AMapSearch'         # Search/Geocode/Route
pod 'AMapLocation'       # Location
```

### Class Mapping

| Google Class | AMap Class | Notes |
|---|---|---|
| `GMSMapView` | `MAMapView` | Core map view |
| `GMSMarker` | `MAPointAnnotation` | Data model only |
| *(marker view)* | `MAAnnotationView` / `MAPinAnnotationView` | AMap separates model and view |
| `GMSPolyline` | `MAPolyline` | Data model |
| *(polyline render)* | `MAPolylineRenderer` | Separate renderer |
| `GMSPolygon` | `MAPolygon` + `MAPolygonRenderer` | — |
| `GMSCircle` | `MACircle` + `MACircleRenderer` | — |
| `GMSCameraPosition` | `MAMapStatus` | Camera |
| `GMSCoordinateBounds` | `MACoordinateRegion` | Bounds |
| `GMSGeocoder` | `AMapSearchAPI` | Unified search API |
| `GMSPlacesClient` | `AMapSearchAPI` | Unified search API |
| `GMSMapViewDelegate` | `MAMapViewDelegate` | Delegate |
| `CLLocationCoordinate2D` | `CLLocationCoordinate2D` | Same (CoreLocation) |

### Code: Map Init

```objc
// ── GOOGLE ──
GMSCameraPosition *camera = [GMSCameraPosition cameraWithLatitude:35.68 longitude:139.76 zoom:12];
GMSMapView *mapView = [GMSMapView mapWithFrame:CGRectZero camera:camera];
self.view = mapView;

// ── AMAP ──
MAMapView *mapView = [[MAMapView alloc] initWithFrame:self.view.bounds];
mapView.delegate = self;
[mapView setCenterCoordinate:CLLocationCoordinate2DMake(35.68, 139.76) animated:NO];
[mapView setZoomLevel:12 animated:NO];
[self.view addSubview:mapView];
```

### Code: Markers / Annotations

```objc
// ── GOOGLE ──
GMSMarker *marker = [[GMSMarker alloc] init];
marker.position = CLLocationCoordinate2DMake(35.68, 139.76);
marker.title = @"Tokyo";
marker.snippet = @"Capital of Japan";
marker.map = mapView;

// ── AMAP ──
MAPointAnnotation *annotation = [[MAPointAnnotation alloc] init];
annotation.coordinate = CLLocationCoordinate2DMake(35.68, 139.76);
annotation.title = @"Tokyo";
annotation.subtitle = @"Capital of Japan";
[mapView addAnnotation:annotation];

// Customize view via delegate:
- (MAAnnotationView *)mapView:(MAMapView *)mapView viewForAnnotation:(id<MAAnnotation>)annotation {
    MAPinAnnotationView *pinView = (MAPinAnnotationView *)[mapView
        dequeueReusableAnnotationViewWithIdentifier:@"pin"];
    if (!pinView) {
        pinView = [[MAPinAnnotationView alloc] initWithAnnotation:annotation reuseIdentifier:@"pin"];
        pinView.canShowCallout = YES;
    }
    return pinView;
}
```

### Code: Polyline

```objc
// ── GOOGLE ──
GMSMutablePath *path = [GMSMutablePath path];
[path addCoordinate:CLLocationCoordinate2DMake(35.68, 139.76)];
[path addCoordinate:CLLocationCoordinate2DMake(35.65, 139.69)];
GMSPolyline *polyline = [GMSPolyline polylineWithPath:path];
polyline.strokeColor = [UIColor redColor];
polyline.strokeWidth = 3;
polyline.map = mapView;

// ── AMAP ──
CLLocationCoordinate2D coords[2] = {
    CLLocationCoordinate2DMake(35.68, 139.76),
    CLLocationCoordinate2DMake(35.65, 139.69)
};
MAPolyline *polyline = [MAPolyline polylineWithCoordinates:coords count:2];
[mapView addOverlay:polyline];

// Customize via delegate:
- (MAOverlayRenderer *)mapView:(MAMapView *)mapView rendererForOverlay:(id<MAOverlay>)overlay {
    if ([overlay isKindOfClass:[MAPolyline class]]) {
        MAPolylineRenderer *renderer = [[MAPolylineRenderer alloc] initWithPolyline:overlay];
        renderer.strokeColor = [UIColor redColor];
        renderer.lineWidth = 3;
        return renderer;
    }
    return nil;
}
```

### Code: Geocoding (Forward)

```objc
// ── GOOGLE ──
CLGeocoder *geocoder = [[CLGeocoder alloc] init];
[geocoder geocodeAddressString:@"Tokyo" completionHandler:^(NSArray<CLPlacemark *> *placemarks, NSError *err) {
    CLLocationCoordinate2D coord = placemarks.firstObject.location.coordinate;
}];

// ── AMAP ──
AMapSearchAPI *search = [[AMapSearchAPI alloc] init];
search.delegate = self;
AMapGeocodeSearchRequest *req = [[AMapGeocodeSearchRequest alloc] init];
req.address = @"Tokyo";
[search AMapGeocodeSearch:req];

// Delegate callback:
- (void)onGeocodeSearchDone:(AMapGeocodeSearchRequest *)request response:(AMapGeocodeSearchResponse *)response {
    AMapGeocode *geo = response.geocodes.firstObject;
    CLLocationCoordinate2D coord = CLLocationCoordinate2DMake(geo.location.latitude, geo.location.longitude);
}
```

### Code: Geocoding (Reverse)

```objc
// ── GOOGLE ──
GMSGeocoder *geocoder = [GMSGeocoder geocoder];
[geocoder reverseGeocodeCoordinate:coord completionHandler:^(GMSReverseGeocodeResponse *resp, NSError *err) {
    GMSAddress *address = resp.firstResult;
}];

// ── AMAP ──
AMapSearchAPI *search = [[AMapSearchAPI alloc] init];
search.delegate = self;
AMapReGeocodeSearchRequest *req = [[AMapReGeocodeSearchRequest alloc] init];
req.location = [AMapGeoPoint locationWithLatitude:35.68 longitude:139.76];
[search AMapReGoecodeSearch:req];

// Delegate callback:
- (void)onReGeocodeSearchDone:(AMapReGeocodeSearchRequest *)request response:(AMapReGeocodeSearchResponse *)response {
    NSString *address = response.regeocode.formattedAddress;
}
```

### iOS Key Difference: Model/View Separation

Google iOS SDK (`GMSMarker`, `GMSPolyline`, etc.) combines data and visual representation in one object. AMap iOS SDK separates them:

- **Data model:** `MAPointAnnotation`, `MAPolyline`, `MAPolygon`, `MACircle`
- **Visual renderer:** `MAAnnotationView`, `MAPolylineRenderer`, `MAPolygonRenderer`, `MACircleRenderer`

You configure visuals via `MAMapViewDelegate` methods, similar to `UITableViewDelegate` pattern. This is more code but gives finer control.

---

## Non-Mainland SDK

Native mobile SDK for Non-Mainland (excl. HK/MO/TW) regions is **coming soon / 敬请期待**. Current options for Non-Mainland mobile:

1. **WebView + JS API** — Use AMap JS API in a WebView for map rendering
2. **Web Service API** — Call REST APIs from native code for geocoding, search, routing
3. **Hybrid approach** — Native UI + WebView map + REST APIs for services
