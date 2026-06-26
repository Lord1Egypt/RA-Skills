# 类速查表

**边界**：按头文件组织的类速查；用法与示例见 [annotations.md](annotations.md)、[overlays.md](overlays.md) 等各功能文档。下表记录类名、头文件及主要方法/属性名，便于不依赖外链查阅。

## 地图核心

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKMapManager | BMKMapManager.h | 主引擎 |
| BMKMapView | BMKMapView.h | 地图视图 |
| BMKMapStatus | BMKMapStatus.h | 地图状态 |
| BMKMapViewDelegate | BMKMapView.h | 地图回调 |

## 标注

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKAnnotation | BMKAnnotation.h | 标注协议 |
| BMKPointAnnotation | BMKPointAnnotation.h | 点标注 |
| BMKAnnotationView | BMKAnnotationView.h | 标注视图基类 |
| BMKPinAnnotationView | BMKPinAnnotationView.h | 大头针样式 |
| BMKActionPaopaoView | BMKActionPaopaoView.h | 气泡视图 |

## 覆盖物

### 基础

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKOverlay | BMKOverlay.h | 覆盖物协议 |
| BMKOverlayView | BMKOverlayView.h | 覆盖物视图基类 |
| BMKPolyline | BMKPolyline.h | 单色/单纹理折线 |
| BMKPolylineView | BMKPolylineView.h | 折线视图 |
| BMKMultiPolyline | BMKMultiPolyline.h | 分段折线，需 drawIndexs |
| BMKMultiColorPolylineView | BMKMultiPolylineView.h | 分段颜色 |
| BMKMultiTexturePolylineView | BMKMultiPolylineView.h | 分段纹理（路况） |
| BMKCircle | BMKCircle.h | 圆形 |
| BMKCircleView | BMKCircleView.h | 圆形视图 |
| BMKPolygon | BMKPolygon.h | 多边形 |
| BMKPolygonView | BMKPolygonView.h | 多边形视图 |
| BMKGroundOverlay | BMKGroundOverlay.h | 图片图层 |
| BMKGroundOverlayView | BMKGroundOverlayView.h | 图片图层视图 |
| BMKTileLayer | BMKTileLayer.h | 瓦片图层基类 |
| BMKURLTileLayer | BMKTileLayer.h | URL 瓦片图层 |

### 曲线与渐变

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKArcline | BMKArcline.h | 圆弧 |
| BMKArclineView | BMKArclineView.h | 圆弧视图 |
| BMKGradientLine | BMKGradientLine.h | 渐变线 |
| BMKGradientLineView | BMKGradientLineView.h | 渐变线视图 |
| BMKGradientCircleView | BMKGradientCircleView.h | 渐变圆 |
| BMKGeodesicLine | BMKGeodesicLine.h | 大地线 |
| BMKGeodesicLineView | BMKGeodesicLineView.h | 大地线视图 |

### Marker

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKIconMarker | BMKIconMarker.h | 图标 Marker |
| BMKIconMarkerView | BMKIconMarkerView.h | 图标 Marker 视图 |
| BMKTextMarker | BMKTextMarker.h | 文本 Marker |
| BMKTextMarkerView | BMKTextMarkerView.h | 文本 Marker 视图 |
| BMKTextPathMarker | BMKTextPathMarker.h | 沿路径文字 |
| BMKTextPathMarkerView | BMKTextPathMarkerView.h | 沿路径文字视图 |

### 文本与海量点

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKText | BMKText.h | 文本 overlay |
| BMKTextView | BMKTextView.h | 文本 overlay 视图 |
| BMKMultiPointOverlay | BMKMultiPointOverlay.h | 海量点 |
| BMKMultiPointOverlayView | BMKMultiPointOverlayView.h | 海量点视图 |
| BMKMultiPointItem | BMKMultiPointOverlay.h | 海量点数据项 |

### 3D 与轨迹

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMK3DModelOverlay | BMK3DModelOverlay.h | 3D 模型 |
| BMK3DModelOverlayView | BMK3DModelOverlayView.h | 3D 模型视图 |
| BMKPrismOverlay | BMKPrismOverlay.h | 棱柱/3D 建筑 |
| BMKPrismOverlayView | BMKPrismOverlayView.h | 棱柱视图 |
| BMKTraceOverlay | BMKTraceOverlay.h | 路书轨迹 |
| BMKTraceOverlayView | BMKTraceOverlayView.h | 路书轨迹视图 |
| BMK3DTraceOverlay | BMK3DTraceOverlay.h | 3D 轨迹 |
| BMK3DTraceOverlayView | BMK3DTraceOverlayView.h | 3D 轨迹视图 |
| BMKMapTrackAnimation | BMKMapAnimation.h | 轨迹动画 |
| BMKCommonDef | BMKCommonDef.h | 枚举定义 |

详见 [annotations.md](annotations.md)、[overlays.md](overlays.md)。

## 检索

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKSuggestionSearch | BMKSuggestionSearch.h | 建议检索 |
| BMKGeoCodeSearch | BMKGeoCodeSearch.h | 地理编码 |
| BMKPOISearch | BMKPOISearch.h | POI |
| BMKBusLineSearch | BMKBusLineSearch.h | 公交线路 |
| BMKRouteSearch | BMKRouteSearch.h | 路线检索（算路见路线规划） |

## 路线规划

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKRouteSearch | BMKRouteSearch.h | 路线检索 |
| BMKDrivingRoutePlanOption | BMKRouteSearchOption.h | 驾车 |
| BMKWalkingRoutePlanOption | BMKRouteSearchOption.h | 步行 |
| BMKRidingRoutePlanOption | BMKRouteSearchOption.h | 骑行 |
| BMKTransitRoutePlanOption | BMKRouteSearchOption.h | 公交 |
| BMKPlanNode | BMKTypes.h | 路线节点（pt、name、cityName、cityID） |
| BMKDrivingRouteResult / BMKWalkingRouteResult 等 | BMKRouteSearchResult.h | 算路结果 |
| BMKDrivingStep / BMKWalkingStep 等 | BMKRouteSearchType.h | 路线步骤类型 |

## 步骑行导航（BaiduWalkNaviKit）

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKWalkNavigationManager | BMKWalkNavigationManager.h | 步行导航管理，单例；destroy、initNaviEngine、routePlanWithParams、startWalkNaviWithParentController、getBackgroundNavigationView |
| BMKCycleNavigationManager | BMKCycleNavigationManager.h | 骑行导航管理，单例；destroy、initNaviEngine、routePlanWithParams、naviCalcRoute:、startCycleNaviWithParentController、getBackgroundNavigationView |
| BMKWalkNaviLaunchParam | BMKWalkNaviLaunchParam.h | 步行算路参数（startNode/endNode，BMKWalkNaviRouteNodeInfo） |
| BMKCycleNaviLaunchParam | BMKCycleNaviLaunchParam.h | 骑行算路参数（startNode/endNode） |
| BMKWalkNaviRouteNodeInfo | BMKWalkNaviRouteNodeInfo.h | 步行起/终点节点（type BMKWalkNavigationRouteNodeLocation 等） |
| BMKCycleNaviRouteNodeInfo | BMKCycleNaviRouteNodeInfo.h | 骑行起/终点节点 |
| BMKWalkCycleNavigationOptions | BMKWalkCycleNavigationOptions.h | 初始化选项（displayOption 等） |
| BMKWalkCycleNavigationDisplayOption | BMKWalkCycleNavigationDisplayOption.h | 展示选项 |
| BMKWalkCycleSampleGuideInfo | BMKWalkCycleSampleGuideInfo.h | 诱导信息（SampleGuide） |
| BMKMultiNaviView | BMKMultiNaviView.h | 多实例导航地图 View（getNaviMapView） |

后台投屏类（BMKBackgroundMapView、BMKBackgroundNavigationView、BMKBackgroundRoadNetView）见下「后台与导航」。

详见 [navi.md](navi.md)。

## 热力图

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKHeatMap | BMKHeatMap.h | 热力图 |
| BMKHexagonHeatMap | BMKHexagonHeatMap.h | 六边形热力图 |

## 后台与导航

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKBackgroundMapView | BMKBackgroundMapView.h | 后台投屏容器（mapview + roadNetView + navigationView） |
| BMKBackgroundNavigationView | BMKBackgroundNavigationView.h | 导航层：路线、车标、罗盘、起终点；步骑行由 Manager.getBackgroundNavigationView 获取 |
| BMKBackgroundRoadNetView | BMKBackgroundRoadNetView.h | 路网层：路网、路况、路名；从 backgroundMapView.roadNetView 获取 |
| BMKNavigation | BMKNavigation.h | 调起百度地图 |
| BMKNaviPara | BMKNaviPara.h | 导航参数 |

## 坐标与结构体

| 类型 | 说明 |
|------|------|
| CLLocationCoordinate2D | 经纬度（BD09） |
| BMKMapRect | 直角地理坐标矩形 |
| BMKMapPoint | 直角地理坐标点 |
| BMKCoordinateRegion | 经纬度区域 |
| BMKCoordinateBounds | 经纬度边界 |

## 工具

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKGeometry | BMKGeometry.h | 坐标转换、几何计算 |
| BMKInterpolator | BMKInterpolator.h | 动画插值器 |
| BMKCommonDef | BMKCommonDef.h | 枚举定义 |

详见 [utils.md](utils.md)。
