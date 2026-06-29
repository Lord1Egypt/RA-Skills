# 工作区

[English](README_EN.md)

本仓库提供面向 **百度地图 RTOS SDK（mapsdk-rtos）** 的 AI Coding Agent Skill，帮助开发者在智能研发工具（如 Cursor / Claude Code 等）中高效完成 RTOS 地图应用层集成、Canvas 适配、地图组件控制、覆盖物绘制、检索路线、离线地图与导航等开发任务。

## Skills 概览

本仓库包含以下一个 Skill：

| Skill | 说明 |
| --- | --- |
| [baidu-map-rtos-skills](./) | 百度地图 RTOS SDK（mapsdk-rtos）应用层集成开发助手 |

---

### baidu-map-rtos-skills

百度地图 RTOS SDK（mapsdk-rtos）应用层集成规范与代码生成。

- **初始化与鉴权** — License 鉴权、基础配置、包名/缓存路径/版本信息、初始化顺序与联调验收
- **地图组件控制** — `MapComponentApi` 初始化、生命周期、地图状态控制、渲染请求与触摸事件
- **Canvas 适配层** — C 函数桩、C++ 适配类、`MapCanvasImpl` 绑定、绘制/文本/裁剪/变换等实现要点
- **覆盖物绘制** — Marker、Polyline、点集 / GeoJSON、样式设置、显示隐藏与图层更新
- **检索与路线规划** — POI 检索、逆地理、步行/驾车路线规划、路线瓦片预加载
- **离线地图** — 版本请求、可下载城市列表、下载状态、离线包管理
- **导航能力** — `NaviApi` 初始化、路线结果接入、导航启动与状态监听
- **Demo 扩展** — 在 rtos-mac-simulator（mapAPP）工程中扩展新的应用层 Demo

适用于对接 `outputIncludes/` 下 `*_api.h` 公开头文件的 RTOS 地图应用开发场景。

## 适用环境

- **平台**：RTOS / macOS 模拟器（rtos-mac-simulator / mapAPP）
- **开发语言**：C / C++
- **SDK**：mapsdk-rtos
- **核心 API**：`MapComponentApi`、`AuthLicenseApi`、`SearchApi`、`NaviApi`、`MapOfflineApi`
- **集成方式**：对接 `outputIncludes/` 公开头文件与平台 Adapter / Canvas 实现

## 目录结构

```
rtos-sdk-skills/
├── README.md                         # 本文件（中文）
├── README_EN.md                      # English README
├── SKILL.md                          # Skill 定义文件
└── references/
    ├── adapter-build.md              # 平台 Adapter 与 Canvas 适配实现
    ├── demo.md                       # 全流程可运行示例
    ├── init-auth.md                  # 初始化、鉴权与排障
    ├── overlay-map-control.md        # 地图控制与覆盖物
    └── search-navi-offline.md        # 检索、导航与离线地图
```

## 使用方式

### 1. 克隆本仓库

```bash
git clone https://github.com/baidu-maps/rtos-sdk-skills.git
cd rtos-sdk-skills
```

### 2. 从 Release 下载（可选）

你也可以直接从 [Releases](https://github.com/baidu-maps/rtos-sdk-skills/releases) 下载附件 `rtos-sdk-skills.zip`，然后解压使用：

```bash
unzip rtos-sdk-skills.zip
cd rtos-sdk-skills
```

### 3. 将 Skill 注册到你的 AI 助手

把本仓库目录链接或复制到当前环境对应的 skills 目录，这样 AI 在对话时会自动读取这些文档。

**Claude Code（本地）**

- Skills 目录一般为：`~/.claude/skills/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)" ~/.claude/skills/baidu-map-rtos-skills
  ```
- 或直接把本仓库文件夹复制到 `~/.claude/skills/baidu-map-rtos-skills` 下。

**Cursor**

- Skills 目录一般为：`~/.cursor/skills-cursor/`
- 注册（软链，推荐）：
  ```bash
  ln -sfn "$(pwd)" ~/.cursor/skills-cursor/baidu-map-rtos-skills
  ```
- 或直接把本仓库文件夹复制到 `~/.cursor/skills-cursor/baidu-map-rtos-skills` 下。

### 4. 在对话中使用

在支持 Skills 的客户端里，当你的问题涉及「RTOS 地图 SDK」「mapsdk-rtos」「MapComponentApi」「AuthLicenseApi」「SearchApi」「NaviApi」「MapOfflineApi」「Canvas 适配」「RTOS 覆盖物」「RTOS 导航」「RTOS 离线地图」等关键词时，助手会优先参考本仓库文档来回答，从而给出更贴合百度地图 RTOS SDK 的代码与用法。

## 参考文档

- [SKILL.md](SKILL.md) — Skill 触发说明、能力边界与快速参考
- [references/init-auth.md](references/init-auth.md) — 鉴权、初始化顺序、Canvas 适配、联调验收清单、排障关键字
- [references/adapter-build.md](references/adapter-build.md) — 平台 Adapter 接口清单、`MapCanvasImpl` 实现要点与绑定流程
- [references/overlay-map-control.md](references/overlay-map-control.md) — 地图状态控制、Marker、Polyline、触摸事件、路线瓦片预加载
- [references/search-navi-offline.md](references/search-navi-offline.md) — 检索、导航、离线地图、mapAPP Demo 扩展
- [references/demo.md](references/demo.md) — 全流程可运行示例

## 许可证

本项目为百度内部项目，仅供授权使用。
