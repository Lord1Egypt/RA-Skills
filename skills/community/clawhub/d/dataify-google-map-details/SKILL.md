---
name: dataify-google-map-details
description: "Collect structured Google Maps place or business details from a known map URL, CID, location input, or Place ID. Do not use to discover nearby places or collect reviews."
---

# Dataify Google Map Details

Submit Google Maps detail collection jobs through Dataify Builder. This skill is a guided wrapper for four collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| URL | `google_map-details_by-url` | Collecting one or more Google Maps detail records by Google Maps URL. |
| CID | `google_map-details_by-cid` | Collecting one or more Google Maps detail records by CID. |
| Location | `google_map-details_by-location` | Collecting Google Maps detail records by keyword, country, latitude, longitude, and zoom level. |
| Place ID | `google_map-details_by-placeid` | Collecting one or more Google Maps detail records by place ID. |

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

1. First ask the user to choose a collection mode: `url`, `cid`, `location`, or `placeid`.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. For `location` mode, show the `country` dropdown options as a Markdown table with `Label` and `Value` columns. Use `references/google_countries.md`.
4. Ask whether the user wants to change any value before running the task.
5. Ask whether the user wants to collect multiple Google map detail groups for the selected mode.
6. Normalize the final values into a list of parameter objects for the selected mode only.
9. Validate the selected mode, URL, CID, place ID, keyword, country, numeric values, and file name.
10. Submit the Builder request with the selected mode's `spider_id`.
11. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
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

The script supports `--params-json` for multiple groups and prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name` and `message`.

## Troubleshooting

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
python3 scripts/submit_dataify_google_map_details.py --help
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
