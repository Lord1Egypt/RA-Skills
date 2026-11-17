---
name: dataify-google-hotels
description: "Search Google Hotels for hotel discovery, prices, or availability. Do not use to scrape a known Booking.com hotel URL."
---

# Dataify Google Hotels

Use this skill to turn a user's Google Hotels request into a Dataify Scraper API form POST.
## Workflow

1. Parse the user's request into Dataify Google Hotels fields. Read `references/google_hotels_api.md` when the exact field list, accepted values, defaults, or mapping notes are needed.
2. Resolve relative dates from the conversation date, then pass dates as `YYYY-MM-DD`.

```bash
python3 scripts/google_hotels.py --params-json '{"q":"Tokyo hotels","check_in_date":"2026-06-01","check_out_date":"2026-06-03","gl":"us","hl":"en"}' --dry-run
```

5. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. After the user confirms the table, run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_hotels.py`.

```bash
```


## Mapping Rules

- Always submit the API request as form data with UTF-8 encoding and `Content-Type: application/x-www-form-urlencoded; charset=utf-8`.
- Always force `engine` to `google_hotels`.
- Use documented defaults only. Do not treat examples, placeholders, or blank values in the API docs as defaults.
- Use `json: "1"` unless the user asks for another output format.
- Use `q`, `check_in_date`, and `check_out_date` for normal hotel searches when they can be inferred. Ask a follow-up if a normal search is missing any of those fields.
- Use `property_token` for hotel detail requests when the user provides a property token.
- Use `next_page_token` for next-page requests when the user provides a pagination token.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- lowest price / cheapest -> `sort_by: "3"`
- highest rating -> `sort_by: "8"`
- most reviewed -> `sort_by: "13"`
- rating 3.5+ / 4.0+ / 4.5+ -> `rating: "7"` / `"8"` / `"9"`
- free cancellation -> `free_cancellation: "true"`
- special offers -> `special_offers: "true"`
- eco certified -> `eco_certified: "true"`
- vacation rentals -> `vacation_rentals: "true"`
- bypass cache / no cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_hotels.py --params-json '{"q":"Tokyo hotels","check_in_date":"2026-06-01","check_out_date":"2026-06-03","gl":"us","hl":"en"}' --dry-run
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
