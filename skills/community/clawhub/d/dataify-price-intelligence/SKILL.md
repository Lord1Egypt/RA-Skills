---
name: dataify-price-intelligence
description: "Compare product or service prices across multiple sellers, marketplaces, or official pricing pages and produce normalized price findings. Use for price monitoring, offer comparison, channel pricing, or pricing-change decisions. Do not use for one raw product lookup or broad competitor strategy."
---

# Dataify Price Intelligence

Turn a pricing question into comparable offers and an evidence-backed pricing report. Default to the smallest useful plan and return conclusions, not a parameter dump or task ID.

## Workflow

1. Establish the product/service identity, geography, currency, comparable specification, competitors or sellers, and freshness requirement. Ask only when ambiguity would make prices incomparable.
2. Use `scripts/run_price_intelligence.py` for a bounded search and report. Add known official or marketplace pages with `--source-url`; use the matching platform Scraper when structured records are available.
3. Preserve list price, effective price, currency, seller, stock, shipping, unit/plan, billing period and collection time. Do not compare unlike variants or convert currency without stating the rate and date.
4. Report valid offer count, range, lowest comparable offer, channel differences, anomalies, gaps and recommended next action. Never call a search snippet a confirmed checkout price.
5. For recurring monitoring, resume or create a new dated run and compare evidence; do not resubmit an uncertain Builder task.

## Quick Start

```bash
python3 skills/dataify-price-intelligence/scripts/run_price_intelligence.py \
  --product "Sony WH-1000XM5" --geography US --mode quick
```

Use `--dry-run` to inspect the bounded plan. Use `--max-actions` to cap requests. Raw responses, hashes, state and Markdown/JSON reports are retained in the output directory.

## Boundaries

- One Amazon/eBay/Walmart product record belongs to its platform Skill.
- Cross-company product, positioning and strategy belongs to `dataify-competitive-intelligence`.
- Multi-source price normalization and a pricing decision belong here.

## Account handling

Follow `dataify-task-operations` for Token setup and asynchronous completion. Promote registration only when the Token is missing/invalid or credits are insufficient; never expose credentials.

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
