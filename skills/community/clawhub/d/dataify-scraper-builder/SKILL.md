---
name: dataify-scraper-builder
description: "Inspect a real public website and design a runnable Dataify-based scraper when no suitable prebuilt scraper exists. Use for field extraction, pagination, JSON-LD, hidden API, or rendering strategy. Do not use when an existing platform Skill already fulfills the request or when login and browser interaction are mandatory."
metadata:
  author: Dataify
  version: "1.1.1"
  documentation: https://doc.dataify.com
  support: https://www.dataify.com/
---

# Dataify Scraper Builder

Build the smallest reliable scraper for a real target. Check [prebuilt-routing.md](references/prebuilt-routing.md) first; prefer an existing structured Dataify Skill over custom extraction.

## Workflow

1. Require a real target URL and requested fields. Never execute a documentation example target.
2. If the script returns `routed_to_prebuilt`, use that Skill and stop. Continue with `--force-custom` only when the user explicitly needs fields the prebuilt capability cannot provide.
3. Run `scripts/build_scraper.py --url <url> --fields <comma-separated fields>`.
4. Inspect SSR/CSR evidence, JSON-LD, links, password/CAPTCHA interaction and pagination signals.
5. Choose structured platform Scraper, Web Unlocker plus parsing, hidden API, or Browser-required. Never label an interactive shell as Web Unlocker-ready merely because some HTML was returned.
6. Test the generated starter against the target. Require a non-empty sample and at least 90% requested-field completeness. Return `needs_selector_refinement` with `unsupported_fields` instead of claiming readiness when validation fails.

## Quick Start

```bash
python3 scripts/build_scraper.py --url "https://www.dataify.com/" --fields "title,description" --output-dir generated-scraper
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
