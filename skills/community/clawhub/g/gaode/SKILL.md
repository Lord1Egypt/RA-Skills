---
name: "高德地图"
version: "2.0.0"
description: "高德地图 Web API 工具与开发指南。Use for: (1) 用附带的零依赖 CLI 直接查地理编码/POI/路线/天气/IP定位, (2) 中国坐标系(WGS-84/GCJ-02/BD-09)转换与避坑, (3) 高德全套 Web Service API 开发指导。Amap (Gaode) Web API CLI (zero-dependency) for geocoding, POI search, routing, weather and IP location, plus China coordinate-system guide."
tags: ["gaode", "amap", "map", "lbs", "geocoding", "cli"]
author: "ClawSkills Team"
category: "navigation"
---

# 高德地图 Web API Skill

附带零依赖 CLI（`scripts/amap.py`，仅 Python 标准库），agent 可直接替
用户完成地理查询任务：地址↔坐标、找店、算路线、查天气、IP 定位。

## 快速开始

```bash
# lbs.amap.com 免费申请（个人开发者即可），Key 类型选 "Web服务"
export AMAP_KEY=你的key

python3 scripts/amap.py geocode "北京市朝阳区阜通东大街6号"
python3 scripts/amap.py around 116.481028,39.989643 咖啡 1000
python3 scripts/amap.py driving 116.481028,39.989643 116.434446,39.90816
python3 scripts/amap.py weather 110101 all
```

脚本行为声明：仅请求 `restapi.amap.com`，不读写本地文件。

## 命令手册

| 命令 | 作用 |
|------|------|
| `geocode <地址> [城市]` | 地址 → 坐标（返回 lng,lat 与规范化地址） |
| `regeo <lng,lat>` | 坐标 → 结构化地址（省市区街道） |
| `search <关键词> [城市]` | POI 关键词搜索 |
| `around <lng,lat> <关键词> [半径米]` | 周边搜索（默认 3000 米） |
| `driving / walking <起点> <终点>` | 路线规划（返回距离米/耗时秒/分步导航） |
| `weather <adcode> [all]` | 实况天气；带 `all` 返回未来 4 天预报 |
| `ip [地址]` | IP 定位到城市 |
| `call <path> k=v ...` | 通用兜底：调任意 v3/v5 接口（公交/骑行/静态图等） |

`call` 兜底示例：

```bash
python3 scripts/amap.py call /v5/direction/bicycling origin=116.48,39.98 destination=116.43,39.90
python3 scripts/amap.py call /v5/direction/transit/integrated origin=116.48,39.98 destination=116.43,39.90 city1=010 city2=010
```

## Agent 典型用法

1. **"帮我找 XX 附近的咖啡馆"**：先 `geocode` 定位 XX → `around` 搜周边
   → 按距离/评分整理成清单给用户
2. **通勤方案对比**：同一起终点分别跑 `driving`/`walking`/公交（call 兜底），
   对比耗时与距离给建议
3. **批量地址清洗**：一批不规范地址循环 `geocode`，拿规范化地址 + adcode
   + 坐标，用于数据入库
4. **出行前置检查**：`weather <目的地adcode> all` 看未来 4 天预报

## 中国坐标系必读（跨平台开发最大的坑）

- **WGS-84**：GPS 原始坐标。直接标在高德地图上会偏移约几百米
- **GCJ-02**（火星坐标）：国家测绘局加密标准，**高德、腾讯地图使用**
- **BD-09**：百度自有，GCJ-02 二次加密，仅百度使用
- 转换：高德提供官方接口 `/v3/assistant/coordinate/convert`
  （`coordsys=gps|baidu` → GCJ-02），跨平台迁移数据先转坐标再入库
- 症状自查：位置整体偏移几百米 ≈ 坐标系搞混；偏移几十米 ≈ 精度问题

## 高频错误码

| infocode | 含义 | 处理 |
|----------|------|------|
| 10001 | Key 无效 | 检查 Key 类型必须是"Web服务"（JS API 的 Key 调 REST 会报这个） |
| 10003 | 日配额超限 | 免费版各接口每日限额不同，次日重置；商用需认证/付费 |
| 10021 | 并发超限 | 加限速，免费版 QPS 很低（约 3/秒） |
| 30001 | 无查询结果 | 地址写法换个粒度重试（省市+街道） |

## 与其他地图平台对比选型

| 场景 | 建议 |
|------|------|
| 微信小程序 | 腾讯地图（微信官方推荐，见 `tencent-map` skill） |
| POI/检索数据要求高 | 高德或百度（见 `baidu-map` skill）实测对比 |
| 导航/驾车生态 | 高德（车机市占率最高） |
| 海外地图 | 三家境外数据都弱，选 Google Maps/Mapbox |

## 本 skill 不做什么

- 不提供爬取高德网页端数据的方法（用官方 API，免费额度对个人够用）
- 静态地图、轨迹纠偏、地理围栏等低频接口未封装命令，用 `call` 兜底，
  参数以官方文档 lbs.amap.com/api/webservice/summary 为准
