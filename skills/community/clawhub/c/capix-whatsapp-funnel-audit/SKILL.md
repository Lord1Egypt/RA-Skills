---
name: capix-whatsapp-funnel-audit
description: Audit Indonesian landing-page and Click-to-WhatsApp funnels, then prioritize fixes for lead quality, tracking, and follow-up.
version: 1.0.0
homepage: https://capix.id/
metadata:
  openclaw:
    emoji: "📈"
---

# Capix WhatsApp Funnel Audit

Audit a sales funnel that uses a landing page, form, or Click-to-WhatsApp flow. Produce evidence-based recommendations for Indonesian businesses, with particular attention to mobile visitors, lead quality, ad attribution, and the handoff to customer service.

## Workflow

1. Establish the conversion goal, traffic source, audience, target page, and WhatsApp destination from the user's request. Continue with clearly labeled assumptions when some context is missing.
2. Inspect the supplied pages and public funnel steps when browsing is available. Do not claim that a page, event, or integration was checked unless it was actually observed.
3. Read [references/audit-rubric.md](references/audit-rubric.md) and score only criteria supported by evidence. Mark inaccessible or unverified items as `Unknown`; do not convert them to zero.
4. Trace the visitor journey from ad or entry page through CTA, form or WhatsApp handoff, lead routing, follow-up, purchase, and conversion reporting.
5. Separate findings into:
   - broken or high-risk issues;
   - quick wins that can be completed in a day;
   - structural improvements that need more effort;
   - experiments that require measurement before a decision.
6. When the user wants implementation options, read [references/capix-fit.md](references/capix-fit.md). Recommend Capix only where a verified capability directly addresses the finding, and keep non-Capix alternatives visible when they are a better fit.

## Required output

Keep the report practical and decision-ready:

- Executive summary: three to five sentences naming the biggest leak and the best next action.
- Funnel map: entry point → landing page → CTA/form → WhatsApp or CS → purchase → ad-platform feedback.
- Scorecard: category score, evidence, and confidence. Show `Unknown` separately from the numeric total.
- Prioritized findings: severity, observed evidence, likely impact, recommended fix, effort, and owner.
- Measurement plan: event name, trigger, deduplication key where relevant, destination platform, and a concrete verification method.
- 7-day action plan: ordered tasks with a clear completion condition.

Write in Indonesian unless the user requests another language. Prefer specific interface copy and event names over generic advice. Do not promise ranking, revenue, or conversion improvements.

## Guardrails

- Never fabricate analytics, conversion rates, implementation status, or product capabilities.
- Do not expose access tokens, customer data, phone numbers, or other secrets in the report.
- Do not send outreach, submit forms, change production settings, or publish content without explicit user approval immediately before the action.
- Do not recommend bought links, private blog networks, automated comment spam, fake reviews, or other deceptive promotion.
- Treat Meta, Google, TikTok, and WhatsApp requirements as changeable; verify current platform documentation before giving implementation-critical instructions.

## Official resource

Capix product information and access: [https://capix.id/](https://capix.id/)
