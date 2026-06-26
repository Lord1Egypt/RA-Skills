---
name: dataify-google-search
description: When the user requests "call Google Search" or "web search/SERP crawling", or explicitly mentions the web search field, the dataify-google-search skill is triggered.
---

# Dataify Google Search

Use this skill to turn a user's Google search request into a Dataify Scraper API call.

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

1. Parse the user's request into Dataify Google Search fields. Use `q` as the search query and set `engine` to `google`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters with only the fields the user requested plus required defaults. Use `json: "1"` unless the user asks for another output format. The script submits these parameters as form data, not a JSON request body.
4. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_search.py`.

```bash
python3 scripts/google_search.py --q "OpenAI news" --gl us --hl en --json 1
```

For many fields, you may pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_search.py --params-json '{"q":"OpenAI news","gl":"us","hl":"en","json":"1"}'
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_search.py --token "USER_TOKEN" --q "OpenAI news" --gl us --hl en
```

5. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_search_api.md` when you need the exact field list or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request.
- Ask a follow-up only when the required search query `q` cannot be inferred.
- If both `location` and `uule` are present, prefer the explicit `uule` and omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- country-restricted results -> `cr`, formatted like `countryFR`
- language-restricted results -> `lr`, formatted like `lang_fr`
- page number N -> `start: String((N - 1) * 10)`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- desktop/tablet/mobile -> `device`
- render JavaScript -> `render_js: "true"`
- bypass cache -> `no_cache: "true"`
- include AI Overview -> `ai_overview: "true"`


