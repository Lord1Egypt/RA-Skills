# 点标记（Marker）

## 添加 Marker

- `LatLng point = new LatLng(lat, lng);`
- `BitmapDescriptor bitmap = BitmapDescriptorFactory.fromResource(R.drawable.xxx);`
- `OverlayOptions option = new MarkerOptions().position(point).icon(bitmap);`
- `mBaiduMap.addOverlay(option);` 返回 Overlay，可强转为 Marker。

## MarkerOptions 常用属性

| 名称 | 说明 |
|------|------|
| icon | 图标 BitmapDescriptor |
| animateType | 动画类型：MarkerAnimateType.none / drop / grow / jump |
| alpha | 透明度 |
| position | 位置 LatLng |
| perspective | 是否近大远小，默认 true |
| draggable | 是否可拖拽 |
| flat | 是否平贴地图（俯视效果） |
| anchor | 锚点比例 |
| rotate | 旋转角度 |
| title | 标题 |
| visible | 是否可见 |
| extraInfo | 额外信息 Bundle |

示例：`.position(point).icon(bitmap).draggable(true).flat(true).alpha(0.5f)`。

## 事件

- **点击**：`mBaiduMap.setOnMarkerClickListener(BaiduMap.OnMarkerClickListener)`，`onMarkerClick(Marker marker)`，返回 true 表示消费事件。
- **拖拽**：需在 MarkerOptions 中 `draggable(true)`；`setOnMarkerDragListener`，回调 `onMarkerDrag`、`onMarkerDragEnd`、`onMarkerDragStart`。

## 底图标注

- `mBaiduMap.showMapPoi(false)` 可隐藏底图 POI，仅显示道路。

## Marker 碰撞策略（v7.5.0+）

- 属性：`isJoinCollision`（是否参与碰撞）、`isForceDisplay`（参与后是否强制展示）、`priority`（碰撞优先级，默认整型最大）、`startLevel`/`endLevel`（最小/最大展示层级，室外默认 4–21，室内至 22）。
- 使用：`MarkerOptions().position(...).icon(...).isJoinCollision(true).isForceDisplay(true).priority(9)`，再 `addOverlay` 即生效。

## 3D Marker（v7.5.2+）

- 带高度的 Marker：先设高度，用 `projection.geoPoint3toScreenLocation(LatLng, height)` 转成屏幕点，再用 `projection.fromScreenLocation(Point)` 转回经纬度，然后按普通 Marker 添加。

## Marker 的 Title（v7.5.7+）

- 通过 `TitleOptions`：titleBgColor、titleFrontColor、titleFrontSize、titleAnchorX/Y、titileOffsetX/Y、titleRotate。
- `MarkerOptions.titleOptions(titleOptions)`。

## Marker 碰撞 POI（v7.5.7+）

- `MarkerOptions.poiCollided(true)` 使 Marker 及其 title 可与底图 POI 碰撞。
