---
name: commerce-bi-copilot
description: Turn ecommerce exports, KPI notes, and natural-language business questions into metric alignment notes, anomaly diagnoses, operator-ready summaries, and prioritized next actions for founders, operators, and analysts. Use when reviewing GMV, net revenue, ROAS, refund rate, inventory health, channel mix, or campaign performance without live BI connectors or SQL access.
---

# Commerce BI Copilot

## Overview

Use this skill to convert fragmented commerce data context into an operator-friendly insight brief. It is designed for teams that need quick explanations, not a heavyweight dashboard rebuild.

This MVP is heuristic. It does **not** access live warehouses, ad APIs, ERP systems, or real spreadsheets. Instead, it applies a commerce metric dictionary, anomaly checklist, and action-planning framework to the user's provided notes.

## Trigger

Use this skill when the user wants to:
- explain why a KPI moved up or down
- prepare a daily, weekly, campaign, or executive business review
- align teams on metric definitions such as GMV, net revenue, ROAS, MER, or refund rate
- turn rough exports or pasted KPI notes into a concise action brief
- produce follow-up questions for an analyst, founder, or agency client

### Example prompts
- "Why did GMV drop 12% this week?"
- "Create a weekly ecommerce business review from these KPI notes"
- "Help me explain falling ROAS after our spring promotion"
- "Turn these Shopify, Meta, and refund notes into an executive summary"

## Workflow

1. Capture the business question, time frame, and referenced channels.
2. Normalize the likely metric set and call out any definition ambiguity.
3. Build a short driver tree across traffic, conversion, pricing, refunds, inventory, and mix.
4. Produce prioritized drill-downs and next actions.
5. Return a markdown brief that a founder or operator can immediately use.

## Inputs

The user can provide any mix of:
- pasted KPI snapshots or rough metric notes
- mentions of data sources such as Shopify, Amazon, Meta Ads, Google Ads, GA4, ERP, or CRM
- campaign or calendar context, such as promotions, launches, or stockouts
- business questions about revenue, efficiency, refunds, margin, or channel contribution
- audience context, such as founder update, operator review, or agency client recap

## Outputs

Return a markdown brief with:
- analysis mode and source assumptions
- KPI snapshot table
- likely driver tree
- recommended drill-downs
- prioritized next best actions
- executive-ready summary bullets
- assumptions and limitations

## Safety

- Do not pretend to read live numbers or source files.
- Surface metric-definition ambiguity when GMV, net revenue, refunds, or attribution may conflict.
- Avoid certainty when the input is partial or anecdotal.
- Keep budget, pricing, inventory, and operational decisions human-approved.

## Examples

### Example 1
Input: Shopify orders, Meta spend notes, and the question "Why did yesterday GMV fall?"

Output: identify a likely mix of traffic decline, conversion weakness, or stock issues, then recommend the next drill-downs and immediate operator actions.

### Example 2
Input: weekly KPI notes for channels, refunds, and top products.

Output: generate a compact weekly business brief with risks, wins, and next-week priorities.

## Acceptance Criteria

- Return markdown text.
- Include KPI, diagnosis, and action sections.
- Mention evidence gaps or metric ambiguity when relevant.
- Keep the output practical for operators and founders.
