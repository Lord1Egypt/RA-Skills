---
name: dataify-bing-shopping
description: Use when a user search Bing Shopping, find product or shopping results
---

# Bing Shopping

## Overview

Use this skill to convert a natural-language Bing Shopping request into Dataify Bing Shopping API fields, call the fixed Dataify endpoint through `scripts/bing_shopping.py`, and return the API response directly to the user without summarizing, parsing, or post-processing it.

The source API document is summarized in `references/api.md`. Read it when field behavior or response shape is unclear.

## Workflow

1. Identify the user's product or shopping query and map optional requirements to API fields:
   - `q`: shopping search query. Required.
   - `json`: output format. Default is `1` because the field description says JSON is the default. Use `2` only when the user asks for JSON plus HTML, and `3` only when the user asks for HTML.
   - `mkt`: display language and market. No default in the field description.
   - `cc`: two-letter country or region code. No default in the field description.
   - `efirst`: shopping result offset. No default in the field description.
   - `filters`: advanced Bing filter string. No default in the field description.
   - `no_cache`: cache behavior. Default is `false` because the field description says `false` is the default.
2. Use defaults only when the field description explicitly states a default. Do not treat example request body values as defaults. Values such as `pizza`, `en-US`, `us`, empty strings, or sample filters are examples only, not defaults.
3. Prefer explicit user-provided field values over inferred values. If an optional field is ambiguous and has no documented default, omit it.
4. Before every live API call, show the full request-parameter table to the user. Do not include `Authorization` in the table. Include exactly these columns: `参数名`, `当前值`, `默认值`, `说明`. Display the `说明` column in Chinese.
5. Ask the user whether they want to modify any parameter. Do not call the API until the user confirms. If the user modifies parameters, show the updated table and ask again.
6. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags only when overriding automatic parsing.
7. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - If the user provides a token during the task, pass it with `--token` or set `DATAIFY_API_TOKEN` for the command before invoking the script.
   - The script adds a `Bearer ` prefix when the token does not already include one.
   - If no token is available, the script exits with a Chinese prompt; ask the user to input a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).
8. Generate the parameter table before requesting confirmation:

```bash
python3 scripts/bing_shopping.py --prompt "Search Bing Shopping for wireless earbuds" --preview-table
```

9. Run a live call only after the user confirms the displayed table:

```bash
python3 scripts/bing_shopping.py --prompt "Search Bing Shopping for wireless earbuds" --confirmed
```

10. Return the script output directly to the user. Do not summarize shopping results, extract fields, reformat JSON, parse embedded JSON strings, or process returned HTML unless the user separately asks for processing.

## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_shopping.py \
  --prompt "Bing Shopping search for laptop stand, return JSON and HTML in the US market" \
  --json 2 \
  --cc us
```

Useful flags:

- `--q`, `--json`, `--mkt`, `--cc`, `--efirst`, `--filters`, `--no-cache`
- `--field key=value` for any supported API field
- `--token` to provide a token for the current run
- `--body-format form|json`, default `form`
- `--dry-run` to print the parsed payload and skip network/auth checks
- `--preview-table` to print the full parameter table and skip network/auth checks
- `--confirmed` to allow the live API call after the user has confirmed the table

When no optional fields are specified by the user, the payload should contain `engine`, `q`, `json=1`, and `no_cache=false`.

