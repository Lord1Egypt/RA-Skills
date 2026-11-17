---
name: dataify-google-finance
description: "Search Google Finance for stocks, indices, funds, currencies, or futures. Do not use for general web search or personalized financial advice."
---

# Dataify Google Finance

Use this skill to turn a user's Google Finance request into a Dataify Scraper API form POST.
## Workflow

1. Parse the user's request into Dataify Google Finance fields. Use `q` as the finance query and set `engine` to the fixed value `google_finance`.
2. Apply only documented defaults from the parameter descriptions:
   - `engine`: fixed `google_finance`
   - `json`: default `1`
   - `window`: default `1D`
   - `no_cache`: default `false`
   - `q`: no default; ask the user if it cannot be inferred
   - `hl`: no documented default; leave empty unless the user specifies it

```bash
python3 scripts/google_finance.py --request "查询 NASDAQ:GOOGL，窗口 1年，英文，返回 JSON" --preview-table
```

For many fields, pass one JSON object with shell-appropriate quoting:

```bash
python3 scripts/google_finance.py --params-json '{"q":"NASDAQ:GOOGL","window":"1Y","hl":"en","json":"1"}' --preview-table
```

5. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
6. Run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_finance.py`.

```bash
python3 scripts/google_finance.py --q "NASDAQ:GOOGL" --window 1Y --hl en --json 1
```

For a natural-language fallback, pass the whole request:

```bash
python3 scripts/google_finance.py --request "搜索苹果股票，图表范围 5天，不使用缓存"
```


## Field Mapping

Use `references/google_finance_api.md` for the complete parameter descriptions and documented defaults.

Core rules:

- Always submit the API request as form data with `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_finance`.
- Keep request values as strings unless the script accepts and normalizes a boolean.
- Ask a follow-up only when the required finance query `q` cannot be inferred.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.
- Do not show `Authorization` in the pre-call parameter table.
- Do not invent defaults from examples. Only use defaults explicitly stated in the parameter descriptions.

Common mappings:

- stock, index, mutual fund, currency, or futures search term -> `q`
- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- interface/search language -> `hl`
- "1天", "1 day", or "1D" -> `window: "1D"`
- "5天", "5 days", or "5D" -> `window: "5D"`
- "1个月", "1 month", or "1M" -> `window: "1M"`
- "6个月", "6 months", or "6M" -> `window: "6M"`
- "年初至今" or "YTD" -> `window: "YTD"`
- "1年", "1 year", or "1Y" -> `window: "1Y"`
- "5年", "5 years", or "5Y" -> `window: "5Y"`
- "最大", "max", or "MAX" -> `window: "MAX"`
- bypass cache -> `no_cache: "true"`

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/google_finance.py --help
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
