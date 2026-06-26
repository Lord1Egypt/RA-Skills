---
name: ai-ops-outreach
version: 1.0.0
description: Generate personalized cold outreach messages for AI Operations clients. Based on Reddit research showing "AI ops managed services" is more valuable than "AI agent building."
tags: [outreach, sales, ai-ops, cold-email, client-acquisition]
triggers: ["find ai ops clients", "cold outreach for AI agent services", "AI operations managed services"]
---

# AI Ops Client Outreach Generator

> "Not 'I will build you an agent.' Instead: 'I will run your AI operations so you never have to think about it.'" — Reddit r/Entrepreneur

## Core Positioning

**The problem with "I build AI agents":**
- One-time project, race to the bottom
- Client gets tool they have to manage themselves
- No recurring revenue for you

**The AI Ops model:**
- You OWN the client's AI operations
- They pay monthly for outcomes, not tools
- You fix it when it breaks, update it when context changes
- Recurring revenue, compounding relationships

## Who to Target

### Tier 1 — Solo Founders / Indie Hackers
- Have side projects, no time to manage them
- Want "cofounder who works 24/7"
- Pain: tasks pile up, nothing gets done consistently
- Budget: $200-500/month
- Where to find: Twitter/X, Indie Hackers, Product Hunt

### Tier 2 — Small Agencies
- Need automation but no technical cofounder
- Pain: repetitive tasks eating billable hours
- Budget: $500-1,500/month
- Where to find: LinkedIn, agency forums, cold outreach

### Tier 3 — Consultants / Professionals
- Generate reports, do research, manage clients
- Pain: research and reporting eats all their time
- Budget: $500-2,000/month
- Where to find: LinkedIn, industry communities

## Outreach Message Framework

### Subject Line Options
```
- Your AI operations, handled
- [Name], I run AI agents for [their industry] owners
- Stop doing [task] manually — I automate it
- The "AI cofounder" setup for solo founders
```

### Body Template (3 variants)

**Variant A — Pain-Led**
```
Subject: Stop spending [X] hours/week on [painful task]

Hi [Name],

You're probably spending too much time on [task].

I run AI operations for [type of person] — which means I handle the [task category] so you don't have to think about it.

Most people I work with were doing [specific thing] manually. After 30 days, they get [specific outcome].

No setup fees. $300/month. Cancel anytime.

Worth a 15-min call?
```

**Variant B — Social Proof Led**
```
Subject: The AI ops setup that saved [similar person] 20 hrs/week

Hi [Name],

I manage AI operations for [type of business]. 

One client — a solo founder like you — was spending every Sunday on content. Now AI handles it while she sleeps. Her only job: review what AI produced.

I'm looking for 2 more clients to onboard this month.

Is that interesting?
```

**Variant C — Direct**
```
Subject: AI operations manager available

Hi [Name],

I manage AI agents for [their industry] businesses. My job is to make sure your AI never stops working, never goes off-script, and keeps producing.

$300/month, no contract. I handle everything.

Interested?
```

## Customization Per Client Type

### Solo Founder
- Lead with "cofounder" framing
- Pain points: content, social media, lead research, admin tasks
- Price: $200-500/month

### Agency Owner
- Lead with "automate your repetitive work"
- Pain points: client reporting, lead follow-up, data aggregation
- Price: $500-1,500/month

### Consultant
- Lead with "research and reports on autopilot"
- Pain points: due diligence, market research, competitive analysis
- Price: $500-2,000/month

### E-commerce Operator
- Lead with "never manually check [competitor X] again"
- Pain points: inventory, competitor pricing, customer reviews
- Price: $300-800/month

## Discovery Questions (For Call)

When they respond, qualify with:

1. "What are you spending the most time on that feels repetitive?"
2. "What tools don't talk to each other that should?"
3. "If you had 10 more hours a week, what would you do with them?"
4. "What's preventing you from [their stated goal]?"

## Follow-Up Sequence

After initial message, follow this sequence:

| Day | Action |
|-----|--------|
| Day 1 | Initial message |
| Day 3 | Follow-up: "Did you see this?" |
| Day 7 | Value-add: share relevant article/insight |
| Day 14 | Final: "Worth revisiting?" |

## Output

Generate 3 variants of:
1. Subject line
2. Opening hook
3. Body (2-3 paragraphs)
4. CTA

All personalized to the specific client type and their known pain points.

## Scripts

### `/scripts/generate_outreach.py`
Run: `python3 scripts/generate_outreach.py --client solo_founder --pain "content creation"`

Generates a complete outreach message for the specified client type.

## Security Notes

- Never include API keys or tokens in messages
- Use environment variables for credentials
- Verify email addresses before sending
