---
name: coord-transform
version: 1.0.0
description: 坐标转换技能。当用户提到坐标转换、坐标系转换、EPSG转换、CGCS2000、WGS84、地理坐标转换、投影坐标转换、火星坐标系、百度坐标转换时激活。支持GeoJSON文件和WKT字符串的坐标系统转换，支持中国常用坐标系互转。
---

# 坐标转换技能 (coord-transform)

坐标系转换工具，支持 GeoJSON 和 WKT 格式，支持中国常用坐标系。

## 核心功能

- **格式互转**：WKT ↔ GeoJSON 互转
- **坐标转换**：支持各种坐标系之间的转换
- **中国坐标系**：完整支持 CGCS2000、WGS84、火星坐标系(GCJ-02)、百度坐标系(BD-09)

## 支持的坐标系

| 代码 | 名称 | 说明 |
|------|------|------|
| 4326 | WGS84 | GPS 标准，地理坐标 |
| 4490 | CGCS2000 | 中国 2000 国家坐标系 |
| 4547-4556 | CGCS2000 分带 | 3 度分带投影坐标系 |
| 3857 | Web Mercator | 互联网地图常用 |
| 4214 | Beijing 1954 | 北京 54 坐标系 |
| gcj02 | 火星坐标系 | 高德地图、腾讯地图使用 |
| bd09 | 百度坐标系 | 百度地图专属 |

## 依赖

```bash
apt-get install python3-pyproj
```

## 使用方式

### 基本语法

```
python3 scripts/coord_convert.py --input <文件或字符串> --from <源坐标系> --to <目标坐标系> [--format <输出格式>] [--output <输出文件>]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--input` / `-i` | 输入文件路径或 GeoJSON/WKT 字符串 |
| `--wkt` | 直接指定 WKT 字符串（覆盖 --input） |
| `--from` / `-f` | 源坐标系 |
| `--to` / `-t` | 目标坐标系 |
| `--format` / `-F` | 输出格式：geojson / wkt / auto（默认 auto） |
| `--output` / `-o` | 输出文件路径 |
| `--list-crs` | 列出所有支持的坐标系 |

## 使用示例

### 1. 坐标系统转换

**CGCS2000 (4490) → WGS84 (4326)：**
```bash
python3 scripts/coord_convert.py --wkt "POINT(113 23)" --from 4490 --to 4326
```

**CGCS2000 (4490) → 投影坐标系 (4547)：**
```bash
python3 scripts/coord_convert.py --wkt "POLYGON((112.58 26.56,112.60 26.56,112.60 26.58,112.58 26.58,112.58 26.56))" --from 4490 --to 4547
```

### 2. WKT ↔ GeoJSON 格式互转

**WKT 转 GeoJSON：**
```bash
python3 scripts/coord_convert.py --wkt "POINT(113 23)" --from 4326 --to 4490 --format geojson
```

**GeoJSON 转 WKT：**
```bash
python3 scripts/coord_convert.py --input data.geojson --from 4490 --to 4326 --format wkt
```

### 3. 火星坐标系转换

**WGS84 → 火星坐标系 (GCJ-02)：**
```bash
python3 scripts/coord_convert.py --wkt "POINT(113 23)" --from 4326 --to gcj02
```

**火星坐标系 → WGS84：**
```bash
python3 scripts/coord_convert.py --wkt "POINT(113 23)" --from gcj02 --to 4326
```

### 4. 百度坐标系转换

**GCJ-02 → 百度坐标系 (BD-09)：**
```bash
python3 scripts/coord_convert.py --wkt "POINT(113 23)" --from gcj02 --to bd09
```

**BD-09 → WGS84：**
```bash
python3 scripts/coord_convert.py --wkt "POINT(113 23)" --from bd09 --to 4326
```

### 5. 完整流程示例

**从百度坐标系的 GeoJSON 文件转换到 CGCS2000 投影坐标系：**
```bash
python3 scripts/coord_convert.py --input baidu_data.geojson --from bd09 --to 4547 --output result.geojson
```

## 工作流程

1. 解析输入（判断是 WKT 还是 GeoJSON）
2. 解析源坐标系和目标坐标系
3. 如果需要格式转换，先进行格式转换
4. 使用合适的转换器（pyproj 或中国坐标转换算法）转换坐标
5. 输出转换后的结果

## 输出格式

- GeoJSON 输入 → 默认输出 GeoJSON
- WKT 输入 → 默认输出 WKT
- 可用 `--format` 参数强制指定输出格式

## 坐标系转换关系图

```
WGS84 (4326) ←→ GCJ-02 (火星坐标系) ←→ BD-09 (百度坐标系)
     ↑                ↑                    ↑
     └────────────────┼────────────────────┘
                     ↓
              CGCS2000 (4490)
                    ↓
           CGCS2000 分带 (4547-4556)
```

## 注意事项

1. **火星坐标系和百度坐标系是中国特有的加密坐标系**，无法直接用 pyproj 转换，使用内置算法
2. **WGS84 和 CGCS2000 在中国境内差异很小**（通常 <1米），实际使用中可互换
3. **投影坐标系（如 4547）是平面坐标**，单位为米，适用于工程测量
4. **地理坐标系（如 4326）是经纬度**，单位为度
