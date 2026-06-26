---
name: dataify-youtube-product-by-id
description: Submit Dataify YouTube Video Basic Information by Video ID Builder tasks. Use when the user wants the YouTube video basic information collection tool, collect YouTube video information, scrape YouTube video information, crawl YouTube video details, fetch YouTube video basic data, collect video info by video ID, create a Dataify youtube_product_by-id task, or asks in Chinese with meanings like "YouTube视频基本信息采集", "YouTube视频基本信息抓取", "YouTube视频信息采集", "YouTube视频信息抓取", "YouTube视频详情采集", "YouTube视频详情抓取", "视频基本信息采集", "视频基本信息抓取", "视频信息采集", "视频信息抓取", or similar noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify YouTube Product By ID

Submit YouTube video basic information collection jobs through Dataify Builder by video ID. After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

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

1. Before submitting, show the user the required values, shared values, optional values, and defaults listed in the Parameter Checklist.
2. For dropdown fields, show all allowed options as Markdown tables with both `Label` and `Value` columns. Use `scripts/submit_dataify_youtube_product_by_id.py --list-options` to print the full dropdown tables.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple YouTube video basic information records. If yes, ask for multiple `video_id` values.
5. Normalize the final `video_id` values into a list of `spider_parameters` objects.
6. Normalize `subtitles_language`, `subtitles_type`, and `selected_only` into one shared `spider_universal` object.
7. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
8. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
9. Validate each video ID, dropdown value, and file name.
10. Submit a Builder request to create the task.
11. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
12. Stop after Builder succeeds.
13. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Parameter Checklist

When the user invokes this skill, first tell them these values are used. Always display submitted parameters as a Markdown table; do not use a plain sentence or bullet list for the parameter confirmation.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `video_id` | Yes | `8RePenzQH80` | `spider_parameters` | Unique YouTube video ID used to identify the video whose basic information should be collected. |
| `subtitles_language` | No | `ab` | `spider_universal` | Dropdown-style shared parameter. Subtitle language. |
| `subtitles_type` | No | `auto_generated` | `spider_universal` | Dropdown-style shared parameter. Subtitle type. |
| `selected_only` | No | `false` | `spider_universal` | Dropdown-style shared parameter. Whether to use only selected specifications. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple YouTube video basic information records? If yes, provide multiple `video_id` values."

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Dropdown Options

Before asking the user to choose dropdown values, show all allowed options as Markdown tables with both `Label` and `Value` columns.

Use this command to print the complete tables:

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --list-options
```

If `python3` is not available, use the local Python 3 command for that machine, such as `python`.

The script prints:

- `subtitles_language` options, using the supplied `cn` value as `Label` and `typeValue` as `Value`.
- `subtitles_type` options.
- `selected_only` options.

## Parameter Handling

- `video_id` is required. If the user does not provide it, use the default `8RePenzQH80` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `video_id`.
- `video_id` cannot be empty.
- Multiple collection groups only repeat `video_id` inside `spider_parameters`.
- `subtitles_language`, `subtitles_type`, and `selected_only` are shared parameters. Send them in `spider_universal`, not inside each `spider_parameters` object.
- `subtitles_language` defaults to `ab`.
- `subtitles_type` defaults to `auto_generated`.
- `selected_only` defaults to `false`.
- `file_name` defaults to `{{TasksID}}`. If the user changes it, submit the user-provided value.
- `file_name` cannot be empty.

Single-group example:

```json
spider_parameters=[{"video_id":"8RePenzQH80"}]
spider_universal={"subtitles_language":"ab","subtitles_type":"auto_generated","selected_only":"false"}
```

Multi-group example:

```json
spider_parameters=[{"video_id":"8RePenzQH80"},{"video_id":"dQw4w9WgXcQ"}]
spider_universal={"subtitles_language":"ab","subtitles_type":"auto_generated","selected_only":"false"}
```

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=youtube.com`
  - `spider_id=youtube_product_by-id`
  - `spider_errors=true`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic fields:
  - `spider_parameters` must be a JSON string array of video ID objects.
  - `spider_universal` must be a JSON string object containing shared subtitle settings.

## Script

For stable execution, prefer `scripts/submit_dataify_youtube_product_by_id.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --video-id "8RePenzQH80"
```

To override the saved environment token or default shared parameters for one run:

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --api-token "YOUR_DATAIFY_API_TOKEN" --video-id "8RePenzQH80" --subtitles-language "ab" --subtitles-type "auto_generated" --selected-only "false" --file-name "{{TasksID}}"
```

To submit multiple video IDs:

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --params-json '[{"video_id":"8RePenzQH80"},{"video_id":"dQw4w9WgXcQ"}]'
```

The script prints a JSON summary with `task_id`, `status`, `parameters`, `spider_universal`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`video_id cannot be empty` means the required YouTube video ID is missing.

`Unsupported subtitles_language` means the value must be one of the allowed subtitle language codes.

`Unsupported subtitles_type` means the value must be `auto_generated` or `uploader_provided`.

`Unsupported selected_only` means the value must be `false` or `true`.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, `spider_universal` was not a JSON string object, or one `spider_parameters` object is missing `video_id`.

Missing `task_id` usually means the authorization header, token, `spider_name`, `spider_id`, `spider_parameters`, or `spider_universal` is wrong.

## Guardrails

- Do not put `subtitles_language`, `subtitles_type`, or `selected_only` inside `spider_parameters`.
- Do not omit `spider_universal`.
- Do not poll for results after Builder succeeds.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not claim the Builder response contains YouTube video data files.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
