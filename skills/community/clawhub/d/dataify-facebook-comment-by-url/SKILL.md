---
name: dataify-facebook-comment-by-url
description: "Collect comments from a known Facebook post URL. Do not use for the post body, personal profiles, or events."
---

# Dataify Facebook Comment By URL

Submit Facebook post comment collection jobs through Dataify Builder by post URL. After submission, continue monitoring the returned `task_id` and return the final result by default.

## API TOKEN Handling

Use `DATAIFY_API_TOKEN` as the long-term saved token name.

- If `DATAIFY_API_TOKEN` is saved locally, use it without asking the user to re-enter the token.
- If the user does not have an API TOKEN, tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one.
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

2. For dropdown fields, show all allowed options as Markdown tables with both `Label` and `Value` columns.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple Facebook post comment groups. If yes, ask for multiple groups of `url`, `get_all_replies`, `limit_records`, and `comments_sort`.
5. Normalize the final values into a list of `spider_parameters` objects.
8. Validate URLs, dropdown values, numeric values, and file name.
9. Submit the Builder request with `spider_id=facebook_comment_by-comments-url`.
10. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
## Parameter Checklist


| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/share/p/1K6xfHFkrK/` | `spider_parameters` | Facebook post URL. |
| `get_all_replies` | No | `True` | `spider_parameters` | Dropdown-style parameter. Whether to collect all replies. |
| `limit_records` | No | `10` | `spider_parameters` | Integer greater than or equal to `0`. Maximum reply count. |
| `comments_sort` | No | `All comments` | `spider_parameters` | Dropdown-style parameter. Comment sorting mode. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Facebook post comment groups? If yes, provide multiple groups of `url`, `get_all_replies`, `limit_records`, and `comments_sort`."

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Dropdown Options

Show these dropdown options as Markdown tables with both `Label` and `Value` columns.

`get_all_replies` options:

| Label | Value |
| --- | --- |
| True | `True` |
| Flase | `Flase` |

`comments_sort` options:

| Label | Value |
| --- | --- |
| 最相关 | `Most Relevent` |
| 由新到旧 | `Newest` |
| 所有评论 | `All comments` |

## Parameter Handling

- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.facebook.com/`.
- `get_all_replies` defaults to `True`. Allowed values are `True` and `Flase`.
- `limit_records` defaults to `10`. It must be an integer greater than or equal to `0`.
- Submit numeric values as strings to match the Builder examples, for example `"limit_records":"10"`.
- `comments_sort` defaults to `All comments`. Allowed values are `Most Relevent`, `Newest`, and `All comments`.
- `file_name` defaults to `{{TasksID}}`. If the user changes it, submit the user-provided value.
- `file_name` cannot be empty.

Single-group example:

```json
spider_parameters=[{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"}]
```

Multi-group example:

```json
spider_parameters=[{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"},{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"}]
```

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=facebook.com`
  - `spider_id=facebook_comment_by-comments-url`
  - `spider_errors=true`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array of comment parameter objects.

## Script

For stable execution, prefer `scripts/submit_dataify_facebook_comment_by_url.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_facebook_comment_by_url.py" --url "https://www.facebook.com/share/p/1K6xfHFkrK/"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_facebook_comment_by_url.py" --url "https://www.facebook.com/share/p/1K6xfHFkrK/" --get-all-replies "True" --limit-records "10" --comments-sort "All comments" --file-name "{{TasksID}}"
```

To submit multiple groups:

```powershell
python3 ".\scripts\submit_dataify_facebook_comment_by_url.py" --params-json '[{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"},{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"}]'
```

The script prints a JSON summary with `spider_id`, `task_id`, `status`, `parameters`, `file_name` and `message`.

## Troubleshooting


`url cannot be empty` means the required Facebook post URL is missing.

`url must start with https://www.facebook.com/` means the URL is outside the allowed Facebook domain.

`Unsupported get_all_replies` means the value must be `True` or `Flase`.

`limit_records must be an integer greater than or equal to 0` means the reply count is invalid.

`Unsupported comments_sort` means the value must be `Most Relevent`, `Newest`, or `All comments`.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or one `spider_parameters` object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not put `file_name` inside `spider_parameters`.
- Do not use a Facebook URL from outside `https://www.facebook.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.

## Default completion behavior

The default deliverable is the collected result, not only a `task_id`.

1. Submit the Builder task once and capture its `task_id`.
2. Immediately continue with `$dataify-task-operations` and monitor the same task ID.
   - Use the default 600-second wait for ordinary collections.
   - Use `--timeout 1800` for media downloads or clearly high-volume, multi-page, or multi-input collections.
3. When the task succeeds, download and return the final JSON result. Summarize large payloads while preserving access to the raw result.
4. If monitoring times out or is interrupted, return the task ID and a resume command. Do not resubmit the paid task.
5. Stop after submission only when the user explicitly asks for submission only, a task ID, or `--no-wait` behavior.

## Quick Start

```bash
python3 scripts/submit_dataify_facebook_comment_by_url.py --help
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
