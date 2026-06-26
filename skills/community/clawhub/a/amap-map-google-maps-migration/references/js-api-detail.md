# JS API Migration: Google Maps → AMap — Complete Reference

Self-contained reference. No external links needed — all migration info is here.

---

## Setup: Google → AMap

```html
<!-- ══ GOOGLE ══ -->
<script src="https://maps.googleapis.com/maps/api/js?key=GOOGLE_KEY&callback=initMap" async defer></script>

<!-- ══ AMAP (Non-Mainland) ══ -->
<script>window._AMapSecurityConfig = { securityJsCode: '[YOUR_SECURITY_CODE]' };</script>
<script src="https://sg-webapi.opnavi.com/maps?v=2.0&key=b87b3d194a024295b1b17be020659457&appname=amap-map-google-maps-migration"></script>

<!-- ══ AMAP (Mainland) ══ -->
<script>window._AMapSecurityConfig = { securityJsCode: '[YOUR_SECURITY_CODE]' };</script>
<script src="https://webapi.amap.com/maps?v=2.0&key=b87b3d194a024295b1b17be020659457&appname=amap-map-google-maps-migration"></script>
```

AMap requires dual auth: `securityJsCode` BEFORE CDN loads + `key` in CDN URL. Google needs only one key.

---

## AMap.Map (replaces google.maps.Map)

### Constructor

```javascript
// Google
const map = new google.maps.Map(document.getElementById('map'), {
  center: { lat: 35.68, lng: 139.76 },
  zoom: 12,
  mapTypeId: 'roadmap'
});

// AMap
const map = new AMap.Map('map', {  // string ID, not element
  center: [139.76, 35.68],         // [lng, lat] REVERSED
  zoom: 12,
  viewMode: '2D',                   // or '3D'
  mapStyle: 'amap://styles/normal'  // normal/dark/light/fresh
});
```

### Options Mapping

| Google Option | AMap Option | Notes |
|---|---|---|
| `center: {lat, lng}` | `center: [lng, lat]` | Reversed |
| `zoom` | `zoom` | Same (2-20) |
| `mapTypeId: 'roadmap'` | `mapStyle: 'amap://styles/normal'` | Different system |
| `mapTypeId: 'satellite'` | `layers: [new AMap.TileLayer.Satellite()]` | Layer-based |
| `tilt` | `pitch` | 3D tilt (0-83) |
| `heading` | `rotation` | 0-360 |
| *(no equivalent)* | `viewMode: '3D'` | Enable 3D |
| *(no equivalent)* | `features: ['bg','road','building','point']` | Toggle features |

### Methods Mapping

| Google Method | AMap Method | Notes |
|---|---|---|
| `map.setCenter({lat,lng})` | `map.setCenter([lng,lat])` | Reversed |
| `map.getCenter()` | `map.getCenter()` | Returns LngLat |
| `map.setZoom(n)` | `map.setZoom(n)` | Same |
| `map.getZoom()` | `map.getZoom()` | Same |
| `map.panTo({lat,lng})` | `map.panTo([lng,lat])` | Reversed |
| `map.fitBounds(bounds)` | `map.setBounds(bounds)` | Different name |
| `map.getBounds()` | `map.getBounds()` | Same |
| *(no equivalent)* | `map.setZoomAndCenter(zoom,[lng,lat])` | Set both |
| *(no equivalent)* | `map.add(overlay)` | Add overlay |
| *(no equivalent)* | `map.remove(overlay)` | Remove overlay |
| *(no equivalent)* | `map.clearMap()` | Clear all overlays |
| *(no equivalent)* | `map.destroy()` | Destroy instance |

---

## AMap.Marker (replaces google.maps.Marker)

### Constructor

```javascript
// Google
const marker = new google.maps.Marker({
  position: { lat: 35.68, lng: 139.76 },
  map: map,
  title: 'Tokyo',
  icon: 'icon.png'
});
marker.setMap(null); // remove

// AMap
const marker = new AMap.Marker({
  position: [139.76, 35.68],   // [lng, lat] REVERSED
  map: map,
  title: 'Tokyo',
  icon: 'icon.png'             // or AMap.Icon instance
});
marker.setMap(null);            // same removal pattern
// or: map.remove(marker);
```

### Options Mapping

| Google Option | AMap Option | Notes |
|---|---|---|
| `position: {lat,lng}` | `position: [lng,lat]` | Reversed |
| `map` | `map` | Same |
| `title` | `title` | Same |
| `icon: 'url'` | `icon: 'url'` or `new AMap.Icon(opts)` | Same or richer |
| `label: {text}` | `label: {content, offset, direction}` | Richer |
| `draggable` | `draggable` | Same |
| `visible` | `visible` | Same |
| *(no equivalent)* | `content: '<div>...'` | Custom HTML replaces icon |
| *(no equivalent)* | `anchor: 'center'` | Anchor point |

---

## AMap.InfoWindow (replaces google.maps.InfoWindow)

```javascript
// Google
const iw = new google.maps.InfoWindow({ content: '<h3>Title</h3>' });
marker.addListener('click', () => iw.open(map, marker));

// AMap
const iw = new AMap.InfoWindow({
  content: '<h3>Title</h3>',
  offset: new AMap.Pixel(0, -30)
});
marker.on('click', () => iw.open(map, marker.getPosition()));
```

**Key difference:** Google's `open(map, marker)` takes marker. AMap's `open(map, position)` takes LngLat position.

---

## Events: Google → AMap

### Syntax

```javascript
// Google — verbose
google.maps.event.addListener(map, 'click', handler);
google.maps.event.removeListener(listenerRef);

// AMap — simple
map.on('click', handler);
map.off('click', handler);
```

### Event Name Mapping

| Google Event | AMap Event |
|---|---|
| `'click'` | `'click'` |
| `'dblclick'` | `'dblclick'` |
| `'rightclick'` | `'rightclick'` |
| `'mousemove'` | `'mousemove'` |
| `'mouseout'` | `'mouseout'` |
| `'mouseover'` | `'mouseover'` |
| `'center_changed'` | `'moveend'` |
| `'zoom_changed'` | `'zoomchange'` |
| `'bounds_changed'` | `'moveend'` |
| `'dragstart'` | `'dragstart'` |
| `'drag'` | `'dragging'` |
| `'dragend'` | `'dragend'` |
| `'idle'` | `'complete'` |
| `'tilesloaded'` | `'complete'` |
| `'resize'` | `'resize'` |

### Event Object

```javascript
// Google
map.addListener('click', (e) => {
  console.log(e.latLng.lat(), e.latLng.lng());  // methods
});

// AMap
map.on('click', (e) => {
  console.log(e.lnglat.getLat(), e.lnglat.getLng());  // methods
  // or: e.lnglat.lat, e.lnglat.lng                   // properties
});
```

---

## Overlays: Google → AMap

### Polyline

```javascript
// Google
new google.maps.Polyline({
  path: [{lat:35.68,lng:139.76}, {lat:35.65,lng:139.69}],
  strokeColor: '#FF0000', strokeWeight: 2, map: map
});

// AMap
new AMap.Polyline({
  path: [[139.76,35.68], [139.69,35.65]],  // [lng,lat] arrays
  strokeColor: '#FF0000', strokeWeight: 2, map: map
});
```

### Polygon

```javascript
// Google
new google.maps.Polygon({
  paths: [{lat:35.68,lng:139.76}, {lat:35.65,lng:139.69}, {lat:35.66,lng:139.72}],
  fillColor: '#FF0000', fillOpacity: 0.35, map: map
});

// AMap — note: "path" singular, not "paths"
new AMap.Polygon({
  path: [[139.76,35.68], [139.69,35.65], [139.72,35.66]],
  fillColor: '#FF0000', fillOpacity: 0.35, map: map
});
```

### Circle

```javascript
// Google
new google.maps.Circle({ center: {lat:35.68,lng:139.76}, radius: 1000, map: map });

// AMap
new AMap.Circle({ center: [139.76,35.68], radius: 1000, map: map });
```

---

## Plugins: Google → AMap

Google loads all services with the main script. AMap requires explicit plugin loading.

```javascript
AMap.plugin(['AMap.Geocoder','AMap.Driving','AMap.Walking','AMap.Transfer',
  'AMap.PlaceSearch','AMap.Autocomplete','AMap.Scale','AMap.ToolBar',
  'AMap.ControlBar','AMap.MapType','AMap.HeatMap','AMap.MarkerCluster'], function() {
  // All constructors now available
});
```

### Geocoder: Google → AMap

```javascript
// Google
const geocoder = new google.maps.Geocoder();
geocoder.geocode({ address: 'Tokyo' }, (results, status) => {
  if (status === 'OK') {
    const loc = results[0].geometry.location; // LatLng object
  }
});

// AMap
AMap.plugin('AMap.Geocoder', () => {
  const geocoder = new AMap.Geocoder();
  geocoder.getLocation('Tokyo', (status, result) => {
    if (status === 'complete') {
      const loc = result.geocodes[0].location; // LngLat object
    }
  });
});
```

### Driving Directions: Google → AMap

```javascript
// Google
const svc = new google.maps.DirectionsService();
svc.route({
  origin: {lat:35.68, lng:139.76},
  destination: {lat:35.65, lng:139.69},
  travelMode: 'DRIVING'
}, (result, status) => {
  // result.routes[0].legs[0].distance
});

// AMap
AMap.plugin('AMap.Driving', () => {
  const driving = new AMap.Driving({ map: map });
  driving.search(
    new AMap.LngLat(139.76, 35.68),   // origin [lng, lat]
    new AMap.LngLat(139.69, 35.65),   // destination
    (status, result) => {
      // result.routes[0].distance
    }
  );
});
```

### Place Search: Google → AMap

```javascript
// Google
const svc = new google.maps.places.PlacesService(map);
svc.textSearch({ query: 'restaurants' }, (results, status) => {
  results.forEach(r => console.log(r.name, r.geometry.location));
});

// AMap
AMap.plugin('AMap.PlaceSearch', () => {
  const ps = new AMap.PlaceSearch({ map: map, pageSize: 10 });
  ps.search('restaurants', (status, result) => {
    result.poiList.pois.forEach(p => console.log(p.name, p.location));
  });
});
```

### Autocomplete: Google → AMap

```javascript
// Google
const ac = new google.maps.places.Autocomplete(document.getElementById('input'));
ac.addListener('place_changed', () => { const place = ac.getPlace(); });

// AMap
AMap.plugin('AMap.Autocomplete', () => {
  const ac = new AMap.Autocomplete({ input: 'input' });  // element ID string
  ac.on('select', (e) => { const poi = e.poi; });
});
```

---

## Controls: Google → AMap

```javascript
// Google — declarative options
map.setOptions({ zoomControl: true, mapTypeControl: true, scaleControl: true });

// AMap — plugins
AMap.plugin(['AMap.Scale','AMap.ToolBar','AMap.ControlBar','AMap.MapType'], () => {
  map.addControl(new AMap.Scale());      // Scale bar
  map.addControl(new AMap.ToolBar());    // Zoom + pan
  map.addControl(new AMap.ControlBar()); // 3D rotation
  map.addControl(new AMap.MapType());    // Map type switch
});
```

---

## Complete Before/After Example

### Google Maps (Before)

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://maps.googleapis.com/maps/api/js?key=GOOGLE_KEY"></script>
</head>
<body>
  <div id="map" style="width:100%;height:400px;"></div>
  <script>
    const map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: 1.3521, lng: 103.8198 }, zoom: 13
    });
    const marker = new google.maps.Marker({
      position: { lat: 1.3521, lng: 103.8198 }, map: map, title: 'Singapore'
    });
    const iw = new google.maps.InfoWindow({ content: '<h3>Singapore</h3>' });
    marker.addListener('click', () => iw.open(map, marker));
    map.addListener('click', (e) => {
      console.log(e.latLng.lat(), e.latLng.lng());
    });
  </script>
</body>
</html>
```

### AMap (After — Non-Mainland)

```html
<!DOCTYPE html>
<html>
<head>
  <script>window._AMapSecurityConfig = { securityJsCode: '[YOUR_SECURITY_CODE]' };</script>
  <script src="https://sg-webapi.opnavi.com/maps?v=2.0&key=b87b3d194a024295b1b17be020659457&appname=amap-map-google-maps-migration"></script>
</head>
<body>
  <div id="map" style="width:100%;height:400px;"></div>
  <script>
    const map = new AMap.Map('map', {
      center: [103.8198, 1.3521], zoom: 13   // [lng, lat]
    });
    const marker = new AMap.Marker({
      position: [103.8198, 1.3521], map: map, title: 'Singapore'
    });
    const iw = new AMap.InfoWindow({
      content: '<h3>Singapore</h3>', offset: new AMap.Pixel(0, -30)
    });
    marker.on('click', () => iw.open(map, marker.getPosition()));
    map.on('click', (e) => {
      console.log(e.lnglat.getLat(), e.lnglat.getLng());
    });
  </script>
</body>
</html>
```

### Key Changes Summary

1. Script tag → dual auth + AMap CDN
2. `document.getElementById('map')` → `'map'` (string ID)
3. `{lat, lng}` → `[lng, lat]`
4. `google.maps.Map` → `AMap.Map`
5. `google.maps.Marker` → `AMap.Marker`
6. `google.maps.InfoWindow` → `AMap.InfoWindow` + `offset` + `.open(map, position)`
7. `marker.addListener(...)` → `marker.on(...)`
8. `e.latLng.lat()` → `e.lnglat.getLat()`
