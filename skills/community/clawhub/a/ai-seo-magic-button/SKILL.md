---
name: ai-seo-magic-button
description: >
  The one-command magic button for AI-SEO. Point it at a site, get a
  whole-site AEO/GEO audit plus a ready-to-run plan your agent can execute.
  Trigger when the user says "audit my site for AI SEO", "make my site
  citable by ChatGPT/Perplexity/Claude", "AEO/GEO audit", "generate an
  AI-SEO plan", or "improve my AI citation eligibility".
---

# ai-seo-magic-button

The magic button: point it at your site, get a whole-site AEO/GEO audit plus a ready-to-run plan your agent can execute. It produces an actionable PLAN (plan.json + markdown checklist) - not direct edits. You then drive your agent against the plan to execute it.

It is a thin orchestration layer over two engines: the ai-seo MCP (audit + score + rewrite) and the citation-intelligence MCP (what AI engines cite). Both are spawned automatically as subprocesses; you do not call them yourself.

## Setup (once)

This skill shells out to the ai-seo-magic-button CLI. From the product dir:

npm install && npm run build

## The two-step flow

Step 1 - run it (audit then plan). It crawls the site, audits each page, pulls citation gaps, and writes plan.json + plan.md.

Step 2 - execute the plan. Work the items in priority order.

## Rules

- This produces an actionable plan, not direct edits.
- Honour priority. Lead with critical/high items.
- Never recommend blocking AI crawlers.
