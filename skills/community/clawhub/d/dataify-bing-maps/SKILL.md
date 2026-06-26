---
name: dataify-bing-maps
description: When the user uses Bing Maps to search for locations or view maps, this skill is executed
---

# Bing Maps

## Overview

Use this skill to convert a natural-language Bing Maps request into Dataify Bing Maps API fields, call the fixed Dataify endpoint through `scripts/bing_maps.py`, and return the API response directly to the user without summarizing, parsing, or post-processing it.

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
5. Before every live API call, show the user a Markdown table containing the complete field list, excluding `Authorization`. The table must have only these columns: `参数名`, `当前值`, `默认值`, `说明`. The `说明` column must be Chinese. Ask whether the user wants to modify anything. Do not call the API until the user confirms.
6. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags only when overriding automatic parsing.
7. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - If the user provides a token during the task, pass it with `--token` or set `DATAIFY_API_TOKEN` for the command before invoking the script.
   - The script adds a `Bearer ` prefix when the token does not already include one.
   - If no token is available, the script exits with a Chinese prompt; ask the user to input a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).
8. Generate the confirmation table before a live call:

```bash
python3 scripts/bing_maps.py --prompt "JiangSu" --params-table
```

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

10. Run a live call only after token is available and the user confirms the parameter table. Add `--confirmed`; the script refuses live calls without it:

```bash
python3 scripts/bing_maps.py --prompt "JiangSu" --confirmed
```

11. Return the script output directly to the user. Do not summarize map results, extract fields, reformat JSON, parse embedded JSON strings, or process returned HTML unless the user separately asks for processing.

## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_maps.py \
  --prompt "搜索JiangSu，并返回 JSON 和 HTML" \
  --json 2
```

Useful flags:

- `--q`, `--json`, `--cp`, `--lat`, `--lon`, `--setlang`, `--place-id`, `--first`, `--count`, `--no-cache`
- `--field key=value` for any supported API field
- `--token` to provide a token for the current run
- `--body-format form|json`, default `form`
- `--params-table` to print the required pre-call Markdown parameter table and skip network/auth checks
- `--dry-run` to print the parsed payload and skip network/auth checks
- `--confirmed` to allow a live API call after the user confirms the parameter table

If a live call fails because `DATAIFY_API_TOKEN` is missing, ask the user to provide a token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).