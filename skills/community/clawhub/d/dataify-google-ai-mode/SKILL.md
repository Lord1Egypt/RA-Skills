---
name: dataify-google-ai-mode
description: "Search with Google AI Mode when the user explicitly requests AI Mode or AI-generated Google search results. Do not use for ordinary Google SERP results."
---

# Dataify Google AI Mode

Use this skill to turn a user's Google AI Mode request into a Dataify Scraper API form submission.
## Workflow

1. Parse the user's request into Google AI Mode fields. Use `q` as the query and set `engine` to `google_ai_mode`.
2. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters with only the fields the user requested plus required defaults. Use `json: "1"` unless the user asks for another output format.
4. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_ai_mode.py`.

```bash
python3 scripts/google_ai_mode.py --q "pizza" --json 1
```

For many fields, you may pass one JSON object with shell-appropriate quoting. The script will still submit form data to the API:

```bash
python3 scripts/google_ai_mode.py --params-json '{"q":"pizza","json":"1","gl":"us","hl":"en"}'
```


## Field Mapping

Use `references/google_ai_mode_api.md` when you need the exact field list or examples.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_ai_mode`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request.
- Ask a follow-up only when the required query `q` cannot be inferred.
- If both `location` and `uule` are present, prefer the explicit `uule` and omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- search origin location -> `location`
- Google encoded location -> `uule`
- bypass cache / no cache -> `no_cache: "true"`
- use cache -> `no_cache: "false"`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_ai_mode.py --q "pizza" --json 1
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
