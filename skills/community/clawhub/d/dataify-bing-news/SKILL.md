---
name: dataify-bing-news
description: Use when a user to run a Bing news search
---

# Bing News

## Overview

Use this skill to turn a natural-language Bing News request into Dataify Bing News API fields, preview the full request body fields for user confirmation, call the API through `scripts/bing_news.py` only after confirmation, and return the API response directly to the user without summarizing, parsing, reformatting, or post-processing it.

The source API document is summarized in `references/api.md`. Read it when field behavior, allowed values, or response shape is unclear.

## Workflow

1. Identify the user's news query and map optional requirements to API fields:
   - `engine`: always `bing_news`. Default comes from the parameter description.
   - `q`: news search keywords. Default is `pizza` when the user does not specify a query, because the parameter description says the default is pizza.
   - `json`: output format. Default is `1` for JSON. Use `2` only when the user asks for JSON plus HTML. Use `3` only when the user asks for HTML.
   - `mkt`: display language and market, such as `en-US` or `zh-CN`. No default in the parameter description.
   - `cc`: two-letter country or region code, such as `us`, `cn`, `jp`, or `uk`. No default in the parameter description.
   - `first`: result offset. Default is `1` because the parameter description says the default is 1.
   - `count`: requested result count. No default in the parameter description.
   - `qft`: Bing query filter string for date sorting/filtering. No default in the parameter description.
   - `safeSearch`: `Off`, `Moderate`, or `Strict`. No default in the parameter description.
   - `no_cache`: `true` to bypass cache, `false` to use cache. Default is `false` because the parameter description says false is the default.
2. Get defaults only from parameter descriptions. Do not treat YAML body examples or inline examples like `mkt=en-US`, `cc=us`, or `count=10` as defaults.
3. Prefer explicit user-provided field values over inferred values. Add optional fields without defaults only when the user clearly asks for them or provides exact field values.
4. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags for any fields that should override automatic parsing. On Windows, if `python3` is not installed but `python` points to Python 3, use `python` for local execution.
5. Before every live API call, show the complete request parameter table and ask whether the user wants to modify anything. Do not show `Authorization`.
   - Run `--preview` to print a Markdown table with exactly these columns: 参数名, 当前值, 默认值, 说明.
   - Show the table to the user and ask for confirmation.
   - If the user asks to modify values, update the fields and preview the full table again.
   - Call the API only after the user confirms the displayed parameters.
6. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - If the user provides a token during the task, pass it with `--token` or set `DATAIFY_API_TOKEN` for the command before invoking the script.
   - The script adds a `Bearer ` prefix when the token does not already include one.
   - If no token is available, ask the user to input a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).
7. Preview parameters before calling:

```bash
python3 scripts/bing_news.py --prompt "Search Bing news for OpenAI" --preview
```

8. Run a live call only after the user confirms the previewed table:

```bash
python3 scripts/bing_news.py --prompt "Search Bing news for OpenAI"
```

9. Return the script output directly to the user. Do not summarize news results, extract fields, reformat JSON, parse embedded JSON strings, or process returned HTML unless the user separately asks for processing.

## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_news.py \
  --prompt "用必应新闻搜索 OpenAI"
```

Useful flags:

- `--q`, `--json`, `--mkt`, `--cc`, `--first`, `--count`, `--qft`, `--safeSearch`, `--no-cache`
- `--field key=value` for any supported API field
- `--token` to provide a token for the current run
- `--body-format form|json`, default `form`
- `--preview` to print the full confirmation table and skip network/auth checks
- `--dry-run` to print the parsed payload and skip network/auth checks
