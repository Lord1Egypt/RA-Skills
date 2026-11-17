---

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.
name: dataify-google-maps-reviews
description: "Collect reviews and comments for a known Google Maps place URL. Do not use for place discovery or general place details without reviews."
---

# Dataify Google Maps Reviews

Use this skill to create Google Maps review/comment collection tasks through Dataify's builder endpoint.

## Required Workflow

1. Use the `google_comment_by-url` spider when the user wants to collect Google Maps review information, comment information, or reviews/comments from a Google Maps URL.
2. Check the local Python runtime before calling scripts. Prefer `python`; use `python3` if that is the available Python command. Require Python 3 or newer. Do not use version-specific commands such as `py -3.10`.
3. Tell the user which parameters are required and what the defaults are. Ask whether any values should be changed.
6. If any dropdown fields are added in the future, show all available dropdown values in Markdown tables with exactly these columns: `Label`, `Value`. This tool currently has no dropdown fields.
## API Call


```bash
python scripts/google_maps_reviews.py --url "https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu" --days-limit 20
python scripts/google_maps_reviews.py --parameters-json '[{"url":"https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu","days_limit":"20"},{"url":"https://www.google.com/maps/place/example","days_limit":"30"}]'
```


```bash
```

## Tool

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `url` | `google_comment_by-url` | `url`, `days_limit` | `[{"url":"https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu","days_limit":"20"}]` |

Every request also accepts `file_name`. If omitted, use `{{TasksID}}`.

## Fixed Request Fields

Always submit to `https://scraperapi.dataify.com/builder?platform=1` with:

| Field | Value |
|---|---|
| `spider_name` | `google.com` |
| `spider_id` | `google_comment_by-url` |
| `spider_parameters` | JSON array of one or more parameter objects |
| `spider_errors` | `true` |
| `file_name` | User value, otherwise `{{TasksID}}` |

Send parameters as form data. Keep `spider_parameters` as a JSON string inside the form body.

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
python3 scripts/google_maps_reviews.py --help
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
