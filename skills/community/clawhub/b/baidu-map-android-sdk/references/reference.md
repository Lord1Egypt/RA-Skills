# 百度地图 Android SDK 参考索引

按需选下表文档；通用规则（隐私、AK、MapView 生命周期、监听先于请求、步骑行选型）见 [SKILL.md](../SKILL.md)。

**步骑行**：算路画线（route）与实时导航为**不同服务**——仅画线用 [route.md](route.md)，要诱导/TTS/偏航用步骑行导航（overview + class-reference）。

## 按需求选文档

| 你要做的 | 用到的文档 |
|----------|------------|
| Gradle 依赖、Maven 仓库、地图/检索/工具/定位/步骑行/导航组件、冲突说明 | [gradle.md](gradle.md) |
| AndroidManifest（AK、权限、定位 Service）、混淆、资源与 assets | [project-config.md](project-config.md) |
| 集成步骤、AK、SHA1、包名、Application 初始化、隐私接口 | [overview.md](overview.md) |
| 显示地图、MapView、BaiduMap、生命周期、地图类型、缩放与视野 | [mapview.md](mapview.md) |
| 显示定位、定位图层、定位模式、自定义定位图标 | [location.md](location.md) |
| 点标记、Marker 属性、点击/拖拽、碰撞、Title、3D Marker | [marker.md](marker.md) |
| 折线、多边形、PolylineOptions 属性、虚线、分段颜色/纹理、点击 | [overlays.md](overlays.md) |
| POI 城市/周边/区域/详情、地理编码、逆地理编码 | [search.md](search.md) |
| 驾车/步行/骑行/公交路线规划、Overlay 绘制 | [route.md](route.md) |
| 坐标转换、BD09LL/GCJ02/WGS84、CoordinateConverter | [coordinate.md](coordinate.md) |
| 距离/面积、点与圆/多边形/折线关系、调起百度地图、短地址分享、收藏夹 | [tools.md](tools.md) |
| 检索/路线返回错误码含义 | [errorcode.md](errorcode.md) |
| 类与包速查 | [class-reference.md](class-reference.md) |
| 地图布局、检索/路线面板、Logo/padding、选点/弹窗等 UI 约定 | [ui-standards.md](ui-standards.md) |

## 常见组合

| 需求 | 文档组合 |
|------|----------|
| 地图 + 定位 | gradle → project-config → overview → mapview + location（坐标系统一） |
| 地图 + 路线画线 | mapview + route + search（选点）；步骑行仅画线用 route |
| 步骑行实时导航 | overview → 步行/骑行导航（引擎初始化 → 算路 → 诱导页 → TTS；具体类见 overview 与 class-reference） |
| 标注 + 点聚合 | mapview + marker（点聚合逻辑见 overlay 开源或自实现） |
| POI / 选点 | mapview + search（POI 或地理编码） |
| 定位/鉴权失败、地图闪退 | [location.md](location.md)（如有鉴权排查）+ [project-config.md](project-config.md)（主题、compileSdk、集成经验与常见问题）+ Logcat |

## 文档边界（一览）

| 文档 | 内容 | 边界 |
|------|------|------|
| [gradle.md](gradle.md) | 依赖、冲突、NDK、环境与国内镜像 | 构建报错见 project-config |
| [project-config.md](project-config.md) | AndroidManifest、主题、混淆、集成经验与常见问题 | 仅百度 SDK 相关配置 |
| [overview.md](overview.md) | 集成、AK、隐私、Application、核心类 | 具体 API 见各功能文档 |
| [mapview.md](mapview.md) | MapView、BaiduMap、生命周期、类型、视野 | 不含 Marker/Overlay 具体类型 |
| [location.md](location.md) | 定位图层、模式、自定义图标 | 不含步骑行导航内部定位 |
| [marker.md](marker.md) | Marker、碰撞、Title、3D | 与 overlays 组合使用 |
| [overlays.md](overlays.md) | Polyline、Polygon、折线属性 | 路线 Overlay 见 route |
| [search.md](search.md) | POI、地理编码、逆地理 | 路线算路见 route |
| [route.md](route.md) | RoutePlanSearch、驾车/步行/骑行/公交算路与画线 | 与步骑行实时导航不同；仅算路+画线用本文档 |
| [coordinate.md](coordinate.md) | 坐标转换、BD09LL/GCJ02 | 与 overview 坐标类型一致 |
| [tools.md](tools.md) | 距离、面积、调起地图、短地址 | 工具类，与其它文档组合 |
| [errorcode.md](errorcode.md) | 错误码 | 检索/路线返回码 |
| [class-reference.md](class-reference.md) | 类与包速查 | 用法与示例见各功能文档 |
| [ui-standards.md](ui-standards.md) | 布局结构、面板高度、setViewPadding、fitBounds、检索/路线/选点/弹窗/Logo、触控与边距 | 无特殊要求时按此实现 |

## 能力一览（技能内已覆盖）

- **地图**：MapView/SupportMapFragment/TextureMapView、BaiduMap、地图类型（普通/卫星/空白）、路况/热力、缩放 4–21 级（室内至 22）、BaiduMapOptions、多实例、视野与内边距、底图 POI 显示控制。
- **定位**：定位图层、MyLocationConfiguration、NORMAL/FOLLOWING/COMPASS、自定义图标与精度圈、v7.5.7 自定义中心图/箭头/GIF。
- **覆盖物**：Marker（含动画、碰撞、Title、3D）、Polyline（虚线、分段颜色/纹理、大地曲线、渐变色、发光）、Polygon、信息窗、点聚合、路线 Overlay（开源）。
- **检索**：POI 城市/周边/区域/详情、GeoCoder 正逆地理、输入提示、行政区、AOI、公交、天气等（部分见 search 与 class-reference）。
- **路线**：驾车/步行/骑行/公交规划、PlanNode、RoutePlanSearch、DrivingRouteOverlay 等开源 Overlay。
- **导航**：步行导航、骑行导航（含电动车）、诱导、TTS、偏航纠正（类见 overview/class-reference）。
- **工具**：Gradle 集成、工程配置与混淆、坐标转换、距离/面积、点与图形关系、调起百度地图、短地址分享、地图收藏夹、错误码。
