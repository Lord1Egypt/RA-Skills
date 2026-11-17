---
name: ai-web-search
description: "Trigger when the user needs AI Web API aggregate search across web, news, shopping, or scholar sources, with optional extraction of result content; when multiple tools are enabled under one product, select tool_code according to the user intent."
---

# AI Web Search

Call the AI Web API `/search` endpoint directly with four fixed modes. Do not expose or derive `unique_id` dynamically.

| Mode | `unique_id` | `source` | Required |
| --- | --- | --- | --- |
| Web | `search_web` | `web` | `query` |
| Shopping | `search_shopping` | `shopping` | `query` |
| News | `search_news` | `news` | `query` |
| Scholar | `search_scholar` | `scholar` | `query` |

## Quick Start

The production origin is built in. Set `AI_WEB_API_BASE_URL` only to override it for another environment.

```powershell
$env:AI_WEB_API_BASE_URL = "https://aiwebapi.dataify.com"
$env:DATAIFY_API_TOKEN = "your_token_here"
```

```bash
python3 scripts/search.py web --query "AI news" --time-range week --dry-run
python3 scripts/search.py shopping --query "wireless mouse" --dry-run
python3 scripts/search.py news --query "latest technology news" --time-range week --dry-run
python3 scripts/search.py scholar --query "large language models" --language en --dry-run
```

Run news search with body extraction:

```bash
python3 scripts/search.py news --query "OpenAI" --extract-content --extract-format markdown
```

## Web Search

Fixed identity: `{"unique_id":"search_web","source":"web"}`.

Options: `--query`, `--max-results`, `--country`, `--language`, `--time-range`, and extraction options. Country codes must be uppercase, for example `US`. Web supports `time_range`.

## Shopping Search

Fixed identity: `{"unique_id":"search_shopping","source":"shopping"}`.

Options: `--query`, `--max-results`, `--country`, `--language`, and extraction options. Shopping does not support `time_range` or an input `url`.

## News Search

Fixed identity: `{"unique_id":"search_news","source":"news"}`.

Options: `--query`, `--max-results`, `--country`, `--language`, `--time-range`, and extraction options. News supports `time_range`.

## Scholarly Search

Fixed identity: `{"unique_id":"search_scholar","source":"scholar"}`.

Options: `--query`, `--max-results`, `--language`, and extraction options. Scholar does not support `country` or `time_range`.

## Result Extraction

Available only with `--extract-content`: `--extract-format`, `--only-main-content` / `--no-only-main-content`, `--include-tag`, `--exclude-tag`, `--max-age-ms`, `--timeout-ms`, `--wait-for-ms`, and `--advanced-mode` / `--no-advanced-mode`.

Formats: `markdown`, `raw_html`, `clean_html`, `links`; no duplicates.

## Response and Cost

The direct API returns the gateway `outputs` value. Search results are normally arrays; no results may be `null`. Shopping and news URLs may be Google search or redirect URLs rather than final source URLs, and `snippet` may be `null`.

Search billing is based on returned results, plus successful uncached extraction details. Confirm before high `max_results` or bulk extraction.

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.

## References

- `references/search-api.md` contains the fixed-mode parameter contract.
- `scripts/search.py` is the request entry point.
- `scripts/ai_web_client.py` contains shared request helpers.
