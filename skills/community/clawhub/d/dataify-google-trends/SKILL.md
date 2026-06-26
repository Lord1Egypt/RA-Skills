---
name: dataify-google-trends
description: When the user requests "Call Google Trends" or "Trend Search/Google Trends", or explicitly mentions the trend search field, the dataify-google-trends skill is triggered.
---

# Dataify Google Trends

Use this skill to turn a user's Google Trends request into a Dataify Scraper API form submission.

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
9. After confirmation and token handling, call the bundled Python script with `python3` and return the API response body directly without summarizing, extracting, cleaning, translating, or reshaping it.

Use the bundled preview helper whenever possible to generate the confirmation table from this skill's reference document:

```bash
python3 scripts/preview_params.py --q "USER_QUERY"
```

Pass every parsed current value to `preview_params.py` using matching `--field value` arguments. The helper reads defaults and descriptions from `references/*api.md`; if the helper cannot parse a default, leave the default blank rather than inventing one.
## Workflow

1. Parse the user's request into Google Trends fields. Use `q` as the query and set `engine` to `google_trends`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters from the user's request plus required API defaults. Do not use example values as defaults. In particular, do not default `q` to `pizza`; ask the user for a query if it cannot be inferred.
4. Before every API call, show a Markdown table with the complete field list and only these columns: `参数名`, `当前值`, `默认值`, `说明`. Do not include `Authorization` in the parameter table.
5. Ask the user whether to modify any parameters. Do not call the API until the user confirms.
6. After confirmation, run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_trends.py`.

```bash
python3 scripts/google_trends.py --q "AI" --json 1
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_trends.py --token "USER_TOKEN" --q "AI" --geo "United+States" --hl en --data_type TIMESERIES --no_cache true
```

For many fields, pass one JSON object with shell-appropriate quoting. The script still submits form data to the API:

```bash
python3 scripts/google_trends.py --params-json '{"q":"AI","json":"1","hl":"en","geo":"United+States","data_type":"TIMESERIES"}'
```

To generate the required pre-call parameter table from the normalized request without calling the API:

```bash
python3 scripts/google_trends.py --request "search Google Trends for AI in the United States, English, timeseries" --preview-table
```

Return the final script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_trends_api.md` when you need the exact field list, defaults, values, or parameter descriptions.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_trends`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request unless the API has a documented default that should be shown in the confirmation table.
- Ask a follow-up only when required `q` cannot be inferred.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Use UTF-8 for all files, script output, and request encoding.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- bypass cache / no cache / skip cache -> `no_cache: "true"`
- use cache -> `no_cache: "false"`
- language / interface language -> `hl`
- country, region, or Google Trends location -> `geo`
- subregion level / city / DMA / country-region breakdown -> `region`
- time trend / interest over time -> `data_type: "TIMESERIES"`
- regional comparison -> `data_type: "GEO_MAP"`
- regional interest distribution -> `data_type: "GEO_MAP_0"`
- related topics -> `data_type: "RELATED_TOPICS"`
- related queries -> `data_type: "RELATED_QUERIES"`
- timezone offset in minutes -> `tz`
- category -> `cat`
- image search -> `gprop: "images"`
- news search -> `gprop: "news"`
- Google Shopping -> `gprop: "froogle"`
- YouTube Search -> `gprop: "youtube"`
- date range, "past 12 months", "today 5-y", or other Google Trends date expression -> `date`
- CSV results -> `csv: "true"`
- include low search volume regions -> `include_low_search_volume: "true"`

