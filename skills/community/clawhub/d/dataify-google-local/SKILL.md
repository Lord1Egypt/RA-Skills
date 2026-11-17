---
name: dataify-google-local
description: "Search Google Local for nearby businesses and local results. Do not use for a known Place ID or detailed map record."
---

# Dataify Google Local

Use this skill for Google Local/local pack keyword-and-location business results. Do not use it for map-coordinate browsing, a known Place ID, place details, or reviews.
## Workflow

1. Parse the user's request into Google Local fields. Always set `engine` to the fixed value `google_local`.
4. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
5. Build request parameters with the fields the user requested plus documented defaults only: `engine: "google_local"`, `json: "1"`, `google_domain: "google.com"`, and `no_cache: "false"`. Omit optional fields that the user did not request and that have no documented default.


```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --gl us --hl en
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_local.py --params-json '{"q":"coffee shops","location":"New York","gl":"us","hl":"en"}'
```

PowerShell may need the quotes escaped:

```powershell
python3 scripts/google_local.py --params-json '{\"q\":\"coffee shops\",\"location\":\"New York\",\"gl\":\"us\",\"hl\":\"en\"}'
```

To let the script parse a natural-language request:

```bash
python3 scripts/google_local.py --request "搜索纽约咖啡店，语言英文，地区美国，不走缓存"
```

## Field Mapping

Use `references/google_local_api.md` when exact parameter wording is needed.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_local`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request unless the field has a documented default.
- Ask a follow-up only when the required search query `q` cannot be inferred.
- If both `location` and `uule` are present, prefer the explicit `uule` and omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- named search origin -> `location`
- encoded location -> `uule`
- page number N -> `start: String((N - 1) * 10)`
- Google place CID -> `ludocid`
- advanced search filters -> `tbs`
- bypass/no cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --gl us --hl en
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
