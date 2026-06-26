# 导航

**边界**：应用内步骑行实时导航（BaiduWalkNaviKit），与 BMKRouteSearch 算路画线为不同能力；多路线选路、诱导、TTS、偏航纠偏均属本能力。算路与画线见 [route.md](route.md)。

---

## 步骑行实时导航（BaiduWalkNaviKit）经验与注意事项

### 基本原则

1. **每次切换导航算路前必须销毁**：在发起新一轮算路（如再次点击「步行/骑行导航」或切换起终点）前，必须调用 **`[BMKWalkNavigationManager destroy]`** 与 **`[BMKCycleNavigationManager destroy]`**，再创建新 container 并 `initNaviEngine`、`routePlanWithParams`。否则上一次的引擎状态会干扰本次算路或导航，易出现无路线、回调错乱等问题。
2. **Manager 与类型一致**：步行只用 `BMKWalkNavigationManager sharedManager`，骑行只用 `BMKCycleNavigationManager sharedManager`；LaunchParam 的 `naviType`（如 `BMK_WALK_CYCLE_NAVIGATION_TYPE_NORMAL_CYCLE`）与回调里的 `naviType` 判断一致，避免混用。
3. **不在算路/导航进行中销毁**：仅在**新一轮算路开始前**调用 destroy；仅释放业务侧对「传给 initNaviEngine 的 container」的引用，且应在**启动导航之后**再置 nil（见下）。
4. **多路线流程**：`enableMultiRoute = YES` 且设置 `routePlanDelegate`、`calcRouteDelegate` → `routePlanWithParams` → 多路线结果在 `onRoutePlanResult:naviType:` → 用 `getWalkNaviMulRouteInfos`/`getCycleNaviMulRouteInfos` 与 `displayRoutePlanResult:mapView` 在地图展示 → 用户选路线后调用 `naviCalcRoute:(routeIndex)` → 引擎算路完成后 `onNaviCalcRouteResult:naviType:` → 再 `startWalkNaviWithParentController`/`startCycleNaviWithParentController`。

### 导航生命周期与 container

- 传给 `initNaviEngine:` 的 **container（UIViewController）** 会被引擎用于地图/导航视图；若在回调里**过早**置 nil，引擎依赖的 controller 可能被释放，导致**进入导航无路线**。
- **正确做法**：在 `onNaviCalcRouteResult` 中，**仅在算路失败时**置 nil container；**算路成功时**先调用 `startWalkNavi`/`startCycleNavi`，**在启动导航之后再**置 nil container（步行可紧接着置 nil；骑行建议在 `dispatch_async(main_queue)` 的 block 内先 `startCycleNavi` 再置 nil，并可保留 block 内对 container 的强引用以免提前释放）。

示例（骑行，选路后进入导航）：

```objc
- (void)onNaviCalcRouteResult:(BMKWalkCycleRoutePlanErrorCode)errorCode naviType:(BMKWalkCycleNavigationType)naviType {
    if (errorCode != BMK_WALK_CYCLE_ROUTEPLAN_RESULT_SUCCESS) {
        _walkCycleNaviContainer = nil;
        // 提示错误...
        return;
    }
    if (naviType == BMK_WALK_CYCLE_NAVIGATION_TYPE_WALK) {
        [[BMKWalkNavigationManager sharedManager] startWalkNaviWithParentController:self isPush:YES];
        _walkCycleNaviContainer = nil;
    } else if (naviType == BMK_WALK_CYCLE_NAVIGATION_TYPE_NORMAL_CYCLE || naviType == BMK_WALK_CYCLE_NAVIGATION_TYPE_ELECTRIC_CYCLE) {
        __weak typeof(self) wself = self;
        UIViewController *container = _walkCycleNaviContainer;
        dispatch_async(dispatch_get_main_queue(), ^{
            if (wself) [[BMKCycleNavigationManager sharedManager] startCycleNaviWithParentController:wself isPush:YES];
            wself.walkCycleNaviContainer = nil;
            (void)container;
        });
    }
}
```

### 骑行多路线与展示

- 骑行也支持多路线：`enableMultiRoute = YES`、`routePlanDelegate = self`，与步行一致；选路后对骑行调用 `[[BMKCycleNavigationManager sharedManager] naviCalcRoute:(NSInteger)index]`。
- 骑行引擎建议用 `initNaviEngine:options:` 传入 `BMKWalkCycleNavigationOptions`（含 `displayOption`），并设置 `cycleNaviMode = BMK_CYCLE_NAVIGATION_MODE_NORMAL`；container 的 view 在 init 前可设 `frame = [UIScreen mainScreen].bounds` 以便路线正确布局。

### 驾车与步骑行分工

- **驾车**：可用 [utils.md](utils.md) 的 **BMKNavigation** `openBaiduMapNavigation:` 调起百度地图客户端。
- **步骑行**：应用内导航用 BaiduWalkNaviKit 的 Walk/Cycle Manager，算路前需先拿到用户位置（如 BMKLocationManager 单次定位），再组 LaunchParam（startNode/endNode，type `BMKWalkNavigationRouteNodeLocation`）调用 `routePlanWithParams:`。

---

## 按需方案（导航相关）

| 需求 | 能力组合 | 说明 |
|------|----------|------|
| 驾车调起导航 | BMKNavigation openBaiduMapNavigation: | 调起百度地图客户端，见 utils.md |
| 步骑行多路线选路+应用内导航 | BaiduWalkNaviKit enableMultiRoute + routePlanDelegate + displayRoutePlanResult + naviCalcRoute | 多路线在地图展示折线，用户选路线后 naviCalcRoute(index)，onNaviCalcRouteResult 后再 start 导航；container 在启动导航后再置 nil |
| 多实例后台投屏 | BMKBackgroundMapView + getBackgroundNavigationView | 步骑行导航画面投到外接屏/小窗：mapview、roadNetView、navigationView（由 Manager.getBackgroundNavigationView 获取），startRender/stopRender。详见 [mapview.md](mapview.md)「BMKBackgroundMapView」 |
