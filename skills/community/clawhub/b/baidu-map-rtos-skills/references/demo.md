# 完整 Demo 示例

所有示例均源自 SDK 全流程示例，可直接对照集成。头文件路径以实际工程 `outputIncludes/` 为准。

---

## main：初始化全流程

```cpp
using namespace baidu::rtos_map;
using namespace baidu::rtos_map::auth;
using namespace baidu::rtos_map::base;
using namespace baidu::rtos_map::view;

int main() {
    BaseApi* baseApi = BaseApi::GetInstance();
    baseApi->SetPackageName("your_package_name");

    AuthLicenseApi* authApi = AuthLicenseApi::GetInstance();
    authApi->SetAk("your_ak");
    authApi->RequestLicense([](license::LicenseErrorCode code) { /* ... */ });
    authApi->Authenticate([](MapAuthErrorCode code) { /* ... */ });

    MapComponentApi& mapApi = MapComponentApi::GetInstance();
    mapApi.MarkComponentAlive(true);

    auto baiduMapCanvas = std::make_shared<MapCanvasImpl>();
    // 传入平台真实 canvas/context，例如 OHOS 先创建 UICanvasExt 再 setCanvas
    baiduMapCanvas->setCanvas(platformCanvasContext);
    mapApi.SetCanvas(baiduMapCanvas);

    // SDK 内部渲染数据更新时触发此回调，在此调用 RequestRender 拉取新数据
    mapApi.SetUIThreadFunc([]() {
        MapComponentApi::GetInstance().RequestRender();
    });
    mapApi.InitMap();
    mapApi.RequestRender();

    // ... 业务 Demo ...

    mapApi.MarkComponentAlive(false);
    return 0;
}
```

---

## RunMapStateAndOverlayDemo：地图状态、Marker、折线

```cpp
static void RunMapStateAndOverlayDemo(MapComponentApi& mapApi) {
    mapApi.setCenterPoint(VDPOINT(116.404, 39.915));
    mapApi.setZoom(15.0f);
    mapApi.zoomIn();
    mapApi.zoomOut();
    mapApi.setRotationAngle(30.0);
    mapApi.SetMapBackgroundColor(VColor(18, 18, 24, 255));
    mapApi.setViewBound(utils::geo::VRect(0, 0, 800, 480));

    const VDPOINT pixel  = mapApi.LatLngToScreenPixel(VDPOINT(116.404, 39.915));
    const VDPOINT restore = mapApi.ScreenPixelToLatLng(pixel);

    const int layerId   = mapApi.createLayer(LayerType::OVERLAYER, "demo_overlay_layer");

    // Marker
    const int markerId = mapApi.CreateMarker();
    mapApi.setMarkerPosition(markerId, VDPOINT(116.404, 39.915));
    mapApi.setMarkerSize(markerId, utils::geo::VSize(36, 36));
    mapApi.setMarkerOffset(markerId, utils::geo::VSize(18, 36));
    mapApi.setMarkerAngle(markerId, 0.0);
    mapApi.addOverlay(layerId, markerId);
    mapApi.showOverlay(markerId);

    // 折线（点集）
    const int polylineId = mapApi.CreatePolyline();
    std::vector<VDPOINT> routePoints = {
        VDPOINT(116.400, 39.910),
        VDPOINT(116.404, 39.915),
        VDPOINT(116.410, 39.920)
    };
    mapApi.setPolylinePoints(polylineId, routePoints);
    mapApi.setPolylineFillColor(polylineId, VColor(0, 153, 255, 220));
    mapApi.setPolylineStrokeColor(polylineId, VColor(255, 255, 255, 255));
    mapApi.setPolylineLineWidth(polylineId, 8);
    mapApi.setPolylineStrokeWidth(polylineId, 2);
    mapApi.addOverlay(layerId, polylineId);
    mapApi.showOverlay(polylineId);
    mapApi.updateLayer(layerId);

    const utils::geo::VRect bounds = mapApi.getOverlayBounds(polylineId);
    mapApi.setViewBound(bounds);
    mapApi.RequestRender();
}
```

---

## RunTouchDemo：触摸事件

```cpp
static void RunTouchDemo(MapComponentApi& mapApi) {
    auto makeEvent = [](TouchEvent::Type type, float x, float y) {
        TouchEvent e;
        e.type = type;
        Touch p;
        p.clientX = x;
        p.clientY = y;
        e.touches.push_back(p);
        e.changedTouches.push_back(p);
        return e;
    };

    mapApi.OnTouchDown(makeEvent(TouchEvent::Type::TOUCH_START, 100, 100));
    mapApi.OnTouchMove(makeEvent(TouchEvent::Type::TOUCH_MOVE, 180, 160));
    mapApi.OnTouchUp(makeEvent(TouchEvent::Type::TOUCH_END,  220, 180));
}
```

---

## RunSearchAndRoutePlanDemo：POI 搜索与步行路线规划

```cpp
static void RunSearchAndRoutePlanDemo() {
    using namespace baidu_search;
    SearchApi& searchApi = SearchApi::GetInstance();

    PoiCitySearchOption poiOption;
    poiOption.city       = "北京";
    poiOption.keyword    = "地铁站";
    poiOption.isCityLimit = true;
    poiOption.scope      = POI_SEARCH_SCOPE_TYPE::DETAIL_INFORMATION;
    poiOption.pageIndex  = 0;
    poiOption.pageSize   = 10;
    searchApi.PoiCitySearch(poiOption,
        [](void*, PoiSearchResult* result, SEARCH_ERROR_CODE code, const std::string&) {
            // result 可能为 nullptr
        });

    WalkingSearchOption walkOption;
    walkOption.from.pt       = Coordinate(39.915, 116.404);   // 纬度, 经度
    walkOption.from.cityName = "北京";
    walkOption.to.pt         = Coordinate(39.99466, 116.502966);
    walkOption.to.cityName   = "北京";
    searchApi.RouteWalkingSearch(walkOption,
        [](void*, WalkingSearchResult* result, SEARCH_ERROR_CODE code, const std::string&) {
            // 回调在 HTTP 线程，操作 MapComponentApi 须切回 UI 线程
        });
}
```

> `Coordinate` 构造顺序为 **(纬度, 经度)**，勿颠倒。

---

## RunOfflineDemo：离线地图

```cpp
static void RunOfflineDemo() {
    using namespace baidu::rtos_map::offline;
    MapOfflineApi* api = MapOfflineApi::GetInstance();

    api->RegisterRequestVersionCallback([](const MapOfflineGetVersionCode& code) { });
    api->RegisterDownloadProgressCallback(
        [](const std::string& cityName, MapOfflineDownloadStatus status,
           int progress, int64_t downloaded, int64_t total) { });

    api->RequestVersion();   // 异步，版本回调后列表才有效

    std::vector<OfflineCityInfo> downloadable, downloaded;
    api->GetDownloadableCityList(downloadable);
    api->GetDownloadedCityList(downloaded);

    std::vector<std::string> queryCities = {"北京", "上海"};
    std::vector<OfflineCityInfo> cityInfos;
    api->GetOfflineCityInfo(queryCities, cityInfos);  // 先清空再写入，匹配不到的跳过

    const std::string city = downloadable.empty() ? "北京" : downloadable.front().name;
    int code = api->StartDownloadByCityName(city);
    // code == OfflinePackageNeedDelete：先 DeleteDownloadedCityPackageFile 再重试

    api->GetOfflineCityInfoByCurrentLocation([](bool success, const OfflineCityInfo& info) {
        // success=false 表示未命中或定位失败
    });
}
```

---

## RunRouteTileDemo：路线瓦片预加载

```cpp
static void RunRouteTileDemo(MapComponentApi& mapApi) {
    const std::string routeFile = "route.json";   // 文件名，非完整路径

    mapApi.LoadRouteMapData(routeFile, [](const TilePreloadResponse& resp) {
        // resp.progressPercent == -1 表示瓦片数量超限
    });

    mapApi.CancelMapDataDownload();
    mapApi.DeleteRouteMapData(routeFile);
}
```

---

## RunNaviDemo：导航

```cpp
static void RunNaviDemo() {
    using namespace baidu::rtos_map::navi;
    NaviApi* navi = NaviApi::GetInstance();

    navi->RegisterGuideInfoCallback([](NaviType type, const std::string& info) { });
    navi->RegisterYawingCallback([](NaviType type, NaviYawingStatus status) { });
    navi->RegisterRemainDistanceCallback([](NaviType type, int meters) { });
    navi->RegisterRemainTimeCallback([](NaviType type, int seconds) { });
    navi->RegisterTrackCallback(
        [](NaviType type, int stepIndex, const std::string& curLoc,
           const std::string& nextPoint, const std::string& routeInfo) { });

    navi->Init("route.json", [](bool ok) { });
    navi->UpdateRoute("new_route.json", [](bool ok) { });
    navi->SetNaviType(NaviType::WALKING);
    navi->StartNavi();

    // 持续喂入传感器数据
    navi->UpdateCompass(45.0f);
    location::Location loc(39.915, 116.404);
    loc.setTime(1234567890);
    loc.setDirection(45.0);
    loc.setSpeed(1.2);
    navi->UpdateLocation(loc);

    navi->ExitNavi();
}
```
