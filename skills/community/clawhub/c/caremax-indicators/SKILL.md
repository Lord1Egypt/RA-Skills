---
name: caremax-indicators
description: "Query and track health indicators from CareMax Health API. Use when a user asks about health metrics, lab results, trends, or wants to quickly log everyday vitals (e.g. height, weight, blood pressure — whatever presets the API returns for their account). Trigger terms: health indicator, lab result, blood test, trend, quick log, daily vitals, 指标, 趋势, 血常规, 血糖, 胆固醇, 快捷记一笔, 快速记录, 记一笔, 身高, 体重, 血压, 心率, 体温, 腰围."
license: MIT
---

# CareMax Health Indicators

> **Requires `caremax-auth` as a sibling directory** (`../caremax-auth/`, same layout as `skills/caremax-auth` + `skills/caremax-indicators` in this repo, or under `~/.agents/skills/`). If missing: `npx skills add KittenYang/caremax-skills` and select caremax-auth.

## What end users can do (plain language)

- **Browse and analyze** their saved indicators: lists, categories, trends over time (labs and long-term metrics).
- **Quickly add a single reading** for common day-to-day metrics — the same idea as the app’s **「快捷记一笔」**: pick a familiar item (often things like **身高、体重、血压、心率、体温、腰围**等，**具体有哪些以当前账号下列出的可选项为准**), enter a value and date, and it is stored like a normal indicator data point. No upload or report file required.

Agents should **describe this in user-friendly terms** (“帮你记一笔今天的体重”“看看现在能快捷记录哪些项目”) and only use the API steps below to implement it after the user is authenticated.

This skill also covers the **agent/skill** indicator endpoints under `/api/skill/indicators/*` for listing, categories, and trends.

## Prerequisites — Auto-Auth (MANDATORY)

**Working directory:** this skill’s root folder (`caremax-indicators/`, sibling of `caremax-auth/`). Scripts in auth are reached with **`../caremax-auth/scripts/`**.

```bash
# shorthand — run from caremax-indicators/
APICALL="bash ../caremax-auth/scripts/api-call.sh"
LIST_PRESETS="bash ../caremax-auth/scripts/list-system-presets.sh"
QUICK_LOG="bash ../caremax-auth/scripts/quick-log.sh"
```

If any script returns `{"error":"no_credentials",...}` → **immediately run `bash ../caremax-auth/scripts/auth-flow.sh [base_url]`** in background. If the user specified a custom URL (e.g., `http://localhost:8788`), pass it as the argument. It opens the browser and auto-polls. Tell the user "please authorize in browser". Once it outputs `authorized`, retry.

## List All Indicators

```bash
$APICALL GET /api/skill/indicators
# with category filter:
$APICALL GET "/api/skill/indicators?category=血常规"
```

Response fields: `id` (UUID, needed for trend), `canonical_name`, `display_name`, `canonical_unit`, `category`, `latest_value`, `data_count`

## Get Indicator Categories

```bash
$APICALL GET /api/skill/indicators/categories
```

## Get Indicator Trend

**Important**: Get the indicator UUID from the list endpoint first.

```bash
$APICALL GET "/api/skill/indicators/trend?id={indicator_uuid}"
```

Returns time-series: `date`, `value`, `unit`, `reference_range`, `is_abnormal` (0/1)

## Quick log — same feature as 「快捷记一笔」 (authenticated user only)

**Prefer the dedicated scripts** (wrap `api-call.sh` with the same OAuth user token). Do not hand-roll `curl`.

**Typical user intents:** “记一下体重 70”“今天身高 175”“帮妈妈记血压 120/80” — always **run `list-system-presets.sh` first** so you use a valid `preset_key` and know default units; use `--member` when logging for a family profile.

### 1) List what the user can quick-log right now

```bash
$LIST_PRESETS
```

Response: `presets[]` — use `preset_key` for `quick-log.sh`; show `display_name` / `canonical_unit` when confirming with the user. **Do not assume** a fixed list of metrics in prose.

### 2) Save one value

```bash
$QUICK_LOG weight 72.5 --unit kg --date 2026-03-28
$QUICK_LOG height 175 --member <family_member_uuid>
```

- Positional: `preset_key`, `value` (required).
- Optional: `--unit`, `--date YYYY-MM-DD` (omit date → server default today), `--member` (family member UUID).

### Lower-level equivalent (only if you need custom JSON)

```bash
$APICALL GET /api/indicators/system-presets
$APICALL POST /api/indicators/quick-log '{"preset_key":"weight","value":"72.5","unit":"kg","test_date":"2026-03-28","member_id":"..."}'
```

### Recommended workflow (quick log)

```bash
# User: "帮我记身高" / "quick log my weight"
$LIST_PRESETS
# Match user wording to preset_key (or ask if ambiguous)
$QUICK_LOG <preset_key> <value> [--date ...] [--member ...]
# Confirm aloud: value, unit, date, whose profile
```

## Get Trends by Category

```bash
$APICALL GET "/api/skill/indicators/trends-by-category?category={category_name}"
```

## Recommended Workflow

When user asks "show my creatinine trend":

```bash
# 1. List all indicators, find the matching one
$APICALL GET /api/skill/indicators
# 2. Extract the id (UUID) of the matching indicator from the response
# 3. Get trend data
$APICALL GET "/api/skill/indicators/trend?id={uuid}"
# 4. Present with dates, values, units, highlight abnormals
```

When user asks "what are my abnormal indicators":

```bash
# 1. Get all indicators
$APICALL GET /api/skill/indicators
# 2. Filter response for those with abnormal latest values
# 3. Present with values and reference ranges
```

## Display Guidelines

- Always show values with units (e.g., "98 μmol/L" not just "98")
- Include reference ranges when available
- Flag abnormal values clearly
- For trends, show dates in chronological order
- Chinese indicator names are standard — display them as-is
