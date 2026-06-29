# 检索、导航、离线地图与 mapAPP Demo 扩展

完整可运行示例见 [demo.md](demo.md)。

## 检索（SearchApi）

入口：`outputIncludes/search_api.h`，`SearchApi::GetInstance()`。  
**坐标：** `baidu_search::Coordinate` 构造为 **(纬度, 经度)**，勿颠倒。  
**线程：** 回调在 HTTP 线程触发；操作 `MapComponentApi` 须切回 UI 线程（mapAPP 用 `EnqueueMainThreadMapWork`）。

| 场景 | 典型 API |
|------|----------|
| 城市 POI | `PoiCitySearch(PoiCitySearchOption, callback)` |
| 周边 POI | `PoiNearbySearch(PoiNearbySearchOption, callback)` |
| 步行路线 | `RouteWalkingSearch(WalkingSearchOption, callback)` |
| 简化步行 | `RouteSimpleWalkingSearch(...)` |
| 逆地理 | `ReverseGeoCodeSearch(ReverseGeoCodeSearchOption, callback)` |

## 导航（NaviApi）

入口：`outputIncludes/navi_api.h`。路线瓦片预加载用 `MapComponentApi::LoadRouteMapData`，不再通过 NaviApi。

```cpp
NaviApi* navi = NaviApi::GetInstance();

navi->RegisterGuideInfoCallback([](NaviType type, const std::string& info) { });
navi->RegisterYawingCallback([](NaviType type, NaviYawingStatus status) { });
navi->RegisterRemainDistanceCallback([](NaviType type, int meters) { });
navi->RegisterRemainTimeCallback([](NaviType type, int seconds) { });
navi->RegisterTrackCallback(
    [](NaviType type, int stepIndex, const std::string& curLoc,
       const std::string& nextPoint, const std::string& routeInfo) { });

navi->Init("route.json", [](bool ok) { });
navi->SetNaviType(NaviType::WALKING);
navi->StartNavi();

// 持续喂入传感器数据
navi->UpdateCompass(45.0f);
location::Location loc(39.915, 116.404);
navi->UpdateLocation(loc);

navi->ExitNavi();
```

## 离线地图（MapOfflineApi）

入口：`outputIncludes/offline/map_offline_api.h`。

```cpp
MapOfflineApi* api = MapOfflineApi::GetInstance();

api->RegisterRequestVersionCallback([](const MapOfflineGetVersionCode& code) { });
api->RegisterDownloadProgressCallback(
    [](const std::string& cityName, MapOfflineDownloadStatus status,
       int progress, int64_t downloaded, int64_t total) { });

api->RequestVersion();   // 异步，回调后列表才有效

std::vector<OfflineCityInfo> downloadable, downloaded;
api->GetDownloadableCityList(downloadable);
api->GetDownloadedCityList(downloaded);

// 批量查询：先清空 cityRecords，匹配不到的城市跳过
std::vector<OfflineCityInfo> cityRecords;
api->GetOfflineCityInfo({"北京", "上海"}, cityRecords);

// 返回 0 表示已提交；OfflinePackageNeedDelete 须先 DeleteDownloadedCityPackageFile 再重试
int code = api->StartDownloadByCityName("北京");

// success=false 表示未命中或定位失败
api->GetOfflineCityInfoByCurrentLocation([](bool success, const OfflineCityInfo& info) { });
```

---

## mapAPP（rtos-mac-simulator）扩展新 Demo

### 调度关系

```
main (SDL Confirm)
  └─ RunMapDemoById(demo_id)          [freertos_app.cpp]
       ├─ MapRuntime::RunDemo
       ├─ OfflineRuntime::EnterDemo
       ├─ RouteSearchRuntime / PoiSearchRuntime / RouteTileRuntime / ReverseGeocodeRuntime
```

### 扩展步骤

| 步骤 | 说明 |
|------|------|
| 1 | 参考 [demo.md](demo.md) 确认 SDK API 与回调线程 |
| 2 | 地图类逻辑放 `map_runtime.cpp`；独立面板仿 `*_runtime.cpp` + `src/demo/*_page.cpp` |
| 3 | 同步注册 `DemoId`、`RunMapDemoById`、`main` 右侧列表 |
| 4 | 网络/搜索回调里操作 `MapComponentApi` 须用 `EnqueueMainThreadMapWork` |
| 5 | 需干净地图用 `EnsureMapReinitialized()`；默认底图勿对刚 Init 的实例重入销毁 |
| 6 | 资源路径：Windows（含 MSYS）`<exe>/app/bd_map/`；macOS `includes/v_config.h` 的 `ROOT_DIR` |

### 内置 Demo 入口速查

| Demo | mapAPP 入口 | 逻辑文件 |
|------|-------------|----------|
| DefaultMap | `RunDemoDefaultMap` | `map_runtime.cpp` |
| GeoJSONPathOverview | `RunDemoGeoJsonPathOverview` | `map_runtime.cpp` |
| DrawMarker | `RunDemoDrawMarker` | `map_runtime.cpp` |
| WalkingRoutePlan | `RunDemoWalkingRoutePlan` | `map_runtime.cpp` |
| WalkingRouteNaviPreview | `RunDemoWalkingRouteNaviPreview` | `map_runtime.cpp` |
| OfflineDownload | `OfflineRuntime::EnterDemo` | `offline_runtime.cpp` |
| RouteTileDownload | `RouteTileRuntime::EnterDemo` | `route_tile_runtime.cpp` |
| RouteSearch | `RouteSearchRuntime::EnterDemo` | `route_search_runtime.cpp` |
| PoiSearch | `PoiSearchRuntime::EnterDemo` | `poi_search_runtime.cpp` |
| ReverseGeocode | `ReverseGeocodeRuntime::EnterDemo` | `reverse_geocode_runtime.cpp` |

### 常用辅助函数

| 函数 | 位置 | 用途 |
|------|------|------|
| `EnsureMapReinitialized` | `map_runtime.cpp` | 退出导航、销毁旧地图再 Init |
| `ApplyGeoJsonRouteFromFile` | `map_runtime.cpp` | 封装折线 + 全览 |
| `EnqueueMainThreadMapWork` | `freertos_app.cpp` | HTTP/搜索回调切回 SDL 主线程 |
| `PostMapRenderEvent` | `freertos_app.cpp` | 请求重绘 |
