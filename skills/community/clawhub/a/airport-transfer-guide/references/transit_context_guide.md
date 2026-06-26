# Transit Context 取数脚本使用指南

## 概述

本脚本为 `airport-transfer-guide` skill 提供机场图片和拥挤度数据。通过三层取数架构，从第三方聚合站、重点机场官网和 CDP 截图降级获取实时信息，帮助用户了解机场转机环境。

## 运行方式

```bash
python3 {baseDir}/scripts/fetch_transit_context.py \
  --airport [airport_code] \
  --inbound-terminal [terminal] \
  --outbound-terminal [terminal] \
  --transit-datetime "[ISO datetime]" \
  --mode [normal|delay] \
  --output transit_context.json
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| --airport | 是 | 无 | 机场三字码（如 NRT、HKG） |
| --inbound-terminal | 是 | 无 | 到达航班的航站楼 |
| --outbound-terminal | 是 | 无 | 出发航班的航站楼 |
| --transit-datetime | 是 | 无 | 转机时间的 ISO 8601 格式（需用引号包裹） |
| --mode | 否 | normal | 模式选择：normal（正常）或 delay（延误） |
| --output | 否 | transit_context.json | 输出 JSON 文件路径 |

## JSON 输出字段说明

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| airport_code | string | 机场三字码 |
| airport_name | string | 机场中文名 |
| fetched_at | string | 数据抓取时间（ISO 8601 + 时区） |
| images | array | 图片列表 |
| crowd | object | 拥挤度数据 |
| baggage_note | string | 机场层面的行李重托运备注 |
| support | object | 当前机场的数据支持能力 |

### images 数组元素

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 图片标题（中文） |
| image_url | string/null | 可直接嵌入的图片 URL |
| source_url | string | 图片来源页面 URL |
| source_type | string | third_party_aggregator / official / wikimedia |
| inline_available | boolean | 是否可直接嵌入 Markdown |
| cdp_screenshot_path | string/null | CDP 截图本地路径（可选） |
| why_it_matters | string | 这张图对转机的帮助说明（中文） |

### crowd 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | available / proxy / unavailable |
| level | string/null | low / medium / high / null |
| wait_minutes | number/null | 预估等待分钟数 |
| signal_type | string | flightqueue / official_wait_time / flight_board_proxy / none |
| summary | string | 中文摘要 |
| source_url | string | 数据来源 URL |
| details | object | 各环节详情 |

### crowd.details 各环节

| 环节 | 说明 |
|------|------|
| security | 安检等待 |
| immigration | 入境审查等待 |
| baggage_claim | 行李提取等待 |

每个环节包含以下字段：
- `level`: string/null - 拥挤级别
- `wait_minutes`: number/null - 预估等待分钟数
- `source`: string - 数据来源说明

### support 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| images | boolean | 是否成功获取到图片 |
| crowd | string | flightqueue / official / proxy / none |
| cdp_available | boolean | 是否有 CDP 截图能力 |

## 三层取数架构

### Layer 1: 第三方聚合站（全球覆盖）

- **图片**: airportguide.com → 375+ 机场 terminal map
- **拥挤度**: flightqueue.com → 8000+ 机场等待时间预估
- 无需登录，无需 API key

### Layer 2: 重点机场官网（数据更权威）

- 在 `airport_registry.json` 中注册的机场
- 优先使用官方数据源
- 当前注册: NRT, HND, HKG, DXB, SIN, ICN, BKK, DOH, IST, KUL

### Layer 3: CDP 截图降级（JS 动态页面）

- 需要本机有 Chrome/Chromium
- 对 JS 动态渲染的页面进行截图
- 无 Chrome 时自动跳过

## 机场支持能力矩阵

| 机场 | 图片来源 | 拥挤度来源 | CDP 截图 | 行李备注 |
|------|---------|-----------|---------|----------|
| NRT | 聚合站+官方 | 官方+FlightQueue | 支持 | 有 |
| HKG | 聚合站+官方 | FlightQueue | 支持 | 有 |
| DXB | 聚合站+官方 | FlightQueue | 支持 | 有 |
| SIN | 聚合站+官方 | FlightQueue | 支持 | 有 |
| ICN | 聚合站+官方 | FlightQueue | 支持 | 有 |
| 其他 | 聚合站 | FlightQueue | 视环境 | 通用 |

## 降级策略

| 环境 | 图片 | 拥挤度 | CDP |
|------|------|--------|-----|
| 有网+有Chrome | 聚合站图片+CDP截图 | FlightQueue+官方 | 可用 |
| 有网+无Chrome | 聚合站图片 | FlightQueue+官方 | 跳过 |
| 无网 | 无 | 无 | 不可用 |
| 所有无数据 | 输出页面链接 | "暂无公开实时数据" | — |

## 扩展新机场

只需在 `airport_registry.json` 中添加新条目即可。非注册机场自动通过聚合站覆盖。

添加步骤：
1. 在 `airport_registry.json` 中添加机场三字码为 key 的对象
2. 填写 `name`, `name_en`, `official_map` 等字段
3. 设置 `crowd_support` 和 `baggage_note`
4. 可选：添加 `cdp_targets` 指定需要截图的页面

## CDP 截图环境要求

- **macOS**: 需要安装 Google Chrome（默认路径 `/Applications/Google Chrome.app/`）
- **Linux**: 需要安装 `google-chrome` 或 `chromium-browser`
- 无 Chrome 时脚本正常运行，仅跳过 CDP 截图功能
