---
name: dataify-google-map-details
description: Submit Dataify Google Map Details Builder tasks for four Google Maps detail collection modes. Use when the user wants the Google map details collection tool, collect Google Maps details, scrape Google Maps information, crawl Google map data, collect Google map details by URL, collect Google map details by CID, collect Google map details by location, collect Google map details by place_id, collect Google map business details, create Dataify google_map-details_by-url, google_map-details_by-cid, google_map-details_by-location, or google_map-details_by-placeid tasks, or asks in Chinese with meanings like "Google 地图信息采集", "Google 地图信息抓取", "Google地图详细信息采集", "Google地图详细信息抓取", "Google Maps 信息采集", "Google Maps 信息抓取", "谷歌地图信息采集", "谷歌地图信息抓取", "Google地图URL采集", "Google地图CID采集", "Google地图位置采集", "通过位置采集Google地图信息", "Google地图place_id采集", "Google地图place ID采集", "Google地图商家ID采集", or similar Google Maps details noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Google Map Details

Submit Google Maps detail collection jobs through Dataify Builder. This skill is a guided wrapper for four collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| URL | `google_map-details_by-url` | Collecting one or more Google Maps detail records by Google Maps URL. |
| CID | `google_map-details_by-cid` | Collecting one or more Google Maps detail records by CID. |
| Location | `google_map-details_by-location` | Collecting Google Maps detail records by keyword, country, latitude, longitude, and zoom level. |
| Place ID | `google_map-details_by-placeid` | Collecting one or more Google Maps detail records by place ID. |

After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

## API TOKEN Handling

Use `DATAIFY_API_TOKEN` as the long-term saved token name.

- If the user provides a token in the request, use it for this run.
- If no token is provided, first check whether `DATAIFY_API_TOKEN` is already saved locally in the environment.
- If `DATAIFY_API_TOKEN` is saved locally, use it without asking the user to re-enter the token.
- If no token is available locally, tell the user they need to provide a Dataify API TOKEN.
- If the user does not have an API TOKEN, tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one.
- If the user already has an API TOKEN, tell them it is available in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).
- After the user provides an API TOKEN and no local `DATAIFY_API_TOKEN` is saved, ask whether they want to save it locally as `DATAIFY_API_TOKEN` for future use.
- If the user wants to save it, give the appropriate command for their shell and ask them to run it; do not silently persist tokens without confirmation.
- Do not call the Builder endpoint without a token.
- Always call it `API TOKEN` in user-facing instructions. Prefer the environment variable name `DATAIFY_API_TOKEN` for saved local use.

PowerShell examples for saving the token for the current session:

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_DATAIFY_API_TOKEN"
```

For a persistent user-level variable on Windows:

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_DATAIFY_API_TOKEN", "User")
```

## Core Workflow

1. First ask the user to choose a collection mode: `url`, `cid`, `location`, or `placeid`.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. For `location` mode, show the `country` dropdown options as a Markdown table with `Label` and `Value` columns. Use `references/google_countries.md`.
4. Ask whether the user wants to change any value before running the task.
5. Ask whether the user wants to collect multiple Google map detail groups for the selected mode.
6. Normalize the final values into a list of parameter objects for the selected mode only.
7. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
8. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
9. Validate the selected mode, URL, CID, place ID, keyword, country, numeric values, and file name.
10. Submit the Builder request with the selected mode's `spider_id`.
11. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
12. Stop after Builder succeeds.
13. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect Google map details by URL | `url` |
| Collect Google map details by CID | `cid` |
| Collect Google map details by location | `location` |
| Collect Google map details by place ID | `placeid` |

Ask: "Which collection mode do you want to use: `url`, `cid`, `location`, or `placeid`?"

Do not submit a Builder request until the mode is clear.

## URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.google.com/maps/place/Pizza+Inn+Magdeburg/data=!4m7!3m6!1s0x47a5f50c083530a3:0xfdba8746b538141!8m2!3d52.1263086!4d11.6094743!16s%2Fg%2F11kqmtk3dt!19sChIJozA1CAz1pUcRQYFTa3So2w8?authuser=0&hl=en&rclk=1` | `spider_parameters` | Google Maps URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Ask whether the user wants to change any value, and whether they want multiple URL groups.

Submit `spider_id=google_map-details_by-url` and `spider_parameters` like:

```json
[{"url":"https://www.google.com/maps/place/Pizza+Inn+Magdeburg/data=!4m7!3m6!1s0x47a5f50c083530a3:0xfdba8746b538141!8m2!3d52.1263086!4d11.6094743!16s%2Fg%2F11kqmtk3dt!19sChIJozA1CAz1pUcRQYFTa3So2w8?authuser=0&hl=en&rclk=1"}]
```

## CID Mode Parameters

Use this section only when the user chooses `cid`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `CID` | Yes | `2476046430038551731` | `spider_parameters` | Google Maps CID. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Ask whether the user wants to change any value, and whether they want multiple CID groups.

Submit `spider_id=google_map-details_by-cid` and `spider_parameters` like:

```json
[{"CID":"2476046430038551731"}]
```

## Location Mode Parameters

Use this section only when the user chooses `location`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keyword` | Yes | `pizza` | `spider_parameters` | Google Maps search keyword. |
| `country` | Yes | `us` | `spider_parameters` | Google country. Show options using `references/google_countries.md`. |
| `lat` | No | `38` | `spider_parameters` | Latitude. Must be numeric. |
| `long` | No | `77` | `spider_parameters` | Longitude. Must be numeric. |
| `zoom_level` | No | `20` | `spider_parameters` | Zoom level. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the full `country` dropdown table from `references/google_countries.md`.

Ask whether the user wants to change any value, and whether they want multiple location groups.

Submit `spider_id=google_map-details_by-location` and `spider_parameters` like:

```json
[{"keyword":"pizza","country":"us","lat":"38","long":"77","zoom_level":"20"}]
```

## Place ID Mode Parameters

Use this section only when the user chooses `placeid`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `place_id` | Yes | `ChIJ3S-JXmauEmsRUcIaWtf4MzE` | `spider_parameters` | Google Maps place ID. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Ask whether the user wants to change any value, and whether they want multiple place ID groups.

Submit `spider_id=google_map-details_by-placeid` and `spider_parameters` like:

```json
[{"place_id":"ChIJ3S-JXmauEmsRUcIaWtf4MzE"}]
```

## Shared File Name Handling

- `file_name` defaults to `{{TasksID}}`.
- If the user changes `file_name`, submit the user-provided value.
- `file_name` cannot be empty.
- Send `file_name` as a Builder form field.

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=google.com`
  - `spider_errors=true`
- Mode-specific field:
  - URL mode: `spider_id=google_map-details_by-url`
  - CID mode: `spider_id=google_map-details_by-cid`
  - Location mode: `spider_id=google_map-details_by-location`
  - Place ID mode: `spider_id=google_map-details_by-placeid`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array.

## Script

For stable execution, prefer `scripts/submit_dataify_google_map_details.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_google_map_details.py" --mode location --keyword "pizza" --country "us" --lat "38" --long "77" --zoom-level "20"
```

The script supports `--params-json` for multiple groups and prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `url`, `cid`, `location`, or `placeid`.

`url must start with https://www.google.com/maps/` means the URL is outside the allowed Google Maps URL pattern.

`country must be one of the allowed Google country values` means the country dropdown value is invalid.

`zoom_level must be an integer greater than or equal to 0` means the zoom value is invalid.

`lat must be numeric` or `long must be numeric` means a coordinate is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

## Guardrails

- Do not mix URL, CID, Location, and Place ID mode parameters in the same Builder request.
- Do not submit a Builder request until the mode is clear.
- Do not put `file_name` inside `spider_parameters`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
