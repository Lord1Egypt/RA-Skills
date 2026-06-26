# 类与包速查

以下为百度地图 Android SDK 常用类与包，便于按能力查找。具体方法、参数以工程所集成的 SDK 版本为准。

## 初始化与配置

- `com.baidu.mapapi.SDKInitializer`：initialize、setApiKey、setCoordType、setAgreePrivacy、getCoordType
- `com.baidu.mapapi.CoordType`：BD09LL、GCJ02

## 地图容器与控制器

- `com.baidu.mapapi.map.MapView`、`BaiduMap`、`getMap()`、onResume/onPause/onDestroy
- `com.baidu.mapapi.map.SupportMapFragment`、`TextureMapView`、`TextureSupportMapFragment`
- `com.baidu.mapapi.map.BaiduMapOptions`：mapType、compassEnable、zoomGesturesEnabled 等

## 地图状态与视野

- `MapStatus`、`MapStatus.Builder`、`MapStatusUpdate`、`MapStatusUpdateFactory`
- `MapStatusUpdateFactory.zoomTo/zoomIn/zoomOut/zoomBy`、`newLatLng`、`newLatLngBounds`、`newMapStatus`
- `BaiduMap`：setMapStatus、animateMapStatus、setMapType、setTrafficEnabled、setBaiduHeatMapEnabled、setViewPadding、showMapPoi、setPoiTagEnable、setMapBackgroundColor

## 几何与覆盖物基础

- `com.baidu.mapapi.model.LatLng`、`LatLngBounds`、`LatLngBounds.Builder`
- `com.baidu.mapapi.map.BitmapDescriptor`、`BitmapDescriptorFactory`
- `OverlayOptions`、`Overlay`、`BaiduMap.addOverlay`、`clear`
- `Marker`、`MarkerOptions`：position、icon、draggable、flat、alpha、animateType、titleOptions、isJoinCollision、poiCollided 等
- `Polyline`、`PolylineOptions`：points、width、color、dottedLine、colorsValues、customTextureList、textureIndex、isGeodesic、isGradient、bloomType 等
- `Polygon`、`PolygonOptions`

## 事件监听

- `BaiduMap.OnMarkerClickListener`、`OnMarkerDragListener`、`OnPolylineClickListener`、`OnMapLoadedCallback`

## 定位

- `com.baidu.location.LocationClient`、`LocationClientOption`、`BDAbstractLocationListener`、`BDLocation`
- `com.baidu.mapapi.map.MyLocationData`、`MyLocationConfiguration`、`LocationMode`（NORMAL、FOLLOWING、COMPASS）
- `BaiduMap`：setMyLocationEnabled、setMyLocationData、setMyLocationConfiguration

## 检索

- `com.baidu.mapapi.search.poi.PoiSearch`、`PoiSearch.newInstance()`、setOnGetPoiSearchResultListener、searchInCity、searchNearby、searchInBound、searchPoiDetail、destroy
- `PoiCitySearchOption`、`PoiNearbySearchOption`、`PoiBoundSearchOption`、`PoiDetailSearchOption`
- `OnGetPoiSearchResultListener`、`PoiResult`、`PoiDetailSearchResult`、`PoiInfo`
- `com.baidu.mapapi.search.geocode.GeoCoder`、`GeoCodeOption`、`ReverseGeoCodeOption`、`OnGetGeoCoderResultListener`、`GeoCodeResult`、`ReverseGeoCodeResult`

## 路线规划

- `com.baidu.mapapi.search.route.RoutePlanSearch`、`RoutePlanSearch.newInstance()`、setOnGetRoutePlanResultListener、drivingSearch、walkingSearch、ridingSearch、transitSearch、destroy
- `PlanNode`、`PlanNode.withCityNameAndPlaceName`、`PlanNode.withLocation`
- `DrivingRoutePlanOption`、`WalkingRoutePlanOption`、`BikingRoutePlanOption`、`TransitRoutePlanOption`
- `OnGetRoutePlanResultListener`、`DrivingRouteResult`、`WalkingRouteResult`、`BikingRouteResult`、`TransitRouteResult`、`getRouteLines()`
- 开源 Overlay：DrivingRouteOverlay、WalkingRouteOverlay、BikingRouteOverlay、TransitRouteOverlay、PoiOverlay（overlayutil 包）

## 步骑行导航（实时诱导）

- WalkNavigateHelper、BikeNavigateHelper、WalkNaviLaunchParam、BikeNaviLaunchParam、initNaviEngine、routePlanWithParams、onCreate（诱导 View）、startWalkNavi/startBikeNavi、setRouteGuidanceListener、setTTsPlayer、resume/pause/quit

## 坐标转换

- `com.baidu.mapapi.utils.CoordinateConverter`、`CoordType.GPS`、`COMMON`、`BD09MC` 等、`from()`、`coord()`、`convert()`

## 室内图

- `BaiduMap.setOnBaseIndoorMapListener`、`switchBaseIndoorMapFloor`、MapBaseIndoorMapInfo、SwitchFloorError

## 投影与 3D Marker

- `BaiduMap.getProjection()`、`projection.geoPoint3toScreenLocation(LatLng, height)`、`fromScreenLocation(Point)`

## 工具（BaiduMapSDK_Util）

- **距离与面积**：`DistanceUtil.getDistance(LatLng, LatLng)` 返回米；`AreaUtil.calculateArea(LatLng northeast, LatLng southwest)` 返回平方米。
- **点与图形**：`SpatialRelationUtil.isCircleContainsPoint(center, radius, point)`、`isPolygonContainsPoint(points, pt)`、`getNearestPointFromLine(points, pt)`。
- **调起百度地图**：`BaiduMapRoutePlan`（RouteParaOption、openBaiduMapTransitRoute 等）、`BaiduMapNavigation`（NaviParaOption、openBaiduMapWalkNavi 等）、`BaiduMapPoiSearch`（PoiParaOption、openBaiduMapPoiNearbySearch、openBaiduMapPoiDetialsPage、openBaiduMapPanoShow），调起后调用对应 `finish(context)`。
- **短地址分享**：`ShareUrlSearch`、OnGetShareUrlResultListener、PoiDetailShareURLOption、LocationShareURLOption、RouteShareURLOption、requestPoiDetailShareUrl/requestLocationShareUrl/requestRouteShareUrl，ShareUrlResult.getUrl()，destroy()。
