---
name: dataify-google-patents
description: "Search Google Patents for patent records. Do not use for Google Scholar papers or general web results."
---

# Dataify Google Patents

Use this skill to turn a user's Google Patents request into a Dataify Scraper API call.
## Workflow

1. Parse the user's request into Dataify Google Patents fields. Always set `engine` to `google_patents`.
2. Apply only defaults that are explicitly stated in the parameter descriptions:
   - `json: "1"`
   - `page: "0"`
   - `dups: "family"`
   - `patents: "true"`
   - `scholar: "false"`
   - `no_cache: "false"`
   - `sort` defaults to relevance by omitting the field.
3. Do not use example values as defaults. Omit optional fields that have no documented default unless the user requested them.
4.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents" --print-table
```


6. If the user changes parameters, pass the edited values with explicit flags or with `--params-json`, show the table again, and ask for confirmation again.

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents"
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_patents.py --params-json '{"q":"battery recycling","status":"GRANT","country":"US","json":"1"}'
```


## Field Mapping

Use `references/google_patents_api.md` when you need the exact field list, defaults, accepted values, and mapping hints.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always use UTF-8 encoding.
- Always force `engine` to `google_patents`; ignore any conflicting user-provided engine.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up when no meaningful search query or filter can be inferred.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not reveal the full token in the parameter review table.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- first page -> `page: "0"`, second page -> `page: "1"`
- newest/latest/recent -> `sort: "new"`
- oldest/earliest -> `sort: "old"`
- relevance/default relevance -> omit `sort`
- grouped/clustered results -> `clustered: "true"`
- family deduplication -> `dups: "family"`
- publication deduplication -> `dups: "language"`
- include patent results -> `patents: "true"`
- include Google Scholar results -> `scholar: "true"`
- before/after dates -> `before` or `after`, formatted as `priority:YYYYMMDD`, `filing:YYYYMMDD`, or `publication:YYYYMMDD`
- inventor names -> `inventor`
- assignee, applicant, or owner names -> `assignee`
- country/region patent codes -> `country`
- result language filter -> `language`
- granted patents -> `status: "GRANT"`
- applications -> `status: "APPLICATION"`
- patent type -> `type: "PATENT"`
- design type -> `type: "DESIGN"`
- litigation yes/no -> `litigation: "YES"` or `litigation: "NO"`
- bypass cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents" --print-table
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
