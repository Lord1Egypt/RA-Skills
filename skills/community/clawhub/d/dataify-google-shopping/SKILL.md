---
name: dataify-google-shopping
description: "Search Google Shopping for product discovery, offers, and price comparison. Do not use for structured bulk product extraction by keyword."
---

# Dataify Google Shopping

Use this skill to turn a user's Google Shopping request into a Dataify Scraper API call.
## Workflow

1. Parse the user's request into Dataify Google Shopping fields. Use `q` as the shopping search query and always set `engine` to `google_shopping`.
2.  If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
3. Build request parameters with only the fields the user requested plus required documented defaults. Use `json: "1"` and `google_domain: "google.com"` unless the user asks for another value. Do not use example values from the API document as defaults.
5. If the user changes any parameter, update the values and show the complete table again before calling.

## Script Usage

Run commands from this skill directory, or use the absolute path to `scripts/google_shopping.py`.

Preview the complete parameter table:

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true --table
```

Call the API after the user confirms:

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true
```

For natural-language parsing, pass the user's request:

```bash
python3 scripts/google_shopping.py --request "搜索美国 Google Shopping 上 100 美元以下包邮的无线耳机，英文，返回 JSON" --table
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_shopping.py --params-json '{"q":"wireless headphones","gl":"us","hl":"en","max_price":"100","free_shipping":"true"}' --table
```

Use `--dry-run` only for internal verification. It prints the normalized payload JSON and does not call the API.

## Field Mapping


Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_shopping`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Omit optional fields that the user did not request unless the API document gives a real default.
- Ask a follow-up only when the required shopping query `q` cannot be inferred.
- If both `location` and `uule` are present, prefer the explicit `uule` and omit `location`.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- country or region for Google behavior -> `gl`
- interface/search language -> `hl`
- page number N -> `start: String((N - 1) * 10)`
- raw Google Shopping filter token -> `shoprs`
- minimum price -> `min_price`
- maximum price -> `max_price`
- price low to high -> `sort_by: "1"`
- price high to low -> `sort_by: "2"`
- free shipping only -> `free_shipping: "true"`
- sale or discount items only -> `on_sale: "true"`
- small business items only -> `small_business: "true"`
- bypass cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true --table
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
