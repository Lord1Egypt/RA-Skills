---
name: dataify-bing-maps
description: "Search Bing Maps for places or map results. Do not use for Bing web search or Google Maps structured details."
---

# Bing Maps

## Overview


The source API document is summarized in `references/api.md`. Read it when field behavior or response shape is unclear.

## Workflow

1. Identify the user's map/place query and map optional requirements to API fields:
   - `q`: Bing Maps 搜索关键词。必填。
   - `json`: 输出格式。用户未指定输出格式时默认使用 `1`；`2` 表示 JSON+HTML，`3` 表示 HTML。
   - `cp`: 查询中心点 GPS 坐标，格式为 `纬度~经度`。仅当用户提供坐标时传入。
   - `setlang`: 两位语言/地区值，例如 `us`、`de`、`gb`。仅当用户要求语言/地区时传入。
   - `place_id`: Bing Maps 地点唯一引用。仅当用户提供地点 ID 时传入。
   - `first`: 本地结果偏移量。参数说明写明默认值为 `0`，因此用户未指定时使用 `0`。
   - `count`: 每页建议返回结果数量。最大值为 `30`，但最大值不是默认值。仅当用户要求结果数量时传入。
   - `no_cache`: `true` 表示跳过缓存，`false` 表示使用缓存。参数说明写明默认值为 `false`，因此用户未指定时使用 `false`。
2. Prefer explicit user-provided field values over inferred values.
3. Use defaults from the parameter descriptions when the user does not specify a value:
   - `engine`: `bing_maps`
   - `json`: `1`
   - `first`: `0`
   - `no_cache`: `false`
   - No defaults for `q`, `cp`, `setlang`, `place_id`, or `count`.
4. Never treat documentation examples as defaults. Do not add sample values such as coordinates, `setlang=us`, or `count=30` unless the user explicitly requested that field.
6. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags only when overriding automatic parsing.
7. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - The script adds a `Bearer ` prefix when the token does not already include one.
9. Run a dry run when you need machine-readable parsing output without calling the API:

```bash
python3 scripts/bing_maps.py --prompt "JiangSu" --dry-run
```

Expected dry-run payload:

```json
{
  "engine": "bing_maps",
  "q": "JiangSu",
  "json": "1",
  "first": "0",
  "no_cache": "false"
}
```


```bash
```


## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_maps.py \
  --prompt "搜索JiangSu，并返回 JSON 和 HTML" \
  --json 2
bash
python3 scripts/bing_maps.py --prompt "JiangSu" --dry-run
```

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/bing_maps.py --prompt "JiangSu" --dry-run
```

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
