---
name: dataify-google-maps
description: When the user requests "call Google Maps" or "map search/location details", or explicitly mentions the map search field, the dataify-google-maps skill is triggered.
---

# Dataify Google Maps

Use this skill to turn a user's Google Maps request into a Dataify Scraper API form submission.

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

1. Parse the user's request into Google Maps fields. Set `engine` to the fixed value `google_maps`.
2. Apply documented defaults from parameter descriptions when the user does not specify a value. For this API, documented defaults are:
   - `engine`: `google_maps`
   - `json`: `1`
   - `google_domain`: `google.com`
   - `start`: `0`
   - `no_cache`: `false`

   Treat every other field as having no default unless the user supplies it. Never treat examples such as `United States`, `en`, `us`, `@40.7455096,-74.0083012,14z`, or `true` as defaults.
3. Before every real API call, show the user a complete request-parameter table and ask whether to modify anything. Do not show `Authorization` in the table. Do not call the API until the user confirms.

Use this exact table shape, including every body field:

```text
请确认是否要修改参数；你确认后我再调用接口。

| 参数名 | 当前值 | 默认值 | 说明 |
|---|---|---|---|
| `engine` | `google_maps` | `google_maps` | 固定引擎值。 |
| `q` | `<从用户需求解析出的值；无值则询问>` | 无 | Google Maps 搜索关键词。 |
| `json` | `<用户指定值或 1>` | `1` | 返回格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。 |
| `ll` | `<用户指定值或空>` | 无 | 完整地图坐标起点，格式为 `@纬度,经度,缩放z` 或 `@纬度,经度,高度m`。不能和 `location`、`lat`、`lon`、`z`、`m` 同用。 |
| `location` | `<用户指定值或空>` | 无 | 文字地点起点；需配合 `z` 或 `m`。不能和 `ll`、`lat`、`lon` 同用。 |
| `lat` | `<用户指定值或空>` | 无 | 搜索起点纬度；必须和 `lon` 成对使用，并配合 `z` 或 `m`。 |
| `lon` | `<用户指定值或空>` | 无 | 搜索起点经度；必须和 `lat` 成对使用，并配合 `z` 或 `m`。 |
| `z` | `<用户指定值或空>` | 无 | 地图缩放级别；不能和 `m` 同用。 |
| `m` | `<用户指定值或空>` | 无 | 地图高度，单位米；不能和 `z` 同用。 |
| `nearby` | `<用户指定值或空>` | 无 | 是否强制返回更接近指定起点的结果；应与 `ll`、`location` 或 `lat`/`lon` 一起使用。 |
| `google_domain` | `<用户指定值或 google.com>` | `google.com` | Google 域名。 |
| `hl` | `<用户指定值或空>` | 无 | Google Maps 搜索语言代码。 |
| `gl` | `<用户指定值或空>` | 无 | Google Maps 搜索国家/地区代码。 |
| `start` | `<用户指定值或 0>` | `0` | 分页偏移量。 |
| `type` | `<用户指定值或空>` | 无 | 搜索类型：`search` 或 `place`。 |
| `data` | `<用户指定值或空>` | 无 | 已废弃的结果过滤参数，优先使用 `place_id` 或 `data_cid`。 |
| `place_id` | `<用户指定值或空>` | 无 | Google Maps 地点唯一 ID。 |
| `data_cid` | `<用户指定值或空>` | 无 | Google Maps CID，不能和 `place_id` 同用。 |
| `no_cache` | `<用户指定值或 false>` | `false` | 是否跳过缓存；`true` 跳过缓存，`false` 使用缓存。 |
```

If the user asks to modify parameters, update the current values and show the full table again. Call the API only after a clear confirmation such as "确认", "可以", "调用", "继续", "yes", or equivalent.
4.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
5. Build request parameters with only requested fields plus documented defaults. The script submits these parameters as form data, not a JSON request body.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_maps.py`.

```bash
python3 scripts/google_maps.py --q "coffee shops near Seattle" --json 1
```

If the user provided a token in the conversation instead of an environment variable, pass it with `--token` and avoid echoing it back in the final answer:

```bash
python3 scripts/google_maps.py --token "USER_TOKEN" --q "coffee shops near Seattle" --gl us --hl en
```

For many fields, pass one JSON object with shell-appropriate quoting. The script will still submit form data to the API:

```bash
python3 scripts/google_maps.py --params-json '{"q":"coffee shops","json":"1","location":"Seattle","z":"14","gl":"us","hl":"en"}'
```

For natural-language parsing fallback, pass the user's request to `--request`:

```bash
python3 scripts/google_maps.py --request "搜索 Seattle 的咖啡店，返回 JSON，gl=us，hl=en"
```

7. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_maps_api.md` when you need the exact field list, defaults, constraints, or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_maps`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request, except documented defaults from the parameter descriptions.
- Before each real API call, show the complete body-parameter table (`engine` through `no_cache`), omit `Authorization`, and wait for user confirmation.
- Ask a follow-up only when required `q` or a required paired parameter cannot be inferred.
- Use `ll` by itself for a full Google Maps coordinate string such as `@lat,lon,14z` or `@lat,lon,10410m`; do not combine it with `location`, `lat`, `lon`, `z`, or `m`.
- Use `lat` and `lon` together. If only one is available, ask for the missing coordinate.
- Use either `z` or `m`, not both. When using `location` or `lat`/`lon`, include one of `z` or `m` if the user supplied a search origin.
- Use `nearby` only with `ll`, `location`, or `lat`/`lon`. For "near me" requests without a location anchor, ask the user for a Maps origin.
- Do not use `place_id` and `data_cid` together.
- Prefer `place_id` or `data_cid` over the deprecated `data` field.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google domain -> `google_domain`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- page number N -> `start: String((N - 1) * 20)`
- a full Maps coordinate string -> `ll`
- named search origin -> `location`
- GPS coordinates -> `lat` and `lon`
- zoom level -> `z`
- map height in meters -> `m`
- force closer results / "near me" with an origin -> `nearby: "true"`
- result list search -> `type: "search"`
- place details -> `type: "place"` when using `data`; omit `type` when using `place_id` or `data_cid` unless the user explicitly requests it
- Google Maps place identifier -> `place_id`
- Google Maps CID -> `data_cid`
- bypass cache -> `no_cache: "true"`


