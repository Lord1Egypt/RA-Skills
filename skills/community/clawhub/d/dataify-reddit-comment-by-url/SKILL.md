---
name: dataify-reddit-comment-by-url
description: Submit Dataify Reddit Post Comment by URL Builder tasks. Use when the user wants the Reddit post comment collection tool, collect Reddit post comments, scrape Reddit post comments, crawl Reddit comment data, collect Reddit comments by URL, create a Dataify reddit_comment_by-url task, or asks in Chinese with meanings like "Reddit 帖子评论采集", "Reddit 帖子评论抓取", "Reddit评论采集", "Reddit评论抓取", "Reddit帖子URL评论采集", or similar Reddit post comment noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Reddit Comment By URL

Submit Reddit post comment collection jobs through Dataify Builder by Reddit URL. After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

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
3. Ask whether the user wants to collect multiple Reddit comment groups. If yes, ask for multiple groups with `url`, `days_back`, and `comment_limit`.
4. Normalize the final values into a list of `spider_parameters` objects.
5. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
6. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
7. Validate the Reddit URL, numeric values, and file name.
8. Submit the Builder request with `spider_id=reddit_comment_by-url`.
9. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
10. Stop after Builder succeeds.
11. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Parameter Checklist

When the user invokes this skill, first tell them these values are used. Always display submitted parameters as a Markdown table; do not use a plain sentence or bullet list for the parameter confirmation.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button` | `spider_parameters` | Reddit URL. |
| `days_back` | No | `10` | `spider_parameters` | Number of days back for collecting comments. Must be an integer greater than or equal to `0`. |
| `comment_limit` | No | `5` | `spider_parameters` | Reply comment limit. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Reddit comment groups? If yes, provide multiple groups with `url`, `days_back`, and `comment_limit`."

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Parameter Handling

- `url` is required. If the user does not provide it, use the default `https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.reddit.com/`.
- `days_back` must be an integer greater than or equal to `0`.
- `comment_limit` must be an integer greater than or equal to `0`.
- Multiple collection groups repeat `url`, `days_back`, and `comment_limit` inside `spider_parameters`.
- `file_name` defaults to `{{TasksID}}`. If the user changes it, submit the user-provided value.
- `file_name` cannot be empty.

Single-group example:

```json
spider_parameters=[{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"}]
```

Multi-group example:

```json
spider_parameters=[{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"},{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"}]
```

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=reddit.com`
  - `spider_id=reddit_comment_by-url`
  - `spider_errors=true`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array of Reddit comment objects.

## Script

For stable execution, prefer `scripts/submit_dataify_reddit_comment_by_url.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_reddit_comment_by_url.py" --url "https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button" --days-back "10" --comment-limit "5"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_reddit_comment_by_url.py" --api-token "YOUR_DATAIFY_API_TOKEN" --url "https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button" --file-name "{{TasksID}}"
```

To submit multiple Reddit comment groups:

```powershell
python3 ".\scripts\submit_dataify_reddit_comment_by_url.py" --params-json '[{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"},{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"}]'
```

The script prints a JSON summary with `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`url cannot be empty` means the Reddit URL is missing.

`url must start with https://www.reddit.com/` means the URL is outside the allowed Reddit domain.

`days_back must be an integer greater than or equal to 0` means the day limit is invalid.

`comment_limit must be an integer greater than or equal to 0` means the reply comment limit is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or one `spider_parameters` object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not put `file_name` inside `spider_parameters`.
- Do not use a Reddit URL from outside `https://www.reddit.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
