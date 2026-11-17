---
name: ai-web-map
description: "Trigger when the user needs to discover page URLs from a public website, map a site, or collect site-wide entry points; when multiple tools are enabled, select tool_code according to the user intent."
---

# AI Web Map

Call the AI Web API `/map` endpoint directly with the fixed `unique_id=map`.

## Quick Start

The production origin is built in. Set `AI_WEB_API_BASE_URL` only for another environment.

```powershell
$env:AI_WEB_API_BASE_URL = "https://aiwebapi.dataify.com"
$env:DATAIFY_API_TOKEN = "your_token_here"
```

```bash
python3 scripts/map.py --url "https://docs.example.com" --limit 100 --dry-run
python3 scripts/map.py --url "https://docs.example.com" --limit 100
```

## Parameters

| Option | Required | Notes |
| --- | --- | --- |
| `--url` | Yes | Public HTTP(S) starting address. |
| `--country` | No | Two-letter uppercase code; default `US`. |
| `--domain-filter` | No | `domain` or `all`; default `all`. |
| `--limit` | No | 1 to 100000; default 5000. |
| `--sitemap` | No | `skip`, `include`, or `only`; default `include`. |


The wrapper rejects URL credentials, local hosts, and private, loopback, link-local, or reserved IPs before sending.

## Response and Cost

The direct API returns the `outputs` value, normally an array of URL objects. `null` means no addresses were discovered. The entry URL is excluded from Map billing; other returned addresses use the gateway tool unit price.

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

- `references/map-api.md`
- `scripts/map.py`
- `scripts/ai_web_client.py`
