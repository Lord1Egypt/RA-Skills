---
name: ecommerce-pulse-board
description: Synthesize ecommerce operational health across channels, inventory, marketing efficiency, customer metrics, and fulfillment into a single operator pulse brief. Use when founders, ops leads, or channel managers need a periodic health-check summary that surfaces what is working, what is at risk, and what needs immediate attention — without live BI, ERP, or dashboard API integrations.
---

# Ecommerce Pulse Board

## Overview

Use this skill to generate a structured operational pulse brief from rough KPI notes, multi-channel context, and operational observations. It applies a built-in ecommerce health framework across five pillars — traffic, conversion, inventory, marketing efficiency, and fulfillment — to surface signal, risk, and priority action items in one readable digest.

This MVP is heuristic. It does **not** connect to live analytics platforms, ad dashboards, ERPs, or order management systems. It relies on the user's provided KPI notes, channel mix, and operational context.

## Trigger

Use this skill when the user wants a:
- daily or weekly operational pulse check across all ecommerce channels
- monthly executive health brief for a brand or store
- post-campaign operational debrief covering inventory, fulfillment, and margin side effects
- rapid health scan before a board meeting, investor update, or team sync
- structured digest when data is partial or non-standard across channels

### Example prompts

- "Give me a pulse check on our Shopify and Amazon operations this week"
- "Create a monthly ecommerce health brief from these KPI notes"
- "Run a quick health scan before our investor update"
- "What should our ops team be paying attention to this week?"

## Workflow

1. Capture the review window, channels in scope, and the user's main concern or question.
2. Organize KPI notes and operational observations into the five health pillars.
3. Score each pillar (green / yellow / red) with supporting evidence.
4. Surface the top 3 priority signals and recommended owner actions.
5. Return a markdown pulse brief.

## Inputs

The user can provide any mix of:
- review window: daily, weekly, monthly, post-campaign, quarterly
- channel mix: Shopify, Amazon, TikTok Shop, JD, Taobao, WeChat, Weidian, other
- KPI notes: GMV, net revenue, orders, AOV, refund rate, ROAS, CPC, inventory levels, stockout SKUs
- operational context: staffing, warehouse delays, campaign context, product launch
- main concern or question: e.g., "Are we on track for Q2 targets?" or "Did the promo hurt margin?"

## Outputs

Return a markdown pulse brief with:
- pulse summary: overall health score, review window, and main story in 3 sentences
- pillar health grid: traffic, conversion, inventory, marketing efficiency, fulfillment — each scored and annotated
- signal of the week: the single most important observation and what it means
- risk watchlist: top 2-3 at-risk areas with likely cause and recommended owner
- priority actions: 3-5 specific, operator-ready next steps with owner assignment
- channel spotlight: per-channel pulse for each channel in scope
- data quality note: what was confirmed, what was inferred, and what needs verification

## Safety

- No live analytics, ad platform, ERP, or OMS access.
- Health scores are directional unless comprehensive data is provided.
- Do not fabricate KPI values or claim live data access.
- Strategic budget, pricing, and inventory decisions remain human-approved.

## Best-fit Scenarios

- founders and ops leads who need a quick weekly or monthly health check without dashboard tooling
- teams with fragmented data across platforms that need a single structured digest
- post-campaign or seasonal debriefs that need an operational lens beyond pure media metrics

## Not Ideal For

- real-time operational monitoring, automated alerting, or live KPI dashboards
- enterprises requiring formal financial reporting or audit-grade data reconciliation
- situations where data is so incomplete that any health score would be misleading

## Acceptance Criteria

- Return markdown text.
- Include pillar health grid, signal of the week, risk watchlist, and priority actions.
- Cover at least 3 of the 5 health pillars.
- Make data-quality assumptions explicit when inputs are partial.
- Keep the brief practical for founders, ops leads, and channel managers.
