---
name: dataify-bing-videos
description: Use when a user run a Bing video search
---

# Bing Videos

## Overview

Use this skill to turn a natural-language Bing video search request into Dataify Bing Videos API fields, show the full request-parameter table for confirmation, call the API through `scripts/bing_videos.py` only after the user confirms, and return the API response directly without summarizing, parsing, reformatting, or post-processing it.

The source API document is summarized in `references/api.md`. Read it when field behavior, allowed values, or response shape is unclear.

## Defaults

Use defaults only when they come from parameter descriptions, not from request examples.

- `engine`: default `bing_videos`.
- `json`: default `1`.
- `first`: default `1`.
- `no_cache`: default `false`.
- `q`: default `pizza` from the field description. Prefer the user's requested query whenever provided.
- `mkt`, `cc`, `setlang`, `length`, `date`, `resolution`, `source_site`, `price`: no default.

Treat source-document sample values such as `en-US`, `us`, `short`, `lt1440`, `360p`, `dailymotion.com`, `free`, or `no_cache=true` as examples only. `pizza` is used only because the `q` field description states it as the default.

## Workflow

1. Identify the user's video search query and map optional requirements to API fields:
   - `q`: search keywords. Default `pizza` when the user provides no query.
   - `json`: output format. Default `1`; use `2` for JSON plus HTML, `3` for HTML.
   - `mkt`: display language and market, such as `en-US` or `zh-CN`.
   - `cc`: two-letter country or region code, such as `us`, `cn`, `jp`, `uk`.
   - `setlang`: two-letter search language, such as `en`, `zh`, or `ja`.
   - `first`: organic result offset. Default `1`.
   - `length`: video duration filter: `short`, `medium`, or `long`.
   - `date`: freshness filter: `lt1440`, `lt10080`, `lt43200`, or `lt525600`.
   - `resolution`: resolution filter: `lowerthan_360p`, `360p`, `480p`, `720p`, or `1080p`.
   - `source_site`: source filter, such as `vimeo.com`, `dailymotion.com`, or `cnn.com`.
   - `price`: `free` or `paid`.
   - `no_cache`: cache behavior. Default `false`; use `true` only when requested.
2. Prefer explicit user-provided field values over inferred values. Never fill fields from API example YAML values.
3. Before every live API call, run a dry run with `--table`, show the resulting Markdown table to the user, and ask whether they want to modify parameters. The table must include the complete field list except `Authorization`, with only these columns: 参数名, 当前值, 默认值, 说明.

```bash
python3 scripts/bing_videos.py --prompt "pizza" --dry-run --table
```

4. If the user asks to modify parameters, apply their changes and show the full table again.
5. Call the live API only after the user confirms the displayed parameters.
6. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - If the user provides a token during the task, pass it with `--token` or set `DATAIFY_API_TOKEN` for the command before invoking the script.
   - The script adds a `Bearer ` prefix when the token does not already include one.
   - If no token is available, ask the user to input a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).
7. Return the live script output directly to the user. Do not summarize video results, extract fields, reformat JSON, parse embedded JSON strings, or process returned HTML unless the user separately asks for processing.

## Script Usage

Preview full parameters before confirmation:

```bash
python3 scripts/bing_videos.py \
  --prompt "用必应视频搜索 OpenAI 发布会，过去一周，免费，1080p，返回 JSON 和 HTML" \
  --dry-run \
  --table
```

Run the live call only after confirmation:

```bash
python3 scripts/bing_videos.py \
  --prompt "用必应视频搜索 OpenAI 发布会，过去一周，免费，1080p，返回 JSON 和 HTML"
```

Useful flags:

- `--q`, `--json`, `--mkt`, `--cc`, `--setlang`, `--first`, `--length`, `--date`, `--resolution`, `--source-site`, `--price`, `--no-cache`
- `--field key=value` for any supported API field
- `--token` to provide a token for the current run
- `--body-format form|json`, default `form`
- `--dry-run` to print parsed payload JSON and skip network/auth checks
- `--table` with `--dry-run` to print the full confirmation table

