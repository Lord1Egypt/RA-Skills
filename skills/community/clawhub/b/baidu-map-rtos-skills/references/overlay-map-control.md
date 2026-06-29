# 地图状态、覆盖物与触摸

完整可运行示例见 [demo.md § RunMapStateAndOverlayDemo](demo.md) 和 [demo.md § RunTouchDemo](demo.md)。

## 地图状态与坐标

```cpp
mapApi.setCenterPoint(VDPOINT(lng, lat));  // VDPOINT 为经度/纬度顺序
mapApi.setZoom(level);
mapApi.zoomIn() / zoomOut();
mapApi.setRotationAngle(degrees);
mapApi.setViewBound(rect);
mapApi.LatLngToScreenPixel(center);
mapApi.ScreenPixelToLatLng(pixel);
```

## 触摸事件

构造 `TouchEvent`（类型：`TOUCH_START` / `TOUCH_MOVE` / `TOUCH_END`），填充 `touches` / `changedTouches` 后：

```cpp
mapApi.OnTouchDown(event);
mapApi.OnTouchMove(event);
mapApi.OnTouchUp(event);
```

## Overlay 层与 Marker

```cpp
int layerId  = mapApi.createLayer(LayerType::OVERLAYER, "layer_name");
int markerId = mapApi.CreateMarker();
mapApi.setMarkerPosition(markerId, VDPOINT(lng, lat));
mapApi.setMarkerSize(markerId, VSize(w, h));
mapApi.setMarkerOffset(markerId, VSize(ox, oy));
mapApi.setMarkerIcon(markerId, resPath);   // 须为可访问绝对路径
mapApi.addOverlay(layerId, markerId);
mapApi.showOverlay(markerId);
mapApi.updateLayer(layerId);
mapApi.RequestRender();
```

> `drawMarker: pixel=(0,0)` 日志是 marker 与地图中心重合的正常现象。

## 折线（点集）

```cpp
int polylineId = mapApi.CreatePolyline();
mapApi.setPolylinePoints(polylineId, points);
mapApi.setPolylineLineWidth(polylineId, 8);
mapApi.setPolylineFillColor(polylineId, VColor(0, 153, 255, 220));
mapApi.setPolylineStrokeColor(polylineId, color);   // 可选
mapApi.setPolylineStrokeWidth(polylineId, 2);        // 可选
mapApi.addOverlay(layerId, polylineId);
mapApi.showOverlay(polylineId);
mapApi.updateLayer(layerId);
mapApi.setViewBound(mapApi.getOverlayBounds(polylineId));
mapApi.RequestRender();
```

## 折线（GeoJSON 文件）

```cpp
mapApi.setPolylinePointsURI(polylineId, "/abs/path/to/routes.geojson");
mapApi.setPolylineLineWidth(polylineId, 12);
mapApi.setPolylineFillColor(polylineId, VColor::fromHex("#09cfed"));
// addOverlay → showOverlay → updateLayer → setRotationAngle(0) → setViewBound → RequestRender
```

**必须显式设置线宽与颜色；勿依赖默认样式。**

## 路线瓦片预加载

```cpp
mapApi.LoadRouteMapData(routeFileName, [](const TilePreloadResponse& resp) {
    // resp.progressPercent == -1 表示瓦片数量超限
});
mapApi.CancelMapDataDownload();
mapApi.DeleteRouteMapData(routeFileName);  // routeFileName 为文件名，非完整路径
```
