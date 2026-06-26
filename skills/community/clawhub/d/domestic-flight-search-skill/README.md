# Domestic Flight Search

An OpenClaw skill for querying China domestic flights with schedules, airport details, duration, and reference fares.

## 中文介绍

一个面向 OpenClaw 的国内航班查询技能，用于查询中国国内航班的班次、起降机场、起降时间、飞行时长和参考票价。

### 功能特点

- 查询指定日期的中国国内航班
- 支持中文城市名、机场名和 IATA 三字码输入
- 返回航司、航班号、起降机场、起降时间、时长和参考票价
- 默认按参考票价排序
- 支持直接命令行查询，也支持可选的本地 HTTP 模式

### 使用前提

- 需要 `python3`
- 需要用户自己申请 Juhe 航班(https://www.juhe.cn/) API key
- 需要网络访问 Juhe 航班接口

本技能不自带 API key。每位用户都需要自行申请并配置：

```bash
export JUHE_FLIGHT_API_KEY='your_juhe_api_key'
```

接口文档：

- `https://www.juhe.cn/docs/api/id/818`

### 示例提问

- `帮我查 2026-03-20 北京到上海最便宜的航班`
- `查一下明天广州到成都的航班和价格`
- `帮我看首都机场到深圳宝安当天有哪些航班`
- `上海虹桥到重庆，按价格从低到高列 5 个`

### 限制说明

- 仅支持中国国内航班
- 票价为参考票价，不保证等于最终出票价
- 数据时效性和准确性依赖 Juhe
- 往返行程需要拆成两次单程查询

## What It Does

- Query China domestic flights for a specific date
- Accept Chinese city names, airport names, or IATA codes
- Return airline, flight number, departure and arrival airports, times, duration, and reference fare
- Sort results by reference fare
- Support direct CLI usage and optional local HTTP mode

## Requirements

- `python3`
- A Juhe flight API key
- Network access to the Juhe flight API

This skill does not include an API key. Each user must apply for their own Juhe key and configure:

```bash
export JUHE_FLIGHT_API_KEY='your_juhe_api_key'
```

Provider docs:

- `https://www.juhe.cn/docs/api/id/818`

## Skill Files

- `SKILL.md`: skill instructions and trigger metadata
- `agents/openai.yaml`: UI-facing skill metadata
- `scripts/domestic_flight_service.py`: main query script
- `references/provider-juhe.md`: provider notes
- `assets/data/*.json`: city and airport alias mappings

## Example Usage

```bash
python3 ./scripts/domestic_flight_service.py search \
  --from 北京 --to 上海 --date 2026-03-20 --pretty
```

Optional HTTP mode:

```bash
python3 ./scripts/domestic_flight_service.py serve --port 8765
```

Then:

```bash
curl 'http://127.0.0.1:8765/search?from=北京&to=上海&date=2026-03-20'
```

## Example Prompts

- `帮我查 2026-03-20 北京到上海最便宜的航班`
- `查一下明天广州到成都的航班和价格`
- `帮我看首都机场到深圳宝安当天有哪些航班`
- `上海虹桥到重庆，按价格从低到高列 5 个`

## Limitations

- China domestic flights only
- Fares are reference fares, not guaranteed ticketing prices
- Data freshness and accuracy depend on Juhe
- Round trips should be queried as two one-way searches

## Publishing

This repository is structured so it can be used directly as a GitHub-backed skill source.
