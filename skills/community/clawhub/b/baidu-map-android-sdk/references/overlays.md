# 折线与多边形覆盖物

## 折线 PolylineOptions

- 坐标列表：`List<LatLng> points`。
- 常用属性：`color`、`width`、`points`、`colorsValues`（分段颜色）、`customTexture` / `customTextureList` + `textureIndex`（分段纹理）、`visible`、`extraInfo`。
- 添加：`OverlayOptions o = new PolylineOptions().width(10).color(0xAAFF0000).points(points);`，`mBaiduMap.addOverlay(o);` 返回可强转为 Polyline。

## 虚线

- 构造时：`PolylineOptions().dottedLine(true)`；或对已添加的 Polyline：`((Polyline)mPolyline).setDottedLine(true)`。

## 分段颜色

- `PolylineOptions().points(points).colorsValues(List<Integer> colors)`，colors 与线段段数对应。

## 分段纹理

- 纹理宽高建议 2 的幂；设纹理后折线颜色不生效。`customTextureList(List<BitmapDescriptor>)`、`textureIndex(List<Integer>)`；建议配合 `dottedLine(true)`。

## Polyline 点击

- `mBaiduMap.setOnPolylineClickListener(BaiduMap.OnPolylineClickListener)`，`onPolylineClick(Polyline polyline)` 返回 boolean。

## 大地曲线

- `PolylineOptions().isGeodesic(true).points(pointList)`；经度跨 180° 时需设置 `lineDirectionCross180(PolylineOptions.LineDirectionCross180.FROM_WEST_TO_EAST)`。点数 2–10000，且不能含 null。

## 渐变色

- `PolylineOptions().isGradient(true).points(points).colorsValues(List<Integer> colorValue)`，colorValue 为每个点的颜色，按索引与点对应。

## Polyline 发光（v7.5.7+）

- `PolylineOptions.bloomType(LineBloomType)`（默认不发光）、`bloomWidth(int)`、`bloomAlpha(int)`、`setBloomGradientASpeed(float)`、`setBloomBlurTimes(int)` 等。

## 多边形

- 使用 `PolygonOptions` 设置轮廓点、填充色、边框等，`mBaiduMap.addOverlay(polygonOptions)` 得到 Polygon。具体属性见类参考。

## 路线 Overlay（开源）

- 自 V3.6.0 起 Overlay 源码在 Demo 的 overlayutil 包：PoiOverlay、TransitRouteOverlay、WalkingRouteOverlay、BikingRouteOverlay、DrivingRouteOverlay、BusLineOverlay、MassTransitRouteOverlay 等，需自行拷贝到项目使用。
