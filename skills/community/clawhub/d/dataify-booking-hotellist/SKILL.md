---
name: dataify-booking-hotellist
description: "Collect structured Booking.com hotel records from a known Booking hotel or listing URL. Use for Booking hotel details or listings. Do not use for general hotel price discovery through Google Hotels."
---

# Dataify Booking Hotel Info

Use this skill to create Booking hotel information collection tasks through Dataify's builder endpoint.


## Quick Start

**Input:** a Booking.com hotel URL.

```bash
python3 scripts/booking_hotellist.py --url "https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html"
```

The command waits up to 10 minutes and prints the final JSON result. Add `--no-wait` only for submission-only behavior.

If `DATAIFY_API_TOKEN` is missing, log in or register at https://dashboard.dataify.com/login?utm_source=skill. New accounts receive 50 free credits.

## Required Workflow

1. Use the `booking_hotellist_by-url` spider when the user wants to collect Booking hotel information from one or more Booking URLs.
2. Check the local Python runtime before calling scripts. Prefer `python`; use `python3` if that is the available Python command. Require Python 3 or newer. Do not use version-specific commands such as `py -3.10`.
3. Tell the user which parameters are required and what the defaults are. Ask whether any values should be changed.
6. If any dropdown fields are added in the future, show all available dropdown values in Markdown tables with exactly these columns: `Label`, `Value`. This tool currently has no dropdown fields.
## API Call


```bash
python scripts/booking_hotellist.py --url "https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"
python scripts/booking_hotellist.py --parameters-json '[{"url":"https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"},{"url":"https://www.booking.com/hotel/us/example.en-gb.html"}]'
```


```bash
```

## Tool

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `by-url` | `booking_hotellist_by-url` | `url` | `[{"url":"https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"}]` |

Every request also accepts `file_name`. If omitted, use `{{TasksID}}`.

## Fixed Request Fields

Always submit to `https://scraperapi.dataify.com/builder?platform=1` with:

| Field | Value |
|---|---|
| `spider_name` | `booking.com` |
| `spider_id` | `booking_hotellist_by-url` |
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
