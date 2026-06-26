# 百度地图 iOS SDK 参考索引

按需选下表文档；通用规则（隐私、坐标系、版本以本地为准）见 [SKILL.md](../SKILL.md)。

## 按需求选文档

| 你要做的 | 用到的文档 |
|----------|------------|
| 集成 Pod、选地图/定位/步骑行/导航套件 | [cocoapods.md](cocoapods.md) |
| Info.plist、隐私弹窗、Launch Screen、构建沙盒 | [project-config.md](project-config.md) |
| 单次/连续/后台/室内定位、地理围栏、鉴权失败 | [location.md](location.md) |
| 地图视图、属性、生命周期、全屏 | [mapview.md](mapview.md) |
| 点标注、固定屏、点聚合展示 | [annotations.md](annotations.md) |
| 覆盖物、热力、点聚合逻辑、轨迹、Marker/RichView | [overlays.md](overlays.md) |
| 检索/路线/选点/弹窗/视野/Logo 等 UI 规范 | [ui-standards.md](ui-standards.md) |
| Sug、地理编码、逆地理、POI、公交 | [search.md](search.md) |
| 驾车/步行/骑行/公交**算路与画线**（BMKRouteSearch，仅算路+画线） | [route.md](route.md) |
| **步骑行实时导航**（BaiduWalkNaviKit，诱导、TTS、偏航纠偏、多实例） | [navi.md](navi.md) |
| 坐标转换、几何、视野适配、调起地图 | [utils.md](utils.md) |
| 图片资源路径与命名 | [assets.md](assets.md) |
| 类与头文件速查 | [class-index.md](class-index.md) |

**步骑行**：算路画线（route）与实时导航（navi）为**不同服务**——仅画线用 route，要诱导/TTS/偏航用 [navi.md](navi.md)。

## 文档一览与边界

| 文档 | 内容 | 边界 |
|------|------|------|
| [cocoapods.md](cocoapods.md) | Podfile、pod 命令、地图/定位/步骑行套件 | 构建报错见 [project-config.md](project-config.md) |
| [project-config.md](project-config.md) | Info.plist、隐私弹窗、Launch Screen、CocoaPods 沙盒 | 仅百度 SDK 相关配置 |
| [location.md](location.md) | BMKLocationKit、定位方式、鉴权排查、坐标系 | 不含步骑行导航内部定位 |
| [mapview.md](mapview.md) | BMKMapView、状态、生命周期 | 不含标注/覆盖物具体类型 |
| [annotations.md](annotations.md) | 标注、固定屏、点聚合展示 | 聚类逻辑见 [overlays.md](overlays.md) |
| [overlays.md](overlays.md) | 覆盖物、热力、点聚合逻辑、轨迹、Marker | 与 annotations 组合使用 |
| [ui-standards.md](ui-standards.md) | 检索/路线/选点/弹窗/视野/Logo 等 UI 标准 | 无特殊要求时方案按此实现 |
| [search.md](search.md) | Sug、地理编码、逆地理、POI、公交 | 路线算路见 [route.md](route.md) |
| [route.md](route.md) | BMKRouteSearch：驾车/步行/骑行/公交算路与画线、BMKPlanNode、路况 | 与 walkcyclenavi 不同服务；仅算路+画线用本文档 |
| [navi.md](navi.md) | BaiduWalkNaviKit：步骑行实时导航、诱导、TTS、偏航、多实例、无UI | 与 route 不同服务；需实时导航用本文档 |
| [utils.md](utils.md) | BMKCoordTrans、BMKGeometry、视野、调起地图 | 工具类，与其它文档组合 |
| [assets.md](assets.md) | 图片资源 | 技能内 assets 目录 |
| [class-index.md](class-index.md) | 类与头文件速查 | 用法与示例见各功能文档 |

## 常见组合

| 需求 | 文档组合 |
|------|----------|
| 地图 + 定位 | cocoapods → project-config → mapview + location（坐标系统一 BD09） |
| 地图 + 路线画线 | mapview + route + search（选点）；步骑行仅画线用 route |
| 步骑行实时导航 | cocoapods（BaiduWalkNaviKit）→ project-config → navi |
| 标注 + 点聚合 | annotations + overlays（聚类与 Marker） |
| 定位鉴权失败 | [location.md](location.md)「鉴权失败排查」+ project-config 隐私与 Info.plist |
