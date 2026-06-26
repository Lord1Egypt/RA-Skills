---
name: dataify-bing-search
description: Use when a user ask run a Bing web search
---

# Bing Search

## Overview

Use this skill to turn a natural-language Bing search request into Dataify Bing Search API fields, call the API through `scripts/bing_search.py`, and return the API response directly to the user without summarizing, parsing, or post-processing it.

The source API document is summarized in `references/api.md`. Read it when field behavior, allowed values, or response shape is unclear.

## Workflow

1. Identify the user's actual search query and map requirements to API fields:
   - `q`: search terms. Required.
   - `json`: output format. Default to `1` for JSON when the user does not specify an output format. Use `2` for JSON plus HTML, `3` for HTML.
   - `location`: named geographic search origin.
   - `lat` and `lon`: GPS search origin.
   - `mkt`: display language and market, such as `zh-CN` or `en-US`. Do not pass it unless the user asks for a market/language.
   - `cc`: two-letter country or region code, such as `us`, `cn`, `jp`, `uk`. Do not pass it unless the user asks for a country/region.
   - `first`: organic result offset. Default to `1` when the user does not specify it.
   - `safeSearch`: `Off`, `Moderate`, or `Strict`.
   - `filters`: advanced Bing filter string.
   - `no_cache`: `true` to bypass cache, `false` to use cache. Default to `false` when the user does not specify it.
2. Apply defaults only when the parameter description states a default. Current defaults from the API description are `engine=bing`, `q=pizza`, `json=1`, `first=1`, and `no_cache=false`. Do not treat body examples such as `location=India`, `lat=1`, `lon=1`, `mkt=zh-cn`, or `cc=AR` as defaults.
3. Prefer explicit user-provided field values over inferred values. If the user asks for a concrete search, replace the documented default `q=pizza` with the user's actual query.
4. Before every live API call, show the user a complete request parameter table and ask whether to modify it. Do not show `Authorization`. Use:

```bash
python3 scripts/bing_search.py --prompt "<user request>" --show-params
```

The table must include exactly these columns: parameter name, current value, default value, and description. Wait for user confirmation before calling the API.
5. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags for any fields that should override automatic parsing.
6. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - If the user provides a token during the task, set `DATAIFY_API_TOKEN` in the environment for the command before invoking the script.
   - The script adds a `Bearer ` prefix when the token does not already include one.
   - If no token is available, the script exits with a Chinese prompt; ask the user to input a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).
7. Run a dry run when you need to inspect parsed payload JSON without calling the API:

```bash
python3 scripts/bing_search.py --prompt "Search Bing for current OpenAI news, return JSON and HTML" --dry-run
```

8. Run a live call only after the user confirms the parameter table:

```bash
python3 scripts/bing_search.py --prompt "Search Bing for current OpenAI news, return JSON and HTML"
```

9. Return the script output directly to the user. Do not summarize the search results, extract fields, reformat JSON, parse embedded JSON strings, or process returned HTML unless the user separately asks for processing.

## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_search.py \
  --prompt "Find current OpenAI news, return JSON and HTML" \
  --no-cache true
```

Useful flags:

- `--q`, `--json`, `--location`, `--lat`, `--lon`, `--mkt`, `--cc`, `--first`, `--safeSearch`, `--filters`, `--no-cache`
- `--field key=value` for any supported API field
- `--url` to override the fixed endpoint only when explicitly needed for debugging
- `--token` to provide a token for the current run
- `--body-format form|json`, default `form`
- `--dry-run` to print the parsed payload and skip network/auth checks
- `--show-params` to print the complete pre-call parameter table and exit

If a live call fails because `DATAIFY_API_TOKEN` is missing, ask the user to provide a token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill). 