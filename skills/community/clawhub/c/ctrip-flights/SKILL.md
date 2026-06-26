---
name: ctrip-flight
description: "This skill should be used when the user wants to search for domestic flight tickets in China, query flight prices, find the cheapest flights, compare airline prices, or get low-price calendars. Trigger phrases include 查机票, 航班查询, 机票价格, 最低价, flights, cheap flights, 北京到上海机票, or any mention of Chinese city pairs with travel dates."
---

# Ctrip Domestic Flight Search

Search domestic flight tickets via Ctrip's API. Provides real-time flight information including prices, airlines, schedules, aircraft types, and low-price calendars.

## Prerequisites

Install the required Python package before first use:

```bash
pip install quickjs
```

The skill also requires the `_extract/c-sign.js` file bundled in the `scripts/` directory.

## Usage

Run the search script located at `scripts/ctrip_flight.py`. Both departure and arrival support city names, IATA codes, or **province names**. When a province is specified, all airports in that province are queried and compared automatically.

```bash
python3 scripts/ctrip_flight.py 北京 上海 2026-04-02 --md
python3 scripts/ctrip_flight.py 北京 广东 2026-04-02 --md
python3 scripts/ctrip_flight.py 浙江 云南 2026-04-05 --json
```

**Parameters:**
- Arg 1: departure — city name, IATA code, or **province name**
- Arg 2: arrival — city name, IATA code, or **province name**
- Arg 3: departure date in `YYYY-MM-DD` format
- Arg 4 (optional): cabin — `Y` = Economy (default), `C` = Business, `F` = First
- `--json` or `-j`: output structured JSON
- `--md` or `-m`: output Markdown tables (default)

When a province is given (e.g. "广东"), the script queries all airport cities in that province (广州, 深圳, 珠海), compares prices across routes, and recommends the cheapest option.

**Examples:**
```bash
python3 scripts/ctrip_flight.py 北京 上海 2026-04-02
python3 scripts/ctrip_flight.py 广州 成都 2026-04-05 C
```

## Programmatic Usage

```python
import sys
sys.path.insert(0, "path/to/ctrip-flight/scripts")
from ctrip_flight import search_to_region, to_json, to_markdown

# Single city or province query — province auto-expands to all airports
result = search_to_region("北京", "广东", "2026-04-02")

# result contains:
#   query.isMultiRoute  — True if province was used
#   routeSummaries      — per-route lowest price comparison
#   bestRoute           — the cheapest route overall
#   allFlights          — combined flight list from all routes

md = to_markdown(result)
js = to_json(result)
```

## Supported Locations

**Cities:** 北京, 上海, 广州, 深圳, 珠海, 成都, 杭州, 温州, 宁波, 武汉, 西安, 重庆, 南京, 天津, 长沙, 三亚, 海口, 昆明, 丽江, 西双版纳, 厦门, 福州, 大连, 沈阳, 青岛, 济南, 哈尔滨, 长春, 郑州, 贵阳, 太原, 兰州, 乌鲁木齐, 南宁, 桂林, 合肥, 南昌

**Provinces (auto-expand to all airport cities):** 广东(广州/深圳/珠海), 浙江(杭州/温州/宁波), 福建(厦门/福州), 山东(青岛/济南), 辽宁(大连/沈阳), 海南(三亚/海口), 云南(昆明/丽江/西双版纳), 广西(南宁/桂林), 黑龙江, 吉林, 河南, 湖北, 湖南, 江苏, 江西, 安徽, 陕西, 四川, 贵州, 山西, 甘肃, 新疆

## Output

Two output formats are supported:

**Markdown (`--md`, default):** Renders flight data as Markdown with tables and summary. Ideal for LLM responses and chat display.

**JSON (`--json`):** Structured JSON with `query`, `summary`, `directFlights`, `transferFlights`, and `lowPriceCalendar` fields. Ideal for downstream processing.

## How It Works

The skill reverse-engineered Ctrip's anti-crawl protections:
- `sign` header: `MD5(transactionID + cityCode + cityCode + date)`
- `w-payload-source` header: Ctrip's c-sign.js executed via QuickJS engine
- `FVP` cookie: Extracted from server-rendered HTML page
- `token` header: Not required (discovered via testing)
