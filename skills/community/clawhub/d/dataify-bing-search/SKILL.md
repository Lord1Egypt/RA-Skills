---
name: dataify-bing-search
description: "Run a general Bing web search. Do not use when the user explicitly requests Bing images, maps, news, shopping, or videos."
---

# Bing Search

## Overview


The source API document is summarized in `references/api.md`. Read it when field behavior, allowed values, or response shape is unclear.

## Workflow

1. Identify the user's actual search query and map requirements to API fields:
   - `q`: search terms. Required.
   - `json`: output format. Default to `1` for JSON when the user does not specify an output format. Use `2` for JSON plus HTML, `3` for HTML.
   - `location`: named geographic search origin.
   - `lat` and `lon`: GPS search origin.
   - `mkt`: display language and market, such as `zh-CN` or `en-US`. Do not pass it unless the user asks for a market/language.
   - `cc`: two-letter country or region code, such as `us`, `cn`, `jp`, `uk`. Do not pass it unless the user asks for a country/region.
   - `first`: organic result offset. Default to `1` when the user does not specify it.
   - `safeSearch`: `Off`, `Moderate`, or `Strict`.
   - `filters`: advanced Bing filter string.
   - `no_cache`: `true` to bypass cache, `false` to use cache. Default to `false` when the user does not specify it.
2. Apply defaults only when the parameter description states a default. Current defaults from the API description are `engine=bing`, `q=pizza`, `json=1`, `first=1`, and `no_cache=false`. Do not treat body examples such as `location=India`, `lat=1`, `lon=1`, `mkt=zh-cn`, or `cc=AR` as defaults.
3. Prefer explicit user-provided field values over inferred values. If the user asks for a concrete search, replace the documented default `q=pizza` with the user's actual query.

```bash
python3 scripts/bing_search.py --prompt "<user request>" --show-params
```

5. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags for any fields that should override automatic parsing.
6. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - The script adds a `Bearer ` prefix when the token does not already include one.
7. Run a dry run when you need to inspect parsed payload JSON without calling the API:

```bash
python3 scripts/bing_search.py --prompt "Search Bing for current OpenAI news, return JSON and HTML" --dry-run
```


```bash
python3 scripts/bing_search.py --prompt "Search Bing for current OpenAI news, return JSON and HTML"
```


## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_search.py \
  --prompt "Find current OpenAI news, return JSON and HTML" \
  --no-cache true
```

Useful flags:

- `--q`, `--json`, `--location`, `--lat`, `--lon`, `--mkt`, `--cc`, `--first`, `--safeSearch`, `--filters`, `--no-cache`
- `--field key=value` for any supported API field
- `--url` to override the fixed endpoint only when explicitly needed for debugging
- `--body-format form|json`, default `form`
- `--dry-run` to print the parsed payload and skip network/auth checks
- `--show-params` to print the complete pre-call parameter table and exit


## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/bing_search.py --prompt "<user request>" --show-params
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
