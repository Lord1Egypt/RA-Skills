---
name: dataify-google-jobs
description: When the user requests "Call Google Jobs" or "Search for job/recruitment information and return the original response", or specifies the job search fields, the dataify-google-jobs skill is triggered.
---

# Dataify Google Jobs

Use this skill to turn a user's Google Jobs request into a Dataify Scraper API form POST.

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

1. Parse the user's request into Dataify Google Jobs fields. Use `q` as the job search query and set `engine` to the fixed value `google_jobs`.
2. Build request parameters from the user-provided values plus documented defaults only. Defaults must come from the parameter descriptions in `references/google_jobs_api.md`; never treat examples as defaults.
   - `engine`: fixed `google_jobs`
   - `json`: default `1`
   - `google_domain`: default `google.com`
   - `no_cache`: default `false`
   - All other parameters have no documented default and must stay unset unless the user provides them.
3. Before every API call, show a Markdown table containing the complete body parameter list, excluding `Authorization`. The table must have exactly these columns: parameter name, current value, default value, description. Ask the user whether to modify the parameters. If the user requests changes, update the values and show the table again. Only call the API after the user confirms the table.
4. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
5. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_jobs.py`. 

```bash
python3 scripts/google_jobs.py --q "software engineer jobs" --location "San Francisco" --gl us --hl en
```

Generate the confirmation table with:

```bash
python3 scripts/google_jobs.py --request "搜索 java 相关工作" --preview-table
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_jobs.py --params-json '{"q":"software engineer jobs","location":"San Francisco","gl":"us","hl":"en"}'
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_jobs.py --token "USER_TOKEN" --q "software engineer jobs" --location "San Francisco"
```

For a natural-language fallback, pass the whole request:

```bash
python3 scripts/google_jobs.py --request "搜索美国旧金山的软件工程师工作，语言英文，不使用缓存"
```

6. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response body.

## Field Mapping

Use `references/google_jobs_api.md` for the complete parameter descriptions and defaults.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_jobs`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up only when the required job search query `q` cannot be inferred.
- If both `location` and `uule` are present, prefer the explicit `uule` and omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not include `Authorization` in the preview table.
- Do not call the API until the user confirms the preview table.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google domain -> `google_domain`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- geographic search origin -> `location`
- encoded Google location -> `uule`
- next page -> `next_page_token`
- chips/filter token from Google Jobs -> `chips`
- search radius in kilometers -> `lrad`
- work from home / remote-only filter -> `ltype: "1"` when requested
- Google-provided filter string -> `uds`
- bypass cache -> `no_cache: "true"`


