---
name: arcgis-agent
description: 'ArcGIS Agent - drive 2500+ ArcGIS Pro geoprocessing tools across 46 toolboxes (buffer/clip/intersect, slope/aspect/viewshed, kriging/IDW, hotspot/Moran''s I, image analysis, GeoAI deep learning, multidimensional rasters, utility networks, geocoding and more) with natural language, via a local HTTP API. Use when the user asks for GIS/spatial analysis, ArcGIS automation, or arcpy operations. Requires Windows + ArcGIS Pro 3.x. 通过自然语言驱动 ArcGIS Pro 的 2500+ 个 arcpy 空间分析工具，覆盖 46 个工具箱（缓冲区/裁剪/相交、坡度/可视域、克里金/IDW、热点分析、影像分析、GeoAI 深度学习、多维栅格、公共设施网络、地址匹配等）。适用于 GIS 与空间分析、ArcGIS 自动化、arcpy 操作等需求。需要 Windows + ArcGIS Pro 3.x。'
version: 1.2.0
metadata:
  author: based on zhaojj662/arcpy-mcp-server (MIT)
  source: https://github.com/zhaojj662/arcpy-mcp-server
  tags: [gis, arcgis, arcpy, spatial-analysis, mcp]
---

# ArcGIS Agent

## English

Drive 2500+ arcpy tools (46 toolboxes) on the local ArcGIS Pro installation, letting an AI assistant complete spatial analysis tasks in natural language.

Architecture: `this skill (agent) --HTTP--> scripts/server.py (arcpy) --> ArcGIS Pro 3.x`

### Prerequisites

- Windows 10/11 + **ArcGIS Pro 3.x** with a valid license — arcpy only runs inside the Python shipped with ArcGIS Pro
- Server address: `http://127.0.0.1:8765` (localhost only)

### Step 1 — make sure the server is running

```bash
curl -s http://127.0.0.1:8765/health
# {"status":"ok","server":"arcpy-mcp-server","version":"2.1","tools":2500,"modules":46}
```

If it is not running, start it in the background with ArcGIS Pro's own Python:

```bash
"C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" "<skill_dir>/scripts/server.py" 8765
```

On Windows you can also run `scripts/start_server.bat` (foreground window, Ctrl+C to stop).

### Step 2 — call tools (plain HTTP, no MCP client needed)

```bash
# list all modules and their tool counts
curl -s http://127.0.0.1:8765/modules

# list every tool in one module (e.g. analysis)
curl -s http://127.0.0.1:8765/module/analysis

# run a tool: POST /call with body {"name": "<module>_<tool>", "arguments": {...}}
curl -s -X POST http://127.0.0.1:8765/call -H "Content-Type: application/json" \
  -d '{"name":"analysis_Buffer","arguments":{"in_features":"C:/data/roads.shp","out_feature_class":"C:/out/roads_buf.shp","buffer_distance_or_field":"500 meters"}}'
```

Naming rule: `{module}_{ToolName}`, e.g. `analysis_Buffer`, `sa_Reclassify`, `ga_Kriging`.
When unsure, browse `/modules` → `/module/{name}`, then confirm a single tool with `/tool/{tool_id}`.
Arguments are the keyword parameters of the underlying arcpy tool (see the ArcGIS Pro documentation for each tool signature).

### Module cheat-sheet (46 toolboxes, grouped by availability)

**Core local toolboxes** (available with a basic license):

| Module | Tools | Purpose |
|---|---|---|
| management | 431 | Data management, projections, fields, topology |
| conversion | 59 | shp/gdb/KML/CAD/Excel/raster conversion |
| stats | 59 | Moran's I, Gi*, KDE, GWR |
| cartography | 48 | Generalization, annotation, masking |
| analysis | 38 | Buffer, Clip, Intersect, Erase, Thiessen |
| geocoding | 18 | Address matching, reverse geocoding |
| edit | 18 | Align, extend, trim, merge |
| server | 20 | Service publishing, tile caching |
| sharing | 3 | Web layers, web maps |

**Extension toolboxes** (registration is free; calls require the matching extension license):

| Module | Tools | Purpose | Extension |
|---|---|---|---|
| sa | 363 | Slope, reclassify, viewshed, hydrology, density | Spatial Analyst |
| ia | 328 | Raster functions, image classification, DL inference | Image Analyst |
| ddd | 150 | DEM, contours, skyline, point cloud | 3D Analyst |
| un / nd / tn | 117/72/13 | Utility network, diagrams, trace network | Utility Network |
| nax / na | 94/57 | Routes, service areas, OD matrix | Network Analyst |
| ga | 42 | Kriging, IDW, EBK | Geostatistical |
| aviation / topographic / defense | 47/67/24 | Aviation / map production / defense mapping | respective ext. |
| locref / lr | 44/7 | Linear referencing, roadway | Roads & Highways |
| ba | 46 | Site selection, market analysis | Business Analyst |
| parcel | 25 | Parcel fabric | Parcel Fabric |
| md | 20 | Multidimensional rasters, NetCDF, climate data | built into 3.x |
| indoors / indoorpositioning | 22/8 | Indoor GIS / positioning | Indoors |
| maritime / bathymetry | 22/8 | S-57 charts, bathymetry | Maritime |
| ca / td / intelligence | 13/19/18 | Crime analysis / territory design / intelligence | respective ext. |
| rm / oi / reviewer / wmx / transit / geoai | 14/6/5/18/8/12 | Ortho mapping / oriented imagery / QA / workflow / GTFS / GeoAI | respective ext. |

**Portal / Enterprise modules** (calls require an active Portal or ArcGIS Online sign-in): `ra`, `geoanalytics`, `gapro`, `sfa`, `agolservices`

The authoritative runtime list is always `/modules` and `/module/{name}` — tool counts vary with the extensions installed on each machine.

### Typical composite call chains

Site-selection requests such as "hospital within 500 m of a main road and slope below 5 degrees" are decomposed into several `/call`s:

1. `analysis_Buffer` on roads 500 m → 2. `ddd_Slope` on the DEM → 3. `sa_Reclassify` to binarize slope → 4. `analysis_Intersect` to stack the layers

More examples (buffer, kriging, hotspot analysis, viewshed, projections, field calculation) are in `references/examples.md`.

### Error handling

Errors come back as `{"status":"error","message":"...","suggestion":"..."}`. Frequent codes:

- `000732`: dataset does not exist → check the path and extension first
- `000725`: output already exists (the server sets `overwriteOutput=True`, so this is rare)
- `000735` / `000622`: wrong parameter format or type → verify the tool signature

Successful responses include elapsed time in `info`; for vector/raster outputs they also report feature count, geometry type or raster size.

### Security and configuration

- The server binds to `127.0.0.1` only and is unreachable from the LAN
- Path whitelist: by default only `.shp/.tif/.gdb` under `C:/GIS-AI-Course/` may be read or written. Extend it with the `ARCPY_ALLOWED_PATHS` environment variable (semicolon-separated), e.g. `set ARCPY_ALLOWED_PATHS=C:/GIS-AI-Course/;D:/data/`
- Module whitelist: edit `INCLUDE_MODULES` in `scripts/server.py` to expose only what you need
- Confirm the target data with the user before write operations in the `management` / `edit` modules

## 中文

驱动本机 ArcGIS Pro 的 **2500+ arcpy 工具（46 个工具箱）**，让 AI 直接用自然语言完成空间分析。

架构：`本技能(Agent) --HTTP--> scripts/server.py (arcpy) --> ArcGIS Pro 3.x`

### 前置条件

- Windows 10/11 + **ArcGIS Pro 3.x**（有效许可证）——arcpy 只能在 ArcGIS Pro 自带的 Python 中运行
- 服务端 HTTP 地址：`http://127.0.0.1:8765`（仅本机监听）

### 第一步：确保服务在运行

```bash
curl -s http://127.0.0.1:8765/health
# {"status":"ok","server":"arcpy-mcp-server","version":"2.1","tools":2500,"modules":46}
```

若未启动，后台启动服务（用 ArcGIS Pro 自带 Python）：

```bash
"C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" "<本技能目录>/scripts/server.py" 8765
```

Windows 下也可运行 `scripts/start_server.bat`（前台窗口，Ctrl+C 停止）。

### 第二步：调用工具（纯 HTTP，无需 MCP 客户端）

```bash
# 列出全部模块及工具数量
curl -s http://127.0.0.1:8765/modules

# 列出某个模块的全部工具名（如分析模块）
curl -s http://127.0.0.1:8765/module/analysis

# 执行工具：POST /call  body = {"name": "模块_工具名", "arguments": {...}}
curl -s -X POST http://127.0.0.1:8765/call -H "Content-Type: application/json" \
  -d '{"name":"analysis_Buffer","arguments":{"in_features":"C:/data/roads.shp","out_feature_class":"C:/out/roads_buf.shp","buffer_distance_or_field":"500 meters"}}'
```

工具命名规则：`{模块名}_{工具名}`，如 `analysis_Buffer`、`sa_Reclassify`、`ga_Kriging`。
不确定工具名时，先查 `/modules` → `/module/{name}`，再用 `/tool/{工具id}` 确认。
参数为 arcpy 该工具的关键字参数（详见 ArcGIS Pro 官方文档中的对应工具签名）。

### 模块速查（46 个工具箱，按可用性分组）

**核心本地模块**（基础许可即可用）：

| 模块 | 工具数 | 用途 |
|---|---|---|
| management | 431 | 数据管理、投影、字段、拓扑 |
| conversion | 59 | shp/gdb/KML/CAD/Excel/栅格互转 |
| stats (空间统计) | 59 | Moran's I、Gi*、KDE、GWR |
| cartography | 48 | 制图综合、注记、掩膜 |
| analysis | 38 | 缓冲区、裁剪、相交、擦除、泰森多边形 |
| geocoding | 18 | 地址匹配、反查 |
| edit | 18 | 对齐、延伸、裁剪、合并 |
| server | 20 | 服务发布、缓存切片 |
| sharing | 3 | Web 图层/Web 地图分享 |

**扩展模块**（注册无门槛，调用需对应扩展许可证）：

| 模块 | 工具数 | 用途 | 需要的扩展 |
|---|---|---|---|
| sa | 363 | 坡度坡向、重分类、可视域、水文、密度 | Spatial Analyst |
| ia | 328 | 栅格函数、影像分类、深度学习推理 | Image Analyst |
| ddd | 150 | DEM、等高线、天际线、点云 | 3D Analyst |
| un / nd / tn | 117/72/13 | 公共设施网络、网络示意图、追踪网络 | Utility Network |
| nax / na | 94/57 | 路径、服务区、OD 矩阵 | Network Analyst |
| ga | 42 | 克里金、IDW、EBK | Geostatistical |
| aviation / topographic / defense | 47/67/24 | 航空/地形生产/国防制图 | 对应扩展 |
| locref / lr | 44/7 | 线性参考、道路仪器 | Roads & Highways |
| ba | 46 | 商业选址、市场分析 | Business Analyst |
| parcel | 25 | 宗地结构 | Parcel Fabric |
| md | 20 | 多维栅格、NetCDF、气候数据 | 无（3.x 自带） |
| indoors / indoorpositioning | 22/8 | 室内 GIS/定位 | Indoors |
| maritime / bathymetry | 22/8 | 海图 S-57/测深 | Maritime |
| ca / td / intelligence | 13/19/18 | 犯罪分析/区域设计/情报 | 对应扩展 |
| rm / oi / reviewer / wmx / transit / geoai | 14/6/5/18/8/12 | 正射/定向影像/质检/工作流/GTFS/GeoAI | 对应扩展 |

**门户/企业服务模块**（调用需已登录 Portal 或 ArcGIS Online）：`ra`、`geoanalytics`、`gapro`、`sfa`、`agolservices`

完整模块与工具列表运行时以 `/modules` 和 `/module/{name}` 为准（不同机器扩展安装情况不同，工具总数会有差异）。

### 典型调用链（复合分析）

选址类需求按"缓冲区→叠加→筛选"链条自动拆解为多次 `/call`，例：
医院选址（距主干道 500m 内、坡度 < 5°）：

1. `analysis_Buffer` 道路 500m → 2. `ddd_Slope` DEM 求坡度 → 3. `sa_Reclassify` 坡度二值化 → 4. `analysis_Intersect` 叠加取交集

更多示例（缓冲区、克里金、热点分析、可视域、投影、字段计算等）见 `references/examples.md`。

### 错误处理

返回 `{"status":"error","message":"...","suggestion":"..."}`，常见代码：

- `000732`：数据集不存在 → 先确认路径/扩展名
- `000725`：输出已存在（服务端已自动 `overwriteOutput=True`，一般不出现）
- `000735` / `000622`：参数格式或类型错误 → 核对工具签名

结果中 `info` 含执行耗时；若输出为矢量/栅格数据，还会带要素数、几何类型或栅格尺寸。

### 安全与配置

- 服务只监听 `127.0.0.1`，不会暴露到局域网
- 路径白名单：默认只允许 `C:/GIS-AI-Course/` 下的 .shp/.tif/.gdb 读写；用环境变量 `ARCPY_ALLOWED_PATHS`（分号分隔多个路径）放开其他目录，例如
  `set ARCPY_ALLOWED_PATHS=C:/GIS-AI-Course/;D:/data/`
- 模块白名单：编辑 `scripts/server.py` 中 `INCLUDE_MODULES` 只暴露需要的模块
- 谨慎执行 `management`/`edit` 模块的写操作前，向用户确认目标数据
