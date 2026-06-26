---
name: dataify-google-local
description: When the user requests "call Google Local" or "local search/nearby search/place search", or explicitly mentions the local search field, the dataify-google-local skill is triggered.
---

# Dataify Google Local

Use this skill to turn a user's Google Local request into a Dataify Scraper API form POST.

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

1. Parse the user's request into Google Local fields. Always set `engine` to the fixed value `google_local`.
2. Before every API call, show the user a complete parameter preview in the visible conversation with all documented parameters, including fields that are not assigned. Include each field's current value, documented default, and description. Do not treat examples or allowed values as defaults. Prefer running `python3 scripts/google_local.py ... --preview-params --preview-format markdown` after parsing the request and pasting that Markdown table into the chat.
3. After showing the table, ask the user whether to modify any parameters or confirm the call. Do not call the API until the user explicitly confirms. Accept confirmations such as `确认`, `可以`, `继续`, `调用`, `yes`, or `go`.
4. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
5. Build request parameters with the fields the user requested plus documented defaults only: `engine: "google_local"`, `json: "1"`, `google_domain: "google.com"`, and `no_cache: "false"`. Omit optional fields that the user did not request and that have no documented default.


```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --gl us --hl en
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_local.py --params-json '{"q":"coffee shops","location":"New York","gl":"us","hl":"en"}'
```

PowerShell may need the quotes escaped:

```powershell
python3 scripts/google_local.py --params-json '{\"q\":\"coffee shops\",\"location\":\"New York\",\"gl\":\"us\",\"hl\":\"en\"}'
```

To let the script parse a natural-language request:

```bash
python3 scripts/google_local.py --request "搜索纽约咖啡店，语言英文，地区美国，不走缓存"
```

If the user provided a token in the conversation, pass it with `--token` and avoid echoing it back:

```bash
python3 scripts/google_local.py --token "USER_TOKEN" --q "coffee shops" --location "New York"
```

7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Parameter Notice

When using this skill, show this concise parameter list before making the API call, or run `python3 scripts/google_local.py --describe-params` and relay that output:

| Field | Required | Default | Description |
|---|---:|---|---|
| `Authorization` | yes | none | Dataify API token in the request header. If the token does not start with `Bearer `, the script adds it. |
| `engine` | yes | `google_local` | Fixed engine value for Google Local. |
| `q` | yes | none | Search query content. |
| `json` | yes | `1` | Output format. `1` = JSON, `2` = JSON+HTML, `3` = HTML, `4` = Light JSON. |
| `google_domain` | no | `google.com` | Google domain to use. |
| `gl` | no | none | Two-letter Google country/region code, such as `us`, `uk`, or `fr`. |
| `hl` | no | none | Google interface/search language code, such as `en`, `es`, or `fr`. |
| `location` | no | none | Geographic location where the search originates. |
| `uule` | no | none | Google encoded location. Do not use with `location`; prefer explicit `uule` if both are present. |
| `start` | no | none | Result offset for pagination. |
| `ludocid` | no | none | Google place CID/customer identifier. |
| `tbs` | no | none | Advanced search parameter not represented by the regular query field. |
| `no_cache` | no | `false` | `true` bypasses cache; `false` uses cached results when available. |

For an actual request, show a complete preview instead of only the assigned request payload:

```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --preview-params --preview-format markdown
```

The preview output must include unset fields such as `gl`, `hl`, `uule`, `start`, `ludocid`, and `tbs` when the user did not provide them.
After pasting the preview table, ask: `请确认是否按以上参数调用接口，或告诉我要修改哪些字段。`

## Field Mapping

Use `references/google_local_api.md` when exact parameter wording is needed.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_local`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request unless the field has a documented default.
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
- named search origin -> `location`
- encoded location -> `uule`
- page number N -> `start: String((N - 1) * 10)`
- Google place CID -> `ludocid`
- advanced search filters -> `tbs`
- bypass/no cache -> `no_cache: "true"`


