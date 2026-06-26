---
name: dataify-google-hotels
description: When the user requests "Call Google Hotels" or "Search hotel prices/availability", or explicitly mentions the hotel query field, the dataify-google-hotels skill is triggered.
---

# Dataify Google Hotels

Use this skill to turn a user's Google Hotels request into a Dataify Scraper API form POST.

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

1. Parse the user's request into Dataify Google Hotels fields. Read `references/google_hotels_api.md` when the exact field list, accepted values, defaults, or mapping notes are needed.
2. Resolve relative dates from the conversation date, then pass dates as `YYYY-MM-DD`.
3. Run a dry run with `python3` before every API call. Show the generated Markdown table to the user exactly as the pre-call parameter review. The table must contain the complete field list and only these columns: parameter name, current value, default value, and description.

```bash
python3 scripts/google_hotels.py --params-json '{"q":"Tokyo hotels","check_in_date":"2026-06-01","check_out_date":"2026-06-03","gl":"us","hl":"en"}' --dry-run
```

4. Ask the user whether they want to modify any parameters. Do not call the API until the user confirms.
5. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. After the user confirms the table, run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_hotels.py`.

```bash
python3 scripts/google_hotels.py --token "USER_TOKEN" --params-json '{"q":"Tokyo hotels","check_in_date":"2026-06-01","check_out_date":"2026-06-03","gl":"us","hl":"en"}'
```

7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response body.

## Mapping Rules

- Always submit the API request as form data with UTF-8 encoding and `Content-Type: application/x-www-form-urlencoded; charset=utf-8`.
- Always force `engine` to `google_hotels`.
- Use documented defaults only. Do not treat examples, placeholders, or blank values in the API docs as defaults.
- Use `json: "1"` unless the user asks for another output format.
- Use `q`, `check_in_date`, and `check_out_date` for normal hotel searches when they can be inferred. Ask a follow-up if a normal search is missing any of those fields.
- Use `property_token` for hotel detail requests when the user provides a property token.
- Use `next_page_token` for next-page requests when the user provides a pagination token.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- lowest price / cheapest -> `sort_by: "3"`
- highest rating -> `sort_by: "8"`
- most reviewed -> `sort_by: "13"`
- rating 3.5+ / 4.0+ / 4.5+ -> `rating: "7"` / `"8"` / `"9"`
- free cancellation -> `free_cancellation: "true"`
- special offers -> `special_offers: "true"`
- eco certified -> `eco_certified: "true"`
- vacation rentals -> `vacation_rentals: "true"`
- bypass cache / no cache -> `no_cache: "true"`


