---
name: dataify-google-lens
description: When the user requests "Call Google Lens" or "Search by Image", the dataify-google-lens skill is triggered.
---

# Dataify Google Lens

Use this skill to turn a user's Google Lens or reverse-image-search request into a Dataify Scraper API form submission.

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

1. Parse the user's request into Google Lens fields. Use `url` for the image URL, set `engine` to `google_lens`, and infer optional fields only when the user asks for them.
2. Build request parameters from the user's request. If the user did not specify a field, use only the documented default from the parameter description:
   - `engine`: `google_lens`
   - `json`: `1`
   - `type`: `all`
   - `no_cache`: `false`
   Fields with no documented default stay unset. Do not treat examples such as `us`, `en`, `active`, or `true` as defaults.
3. Before every API call, show the complete request parameter table and ask whether the user wants to modify anything. Do not include `Authorization` in the table. Use the bundled script's preview mode, then show its Markdown table directly:

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us --preview
```

Ask the user: `请确认是否需要修改这些参数；确认无误后我再调用接口。`

4. If the user changes parameters, update the values and show the preview table again. Do not call the API until the user confirms.
5. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_lens.py`. The script submits form data to the hardcoded API endpoint; it does not send a JSON body.

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us
```

Natural-language fallback is available when useful:

```bash
python3 scripts/google_lens.py --request "Search Google Lens for https://example.com/image.jpg, products, country US, safe on, no cache"
```

7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_lens_api.md` when you need the exact field list, defaults, constraints, or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always encode request data as UTF-8.
- Always force `engine` to `google_lens`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Use documented defaults when the user does not specify a value. Omit fields that have no documented default and were not requested.
- Ask a follow-up only when the required image `url` cannot be inferred from the user's request.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Never include `Authorization` in the preview table, and never print the token value in the final explanation.

Common mappings:

- Image URL, picture URL, reverse image search target -> `url`
- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- interface/search language -> `hl`
- country or region for Lens behavior -> `country`
- all results -> `type: "all"`
- product results -> `type: "products"`
- about this image -> `type: "about_this_image"`
- exact matches -> `type: "exact_matches"`
- visual matches or similar images -> `type: "visual_matches"`
- extra query/keyword/refinement used with `all`, `visual_matches`, or `products` -> `q`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- bypass cache -> `no_cache: "true"`


