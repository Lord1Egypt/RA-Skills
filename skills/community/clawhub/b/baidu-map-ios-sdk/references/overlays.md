# 覆盖物 (Overlay)

**边界**：addOverlay 体系；标注见 [annotations.md](annotations.md)，地图 API 见 [mapview.md](mapview.md)。**必须遵守**：点标注**优先使用 Marker**（本 addOverlay 体系），不得使用 BMKPointAnnotation/BMKPinAnnotationView，除非点聚合、固定屏选点等例外。见 [SKILL.md](../SKILL.md) 规则 3。

## 路线与起终点：纹理优先（必须遵守）

**绘制路线与起终点覆盖物时，须优先使用纹理，仅无可用纹理时再使用纯色或自绘。**

- **路线折线**
  - 单色/单纹理：`BMKPolyline` + `BMKPolylineView`。**优先**设置 `view.textureImage`（图片宽高须为 2 的 n 次幂），无纹理时再设 `view.strokeColor`。线宽 8pt，见 [ui-standards.md](ui-standards.md)。
  - 路况分段：`BMKMultiPolyline` + `BMKMultiTexturePolylineView`，`textureImages` 使用 [assets](assets.md) 提供的 traffic_texture_* 等。
- **起终点 Marker**
  - `BMKIconMarker.icon` **须优先**使用 [assets](assets.md) 的 **icon_start**（起点）、**icon_end**（终点）；实现时先 `[UIImage imageNamed:@"icon_start"]` / `imageNamed:@"icon_end"`，为 nil 再回退到自绘或纯色。
- **小车图标**：见 [SKILL.md](../SKILL.md) 规则 3「路线小车纹理」及 [assets](assets.md)。

生成或修改覆盖物相关代码时，**必须先检查并应用上述纹理优先**，避免仅写 strokeColor/自绘导致规范未生效。

## 使用须知
- **Delegate**：addOverlay 前必须设置 `mapView.delegate`，并实现 `mapView:viewForOverlay:`。
- **批量添加**：`addOverlays:` 可一次添加多个 overlay。
- **起终点推荐 BMKIconMarker**：添加顺序为路线→起终点→小车。起终点 icon 须优先使用 [assets](assets.md) 的 icon_start/icon_end；小车图标须优先使用技能 [assets](assets.md) 纹理（icon_car 等），无则再颜色/自绘。样式见 [ui-standards.md](ui-standards.md)。
- **步骑行多路线折线**：BaiduWalkNaviKit 的 `displayRoutePlanResult:mapView` 返回 `NSArray<BMKPolyline *>`；若由业务侧 addOverlay，需在 `mapView:viewForOverlay:` 中对 `BMKPolyline` 返回 `BMKPolylineView`（如 textureImage 或 strokeColor、lineWidth），否则路线不显示。

## 示例：添加折线（Overlay，addOverlay）

需实现 `mapView:viewForOverlay:`，根据 overlay 类型返回对应 View。

```objc
CLLocationCoordinate2D coords[2] = {
    CLLocationCoordinate2DMake(39.915, 116.404),
    CLLocationCoordinate2DMake(39.920, 116.410)
};
BMKPolyline *polyline = [BMKPolyline polylineWithCoordinates:coords count:2];
[mapView addOverlay:polyline];

#pragma mark - BMKMapViewDelegate
- (BMKOverlayView *)mapView:(BMKMapView *)mapView viewForOverlay:(id<BMKOverlay>)overlay {
    if ([overlay isKindOfClass:[BMKPolyline class]]) {
        BMKPolylineView *view = [[BMKPolylineView alloc] initWithOverlay:overlay];
        // 纹理优先：有纹理图时设置 textureImage（宽高须 2 的 n 次幂），无则 strokeColor
        UIImage *tex = [UIImage imageNamed:@"route_texture"];  // 示例；可用 assets 或自备
        if (tex) view.textureImage = tex;
        else view.strokeColor = [UIColor blueColor];
        view.lineWidth = 8.0f;  // 路线线宽 8pt，见 ui-standards
        return view;
    }
    return nil;
}
```

## 示例：添加图标 Marker（Overlay，addOverlay）

点标注推荐用 BMKIconMarker（addOverlay），与地图坐标系一致；anchor 沿路线居中时设 0.5/0.5。

```objc
BMKIconMarker *marker = [[BMKIconMarker alloc] init];
marker.coordinate = CLLocationCoordinate2DMake(39.915, 116.404);
// 起终点纹理优先：起点用 icon_start，终点用 icon_end，无则回退自绘/纯色
marker.icon = [UIImage imageNamed:@"icon_start"];  // 或 icon_end / icon_pin
if (!marker.icon) marker.icon = [self drawDefaultPinImage];  // 回退
marker.anchorX = 0.5;  // 沿路线居中时 0.5/0.5，否则默认 anchorY=1 坐标在底部中心
marker.anchorY = 0.5;
[mapView addOverlay:marker];

#pragma mark - BMKMapViewDelegate
- (BMKOverlayView *)mapView:(BMKMapView *)mapView viewForOverlay:(id<BMKOverlay>)overlay {
    if ([overlay isKindOfClass:[BMKIconMarker class]]) {
        BMKIconMarkerView *view = [[BMKIconMarkerView alloc] initWithOverlay:overlay];
        view.isClickable = YES;  // 点击触发 mapView:onClickedBMKOverlayView:
        return view;
    }
    return nil;
}
```

## 常用默认值（易导致不生效或与预期不符）

以下为地图/覆盖物相关类常见默认值，未显式设置时可能造成行为差异，建议按需显式赋值。

| 类/接口 | 属性/方法 | 默认值 | 说明 |
|---------|-----------|--------|------|
| BMKMapTrackAnimation | setTrackPosRadio | **0.0 ~ 0.0**（无有效范围） | 轨迹动画**必须**显式调用 `setTrackPosRadio:0.0 to:1.0`，否则无有效播放范围 |
| BMKMapTrackAnimation / BMKMapAnimationSet | start | **不自动 start** | 需手动调用 `start`；其他动画类型默认自动 start |
| BMKIconMarker | anchorX / anchorY | **0.5 / 1.0** | 坐标在图标底部中心；沿路线居中时设 0.5/0.5 |
| BMKMultiColorPolylineView | lineCapType | **kBMKLineCapButt** | 不支持虚线；kBMKLineCapRound 支持虚线 |
| BMKMapView | setMapStatus:withAnimation: | 动画时长为 SDK 默认 | 需指定时长时用 `setMapStatus:withAnimation:withAnimationTime:`（单位 ms） |
| 定位 SDK（BMKLocationManager） | coordinateType | **BMKLocationCoordinateTypeGCJ02** | 与地图（BD09）混用时须设为 BMK09LL 或做转换，见 [location.md](location.md) |

## 覆盖物

### 基础覆盖物

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKOverlay | BMKOverlay.h | 覆盖物协议 |
| BMKOverlayView | BMKOverlayView.h | 覆盖物视图基类 |
| BMKPolyline | BMKPolyline.h | 单色/单纹理折线 |
| BMKPolylineView | BMKPolylineView.h | 折线视图，支持 textureImage、lineDashType |
| BMKMultiPolyline | BMKMultiPolyline.h | 分段折线，需 drawIndexs |
| BMKMultiColorPolylineView | BMKMultiPolylineView.h | 分段颜色 |
| BMKMultiTexturePolylineView | BMKMultiPolylineView.h | 分段纹理（路况） |
| BMKCircle | BMKCircle.h | 圆形 |
| BMKCircleView | BMKCircleView.h | 圆形视图 |
| BMKPolygon | BMKPolygon.h | 多边形 |
| BMKPolygonView | BMKPolygonView.h | 多边形视图 |
| BMKGroundOverlay | BMKGroundOverlay.h | 图片图层 |
| BMKGroundOverlayView | BMKGroundOverlayView.h | 图片图层视图 |

**折线**：`BMKPolyline polylineWithCoordinates:count:`。`BMKPolylineView.textureImage` 要求图片宽高为 2 的 n 次幂。**路线线宽**标准 **8pt**，见 [ui-standards.md](ui-standards.md)。`lineDashType`：`kBMKLineDashTypeDot`（圆点虚线）、`kBMKLineDashTypeSquare` 等。

**分段折线**：`BMKMultiPolyline multiPolylineWithCoordinates:count:drawIndexs:`，drawIndexs 为 NSNumber 数组，对应 strokeColors 或 textureImages 索引。`BMKMultiColorPolylineView.lineCapType` 默认 `kBMKLineCapButt`（不支持虚线），`kBMKLineCapRound` 支持。`BMKMultiTexturePolylineView.lineJoinType`：`kBMKLineJoinRound`/`Bevel`/`Miter`。

**镂空**：BMKCircle、BMKPolygon 支持 `hollowShapes`，可传入 BMKCircle、BMKPolygon 数组实现镂空。

**圆形**：`BMKCircle circleWithCenterCoordinate:radius:`，radius 单位米。BMKCircleView 设置 `fillColor`、`strokeColor`、`lineWidth`。

**多边形**：`BMKPolygon polygonWithCoordinates:count:`。BMKPolygonView 支持 `lineDashType`。

**图片图层**：`BMKGroundOverlay groundOverlayWithBounds:icon:`（BMKCoordinateBounds：southWest、northEast）；或 `groundOverlayWithPosition:zoomLevel:anchor:icon:`。`alpha` 控制透明度 [0, 1]。

### 曲线与渐变

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKArcline | BMKArcline.h | 圆弧（3 点确定） |
| BMKArclineView | BMKArclineView.h | 圆弧视图 |
| BMKGradientLine | BMKGradientLine.h | 渐变线 |
| BMKGradientLineView | BMKGradientLineView.h | 渐变线视图 |
| BMKGradientCircleView | BMKGradientCircleView.h | 渐变圆（BMKCircle + 渐变） |
| BMKGeodesicLine | BMKGeodesicLine.h | 大地线（球面最短路径） |
| BMKGeodesicLineView | BMKGeodesicLineView.h | 大地线视图 |

**圆弧**：`BMKArcline arclineWithCoordinates:` 需传入 3 个点。

**渐变线**：`BMKGradientLine gradientLineWithCoordinates:count:drawIndexs:`，用法类似 BMKMultiPolyline。BMKGradientLineView 设置 `strokeColors`、`lineWidth`。

**渐变圆**：BMKGradientCircleView 用 `initWithOverlay:` 传入 BMKCircle。`radiusWeight`、`colorWeight` 控制渐变规则；`centerColor`、`sideColor` 为渐变起止色。

**大地线**：`BMKGeodesicLine geodesicLineWithCoordinates:count:`。经度跨 180° 时须设置 `lineDirectionCross180`（如 `kBMKLineDirectionCross180TypeWEST_TO_EAST`）。**沿大地线模拟移动**：用球面线性插值 slerp 从 origin 到 dest，`coord = slerp(origin, dest, progress)`；`BMKGetDirectionFromCoords(current, slerp(origin,dest, progress+0.02))` 得切线方向。往返飞行：`routeDirection` 1 或 -1 切换，回程 `coord = slerp(dest, origin, 1-progress)`。slerp 公式见 [utils.md](utils.md)。

### Marker 类（addOverlay）

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKIconMarker | BMKIconMarker.h | 图标 Marker |
| BMKIconMarkerView | BMKIconMarkerView.h | 图标 Marker 视图 |
| BMKTextMarker | BMKTextMarker.h | 文本 Marker |
| BMKTextMarkerView | BMKTextMarkerView.h | 文本 Marker 视图 |
| BMKTextPathMarker | BMKTextPathMarker.h | 沿路径文字 |
| BMKTextPathMarkerView | BMKTextPathMarkerView.h | 沿路径文字视图 |

**BMKIconMarker**：`icon` 单图，`icons` 图片组（按间隔轮播）。`scaleX`/`scaleY`、`anchorX`/`anchorY`（默认 0.5/1.0）。**沿路线居中**：设置 `anchorX = 0.5`、`anchorY = 0.5`，否则默认 anchorY=1 使坐标在图标底部中心，圆心会偏上。`addRichView:` 挂接 BMKRichView（BMKImageUIView、BMKLabelUIView、BMKVerticalLayout、BMKHorizontalLayout），RichView 无坐标，必须挂到 marker 上。

**BMKIconMarker 旋转**：`marker.rotateFeature = BMKRotateItem | BMKRotateGeoNorth`（地理北为基准，与 BMKGetDirectionFromCoords 一致）。基准图标建议机头朝上，`marker.rotate = heading`；若方向相反可试 `rotate = -heading` 或 `heading ± 90`。沿大地线移动时用「当前点→路径稍前点」算切线：`BMKGetDirectionFromCoords(current, slerpCoord(origin,dest, progress+0.02))`。

**BMKRichView 示例**：BMKLabelUIView + BMKTextStyle + BMKVerticalLayout，`richView.locate = BMKLocateBottom`、`offsetY` 控制位置。`rootView = layout`，`[marker addRichView:richView]`。

**碰撞检测**：`marker.collisionBehavior = BMKCollisionWithInner | BMKCollisionHideByPriority`，`collisionPriority` 越大越不易被遮挡。RichView 同理。**注意**：动画中暂不支持，定时器驱动的位置更新可生效。

**BMKTextMarker**：`text`、`style`（BMKTextStyle：fontSize、fontOption、borderWidth、textColor、borderColor）。

**BMKTextPathMarker**（路线路名沿路径绘制）：用 `textPathMarkerWithPoints:count:` 或 `textPathMarkerWithCoordinates:count:` 传入路径点（如 BMKDrivingStep 的 points/count），再设 `text`（路名）、`style`（BMKTextStyle，如 22pt 黑字白边见 [ui-standards.md](ui-standards.md)）。View 为 **BMKTextPathMarkerView**，`initWithMarker:` 传入 marker。路线规划时每段 step 若有 `roadName` 可创建一条 BMKTextPathMarker 沿该 step 的 points 绘制，路名随路径走向展示。

**动画**：BMKMapScaleAnimation、BMKMapRotateAnimation、BMKMapAlphaAnimation、BMKMapAnimationSet。BMKMapTrackAnimation、BMKMapAnimationSet 默认不自动 start，其他动画默认自动 start。`addAnimation:addAnimationSetOrderType:` 支持 `BMKAnimationSetOrderTypeWith`（并行）、`BMKAnimationSetOrderTypeThen`（串行）。

**轨迹动画（BMKMapTrackAnimation）**：polyline 与 BMKIconMarker **必须共用同一 trackAnim**，否则小车不显示；只 `start` 一次。路线推荐 BMKMultiPolyline + BMKMultiTexturePolylineView；Forward=未走过（原色），Backward=已走过（灰度）。**走过置灰**（BMKGeometryView）：`strokeColorProgressForward`=原色（未走过）、`strokeColorProgressBackward`=灰色（已走过）；模拟导航同此。轨迹回放相反。驾车路况：drawIndexs 来自 traffics，textureImages 5 种（0 无数据/1 畅通/2 缓行/3 拥堵/4 严重拥堵），见 [assets.md](assets.md)。停止仅 `cancel`，勿解绑 overlay.animation。

**动画不显示时排查**（不建议用 CADisplayLink 等手动方案替代）：

| 检查项 | 说明 |
|--------|------|
| 共用同一实例 | `polyline.animation` 与 `marker.animation` 必须指向**同一个** BMKMapTrackAnimation |
| setTrackLine | 调用 `[trackAnim setTrackLine:polyline]`；部分场景需**先 addOverlay:polyline 再 setTrackLine** |
| setTrackPosRadio | **必须**调用 `[trackAnim setTrackPosRadio:0.0 to:1.0]`，默认 0~0 无有效范围 |
| 添加顺序 | 先 `addOverlay:polyline`，再 `addOverlay:marker` |
| trackBy | marker 设置 `trackBy = BMKAnimationTrackXY`；可加 `BMKAnimationTrackForward` 尝试使机头沿线段前进方向旋转（效果因场景而异，若方向仍不对改用 BMKRotateItem 手动计算 heading） |
| 只 start 一次 | 对所有 trackAnim 只调用一次 `start`；可 `dispatch_async` 到下一 RunLoop |
| polyline.isThined | 设为 NO，避免抽稀导致轨迹点丢失 |
| 参考 Demo | 对照官方 `BMKPolylineMarkerTeackAnimationPage.mm` |

**点击**：`BMKIconMarkerView`/`BMKTextMarkerView.isClickable = YES` 后，点击触发 `mapView:onClickedBMKOverlayView:`。

### 文本与海量点

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKText | BMKText.h | 文本 overlay（中心+文字） |
| BMKTextView | BMKTextView.h | 文本 overlay 视图 |
| BMKMultiPointOverlay | BMKMultiPointOverlay.h | 海量点 |
| BMKMultiPointOverlayView | BMKMultiPointOverlayView.h | 海量点视图 |
| BMKMultiPointItem | BMKMultiPointOverlay.h | 海量点数据项 |

**BMKText**：`textWithCenterCoordinate:text:`。BMKTextView 设置 `textColor`、`backgroundColor`、`fontSize`、`textFontType`、`textAlignment`、`textMaxLineWidth`、`textLineSpacing`、`textParagraphSpacing`、`textLineBreakMode`。点击回调 `mapView:onClickedBMKOverlayView:`。

**海量点**：`BMKMultiPointOverlay multiPointOverlayWithMultiPointItems:`。BMKMultiPointOverlayView 设置 `icon`、`anchor`、`pointSize`、`delegate`。BMKMultiPointOverlayViewDelegate 的 `didItemTapped:` 处理点击。

### 点聚合（SDK 未内置，参考 BMKPointCluster Demo）

将大量 BMKPointAnnotation 按地理距离聚合，zoom 小时显示聚合点（带数量），zoom 大时拆分为单点。**核心类**：BMKClusterManager、BMKClusterQuadtree、BMKQuadItem、BMKCluster。**流程**：坐标→BMKQuadItem 加入 quadtree；`getClusters:zoomLevel` 按 zoom 获取聚合；`clusterCaches[zoom-3]` 缓存；`mapViewDidFinishLoading` 与 `onDrawMapFrame`（zoom 变化时）触发 updateClusters。**标注展示**见 [annotations.md](annotations.md)。

### 3D 与轨迹

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMK3DModelOverlay | BMK3DModelOverlay.h | 3D 模型 |
| BMK3DModelOverlayView | BMK3DModelOverlayView.h | 3D 模型视图 |
| BMKPrismOverlay | BMKPrismOverlay.h | 棱柱/3D 建筑 |
| BMKPrismOverlayView | BMKPrismOverlayView.h | 棱柱视图 |
| BMKTraceOverlay | BMKTraceOverlay.h | 路书轨迹（发光、渐变色） |
| BMKTraceOverlayView | BMKTraceOverlayView.h | 路书轨迹视图 |
| BMK3DTraceOverlay | BMK3DTraceOverlay.h | 3D 轨迹 |
| BMK3DTraceOverlayView | BMK3DTraceOverlayView.h | 3D 轨迹视图 |

**3D 模型**：`BMK3DModelOverlay modelOverlayWithCenterCoordinate:option:`。BMK3DModelOption：`modelName`、`modelPath`、`scale`、`type`（BMK3DModelTypeGLTF）、`zoomFixed`、`rotateX`、`animationIsEnable`、`animationIndex`、`animationSpeed`、`animationRepeatCount`。3D 展示标准见 [ui-standards.md](ui-standards.md)。

**棱柱**：`BMKPrismOverlay prismOverlayWithPoints:count:` 传入 BMKMapPoint 数组，`height` 设高度。BMKPrismOverlayView 设置 `sideFaceColor`、`topFaceColor`。可用 BMKDistrictSearch 获取区域边界转 BMKMapPoint。

**3D 轨迹**：`BMK3DTraceOverlay traceOverlay3DWithCoordinates:count:option:`。BMK3DTraceOverlayOption：`traceType`、`duration`、`easingCurve`、`opacity`、`paletteOpacity`、`paletteImage`、`projectionPaletteImage`。BMK3DTraceOverlayView 的 `strokeHeights` 长度须与轨迹点数一致。BMK3DTraceOverlayAnimationDelegate 监听动画开始、进度、结束、实时位置。

**BMKTraceOverlay**：`traceOverlayWithCoordinates:count:option:`。Option：`animate=YES`、`trackMove=YES`、`isRotateWhenTrack=YES`、`pointMove=YES`。**pointImage 箭头尖端须朝右**，SDK 旋转后指向行进方向；建议 80×80。BMKTraceOverlayView 设置 `strokeColors`、`strokeColor`、`fillColor`。

**BMKMapTrackAnimation 图标**：polyline 与 BMKIconMarker 共用同一 trackAnim。marker 设置 `anchorX=0.5`、`anchorY=0.5`。**优先使用图片资源**（如 [assets.md](assets.md) 的 track_car 等），不合适时再自绘。旋转以图像**右侧**为行进方向。自绘时：40×40 画布，箭头尖端朝右；UIBezierPath 尖端在 `CGRectGetMaxX(rect) - w*0.05`，底座在左，`baseX + w*0.25` 为左侧凹进形成箭尾。

### 热力图（addHeatMap，非 overlay）

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKHeatMap | BMKHeatMap.h | 热力图 |
| BMKHexagonHeatMap | BMKHexagonHeatMap.h | 六边形热力图 |

**BMKHeatMap**：`mDatas` 为 BMKHeatMapNode 二维数组（支持帧动画），`mMaxHight`、`mGradient`（BMKGradient）、`animation`、`frameAnimation`、`delegate`。`addHeatMap`/`removeHeatMap`。`startHeatMapFrameAnimation`/`stopHeatMapFrameAnimation`/`setHeatMapFrameAnimationIndex:`。

**BMKHexagonHeatMap**：`mData`、`mRadius`、`mOpacity`、`mMaxIntensity`、`mGap`、`mHexagonType`（BMKHexagonTypeVertexUp）、`mGradient`。`addHexagonHeatMap`/`removeHexagonHeatMap`。

### 自定义 Overlay

继承 BMKShape，实现 `boundingMapRect`（用 BMKMapRect 包住所有点）。CustomOverlayView 继承 BMKOverlayView，重载 `glRender`。坐标用 `BMKMapPointForCoordinate` 转换。绘制：`renderLinesWithPoints:pointCount:strokeColor:lineWidth:looped:lineDashType:`、`renderRegionWithPoints:pointCount:fillColor:usingTriangleFan:`、`loadStrokeTextureImage:` + `renderTexturedLinesWithPoints:...`。纹理图片宽高须为 2 的 n 次幂。

## 坐标与结构体

| 类型 | 说明 |
|------|------|
| CLLocationCoordinate2D | 经纬度（BD09） |
| BMKMapRect | 直角地理坐标矩形 |
| BMKMapPoint | 直角地理坐标点 |
| BMKCoordinateRegion | 经纬度区域 |
| BMKCoordinateBounds | 经纬度边界（southWest、northEast） |

**坐标转换**（BMKGeometry.h）：`BMKMapPointForCoordinate`、`BMKCoordinateForMapPoint`。自定义 overlay 用 BMKMapPoint 计算 boundingMapRect。

---

## 按需方案

| 需求 | 基础能力 |
|------|----------|
| 起终点标记（推荐） | BMKIconMarker + addOverlay 顺序 |
| 起终点大头针 | BMKPointAnnotation + BMKAnnotationView，见 [annotations.md](annotations.md) |
| 单色路线 | BMKPolyline + BMKPolylineView，lineWidth 8pt（见 ui-standards） |
| 路况路线 | BMKMultiPolyline + BMKMultiTexturePolylineView，lineWidth 8pt（见 ui-standards） |
| 路线路名 | BMKTextPathMarker + BMKTextPathMarkerView（沿 step 路径绘制 roadName） |
| 路线动画 | BMKMapTrackAnimation + BMKPolyline/MultiPolyline + BMKIconMarker（共用 trackAnim） |
| 圆弧 | BMKArcline + BMKArclineView |
| 渐变线 | BMKGradientLine + BMKGradientLineView |
| 渐变圆 | BMKCircle + BMKGradientCircleView |
| 大地线 | BMKGeodesicLine + BMKGeodesicLineView |
| 图标按行进方向旋转 | BMKRotateItem \| BMKRotateGeoNorth + rotate |
| 航班/信息标签 | BMKRichView + BMKLabelUIView + BMKVerticalLayout |
| 重叠时隐藏 | collisionBehavior + collisionPriority |
| 沿大地线移动/往返 | slerp + BMKGetDirectionFromCoords + routeDirection |
| 文本 overlay | BMKText + BMKTextView |
| 海量点 | BMKMultiPointOverlay + BMKMultiPointItem |
| 点聚合（海量标注） | BMKClusterManager + BMKClusterQuadtree + BMKPointAnnotation |
| 3D 模型 | BMK3DModelOverlay + BMK3DModelOption |
| 棱柱/建筑 | BMKPrismOverlay + BMKPrismOverlayView |
| 路书轨迹 | BMKTraceOverlay + BMKTraceOverlayOption |
| 3D 轨迹 | BMK3DTraceOverlay + BMK3DTraceOverlayOption |
| 热力图 | BMKHeatMap + addHeatMap |
| 六边形热力图 | BMKHexagonHeatMap + addHexagonHeatMap |
