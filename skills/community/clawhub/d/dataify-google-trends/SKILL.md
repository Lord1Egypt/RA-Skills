---
name: dataify-google-trends
description: "Search Google Trends for keyword interest and trend data. Do not use for general Google web search."
---

# Dataify Google Trends

Use this skill to turn a user's Google Trends request into a Dataify Scraper API form submission.
## Workflow

1. Parse the user's request into Google Trends fields. Use `q` as the query and set `engine` to `google_trends`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters from the user's request plus required API defaults. Do not use example values as defaults. In particular, do not default `q` to `pizza`; ask the user for a query if it cannot be inferred.

```bash
python3 scripts/google_trends.py --q "AI" --json 1
```

For many fields, pass one JSON object with shell-appropriate quoting. The script still submits form data to the API:

```bash
python3 scripts/google_trends.py --params-json '{"q":"AI","json":"1","hl":"en","geo":"United+States","data_type":"TIMESERIES"}'
```

To generate the required pre-call parameter table from the normalized request without calling the API:

```bash
python3 scripts/google_trends.py --request "search Google Trends for AI in the United States, English, timeseries" --preview-table
```

Return the final script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response.

## Field Mapping

Use `references/google_trends_api.md` when you need the exact field list, defaults, values, or parameter descriptions.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_trends`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up only when required `q` cannot be inferred.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Use UTF-8 for all files, script output, and request encoding.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- bypass cache / no cache / skip cache -> `no_cache: "true"`
- use cache -> `no_cache: "false"`
- language / interface language -> `hl`
- country, region, or Google Trends location -> `geo`
- subregion level / city / DMA / country-region breakdown -> `region`
- time trend / interest over time -> `data_type: "TIMESERIES"`
- regional comparison -> `data_type: "GEO_MAP"`
- regional interest distribution -> `data_type: "GEO_MAP_0"`
- related topics -> `data_type: "RELATED_TOPICS"`
- related queries -> `data_type: "RELATED_QUERIES"`
- timezone offset in minutes -> `tz`
- category -> `cat`
- image search -> `gprop: "images"`
- news search -> `gprop: "news"`
- Google Shopping -> `gprop: "froogle"`
- YouTube Search -> `gprop: "youtube"`
- date range, "past 12 months", "today 5-y", or other Google Trends date expression -> `date`
- CSV results -> `csv: "true"`
- include low search volume regions -> `include_low_search_volume: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_trends.py --q "AI" --json 1
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
