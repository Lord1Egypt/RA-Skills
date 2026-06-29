---
name: fishing-trip-planner
description: AI钓鱼行程规划助手。输入出发地、目的地、钓鱼时间和出行方式，自动调用高德地图API(路线规划)和和风天气API(天气+潮汐)，生成完整钓鱼行程规划报告(HTML)。支持配置管理(--setup)和历史记录(--history/--view)。触发词：钓鱼行程、钓鱼规划、钓鱼攻略、出海钓鱼、钓鱼行程报告、fishing trip planner。
agent_created: true
---

# Fishing Trip Planner - 钓鱼行程规划 v2.0

## Overview

基于高德地图路线规划API与和风天气(天气+潮汐)API，自动生成专业钓鱼行程规划报告。用户只需提供出发地、目的地、钓鱼时间和出行方式，系统自动整合路线、天气、潮汐数据，输出HTML可视化报告。

**v2.0 新增**:
- `--setup` 交互式配置向导，无需手动设置环境变量
- `--history` / `--view` 行程历史记录管理系统
- API Key 持久化存储 `~/.fishing-planner/config.json`
- 每次规划自动存档，支持回顾对比

## When to Use

- 用户询问钓鱼出行规划、钓鱼行程安排
- 用户想了解某海域/钓点的路线、天气、潮汐情况
- 用户问"我之前去过XX钓点"需要查看历史记录
- 触发词：钓鱼行程、钓鱼规划、出海钓鱼、钓鱼攻略、潮汐查询、钓鱼天气

## Workflow

### Step 0: 首次配置 (仅一次)

引导用户运行配置向导：

```bash
python scripts/fishing_planner.py --setup
```

交互式输入：
1. 高德地图 API Key → 申请: https://lbs.amap.com/
2. 和风天气 API Key → 申请: https://dev.qweather.com/
3. 默认潮汐站点ID → 可选，海钓必填，格式如 P2951
4. 用户名 → 可选

配置持久化保存到 `~/.fishing-planner/config.json` (权限 600)。
向导会自动验证 Key 有效性。

**如果用户不想运行向导**: 也可通过环境变量 `AMAP_KEY`、`QWEATHER_KEY`、`TIDE_STATION` 设置。

### Step 1: 收集用户输入

确认以下必填信息：
- **出发地** (origin): 城市名或具体地址，如"深圳南山"
- **目的地** (destination): 钓点/海域，如"惠州巽寮湾"
- **钓鱼时间** (date): 日期，如"2026-06-15"或"明天"
- **出行方式** (mode): driving/walking/transit/bicycling (默认 driving)

### Step 2: 运行规划脚本

```bash
python scripts/fishing_planner.py \
  -o "深圳南山" \
  -d "惠州巽寮湾" \
  -t "2026-06-15" \
  -m driving
```

脚本自动完成：
1. 地理编码 (地名→坐标) → 高德地图
2. 路线规划 (距离、时间、步骤) → 高德地图
3. 7天预报 + 逐小时预报 → 和风天气
4. 潮汐查询 (满潮/干潮时间、潮高) → 和风天气
5. 综合钓鱼评分 (0-100) → 本地算法
6. 生成HTML报告并自动存档 → `~/.fishing-planner/trips/`

### Step 3: 展示报告

脚本输出HTML报告路径，使用 `preview_url` 展示。

报告包含：
- **综合评分盘**: 0-100分 + 四级评级 (优秀/良好/一般/不佳)
- **路线总览**: 距离、预计时间、过路费、路线步骤
- **天气预报**: 7天天气卡片矩阵 + 钓鱼日逐小时天气表
- **潮汐预报**: 满潮/干潮时间表
- **条件评估**: 风力/温度/降水/潮汐 四维评级表
- **钓鱼建议**: 智能建议 + 装备清单 + 安全提醒

### Step 4: 查看历史记录

```bash
python scripts/fishing_planner.py --history    # 列表
python scripts/fishing_planner.py --view 1     # 按序号打开
python scripts/fishing_planner.py --view 20260615  # 按ID打开
```

## 数据存储结构

```
~/.fishing-planner/
├── config.json              # API Key配置 (权限 600)
├── trips_index.json         # 行程元数据索引
└── trips/
    ├── 20260615_083000.html # 行程HTML报告
    ├── 20260612_143000.html
    └── ...
```

## API 能力覆盖

| 数据源 | API | 用途 |
|--------|-----|------|
| 高德地图 | 地理编码 `/v3/geocode/geo` | 地名→坐标 |
| 高德地图 | 驾车规划 `/v3/direction/driving` | 路线规划 |
| 高德地图 | 步行规划 `/v3/direction/walking` | 路线规划 |
| 高德地图 | 公交规划 `/v3/direction/transit/integrated` | 路线规划 |
| 和风天气 | 7天预报 `/v7/weather/7d` | 天气预报 |
| 和风天气 | 逐小时预报 `/v7/weather/24h` | 精细天气 |
| 和风天气 | 潮汐 `/v7/ocean/tide` | 潮汐数据 |
| 和风天气 | 钓鱼指数 `/v7/indices/1d` | 专业评分 |

## 命令行参考

```
python fishing_planner.py --setup          # 配置向导
python fishing_planner.py --history        # 查看历史
python fishing_planner.py --view <ID>      # 查看历史报告
python fishing_planner.py -o <出发> -d <目的> -t <日期> [-m <方式>] [-O <输出路径>]
```

## Resources

### scripts/fishing_planner.py
核心规划脚本 v2.0。包含配置管理、API调用、评分算法、HTML生成、历史存档全部功能。

### references/api_guide.md
API密钥申请步骤、接口详细文档、常见问题。
