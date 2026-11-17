---
name: dataify-google-flights
description: "Search Google Flights for fares and itineraries. Do not use for hotels or general travel web search."
---

# Dataify Google Flights

Use this skill to turn a user's Google Flights request into a Dataify Scraper API form POST.
## Workflow

1. Parse the user's request into Dataify Google Flights fields. Read `references/google_flights_api.md` for the full field list, accepted values, defaults, and conditional requirements.
   - Do not show `Authorization`.
   - Show the complete documented body field list, not only fields present in the user request.
   - Use exactly these columns: `参数名`, `当前值`, `默认值`, `说明`.
   - For parameters whose description states a default value, use that default when the user did not specify a value.
   - Leave default value blank when the parameter description does not state a default.
   - Never use examples, placeholders, sample YAML values, or blank values as defaults.
3. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
4. Build request parameters with documented defaults only. The script submits these parameters as form data, not a JSON request body.
5. After the user confirms the table, run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_flights.py`.

```bash
python3 scripts/google_flights.py --params-json '{"departure_id":"JFK","arrival_id":"LAX","type":"2","outbound_date":"2026-06-01","currency":"USD","gl":"us","hl":"en"}' --dry-run --dry-run-format markdown
```


```bash
```


## Mapping Rules

- Always submit the API request as form data with UTF-8 encoding and `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_flights`.
- Use `json: "1"` unless the user asks for another output format.
- Resolve relative dates from the conversation date, then pass dates as `YYYY-MM-DD`.
- Ask a follow-up when the user's route or requested continuation cannot be inferred safely. Do not require dates unless the user explicitly asks for a dated itinerary.
- If the user gives city names instead of airport codes and the airport is ambiguous, ask for the airport code or Google kgmid.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- one-way/single trip -> `type: "2"`
- round trip/return trip -> `type: "1"`
- multi-city -> `type: "3"` and `multi_city_json`
- economy/premium economy/business/first -> `travel_class: "1"`, `"2"`, `"3"`, `"4"`
- best/price/departure time/arrival time/duration/emissions sort -> `sort_by: "1"`, `"2"`, `"3"`, `"4"`, `"5"`, `"6"`
- any stops/nonstop/one stop or fewer/two stops or fewer -> `stops: "0"`, `"1"`, `"2"`, `"3"`
- bypass cache/no cache -> `no_cache: "true"`
- deep search -> `deep_search: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_flights.py --params-json '{"departure_id":"JFK","arrival_id":"LAX","type":"2","outbound_date":"2026-06-01","currency":"USD","gl":"us","hl":"en"}' --dry-run --dry-run-format markdown
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
