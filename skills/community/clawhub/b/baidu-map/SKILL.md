---
name: "百度地图"
version: "2.0.0"
description: "百度地图 Web 服务 API 工具与 BD-09 坐标系指南。Use for: (1) 用附带的零依赖 CLI 查地理编码/POI/路线并做坐标系转换, (2) BD-09 与 WGS-84/GCJ-02 互转避坑, (3) 百度地图开放平台开发指导。Baidu Maps Web API CLI (zero-dependency) for geocoding, POI, routing and coordinate conversion, plus a BD-09 coordinate-system guide."
tags: ["baidu", "map", "lbs", "geocoding", "bd09", "cli"]
author: "ClawSkills Team"
category: "navigation"
---

# 百度地图 Web API Skill

附带零依赖 CLI（`scripts/bmap.py`，仅 Python 标准库）。百度地图的
独有能力：**官方坐标转换接口**（WGS-84/GCJ-02 → BD-09）和丰富的
POI 检索数据。

## 快速开始

```bash
# lbsyun.baidu.com 免费申请 AK，应用类型选 "服务端"
export BMAP_AK=你的ak

python3 scripts/bmap.py geocode "北京市海淀区上地十街10号"
python3 scripts/bmap.py around 39.915,116.404 咖啡 1000
python3 scripts/bmap.py convert 116.404,39.915 1 5   # GPS坐标转百度坐标
```

脚本行为声明：仅请求 `api.map.baidu.com`，不读写本地文件。

## 命令手册

| 命令 | 作用 |
|------|------|
| `geocode <地址> [城市]` | 地址 → 坐标（**返回 BD-09**） |
| `regeo <lat,lng>` | 坐标 → 结构化地址 |
| `search <关键词> <城市>` | POI 城市内检索 |
| `around <lat,lng> <关键词> [半径米]` | POI 周边检索 |
| `driving / walking <起点> <终点>` | 轻量路线规划（directionlite） |
| `convert <lng,lat> <from> <to>` | 坐标转换：1=WGS84 3=GCJ-02 5=BD-09 |
| `call <path> k=v ...` | 通用兜底：调任意接口 |

**⚠️ 两个坐标陷阱（跨平台翻车重灾区）**：

1. **顺序**：百度接口的 location 参数是 `纬度,经度`（lat,lng），
   但 convert 接口的 coords 是 `经度,纬度`（lng,lat）——同平台内都不统一
2. **坐标系**：百度全系输入输出默认 BD-09。把高德/腾讯的 GCJ-02 坐标
   直接传入会偏移几百米；把 GPS 原始坐标传入偏移更大。
   进百度先 `convert`，出百度无官方反向接口（社区近似算法有精度损失，
   所以**数据库存坐标建议存 GCJ-02 或 WGS-84，展示层再转 BD-09**）

## Agent 典型用法

1. **坐标系清洗**：一批 GPS 轨迹要在百度地图展示 → 循环 `convert 1 5`
2. **位置偏移排障**：用户反馈"标注偏了几百米" → 十有八九是坐标系混用，
   按上面陷阱清单排查
3. **找地点/周边分析**：`search`/`around` 拿 POI 数据，按距离评分整理
4. **批量地址入库**：`geocode` 规范化地址，注意存储坐标系的选择（见上）

## 高频错误码（实测）

| status | 含义 | 处理 |
|--------|------|------|
| 200 | AK 不存在 | 检查 AK 拼写（实测拼错返回的就是它，不是 210） |
| 210 | AK 校验失败 | 服务端 AK 配置了 IP 白名单但请求 IP 不在其中 |
| 302 | 天配额超限 | 免费版按接口独立计额，次日重置；量大需企业认证 |
| 401/402 | 并发超限 | 加限速重试 |

## 与其他平台对比

| 场景 | 建议 |
|------|------|
| 微信小程序 | 腾讯地图（见 `tencent-map` skill） |
| 导航/车机生态 | 高德（见 `gaode` skill） |
| 需要街景全景 | 百度（独有全景 API，用 `call` 调 /panorama/v2） |
| POI 数据对比 | 高德/百度各有覆盖强区，重要项目两家实测对比 |

## 本 skill 不做什么

- 不含 JavaScript API（前端渲染）细节，只覆盖服务端 Web API
- BD-09 → 其他坐标系的"逆转换"官方不支持，本 skill 不提供
  近似算法实现（有精度损失，需要时明确告知用户风险）
