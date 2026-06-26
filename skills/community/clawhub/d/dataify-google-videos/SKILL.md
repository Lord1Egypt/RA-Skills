---
name: dataify-google-videos
description: When the user requests "Call Google Videos" or "Video Search", or explicitly mentions the video field, the dataify-google-videos skill is triggered.
---

# Dataify Google Videos

Use this skill to turn a user's Google Videos request into a Dataify Scraper API form submission.

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

1. Parse the user's request into Google Videos fields. Use `q` as the video search query and force `engine` to `google_videos`.
2. Build request parameters with the fields the user requested plus the documented defaults only: `json: "1"`, `google_domain: "google.com"`, `no_cache: "false"`, `nfpr: "0"`, and `filter: "0"`. Do not treat examples such as `us`, `en`, or `true` as defaults.
3. Before every API call, show the complete parameter table to the user and ask whether they want to modify anything. The table must contain only these columns: parameter name, current value, default value, and description. Include the complete field list from `references/google_videos_api.md`, including `Authorization` and `engine`. Mask any token value, or show `missing` when no token is available.
4. If the user requests changes, update the parameters and show the complete table again. Call the API only after the user confirms.
5.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_videos.py`.

Preview the confirmation table:

```bash
python3 scripts/google_videos.py --request "search Google videos for electric cars in English" --preview-table
```

Call the API after confirmation:

```bash
python3 scripts/google_videos.py --q "electric cars" --hl en
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_videos.py --token "USER_TOKEN" --q "electric cars" --gl us --hl en
```

For many fields, pass one JSON object with shell-appropriate quoting. The script will still submit form data to the API:

```bash
python3 scripts/google_videos.py --params-json '{"q":"electric cars","json":"1","google_domain":"google.com","gl":"us","hl":"en","no_cache":"true"}'
```

7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_videos_api.md` when you need the exact field list, defaults, constraints, or table descriptions.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_videos`.
- Use UTF-8 for script source, form encoding, and displayed text.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up only when the required video query `q` cannot be inferred.
- If `uule` is present, omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google domain -> `google_domain`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- named search origin -> `location`
- Google encoded location -> `uule`
- page number N -> `start: String((N - 1) * 10)`
- advanced video filters, duration, quality, source, or date -> `tbs`
- bypass cache / no cache -> `no_cache: "true"`
- language-restricted results -> `lr`, formatted like `lang_fr`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- exclude autocorrected query results -> `nfpr: "1"`
- include autocorrected query results -> `nfpr: "0"`
- disable similar/omitted result filters -> `filter: "1"`
- enable similar/omitted result filters -> `filter: "0"`


