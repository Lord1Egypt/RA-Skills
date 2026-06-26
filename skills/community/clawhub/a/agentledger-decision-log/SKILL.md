---
name: decision-log
version: "1.0.2"
description: AI-powered decision journal for solopreneurs — capture decisions with context, rationale, and expected outcomes, then review them later to learn from what you got right and wrong.
tags: [decisions, journal, learning, accountability, retrospective, strategy, solopreneur, judgment, decision-making, review]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Decision Log

Stop making the same expensive mistakes. Start learning from the ones you've already made.

**by The Agent Ledger** — [theagentledger.com](https://theagentledger.com)

---

## The Problem

Most solopreneurs make dozens of meaningful decisions every week — which products to build, which clients to take, which tools to use, which strategies to pursue. They almost never write them down. Six months later, when a decision goes sideways, the context is gone: what were the alternatives? What did you expect to happen? Why did you choose this over that?

The result: you can't learn systematically from your own experience. You repeat mistakes. You forget what worked and why.

This skill turns your agent into a decision journal. Capture any decision in seconds. Get a structured record with context, alternatives, expected outcomes, and confidence level. Then, on a schedule you set, your agent reviews past decisions against what actually happened and surfaces patterns in your judgment.

---

## Setup

### Step 1 — Create Your Decisions Directory

```bash
mkdir -p decisions/
```

### Step 2 — Create Your Decision Index

Create `decisions/INDEX.md`:

```markdown
# Decision Log

**Started:** [date]
**Total decisions logged:** 0
**Last review:** —

---

## Open Decisions (awaiting outcome)

| ID | Date | Decision | Category | Expected Outcome | Review Date |
|----|------|----------|----------|-----------------|-------------|
| — | — | — | — | — | — |

---

## Reviewed Decisions

| ID | Date | Decision | Category | Outcome | Verdict | Lesson |
|----|------|----------|----------|---------|---------|--------|
| — | — | — | — | — | — | — |

---

## Patterns (updated during reviews)

*Will be filled in by your agent after the first batch of reviews.*
```

### Step 3 — Create Your First Decision Entry

Each decision gets its own file: `decisions/YYYY-MM-DD-short-title.md`

Template:

```markdown
# Decision: [Short Title]

**ID:** DEC-[001]
**Date:** [YYYY-MM-DD]
**Category:** [business / product / operations / financial / personal / hiring / strategy]
**Status:** open

---

## The Decision

[What did you decide? Be specific. One sentence if possible.]

---

## Context

[What was happening when you made this decision? What problem were you solving? What constraints existed?]

---

## Alternatives Considered

1. **Option A (chosen):** [description]
   - Pros: [list]
   - Cons: [list]

2. **Option B:** [description]
   - Pros: [list]
   - Cons: [list]

3. **Option C (do nothing):** [description]
   - Why rejected: [reason]

---

## Why I Chose This

[The actual reasoning. Not the polished version — the real one. What tipped the scale?]

---

## Expected Outcome

[What do you expect to happen if this was the right call? Be specific and measurable where possible.]

**Time horizon:** [When will you know if this was right? 30 days? 6 months? 1 year?]

---

## Confidence Level

**Rating:** [1-10]
**Why:** [What would make this more or less confident?]

---

## Risk / Downside

[If this is wrong, what's the worst case? How recoverable is it?]

---

## Review Scheduled

**Review date:** [YYYY-MM-DD based on time horizon above]
**Review prompt:** "Check decision DEC-[001] — was [expected outcome] realized?"

---

## Outcome Review

*Fill in when reviewing:*

**Reviewed:** [date]
**What actually happened:** [description]
**Verdict:** ✅ Right call / ⚠️ Partially right / ❌ Wrong call / 🔄 Too early to tell
**Lesson:** [What would you do differently? What did you learn about your judgment?]
```

### Step 4 — Configure Your Agent

Add to your agent's instructions or AGENTS.md:

```markdown
## Decision Log

I maintain a decision journal in `decisions/`. When I make a significant decision:

1. Create a new entry: `decisions/YYYY-MM-DD-short-title.md`
2. Use the decision log template
3. Update `decisions/INDEX.md` with the new entry
4. Flag for review at the appropriate horizon

**Log decisions when:**
- Spending more than $100 on a tool, service, or ad campaign
- Starting or stopping a project
- Taking on or declining a client/partnership
- Choosing between two meaningful strategies
- Making a hiring/contractor decision
- Any choice I'll want to revisit in 90+ days

**Do not log:**
- Routine operational choices (which tool to use for a small task)
- Decisions that are immediately reversible with no material cost
- Personal/lifestyle choices (unless I ask you to track them)

**Weekly prompt (optional):** "Check decisions/INDEX.md for any decisions with a review date this week."
```

---

## Logging a Decision (Quick Capture)

When you're in a hurry, give your agent this prompt:

```
Log a decision: [what you decided]. Category: [category]. Why: [brief reason]. Expected: [outcome]. Review in: [timeframe].
```

Your agent will create a properly formatted entry, assign an ID, and update the index.

---

## The Review Protocol

### Weekly Review (5 minutes)

Ask your agent:

```
Check decisions/INDEX.md for any open decisions with a review date this week or earlier. For each one, ask me: what actually happened?
```

Your agent will pull each due decision, prompt you for the outcome, fill in the verdict and lesson, and move it to the reviewed section.

### Monthly Pattern Analysis

Ask your agent:

```
Review all decisions in decisions/ logged in the last 90 days. Identify:
1. My verdict breakdown (% right / partial / wrong)
2. Which categories I'm most accurate in
3. Which categories I'm least accurate in
4. Any repeated mistakes or blind spots
5. My calibration: am I overconfident or underconfident relative to my confidence ratings?

Summarize findings in decisions/PATTERNS.md.
```

### Quarterly Decision Retrospective

Add to your quarterly review:

```
Pull decisions/PATTERNS.md and all decisions from this quarter. Write a 1-page decision retrospective:
- My best decision this quarter (and why)
- My worst decision this quarter (and what I missed)
- The pattern I most need to address
- One rule I'm adding to my decision-making process
```

---

## Decision Categories

Use consistent categories for meaningful pattern analysis:

| Category | Use For |
|----------|---------|
| `business` | Business model, positioning, pivots |
| `product` | What to build, features, prioritization |
| `operations` | Tools, processes, systems |
| `financial` | Spending, pricing, investment |
| `marketing` | Channels, campaigns, messaging |
| `partnership` | Clients, collaborators, vendors |
| `hiring` | Contractors, employees, agencies |
| `strategy` | Long-term direction, market entry |
| `personal` | Work style, schedule, habits |

---

## Confidence Calibration Guide

Use this to rate decisions consistently:

| Score | Meaning |
|-------|---------|
| 9-10 | Near certain. Strong evidence, low complexity, proven pattern. |
| 7-8 | High confidence. Good evidence, manageable unknowns. |
| 5-6 | Moderate confidence. Mixed signals or real uncertainty. |
| 3-4 | Low confidence. Mostly a bet. Limited evidence. |
| 1-2 | Essentially a guess. High uncertainty, no clear evidence. |

Track your calibration over time: if your "7s" only pan out 40% of the time, you're overconfident. If your "4s" pan out 80% of the time, you're underconfident. Good calibration is when your 7s hit ~70% of the time.

---

## Integration With Other Agent Ledger Skills

This skill works well alongside:

- **solopreneur-assistant** — Log decisions surfaced in your weekly business review
- **goal-tracker** — Tag decisions that affect quarterly goals; review whether decisions moved the needle
- **project-tracker** — Log project go/no-go decisions and major pivots
- **research-assistant** — Research briefs inform decision context; link briefs to decision entries

**Cross-skill pattern:** When your goal-tracker flags a missed KR, ask your agent to pull any decisions logged in that goal's category during the quarter. Often the root cause of a missed goal is a bad decision logged months earlier — now you have the receipt.

---

## Customization Options

### Track Only High-Stakes Decisions

Raise the threshold in your agent instructions:

```markdown
Only log decisions involving: >$500 spend, >10 hours of effort commitment, or any choice I explicitly flag as "log this."
```

### Add Stakeholder Field

For decisions that affect others:

```markdown
**Stakeholders:** [who else is affected or needs to know]
**Communicated:** yes / no / partial
```

### Add Emotional State

For decisions where cognitive bias is a real risk:

```markdown
**Emotional state when deciding:** [rushed / calm / anxious / excited / frustrated]
```

Over time, your agent can correlate emotional state with decision quality. Most solopreneurs find their worst decisions happen when rushed or excited.

### Public Accountability Mode

Share a sanitized decision log in your newsletter:

```
Pull my last 5 reviewed decisions from decisions/. Summarize the lesson from each in one sentence, anonymizing any sensitive details. Format for a newsletter section called "What I Got Wrong This Month."
```

---

## File Structure

```
decisions/
├── INDEX.md                          # Decision inventory + patterns
├── PATTERNS.md                       # Quarterly pattern analysis (agent-generated)
├── 2026-03-01-launch-channel.md      # Example: "Which channel to launch on first"
├── 2026-03-05-pricing-model.md       # Example: "Subscription vs one-time pricing"
└── 2026-04-02-contractor-hire.md     # Example: "Hire VA or DIY content creation"
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Decision entries are too vague | Ask agent: "Make me fill in the 'Why I Chose This' field before creating the entry — don't let me skip it" |
| Review dates pile up | Add a weekly recurring reminder or heartbeat check for due reviews |
| Index gets out of sync | Ask agent: "Scan decisions/ and rebuild INDEX.md from actual files" |
| Patterns analysis is shallow | Make sure you have at least 10 reviewed decisions before running pattern analysis |
| I'm logging too many decisions | Raise the threshold — only log decisions you'd want to justify to a board |

---

## Why This Works

Most "decision journals" fail because they require too much friction at capture time and provide no structured review. This skill solves both problems:

1. **Low-friction capture** — Quick-capture prompt gets you a full entry in under 2 minutes
2. **Automatic review prompts** — Review dates are set at capture time, not whenever you remember
3. **Pattern analysis** — Your agent synthesizes across entries, surfacing insights you'd never see manually
4. **Calibration tracking** — Over time you build a data-driven model of your own judgment quality

The goal isn't to second-guess every decision. It's to get 10% smarter per quarter by learning systematically from your own track record.

---

## License

CC-BY-NC-4.0 — Free to use and share with attribution. Not for resale.

**by The Agent Ledger** | [theagentledger.com](https://theagentledger.com)

> Premium skills, playbooks, and the complete Agent Blueprint guide are available at theagentledger.com. Subscribe to the newsletter for release announcements.

---

> *DISCLAIMER: This skill was created by an AI agent. It is provided "as is" for informational and educational purposes only. It does not constitute professional, financial, legal, or technical advice. Review all generated files before use. The Agent Ledger assumes no liability for outcomes resulting from use. Use at your own risk.*
