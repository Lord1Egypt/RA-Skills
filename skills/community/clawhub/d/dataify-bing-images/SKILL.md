---
name: dataify-bing-images
description: When users want to use Bing for image search, they can use this skill
---

# Bing Images

## Overview

Use this skill to turn a natural-language Bing image search request into Dataify Bing Images API fields, preview the complete request parameters, ask the user whether to modify them, call the API through `scripts/bing_images.py` only after confirmation, and return the API response directly without summarizing, parsing, reformatting, or post-processing it.

The source API document is summarized in `references/api.md`. Read it when field behavior, allowed values, defaults, or response shape is unclear.

## Default Rules

Use parameter defaults only when the field's description states a default value. Do not use example values from the API document as defaults.

Default values used by this skill:

- `engine`: `bing_images`.
- `json`: `1`.
- `first`: `1`.
- `no_cache`: `false`.

All other fields have no default and stay blank unless the user provides them or the prompt parser confidently infers them.

## Workflow

1. Identify the user's image search query and map optional requirements to API fields:
   - `q`: 搜索关键词，必填；可以是任意语言。
   - `json`: 采集结果输出格式；默认 `1` 返回 JSON，`2` 返回 JSON 和 HTML，`3` 返回 HTML。
   - `mkt`: 搜索结果界面显示语言，格式为 `<语言代码>-<国家/地区代码>`，例如 `en-US`。
   - `cc`: 按国家或地区用户习惯展示搜索结果，使用两个字母的国家/地区代码，例如 `us`、`cn`、`jp`、`uk`。
   - `first`: 控制自然结果偏移量，默认值为 `1`。
   - `count`: 控制每页结果数量；该值为建议值，可能无法完全反映实际返回数量。
   - `imagesize`: 按图片尺寸过滤：`small` 小、`medium` 中、`large` 大、`wallpaper` 超大/壁纸。
   - `color2`: 按图片颜色过滤，例如 `color` 彩色、`bw` 黑白、`FGcls_RED` 红色、`FGcls_BLUE` 蓝色。
   - `photo`: 按图片类型过滤：`photo` 照片、`clipart` 剪贴画、`linedrawing` 线条画、`animatedgif` 动图、`animatedgifhttps` HTTPS 动图、`transparent` 透明、`shopping` 购物。
   - `aspect`: 按图片布局过滤：`square` 方形、`wide` 宽图、`tall` 高图。
   - `face`: 按人物类型过滤：`face` 仅面部、`portrait` 头肩肖像。
   - `age`: 按日期过滤：`lt1440` 过去 24 小时、`lt10080` 过去一周、`lt43200` 过去一个月、`lt525600` 过去一年。
   - `license`: 按使用许可过滤，例如 `Type-Any` 所有 Creative Commons、`L1` Public Domain、`L2_L3` 免费修改共享和商业使用。
   - `no_cache`: 是否跳过缓存；默认 `false` 使用缓存，`true` 跳过缓存。
2. Prefer explicit user-provided field values over inferred values. Never use API examples such as `pizza`, `count=10`, or sample filters as defaults.
3. Before every live call, preview the complete request parameter table. Do not show `Authorization`.

```bash
python3 scripts/bing_images.py --prompt "pizza" --preview
```

4. Show the table to the user and ask whether they want to modify any parameter. The table must include the complete field list and exactly these columns: parameter name, current value, default value, description.
5. If the user requests changes, rerun the preview with explicit flags or `--field key=value`, show the updated table, and ask again.
6. Call the API only after the user confirms the table. Use `--confirmed` for the live call:

```bash
python3 scripts/bing_images.py --prompt "pizza" --confirmed
```

7. Ensure authentication before the live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - If the user provides a token during the task, pass it with `--token` or set `DATAIFY_API_TOKEN` for the command before invoking the script.
   - The script adds a `Bearer ` prefix when the token does not already include one.
   - If no token is available, ask the user to input a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).
8. Return the script output directly to the user. Do not summarize image results, extract fields, reformat JSON, parse embedded JSON strings, or process returned HTML unless the user separately asks for processing.

## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_images.py \
  --prompt "用必应图片搜索 OpenAI 标志，正方形透明图片，过去一周，返回 JSON 和 HTML" \
  --no-cache true \
  --preview
```

Useful flags:

- `--q`, `--json`, `--mkt`, `--cc`, `--first`, `--count`, `--imagesize`, `--color2`, `--photo`, `--aspect`, `--face`, `--age`, `--license`, `--no-cache`
- `--field key=value` for any supported API field
- `--preview` to print the complete request-parameter table and skip network/auth checks
- `--confirmed` to allow a live API call after user confirmation
- `--token` to provide a token for the current run
- `--body-format form|json`, default `form`
- `--dry-run` to print the parsed payload and skip network/auth checks

If a live call fails because `DATAIFY_API_TOKEN` is missing, ask the user to provide a token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill). 