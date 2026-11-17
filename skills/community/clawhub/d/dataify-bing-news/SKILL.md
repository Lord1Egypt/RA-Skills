---
name: dataify-bing-news
description: "Search Bing News for current news results. Do not use for general Bing web search."
---

# Bing News

## Overview


The source API document is summarized in `references/api.md`. Read it when field behavior, allowed values, or response shape is unclear.

## Workflow

1. Identify the user's news query and map optional requirements to API fields:
   - `engine`: always `bing_news`. Default comes from the parameter description.
   - `q`: news search keywords. Default is `pizza` when the user does not specify a query, because the parameter description says the default is pizza.
   - `json`: output format. Default is `1` for JSON. Use `2` only when the user asks for JSON plus HTML. Use `3` only when the user asks for HTML.
   - `mkt`: display language and market, such as `en-US` or `zh-CN`. No default in the parameter description.
   - `cc`: two-letter country or region code, such as `us`, `cn`, `jp`, or `uk`. No default in the parameter description.
   - `first`: result offset. Default is `1` because the parameter description says the default is 1.
   - `count`: requested result count. No default in the parameter description.
   - `qft`: Bing query filter string for date sorting/filtering. No default in the parameter description.
   - `safeSearch`: `Off`, `Moderate`, or `Strict`. No default in the parameter description.
   - `no_cache`: `true` to bypass cache, `false` to use cache. Default is `false` because the parameter description says false is the default.
2. Get defaults only from parameter descriptions. Do not treat YAML body examples or inline examples like `mkt=en-US`, `cc=us`, or `count=10` as defaults.
3. Prefer explicit user-provided field values over inferred values. Add optional fields without defaults only when the user clearly asks for them or provides exact field values.
4. Use the bundled Python script with `python3`. Pass the whole user request through `--prompt` and add explicit flags for any fields that should override automatic parsing. On Windows, if `python3` is not installed but `python` points to Python 3, use `python` for local execution.
   - Run `--preview` to print a Markdown table with exactly these columns: 参数名, 当前值, 默认值, 说明.
   - Show the table to the user and ask for confirmation.
   - If the user asks to modify values, update the fields and preview the full table again.
   - Call the API only after the user confirms the displayed parameters.
6. Ensure authentication before a live call:
   - Read `DATAIFY_API_TOKEN` from the current environment.
   - The script adds a `Bearer ` prefix when the token does not already include one.
7. Preview parameters before calling:

```bash
python3 scripts/bing_news.py --prompt "Search Bing news for OpenAI" --preview
```

8. Run a live call only after the user confirms the previewed table:

```bash
python3 scripts/bing_news.py --prompt "Search Bing news for OpenAI"
```


## Script Usage

The script supports automatic parsing plus explicit overrides:

```bash
python3 scripts/bing_news.py \
  --prompt "用必应新闻搜索 OpenAI"
```

Useful flags:

- `--q`, `--json`, `--mkt`, `--cc`, `--first`, `--count`, `--qft`, `--safeSearch`, `--no-cache`
- `--field key=value` for any supported API field
- `--body-format form|json`, default `form`
- `--dry-run` to print the parsed payload and skip network/auth checks

## Result presentation

- Return a compact, user-facing result by default: the most relevant titles, links, and vertical-specific fields, plus a count or truncation note when useful.
- Do not expose transport details, fixed engine fields, task plumbing, or the full response envelope in the ordinary flow.
- Return raw JSON or HTML only when the user explicitly requests raw output.
- Preserve source links and distinguish missing fields from empty values; do not invent data.

## Quick Start

```bash
python3 scripts/bing_news.py --help
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
