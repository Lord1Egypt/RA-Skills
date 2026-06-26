# 路线规划

## 通用规则

- **监听先于请求**：先 `setOnGetRoutePlanResultListener`，再调用 `drivingSearch` / `walkingSearch` / `ridingSearch` / `transitSearch` 等，否则可能拿不到回调。
- 用完后 `destroy()` 释放 RoutePlanSearch 实例。
- 自 V3.6.0 起路线 Overlay 不再内置，需从官方 Demo 的 **overlayutil** 包拷贝 DrivingRouteOverlay、WalkingRouteOverlay、BikingRouteOverlay、TransitRouteOverlay、MassTransitRouteOverlay 等至项目。

## 驾车路线规划

1. `RoutePlanSearch mSearch = RoutePlanSearch.newInstance();`
2. `OnGetRoutePlanResultListener` 中实现 `onGetDrivingRouteResult(DrivingRouteResult)`，其它路线类型实现对应 onGetXxxRouteResult。
3. `mSearch.setOnGetRoutePlanResultListener(listener);`
4. 起终点：`PlanNode.withCityNameAndPlaceName("北京", "西二旗地铁站")` 或 `PlanNode.withLocation(latLng)`。
5. 发起：`mSearch.drivingSearch(new DrivingRoutePlanOption().from(stNode).to(enNode));`
6. 绘制：若已引入 DrivingRouteOverlay，从 `result.getRouteLines()` 取一条，`overlay.setData(routeLine); overlay.addToMap(); overlay.zoomToSpan();`

### 驾车策略与路况

- **策略**：`DrivingRoutePlanOption.policy(DrivingRoutePlanOption.DrivingPolicy.ECAR_TIME_FIRST)`（时间优先）、`ECAR_AVOID_JAM`（躲避拥堵）、`ECAR_DIS_FIRST`（最短距离）、`ECAR_FEE_FIRST`（较少费用）。
- **路况**：`option.trafficPolicy(ROUTE_PATH)` 关闭路况；`ROUTE_PATH_AND_TRAFFIC` 开启路况。

### 驾车结果错误码（result.error）

- 结果类有 **result.error** 字段（类型 `SearchResult.ERRORNO`）。先判断再使用路线：
  - `result.error == SearchResult.ERRORNO.NO_ERROR`：成功，可用 `result.getRouteLines()`。
  - `result.error == SearchResult.ERRORNO.AMBIGUOUS_ROURE_ADDR`：起终点或途经点歧义，可 `result.getSuggestAddrInfo()` 提示用户。
  - `result == null` 或 `result.error == SearchResult.ERRORNO.RESULT_NOT_FOUND`：未找到路线。

### 示例片段

```java
// 创建 Option 与起终点
DrivingRoutePlanOption option = new DrivingRoutePlanOption();
option.policy(DrivingRoutePlanOption.DrivingPolicy.ECAR_TIME_FIRST);
option.trafficPolicy(DrivingRoutePlanOption.DrivingTrafficPolicy.ROUTE_PATH);
PlanNode start = PlanNode.withCityNameAndPlaceName("北京", "西二旗地铁站");
PlanNode end = PlanNode.withCityNameAndPlaceName("北京", "百度科技园");
mSearch.drivingSearch(option.from(start).to(end));

// 回调中
@Override
public void onGetDrivingRouteResult(DrivingRouteResult result) {
    if (result != null && result.error == SearchResult.ERRORNO.AMBIGUOUS_ROURE_ADDR) {
        // 歧义，可 result.getSuggestAddrInfo()
        return;
    }
    if (result == null || result.error == SearchResult.ERRORNO.RESULT_NOT_FOUND) {
        // 未找到
        return;
    }
    if (result.error == SearchResult.ERRORNO.NO_ERROR && result.getRouteLines() != null && !result.getRouteLines().isEmpty()) {
        DrivingRouteLine line = result.getRouteLines().get(0);
        DrivingRouteOverlay overlay = new DrivingRouteOverlay(mBaiduMap);
        overlay.setData(line);
        overlay.addToMap();
        overlay.zoomToSpan();
    }
}
// onDestroy 中
if (mSearch != null) mSearch.destroy();
```

## 步行 / 骑行 / 公交路线规划

- 同一 RoutePlanSearch，监听中分别实现 `onGetWalkingRouteResult`、`onGetBikingRouteResult`、`onGetTransitRouteResult` 等。
- 起终点同样用 PlanNode（城市+地名或经纬度）。
- 发起：`walkingSearch(WalkingRoutePlanOption)`、`ridingSearch(BikingRoutePlanOption)`、`transitSearch(TransitRoutePlanOption)` 等；Option 可设置策略、途经点等，具体见类参考。
- 绘制：使用对应 WalkingRouteOverlay、BikingRouteOverlay、TransitRouteOverlay 等，setData 后 addToMap、zoomToSpan。
- **错误码**：同上，用 `result.error == SearchResult.ERRORNO.NO_ERROR` 等判断（AMBIGUOUS_ROURE_ADDR、RESULT_NOT_FOUND 通用）。

## PlanNode

- `PlanNode.withCityNameAndPlaceName(cityName, placeName)` 或 `PlanNode.withLocation(LatLng)` 等构造起终点。

## 步骑行实时导航（与路线规划区别）

- 路线规划仅算路+画线；实时导航需步骑行导航 SDK（WalkNavigateHelper、BikeNavigateHelper），包含引擎初始化、算路、诱导页、TTS、偏航纠偏等，类与流程见 [overview.md](overview.md) 与 [class-reference.md](class-reference.md)。
