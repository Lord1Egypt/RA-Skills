---
name: dataify-api-best-practices
description: "Write, review, or debug Dataify SERP, Web Unlocker, Builder, MCP, or SDK integration code using correct authentication, task lifecycle, retry, error, and output patterns. Do not use for ordinary end-user searches, scraping, research, or account setup."
metadata:
  author: Dataify
  version: "1.1.1"
  documentation: https://doc.dataify.com
  support: https://www.dataify.com/
---

# Dataify API Best Practices

Use this narrow developer Skill when integration correctness is the deliverable. Start with [integration-contract.md](references/integration-contract.md), then read only the relevant API or language reference: [authentication](references/authentication.md), [SERP](references/serp-api.md), [Web Unlocker](references/web-unlocker.md), [Builder](references/builder-api.md), [task lifecycle](references/task-lifecycle.md), [Python](references/python.md), [JavaScript/TypeScript](references/javascript-typescript.md), [errors](references/error-catalog.md), and the final [production checklist](references/production-checklist.md). Run the static audit before delivery.

## Required invariants

- Read `DATAIFY_API_TOKEN` from the environment and never log it.
- Search and page reads may retry with a bound; unknown Builder submissions must never be resubmitted automatically.
- Wait for Builder completion and return the final result, not only a task ID.
- Treat local timeout as resumable, not remote failure.
- Decode network and subprocess output explicitly as UTF-8 with replacement on malformed bytes.
- Preserve source, status, error category and recovery information.

## Quick Start

```bash
python3 scripts/audit_integration.py path/to/integration.py
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
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
