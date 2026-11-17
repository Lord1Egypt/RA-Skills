---
name: dataify-bing-shopping
description: "Search Bing Shopping for products and shopping results. Do not use for general Bing web search or structured marketplace scraping."
---

# Bing Shopping

## Overview


The source API document is summarized in `references/api.md`. Read it when field behavior or response shape is unclear.

## Workflow

1. Identify the user's product or shopping query and map optional requirements to API fields:
   - `q`: shopping search query. Required.
   - `json`: output format. Default is `1` because the field description says JSON is the default. Use `2` only when the user asks for JSON plus HTML, and `3` only when the user asks for HTML.
   - `mkt`: display language and market. No default in the field description.
   - `cc`: two-letter country or region code. No default in the field description.
   - `efirst`: shopping result offset. No default in the field description.
   - `filters`: advanced Bing filter string. No default in the field description.
   - `no_cache`: cache behavior. Default is `false` because the field description says `false` is the default.
2. Use defaults only when the field description explicitly states a default. Do not treat example request body values as defaults. Values such as `pizza`, `en-US`, `us`, empty strings, or sample filters are examples only, not defaults.
3. Prefer explicit user-provided field values over inferred values. If an optional field is ambiguous and has no documented default, omit it.
6. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags only when overriding automatic parsing.
7. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - The script adds a `Bearer ` prefix when the token does not already include one.
8. Generate the parameter table before requesting confirmation:

```bash
python3 scripts/bing_shopping.py --prompt "Search Bing Shopping for wireless earbuds" --preview-table
```

9. Run a live call only after the user confirms the displayed table:

```bash
```


## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_shopping.py \
  --prompt "Bing Shopping search for laptop stand, return JSON and HTML in the US market" \
  --json 2 \
  --cc us
```

Useful flags:

- `--q`, `--json`, `--mkt`, `--cc`, `--efirst`, `--filters`, `--no-cache`
- `--field key=value` for any supported API field
- `--body-format form|json`, default `form`
- `--dry-run` to print the parsed payload and skip network/auth checks
- `--preview-table` to print the full parameter table and skip network/auth checks

When no optional fields are specified by the user, the payload should contain `engine`, `q`, `json=1`, and `no_cache=false`.

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/bing_shopping.py --help
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
