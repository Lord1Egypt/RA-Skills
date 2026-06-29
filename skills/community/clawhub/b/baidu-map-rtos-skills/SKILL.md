---
name: baidu-map-rtos-skills
description: 百度地图 RTOS SDK（mapsdk-rtos）应用层集成规范与代码生成。帮助应用开发者对接 mapsdk-rtos，开发类似 rtos-mac-simulator（mapAPP）的应用层，包含初始化鉴权、地图组件控制、覆盖物（Marker/Polyline）、检索路线、离线地图、导航、Canvas 适配层等能力。当用户提到：对接 RTOS 地图 SDK、集成 mapsdk-rtos、RTOS 地图初始化、MapComponentApi、AuthLicenseApi、SearchApi、NaviApi、MapOfflineApi、Canvas 适配、RTOS 覆盖物、RTOS 导航、RTOS 离线地图时，必须使用本 skill 确保生成正确可运行的代码。
---

# mapsdk-rtos 应用层集成规范

## 目标与边界

- **目标**：帮助应用开发者正确集成 mapsdk-rtos，生成符合 SDK 公开 API 规范的业务代码。
- **负责**：鉴权与 License、地图组件初始化、地图状态控制、覆盖物（Marker/Polyline）、检索与路线规划、离线地图、导航、Canvas 适配层要点、macOS 模拟器（mapAPP）扩展新 Demo。
- **不负责**：SDK 内部实现修改；若需改 SDK 源码，阅读 `mapsdk-rtos` 工程后再操作。

## 使用时机

满足其一即启用：

- 集成 `outputIncludes/` 下的 `*_api.h` 头文件
- 调用 `MapComponentApi` / `AuthLicenseApi` / `SearchApi` / `NaviApi` / `MapOfflineApi`
- 实现或调试 Canvas 适配层（`drawImage`、`measureText`、`stroke` 等）
- 在 rtos-mac-simulator（mapAPP）工程中扩展新 Demo
- 排查地图不渲染、覆盖物不可见、鉴权失败、离线列表为空等问题

## 对外头文件（`outputIncludes/`）

| 头文件 | 职责 |
|--------|------|
| `map_component_api.h` | 地图组件（`MapComponentApi`） |
| `auth_license_api.h` | 鉴权与 License（`AuthLicenseApi`） |
| `base_api.h` | 基础能力（包名、缓存路径、版本） |
| `search_api.h` | 检索聚合入口（POI、路线、逆地理） |
| `navi_api.h` | 导航（`NaviApi`） |
| `offline/map_offline_api.h` | 离线地图（`MapOfflineApi`） |

非 `*_api.h` 文件多为类型/枚举/结构体，按 `*_api.h` include 关系引用即可。

## 快速参考

详细 API 及注意事项按需阅读参考文件：

- [init-auth.md](references/init-auth.md) — 鉴权、初始化顺序、Canvas 适配、联调验收清单、排障关键字。
- [adapter-build.md](references/adapter-build.md) — 平台 Adapter 接口清单（C 函数桩 + C++ 适配类）、MapCanvasImpl 实现要点与绑定流程。
- [overlay-map-control.md](references/overlay-map-control.md) — 地图状态控制、Marker、Polyline（点集 / GeoJSON）、触摸事件、路线瓦片预加载。
- [search-navi-offline.md](references/search-navi-offline.md) — 检索（POI/逆地理/路线规划）、导航、离线地图、mapAPP Demo 扩展。
- [demo.md](references/demo.md) — 全流程可运行示例（main 初始化、地图状态与覆盖物、触摸、POI 搜索、离线、路线瓦片、导航）。

## 常见问题速查

| 现象 | 首先检查 |
|------|----------|
| 折线 / Marker 有数据不可见 | 显式设置线宽与颜色；确认已 `showOverlay` + `updateLayer` + `RequestRender` |
| 地图白屏 / 不渲染 | 确认 `Authenticate` 成功、`MarkComponentAlive(true)`、`SetCanvas`、`InitMap` 顺序 |
| 步行 / POI 无结果 | 检查鉴权 token、网络层实现、坐标顺序（纬度, 经度） |
| 离线列表为空 | 先 `RequestVersion`，确认 callback 成功后再 `GetDownloadableCityList` |
| 路线瓦片 progress=-1 | 瓦片数量超限 |
| 实机与模拟器绘制不一致 | 查 Canvas 后端 stroke/clip/transform，不要先怀疑 GeoJSON 数据丢点 |
| MSVC LNK2038 | SDK 与 mapAPP 须同为 Debug 或 Release |
