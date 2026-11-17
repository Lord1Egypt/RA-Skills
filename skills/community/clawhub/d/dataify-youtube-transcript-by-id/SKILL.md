---
name: dataify-youtube-transcript-by-id
description: "Collect subtitles, captions, or transcript text for a known YouTube video ID. Do not use for video or audio files, metadata, comments, or video discovery."
---

# Dataify YouTube Transcript By ID

Submit YouTube subtitle/transcript collection jobs through Dataify Builder by video ID. After submission, continue monitoring the returned `task_id` and return the final result by default.

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

2. For dropdown fields, show all allowed options as Markdown tables with both `Label` and `Value` columns. Use `scripts/submit_dataify_youtube_transcript_by_id.py --list-options` to print the full dropdown tables.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple YouTube transcript groups. If yes, ask for multiple `video_id` values.
5. Normalize the final `video_id` values into a list of `spider_parameters` objects.
6. Normalize `subtitles_language`, `subtitles_type`, and `selected_only` into one shared `spider_universal` object.
9. Validate each video ID, dropdown value, and file name.
10. Submit a Builder request to create the task.
11. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
## Parameter Checklist


| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `video_id` | Yes | `8RePenzQH80` | `spider_parameters` | Unique YouTube video ID used to identify the video whose subtitles should be collected. |
| `subtitles_language` | No | `ab` | `spider_universal` | Dropdown-style shared parameter. Subtitle language. |
| `subtitles_type` | No | `auto_generated` | `spider_universal` | Dropdown-style shared parameter. Subtitle type. |
| `selected_only` | No | `false` | `spider_universal` | Dropdown-style shared parameter. Whether to use only selected specifications. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple YouTube transcript groups? If yes, provide multiple `video_id` values."

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Dropdown Options

Before asking the user to choose dropdown values, show all allowed options as Markdown tables with both `Label` and `Value` columns.

Use this command to print the complete tables:

```powershell
python3 ".\scripts\submit_dataify_youtube_transcript_by_id.py" --list-options
```

If `python3` is not available, use the local Python 3 command for that machine, such as `python`.

The script prints:

- `subtitles_language` options, using the supplied `cn` value as `Label` and `typeValue` as `Value`.
- `subtitles_type` options.
- `selected_only` options.

## Parameter Handling

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
  - `spider_id=youtube_transcript_by-id`
  - `spider_errors=true`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic fields:
  - `spider_parameters` must be a JSON string array of video ID objects.
  - `spider_universal` must be a JSON string object containing shared subtitle settings.

## Script

For stable execution, prefer `scripts/submit_dataify_youtube_transcript_by_id.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_youtube_transcript_by_id.py" --video-id "8RePenzQH80"
```

To override the saved environment token or default shared parameters for one run:

```powershell
python3 ".\scripts\submit_dataify_youtube_transcript_by_id.py" --video-id "8RePenzQH80" --subtitles-language "ab" --subtitles-type "auto_generated" --selected-only "false" --file-name "{{TasksID}}"
```

To submit multiple video IDs:

```powershell
python3 ".\scripts\submit_dataify_youtube_transcript_by_id.py" --params-json '[{"video_id":"8RePenzQH80"},{"video_id":"dQw4w9WgXcQ"}]'
```

The script prints a JSON summary with `task_id`, `status`, `parameters`, `spider_universal`, `file_name` and `message`.

## Troubleshooting


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
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not claim the Builder response contains YouTube transcript files.
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
python3 scripts/submit_dataify_youtube_transcript_by_id.py --help
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
