# 工具组件

**边界**：距离与面积、点与图形位置关系、调起百度地图、位置短地址分享、地图收藏夹等；与其它文档组合使用。坐标转换见 [coordinate.md](coordinate.md)。

## 距离与面积

- **两点距离**（米）：`DistanceUtil.getDistance(LatLng p1, LatLng p2)`，返回 double，单位米。
- **矩形面积**（平方米）：由东北角、西南角构成矩形，`AreaUtil.calculateArea(LatLng northeast, LatLng southwest)`，返回 double，单位平方米。

## 点与图形位置关系

类：`SpatialRelationUtil`（com.baidu.mapapi.utils 包，属 BaiduMapSDK_Util）。

- **点与圆**：`SpatialRelationUtil.isCircleContainsPoint(center, radius, point)`，center 为圆心 LatLng，radius 半径（米），point 待判断点，返回 boolean。
- **点与多边形**：`SpatialRelationUtil.isPolygonContainsPoint(List<LatLng> points, LatLng pt)`，points 为多边形顶点顺序列表，返回 boolean 表示 pt 是否在多边形内。
- **点与折线最近点**：`SpatialRelationUtil.getNearestPointFromLine(List<LatLng> points, LatLng pt)`，返回折线上与 pt 距离最近的 LatLng。

## 调起百度地图

调起百度地图客户端（Native 或 Web）做路线规划、导航、POI 详情/全景等。传入坐标类型需与 SDK 全局坐标类型一致。部分能力需百度地图 APP 8.6.6 以上；未安装时可调起 Web 版，可通过各类的 setSupportWeb 相关方法设置是否支持 Web。调起结束后调用对应 `finish(context)` 释放资源。

- **路线规划**：`BaiduMapRoutePlan`。参数 `RouteParaOption`，起终点至少包含 startName+endName 或 startPoint+endPoint 等。示例：公交 `BaiduMapRoutePlan.openBaiduMapTransitRoute(paraOption, context)`，需设置 `startPoint/endPoint` 或 `startName/endName`，以及 `busStrategyType` 等。
- **导航**：`BaiduMapNavigation`。参数 `NaviParaOption`，设 startPoint、endPoint、startName、endName。步行 `BaiduMapNavigation.openBaiduMapWalkNavi(para, context)`；驾车/骑行有对应 open 方法。可能抛出 `BaiduMapAppNotSupportNaviException`。结束时 `BaiduMapNavigation.finish(context)`。
- **POI**：`BaiduMapPoiSearch`。周边检索用 `PoiParaOption`（key、center、radius），`openBaiduMapPoiNearbySearch(para, context)`。POI 详情页需 uid：`PoiParaOption().uid("...")`，`openBaiduMapPoiDetialsPage(para, context)`。POI 全景：`openBaiduMapPanoShow(uid, context)`。结束时 `BaiduMapPoiSearch.finish(context)`。

## 位置短地址分享

类：`ShareUrlSearch`（newInstance），监听 `OnGetShareUrlResultListener`，先 `setOnGetShareUrlResultListener` 再发起请求，用毕 `destroy()`。

- **POI 详情短链**：`requestPoiDetailShareUrl(new PoiDetailShareURLOption().poiUid(uid))`，回调 `onGetPoiDetailShareUrlResult(ShareUrlResult)`，`getUrl()` 得短链。
- **逆地理（坐标）短链**：`requestLocationShareUrl(new LocationShareURLOption().location(latLng).name(...).snippet(...))`，回调 `onGetLocationShareUrlResult`，`getUrl()` 得短链。
- **路线规划短链**：起终点用 `PlanNode`（如 `withCityCodeAndPlaceName`），`requestRouteShareUrl(new RouteShareURLOption().from(startNode).to(endNode).routMode(mode))`，mode 为 CAR/FOOT/CYCLE/BUS 等，回调 `onGetRouteShareUrlResult`，`getUrl()` 得短链。步行/骑行目前仅支持同城。

## 地图收藏夹

地图 SDK 提供收藏夹能力，用于收藏地点等，具体 API 以当前版本文档为准，可在类参考中搜索「收藏」或「Favorite」相关类。
