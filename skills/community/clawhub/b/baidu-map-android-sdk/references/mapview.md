# 地图容器与 BaiduMap

## 配置与初始化

- **AndroidManifest**：在 `<application>` 内配置 AK：`<meta-data android:name="com.baidu.lbsapi.API_KEY" android:value="您的AK"/>`。在 `<application>` 外声明权限（如网络、定位等）；自 Android 6.0 起部分权限需代码动态申请。
- **初始化**：在自定义 Application 的 `onCreate` 中调用 `SDKInitializer.initialize(this)` 和 `SDKInitializer.setCoordType(CoordType.BD09LL)`（或 GCJ02）。隐私接口必须在 initialize 之前调用，见 [overview.md](overview.md)。

## 布局与获取 BaiduMap

- 布局中声明：`<com.baidu.mapapi.map.MapView android:id="@+id/bmapView" ... />`。
- 代码获取：`MapView mMapView = findViewById(R.id.bmapView);`，`BaiduMap mBaiduMap = mMapView.getMap();`。
- 纯代码：`MapView mapView = new MapView(this);` 然后 `setContentView(mapView)`。也可用 `BaiduMapOptions` 构造带初始状态的 MapView：`new MapView(this, options)`。

## MapView 生命周期（必须）

在 Activity 中：
- `onResume()` 内调用 `mMapView.onResume()`
- `onPause()` 内调用 `mMapView.onPause()`
- `onDestroy()` 内调用 `mMapView.onDestroy()`

## BaiduMapOptions 可选状态

| 状态 | 含义 |
|------|------|
| mapStatus | 地图状态 |
| compassEnable | 是否开启指南针，默认开启 |
| mapType | 地图模式，默认普通地图 |
| rotateGesturesEnabled | 是否允许旋转手势 |
| scrollGesturesEnabled | 是否允许拖拽 |
| overlookingGesturesEnabled | 是否允许俯视手势 |
| zoomControlsEnabled | 是否显示缩放按钮 |
| zoomControlsPosition | 缩放控件位置 |
| zoomGesturesEnabled | 是否允许缩放手势 |
| scaleControlEnabled | 是否显示比例尺 |
| scaleControlPosition | 比例尺位置 |
| logoPosition | Logo 位置 |

## 地图类型与图层

- **地图类型**（`mBaiduMap.setMapType(...)`）：
  - `BaiduMap.MAP_TYPE_NORMAL`：普通地图（含 3D）
  - `BaiduMap.MAP_TYPE_SATELLITE`：卫星图
  - `BaiduMap.MAP_TYPE_NONE`：空白地图（不下载瓦片，可叠瓦片或覆盖物）
- **实时路况**：`mBaiduMap.setTrafficEnabled(true)`。V4.5.0+ 可自定义路况颜色：`setCustomTrafficColor(严重拥堵, 拥堵, 缓行, 畅通)`，颜色格式 `#AARRGGBB`，不需显示的可将 AA 设为 00。
- **百度城市热力图**：`mBaiduMap.setBaiduHeatMapEnabled(true)`；仅 11–20 级可显示。

## 显示层级与比例尺

- 缩放等级：2D 地图 4–21，3D 地图 19–21，卫星 4–20，路况/热力 11–21，室内 17–22。自 v5.0.0 起由 3–21 改为 4–21。
- 设置缩放：`MapStatus.Builder builder = new MapStatus.Builder(); builder.zoom(18.0f); mBaiduMap.setMapStatus(MapStatusUpdateFactory.newMapStatus(builder.build()));`

## 常用地图容器

- **GLSurfaceView 系**：MapView、MapFragment、SupportMapFragment。
- **TextureView 系**：TextureMapView、TextureMapFragment、TextureSupportMapFragment。与其它 GLSurfaceView（如相机）叠加或放在 ScrollView 时建议用 Texture 系，避免穿透、黑屏。需 Android 4.4+ 且开启硬件加速。
- SupportMapFragment 使用：`SupportMapFragment.newInstance(mapOptions)`，再通过 FragmentTransaction 添加或替换到容器。

## 多实例

同一页面可放多个 MapView/SupportMapFragment，分别操作互不干扰。每个通过 `getBaiduMap()`/`getMapView()` 获取控制器与视图，分别设置 `MapStatusUpdate`、`setLogoPosition` 等。

## 方法交互（BaiduMap）

- **缩放**：`MapStatusUpdateFactory.zoomTo(level)`、`zoomIn()`、`zoomOut()`、`zoomBy(delta)`；`setMapStatus()` 为跳变，`animateMapStatus()` 为动画。级别超出范围时按最大/最小级别显示。
- **操作区内边距**：`mBaiduMap.setViewPadding(left, top, right, bottom)`；地图加载完成后生效，可通过 `OnMapLoadedCallback.onMapLoaded()` 监听。不得遮挡百度 Logo 与版权。布局模式、面板高度、与 fitBounds 区分见 [ui-standards.md](ui-standards.md)。
- **显示范围**：`MapStatusUpdateFactory.newLatLngBounds(bounds)` 或 `newLatLngBounds(bounds, width, height)`，bounds 由 `LatLngBounds.Builder().include(...).include(...).build()` 构造。
- **中心点**：`MapStatusUpdateFactory.newLatLng(latLng)`。
- **底图 POI**：`mBaiduMap.showMapPoi(false)` 可隐藏底图标注仅留道路。POI 标签按类型控制：`setPoiTagEnable(PoiTagType, boolean)`、`getPoiTagEnable(PoiTagType)`；PoiTagType 含 All、Epidemic、Travel、Shop 等。
- **空白地图背景色**：仅当 `setMapType(MAP_TYPE_NONE)` 时生效，`mBaiduMap.setMapBackgroundColor(Color.argb(...))`。
