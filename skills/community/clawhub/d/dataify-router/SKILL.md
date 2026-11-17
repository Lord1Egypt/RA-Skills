---
name: dataify-router
description: "Route broad search, scraping, monitoring, marketplace, social, travel, jobs, and maps requests to the smallest suitable Dataify skill set. Use when the user describes a collection outcome without naming a specific Dataify API or scraper. Do not use for competitor analysis or market intelligence."
---

# Dataify Router

Translate the user's outcome into a capability plan, then invoke the minimum required skills.

## Workflow

1. Restate the desired deliverable, target sources, scope, freshness, and output format.
2. Select capabilities from `references/capability-map.md`.
3. Prefer a synchronous SERP or Web Unlocker call for discovery. Use Builder scrapers when structured platform data is required.
4. Ask only for missing required inputs. Do not ask for fields that have safe documented defaults.
5. Confirm only for high-volume, multi-page, media-download, irreversible, or materially credit-sensitive work. A clear scoped request such as “直接执行” counts as confirmation. Use safe defaults and proceed without an extra confirmation turn for clear low-cost read-only work.
6. Never expose an API token in commands or output. Read `DATAIFY_API_TOKEN` from the environment.
7. For Builder jobs, always hand the returned task ID to `dataify-task-operations` and return the collected result. Stop at task creation only when the user explicitly requests submission only or `--no-wait` behavior.
8. Return a concise answer by default. Provide raw output when the user asks for it.

## Routing Rules

- Use a `serp-*` skill for search-engine discovery and fresh result pages.
- Use `dataify-web-unlocker` for a known page requiring rendering or access handling.
- Use a `scraper-*` skill for structured platform records.
- Use `dataify-agent-onboarding` for first-run setup or access-path selection, and `dataify-mcp` for MCP client configuration or repair.
- Use `dataify-live-research` for broad current-evidence research; keep competitor-specific decisions in `dataify-competitive-intelligence`.
- Use `dataify-seo-audit` for crawlability, indexation and on-page diagnosis of a known site.
- Use `dataify-scraper-builder` only after confirming that no prebuilt platform Skill covers the requested fields.
- Use `dataify-api-best-practices` when the deliverable is Dataify integration code or a code review.
- Use `dataify-competitive-intelligence` when multiple sources must be synthesized into a competitor comparison, pricing or review analysis, battlecard, or market-landscape decision.
- Use `dataify-price-intelligence` for normalized multi-seller or multi-channel price decisions.
- Use `dataify-review-intelligence` for cross-source customer-feedback themes and product actions.
- Use `dataify-lead-intelligence` for ICP company discovery, qualification, and evidence-based ranking.
- Use `dataify-brand-monitoring` for recurring cross-source mentions, issue detection, and reputation risk.
- Combine discovery and structured scraping only when discovery is needed to identify target URLs or IDs.
- If several platforms are requested, state the source plan and run independent sources separately.

## Output

Return the result, source coverage, important limitations, and any remaining asynchronous task state. Do not dump large raw payloads into chat unless requested.

## Quick Start

```bash
python3 -c 'print("Use this routing skill from your agent request.")'
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
