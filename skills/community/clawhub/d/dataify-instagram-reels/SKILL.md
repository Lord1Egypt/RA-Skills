---
name: dataify-instagram-reels
description: "Collect Instagram Reel records from a Reel URL, Reel-list URL, or website URL. Do not use for profile data, post comments, or Google Shopping products."
---

# Dataify Instagram Reels

Submit Instagram Reel information collection jobs through Dataify Builder. This skill is a guided wrapper for three collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| Detail URL | `ins_reel_by-url` | Collecting one or more Instagram Reels by Reel detail URL. |
| List URL | `ins_allreel_by-url` | Collecting Reels from an Instagram list/profile URL with count and date filters. |
| Website URL | `ins_reel_by-listurl` | Collecting Reels from an Instagram website/list URL with count and date filters. |

After submission, continue monitoring the returned `task_id` and return the final result by default.

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

1. First ask the user to choose a collection mode: `detail-url`, `allreel-url`, or `listurl`.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple Instagram Reel groups for the selected mode.
5. Normalize the final values into a list of parameter objects for the selected mode only.
8. Validate the selected mode, Instagram URLs, numeric values, dates, and file name.
9. Submit the Builder request with the selected mode's `spider_id`.
10. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect Reel information by detail URL | `detail-url` |
| Collect Reel information by list URL | `allreel-url` |
| Collect Reel information by website URL | `listurl` |

Ask: "Which collection mode do you want to use: `detail-url`, `allreel-url`, or `listurl`?"

Do not submit a Builder request until the mode is clear.

## Shared File Name Handling

- `file_name` defaults to `{{TasksID}}`.
- If the user changes `file_name`, submit the user-provided value.
- `file_name` cannot be empty.
- Send `file_name` as a Builder form field.

For detailed mode schemas and advanced fields, read [references/modes-and-parameters.md](references/modes-and-parameters.md) only when needed.

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
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode detail-url --url "https://www.instagram.com/reel/C5Rdyj_q7YN/" --file-name "{{TasksID}}"
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

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name` and `message`.

## Troubleshooting

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
python3 scripts/submit_dataify_instagram_reels.py --help
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
