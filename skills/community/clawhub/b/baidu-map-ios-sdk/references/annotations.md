# 标注 (Annotation)

**边界**：addAnnotation 体系；覆盖物见 [overlays.md](overlays.md)。**必须遵守**：点标注**优先使用 Marker**（BMKIconMarker/BMKTextMarker，addOverlay），**不得使用** Annotation/PinAnnotation 做起终点、小车、普通图钉等；**仅**点聚合、固定屏选点等必须用 addAnnotation 的场景才用本 API。见 [SKILL.md](../SKILL.md) 规则 3。

## 使用须知
- **Delegate**：addAnnotation 前必须设置 `mapView.delegate`，并实现 `mapView:viewForAnnotation:`。
- **复用**：使用 `dequeueReusableAnnotationViewWithIdentifier`，identifier 建议唯一。
- **起终点**：推荐 BMKIconMarker（addOverlay），见 [overlays.md](overlays.md)。

## 核心类

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKAnnotation | BMKAnnotation.h | 标注协议，`coordinate`、`title` |
| BMKPointAnnotation | BMKPointAnnotation.h | 点标注 |
| BMKAnnotationView | BMKAnnotationView.h | 标注视图基类 |
| BMKPinAnnotationView | BMKPinAnnotationView.h | 大头针样式 |
| BMKActionPaopaoView | BMKActionPaopaoView.h | 气泡视图 |

**标注规范**：使用 `dequeueReusableAnnotationViewWithIdentifier` 复用，identifier 建议唯一。自定义图片用 BMKAnnotationView + image。

## 固定屏幕标注（地图选点）

`BMKPointAnnotation.isLockedToScreen = YES` + `screenPointToLock`，需在 `mapViewDidFinishLoading` 后设置。常用于地图选点。

**方式 B（BMKIconMarker）**：Marker 无 isLockedToScreen，需在 `regionDidChangeAnimated:reason:` 中（reason == BMKRegionChangeReasonGesture）同步 `marker.coordinate = mapView.centerCoordinate`。**区域回调**：regionWillChange 跳起，regionDidChange 落下 + 逆地理。**选点动画**见 [ui-standards.md](ui-standards.md)。

## BMKPinAnnotationView 常用属性

`centerOffset`、`calloutOffset`（正偏移朝右下方）、`enabled3D`、`canShowCallout`、`leftCalloutAccessoryView`/`rightCalloutAccessoryView`（默认气泡最大 32×41）、`pinColor`（Red/Green/Purple）、`animatesDrop`、`draggable`。直接设置 `selected` 时，非 PinAnnotation 需在设置后调用 `mapForceRefresh`。

## 碰撞检测与展示优先级

`BMKAnnotationView.displayPriority`（如 `BMKFeatureDisplayPriorityDefaultHigh`）、`isOpenCollisionDetection`、`collisionDetectionPriority`（数值越大越优先）、`isForceDisplay`（强制展示）、`displayMaxLevel`/`displayMinLevel`（层级限制）。

## 点聚合中的标注

点聚合（BMKClusterManager + BMKPointAnnotation）将大量标注按 zoom 聚合。`viewForAnnotation` 按 cluster.size 区分单点/聚合点；size>1 可显示数量、按档设圆点大小。**点击拆簇**：`annotationViewForBubble` 中 zoomIn。聚合逻辑见 [overlays.md](overlays.md)。

---

## 按需方案

| 需求 | 基础能力 |
|------|----------|
| 普通点标注 | BMKPointAnnotation + BMKAnnotationView |
| 大头针 | BMKPointAnnotation + BMKPinAnnotationView |
| 固定屏幕选点 | BMKPointAnnotation（isLockedToScreen + screenPointToLock）或 BMKIconMarker |
| 起终点大头针 | BMKPointAnnotation + BMKAnnotationView（起终点推荐 BMKIconMarker，见 [overlays.md](overlays.md)） |
| 点聚合标注 | BMKClusterManager + BMKPointAnnotation，viewForAnnotation 按 size 展示 |
