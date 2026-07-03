---
name: fishing-hotspot-push
description: "钓鱼热点智能推送。自动聚合钓鱼社区、搜索引擎、天气API数据，结合用户位置与和风天气钓鱼指数，推送周边最佳钓点及实时鱼情。支持配置管理、NLP信息提取、HTML可视化报告、历史记录。触发词：钓鱼热点、今日鱼情、附近钓点、哪里出鱼、钓鱼推送、钓鱼情报、fishing hotspot。"
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
      env:
        - AMAP_KEY
        - QWEATHER_KEY
    emoji: "🎣"
    homepage: https://github.com/bettermen/fishing-hotspot-push
---

# Fishing Hotspot Push - 钓鱼热点推送 v1.0

## Overview

主动发现式钓鱼助手。不需要用户指定目的地——系统自动从多渠道聚合钓鱼情报，结合用户位置、天气条件、钓鱼指数，推送"哪里正在出鱼"。与 `fishing-trip-planner` 形成互补：热点推送告诉你「去哪钓」，行程规划帮你「怎么去」。

**核心能力**:
- 🌐 多源数据聚合: 搜索引擎 + 钓鱼社区 + 和风天气 + 高德POI
- 🧠 NLP信息提取: 从非结构化文本中提取钓点、鱼种、鱼获
- 📊 智能排序: 距离 × 鱼获质量 × 天气 × 时效性
- 📱 可视化报告: 交互式HTML，支持一键跳转行程规划
- 📋 历史归档: 每次推送自动存档，可回溯对比

## When to Use

触发词: 钓鱼热点、今日鱼情、附近钓点、哪里出鱼、钓鱼推送、钓鱼情报、fishing hotspot、查鱼情、最新钓况

## Workflow

### Step 0: 首次配置（仅一次）

```bash
python scripts/hotspot_push.py --setup
```

交互式输入:
1. 高德地图 API Key（与 fishing-trip-planner 共用）
2. 和风天气 API Key（与 fishing-trip-planner 共用）
3. 默认城市/位置
4. 搜索半径（默认 50km）
5. 偏好鱼种（淡水/海水/不限）

配置存储于 `~/.fishing-hotspot/config.json`。

**快捷方式**: 如果已配置过 fishing-trip-planner，本技能自动读取其 API Key。

### Step 1: 数据采集（Agent 辅助）

Agent 使用 WebSearch 工具搜索目标城市的钓鱼情报：

```
搜索关键词模板:
- "{城市} 钓鱼 出鱼 钓点 {日期}"
- "{城市} 野钓 爆护 鱼获"
- "{城市} 钓鱼 最新 钓况"
```

同时调用和风天气钓鱼指数 API、高德周边水域 POI 搜索。

### Step 2: 运行热点分析

**方式A — Agent 搜索 + 脚本分析（推荐）**:
Agent 先执行 WebSearch，将搜索结果文本通过 `--input` 传入脚本：
```bash
python scripts/hotspot_push.py --run --input "搜索结果的原始文本..."
```

**方式B — 脚本独立运行**:
```bash
python scripts/hotspot_push.py --run
```
仅使用 API 数据（天气+POI），不含社交媒体情报。

**方式C — 指定城市**:
```bash
python scripts/hotspot_push.py --run --city "深圳"
```

脚本自动完成:
1. 城市坐标定位 → 高德地图
2. 周边水域/钓场 POI 搜索 → 高德地图
3. 钓鱼指数 + 天气预报 → 和风天气
4. 文本情报 NLP 提取（如有 --input）
5. 综合排序评分
6. 生成 HTML 报告并自动存档

### Step 3: 展示报告

脚本输出 HTML 报告路径，使用 `preview_url` 展示。

### Step 4: 查看历史

```bash
python scripts/hotspot_push.py --history    # 列表
python scripts/hotspot_push.py --view 1     # 按序号打开
```

## 与 fishing-trip-planner 联动

热点推送报告中每个钓点都带有「🗺️ 生成行程」链接。Agent 看到用户点击后，自动调用 fishing-trip-planner 的规划流程。

## 数据存储结构

```
~/.fishing-hotspot/
├── config.json              # 配置（权限 600）
├── push_index.json          # 推送历史索引
└── reports/
    ├── 20260613_083000.html # HTML报告
    └── ...
```

## 命令行参考

```
python hotspot_push.py --setup              # 配置向导
python hotspot_push.py --run                # 执行热点分析（仅API数据）
python hotspot_push.py --run --city "深圳"   # 指定城市
python hotspot_push.py --run --input "..."   # 传入外部文本情报
python hotspot_push.py --history             # 查看历史
python hotspot_push.py --view <ID>           # 查看历史报告
```

## Resources

### scripts/hotspot_push.py
核心脚本。包含配置管理、API调用、NLP提取、排序算法、HTML生成、历史存档。

### references/api_guide.md
API 密钥获取指南（与 fishing-trip-planner 共用路径）。
