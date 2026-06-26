---
name: baidu-mapbox-isochrone
description: 生成等时圈（isochrone）。通过百度地理编码API将地址转为BD-09坐标，转换为WGS84后，调用Mapbox Isochrone API生成等时圈SHP文件和Python预览图。当用户需要：给定地址生成等时圈地图、百度坐标转WGS84后做等时圈分析、生成等时圈shapefile并提供预览图时使用此技能。
---

# 等时圈生成器

通过百度地理编码 + 坐标转换 + Mapbox Isochrone API 生成等时圈 SHP 文件和预览图。

## 工作流程

执行 `scripts/generate_isochrone.py`，分 6 步完成：

```
[Step 1] 百度地理编码 (BD-09)
    → 地址 → 百度AK → BD-09 经纬度
[Step 2] 坐标转换 (BD-09 → WGS84)
    → coord_convert.bd2wgs()
[Step 3] Mapbox 等时圈 API
    → WGS84 坐标 + 出行模式 + 时间 → GeoJSON 等时圈面
[Step 4] 保存 Shapefile
    → point.shp（起点） + isochrone.shp（等时圈面）
[Step 5] 获取 WGS84 底图
    → ESRI 卫星影像瓦片 → rasterio 重投影为 WGS84 GeoTIFF
[Step 6] 生成预览图
    → matplotlib 叠加渲染（alpha=0.38半透明等时圈 + 卫星底图）
```

## ⚡ 自动发送流程（必须执行）

脚本成功后将触发自动发送，agent 必须执行以下步骤：

### Step A: 打包所有产物
```bash
cd <output_dir>
zip <名称>.zip point.shp point.shx point.dbf point.prj point.cpg \
    isochrone.shp isochrone.shx isochrone.dbf isochrone.prj isochrone.cpg \
    base_map_wgs84.tif isochrone_preview.jpg
```

### Step B: 发送预览图（通过 message 工具）
```
action: send
channel: feishu
message: 📍 <地址> · <N>分钟<出行模式>等时圈\n\n🗺️ WGS84坐标：<lng>, <lat>\n覆盖范围：<描述>
media: <preview_jpg路径>
```

### Step C: 发送 ZIP 文件包（通过 message 工具）
```
action: send
channel: feishu
message: 📦 SHP全套文件包（含.shp/.shx/.dbf/.prj/.cpg + 底图TIFF + 高清预览图）
filePath: <zip路径>
```

## 参数（按顺序）

| 序号 | 参数 | 说明 | 示例 |
|------|------|------|------|
| 1 | 地址 | 任意百度地图可识别的地址 | `天津市南楼煎饼` |
| 2 | 百度 AK | 百度地图开放平台 AK | MEMORY.md 中已存储 |
| 3 | Mapbox AK | Mapbox 访问令牌 | MEMORY.md 中已存储 |
| 4 | 出行模式 | driving / walking / cycling | `walking` |
| 5 | 时间(分钟) | 等时圈时长 | `15` |
| 6 | 输出目录 | 可选，默认为 `/root/.openclaw/workspace/isochrone_output` | 可省略 |

## 输出文件（默认路径）

生成在 `/root/.openclaw/workspace/isochrone_output/` 下：

| 文件 | 说明 | CRS |
|------|------|-----|
| `point.shp` | 起点（经纬度点） | EPSG:4326 |
| `isochrone.shp` | 等时圈面 | EPSG:4326 |
| `isochrone_preview.jpg` | 预览图（卫星底图 + 半透明等时圈） | — |
| `base_map_wgs84.tif` | WGS84 重投影底图（EPSG:4326 GeoTIFF） | EPSG:4326 |

## 使用示例

```
请帮我生成等时圈：
- 地址：天津市南楼煎饼
- 出行模式：walking
- 时间：15分钟
```

Agent 应执行：
```bash
python3 /root/.openclaw/workspace/skills/baidu-mapbox-isochrone/scripts/generate_isochrone.py "天津市南楼煎饼" "<百度AK>" "<MapboxAK>" "walking" 15
```

然后按"自动发送流程"打包并发送所有文件给用户。

## API 密钥

- 百度 AK：MEMORY.md → `百度AK` 字段
- Mapbox AK：MEMORY.md → `Mapbox AK` 字段

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| `百度地理编码失败` | AK 无效或地址无法识别 | 检查 AK / 换用更精确的地址 |
| `Mapbox API 认证失败` | Mapbox AK 错误 | 核对 AK |
| `Mapbox API 参数错误 (422)` | 坐标超出支持区域 | 确认地址在支持范围内 |
| 依赖缺失 | 包未安装 | `pip install coord_convert geopandas shapely pyshp matplotlib --break-system-packages` |

## 依赖

系统需安装中文字体（matplotlib 使用的字体名为 `Noto Sans CJK JP`，来自 NotoSansCJK-Regular.ttc）。

Python 依赖：
```
coord_convert, geopandas, shapely, pyshp, matplotlib, rasterio, scipy, pykdtree
```
