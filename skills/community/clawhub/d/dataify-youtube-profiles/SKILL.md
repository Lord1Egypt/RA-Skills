---
name: dataify-youtube-profiles
description: Use for Dataify YouTube profile collection Builder tasks. Trigger when the user asks for the YouTube profile collection tool, YouTube profiles collection, YouTube channel profile collection, YouTube profile scraping, YouTube profiles by URL, YouTube profiles by keyword, or a choice between youtube_profiles_by-url and youtube_profiles_by-keyword. Also trigger for Chinese wording such as "YouTube个人资料采集", "YouTube个人资料抓取", "YouTube频道资料采集", "YouTube频道资料抓取", "YouTube个人主页采集", "YouTube个人主页抓取", "通过URL采集YouTube个人资料", "通过URL抓取YouTube个人资料", "通过关键词采集YouTube个人资料", "通过关键词抓取YouTube个人资料", or similar YouTube profile noun plus collection/scraping action wording. Supports returning the task_id and status; configuring or reusing the DATAIFY_API_TOKEN environment variable; and troubleshooting Dataify Builder request failures.
---

# Dataify YouTube Profiles

Submit YouTube profile collection jobs through Dataify Builder, then stop. This skill is a guided wrapper for two collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| URL | `youtube_profiles_by-url` | Collecting one or more specific YouTube channel profile URLs. |
| Keyword | `youtube_profiles_by-keyword` | Searching YouTube channel profiles by keyword and page count. |

After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

## API TOKEN Handling

Use `DATAIFY_API_TOKEN` as the long-term saved token name.

- If the user provides a token in the request, use it for this run.
- If no token is provided, first check whether `DATAIFY_API_TOKEN` is already saved locally in the environment.
- If `DATAIFY_API_TOKEN` is saved locally, use it.
- If no token is available locally, tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).
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

1. First ask the user to choose a collection mode: URL or Keyword. Show the Mode Selection table.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple YouTube profile groups for the selected mode.
5. Normalize the final values into a list of parameter objects for the selected mode only.
6. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
7. If no token is available, tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).
8. Validate the selected mode, parameters, and file name.
9. Submit the Builder request with the selected mode's `spider_id`.
10. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
11. Stop after Builder succeeds.
12. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect profiles by URL | `url` |
| Collect profiles by keyword | `keyword` |

Ask: "Which collection mode do you want to use: `url` or `keyword`?"

Do not submit a Builder request until the mode is clear.

## URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/@mrbeast` | YouTube channel URL. The URL must use the `https://www.youtube.com` domain. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple YouTube profile URL groups? If yes, provide multiple `url` values."

URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.youtube.com/@mrbeast` only after showing it in the parameter confirmation table.
- Accept only URLs whose scheme and host are exactly `https://www.youtube.com`. Reject any other scheme, host, or subdomain as non-compliant.
- Submit `spider_id=youtube_profiles_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.youtube.com/@mrbeast"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keyword`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `MrBeast` | Keyword used to search YouTube channels or profiles. |
| `page_turning` | Yes | `1` | Integer greater than or equal to `0`. Specifies how many search result pages to collect. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple YouTube profile keyword groups? If yes, provide multiple groups of `keyword` and `page_turning`."

Keyword mode handling:

- `keyword` is required. If the user does not provide it, use the default `MrBeast` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `keyword`.
- `keyword` cannot be empty.
- `page_turning` is required. Default: `1`. It must be an integer greater than or equal to `0`.
- Submit numeric values as strings to match the Builder examples, for example `"page_turning":"1"`.
- Submit `spider_id=youtube_profiles_by-keyword`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keyword":"MrBeast","page_turning":"1"}]
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
  - `spider_name=youtube.com`
  - `spider_errors=true`
- Mode-specific field:
  - URL mode: `spider_id=youtube_profiles_by-url`
  - Keyword mode: `spider_id=youtube_profiles_by-keyword`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string, not a raw object.

## Script

For stable execution, prefer `scripts/submit_dataify_youtube_profiles.py` with Python 3.6 or newer instead of rewriting the Builder flow.

URL mode:

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode url --url "https://www.youtube.com/@mrbeast"
```

Keyword mode:

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode keyword --keyword "MrBeast" --page-turning 1
```

If `python3` is not available, use the local Python 3 command for that machine, such as `python`. The script checks the runtime version and tells the user to use Python 3.6 or newer if the active interpreter is too old.

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode url --url "https://www.youtube.com/@mrbeast" --file-name "{{TasksID}}"
```

To submit multiple URL groups:

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode url --params-json '[{"url":"https://www.youtube.com/@mrbeast"},{"url":"https://www.youtube.com/@YouTube"}]'
```

To submit multiple keyword groups:

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode keyword --params-json '[{"keyword":"MrBeast","page_turning":"1"},{"keyword":"cooking","page_turning":"2"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `url` or `keyword`.

`URL must use https://www.youtube.com` means the URL is non-compliant. Ask the user for a URL that starts with `https://www.youtube.com`, such as `https://www.youtube.com/@mrbeast`.

`keyword cannot be empty` means the keyword is missing.

`page_turning must be an integer greater than or equal to 0` means the requested page count is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string, or the selected mode's object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, or selected `spider_id` is wrong.

## Guardrails

- Do not mix URL mode and Keyword mode parameters in the same Builder request.
- Do not send `keyword` or `page_turning` in URL mode.
- Do not send `url` in Keyword mode.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
