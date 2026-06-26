---
name: agent-analytics-autoresearch
description: "Run an autoresearch-style growth loop for landing pages, onboarding, pricing, and experiment candidates. Collect or read analytics snapshots, preserve product truth, generate/critique/synthesize variants, blind-rank with Borda scoring, and output two review-ready A/B test variants. Works with any analytics data; best with Agent Analytics CLI/API."
version: 1.0.9
author: dannyshmueli
license: MIT
repository: https://github.com/Agent-Analytics/skills
homepage: https://agentanalytics.sh
compatibility: Requires a coding agent that can read and write local files. Agent Analytics data collection requires npx and browser approval or detached login. The loop can also run from pasted reports, SQL output, CSV exports, or existing analytics files.
tags:
  - analytics
  - autoresearch
  - growth
  - experiments
  - ab-testing
  - landing-pages
provides:
  - capability: autoresearch
  - capability: ab-testing
  - capability: growth-experiments
  - capability: landing-page-optimization
metadata:
  openclaw:
    requires:
      anyBins:
        - npx
---

# Agent Analytics Autoresearch

Use this skill when the user wants a data-informed growth loop for landing pages, onboarding, pricing, CTAs, signup, checkout, activation, or other experiment candidates.

This skill is based on:

- Autoresearch Growth template: <https://github.com/Agent-Analytics/autoresearch-growth>
- Agent Analytics: <https://agentanalytics.sh>
- Regular Agent Analytics skill: <https://github.com/Agent-Analytics/skills/tree/main/skills/agent-analytics>

Use the regular `agent-analytics` skill for general setup, tracking installation, ad hoc reporting, and normal experiment operations. Use this skill for structured variant generation and judging from a project brief plus analytics data.

## Core Rule

Do not edit production copy, product code, or live experiment setup while running the loop unless the user explicitly asks. Produce reviewable artifacts first.

Default mode is review-only: generate variants, log rounds, and write `final_variants.md`.

After explicit human approval, continue into the outer experiment loop when requested: implement the approved variant or variants, create the experiment, run it, measure it with Agent Analytics or another analytics source, save the results as the next snapshot, and start the next autoresearch run from evidence.

## Inputs

The loop needs:

- target surface
- current control copy
- product truth
- audience
- primary metric
- proxy metric
- guardrails
- analytics snapshot or data brief
- drift constraints

Agent Analytics is preferred, but not required. Accept any evidence source: Agent Analytics CLI/API, PostHog, GA4, Mixpanel, SQL, CSV exports, product logs, dashboard screenshots summarized by the user, or hand-written notes.

When Agent Analytics is the evidence source, use project context as the self-improving product memory for the loop. Read `context get <project>` before collecting a snapshot, fold `project_context` into the product truth and metric definitions, and keep activation/event meaning separate per project or domain. After a human correction, scanner result, completed experiment, or repeated measured finding, update context only with durable product truth. Save activation definitions, event meanings, stable goals, and confirmed interpretations; skip weekly numbers, temporary spikes, pasted reports, PII, and unconfirmed guesses.

## Quick Start

If the user already has a repo or run folder, work there. Otherwise initialize a run:

```bash
bash <skill_dir>/scripts/init_autoresearch_run.sh homepage-signup
```

Then fill `brief.md`, collect or paste data, and run the loop:

```text
Read brief.md and run the autoresearch growth loop. Use the latest data snapshot. Run 5 rounds. Append one row per round to results.tsv and write final_variants.md with two distinct variants for review.
```

When using Agent Analytics, collect a snapshot:

```bash
bash <skill_dir>/scripts/collect_agent_analytics_snapshot.sh my-site signup cta_click
```

If `<skill_dir>` is not obvious in the runtime, read the script from this skill's `scripts/` folder and run an equivalent local command.

## References

Load these files only when needed:

- `references/program.md` - exact loop instructions.
- `references/brief-template.md` - project brief template.
- `references/final-variants-template.md` - final output template.
- `references/results-header.txt` - exact `results.tsv` header.

## Loop Shape

### Inner Autoresearch Loop

1. Define the surface, control, audience, product truth, metric, proxy, and guardrails.
2. Collect or read a dated analytics snapshot.
3. Summarize useful signals and data limitations.
4. Generate candidate A.
5. Critique A harshly for genericness, drift, unsupported claims, weak conversion intent, and competitor-sayable language.
6. Write candidate B from the critique.
7. Synthesize AB from the strongest parts of A and B.
8. Blind-rank A, B, and AB with Borda scoring.
9. Append one TSV-safe row to `results.tsv`.
10. Repeat several rounds.
11. Write `final_variants.md` with two distinct variants and the recommended experiment shape.

### Outer Experiment Loop

Only run this phase when the user explicitly approves implementation or experiment setup.

1. Implement the approved variant or variants in the target product surface.
2. Create the experiment with a control and the approved candidate variants.
3. Verify tracking for the primary metric, proxy metric, and guardrails.
4. Let the experiment collect real behavior for the requested window.
5. Pull experiment results, screenshots or changed-copy notes, funnel movement, guardrails, and data limitations into a new snapshot.
6. Start the next inner autoresearch loop from that measured evidence.

The outer loop prevents the LLM panel from becoming the final judge. LLMs generate and criticize, humans approve risk, and users decide what worked.

## Agent Analytics Snapshot

Use the official CLI when collecting live Agent Analytics data:

```bash
npx --yes @agent-analytics/cli@0.5.31 insights "$PROJECT_SLUG" --period 7d
npx --yes @agent-analytics/cli@0.5.31 pages "$PROJECT_SLUG" --since 7d
npx --yes @agent-analytics/cli@0.5.31 funnel "$PROJECT_SLUG" --steps "page_view,$PROXY_EVENT,$PRIMARY_EVENT" --since 7d
npx --yes @agent-analytics/cli@0.5.31 events "$PROJECT_SLUG" --event "$PROXY_EVENT" --days 7 --limit 50
npx --yes @agent-analytics/cli@0.5.31 events "$PROJECT_SLUG" --event "$PRIMARY_EVENT" --days 7 --limit 50
npx --yes @agent-analytics/cli@0.5.31 experiments list "$PROJECT_SLUG"
```

If login is needed, prefer the regular `agent-analytics` skill's browser approval or detached login guidance.

Before interpreting the snapshot, also read the compact project memory:

```bash
npx --yes @agent-analytics/cli@0.5.31 context get "$PROJECT_SLUG"
```

If the autoresearch run reveals durable product truth that should guide future analytics, use the regular `agent-analytics` skill's project context workflow to read the existing context, merge the compact update, and write it back. Do not store raw round notes or time-bound metric values as project context.

## Scoring

Use Borda scoring:

- first place: 2 points
- second place: 1 point
- third place: 0 points

Judge by:

- specificity to the product
- clarity for the target audience
- likely primary-event intent
- preservation of product truth
- low competitor-sayable language
- fit with analytics data
- respect for guardrails

## Output

`final_variants.md` must include:

- candidate_1
- candidate_2
- exact changed copy
- rationale
- risks
- recommended experiment name
- experiment shape
- data limitations
- clear note that the experiment has not been wired yet

Only create or wire an experiment after explicit human approval.
