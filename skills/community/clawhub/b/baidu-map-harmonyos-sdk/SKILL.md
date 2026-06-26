---
name: baidu-map-harmonyos-sdk
description: 帮助在 HarmonyOS NEXT 上使用百度地图鸿蒙 SDK 进行开发。支持独立包（@bdmap/base、@bdmap/map、@bdmap/search、@bdmap/util）和组合包（@bdmap/map_walkride_search、@bdmap/navi_map），以及定位 SDK（@bdmap/locsdk）。涵盖地图展示与交互、覆盖物绘制、POI/AOI 检索、路线规划、导航、前台/后台定位、地址/POI 获取等场景。适用于提到鸿蒙地图、百度地图 HarmonyNEXT SDK、地图展示、检索、路线规划、导航、定位能力等需求。
---

# Baidu Map HarmonyOS SDK 开发 Skill

## 使用场景

在以下情况**必须优先使用本 Skill**：

- 提到 **HarmonyOS NEXT 百度地图 / 鸿蒙地图 SDK / HarmonyNEXT 地图** 开发
- 在本项目中使用 `@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util` 等包或者直接完全使用 `@bdmap/map_walkride_search`等组合包
- 需要实现以下能力之一：
  - 地图组件展示、手势和控件交互
  - 标注点（Marker）、线、面、多边形、圆、文字、信息窗口等覆盖物
  - 普通地图、卫星地图、个性化地图、自定义瓦片图等图层
  - 驾车/步行/骑行/公交等路线规划以及步骑行导航
  - POI/AOI/室内 POI/建筑物/行政区/天气 等检索
  - 正逆地址解析、推荐上车点、坐标转换、调起百度地图等

以下情况**不适合使用本 Skill，应转用其他平台/能力的 Skill**：

- 仅涉及 **Web 版百度地图 JavaScript API**、Android/iOS 原生 SDK、或小程序地图能力
- 与地图无关的一般 HarmonyOS 应用开发（此时应优先使用空工程/通用 HarmonyOS Skill）

## ⚠️ 强制要求（必须严格遵守）

在使用本 Skill 进行开发时，**必须严格遵守**以下规范（仅列核心摘要，详细说明见引用文档）：

1. **日志 / 注释 / 模块化规范**  
   - 必须使用统一的 `Logger` 工具类封装原生 `console`，第一个参数固定使用场景名 `"SportHealthMap"`，禁止直接使用 `console.info/error/warn/debug`。  
   - 关键业务方法必须补充中文注释说明用途、参数与返回值，通用工具类必须抽取为独立模块，禁止在页面内联定义通用类。  
   - 详细规则与示例见：[代码规范](references/guidelines/coding-standards.md)。

2. **图片资源使用规范（必须主动拷贝）**  
   - 生成或修改示例代码时，优先使用本 Skill 资产中约定的图片名，并保持与 [assets](references/assets.md) 表格中的用途一致或相近。  
   - 必须提醒开发者：将对应图片主动拷贝到 HarmonyOS 工程的 `resources/rawfile/` 目录后，再通过 `rawfile://xxx.png` 方式引用，否则覆盖物会因为找不到资源而不显示或报错。  
   - 详细说明见：[代码规范 / 图片资源使用规范](references/guidelines/coding-standards.md#4-图片资源使用规范)。

3. **地图功能开发（代码组织与规范）（强制要求）**
   - **示例与 API 使用**：回答与实现时，应优先参考本目录下 `references/reference.md` 中给出的示例代码与调用方式，在此基础上按业务场景做适配，避免自创与 SDK 不一致的用法。  
   - **性能与覆盖物分层**：高频 UI 更新场景（如气泡内容刷新、轨迹回放等）必须缓存复用 PopView/Label 等对象，所有覆盖物需显式设置 `zIndex` 并遵循统一分层，避免信息被遮挡；详细见：[地图性能与覆盖物分层规范](references/guidelines/performance-optimization.md)。  
   - **地图 & UI 交互反馈**：地图初始化、检索、路线规划、定位、覆盖物增删、权限/网络异常等关键行为，必须通过 Toast/Dialog/页面状态文本等方式给出清晰的用户反馈，而不仅仅是日志；详细见：[地图 UI 交互与用户反馈规范](references/guidelines/ui-feedback.md)。  
   - **定位与地图协同**：涉及 `@bdmap/locsdk` 的地图场景时，需同时遵守定位 SDK 的初始化顺序、权限与错误处理规范；完整说明见：[定位 SDK 开发指南](references/guidelines/location-sdk-guide.md)。
   - **步骑行导航开发**：涉及步行/骑行导航（`@bdmap/map_walkride_search`）时，需遵循导航引擎初始化时序、生命周期管理、模拟导航退出、默认 UI 手势穿透等规范；完整说明见：[步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md)。
   - **地图样式与视觉规范**：涉及 Marker 锚点、路线/区域颜色与线宽、不同缩放级别信息密度控制等样式问题时，需遵循统一规范；详见：[地图样式与视觉规范](references/guidelines/map-style-guide.md)。
   - **类型与 ArkTSCheck**：实现地图相关回调与方法时，必须显式声明参数与返回值类型，禁止使用 `any` 或隐式 `undefined`；当无法明确 `.catch` 回调参数类型时，优先使用 `Error` 或 `object`，确保通过 ArkTSCheck。

4. **包管理互斥规则（强制要求）**
   - 组合包（`@bdmap/map_walkride_search`、`@bdmap/navi_map`）与独立包（`@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util`）**不允许混用**，否则会导致依赖冲突。
   - 添加任何百度地图依赖前，必须先检查 `oh-package.json5` 中已有的包方案，并严格遵循同一方案。
   - **自动切换**：当项目已使用独立包、但新需求明确需要组合包能力时，Agent 必须**自动执行切换**（卸载独立包 → 安装组合包 → 批量替换 import → 构建验证），无需额外询问用户。
   - `@bdmap/locsdk` 为独立定位包，不受上述互斥限制，可与任何方案搭配使用。
   - 详细规则、自动切换流程与场景建议见：[包管理规范](references/guidelines/package-management.md)。

5. **运行检测（Auto Run 构建）**  
   - 每次完成与百度地图 HarmonyOS SDK 相关的代码改动后，必须按照约定的 Auto Run 流程执行一次构建与 ArkTSCheck，自检是否存在编码错误。  
   - 核心命令为：`ohpm install` + `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon`。  
   - 详细流程与错误分类处理见：[构建与编码错误自检规范](references/guidelines/build-and-test.md)。

## 基本开发流程（通用步骤）

处理任何鸿蒙百度地图 SDK 相关问题时，遵循以下流程组织思路与回答：

1. **确认需求类型**
   - 判断问题属于哪类场景：
     - 地图展示与交互
     - 覆盖物绘制（点/Marker/线/面/文字/圆）
     - 检索（POI/AOI/建筑物/行政区/天气等）
     - 路线规划（驾车/步行/骑行/公交）
     - 步骑行导航（导航引擎、默认导航 UI、导航状态监听、模拟导航等）
     - 定位能力（单点定位/持续定位/后台定位）
     - 工具类能力（距离/面积计算、坐标转换、点与图形位置关系等）
2. **检查依赖与安装方式（强制遵守包管理互斥规则）**
  - **必须先阅读 [包管理规范](references/guidelines/package-management.md)**，确认当前项目使用的是组合包还是独立包方案，严格遵守互斥规则。
  - 根据 `references/api/modules.md`（模块索引）建议：
     - 若只需要部分能力，建议按需安装独立包：
       - `ohpm install @bdmap/base`
       - `ohpm install @bdmap/search`
       - `ohpm install @bdmap/util`
       - `ohpm install @bdmap/map`
       - `ohpm install @bdmap/locsdk`
     - 若需要地图 + 步行/骑行 等组合能力，可直接使用组合包：
       - `ohpm install @bdmap/map_walkride_search`
     - 若需要导航 + 地图能力，可使用组合包：
       - `ohpm install @bdmap/navi_map`
   - **组合包与独立包不允许混用**，详见 [包管理规范](references/guidelines/package-management.md)。
   - 在回答中明确指出需要安装的包以及命令。
3. **确认系统与工具链约束**
  - 参考 `references/api/modules.md`（模块索引）与在线文档的约束与限制，回答时需提醒：
     - 仅支持标准系统，设备为华为手机
     - HarmonyOS 版本：HarmonyOS NEXT Developer Preview1 及以上
     - DevEco Studio 版本：DevEco Studio NEXT Developer Preview1 及以上
     - HarmonyOS SDK 版本：HarmonyOS NEXT Developer Preview1 SDK 及以上
4. **配置权限**
   - 如涉及网络访问、检索、路线规划等，需要在权限配置中加入至少：
     - `"ohos.permission.GET_WIFI_INFO"`
     - `"ohos.permission.GET_NETWORK_INFO"`
     - `"ohos.permission.GET_BUNDLE_INFO"`
     - `"ohos.permission.INTERNET"`
   - 提示在工程配置中正确声明这些权限。
5. **精确定位 API 声明推荐流程**
   - 从业务代码出发：先看 import { MapOptions } from '@bdmap/map' 里的「包名 + 类型名」。
   - 定位包根声明文件：在当前工程找到 oh_modules/@bdmap/map/Index.d.ets。
   - 在 Index.d.ets 中查导出：搜索 MapOptions，找到类似
    import MapOptions from "./src/main/ets/lbsmapsdk/e/p";
   - 跳到具体定义文件：根据相对路径打开 src/main/ets/lbsmapsdk/e/p.d.ets，再在文件内搜索 class MapOptions 查看完整定义。

## 常见能力指引

在提需求时，优先按照下列能力分类，结合对应模块文档进行回答。

### 1. 能力索引（给开发工具全局搜索用）

使用建议：

- **先搜关键词，再跳转**：优先用下表“推荐搜索词”（包含类名/方法名/中文别名）做全局搜索；命中后再打开对应 `references/reference.md` 小节，最后按需下钻到 `references/api/` API 文档。
- **三段式定位**：`关键词（用户问题）` → [references/reference](references/reference.md)（示例与用法） → `references/api/modules/*.md（API 参数/枚举/接口明细）`。

| 场景（按功能归类） | 推荐搜索词 | [references/reference](references/reference.md) 定位 | `references/api/` API 文档入口 |
| --- | --- | --- | --- |
| 地图初始化/展示 | MapComponent、MapController、onReady、MapOptions、MapStatus、显示地图 | [references/reference](references/reference.md#1-地图展示与交互模块map) / [references/reference](references/reference.md#显示地图) | [references/api/modules/map](references/api/modules/map.md) |
| 地图类型/底图 | setMapType、普通图、卫星图、空白地图、POI显隐、交通流 | [references/reference](references/reference.md#地图类型切换) / [references/reference](references/reference.md#交通流控制) | [references/reference](references/api/modules/map.md) |
| 个性化地图 | CustomStyle、setCustomStyleById、initCustomStyle、sty | [references/reference](references/reference.md#个性化地图) | [references/reference](references/api/modules/map.md) |
| 室内图 | indoorMap、INDOORSTATUSCHANGE、switchIndoorFloor、getIndoorInfo | [references/reference](references/reference.md#室内图控制) | [references/reference](references/api/modules/map.md) |
| 离线地图 | LocalMapManager、getHotCities、start、pause、resume、delete | [references/reference](references/reference.md#离线地图) | [references/api/modules/map](references/api/modules/map.md) |
| 手势/交互 | gestures、zoomGesturesEnabled、moveGesturesEnabled、rotateGesturesEnabled、MapEvent.PINCH | [references/reference](references/reference.md#手势交互) | [references/api/modules/map](references/api/modules/map.md) |
| 控件/图层 | CompassLayer、LocationLayer、比例尺、缩放控件、定位控件、getLayerByTag | [references/reference](references/reference.md#控件交互) / [references/reference](references/reference.md#ref-map-compass-layer) | [references/api/modules/map](references/api/modules/map.md) |
| 地图事件 | MAPSTATUSCHANGE、CLICK、DOUBLECLICK、PINCHSTART、ROTATIONUPDATE | [references/reference](references/reference.md#事件交互) | [references/api/modules/map](references/api/modules/map.md) |
| 地图生命周期/销毁 | onWillDisappear、MapController.onWillDisappear、Navigation、Router | [references/reference](references/reference.md#销毁地图) | [references/api/modules/map](references/api/modules/map.md) |
| 英文地图 | MapLanguage、setMapLanguage、getMapLanguage | [references/reference](references/reference.md#英文地图) | [references/api/modules/map](references/api/modules/map.md) |
| 粒子效果 | ParticleEffectType、showParticleEffectByType、customParticleEffectByType | [references/reference](references/reference.md#粒子效果) | [references/api/modules/map](references/api/modules/map.md) |
| 覆盖物：Marker | Marker、ImageEntity、addOverlay、removeOverlay、OverlayEvent.CLICK | [references/reference](references/reference.md#绘制Marker点) | [references/api/modules/map](references/api/modules/map.md) |
| 覆盖物：气泡（弹框、信息窗） | PopView、LabelUI、HorizontalLayout | [references/reference](references/reference.md#添加信息框) / [references/reference](references/reference.md#信息框) | [references/api/modules/map](references/api/modules/map.md) |
| 覆盖物：点聚合 | ClusterGroup、ClusterTemplate、addMarker | [references/reference](references/reference.md#点聚合) | [references/api/modules/map](references/api/modules/map.md) |
| 覆盖物：折线/轨迹 | Polyline、textures、dottedline、TrackAnimation、Track | [references/reference](references/reference.md#绘制线) / [references/reference](references/reference.md#Track动画能力) / [references/reference](references/reference.md#绘制动态轨迹) | [references/api/modules/map](references/api/modules/map.md) |
| 覆盖物：面/圆 | Polygon、Circle、Stroke、fillcolor、alpha | [references/reference](references/reference.md#绘制面) / [references/reference](references/reference.md#绘制圆) | [references/api/modules/map](references/api/modules/map.md) |
| 覆盖物：3D | Prism、Building、Bd_3DModel、GLTF、OBJ | [references/reference](references/reference.md#绘制棱柱) / [references/reference](references/reference.md#建筑物) / [references/reference](references/reference.md#绘制3D模型) | [references/api/modules/map](references/api/modules/map.md) |
| 图层：瓦片/热力 | UrlTileProvider、ImageTileLayer、HeatMapBuilder、HexagonMapBuilder | [references/reference](references/reference.md#瓦片图层) / [references/reference](references/reference.md#ref-map-heatmap-3d) / [references/reference](references/reference.md#ref-map-heatmap-hexagon) / [references/reference](references/reference.md#2D蜂窝热力图) | [references/api/modules/map](references/api/modules/map.md) |
| 检索：POI | PoiSearch、searchInCity、searchNearby、searchInBound、PoiDetail | [references/reference](references/reference.md#POI检索) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：地理编码 | GeoCoder、geocode、reverseGeoCode、GeoCodeOption | [references/reference](references/reference.md#地理编码) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：AOI | AoiSearch、requestAoi、polygon | [references/reference](references/reference.md#AOI检索) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：Sug | SuggestionSearch、requestSuggestion | [references/reference](references/reference.md#ref-search-suggestion) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：公交线路 | BusLineSearch、searchBusLine、BUS_LINE、SUBWAY_LINE | [references/reference](references/reference.md#公交信息检索) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：天气 | WeatherSearch、WeatherResult、districtID | [references/reference](references/reference.md#天气服务) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：推荐上车点 | requestRecommendStop、RecommendStopResult | [references/reference](references/reference.md#推荐上车点) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：行政区 | DistrictSearch、searchDistrict、边界、polylines | [references/reference](references/reference.md#检索行政区边界数据) | [references/api/modules/search](references/api/modules/search.md) |
| 检索：建筑物 | BuildingSearch、requestBuilding、3D楼块 | [references/reference](references/reference.md#地图建筑物检索) | [references/api/modules/search](references/api/modules/search.md) |
| 路线：驾车 | RoutePlanSearch、drivingSearch、DrivingRouteResult | [references/reference](references/reference.md#驾车路线规划) | [references/api/modules/search](references/api/modules/search.md) / [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 路线：步行 | walkingSearch、WalkingRouteResult | [references/reference](references/reference.md#步行路线规划) | [references/api/modules/search](references/api/modules/search.md) / [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 路线：骑行 | bikingSearch、BikingRouteResult | [references/reference](references/reference.md#骑行路线规划) | [references/api/modules/search](references/api/modules/search.md) / [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 路线：公交 | transitSearch、masstransitSearch、TransitRouteResult | [references/reference](references/reference.md#公交路线规划) | [references/api/modules/search](references/api/modules/search.md) / [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 导航：步骑行引擎 | BDNaviService、NaviType、NaviMode、initializer、init、unInit | [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md#4-引擎初始化) | [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 导航：路线规划 | RoutePlanOption、RouteNodeInfo、IRoutePlanListener、RoutePlanError、displayRoutePlanResult | [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md#6-路线规划) | [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 导航：导航控制 | start、stop、pause、resume、isStart、cancelRoutePlanDisplay、isMultiNaviCreated | [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md#7-导航控制) | [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 导航：状态监听 | IGuideSubStatusListener、IGuideInfoListener、onRouteFarAway、onArriveDest、onFinalEnd | [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md#8-导航状态监听) | [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 导航：默认 UI | walkRideDefaultUIPage、walkRideUIPageOption、headerGuideShow、naviETAShow、hitTestBehavior | [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md#9-界面渲染) | [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 导航：模拟导航 | MockLocationPlugin、setLocationPlugin、resetLocationPlugin、reloadTrack | [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md#7-导航控制) | [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 导航：语音播报 | ITTSPlugin、playTTSText、setTTsPlugin | [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md#4-引擎初始化) | [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) |
| 工具：距离/面积 | DistanceUtil、AreaUtil、calculateArea、getDistance | [references/reference](references/reference.md#距离和面积计算) | [references/api/modules/util](references/api/modules/util.md) |
| 工具：空间关系 | SpatialRelationUtil、isPolygonContainsPoint、getNearestPointFromLine | [references/reference](references/reference.md#点和其他图形的位置关系) | [references/api/modules/util](references/api/modules/util.md) |
| 工具：坐标转换 | NativeMethods、wgsll2bdll、gcjll2bdll、mc2ll | [references/reference](references/reference.md#坐标转换) | [references/api/modules/base](references/api/modules/base.md) / [references/api/modules/util](references/api/modules/util.md) |
| 其他：收藏/分享 | FavoriteManager、ShareUrlSearch、requestRouteShareUrl | [references/reference](references/reference.md#地图收藏夹) / [references/reference](references/reference.md#位置短地址分享) | [references/api/modules/map](references/api/modules/map.md) / [references/api/modules/search](references/api/modules/search.md) |

### 2. 地图展示与交互（模块：map）

- 引导：
  - 从 [references/api/modules/map](references/api/modules/map.md) 查找对应的地图组件、控制器 API
  - 选择合适的地图类型：标准地图、个性化地图、卫星图、自定义瓦片图
  - 配置基本参数：中心点、缩放级别、旋转、倾斜、罗盘、比例尺、定位按钮等控件
- 回答中应覆盖：
  - 如何在鸿蒙页面中引入 `MapComponent`
  - 如何在 `onReady` 中拿到 `MapController`
  - 开启/关闭手势交互（缩放、平移、旋转、倾斜等）
  - 控件显隐与自定义样式的关键配置点（如在文档中有具体字段名，需引用）

### 3. 覆盖物绘制（模块：map）

- 关注以下覆盖物类型（优先在 [references/api/modules/map](references/api/modules/map.md) 中查找具体接口名）：
  - Marker 点、点聚合、Marker 动画
  - 折线（Polyline）、弧线
  - 多边形/面
  - 圆
  - 文本注记
  - 地面覆盖物、棱柱、3D 建筑物/模型
  - 气泡/弹框/信息框/信息窗口
- 回答时的通用模式：
  - 指出需要通过 `MapController` 提供的方法添加/更新/删除对应覆盖物
  - 说明必要参数（经纬度、颜色、宽度、透明度、zIndex 等）
  - 如需复杂样式（自定义 icon），引导查阅在线文档中对应章节（地图覆盖物部分）。

### 4. 检索能力（模块：search）

- 根据需求分类：
  - POI 检索：普通地点搜索，支持关键字、城市、范围检索
  - AOI 检索：区域面信息
  - 室内 POI 检索：购物中心、写字楼内部 POI
  - 建筑物检索：楼宇信息
  - 行政区检索：省/市/区划边界数据
  - 天气检索：实况天气、预报等
- 回答时应：
  - 指出需安装 `@bdmap/search` 或组合包
  - 引导查看 [references/api/modules/search](references/api/modules/search.md)的对应接口说明
  - 说明同步/异步调用模式（根据文档）以及结果回调/Promise 的处理方式
  - 提醒注意配额限制、错误码处理，可引导查看在线文档「请求状态码说明」。

### 5. 路线规划（模块：@bdmap/map_walkride_search组合包）

- 支持：
  - 驾车路线规划
  - 步行路线规划
  - 骑行路线规划
  - 公交路线规划
  - 跨城公交路线规划
- 回答步骤建议：
  - 明确需要的出行方式（驾车/步行/骑行/公交）
  - 提示安装 `@bdmap/search` 以及必要的步行/骑行/公交相关模块或组合包，例如 `@bdmap/map_walkride_search`
  - 在 [references/api/modules/search](references/api/modules/search.md)、[references/api/modules/walkridecommon](references/api/modules/walkridecommon.md) 查找对应 API：
    - 典型参数：起终点坐标 / 关键字、策略（最短时间、最短距离、避堵等）、途经点等
  - 在回答中给出：
    - 如何构造请求参数对象
    - 如何发起路线规划调用
    - 如何从返回结果中解析路线、路段、坐标点，并在地图上绘制（配合地图覆盖物功能）。

> **步骑行导航场景**：若需求不仅是路线规划，还涉及**实时导航引导**（导航启停、偏航重算、默认导航 UI、语音播报、模拟导航等），请直接参考第 8 节「步骑行导航能力」和 [步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md)。

### 6. 工具类能力与其他（模块：util / map / search）

- 能力示例：
  - 距离和面积计算
  - 点与其他图形的位置关系判断（点是否在多边形内等）
  - 坐标转换（如与其他坐标系互转）
  - 调起百度地图客户端相关能力（如在线文档中有说明）
  - 位置短地址分享、地图收藏夹等
- 回答方式：
  - 根据具体需求，指明应使用 [references/api/modules/util](references/api/modules/util.md) 或在线文档中「工具」「调起百度地图功能」「位置短地址分享」等章节
  - 简要讲清：
    - 输入参数含义
    - 返回值结构
    - 常见错误和注意事项（如坐标系要求）。

### 7. 定位能力（模块：locsdk / @bdmap/locsdk）
  本节只给出**关键要点**，完整开发指南请见：[定位 SDK 开发指南](references/guidelines/location-sdk-guide.md)。

  - **适用场景**：前台连续定位、单次定位、后台持续定位、经纬度/地址/POI 获取等。  
  - **依赖与安装**：统一使用项目约定的 `@bdmap/locsdk` 版本，按指南配置线上/线下依赖并执行 `ohpm install` + 构建自检。  
  - **隐私与权限（强制）**：先获取用户隐私同意和运行时定位权限，再调用 `LocationClient.setAgreePrivacy(true)`、`LocationClient.checkAuthKey(...)`，并正确声明 `module.json5` 中的定位相关权限与 `backgroundModes`。  
  - **初始化与使用顺序**：遵循「隐私合规 → AK 鉴权 → 权限申请 → 创建 `LocationClient` → 注册监听 → 配置 `LocationClientOption` → 启动定位」的顺序，页面/业务结束时必须停止定位并注销监听。  
  - **模式与能力**：根据业务选择连续定位、单次定位、后台定位，并合理设置坐标系、时间/距离间隔、是否返回地址/位置描述/POI 等参数。  
  - **结果校验与错误处理**：使用前需检查 `isLocSuccess`、坐标非 (0,0)、精度半径合理，并通过 Logger + Toast/状态文本反馈错误原因与解决建议。  
  - **性能与合规**：对连续/后台定位设置合理频率和结束条件，敏感数据通过 HTTPS 传输并避免在日志中输出精确坐标。

### 8. 步骑行导航能力（模块：@bdmap/map_walkride_search 组合包）
  本节只给出**关键要点**，完整开发指南请见：[步骑行导航 SDK 开发指南](references/guidelines/walkride-sdk-guide.md)。

  - **适用场景**：步行导航、骑行导航、路线规划结果展示、导航状态监听、默认导航 UI 渲染、模拟导航调试等。
  - **依赖与安装**：使用组合包 `@bdmap/map_walkride_search`（已包含 base + map + search + util），与独立包不可混用。
  - **核心类与接口**：
    - `BDNaviService`：导航服务主入口，通过 `NaviType.WALK` / `NaviType.RIDE` 创建
    - `RoutePlanOption` + `IRoutePlanListener`：路线规划参数与回调
    - `IGuideSubStatusListener`：导航状态监听（偏航、接近/到达目的地等）
    - `IGuideInfoListener`：诱导信息、剩余距离/时间、速度等实时数据
    - `ITTSPlugin`：语音播报接口
    - `walkRideDefaultUIPage`：内置导航 UI 组件
    - `MockLocationPlugin`：模拟定位插件（调试用）
  - **初始化时序**：`aboutToAppear` 注册 TTS 插件 → `MapComponent.onReady` 获取 MapController → `service.initializer().init(context, mapController)`。
  - **导航控制**：路线规划成功 → `cancelRoutePlanDisplay()` 清除路线展示 → `lifecycle().start()` 启动导航 → 到达终点后 `lifecycle().stop()` 停止 → 页面销毁时 `initializer().unInit()` 释放引擎。
  - **默认 UI**：使用 `walkRideDefaultUIPage` 渲染导航界面时，必须设置 `.hitTestBehavior(HitTestMode.None)` 防止拦截底图手势。
  - **坐标转换**：SDK 使用百度坐标系（BD09ll），外部 WGS84/GCJ-02 数据须通过 `CoordTrans.wgsToBaidu()` / `CoordTrans.gcjToBaidu()` 转换。
  - **错误处理**：`RoutePlanError` 提供 20+ 种错误码，必须封装用户友好的错误提示，不可仅输出日志。


## 回答风格与输出格式要求

在基于本 Skill 回答问题时：

1. **优先使用中文回答**，除非明确要求英文。
2. **文档检索与工具调用顺序（强制要求）**：
   - ✅ 当涉及百度地图 HarmonyOS SDK（例如 `@bdmap/map` 覆盖物、信息框/PopView 等能力）时，**必须优先读取本地文档**：
     - （例如）使用 `read_file` / `grep` 等工具打开并检索：
       - [references/reference](references/reference.md)
       - [references/api/modules](references/api/modules.md)
       - [references/api/modules/map](references/api/modules/map.md)（信息框/PopView 等相关章节）
   - ✅ 只有在本地文档无法覆盖、或发现明显版本差异/缺失时，才使用 `web_search` 查阅在线文档（如 `https://lbsyun.baidu.com/faq/api?title=harmonynextsdk`），并在回答中说明参考来源。
   - ✅ 回答中引用 API 名称、参数、枚举等时，应以「本地文档 + 官方在线文档」为准，**禁止仅凭记忆或经验臆造 API**。
   - ❌ 在未阅读本地 [references/reference](references/reference.md) / `references/api/modules/*.md` 前，**禁止直接通过在线搜索结果给出具体 API 写法**（例如 PopView 的构造参数、事件枚举名等）。
3. **回答结构尽量清晰，建议使用如下顺序**：
   - **场景说明**：先简要说明这是哪个模块/能力（地图展示、检索、路线规划等）。
   - **依赖与权限**：列出需要安装的 ohpm 包和必需权限。
   - **关键步骤**：用 3–6 个步骤说明从初始化到接口调用的流程。
   - **示例代码**：给出尽量简洁的示例（注意不要与本 Skill 说明中的示意代码冲突，应参考项目实际 API 命名）。
   - **扩展阅读**：给出应查看的本地文档文件（如 [references/reference](references/api/modules/map.md) 对应章节）和在线文档章节（如「地图覆盖物」「路线规划」等）。
4. **构建与编码错误自检（强制要求）**：
   - 每次完成与百度地图 HarmonyOS SDK 相关的代码改动后，需在工程根目录执行一次 `ohpm install` 与 `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon` 进行构建与 ArkTSCheck 自检。  
   - 如构建报错，需根据错误信息回溯并修复本次改动引入的编码问题；若为环境/工具链问题，则在回答中明确区分并给出处理建议。详细流程见：[构建与编码错误自检规范](references/guidelines/build-and-test.md)。

## 资源文件
- 图像资源：[assets.md](references/assets.md)，生成代码中的图像，优先使用提供的图像资源

## 参考文档

使用本 Skill 时，**始终优先结合本地文档、安装包声明文件和在线官方文档**：

- 本地文档（本项目）：
  - [references/reference](references/reference.md)：HarmonyNEXT 地图 SDK 使用文档以及参考代码摘要
  - [references/api/modules](references/api/modules.md)：模块总览入口
  - [references/api/modules/base](references/api/modules/base.md)：基础能力接口（坐标类型、权限验证）（按需阅读）
  - [references/api/modules/map](references/api/modules/map.md)：地图组件、地图控制器、地图样式与交互（按需阅读）
  - [references/api/modules/search](references/api/modules/search.md)：检索相关接口（POI/AOI/建筑物/行政区/天气等）（按需阅读）
  - [references/api/modules/util](references/api/modules/util.md)：工具与通用能力（按需阅读）
  - [references/api/modules/walkridecommon](references/api/modules/walkridecommon.md)：步行、骑行、公交等路线规划基础（按需阅读）
- 开发指南（本项目）：
  - [references/guidelines/walkride-sdk-guide](references/guidelines/walkride-sdk-guide.md)：步骑行导航 SDK 完整开发指南（引擎初始化、路线规划、导航控制、状态监听、默认 UI、模拟导航、TTS、资源释放）
  - [references/guidelines/location-sdk-guide](references/guidelines/location-sdk-guide.md)：定位 SDK 开发指南
  - [references/guidelines/package-management](references/guidelines/package-management.md)：包管理互斥规范
  - [references/guidelines/coding-standards](references/guidelines/coding-standards.md)：代码规范（日志、注释、模块化、图片资源）
  - [references/guidelines/performance-optimization](references/guidelines/performance-optimization.md)：性能与覆盖物分层规范
  - [references/guidelines/ui-feedback](references/guidelines/ui-feedback.md)：UI 交互与用户反馈规范
  - [references/guidelines/map-style-guide](references/guidelines/map-style-guide.md)：地图样式与视觉规范
  - [references/guidelines/build-and-test](references/guidelines/build-and-test.md)：构建与编码错误自检规范
- 安装包声明文件：
  - 前置条件，检查`entry/oh-package.json5`中的引用是否已经安装，如果未安装，则需要通过`ohpm install`安装，记录下包名版本号
  - 查声明文件中的 class/接口名：
    用 grep（或 IDE 全局搜索）搜："class MapOptions"，范围限制到 oh_modules/@bdmap/map/src/main/ets/。
  - 不确定具体路径时,统一推荐走 @bdmap/xxx/Index.d.ets → 目标 .d.ets 这条路径，不要直接在大量混淆文件里乱翻:
    - 首先检索当前工程的`oh_modules/.ohpm/@bdmap+包名@版本号`，找到目录
    - 然后，继续往下查找`oh_modules/@bdmap/包名/Index.d.ets`文件
    - 最后，从`Index.d.ets`文件中内部搜索类型名，查看定义
    - (举例)查找 `{MapController} from '@bdmap/map'`的`MapController`定义，定位到当前工程中的`oh_modules/.ohpm/@bdmap+map@2.0.3/oh_modules/@bdmap/map/Index.d.ets`文件，查到`MapController`是`Index.d.ets`的相对路径`./src/main/ets/lbsmapsdk/e/g`，则通过`oh_modules/.ohpm/@bdmap+map@2.0.3/oh_modules/@bdmap/map/src/main/ets/lbsmapsdk/e/g.d.ets`文件，即可找到`MapController`的定义;
- 在线官方文档（需要更详细 API、枚举、参数说明时查阅）：
  - HarmonyNEXT 地图 SDK 概述与开发指南：`https://lbsyun.baidu.com/faq/api?title=harmonynextsdk`

当本地文档与在线文档存在差异时，以**在线官方文档**为准，但要在回答中说明参考了哪一类文档。
