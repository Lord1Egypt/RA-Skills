---
name: dataify-google-shopping
description: When the user requests "call Google Shopping" or "shopping search/product search/price comparison", or explicitly mentions the shopping search field, the dataify-google-shopping skill is triggered.
---

# Dataify Google Shopping

Use this skill to turn a user's Google Shopping request into a Dataify Scraper API call.

## Required Pre-Call Confirmation

Before every real API call, follow this confirmation flow. These rules override any older workflow order in this skill.

1. Parse the user's request into the API body fields and fixed `engine` value.
2. Apply defaults only when the parameter description explicitly states a default. Do not use example YAML values, sample prompts, placeholder values, or examples such as `pizza`, `us`, `en`, dates, airport codes, or tokens as defaults.
3. If a required parameter has no documented default and cannot be inferred from the user request, ask for that parameter before building the table.
4. Show a Markdown table before calling the API. Do not include `Authorization`. Include the complete body field list from this skill's reference document, including `engine`, even when a field is currently blank.
5. The table must have exactly these columns: `参数名`, `当前值`, `默认值`, `说明`.
6. After the table, ask the user whether they want to modify any parameter. Do not call the API until the user explicitly confirms.
7. If the user changes a parameter, regenerate the table and ask for confirmation again.
8.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.

Use the bundled preview helper whenever possible to generate the confirmation table from this skill's reference document:

```bash
python3 scripts/preview_params.py --params-json '{"q":"USER_QUERY"}'
```

Pass every parsed current value to `preview_params.py` using `--params-json` or matching `--field value` arguments. The helper reads defaults and descriptions from `references/*api.md`; if the helper cannot parse a default, leave the default blank rather than inventing one.
9. After confirmation and token handling, call the bundled Python script with `python3` and return the API response body directly without summarizing, extracting, cleaning, translating, or reshaping it.
## Workflow

1. Parse the user's request into Dataify Google Shopping fields. Use `q` as the shopping search query and always set `engine` to `google_shopping`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters with only the fields the user requested plus required documented defaults. Use `json: "1"` and `google_domain: "google.com"` unless the user asks for another value. Do not use example values from the API document as defaults.
4. Before every API call, show the user a Markdown table containing the complete field list with exactly these columns: `参数名`, `当前值`, `默认值`, `说明`. Mask the token status as `已提供` or `未提供`; do not display the token. Ask whether the user wants to modify the parameters and do not call the API until the user confirms.
5. If the user changes any parameter, update the values and show the complete table again before calling.
6. After confirmation, run the bundled Python script with `python3`. The script submits form data to the hardcoded endpoint `https://scraperapi.dataify.com/request`.
7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Script Usage

Run commands from this skill directory, or use the absolute path to `scripts/google_shopping.py`.

Preview the complete parameter table:

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true --table
```

Call the API after the user confirms:

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true
```

For natural-language parsing, pass the user's request:

```bash
python3 scripts/google_shopping.py --request "搜索美国 Google Shopping 上 100 美元以下包邮的无线耳机，英文，返回 JSON" --table
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_shopping.py --params-json '{"q":"wireless headphones","gl":"us","hl":"en","max_price":"100","free_shipping":"true"}' --table
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_shopping.py --token "USER_TOKEN" --q "wireless headphones" --gl us --hl en
```

Use `--dry-run` only for internal verification. It prints the normalized payload JSON and does not call the API.

## Field Mapping

Use `references/google_shopping_api.md` when you need the complete field list, defaults, or exact descriptions for the preview table.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_shopping`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request unless the API document gives a real default.
- Ask a follow-up only when the required shopping query `q` cannot be inferred.
- If both `location` and `uule` are present, prefer the explicit `uule` and omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- page number N -> `start: String((N - 1) * 10)`
- raw Google Shopping filter token -> `shoprs`
- minimum price -> `min_price`
- maximum price -> `max_price`
- price low to high -> `sort_by: "1"`
- price high to low -> `sort_by: "2"`
- free shipping only -> `free_shipping: "true"`
- sale or discount items only -> `on_sale: "true"`
- small business items only -> `small_business: "true"`
- bypass cache -> `no_cache: "true"`


