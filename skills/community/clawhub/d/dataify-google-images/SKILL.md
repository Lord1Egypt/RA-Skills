---
name: dataify-google-images
description: When the user requests "call Google Images" or "search Google Images", or explicitly mentions the image to trigger the dataify-google-images skill.
---

# Dataify Google Images

Use this skill to turn a user's Google Images request into a Dataify Scraper API form submission.

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

1. Parse the user's request into Google Images fields. Use `q` as the image search query and set `engine` to `google_images`.
2. Apply documented defaults when the user does not specify a value. Use only defaults stated in the parameter descriptions: `json=1`, `google_domain=google.com`, `start=0`, `nfpr=0`, `filter=1`, `device=desktop`, and `no_cache=false`. Do not treat examples such as `pizza`, `us`, `en`, `radius=10`, `tbm=isch`, `render_js=true`, or `ai_overview=true` as defaults.
3. Before any API call, show the user a Markdown table containing the complete request field list except `Authorization`. The table must have exactly these columns: `参数名`, `当前值`, `默认值`, `说明`. Include `engine` and every body field, even when the current value is unset. Use the bundled script to generate the table when possible:

```bash
python3 scripts/google_images.py --params-table --q "red sneakers" --json 1
```

4. After showing the table, ask the user whether they want to modify any parameter. Do not call the API until the user explicitly confirms. If the user modifies parameters, regenerate the table and ask again.
5. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. Build request parameters with the fields the user requested plus documented defaults. The script submits these parameters as form data, not a JSON request body.
7. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_images.py`.

```bash
python3 scripts/google_images.py --q "red sneakers" --json 1
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_images.py --token "USER_TOKEN" --q "red sneakers" --gl us --hl en
```

For many fields, pass one JSON object with shell-appropriate quoting. The script will still submit form data to the API:

```bash
python3 scripts/google_images.py --params-json '{"q":"red sneakers","json":"1","google_domain":"google.com","gl":"us","hl":"en","device":"mobile"}'
```

8. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_images_api.md` when you need the exact field list, defaults, constraints, or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_images`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Include documented default values when the user did not request a value. Omit optional fields only when they have no documented default and the user did not request them.
- Ask a follow-up only when the required image query `q` cannot be inferred.
- If `uule` is present, omit `location`, `lat`, `lon`, and `radius`.
- If `location` is present, omit `uule`, `lat`, and `lon`.
- Use `lat` and `lon` together. If only one is available, ask for the missing coordinate.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google domain -> `google_domain`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- country-restricted results -> `cr`, formatted like `countryFR`
- language-restricted results -> `lr`, formatted like `lang_fr`
- named search origin -> `location`
- Google encoded location -> `uule`
- GPS coordinates -> `lat` and `lon`
- location bias radius in meters -> `radius`
- page number N -> `start: String((N - 1) * 10)`
- advanced image filters, size, color, type, rights, or date -> `tbs`
- safe search on/off -> `safe: "active"` or `safe: "off"`
- desktop/tablet/mobile -> `device`
- render JavaScript -> `render_js: "true"`
- bypass cache -> `no_cache: "true"`
- include AI Overview -> `ai_overview: "true"`


