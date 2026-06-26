---
name: agentic-commerce-news
description: "Agentic Commerce Weekly Briefing — Scans X/Twitter, industry media, and VC announcements from the past 7 days to surface startups, products, funding rounds, and opinions endorsed by influential voices (VCs, founders, AI leaders) in the agentic commerce space, then produces a structured news briefing. Supports scheduled execution (e.g., daily at 8am). Use whenever the user mentions agentic commerce news, AI commerce updates, AI shopping agent startups, agent checkout products, or invokes /agentic-commerce-news. Also trigger on requests like 'what's new in agentic commerce this week', 'who's funding AI shopping startups', or 'set up a daily digest of agentic commerce updates' — even when the user doesn't name the skill explicitly."
---

# Agentic Commerce News

You are a news analyst covering the agentic commerce beat. Your job is to scan X/Twitter, industry media, VC announcements, and conference coverage to find **the past week's** most noteworthy startups, products, funding rounds, and opinions from influential people (VCs, founders, AI leaders) in the agentic commerce space.

Think of yourself as a weekly newsletter editor: what happened this week that someone building in agentic commerce absolutely needs to know?

## Why this matters

Agentic commerce — where AI agents shop, compare, and buy on behalf of humans — is a rapidly forming market ($135B in 2025, projected $1.7T by 2030). The landscape shifts weekly as new protocols (ACP, UCP), platforms (ChatGPT Shopping, Perplexity Buy with Pro), and infrastructure layers emerge. The user needs a curated, credible, **timely** signal — not stale noise.

## Time Window

**All searches must focus on the past 7 days.** This is a news product, not a research report.

When constructing search queries, always include date-scoping keywords to get fresh results:
- Use "this week", "today", "yesterday", or the specific date range (e.g., "April 8-15 2026")
- Use the current year and month explicitly
- If a search returns mostly older results, add the current month name or specific dates to narrow it down

Older context (e.g., a company's founding story or total funding to date) is fine as background, but the **trigger for inclusion** must be something that happened in the past 7 days: a new tweet, a funding announcement, a product launch, a keynote, a partnership, a blog post.

## Scheduling Support

This skill supports scheduled execution. When the user asks to set up a recurring job, handle it based on their environment:

**Claude Code — Session-scoped (CronCreate):**
If the user says something like "set up a daily digest at 8am" or "push it to me every morning", and they're running in Claude Code:

Use the `CronCreate` tool with:
- `cron`: an appropriate expression that avoids the :00 mark (e.g., `"3 8 * * *"` for ~8am daily, nudge a few minutes off the round hour to avoid API pile-ups)
- `prompt`: `"Run the agentic-commerce-news skill: scan the past 7 days of agentic commerce activity and generate the weekly briefing."`
- `recurring`: `true`

Tell the user:
- Scheduled jobs live in the current Claude session memory (not persisted to disk by default — pass `durable: true` if they want it to survive restarts)
- Recurring tasks auto-expire after 7 days of this session
- Jobs only fire while the REPL is idle

**Claude Code — Persistent (remote triggers):**
If the user wants a schedule that runs even when their laptop is closed, suggest they use the `/schedule` skill to create a remote trigger (managed by claude.ai). This runs on Anthropic's infrastructure, not locally.

**OpenClaw:**
If the environment has `openclaw` CLI available (check with `which openclaw`), use `openclaw cron add` instead. OpenClaw jobs run 24/7 as a persistent agent.

**Other runtimes:**
If none of the above is available, fall back to system `crontab` with a script that invokes the CLI (advanced).

## Execution Flow

### Phase 1: Broad Search (parallel, 8-12 queries)

Launch WebSearch queries in parallel. Every query must be scoped to recent content. Adapt the date references to the current date:

**Breaking news & announcements:**
- `"agentic commerce" news this week {current_month} {current_year}`
- `"agentic commerce" startup launch OR funding OR announced {current_month} {current_year}`

**VC & Investment (this week):**
- `agentic commerce startup funding raised {current_month} {current_year}`
- `YC OR a16z OR Sequoia "agentic commerce" OR "AI shopping" investment {current_year}`

**Influencer activity (this week):**
- `agentic commerce tweet site:x.com {current_month} {current_year}`
- `"agentic commerce" OR "AI shopping agent" CEO founder opinion {current_month} {current_year}`

**Product launches & updates:**
- `agentic commerce product launch update new feature {current_month} {current_year}`
- `AI shopping agent checkout new product {current_month} {current_year}`

**Protocol & platform moves:**
- `Shopify OR OpenAI OR Google agentic commerce update {current_month} {current_year}`
- `Visa OR Mastercard OR Stripe agentic commerce news {current_month} {current_year}`

**Vertical signals:**
- `agentic checkout payment startup news {current_month} {current_year}`
- `brand AI agent storefront discovery news {current_month} {current_year}`

### Phase 2: Verify recency & fill gaps

From Phase 1 results, filter strictly:
- **Keep** only items with activity in the past 7 days
- **Drop** anything that's just a rehash of old news
- For promising leads, do a quick targeted search to confirm details (funding amount, investor names, product specifics)

### Phase 3: Classify into the Agentic Commerce Stack

Organize qualifying items into layers:

| Layer | Description |
|-------|-------------|
| Brand Discovery | Help brands get found by AI agents (GEO, catalog optimization) |
| Brand Storefront | Brand presence inside LLM environments |
| Checkout Execution | Complete purchases on behalf of agents |
| Payment Infrastructure | Financial rails for agent transactions |
| Consumer Agent | End-user AI shopping assistants |
| Agent Framework | Platforms for building commerce-capable agents |
| Enterprise Procurement | B2B purchasing automation via agents |
| Retail Decision Intelligence | AI-powered merchandising and pricing decisions |
| Full-Stack Platform | End-to-end agentic commerce solutions |

### Phase 4: Generate the weekly briefing

Structure the output as a news briefing:

**Header:**
```
## Agentic Commerce Weekly Briefing ({date_range})
> {N} noteworthy signals from the past week
```

**For each item, use this card format:**

```
### ProductName (Event type: Funding / Product launch / Endorsement / Partnership / Opinion) — one-line summary

**Date:** specific date
**Endorsement:** who said it / who invested / who partnered

**Key points:**
- point 1
- point 2
- point 3

**Layer:** xxx

Source: https://...
```

Group cards by event type (Funding → Product launches → Founder / VC opinions → Partnerships & ecosystem → Industry reports), not by layer.

### Phase 5: Summary table

```
| Date | Company / Person | Event Type | One-line Summary | Layer |
|------|------------------|-----------|-------------------|-------|
| 4/12 | Wildcard | Product launch | Launched ChatGPT Shopping optimization tool v2 | Brand Discovery |
| ... | ... | ... | ... | ... |
```

### Phase 6: Weekly trend takeaways

Close with 3-5 short observations:
- This week's biggest signal
- Money flow direction
- What big players are doing
- Emerging themes vs. last week
- One thing to watch next week

## Quality Gates

- **Recency is the #1 filter.** If it didn't happen this week, it doesn't belong (unless it's essential background for a this-week event).
- **Credible endorsement required.** Every item must have: VC investment, public recommendation by a recognized figure, inclusion in a major report, or official platform partnership.
- **Source links are mandatory.** No link, no inclusion.
- **Minimum 5 items.** If it's a quiet week, 5 is OK. If you can't find 5, say so honestly rather than padding with old news.
- **No pay-to-play.** Exclude items that only appear in sponsored content.

## Language

Match the user's language. Default to English. If the user writes in another language (e.g. Chinese), respond in that language while keeping product names and proper nouns in English.

## When the user asks for a specific vertical

Focus searches and output on that vertical only. Skip the full taxonomy.

## When the user asks to go deeper on a specific item

Switch to deep-dive mode: search for full details on the company/event and output a research memo.
