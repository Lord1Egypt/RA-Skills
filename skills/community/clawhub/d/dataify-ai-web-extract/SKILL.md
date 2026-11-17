---
name: ai-web-extract
description: "Trigger when the user needs to extract Markdown, raw HTML, clean HTML, or links from a specified public webpage while controlling content filtering, timeout, and wait conditions."
---

# AI Web Extract

Call the AI Web API `/extract` endpoint directly with the fixed `unique_id=extract`.

## Quick Start

The production origin is built in. Set `AI_WEB_API_BASE_URL` only for another environment.

```powershell
$env:AI_WEB_API_BASE_URL = "https://aiwebapi.dataify.com"
$env:DATAIFY_API_TOKEN = "your_token_here"
```

```bash
python3 scripts/extract.py --url "https://example.com/article" --format markdown --dry-run
python3 scripts/extract.py --url "https://example.com/article" --format markdown --format links
```

## Parameters

| Option | Required | Notes |
| --- | --- | --- |
| `--url` | Yes | Public HTTP(S) page address. |
| `--format` | No | Repeat `markdown`, `raw_html`, `clean_html`, or `links`; default `markdown`. |
| `--only-main-content` | No | Enable or disable with `--no-only-main-content`; default `true`. |
| `--include-tag` / `--exclude-tag` | No | Repeatable selectors, up to 50 each. |
| `--header` | No | Target header using `Name: Value`; `Host` and hop-by-hop headers are rejected. |
| `--max-age-ms` | No | 0 to 172800000; default 172800000. |
| `--timeout-ms` | No | 1000 to 120000; default 60000. |
| `--wait-for-ms` | No | 0 to 30000, no more than half of timeout. |
| `--country` | No | Two-letter uppercase code; default `US`. |
| `--advanced-mode` | No | Enable or disable with `--no-advanced-mode`; default `true`. |

## Response and Cost

The API returns the `outputs` value, normally an object keyed by the requested formats. A successful uncached extraction is billed once at the gateway tool unit price.

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

- `references/extract-api.md`
- `scripts/extract.py`
- `scripts/ai_web_client.py`
