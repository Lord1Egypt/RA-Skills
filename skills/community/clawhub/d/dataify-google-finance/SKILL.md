---
name: dataify-google-finance
description: This skill is triggered when the user requests "call Google Finance" or "search Google Finance", or explicitly mentions something related to financial data (stocks, indices, funds, currencies, futures)
---

# Dataify Google Finance

Use this skill to turn a user's Google Finance request into a Dataify Scraper API form POST.

## Required Pre-Call Confirmation

Before every real API call, follow this confirmation flow. These rules override any older workflow order in this skill.

1. Parse the user's request into the API body fields and fixed `engine` value.
2. Apply defaults only when the parameter description explicitly states a default. Do not use example YAML values, sample prompts, placeholder values, or examples such as `pizza`, `us`, `en`, dates, airport codes, or tokens as defaults.
3. If a required parameter has no documented default and cannot be inferred from the user request, ask for that parameter before building the table.
4. Show a Markdown table before calling the API. Do not include `Authorization`. Include the complete body field list from this skill's reference document, including `engine`, even when a field is currently blank.
5. The table must have exactly these columns: `参数名`, `当前值`, `默认值`, `说明`.
6. After the table, ask the user whether they want to modify any parameter. Do not call the API until the user explicitly confirms.
7. If the user changes a parameter, regenerate the table and ask for confirmation again.
8. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.

Use the bundled preview helper whenever possible to generate the confirmation table from this skill's reference document:

```bash
python3 scripts/preview_params.py --params-json '{"q":"USER_QUERY"}'
```

Pass every parsed current value to `preview_params.py` using `--params-json` or matching `--field value` arguments. The helper reads defaults and descriptions from `references/*api.md`; if the helper cannot parse a default, leave the default blank rather than inventing one.
9. After confirmation and token handling, call the bundled Python script with `python3` and return the API response body directly without summarizing, extracting, cleaning, translating, or reshaping it.
## Workflow

1. Parse the user's request into Dataify Google Finance fields. Use `q` as the finance query and set `engine` to the fixed value `google_finance`.
2. Apply only documented defaults from the parameter descriptions:
   - `engine`: fixed `google_finance`
   - `json`: default `1`
   - `window`: default `1D`
   - `no_cache`: default `false`
   - `q`: no default; ask the user if it cannot be inferred
   - `hl`: no documented default; leave empty unless the user specifies it
3. Before every API call, run the bundled script with `python3` in preview mode and show the returned Markdown table to the user. The table must contain the complete request field list except `Authorization`, with only these columns: parameter name, current value, default value, and description.

```bash
python3 scripts/google_finance.py --request "查询 NASDAQ:GOOGL，窗口 1年，英文，返回 JSON" --preview-table
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_finance.py --params-json '{"q":"NASDAQ:GOOGL","window":"1Y","hl":"en","json":"1"}' --preview-table
```

4. Ask the user whether they want to modify the parameters. Do not call the API until the user confirms. If they request changes, update the fields and show the preview table again.
5. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_finance.py`.

```bash
python3 scripts/google_finance.py --q "NASDAQ:GOOGL" --window 1Y --hl en --json 1
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_finance.py --token "USER_TOKEN" --q "NASDAQ:GOOGL" --window 1Y
```

For a natural-language fallback, pass the whole request:

```bash
python3 scripts/google_finance.py --request "搜索苹果股票，图表范围 5天，不使用缓存"
```

7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response body.

## Field Mapping

Use `references/google_finance_api.md` for the complete parameter descriptions and documented defaults.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_finance`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up only when the required finance query `q` cannot be inferred.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not show `Authorization` in the pre-call parameter table.
- Do not invent defaults from examples. Only use defaults explicitly stated in the parameter descriptions.

Common mappings:

- stock, index, mutual fund, currency, or futures search term -> `q`
- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- interface/search language -> `hl`
- "1天", "1 day", or "1D" -> `window: "1D"`
- "5天", "5 days", or "5D" -> `window: "5D"`
- "1个月", "1 month", or "1M" -> `window: "1M"`
- "6个月", "6 months", or "6M" -> `window: "6M"`
- "年初至今" or "YTD" -> `window: "YTD"`
- "1年", "1 year", or "1Y" -> `window: "1Y"`
- "5年", "5 years", or "5Y" -> `window: "5Y"`
- "最大", "max", or "MAX" -> `window: "MAX"`
- bypass cache -> `no_cache: "true"`


