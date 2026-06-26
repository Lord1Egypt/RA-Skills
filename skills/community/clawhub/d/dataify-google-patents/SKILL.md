---
name: dataify-google-patents
description: When the user requests "call Google Patents" or "patent search", or explicitly mentions the patent search field, the dataify-google-patents skill is triggered.
---

# Dataify Google Patents

Use this skill to turn a user's Google Patents request into a Dataify Scraper API call.

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

1. Parse the user's request into Dataify Google Patents fields. Always set `engine` to `google_patents`.
2. Apply only defaults that are explicitly stated in the parameter descriptions:
   - `json: "1"`
   - `page: "0"`
   - `dups: "family"`
   - `patents: "true"`
   - `scholar: "false"`
   - `no_cache: "false"`
   - `sort` defaults to relevance by omitting the field.
3. Do not use example values as defaults. Omit optional fields that have no documented default unless the user requested them.
4.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
5. Before every API call, run the bundled Python script with `python3` and `--print-table` to generate the full parameter review table:

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents" --print-table
```

Show the table to the user with exactly these columns: parameter name, current value, default value, and description. Ask whether they want to modify any parameter. Do not call the API until the user confirms.

6. If the user changes parameters, pass the edited values with explicit flags or with `--params-json`, show the table again, and ask for confirmation again.
7. After confirmation, call the script without `--print-table`:

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents"
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_patents.py --params-json '{"q":"battery recycling","status":"GRANT","country":"US","json":"1"}'
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_patents.py --token "USER_TOKEN" --q "battery recycling"
```

8. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_patents_api.md` when you need the exact field list, defaults, accepted values, and mapping hints.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always use UTF-8 encoding.
- Always force `engine` to `google_patents`; ignore any conflicting user-provided engine.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up when no meaningful search query or filter can be inferred.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not reveal the full token in the parameter review table.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- first page -> `page: "0"`, second page -> `page: "1"`
- newest/latest/recent -> `sort: "new"`
- oldest/earliest -> `sort: "old"`
- relevance/default relevance -> omit `sort`
- grouped/clustered results -> `clustered: "true"`
- family deduplication -> `dups: "family"`
- publication deduplication -> `dups: "language"`
- include patent results -> `patents: "true"`
- include Google Scholar results -> `scholar: "true"`
- before/after dates -> `before` or `after`, formatted as `priority:YYYYMMDD`, `filing:YYYYMMDD`, or `publication:YYYYMMDD`
- inventor names -> `inventor`
- assignee, applicant, or owner names -> `assignee`
- country/region patent codes -> `country`
- result language filter -> `language`
- granted patents -> `status: "GRANT"`
- applications -> `status: "APPLICATION"`
- patent type -> `type: "PATENT"`
- design type -> `type: "DESIGN"`
- litigation yes/no -> `litigation: "YES"` or `litigation: "NO"`
- bypass cache -> `no_cache: "true"`


