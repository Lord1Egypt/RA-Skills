---
name: dataify-instagram-reels
description: Submit Dataify Instagram Reel Information Builder tasks for three Instagram Reel collection modes. Use when the user wants the Instagram Reel information collection tool, collect Instagram Reel information, scrape Instagram Reels, crawl Instagram Reel data, collect Instagram Reel information by detail URL, collect Instagram Reels by list URL, collect Instagram Reels by website URL, create Dataify ins_reel_by-url, ins_allreel_by-url, or ins_reel_by-listurl tasks, or asks in Chinese with meanings like "Instagram Reel 信息采集", "Instagram Reel 信息抓取", "Instagram Reels采集", "Instagram Reels抓取", "Instagram短视频采集", "Instagram短视频抓取", "Reel详情URL采集", "Reel列表URL采集", "Instagram Reel网址采集", or similar Instagram Reel noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Instagram Reels

Submit Instagram Reel information collection jobs through Dataify Builder. This skill is a guided wrapper for three collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| Detail URL | `ins_reel_by-url` | Collecting one or more Instagram Reels by Reel detail URL. |
| List URL | `ins_allreel_by-url` | Collecting Reels from an Instagram list/profile URL with count and date filters. |
| Website URL | `ins_reel_by-listurl` | Collecting Reels from an Instagram website/list URL with count and date filters. |

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

1. First ask the user to choose a collection mode: `detail-url`, `allreel-url`, or `listurl`.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple Instagram Reel groups for the selected mode.
5. Normalize the final values into a list of parameter objects for the selected mode only.
6. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
7. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
8. Validate the selected mode, Instagram URLs, numeric values, dates, and file name.
9. Submit the Builder request with the selected mode's `spider_id`.
10. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
11. Stop after Builder succeeds.
12. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect Reel information by detail URL | `detail-url` |
| Collect Reel information by list URL | `allreel-url` |
| Collect Reel information by website URL | `listurl` |

Ask: "Which collection mode do you want to use: `detail-url`, `allreel-url`, or `listurl`?"

Do not submit a Builder request until the mode is clear.

## Detail URL Mode Parameters

Use this section only when the user chooses `detail-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.instagram.com/reel/C5Rdyj_q7YN/` | `spider_parameters` | Instagram Reel detail URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Instagram Reel detail URL groups? If yes, provide multiple `url` values."

Detail URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.instagram.com/reel/C5Rdyj_q7YN/` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.instagram.com/`.
- Submit `spider_id=ins_reel_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.instagram.com/reel/C5Rdyj_q7YN/"}]
```

## List URL Mode Parameters

Use this section only when the user chooses `allreel-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.instagram.com/billieeilish` | `spider_parameters` | Instagram list/profile URL. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of Reels to collect. Must be an integer greater than or equal to `0`. |
| `posts_to_not_include` | No | `DP861NijuwE` | `spider_parameters` | Reel post IDs or PK values to exclude. Use English commas for multiple values. |
| `start_date` | No | `01-28-2025` | `spider_parameters` | Start date in `mm-dd-yyyy` format. Must be on or before `end_date`. |
| `end_date` | No | `01-28-2026` | `spider_parameters` | End date in `mm-dd-yyyy` format. Must be on or after `start_date`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Instagram Reel list URL groups? If yes, provide multiple groups with `url`, `num_of_posts`, `posts_to_not_include`, `start_date`, and `end_date`."

List URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.instagram.com/billieeilish` only after showing it in the parameter confirmation table.
- `url` must start with `https://www.instagram.com/`.
- `num_of_posts` must be an integer greater than or equal to `0`.
- `start_date` and `end_date` must use `mm-dd-yyyy` format.
- `start_date` must be on or before `end_date`.
- Submit `spider_id=ins_allreel_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.instagram.com/billieeilish","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]
```

## Website URL Mode Parameters

Use this section only when the user chooses `listurl`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.instagram.com/espn` | `spider_parameters` | Instagram website/list URL. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of Reels to collect. Must be an integer greater than or equal to `0`. |
| `posts_to_not_include` | No | `DP861NijuwE` | `spider_parameters` | Reel post IDs or PK values to exclude. Use English commas for multiple values. |
| `start_date` | No | `01-28-2025` | `spider_parameters` | Start date in `mm-dd-yyyy` format. Must be on or before `end_date`. |
| `end_date` | No | `01-28-2026` | `spider_parameters` | End date in `mm-dd-yyyy` format. Must be on or after `start_date`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Instagram Reel website URL groups? If yes, provide multiple groups with `url`, `num_of_posts`, `posts_to_not_include`, `start_date`, and `end_date`."

Website URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.instagram.com/espn` only after showing it in the parameter confirmation table.
- `url` must start with `https://www.instagram.com/`.
- `num_of_posts` must be an integer greater than or equal to `0`.
- `start_date` and `end_date` must use `mm-dd-yyyy` format.
- `start_date` must be on or before `end_date`.
- Submit `spider_id=ins_reel_by-listurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.instagram.com/espn","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]
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
  - `spider_name=instagram.com`
  - `spider_errors=true`
- Mode-specific field:
  - Detail URL mode: `spider_id=ins_reel_by-url`
  - List URL mode: `spider_id=ins_allreel_by-url`
  - Website URL mode: `spider_id=ins_reel_by-listurl`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array.

## Script

For stable execution, prefer `scripts/submit_dataify_instagram_reels.py` with Python 3.6 or newer instead of rewriting the Builder flow.

Detail URL mode:

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode detail-url --url "https://www.instagram.com/reel/C5Rdyj_q7YN/"
```

List URL mode:

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode allreel-url --url "https://www.instagram.com/billieeilish" --num-of-posts "10" --posts-to-not-include "DP861NijuwE" --start-date "01-28-2025" --end-date "01-28-2026"
```

Website URL mode:

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode listurl --url "https://www.instagram.com/espn" --num-of-posts "10" --posts-to-not-include "DP861NijuwE" --start-date "01-28-2025" --end-date "01-28-2026"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode detail-url --url "https://www.instagram.com/reel/C5Rdyj_q7YN/" --file-name "{{TasksID}}"
```

To submit multiple detail URL groups:

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode detail-url --params-json '[{"url":"https://www.instagram.com/reel/C5Rdyj_q7YN/"},{"url":"https://www.instagram.com/reel/C5Rdyj_q7YN/"}]'
```

To submit multiple list URL groups:

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode allreel-url --params-json '[{"url":"https://www.instagram.com/billieeilish","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"},{"url":"https://www.instagram.com/billieeilish","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]'
```

To submit multiple website URL groups:

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode listurl --params-json '[{"url":"https://www.instagram.com/espn","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"},{"url":"https://www.instagram.com/espn","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `detail-url`, `allreel-url`, or `listurl`.

`url cannot be empty` means the Instagram URL is missing.

`url must start with https://www.instagram.com/` means the URL is outside the allowed Instagram domain.

`num_of_posts must be an integer greater than or equal to 0` means the Reel count is invalid.

`start_date must use mm-dd-yyyy format` means the start date format is invalid.

`end_date must use mm-dd-yyyy format` means the end date format is invalid.

`start_date must be on or before end_date` means the date range is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or the selected mode's object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, selected `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not mix Detail URL, List URL, and Website URL mode parameters in the same Builder request.
- Do not submit a Builder request until the mode is clear.
- Do not put `file_name` inside `spider_parameters`.
- Do not use an Instagram URL from outside `https://www.instagram.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
