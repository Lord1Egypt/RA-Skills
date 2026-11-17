---
name: dataify-youtube-comment-by-id
description: "Collect YouTube comments for a known video ID. Do not use for video metadata, transcripts, media downloads, or keyword discovery."
---

# Dataify YouTube Comment By ID

Submit YouTube comment collection jobs through Dataify Builder by video ID. After submission, continue monitoring the returned `task_id` and return the final result by default.

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

2. Ask whether the user wants to change any value before running the task.
3. Ask whether the user wants to collect multiple YouTube comment groups. If yes, ask for multiple `video_id`, `load_replies`, and `num_of_comments` groups.
4. Normalize the final values into a list of parameter objects.
7. Validate each video ID, numeric value, and file name.
8. Submit a Builder request to create the task.
9. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
## Parameter Checklist


| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `video_id` | Yes | `8RePenzQH80` | Unique YouTube video ID used to identify the video whose comments should be collected. |
| `load_replies` | Yes | `10` | Integer greater than or equal to `0`. Time used when loading replies on the page. |
| `num_of_comments` | Yes | `10` | Integer greater than or equal to `0`. Number of comments to collect. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple YouTube comment groups? If yes, provide multiple groups of `video_id`, `load_replies`, and `num_of_comments`."

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.


## Parameter Handling

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
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --video-id "8RePenzQH80" --load-replies 10 --num-of-comments 10 --file-name "{{TasksID}}"
```

To submit multiple groups, pass a JSON array:

```powershell
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --params-json '[{"video_id":"8RePenzQH80","load_replies":"10","num_of_comments":"10"},{"video_id":"dQw4w9WgXcQ","load_replies":"10","num_of_comments":"20"}]'
```

The script prints a JSON summary with `task_id`, `status`, `parameters`, `file_name` and `message`.

## Troubleshooting


`video_id cannot be empty` means the required YouTube video ID is missing.

`load_replies must be an integer greater than or equal to 0` means the requested reply loading value is invalid.

`num_of_comments must be an integer greater than or equal to 0` means the requested comment count is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string, or one object is missing `video_id`, `load_replies`, or `num_of_comments`.

Missing `task_id` usually means the authorization header, token, `spider_name`, or `spider_id` is wrong.

## Guardrails

- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not claim the Builder response contains YouTube comment results.
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
python3 scripts/submit_dataify_youtube_comment_by_id.py --help
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
