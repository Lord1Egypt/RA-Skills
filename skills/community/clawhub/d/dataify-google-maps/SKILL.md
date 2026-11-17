---
name: dataify-google-maps
description: "Search Google Maps to discover places, businesses, or map results. Do not use when a known URL, CID, or Place ID requires structured details or reviews."
---

# Dataify Google Maps

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill to turn a user's Google Maps request into a Dataify Scraper API form submission.
## Workflow

1. Parse the user's request into Google Maps fields. Set `engine` to the fixed value `google_maps`.
2. Apply documented defaults from parameter descriptions when the user does not specify a value. For this API, documented defaults are:
   - `engine`: `google_maps`
   - `json`: `1`
   - `google_domain`: `google.com`
   - `start`: `0`
   - `no_cache`: `false`

   Treat every other field as having no default unless the user supplies it. Never treat examples such as `United States`, `en`, `us`, `@40.7455096,-74.0083012,14z`, or `true` as defaults.

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

4.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
5. Build request parameters with only requested fields plus documented defaults. The script submits these parameters as form data, not a JSON request body.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_maps.py`.

```bash
python3 scripts/google_maps.py --q "coffee shops near Seattle" --json 1
```

For many fields, pass one JSON object with shell-appropriate quoting. The script will still submit form data to the API:

```bash
python3 scripts/google_maps.py --params-json '{"q":"coffee shops","json":"1","location":"Seattle","z":"14","gl":"us","hl":"en"}'
```

For natural-language parsing fallback, pass the user's request to `--request`:

```bash
python3 scripts/google_maps.py --request "搜索 Seattle 的咖啡店，返回 JSON，gl=us，hl=en"
```


## Field Mapping

Use `references/google_maps_api.md` when you need the exact field list, defaults, constraints, or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_maps`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request, except documented defaults from the parameter descriptions.
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

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_maps.py --q "coffee shops near Seattle" --json 1
```

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
