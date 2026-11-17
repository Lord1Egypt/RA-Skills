---
name: dataify-lead-intelligence
description: "Discover and rank companies that match an ideal customer profile using public company, hiring, and market evidence. Use for account research, prospect-company lists, territory planning, or evidence-based lead qualification. Do not use to obtain private personal contact data or scrape one company profile without qualification."
---

# Dataify Lead Intelligence

Produce a deduplicated, evidence-backed company prospect list. This Skill qualifies organizations, not private individuals, and must not invent emails, phone numbers, revenue or employee counts.

## Workflow

1. Capture the ICP, geography, industry, material size constraints, buying signals and exclusion criteria. Do not ask for fields that do not affect qualification.
2. Run `scripts/run_lead_intelligence.py` for bounded discovery. Use known LinkedIn, Crunchbase, Indeed, Glassdoor or company URLs as supporting sources when available.
3. Normalize company name, canonical domain, geography, industry, public scale indicators, hiring/growth signals, source and collection date; merge duplicates by verified domain where possible.
4. Score only from explicit evidence. Return the reason for each score, missing fields, disqualifiers and a human-verification queue. A search rank is not lead quality.
5. Do not infer or enrich private personal contact details. Respect public-source and platform boundaries.

## Quick Start

```bash
python3 skills/dataify-lead-intelligence/scripts/run_lead_intelligence.py \
  --ideal-customer-profile "US AI startups hiring data engineers" \
  --geography US --mode quick
```

Use `--keyword` for a buying signal, `--source-url` for a known public company source, and `--dry-run` to review request scope.

## Boundaries

- One known company record belongs to the corresponding LinkedIn/Crunchbase/Indeed/Glassdoor Skill.
- General competitive landscape analysis belongs to `dataify-competitive-intelligence`.
- Multi-source company discovery and qualification belongs here.

## Account handling

Use `dataify-task-operations` for Token setup and safe completion. Never request that a user paste credentials into chat.

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
