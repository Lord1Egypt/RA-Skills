# 路线规划

**边界**：算路与画线（**BMKRouteSearch**，BaiduMapKit）。步骑行实时导航为另一服务，见 [reference.md](reference.md) 选型与 [navi.md](navi.md)。

## 多场景路线类型

路线规划支持多种场景，UI 上可用分段控件或图标切换（参考百度地图 App）：

| 场景 | Option | 方法 | 结果类 | 路名/说明来源 |
|------|--------|------|--------|----------|
| 驾车 | BMKDrivingRoutePlanOption | drivingSearch: | BMKDrivingRouteResult | BMKDrivingStep.roadName |
| 步行 | BMKWalkingRoutePlanOption | walkingSearch: | BMKWalkingRouteResult | BMKWalkingStep.instruction |
| 骑行 | BMKRidingRoutePlanOption | ridingSearch: | BMKRidingRouteResult | BMKRidingStep.instruction |
| 公交 | BMKTransitRoutePlanOption | transitSearch: | BMKTransitRouteResult | BMKTransitStep.instruction、vehicleInfo |

**UI**：见 [ui-standards.md](ui-standards.md)。

## 核心类

| 类 | 头文件 | 说明 |
|----|--------|------|
| BMKRouteSearch | BMKRouteSearch.h | 路线检索，delegate 为 BMKRouteSearchDelegate |
| BMKPlanNode | BMKTypes.h | 路线节点（pt、name、cityName、cityID、floor、building、uid） |
| BMKDrivingRoutePlanOption | BMKRouteSearchOption.h | 驾车 |
| BMKWalkingRoutePlanOption | BMKRouteSearchOption.h | 步行 |
| BMKRidingRoutePlanOption | BMKRouteSearchOption.h | 骑行 |
| BMKTransitRoutePlanOption | BMKRouteSearch.h | 公交（市内） |
| BMKMassTransitRoutePlanOption | BMKRouteSearch.h | 跨城公交 |
| BMKIndoorRoutePlanOption | BMKRouteSearch.h | 室内 |
| BMKIntegralRoutePlanOption | BMKRouteSearch.h | 一体化路线 |
| BMKBusRoutePlanOption | BMKRouteSearch.h | 公交路线（市内+跨城，另一套接口） |

**BMKRouteSearch 方法**：`drivingSearch:`、`walkingSearch:`、`ridingSearch:`、`transitSearch:`、`massTransitSearch:`、`indoorRoutePlanSearch:`、`integralRoutePlanSearch:`、`busRoutePlanSearch:`。均为异步，结果在对应 Delegate 回调中返回。

**BMKRouteSearchDelegate 回调**：`onGetDrivingRouteResult:result:errorCode:`、`onGetWalkingRouteResult:result:errorCode:`、`onGetRidingRouteResult:result:errorCode:`、`onGetTransitRouteResult:result:errorCode:`、`onGetMassTransitRouteResult:result:errorCode:`、`onGetIndoorRouteResult:result:errorCode:`、`onGetIntegralRouteResult:result:errorCode:`、`onGetBusRouteResult:result:errorCode:`。先判断 `errorCode == BMK_SEARCH_NO_ERROR` 再使用 result。

## BMKPlanNode（路线节点）

路线节点可通过**经纬度 pt** 或 **地名 name + 城市** 指定；cityName 与 cityID 同时指定时 **cityID 优先**。

| 属性 | 类型 | 说明 |
|------|------|------|
| name | NSString | 地名（与 cityName 组合使用） |
| pt | CLLocationCoordinate2D | 经纬度，与 name 二选一或同时用于提高精度 |
| cityName | NSString | 节点所在城市 |
| cityID | NSInteger | 城市 ID，与 cityName 同设时优先 |
| floor | NSString | 楼层（室内等场景） |
| building | NSString | 建筑物（室内等场景） |
| uid | NSString |  POI 唯一标识，可选 |

驾车示例：`start.name = @"天安门"`，`start.cityName = @"北京市"`。

## 路线 Option 参数一览

**公共（BMKBaseRoutePlanOption）**：`from`、`to`（BMKPlanNode，起/终点，必填）。

| 类型 | Option 独有参数 | 说明 |
|------|------------------|------|
| 驾车 | wayPointsArray（BMKPlanNode 数组）、**drivingPolicy**、**drivingRequestTrafficType** | 途经点；策略与路况见下 |
| 步行 | 无 | 仅 from / to |
| 骑行 | **ridingType**、**roadPrefer**、wayPointsArray | 普通/电动车；道路偏好；途经点 |
| 公交（市内） | **city**（NSString）、**transitPolicy** | 城市必填；时间优先/换乘优先等 |
| 跨城公交 | **pageIndex**、**pageCapacity**、**incityPolicy**、**intercityPolicy**、**intercityTransPolicy**、**languageType** | 分页与市内/跨城策略 |

**驾车策略 drivingPolicy**（默认 BMK_DRIVING_TIME_FIRST）：如 BMK_DRIVING_BLK_FIRST（避免堵车）、BMK_DRIVING_TIME_FIRST（时间优先）、BMK_DRIVING_DIS_FIRST（距离优先）、BMK_DRIVING_FEE_FIRST（费用优先）等，详见 BMKRouteSearchType.h。

**路况 drivingRequestTrafficType**：`BMK_DRIVING_REQUEST_TRAFFICE_TYPE_NONE`（默认，无路况）、`BMK_DRIVING_REQUEST_TRAFFICE_TYPE_PATH_AND_TRAFFICE`（带路况）。带路况时 Step 的 `traffics` 有效。

**公交策略 transitPolicy**：如 BMK_TRANSIT_TIME_FIRST（时间优先）、BMK_TRANSIT_TRANSFER_FIRST（换乘优先）、BMK_TRANSIT_WALK_FIRST（步行少）等。

**骑行 ridingType**：`BMK_RIDING_TYPE_NORMAL`（普通）、`BMK_RIDING_TYPE_ELECTRIC`（电动车）。**roadPrefer**：道路偏好枚举，见 BMKRouteSearchType.h。

## 驾车路线

| 类 | 说明 |
|----|------|
| BMKDrivingRouteResult | routes（BMKDrivingRouteLine 数组） |
| BMKDrivingRouteLine | steps、duration（BMKTime）、distance、lightNum 等 |
| BMKDrivingStep | points、pointsCount、roadName、instruction、**traffics**、direction、entrace/exit、hasTrafficsInfo 等 |

**路况**：`BMKDrivingStep.traffics` 为 NSArray&lt;NSNumber *&gt;，0=无数据，1=畅通，2=缓行，3=拥堵，4=严重拥堵。需带路况时设置 `drivingRequestTrafficType = BMK_DRIVING_REQUEST_TRAFFICE_TYPE_PATH_AND_TRAFFICE`。textureImages 须按顺序提供 5 张纹理（含 traffic_texture_severe_congestion），见 [assets.md](assets.md)。

**路线线宽**：BMKPolylineView / BMKMultiTexturePolylineView 的 **lineWidth 标准 8pt**，见 [ui-standards.md](ui-standards.md)。

**回调**：`onGetDrivingRouteResult:result:errorCode:`

## 坐标与路况提取

**驾车路况解析**：请求时设置 `drivingRequestTrafficType = BMK_DRIVING_REQUEST_TRAFFICE_TYPE_PATH_AND_TRAFFICE`。坐标按 step 顺序拷贝到总数组；**路况 drawIndexs 按各 step 的 traffics 直接拼接即可**，无需在 step 之间补 0，也无需按 `pointsCount - 1` 补齐。traffics 中 0=无数据、1=畅通、2=缓行、3=拥堵、4=严重拥堵，与 [assets](assets.md) 中 traffic_texture_* 顺序一致。若 `drawIndexs.count < pointCount - 1` 可回退为单折线 BMKPolyline。

```objc
BMKDrivingRouteLine *line = result.routes.firstObject;
NSUInteger pointCount = (NSUInteger)line.totalPointsCount;
BMKMapPoint *points = malloc(pointCount * sizeof(BMKMapPoint));
NSMutableArray<NSNumber *> *drawIndexs = [NSMutableArray array];
NSUInteger j = 0;
for (BMKDrivingStep *step in line.steps) {
    for (NSUInteger i = 0; i < (NSUInteger)step.pointsCount; i++) {
        points[j].x = step.points[i].x;
        points[j].y = step.points[i].y;
        j++;
    }
    for (NSNumber *t in step.traffics) {
        [drawIndexs addObject:t];
    }
}
BMKMultiPolyline *polyline = [BMKMultiPolyline multiPolylineWithPoints:points count:pointCount drawIndexs:drawIndexs];
free(points);
```

## 单色路线（无路况）

步行/骑行/驾车/公交的 **BMKRouteLine**（及子类）均有 **totalPointsCount**，可直接取总点数，无需遍历 steps 累加。Step 均继承 BMKRouteStep，有 `points`、`pointsCount`，将各 step 的 points 依次拷贝到一块缓冲区即可：

```objc
NSUInteger pointCount = (NSUInteger)line.totalPointsCount;  // 直接取总点数
BMKMapPoint *points = malloc(pointCount * sizeof(BMKMapPoint));
NSUInteger j = 0;
for (BMKRouteStep *step in line.steps) {
    for (NSUInteger i = 0; i < step.pointsCount; i++) {
        points[j++] = step.points[i];
    }
}
BMKPolyline *polyline = [BMKPolyline polylineWithPoints:points count:pointCount];
free(points);
```

## 起终点标注

- 起点：`line.steps.firstObject.points[0]` 或 `BMKCoordinateForMapPoint(points[0])`
- 终点：`line.steps.lastObject.points[step.pointsCount-1]` 或 `points[pointCount-1]`
- 起终点**必须用 BMKIconMarker**（addOverlay）展示，不得用 BMKPointAnnotation/BMKPinAnnotationView，见 [overlays.md](overlays.md)、[SKILL.md](../SKILL.md)

## 路线路名绘制

- **路名**：`BMKDrivingStep.roadName` 可用 **BMKTextPathMarker** 沿该 step 的 `points`/`pointsCount` 绘制，文字随路径走向展示。创建 `[BMKTextPathMarker textPathMarkerWithPoints:step.points count:step.pointsCount]`，设置 `text = step.roadName`、`style`（BMKTextStyle，如 22pt 黑字白边），View 用 **BMKTextPathMarkerView** 的 `initWithMarker:`。详见 [overlays.md](overlays.md)「BMKTextPathMarker」、[ui-standards.md](ui-standards.md) 路名字体。

## 视野适配（mapViewFitPolyline，必须考虑）

绘制路线后**必须**做视野适配，使路线与起终点完整落在可视区内且不被 UI 遮挡；同时须保证 Logo 不被遮挡（用 setMapPadding，见 [ui-standards.md](ui-standards.md)）。BMKPolyline 遵循 BMKOverlay，可直接用 **boundingMapRect** 获取折线外包矩形，无需遍历点：

```objc
- (void)mapViewFitPolyline:(BMKPolyline *)polyline {
    if (polyline.pointCount < 2) return;
    BMKMapRect rect = polyline.boundingMapRect;
    [_mapView fitVisibleMapRect:rect edgePadding:UIEdgeInsetsMake(80, 40, 80, 40) withAnimated:YES];  // 标准见 ui-standards
}
```

## 公交多方案

`BMKTransitRouteResult.routes` 为多条方案数组；每条 BMKTransitRouteLine 含 steps（BMKTransitStep）。BMKTransitStep 有 **stepType**（BMK_BUSLINE/BMK_SUBWAY/BMK_WAKLING）、**vehicleInfo**（线路名、首末班等）、instruction、entrace/exit。UI 见 [ui-standards.md](ui-standards.md)。选中某条后绘制并 `mapViewFitPolyline` 适配视野。

**跨城公交**：使用 `massTransitSearch:` + BMKMassTransitRoutePlanOption（from/to 为 BMKPlanNode，起终点城市不支持 cityID，仅 name+cityName）；回调 `onGetMassTransitRouteResult:result:errorCode:`，结果含多种跨城方式（火车、飞机、大巴等）。

**公交线路详情**：BMKBusLineSearch（见 [search.md](search.md)）按线路 UID 查站点与走向，与路线规划为不同能力。

## 骑行类型与道路偏好

- **ridingType**：`BMK_RIDING_TYPE_NORMAL`（普通）、`BMK_RIDING_TYPE_ELECTRIC`（电动车）。
- **roadPrefer**：道路偏好（如优先非机动车道等），见 BMKRouteSearchType.h 中 BMKRidingRoadPrefer。
- 骑行支持 **wayPointsArray**（途经点）。

## 时长与距离格式化

```objc
// duration：BMKTime 含 hours、minutes
NSString *time;
if (routeLine.duration.hours > 0 && routeLine.duration.minutes > 0)
    time = [NSString stringWithFormat:@"%d小时%d分", routeLine.duration.hours, routeLine.duration.minutes];
else if (routeLine.duration.hours > 0)
    time = [NSString stringWithFormat:@"%d小时", routeLine.duration.hours];
else
    time = [NSString stringWithFormat:@"%d分钟", routeLine.duration.minutes];

// distance：米/公里
NSString *distance = routeLine.distance < 100
    ? [NSString stringWithFormat:@"%d米", routeLine.distance]
    : [NSString stringWithFormat:@"%.1f公里", routeLine.distance / 1000.0];
```

## 详情页（Step 列表）

- 从 `line.steps` 构建 DetailModel 数组：`instruction`、`cellHeight`、`stepType`（公交用 BMKTransitStepType）
- 公交：`step.vehicleInfo.title` 作为线路标签，`step.stepType >= BMK_WAKLING` 为步行段可跳过
- 步行/骑行：`step.instruction` 直接展示

---

## 按需方案

| 需求 | 能力组合 | 说明 |
|------|----------|------|
| 驾车路线（无路况） | BMKRouteSearch + BMKPolyline | 合并 steps 为单折线 |
| 驾车路线（带路况） | BMKRouteSearch + BMKMultiPolyline + drawIndexs | drivingRequestTrafficType=PATH_AND_TRAFFICE，traffics→textureImages |
| 步行/骑行仅算路画线 | BMKRouteSearch + BMKPolyline | walkingSearch/ridingSearch；实时导航见上文「步骑行实时导航」 |
| 步骑行多路线选路+应用内导航 | BaiduWalkNaviKit + [navi.md](navi.md) | 多路线选路与导航生命周期见 navi.md |
| 多场景切换 UI | UISegmentedControl（驾车\|步行\|骑行） | 参考 ui-standards.md |
| 起终点选点 | BMKSuggestionSearch | [search.md](search.md) |
| 路线动画 | BMKMapTrackAnimation | [overlays.md](overlays.md) |
