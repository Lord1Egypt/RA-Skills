---
name: dataify-google-play
description: When the user requests "call Google Play" or "app store search/ranking", or explicitly mentions the Google Play search field, the dataify-google-play skill is triggered.
---

# Dataify Google Play

Use this skill to turn a user's Google Play request into a Dataify Scraper API call.

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

1. Parse the user's request into Dataify Google Play fields. Use `q` as the app-store search query and set `engine` to `google_play`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters with only the fields the user requested plus required defaults. Use `json: "1"` unless the user asks for another output format. Do not treat example values in the API docs as defaults.
4. Before calling the API, show the complete field checklist as a Markdown table with exactly these columns: `参数名`, `当前值`, `默认值`, `说明`. Include every request field from `references/google_play_api.md`, including `engine`. Then ask the user whether to modify parameters. Only call the API after the user confirms.
5. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_play.py`.

```bash
python3 scripts/google_play.py --q "meditation app" --gl us --hl en --json 1
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_play.py --params-json '{"q":"meditation app","gl":"us","hl":"en","json":"1"}'
```

To preview the normalized payload for the required confirmation table, use `--dry-run`:

```bash
python3 scripts/google_play.py --request "搜索美国 Google Play 上的冥想 app，英文，JSON" --dry-run
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_play.py --token "USER_TOKEN" --q "meditation app" --gl us --hl en
```

6. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_play_api.md` when you need the exact field list, defaults, and parameter values.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_play`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request.
- Ask a follow-up only when required `q` cannot be inferred and the request is not a category/chart/device-only request supported by the user's provided fields.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not use more than one of `next_page_token`, `section_page_token`, `see_more_token`, and `chart` together.
- Do not use `store_device` together with `apps_category` or `q`.
- Use `age` only when `apps_category` is `FAMILY`.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- app search phrase -> `q`
- country or region for Google Play behavior -> `gl`
- interface/search language -> `hl`
- Google Play category -> `apps_category`
- next page token -> `next_page_token`
- section page token -> `section_page_token`
- top chart / popular ranking -> `chart`
- see more token -> `see_more_token`
- phone/tablet/tv/chromebook/watch/car device browsing -> `store_device`
- kids/family category -> `apps_category: "FAMILY"`
- age 5 and under -> `age: "AGE_RANGE1"`
- age 6 to 8 -> `age: "AGE_RANGE2"`
- age 9 to 12 -> `age: "AGE_RANGE3"`
- bypass cache -> `no_cache: "true"`


