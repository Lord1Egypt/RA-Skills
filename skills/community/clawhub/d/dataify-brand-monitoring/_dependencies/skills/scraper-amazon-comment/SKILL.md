---
name: dataify-amazon-comment
description: "Collect Amazon product reviews from one or more known product URLs. Use for Amazon review or comment extraction. Do not use for product details, product lists, or seller profiles."
---

# Dataify Amazon Comment

Submit Amazon product review collection jobs by URL through Dataify Builder and continue through final-result retrieval. After submission, continue monitoring the returned `task_id` and return the final result by default.


## Quick Start

**Input:** an Amazon product URL.

```bash
python3 scripts/submit_amazon_comment.py --url "https://www.amazon.com/dp/B0BZYCJK89"
```

The command waits up to 10 minutes and prints the final JSON result. Add `--no-wait` only for submission-only behavior.

If `DATAIFY_API_TOKEN` is missing, log in or register at https://dashboard.dataify.com/login?utm_source=skill. New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed.

## API TOKEN Handling

Use `DATAIFY_API_TOKEN` as the long-term saved token name.

- If `DATAIFY_API_TOKEN` is saved locally, use it.
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

3. Ask: "Do you want to change any of these values before I submit the task?"
4. Normalize the final values into `url` and `file_name`.
7. Validate the URL and file name.
8. Submit a Builder request to create the task.
9. Read `data.task_id` from the Builder response.

## Parameter Checklist

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.amazon.com/HISDERN-Checkered-Handkerchief-Classic-Necktie/dp/B0BRXPR726` | Amazon product URL whose reviews should be collected. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=amazon.com`
  - `spider_id=amazon_comment_by-url`
  - `spider_errors=true`
- Dynamic fields:
  - `spider_parameters` must be a JSON string, not a raw object.
  - `file_name` defaults to `{{TasksID}}` and can be changed by the user.

## Script

For stable execution, prefer `scripts/submit_amazon_comment.py` with Python 3.6 or newer instead of rewriting the Builder flow. The script writes and reads UTF-8 text.

```powershell
python3 ".\scripts\submit_amazon_comment.py"
python3 ".\scripts\submit_amazon_comment.py" --url "https://www.amazon.com/HISDERN-Checkered-Handkerchief-Classic-Necktie/dp/B0BRXPR726" --file-name "amazon-comments"
```

The script prints a JSON summary with `task_id`, `url`, `file_name` and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means `DATAIFY_API_TOKEN` is not set in the environment. Tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).

`URL cannot be empty` means no usable product URL was provided.

`File name cannot be empty` means no usable `file_name` was provided.

Missing `task_id` usually means the authorization header, token, `spider_name`, or `spider_id` is wrong.

## Guardrails

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

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
