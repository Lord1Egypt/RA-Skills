---
name: dataify-youtube-comment-by-id
description: Submit Dataify YouTube Comment by Video ID Builder tasks for collecting YouTube comment information. Use when the user wants the YouTube comment collection tool, collect YouTube comments, scrape YouTube comments, crawl YouTube comments, fetch YouTube comment information, extract YouTube comment data, collect comments by video ID, scrape comments by video ID, create a Dataify youtube_comment_by-id task, or asks in Chinese with meanings like "YouTube评论信息采集", "YouTube评论信息抓取", "YouTube评论采集", "YouTube评论抓取", or similar noun plus action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting Dataify Builder requests.
---

# Dataify YouTube Comment By ID

Submit YouTube comment collection jobs through Dataify Builder by video ID. After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

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

1. Before submitting, show the user the required values, optional values, and defaults listed in the Parameter Checklist.
2. Ask whether the user wants to change any value before running the task.
3. Ask whether the user wants to collect multiple YouTube comment groups. If yes, ask for multiple `video_id`, `load_replies`, and `num_of_comments` groups.
4. Normalize the final values into a list of parameter objects.
5. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
6. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
7. Validate each video ID, numeric value, and file name.
8. Submit a Builder request to create the task.
9. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
10. Stop after Builder succeeds.
11. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Parameter Checklist

When the user invokes this skill, first tell them these values are used. Always display submitted parameters as a Markdown table; do not use a plain sentence or bullet list for the parameter confirmation.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `video_id` | Yes | `8RePenzQH80` | Unique YouTube video ID used to identify the video whose comments should be collected. |
| `load_replies` | Yes | `10` | Integer greater than or equal to `0`. Time used when loading replies on the page. |
| `num_of_comments` | Yes | `10` | Integer greater than or equal to `0`. Number of comments to collect. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple YouTube comment groups? If yes, provide multiple groups of `video_id`, `load_replies`, and `num_of_comments`."

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

If any dropdown-style field is added in the future, show all allowed options as a Markdown table with both `Label` and `Value` columns before asking the user to choose.

## Parameter Handling

- `video_id` is required. If the user does not provide it, use the default `8RePenzQH80` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `video_id`.
- `video_id` cannot be empty.
- `load_replies` is required. Default: `10`. It must be an integer greater than or equal to `0`.
- `num_of_comments` is required. Default: `10`. It must be an integer greater than or equal to `0`.
- `file_name` defaults to `{{TasksID}}`. If the user changes it, submit the user-provided value.
- `file_name` cannot be empty.
- Submit numeric values as strings to match the Builder examples, for example `"load_replies":"10"` and `"num_of_comments":"10"`.
- Submit `spider_parameters` as a JSON string containing an array of one or more objects.

Single-group example:

```json
[{"video_id":"8RePenzQH80","load_replies":"10","num_of_comments":"10"}]
```

Multi-group example:

```json
[{"video_id":"8RePenzQH80","load_replies":"10","num_of_comments":"10"},{"video_id":"dQw4w9WgXcQ","load_replies":"10","num_of_comments":"20"}]
```

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=youtube.com`
  - `spider_id=youtube_comment_by-id`
  - `spider_errors=true`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string, not a raw object.

## Script

For stable execution, prefer `scripts/submit_dataify_youtube_comment_by_id.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --video-id "8RePenzQH80"
```

If `python3` is not available, use the local Python 3 command for that machine, such as `python`. The script checks the runtime version and tells the user to use Python 3.6 or newer if the active interpreter is too old.

To override the saved environment token or default parameters for one run:

```powershell
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --api-token "YOUR_DATAIFY_API_TOKEN" --video-id "8RePenzQH80" --load-replies 10 --num-of-comments 10 --file-name "{{TasksID}}"
```

To submit multiple groups, pass a JSON array:

```powershell
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --params-json '[{"video_id":"8RePenzQH80","load_replies":"10","num_of_comments":"10"},{"video_id":"dQw4w9WgXcQ","load_replies":"10","num_of_comments":"20"}]'
```

The script prints a JSON summary with `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`video_id cannot be empty` means the required YouTube video ID is missing.

`load_replies must be an integer greater than or equal to 0` means the requested reply loading value is invalid.

`num_of_comments must be an integer greater than or equal to 0` means the requested comment count is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string, or one object is missing `video_id`, `load_replies`, or `num_of_comments`.

Missing `task_id` usually means the authorization header, token, `spider_name`, or `spider_id` is wrong.

## Guardrails

- Do not poll for results after Builder succeeds.
- Stop after Builder succeeds.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not claim the Builder response contains YouTube comment results.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
