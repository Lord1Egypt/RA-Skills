---
name: dataify-google-scholar
description: When the user requests "call Google Scholar" or "academic search/paper search", or explicitly mentions the academic search field, the dataify-google-scholar skill is triggered.
---

# Dataify Google Scholar

Use this skill to turn a user's Google Scholar request into a Dataify Scraper API call.

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

1. Parse the user's request into Dataify Google Scholar fields. Always set `engine` to `google_scholar`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters from the user's request plus documented defaults. Defaults must come only from parameter descriptions in `references/google_scholar_api.md`; never use example values as defaults.
4. Before calling the API, show the user a Markdown table with the full field list except `Authorization`. The table must contain only these columns: `参数名`, `当前值`, `默认值`, `说明`.
5. Ask the user whether to modify any parameter. Call the API only after the user confirms. If the user changes values, update the table or request payload before calling.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_scholar.py`.

Preview the complete parameter table:

```bash
python3 scripts/google_scholar.py --request "搜索 large language model，2020 到 2024，返回 20 条" --preview
```

Call the API after the user confirms:

```bash
python3 scripts/google_scholar.py --q "large language model" --as_ylo 2020 --as_yhi 2024 --num 20
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_scholar.py --params-json '{"q":"large language model","as_ylo":"2020","as_yhi":"2024","num":"20"}'
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_scholar.py --token "USER_TOKEN" --q "large language model"
```

7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_scholar_api.md` when you need the exact field list, defaults, or accepted values.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_scholar`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Include documented defaults when the user did not specify a field.
- Omit optional fields that have no documented default and no user value.
- Ask a follow-up only when no usable search condition can be inferred. A usable search condition is `q`, `cites`, or `cluster`.
- Do not combine `cluster` with `q` or `cites`; `cluster` must be used by itself.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- interface/search language -> `hl`
- language-restricted results -> `lr`, formatted like `lang_fr` or `lang_fr|lang_de`
- page number N -> `start: String((N - 1) * 10)`
- result count -> `num`, range `1` to `20`
- cited-by search -> `cites`
- all versions search -> `cluster`
- year range lower bound -> `as_ylo`
- year range upper bound -> `as_yhi`
- past-year/date sort -> `scisbd: "1"` for abstracts only or `scisbd: "2"` for all content
- include patents -> `as_sdt: "7"`
- exclude patents -> `as_sdt: "0"`
- US case law -> `as_sdt: "4"`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- disable similar/omitted result filter -> `filter: "0"`
- exclude citations -> `as_vis: "1"`
- include citations -> `as_vis: "0"`
- review articles only -> `as_rr: "1"`
- bypass cache -> `no_cache: "true"`


