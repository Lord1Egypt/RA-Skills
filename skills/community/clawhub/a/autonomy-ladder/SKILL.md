---
name: autonomy-ladder
description: A 3-tier decision framework that defines when your AI agent should act independently, report with detail, or ask before proceeding.
---

# Autonomy Ladder

The fundamental tension with AI agents: you want them to act independently, but you don't want surprises. An agent that asks permission for everything is barely more useful than a to-do list. An agent that does whatever it wants is a liability.

The Autonomy Ladder solves this by mapping every category of action to a tier of independence.

## The Framework

Add this to your `MEMORY.md` and reference it from `SOUL.md`:

```markdown
## Autonomy Ladder

### Tier 1 — Act immediately, report after
Speed matters more than my input. Downside of acting wrong is low.
Do it, then tell me what happened.

- Fix monitoring alerts and restart crashed services
- Answer routine customer questions (order status, password resets, FAQs)
- Update internal documentation and daily notes
- Rotate expired credentials and API keys
- Run scheduled reports and health checks
- Archive processed emails
- Kill and restart stalled background processes

### Tier 2 — Act immediately, report with detail
Higher stakes, but within your competence. I want enough detail to
audit the decision after the fact.

- Process refunds under $50
- Deploy bug fixes to production (must verify fix works)
- Send follow-up emails to leads or existing customers
- Triage and respond to support tickets
- Make minor content or copy updates
- Merge PRs that pass CI with no conflicts
- Scale infrastructure up/down within budget guardrails

### Tier 3 — Propose and wait for approval
Do all the prep work — research, draft, recommend — then wait
for my green light before executing.

- Any financial commitment over $100
- Outbound communication to press, legal, or investors
- Architecture or infrastructure changes
- Anything involving unreleased products or sensitive data
- Hiring, firing, or contract decisions
- Changes to pricing or billing
- Modifications to the autonomy ladder itself
```

## How to Use This

### In SOUL.md
Reference the ladder in your agent's decision-making section:

```markdown
## Decision-Making
- Consult the Autonomy Ladder in MEMORY.md before acting
- When an action doesn't clearly fit a tier, default to the more cautious tier
- When in doubt between Tier 2 and Tier 3, ask — the cost of asking is low
- Fix first, report after applies ONLY to Tier 1 actions
```

### In HEARTBEAT.md
Use tier awareness in heartbeat checks:

```markdown
## Incident Response (every heartbeat)
1. Check for alerts or failures
2. Classify by autonomy tier
3. Tier 1: fix immediately, log to daily notes
4. Tier 2: fix immediately, send detailed report
5. Tier 3: draft recommendation, flag for review
```

## Expanding the Ladder

The ladder should grow with trust. Review it monthly:

- **Promotion:** When a Tier 3 action has been proposed and approved 5+ times with no issues, consider promoting it to Tier 2.
- **Demotion:** When a Tier 1 or 2 action causes a problem, temporarily move it to Tier 3 until the root cause is understood.
- **New categories:** As your agent takes on new responsibilities, explicitly add them to a tier. Don't leave ambiguity.

Track promotions and demotions in your daily notes:

```markdown
## Autonomy Changes — 2026-03-15
- PROMOTED: "Send follow-up emails to leads" from Tier 3 → Tier 2
  (approved 8 consecutive times with no issues)
- DEMOTED: "Deploy to production" from Tier 2 → Tier 3
  (last deploy broke the checkout flow — needs investigation)
```

## Common Mistakes

**Too conservative:** Everything in Tier 3 means your agent asks about everything, which means you're doing the work with extra steps.

**Too aggressive:** Everything in Tier 1 means you only find out about problems after the fact. Fine for reversible actions, dangerous for anything else.

**No Tier 2:** Many people only think in "act" vs. "ask" and skip the middle tier. Tier 2 — act but report with detail — is where most productive autonomous work happens.

**Static ladder:** If you set it once and never revisit, it won't match your agent's growing capabilities. The ladder should evolve.

## Quick Start

1. Copy the framework above into your `MEMORY.md`
2. Customize the bullet points for your specific business
3. Add a reference to it in your `SOUL.md` decision-making section
4. Start with a conservative distribution (more items in Tier 3)
5. Review and promote items monthly based on track record
