---
name: baidu-map-android-sdk
description: 百度地图 Android SDK 集成与开发规范。覆盖地图展示、MapView/BaiduMap 生命周期、定位、标注与覆盖物、POI 检索、路线规划、步骑行导航；输出符合隐私与 AK 配置的 Android 地图方案。在开发 Android 地图应用、集成百度地图 SDK、MapView、路线规划、POI、导航时使用。
compatibility: Android, Gradle, Android Studio
---

# 百度地图 Android SDK

## 目标与边界

- **目标**：在 Android 工程中正确集成百度地图 SDK，并给出符合隐私、AK、坐标系规范的实现方案。
- **负责**：地图展示、MapView 生命周期、覆盖物、POI/路线/地理编码检索、步骑行导航等；以技能内 references 为准。
- **不负责**：服务端逻辑、非百度 SDK、UI 视觉设计。

## 使用时机

满足其一即启用本技能：

- 关键词：百度地图 Android、MapView、BaiduMap、AK、路线规划、POI 检索、步骑行导航、BD09、坐标类型
- 需求类型：地图展示、定位、标注与覆盖物、POI/地点检索、路线规划与画线、步行/骑行实时导航、地理编码

**按需加载**：先根据需求在 [reference.md](references/reference.md) 中选定文档，再引用对应 references 内容；需求含糊时先向用户澄清**再给方案**。

## 必须遵守的规则

1. **隐私与初始化（v7.5.0+）**
   - 调用 SDK 任何接口前必须先调用隐私合规接口，且**必须在 `SDKInitializer.initialize` 之前**调用。见 [overview.md](references/overview.md) 隐私合规小节。
   - Application 中：`SDKInitializer.initialize(this)`；自 4.3.0 起可用 `SDKInitializer.setCoordType(CoordType.BD09LL)` 或 `CoordType.GCJ02`。

2. **AK 与配置**
   - 使用前需在控制台申请 Android SDK 密钥（AK），应用类型选「Android SDK」，填写包名、SHA1。AK 配置到 AndroidManifest 或 `SDKInitializer.setApiKey`；包名与签名须与申请一致。见 [overview.md](references/overview.md)。

3. **MapView 生命周期**
   - Activity 的 `onResume`/`onPause`/`onDestroy` 中必须分别调用 `mMapView.onResume()`、`mMapView.onPause()`、`mMapView.onDestroy()`。见 [mapview.md](references/mapview.md)。

4. **坐标系**
   - 国内默认 BD09LL；可与 GCJ02 通过 `SDKInitializer.setCoordType` 统一。与定位混用时与定位 SDK 坐标类型一致；转换见 [coordinate.md](references/coordinate.md)。

5. **检索与路线**
   - **监听先于请求**：先 `setOnGetPoiSearchResultListener` 再 `searchNearby` 等；先 `setOnGetRoutePlanResultListener` 再 `drivingSearch` 等，否则可能拿不到回调。用完后 `destroy()` 释放实例。

6. **版本与 API 以工程为准**
   - 用户已集成 SDK 时，以其实机/工程内版本为准。若某类或方法**不存在**（编译报错或依赖中无此符号），**提示用户将对应依赖更新到兼容版本**后再重试，勿强行写不存在的 API。

7. **步骑行：按需求区分**
   - **路线规划（算路+画线）**：RoutePlanSearch（驾车/步行/骑行/公交），得到路线后自绘折线或使用开源 Overlay。见 [route.md](references/route.md)。
   - **步骑行实时导航**：步行/骑行导航引擎、诱导、TTS、偏航纠偏等，类见 [overview.md](references/overview.md) 与 [class-reference.md](references/class-reference.md)。
   - 二者是**不同服务**：仅需画线用 route；需实时诱导/TTS 用步骑行导航。给出方案前先按开发者需求选对文档。

## 输出规范（可评估）

- **可落地**：含具体类名、方法、调用顺序与必要配置（AndroidManifest、Application、AK、隐私）。
- **可验证**：隐私与 AK 明确；检索/路线监听顺序正确；若涉及定位/鉴权失败，方案可指向 [location.md](references/location.md) 或 [project-config.md](references/project-config.md) 的排查项。
- **可组合**：按 [reference.md](references/reference.md) 选文档与常见组合。无特殊要求时界面与交互遵循 [ui-standards.md](references/ui-standards.md)。

方案结构：需求 → 对应文档 → 配置与依赖 → 关键 API → 示例片段 → 注意事项。

## 参考索引

- 按需求选文档与常见组合：[reference.md](references/reference.md)
- Gradle 集成（依赖、冲突、NDK、环境与国内镜像）：[gradle.md](references/gradle.md)
- AndroidManifest、主题、混淆、集成经验与常见问题：[project-config.md](references/project-config.md)
- 集成、AK、隐私、生命周期、核心类：[overview.md](references/overview.md)
- 地图容器、类型、层级、方法交互：[mapview.md](references/mapview.md)
- 显示定位、定位模式、自定义图标：[location.md](references/location.md)
- 点标记、Marker 属性与事件：[marker.md](references/marker.md)
- 折线、多边形、Polyline 属性：[overlays.md](references/overlays.md)
- POI、地理编码、逆地理：[search.md](references/search.md)
- 路线规划与 Overlay：[route.md](references/route.md)
- 坐标转换与坐标系：[coordinate.md](references/coordinate.md)
- 距离/面积、点与图形关系、调起地图、短地址分享：[tools.md](references/tools.md)
- 错误码：[errorcode.md](references/errorcode.md)
- 类与包速查：[class-reference.md](references/class-reference.md)
- 检索/路线/选点/弹窗/Logo 等 UI 与交互约定：[ui-standards.md](references/ui-standards.md)
