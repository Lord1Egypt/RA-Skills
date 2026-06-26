---
name: flight-monitor
description: 机票查询与价格监控技能。支持单程/往返查询、价格阈值提醒、定时监控、手机推送通知（Bark/Server酱/PushDeer）。触发词示例：查一下北京到三亚的机票、帮我看看上海飞成都下周六往返票、监控杭州到西安3月26日机票低于500提醒我、查看所有机票监控任务。
---

# Flight Monitor Skill

查询国内外实时机票价格，设置低价提醒，支持定时监控。无需浏览器自动化，无需 API 密钥。

---

## Quick Start

### 单程查询

```
查一下北京到三亚 3 月 25 日的机票价格
Check flights from BJS to SYX on 2026-03-25
查询杭州到西安 3 月 26 日，低于 500 元的机票
```

### 往返查询

```
帮我看看上海飞成都，4 月 1 日去 4 月 5 日回
上海到成都下周六往返票
```

### 设置价格监控与推送

```
监控赣州到哈尔滨 4 月 10 日，每天查一次，低于 700 提醒我
Monitor BJS to SYX on 2026-03-25, daily, alert if under ¥1500
```

### 管理监控任务

```
查看我所有的机票监控任务
暂停北京到三亚的监控
删除杭州到西安的监控任务
```

### 配置手机推送

```
设置推送 Bark Key: xxxxx
```

---

## Core Workflow

### Step 1 — Parse User Intent

Extract these parameters from the user's message:

| Parameter | Required | Example |
|-----------|----------|---------|
| 出发城市 dep | Yes | 北京 / BJS |
| 到达城市 arr | Yes | 三亚 / SYX |
| 出发日期 date | Yes | 2026-04-10 |
| 返程日期 return_date | Round-trip only | 2026-04-15 |
| 最高价 max_price | No | 700 |
| 监控频率 freq | For monitoring | daily / 6h |

City name→code resolution is handled automatically by the scripts.
For cities not recognized, check `references/city_codes.md`.

### Step 2 — Query Flight Data

**⚠️ CRITICAL DATE RULE: Always use the user's exact travel date. NEVER substitute today's date.**

#### Step 2a — Run search_flights.py (always do this first)

```bash
python scripts/search_flights.py --from <dep> --to <arr> --date <YYYY-MM-DD>
python scripts/search_flights.py --from KOW --to HRB --date 2026-04-10 --max-price 700
python scripts/search_flights.py --from SHA --to CTU --date 2026-04-01 --return-date 2026-04-05
```

The script tries three data sources in order and returns one of:

| Result `source` | What it means | What you do next |
|----------------|---------------|------------------|
| `ctrip` | Full flight list fetched directly — **done** | Format the `flights` list into a table. **Skip all web searches.** |
| `zbape` | Lowest price summary only (no schedule) | Show the price summary + booking links. **Skip all web searches.** |
| `fallback` | APIs unavailable | Do **exactly ONE** `web_search` using the `search_query` field. Then stop. **Do NOT fetch any URLs.** |

#### Step 2b — Fallback web_search (only when source == "fallback")

Use the exact query string from `search_query` in the script output:

```
web_search("<value of search_query field>")
```

Parse snippets for: airline name, flight number, departure time, arrival time, price.
**Stop after this one search**, regardless of result quality. Use whatever data the snippets contain.

#### HARD RULES — no exceptions

- **NEVER call `web_fetch`** on any URL (携程/去哪儿/Skyscanner are all JS-rendered; fetching wastes time and returns nothing useful).
- **NEVER run more than 1 `web_search`** per query direction (outbound / return).
- **NEVER try multiple search engines** or reformulate the query if the first search returns partial data.
- If data is incomplete after one search, present what you have and note the limitation.

### Step 3 — Record Price History

After querying, always record the result for trend tracking:

```bash
python scripts/price_history.py append \
  --from KOW --to HRB --date 2026-04-10 \
  --price <lowest_price_found> --flight "<flight_number>" --threshold 700

# View history for a route
python scripts/price_history.py show --from KOW --to HRB --date 2026-04-10

# List all routes with history
python scripts/price_history.py list
```

History files: `~/.workbuddy/flight-monitor/{DEP}-{ARR}-{DATE}.json`

### Step 4 — Check Alert & Send Notification

After recording, check if the price is at or below threshold:

```bash
python scripts/price_history.py show --from KOW --to HRB --date 2026-04-10
```

If the output contains "低价提醒" (price ≤ threshold):

```bash
python scripts/notify.py \
  --title "机票低价提醒 KOW→HRB" \
  --body "赣州→哈尔滨 2026-04-10 最低价 ¥<price>，低于阈值¥700！推荐航班 <flight>" \
  --url "https://flights.ctrip.com/itinerary/oneway/kow-hrb?depdate=2026-04-10"
```

notify.py will automatically use whichever push service is configured.
If no push service is configured, it will print instructions to set one up.

### Step 5 — Set Up Monitoring (when user requests recurring checks)

```bash
# Add a daily monitor with price alert
python scripts/monitor_manager.py add \
  --from KOW --to HRB --date 2026-04-10 \
  --freq daily --threshold 700

# Every 6 hours
python scripts/monitor_manager.py add \
  --from HGH --to SIA --date 2026-03-26 --freq 6h

# List all monitors
python scripts/monitor_manager.py list

# Pause a monitor
python scripts/monitor_manager.py pause --id flight-KOW-HRB-2026-04-10

# Remove a monitor
python scripts/monitor_manager.py remove --id flight-KOW-HRB-2026-04-10

# Show details / manual trigger hint (does NOT execute any shell command)
python scripts/monitor_manager.py run --id flight-KOW-HRB-2026-04-10
```

Monitor tasks are saved as TOML files under `~/.workbuddy/automations/`.

**Security notes:**
- `monitor_manager.py` does **not** import `os` and contains **no** `os.system()` / `subprocess` calls.
- All `--id` arguments are validated against a strict whitelist regex (`flight-[A-Z]+-[A-Z]+-YYYY-MM-DD`) before any filesystem access, preventing path traversal attacks.
- The `run` subcommand only prints a safe hint — it never executes external commands.

---

## Push Notification Setup

Three free services are supported. Configure one:

### Option A — Bark (iOS only, recommended for iPhone users)

1. Install Bark app from App Store
2. Open the app → copy your device key
3. Configure: `python scripts/notify.py --setup bark --key <YOUR_KEY>`

### Option B — Server酱 (WeChat notification, Android & iOS)

1. Visit https://sct.ftqq.com/ and login with GitHub
2. Copy your SendKey
3. Configure: `python scripts/notify.py --setup serverchan --key <YOUR_SENDKEY>`

### Option C — PushDeer (open source, Android & iOS)

1. Install PushDeer app or use web version at https://www.pushdeer.com/
2. Create a device and copy the push key
3. Configure: `python scripts/notify.py --setup pushdeer --key <YOUR_KEY>`

Configuration is saved to `~/.workbuddy/flight-monitor/notify_config.json`.

---

## Frequency Options

| Input | Schedule | Label |
|-------|----------|-------|
| `hourly` / `1h` | Every 1 hour | 每1小时 |
| `2h` | Every 2 hours | 每2小时 |
| `3h` | Every 3 hours | 每3小时 |
| `6h` | Every 6 hours | 每6小时 |
| `12h` / `twice-daily` | Every 12 hours | 每12小时 |
| `daily` / `morning` | Daily at 09:00 CST | 每天9:00 |

**Recommended frequencies by lead time:**

| Lead Time | Recommended Freq |
|-----------|-----------------|
| 1 month+ | daily |
| 2 weeks | 12h |
| 1 week | 6h |
| 3 days | 3h |

---

## Output Format

### Query Result (shown to user)

Always present results in the following table format. For connecting flights, the
"中转" column must list the connection city and layover wait time (e.g. "转上海 1h20m").

```markdown
## 机票查询：赣州(KOW) → 哈尔滨(HRB)

**出行日期：** 2026-04-10（⚠️ 以下均为该日期价格）
**价格筛选：** ≤ ¥700

| 航班 | 价格(含税) | 出发 | 到达 | 全程时长 | 中转（城市 + 等待时间） |
|------|-----------|------|------|----------|------------------------|
| 祥鹏 8L9549 | ¥620 | 09:35 | 13:30 | 3h55m | 直飞 |
| 东航 MU2993+MU5619 | ¥650 | 20:10 | 00:35+1 | 7h25m | 转上海虹桥 1h50m |

最低价：¥620  [立即预订 →](https://flights.ctrip.com/itinerary/oneway/kow-hrb?depdate=2026-04-10)
```

**Column definitions:**
- `全程时长`: total elapsed time from departure to final arrival (including layover)
- `中转（城市 + 等待时间）`: for connecting flights, list connection city + layover wait duration; write "直飞" for non-stop

### Low-Price Alert (sent to phone)

```
🔔 机票低价提醒！

赣州(KOW) → 哈尔滨(HRB)  |  出行日期：2026-04-10
当前最低价：¥620（低于阈值 ¥700）
推荐航班：祥鹏 8L9549  09:35 → 13:30（直飞）

立即预订：https://flights.ctrip.com/...
```

---

## Notes

- **⚠️ Date discipline:** Always search for the user's exact travel date. The travel date is NOT today's date.
- **Query flow:** Always start with `search_flights.py`. Only fall back to `web_search` when the script returns `source: fallback`. Maximum 1 search per direction.
- **Never use web_fetch:** All major OTA sites (携程, 去哪儿, Skyscanner) are JavaScript-rendered. Fetching them returns empty or useless content and wastes tokens.
- **Data source priority:** Ctrip AJAX API (richest, no key) → zbape.com (key required, lowest-price only) → single web_search fallback.
- **zbape key (optional):** Run `python scripts/search_flights.py --setup-zbape <KEY>` once. Adds a useful lowest-price-per-date layer when the Ctrip API is rate-limited.
- **Push notifications:** Configure once, alerts fire automatically on every monitoring cycle when price drops below threshold.
- **City codes:** See `references/city_codes.md` for the full list.

---

## File Overview

```
flight-monitor/
├── SKILL.md                    ← This file
├── scripts/
│   ├── search_flights.py       ← PRIMARY: Multi-source flight query (Ctrip API → zbape → fallback)
│   ├── query_flights.py        ← Legacy: Search query generator + booking links
│   ├── price_history.py        ← Append/read/alert price history records
│   ├── monitor_manager.py      ← Add/pause/remove scheduled monitors
│   └── notify.py               ← Mobile push notifications (Bark/Server酱/PushDeer)
└── references/
    └── city_codes.md           ← Full city name → IATA code table
```

### Optional: zbape API key (adds lowest-price-per-date data when Ctrip API fails)

```bash
python scripts/search_flights.py --setup-zbape <YOUR_KEY>
# Get a free key at: https://api.zbape.com/doc/54
```
