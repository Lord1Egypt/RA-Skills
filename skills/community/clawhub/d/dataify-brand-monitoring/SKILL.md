---
name: dataify-brand-monitoring
description: "Monitor a brand across current news, search, reviews, forums, or public social sources and report material mentions, sentiment signals, and reputation risks. Use for brand listening, campaign monitoring, issue detection, or recurring share-of-voice tracking. Do not use for one news search or one platform's raw posts."
---

# Dataify Brand Monitoring

Turn public brand mentions into a dated monitoring snapshot with traceable risks and changes. Distinguish observed mentions from automated sentiment or analyst inference.

## Workflow

1. Establish the brand, official domain, geography, keywords/campaigns, freshness window, known aliases and exclusions.
2. Run `scripts/run_brand_monitoring.py` for a bounded News plus Web discovery baseline. Add known public sources with `--source-url`; use platform Scrapers when structured social or review records are required.
3. Normalize title/text, URL, publisher/platform, date, geography and evidence ID. Deduplicate syndicated items and separate the brand's own claims from external mentions.
4. Report mention count, channel mix, positive/negative signals, emerging themes, high-risk items, coverage gaps and recommended response. Do not equate raw mention volume with share of voice without a competitor denominator.
5. Store dated runs for comparison. On recurring execution, collect a new snapshot and report added, removed and materially changed evidence.

## Quick Start

```bash
python3 skills/dataify-brand-monitoring/scripts/run_brand_monitoring.py \
  --brand "Dataify" --official-domain www.dataify.com \
  --keyword "web scraping" --mode quick
```

Use `--freshness`, `--max-actions` and `--dry-run` to control scope.

## Boundaries

- A single news query belongs to Google/Bing News.
- Raw posts or comments from one named platform belong to its platform Skill.
- Ongoing cross-source brand signals, reputation risk and change reporting belong here.

## Account handling

Use `dataify-task-operations` for Token setup and safe asynchronous completion. Never expose Token values.

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
