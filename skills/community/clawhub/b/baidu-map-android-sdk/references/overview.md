# 百度地图 Android SDK 集成与核心 API 摘要

SDK 集成方式：推荐通过 **Gradle** 依赖（见 [gradle.md](gradle.md)）；AndroidManifest、混淆等见 [project-config.md](project-config.md)。

## 使用准备与 AK

1. 申请百度账号并完成开发者认证。
2. 在控制台「应用管理 - 我的应用」创建应用，应用类型选 **Android SDK**，填写：
   - 应用名称、**包名**（与 build.gradle 的 applicationId 一致）、**SHA1**（debug/release 可各填一个）。
   - 勾选所需服务（地图、检索、路线等），未勾选则对应接口可能返回无权限。
3. 将生成的 AK 配置到工程：AndroidManifest 的 `<application>` 内 `<meta-data android:name="com.baidu.lbsapi.API_KEY" android:value="您的AK"/>`，或代码中 `SDKInitializer.setApiKey("ak")`（须在 `initialize` 之前）。包名与签名须与申请一致。鉴权结果由 SDK 通过广播回调（成功/失败/网络错误），失败时 Intent 带错误码与错误信息，排查与广播 Action 见 [project-config.md](project-config.md)。

**SHA1**：调试版 `keytool -list -v -keystore ~/.android/debug.keystore`，默认口令 `android`。发布版用 release keystore。

## 隐私合规（v7.5.0+）

- 调用 SDK 任何接口前必须先调用隐私合规接口，且**必须在 `SDKInitializer.initialize` 之前**调用。
- 定位 SDK：不同意则无法正常获取位置；地图 SDK：不同意则检索、路线等请求异常。
- 统一接口：`SDKInitializer.setAgreePrivacy(Context context, boolean isEnable)`，context 必须为 Application Context；`isEnable` 为 true 表示用户同意隐私政策。
- 推荐写法：在 Application 中先 `setAgreePrivacy`，再在 try-catch 中 `initialize`（可捕获 BaiduMapSDKException）。可按用户是否同意隐私分别设置；未同意时 `setAgreePrivacy(context, false)`，同意后再设为 true 并初始化。

```java
// 用户同意后，必须在 initialize 之前调用
SDKInitializer.setAgreePrivacy(getApplicationContext(), true);
try {
    SDKInitializer.initialize(this);
} catch (BaiduMapSDKException e) {
    // 初始化失败可记录日志
}
SDKInitializer.setCoordType(CoordType.BD09LL);
```

## Application 初始化

```java
public class DemoApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        SDKInitializer.setAgreePrivacy(getApplicationContext(), true); // 必须先于 initialize
        try {
            SDKInitializer.initialize(this);
        } catch (BaiduMapSDKException e) { }
        SDKInitializer.setCoordType(CoordType.BD09LL); // 或 CoordType.GCJ02，自 4.3.0
    }
}
```

## MapView 与 BaiduMap 生命周期

- 布局中声明 `MapView`（或代码 `new MapView(this)`），Activity 中 `mMapView.getMap()` 得到 `BaiduMap`。
- **必须在 Activity 中调用**：`onResume()` → `mMapView.onResume()`；`onPause()` → `mMapView.onPause()`；`onDestroy()` → `mMapView.onDestroy()`。

## 核心类速查

| 用途 | 类/接口 |
|------|---------|
| 初始化、坐标类型 | SDKInitializer、CoordType |
| 地图控件与控制器 | MapView、BaiduMap、SupportMapFragment、TextureMapView |
| 地图状态 | MapStatus、MapStatusUpdate、MapStatusUpdateFactory、MapStatus.Builder |
| 经纬度 | LatLng |
| 点标记 | Marker、MarkerOptions、BitmapDescriptor、BitmapDescriptorFactory |
| 折线/多边形 | Polyline、PolylineOptions、Polygon、PolygonOptions |
| POI 检索 | PoiSearch、PoiCitySearchOption、PoiNearbySearchOption、PoiBoundSearchOption、PoiDetailSearchOption、OnGetPoiSearchResultListener、PoiResult、PoiDetailSearchResult |
| 地理编码 | GeoCoder、GeoCodeOption、ReverseGeoCodeOption、OnGetGeoCoderResultListener、GeoCodeResult、ReverseGeoCodeResult |
| 路线规划 | RoutePlanSearch、DrivingRoutePlanOption、PlanNode、OnGetRoutePlanResultListener、DrivingRouteResult；步行/骑行/公交对应 Option/Result |
| 路线 Overlay（开源） | DrivingRouteOverlay、WalkingRouteOverlay、BikingRouteOverlay、TransitRouteOverlay、PoiOverlay |
| 步行/骑行导航 | WalkNavigateHelper、BikeNavigateHelper、WalkNaviLaunchParam、BikeNaviLaunchParam、诱导与 TTS 监听 |
| 定位 | LocationClient、LocationClientOption、BDAbstractLocationListener、MyLocationData、MyLocationConfiguration、LocationMode |
| 室内图 | BaiduMap.setOnBaseIndoorMapListener、switchBaseIndoorMapFloor |
| 坐标转换 | CoordinateConverter、CoordType.GPS/COMMON/BD09MC 等 |

## 检索与路线注意点

- **监听先于请求**：POI 先 `setOnGetPoiSearchResultListener` 再 `searchInCity`/`searchNearby`/`searchInBound`/`searchPoiDetail`；路线先 `setOnGetRoutePlanResultListener` 再 `drivingSearch`/`walkingSearch` 等。
- 使用完毕后 `destroy()` 释放 PoiSearch、RoutePlanSearch、GeoCoder 等实例。

## 系统与包说明

- 支持 Android 4.0+；支持 armeabi-v7a、arm64-v8a、x86、x86_64。
- 自 V3.6.0 起覆盖物相关类开源（OverlayManager、PoiOverlay、TransitRouteOverlay、WalkingRouteOverlay、DrivingRouteOverlay、BusLineOverlay 等），可从 Demo 的 overlayutil 包获取。
- 自 v4.5.0 支持 HTTPS，V5.3.2 起默认 HTTPS；Android P+ 禁止明文，检索建议用 HTTPS 或配置 network_security_config。
