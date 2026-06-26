# BMKMapView 地图视图

**边界**：地图视图、属性、生命周期、控制（BMKMapView）；标注见 [annotations.md](annotations.md)，覆盖物见 [overlays.md](overlays.md)。

## 概述

`BMKMapView` 继承 `UIView`，用于显示地图并执行相关操作。需配合 `BMKMapViewDelegate` 使用。

### 示例：创建地图与生命周期

```objc
#import <BaiduMapAPI_Base/BMKBaseComponent.h>
#import <BaiduMapAPI_Map/BMKMapComponent.h>

@property (nonatomic, strong) BMKMapView *mapView;

- (void)viewDidLoad {
    [super viewDidLoad];
    _mapView = [[BMKMapView alloc] initWithFrame:self.view.bounds];
    _mapView.delegate = self;
    [self.view addSubview:_mapView];
    // 可选：设置中心与缩放（改 centerCoordinate 不改变 zoomLevel）
    _mapView.centerCoordinate = CLLocationCoordinate2DMake(39.917, 116.379);
    _mapView.zoomLevel = 18;
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    [_mapView viewWillAppear];
}
- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];
    [_mapView viewWillDisappear];
}
```

### 示例：设置地图状态（带动画、指定时长）

```objc
// 使用 BMKMapStatus 设置层级与中心，带动画且指定动画时长(ms)
BMKMapStatus *status = [[BMKMapStatus alloc] init];
status.fLevel = 10;
status.targetGeoPt = CLLocationCoordinate2DMake(51.50556, -0.07556);
[_mapView setMapStatus:status withAnimation:YES withAnimationTime:1000];
```

### 示例：室内图

```objc
_mapView.baseIndoorMapEnabled = YES;
_mapView.showIndoorMapPoi = YES;
// 进入/移出室内图回调：mapView:baseIndoorMapWithIn:baseIndoorMapInfo:
```

## 地图引擎与生命周期

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKMapManager | BMKMapManager.h | 主引擎，`start:`、`setAgreePrivacy:` |
| BMKMapView | BMKMapView.h | 地图视图 |
| BMKMapStatus | BMKMapStatus.h | 地图状态（中心、缩放、旋转） |

**生命周期（必须调用）**：viewWillAppear/viewWillDisappear 必须调 mapView 对应方法，否则地图状态异常。

```objc
- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    [_mapView viewWillAppear];
}
- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];
    [_mapView viewWillDisappear];
}
```

### 地图显示当前定位

- 设置 **showsUserLocation = YES**，再通过 **updateLocationData:** 传入 **BMKUserLocation**（含 `location`、可选 `heading`），地图会绘制定位点。
- 定位数据需自行获取（如 BMKLocationManager 单次/连续定位）；与地图混用时坐标系须为 BD09（coordinateType 或转换），见 [location.md](location.md)。

```objc
_mapView.showsUserLocation = YES;
// 在拿到定位结果后（主线程）：
BMKUserLocation *userLoc = [BMKUserLocation new];
userLoc.location = [[CLLocation alloc] initWithLatitude:lat longitude:lng];
userLoc.updating = NO;
[_mapView updateLocationData:userLoc];
```

**注意**：仅在设置 showsUserLocation 且至少调用一次 updateLocationData 传入有效 CLLocation 后，地图上才会显示蓝点；未授权或定位失败时可不调用 updateLocationData。

**俯仰角**：`overlooking` 范围 -45～0，更陡需设 `minOverlooking`（-79～0）。`overlookEnabled` 是否支持俯仰角手势。

---

## 核心属性

### Delegate 与手势

| 属性 | 类型 | 说明 |
|------|------|------|
| delegate | id\<BMKMapViewDelegate\> | 地图回调 |
| gestureDelegate | id\<BMKMapGestureDelegate\> | 手势回调，返回 YES 时拦截地图处理 |

### 地图类型与语言

| 属性 | 类型 | 说明 |
|------|------|------|
| mapType | BMKMapType | 标准/卫星地图 |
| languageType | BMKMapLanguageType | 中/英文地图（since 6.4.0），V6.6.2 起英文不支持个性化地图 |
| backgroundColor | UIColor | 空白地图背景色（since 6.5.4） |
| backgroundImage | UIImage | 底图加载时背景网格（since 6.5.9，≤500KB） |

### 显示范围与中心

| 属性 | 类型 | 说明 |
|------|------|------|
| region | BMKCoordinateRegion | 当前经纬度范围 |
| limitMapRegion | BMKCoordinateRegion | 限制显示范围 |
| centerCoordinate | CLLocationCoordinate2D | 中心点（改值不改变 zoomLevel） |
| visibleMapRect | BMKMapRect | 当前可见范围（直角坐标） |

### 比例尺与视角

| 属性 | 类型 | 说明 |
|------|------|------|
| zoomLevel | float | 比例尺级别，手机 4～21 |
| minZoomLevel / maxZoomLevel | float | 自定义最小/最大级别 |
| rotation | int | 旋转角度 -180～180 |
| overlooking | int | 俯视角度 -45～0 |
| minOverlooking | int | 俯视最小值 -79～0 |
| fontSizeLevel | NSInteger | 字体大小 0～3（小/标准/大/特大，since 6.3.0） |

### 控件与 UI

| 属性 | 类型 | 说明 |
|------|------|------|
| compassPosition | CGPoint | 指南针位置（以左上角为原点） |
| compassSize | CGSize | 指南针宽高（只读） |
| showMapScaleBar | BOOL | 是否显示比例尺 |
| mapScaleBarPosition | CGPoint | 比例尺位置（以 BMKMapView 左上角为原点）；默认与 Logo 重叠，需手动设置使比例尺在 Logo 上方，见 [ui-standards.md](ui-standards.md) |
| mapScaleBarSize | CGSize | 比例尺宽高（只读） |
| mapScaleBarColor / mapScaleBarTextColor | UIColor | 比例尺颜色 |
| logoPosition | BMKLogoPosition | Logo 位置 |

### 图层与显示

| 属性 | 类型 | 说明 |
|------|------|------|
| buildingsEnabled | BOOL | 3D 楼块 |
| showMapPoi | BOOL | 底图 POI 标注 |
| trafficEnabled | BOOL | 路况图层 |
| customTrafficColorEnabled | BOOL | 自定义路况颜色生效（since 6.6.3） |
| baiduHeatMapEnabled | BOOL | 百度城市热力图（层级>11 可显示） |

### 手势

| 属性 | 类型 | 说明 |
|------|------|------|
| gesturesEnabled | BOOL | 所有手势 |
| doubleTapHoldPanEnabled | BOOL | 单指双击滑动缩放，默认 NO |
| zoomEnabled | BOOL | 双指缩放 |
| zoomEnabledWithTap | BOOL | 双击/双指单击缩放 |
| scrollEnabled | BOOL | 移动地图 |
| overlookEnabled | BOOL | 俯仰角 |
| rotateEnabled | BOOL | 旋转 |
| forceTouchEnabled | BOOL | 3D Touch 回调 |
| gestureZoomAnimationEnabled | BOOL | 手势缩放动画（since 6.5.2） |

**手势冲突（地图+ScrollView 共存）**：实现 `shouldRecognizeSimultaneouslyWithGestureRecognizer:` 返回 YES。ScrollView 配置见 [ui-standards.md](ui-standards.md)。

**BMKMapGestureDelegate**：handleTapGesture、handlePanGesture、handleFlyingGesture、handleLongGesture、handleDoubleTapGesture、handleTwoFingersTapGesture、handleTwoFingersPanGesture、handleRotationGesture、handlePinchGesture；返回 YES 时地图不处理。用于与底部抽屉、侧滑菜单等共存。

**BMKAnnotationView/BMKActionPaopaoView**：不推荐直接添加手势，会覆盖点击、长按；如必须添加，将手势 delegate 设到对应 View 并实现协调方法。

### 其他

| 属性 | 类型 | 说明 |
|------|------|------|
| mapPadding | UIEdgeInsets | 地图预留边界；设置后 Logo、比例尺、指南针会避开该区域 |
| updateTargetScreenPtWhenMapPaddingChanged | BOOL | mapPadding 改变时中心是否跟着变 |
| ChangeWithTouchPointCenterEnabled | BOOL | 双指以手势中心/地图中心旋转缩放 |
| ChangeCenterWithDoubleTouchPointEnabled | BOOL | 双击以双击位置/地图中心放大 |
| supportBackgroundDraw | BOOL | 后台绘制（since 6.6.6，进出前后台时设置） |

**mapPadding 与 fitVisibleMapRect edgePadding 区别**：mapPadding 影响指南针、Logo、比例尺位置，用于解决控件被 UI 遮挡；fitVisibleMapRect 的 edgePadding 用于路线视野适配（含 UI 边距和 marker 尺寸）。二者解决不同问题，详见 [ui-standards.md](ui-standards.md)。

---

## 类方法（创建前设置）

| 方法 | 说明 |
|------|------|
| `+ setBaiduMapSDKMetalEnable:` | 是否用 Metal 绘制（V6.5.2，创建前有效） |
| `+ getBaiduMapSDKMetalEnable` | 获取 Metal 开关（V6.6.3） |
| `+ setBaiduMapSDKOverlayNewVersionEnable:` | 覆盖物新版逻辑（V6.5.9，启动期间仅一次） |
| `+ getBaiduMapSDKOverlayNewVersionEnable` | 获取覆盖物新版开关（V6.6.3） |

---

## 实例方法

### 生命周期（必须调用）

| 方法 | 说明 |
|------|------|
| `viewWillAppear` | 即将显示时调用，恢复状态 |
| `viewWillDisappear` | 即将隐藏时调用，存储状态 |

### 地图控制

| 方法 | 说明 |
|------|------|
| `setRegion:animated:` | 设定显示范围 |
| `setCenterCoordinate:animated:` | 设定中心点 |
| `setVisibleMapRect:animated:` | 设定可见范围（直角坐标） |
| `setVisibleMapRect:edgePadding:animated:` | 设定范围并留边距 |
| `fitVisibleMapRect:edgePadding:withAnimated:` | 适配 mapRect 到可见区域 |
| `zoomIn` / `zoomOut` | 放大/缩小一级 |
| `mapForceRefresh` | 强制刷新 |
| `cleanCacheWithMapType:` | 清空缓存 |

### 坐标转换

| 方法 | 说明 |
|------|------|
| `convertCoordinate:toPointToView:` | 经纬度→View 坐标 |
| `convertPoint:toCoordinateFromView:` | View 坐标→经纬度 |
| `convertRegion:toRectToView:` | 经纬度区域→View 矩形 |
| `convertRect:toRegionFromView:` | View 矩形→经纬度区域 |
| `convertMapRect:toRectToView:` | BMKMapRect→View 矩形 |
| `convertRect:toMapRectFromView:` | View 矩形→BMKMapRect |
| `screenPointFromMapPoint3:` | 三维地理坐标→屏幕坐标（since 6.5.2） |
| `glPointForMapPoint:` | BMKMapPoint→OpenGL 坐标 |
| `glPointsForMapPoints:count:` | 批量 BMKMapPoint→OpenGL 坐标 |

### 地图状态

| 方法 | 说明 |
|------|------|
| `getMapStatus` | 获取地图状态 |
| `setMapStatus:` | 设置地图状态 |
| `setMapStatus:withAnimation:` | 设置并动画 |
| `setMapStatus:withAnimation:withAnimationTime:` | 指定动画时长(ms) |
| `getMapStatusFromCoordinateRegion:edgePadding:` | 根据区域和边距计算 BMKMapStatus |
| `setMapCenterToScreenPt:` | 设置中心点屏幕坐标 |

**设置状态并动画**：见上文「示例：设置地图状态（带动画、指定时长）」；不指定时长用 `setMapStatus:withAnimation:` 则使用 SDK 默认动画时长。

### 截图与路况

| 方法 | 说明 |
|------|------|
| `takeSnapshot` | 可视区域截图 |
| `takeSnapshot:` | 指定区域截图 |
| `setCompassImage:` | 设置罗盘图片 |
| `setCustomTrafficColorForSmooth:slow:congestion:severeCongestion:` | 自定义路况颜色（4 种全设） |
| `isSurpportBaiduHeatMap` | 当前区域是否支持百度热力图 |

### OpenGL（3D 绘制）

| 方法 | 说明 |
|------|------|
| `getProjectionMatrix` | 获取投影矩阵 |
| `getViewMatrix` | 获取视图矩阵 |

---

## Category：CustomMapAPI

| 方法 | 说明 |
|------|------|
| `setCustomMapStylePath:` | 个性化地图样式路径（创建后调用，V6.6.2 英文不支持） |
| `setCustomMapStylePath:mode:` | mode 0 本地 1 在线 |
| `setCustomMapStyleEnable:` | 个性化样式开关 |
| `setCustomMapStyleWithOption:preLoad:success:failure:` | 在线个性化样式 |

---

## Category：IndoorMapAPI

| 属性/方法 | 说明 |
|------|------|
| baseIndoorMapEnabled | 是否显示室内图 |
| showIndoorMapPoi | 室内图标注 |
| showDotPoi | 麻点 POI |
| `switchBaseIndoorMapFloor:withID:` | 切换楼层 |
| `getFocusedBaseIndoorMapInfo` | 当前聚焦室内图信息 |

---

## Category：LocationViewAPI

| 属性/方法 | 说明 |
|------|------|
| showsUserLocation | 是否显示定位图层 |
| userTrackingMode | 定位模式 |
| userLocationVisible | 定位点是否在可视区域（只读） |
| `updateLocationViewWithParam:` | 定制我的位置样式 |
| `updateLocationData:` | 更新定位数据 |

---

## Category：AnnotationAPI

| 属性/方法 | 说明 |
|------|------|
| annotations | 已添加标注数组（只读） |
| isSelectedAnnotationViewFront | 选中标注是否置顶 |
| `addAnnotation:` / `addAnnotations:` | 添加标注 |
| `removeAnnotation:` / `removeAnnotations:` | 移除标注 |
| `viewForAnnotation:` | 查找标注对应 View |
| `dequeueReusableAnnotationViewWithIdentifier:` | 复用标注 View |
| `selectAnnotation:animated:` / `deselectAnnotation:animated:` | 选中/取消选中 |
| `showAnnotations:animated:` | 显示区域包含所有标注 |
| `showAnnotations:padding:animated:` | 带边距（since 6.5.7） |
| `annotationsInCoordinateBounds:` | 矩形区域内标注 |

---

## Category：OverlaysAPI

| 属性/方法 | 说明 |
|------|------|
| overlays | 已添加 overlay 数组（只读） |
| `addOverlay:` / `addOverlays:` | 添加 overlay |
| `removeOverlay:` / `removeOverlays:` | 移除 overlay |
| `insertOverlay:atIndex:` | 指定索引插入 |
| `exchangeOverlayAtIndex:withOverlayAtIndex:` | 交换 |
| `insertOverlay:aboveOverlay:` / `belowOverlay:` | 相对插入 |
| `viewForOverlay:` | 查找 overlay 对应 View |

---

## Category：HeatMapAPI

| 方法 | 说明 |
|------|------|
| `addHeatMap:` | 添加热力图 |
| `updateHeatMap:` | 更新热力图（会重置动画） |
| `removeHeatMap` | 移除热力图 |
| `startHeatMapFrameAnimation` / `stopHeatMapFrameAnimation` | 开始/暂停动画 |
| `setHeatMapFrameAnimationIndex:` | 控制帧索引 |

---

## Category：HexagonHeatMapAPI（since 6.6.0）

| 属性/方法 | 说明 |
|------|------|
| showHexagonHeatMap | 是否显示蜂窝热力图 |
| `addHexagonHeatMap:` | 添加 |
| `removeHexagonHeatMap` | 删除 |

---

## Category：MapLayerAPI

| 属性/方法 | 说明 |
|------|------|
| showOperateLayer | 运营图层（since 6.4.0） |
| showOperatePOILayer | 运营 POI 图层（since 6.6.3） |
| showTrafficUGCLayer | 路况事件图层（since 6.6.3） |
| showDEMLayer | 地形图层（since 6.5.9） |
| `switchLayerOrder:otherLayer:` | 交换图层顺序（since 6.5.9） |
| `switchOverlayLayerAndNavigationLayer:` | overlay 与导航图层交换 |
| `switchOverlayLayerAndPOILayer:` | overlay 与 POI 图层交换（addOverlay 后调用） |
| `getPoiTagEnable:` / `setPoiTagEnable:poiTagType:` | 底图 POI 标签显示 |

---

## Category：ParticleEffect（since 6.5.7）

| 方法 | 说明 |
|------|------|
| `showParticleEffect:` | 显示粒子效果 |
| `closeParticleEffect:` | 关闭粒子效果 |
| `customParticleEffect:option:` | 自定义粒子效果 |

---

## BMKBackgroundMapView（后台投屏视图）

**BMKBackgroundMapView**（BMKBackgroundMapView.h）用于将**地图或导航画面**渲染到自定 View，可置于外接屏、投屏窗口或本机副区域，常用于**步骑行多实例后台投屏**：导航进行时把同一段导航同时投到另一块屏或小窗。

### 三层内容与对应类

BMKBackgroundMapView 支持三类内容，通过以下属性挂接：

| 属性 | 类型 | 支持的内容 | 说明 |
|------|------|-------------|------|
| **mapview** | BMKMapView | 底图 | 关联源地图，同步数据；步骑行多实例时可设为 `[multiNaviView getNaviMapView]` |
| **roadNetView** | BMKBackgroundRoadNetView | 路网、路况、路名 | 只读获取，用于自定义路网样式（见下） |
| **navigationView** | BMKBackgroundNavigationView | 导航路线、小车、罗盘、起终点等 | 步骑行由 Manager 的 `getBackgroundNavigationView` 得到并赋值（见下） |

渲染控制：设置完成后调用 **`startRender`**，退出或暂停时 **`stopRender`**，再 `removeFromSuperview`。完整步骑行投屏流程见 [navi.md](navi.md)「多实例后台投屏」。

### BMKBackgroundNavigationView 支持的内容

用于在投屏上绘制**导航相关**内容，步骑行场景下由 **BMKWalkNavigationManager** / **BMKCycleNavigationManager** 的 **`getBackgroundNavigationView`** 返回，引擎会驱动路线与位置更新，无需自行调用 `updateRouteInfo:` 等。

| 能力 | 属性/方法 | 说明 |
|------|-----------|------|
| 路线 | routeColor, routePassedColor, routePassedDisplayMode（如 Grayed） | 未走/已走路线颜色与显示模式 |
| 起终点与途径点 | needDrawStartPoint, needDrawEndPoint, needDrawViaPoint；startPointIcon, endPointIcon, viaPointIcon 等 | 是否绘制及图标 |
| 导航车标与罗盘 | navigationIcon, needDrawCompass, needFllowPhoneHeading | 车头朝向、罗盘、随手机朝向 |
| 引导线（偏航） | needDrawGuideLine, guideLineColor, guideLineWidth | 偏离路线时的引导线 |
| 路名 | needDrawRouteName, routeNameFont, routeNameTextColor 等 | 路线上的路名绘制 |
| 数据更新（非步骑行自管时） | updateRouteInfo:, updateRouteSegmentsInfo:, updateNaviLocationInfo: | 自管数据源时使用；步骑行由 Manager 提供实例则不需要 |

### BMKBackgroundRoadNetView 支持的内容

从 **`backgroundMapView.roadNetView`** 只读获取，用于在底图之上自定义**路网层**样式（不改变地图数据，仅表现）。

| 能力 | 属性 | 说明 |
|------|------|------|
| 路网 | needDrawRoadNet, roadNetColor | 是否绘制路网、路网颜色 |
| 路况 | needDrawRoadTraffic, roadTrafficColor | 是否绘制路况；需关联 mapview 的 trafficEnabled 为 YES；颜色数组 count 为 5（未知/畅通/缓行/拥挤/严重拥堵） |
| 路名 | needDrawRoadName, roadNameFont, roadNameTextColor | 是否绘制路名及字体、颜色 |

渲染由 BMKBackgroundMapView 的 startRender 统一驱动；roadNetView 的 **mapview** 需与 backgroundMapView 的 mapview 一致以同步数据。

### BMKBackgroundMapView 自身属性与接口

| 属性/方法 | 类型/说明 |
|-----------|-----------|
| **mapview** | BMKMapView，关联源地图 |
| **navigationView** | BMKBackgroundNavigationView，步骑行时设为 Manager 的 `getBackgroundNavigationView` |
| **roadNetView** | BMKBackgroundRoadNetView（只读），用于配置路网/路况/路名 |
| **frameRate** | NSInteger，渲染帧率，默认 30，范围 10～60 |
| **enable3D** | BOOL，默认 YES |
| **showScaleBar** | BOOL，是否显示比例尺 |
| **mapScreenExtOffset** | CGPoint，地图额外偏移（微调车标位置等） |
| **startRender** / **stopRender** | 开始/停止渲染 |
| **takeSnapshot:needLogo:** | 截屏 |

---

## BMKMapViewDelegate 回调

### 生命周期与渲染

| 回调 | 说明 |
|------|------|
| `mapViewWillBackground:` | 退到后台前 |
| `mapViewDidForeground:` | 进入前台后 |
| `mapViewDidFinishLoading:` | 地图初始化完毕 |
| `mapViewDidRenderValidData:withError:` | 绘制出有效数据 |
| `mapViewDidFinishRendering:` | 渲染完毕 |
| `mapView:onDrawMapFrame:` | 每帧绘制、重绘时 |

### 区域变化

| 回调 | 说明 |
|------|------|
| `mapView:regionWillChangeAnimated:` | 区域即将改变 |
| `mapView:regionWillChangeAnimated:reason:` | 带原因（Gesture/Event/APIs） |
| `mapView:regionDidChangeAnimated:` | 区域改变完成 |
| `mapView:regionDidChangeAnimated:reason:` | 带原因 |

### 标注

| 回调 | 说明 |
|------|------|
| `mapView:viewForAnnotation:` | 根据 annotation 生成 View（必须实现） |
| `mapView:didAddAnnotationViews:` | 新添加 annotation views |
| `mapView:clickAnnotationView:` | 点击 annotation view |
| `mapView:didSelectAnnotationView:` | 选中 |
| `mapView:didDeselectAnnotationView:` | 取消选中 |
| `mapView:annotationView:didChangeDragState:fromOldState:` | 拖拽状态变化 |
| `mapView:annotationViewForBubble:` | 点击气泡 |

### 覆盖物

| 回调 | 说明 |
|------|------|
| `mapView:viewForOverlay:` | 根据 overlay 生成 View（必须实现） |
| `mapView:didAddOverlayViews:` | 新添加 overlay views |
| `mapView:onClickedBMKOverlayView:` | 点击覆盖物 |

### 地图点击

| 回调 | 说明 |
|------|------|
| `mapView:onClickedMapPoi:` | 点击底图标注 |
| `mapView:onClickedMapBlank:` | 点击空白处 |
| `mapview:onDoubleClick:` | 双击 |
| `mapview:onLongClick:` | 长按 |
| `mapview:onForceTouch:force:maximumPossibleForce:` | 3D Touch |

### 其他

| 回调 | 说明 |
|------|------|
| `mapStatusDidChanged:` | 地图状态改变完成 |
| `mapview:baseIndoorMapWithIn:baseIndoorMapInfo:` | 进入/移出室内图 |
| `mapView:didChangeUserTrackingMode:` | 定位模式切换 |
| `mapViewOnClickCompass:` | 点击指南针 |

---

## 相关枚举与类型

### BMKUserTrackingMode

| 值 | 说明 |
|------|------|
| None | 普通定位 |
| Heading | 定位方向 |
| Follow | 定位跟随 |
| FollowWithHeading | 定位罗盘 |

### BMKLogoPosition

左/中/右 × 上/下 共 6 种。

### BMKRegionChangeReason

| 值 | 说明 |
|------|------|
| Gesture | 手势 |
| Event | 控件事件 |
| APIs | 接口调用 |

### BMKMapParticleEffect

雪、雨、雾霾、沙尘暴、烟花、花瓣等。

### BMKMapPoi

底图点击返回：`text`、`pt`、`uid`、`trafficUGCType`。

### BMKLayerType

kBMKLayerSDKOverlay、kBMKLayerSDKHeatMap、kBMKLayerSDKHexagonHeatMap、kBMKLayerNewSDKDefaultOverlay。
