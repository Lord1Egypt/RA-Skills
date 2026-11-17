---
name: dataify-review-intelligence
description: "Analyze reviews or public customer feedback across multiple sources and produce themes, sentiment signals, and product actions. Use for review mining, complaint analysis, voice-of-customer research, or reputation themes. Do not use to download raw comments from only one named platform without analysis."
---

# Dataify Review Intelligence

Convert public reviews into traceable customer themes and product recommendations. Preserve source bias and sample limitations; sentiment counts are signals, not ground truth.

## Workflow

1. Identify the product, app, place or brand, review period, relevant markets and decision to support.
2. Run `scripts/run_review_intelligence.py`. Provide known Amazon or Google Maps review URLs with `--source-url` to route to structured review collection; otherwise begin with bounded discovery.
3. Retain review text, rating, date, platform and evidence ID. Deduplicate obvious copies and do not infer representativeness across platforms.
4. Group repeated praise, complaint, request and churn-risk themes. Report sample size, rating/sentiment signals, examples linked to evidence, source bias and prioritized product actions.
5. If a paid task times out, preserve and resume its task ID; never submit the same target merely because local monitoring stopped.

## Quick Start

```bash
python3 skills/dataify-review-intelligence/scripts/run_review_intelligence.py \
  --subject "Notion" --freshness "6 months" --mode quick
```

For a known source add `--source-url <public-review-url>`. Use `--dry-run` or `--max-actions` for cost control.

## Boundaries

- Raw comments from one known platform belong to its platform Scraper.
- Competitor-wide product/pricing analysis belongs to `dataify-competitive-intelligence`.
- Cross-source themes and actionable voice-of-customer analysis belong here.

## Account handling

Use `dataify-task-operations` for Token setup and asynchronous completion. Never expose credentials or promote signup during successful execution.

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
