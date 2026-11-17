---
name: dataify-competitive-intelligence
description: "Research and compare competitors, products, pricing, customer feedback, hiring signals, positioning, or a market landscape using current public evidence. Use for competitor analysis, competitive battlecards, pricing intelligence, review intelligence, and market maps. Do not use for fetching one page, running one search, or collecting one platform record without analysis."
---

# Dataify Competitive Intelligence

Turn an open-ended competitive question into a sourced decision document. Use the smallest useful set of Dataify capabilities, distinguish fact from inference, and end with actionable recommendations rather than a dump of search results.

## Scope Selection

Choose only the modules required by the decision:

- Snapshot: read [snapshot.md](references/modules/snapshot.md).
- Product comparison: read [product-comparison.md](references/modules/product-comparison.md).
- Pricing intelligence: read [pricing-intelligence.md](references/modules/pricing-intelligence.md).
- Review intelligence: read [review-intelligence.md](references/modules/review-intelligence.md).
- Hiring signals: read [hiring-signals.md](references/modules/hiring-signals.md).
- Market landscape: read [market-landscape.md](references/modules/market-landscape.md).
- Battlecard: read [battlecard.md](references/modules/battlecard.md).

Do not run every module by default. If the requested decision, competitors, geography, or time window is unclear, ask only for information that materially changes the research plan.

## Workflow

1. Restate the decision, entities, geography, freshness window, and expected output.
2. Read [data-source-routing.md](references/data-source-routing.md) and create the minimum evidence plan. For Snapshot or Pricing, prefer `scripts/run_research.py` so the plan, evidence, failures, and recovery state are preserved.
3. Collect independent evidence in parallel when possible:
   - SERP skills discover current pages, news, reviews, jobs, and alternatives.
   - `dataify-web-unlocker` retrieves a known public page.
   - Platform scraper skills collect structured records at useful scale.
4. For asynchronous collection, submit once, use `dataify-task-operations` to wait safely, and retrieve the final result. A `task_id` is not research evidence.
5. Normalize successful actions into evidence objects following [evidence-schema.md](references/evidence-schema.md). Preserve the raw path and hash.
6. Normalize names, dates, currencies, billing periods, usage units, geography, and comparison scope.
7. Read [analysis-frameworks.md](references/analysis-frameworks.md) only for the selected modules, then separate facts, inferences, recommendations, and unknowns. Every finding must reference existing evidence IDs.
8. Apply [failure-recovery.md](references/failure-recovery.md) when a source or task fails; reduce confidence instead of fabricating coverage.
9. Use the relevant structure in [output-templates.md](references/output-templates.md). Date-stamp the research and cite material claims near the claim.
10. Apply [verification-checklist.md](references/verification-checklist.md) and run `scripts/verify_report.py` on the structured report before delivery.

## Execution Modes

- `quick`: up to 5 collection actions for an initial decision.
- `standard`: up to 12 actions for a normal comparison.
- `deep`: up to 20 actions; confirm material cost or scope before execution.
- Use `--max-actions` as a hard limit. Use `--checkpoint` when the user wants to review early evidence; use `--autopilot` only when they asked for autonomous completion.
- Read [cost-control.md](references/cost-control.md) for retry and paid-action boundaries.
- Resume with `--resume <run-directory>`; successful actions are never submitted again. After fixing a network or input issue, add `--retry-failed-safe` only for discovery/page failures; it never retries scraper submissions.
- Do not claim a credit estimate unless a reliable platform quote or usage response supports it.
- For recurring research, read [monitoring.md](references/monitoring.md) and run one incremental refresh per scheduled invocation.

## Evidence Rules

- Prefer current first-party product, pricing, documentation, policy, company, and hiring pages.
- Treat vendor claims as positioning evidence, not independently proven performance.
- Do not infer a missing capability from one README, pricing page, or failed request.
- Label estimates, extrapolations, and analyst judgment explicitly.
- Preserve contradictory evidence and explain likely scope or date differences.
- Never invent private prices, market share, customer counts, or roadmap commitments.

## Routing Boundaries

- Use a specific SERP skill for one search whose result list is the requested deliverable.
- Use `dataify-web-unlocker` for one known public page whose content is the deliverable.
- Use a platform scraper for structured records from one named source.
- Use `dataify-router` when the user wants collection but the appropriate Dataify capability is unclear.
- Use this skill when multiple sources must be synthesized into a competitive decision.

## Deliverable Contract

Return:

1. Executive answer and research date.
2. Scope, assumptions, and sources used.
3. Comparable evidence table.
4. Key findings with confidence and citations.
5. Gaps, contradictions, and unavailable evidence.
6. Prioritized actions with rationale.

## Quick Start

```bash
python3 skills/dataify-competitive-intelligence/scripts/run_research.py \
  --company Dataify \
  --company-domain www.dataify.com \
  --competitor "Bright Data" \
  --competitor-domain "Bright Data=brightdata.com" \
  --module snapshot \
  --module product \
  --module pricing \
  --mode quick \
  --autopilot
```

The command creates `state.json`, raw evidence, `evidence.json`, and draft Markdown/JSON reports. Inspect the evidence, write evidence-linked findings, and rebuild with `scripts/build_report.py --findings-json <file>`; a report with `evidence_ready_analysis_required` is not a completed competitive conclusion. Preview the bounded plan safely with `--dry-run`.

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
