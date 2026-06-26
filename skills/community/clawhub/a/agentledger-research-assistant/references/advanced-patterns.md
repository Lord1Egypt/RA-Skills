# Research Assistant — Advanced Patterns

**By [The Agent Ledger](https://theagentledger.com)**

---

## 1. Research Chains

Link multiple research tasks into a pipeline where each step feeds the next.

```
Research Chain: Market Entry Analysis
├── Step 1: Market sizing (broad survey)
├── Step 2: Competitor deep dive (based on key players from Step 1)
├── Step 3: Regulatory scan (based on market from Step 1)
├── Step 4: Pricing analysis (using competitor data from Step 2)
└── Step 5: Go/no-go recommendation (synthesize all steps)
```

**Implementation:** Create a chain file in `research/chains/`:

```markdown
# Chain: [Name]
**Status:** In progress (Step 2 of 5)

## Steps
1. [x] Market sizing → `briefs/2026-01-15-market-size.md`
2. [ ] Competitor analysis → (pending)
3. [ ] Regulatory scan → (pending)
4. [ ] Pricing analysis → (depends on #2)
5. [ ] Go/no-go → (depends on all)
```

---

## 2. Source Networks

Build a curated list of trusted sources by domain. Your agent learns which sources are reliable over time.

```markdown
# Source Network: [Domain]

## Tier 1 — Primary / Official
- [Source name] — [URL] — [what they're good for]

## Tier 2 — Expert Analysis
- [Source name] — [URL] — [what they're good for]

## Tier 3 — Community / Anecdotal
- [Source name] — [URL] — [what they're good for]

## Blacklist — Known Unreliable
- [Source name] — [reason to distrust]
```

Store in `research/source-networks/<domain>.md`. Reference when starting domain-specific research.

---

## 3. Research Retrospectives

After a decision is made based on research, circle back to evaluate accuracy.

```markdown
# Retrospective: [Original Research Brief]

**Original brief:** `briefs/YYYY-MM-DD-<slug>.md`
**Decision made:** [what was decided]
**Outcome date:** YYYY-MM-DD

## Accuracy Check
| Finding | Predicted | Actual | Accurate? |
|---------|-----------|--------|-----------|
| [key claim] | [what we said] | [what happened] | ✅/❌ |

## Lessons
- [What the research got right]
- [What it missed and why]
- [How to improve next time]

## Source Quality Review
- [Which sources were most accurate]
- [Which sources were misleading]
- [Update source network accordingly]
```

---

## 4. Collaborative Research

When multiple agents or humans contribute to research:

### Research Handoff Format

```markdown
# Research Handoff: [Topic]

**From:** [who did the initial work]
**To:** [who's continuing]
**Date:** YYYY-MM-DD

## What's Done
- [Completed research steps]
- [Key findings so far]

## What's Needed
- [Specific remaining questions]
- [Suggested sources to check]
- [Deadline or urgency level]

## Files
- Current brief: `briefs/YYYY-MM-DD-<slug>.md`
- Raw notes: [if applicable]
```

### Multi-Agent Research

Split research across specialized agents:

```
Research Assignment: New Product Launch
├── Market Agent → Market sizing + competitor scan
├── Legal Agent → Regulatory requirements + compliance
├── Finance Agent → Cost analysis + pricing models
└── Coordinator → Synthesize into launch recommendation
```

---

## 5. Automated Research Triggers

Set up conditions that automatically kick off research:

### Price/Market Triggers

```markdown
# Auto-Research Triggers

## Trigger: [Name]
**Condition:** [what triggers it]
**Action:** Run [research template] and save to [location]
**Notify:** [who to alert]

Examples:
- "If competitor launches new product → run competitor analysis template"
- "If market metric crosses threshold → run market update brief"
- "If regulatory news appears → run regulatory scan"
```

### News-Driven Research

During monitoring checks, if a significant event is detected:

1. Flag the event in the monitor file
2. Automatically create a new research brief using the relevant template
3. Link the brief back to the monitor entry
4. Alert the user if the finding meets alert trigger criteria

---

## 6. Research Quality Metrics

Track your agent's research quality over time:

```markdown
# Research Quality Log

| Date | Brief | Sources | Confidence | Retrospective Score | Notes |
|------|-------|---------|------------|-------------------|-------|
| YYYY-MM-DD | [slug] | 8 | High | 4/5 | [lesson] |
```

**Scoring:**
- 5/5 — Findings fully confirmed, no surprises
- 4/5 — Mostly accurate, minor gaps
- 3/5 — Key finding correct but missed important nuances
- 2/5 — Significant misses that affected the decision
- 1/5 — Research was misleading

---

## 7. Knowledge Graph Building

Over time, connect research briefs into a knowledge graph:

```markdown
# Knowledge Map: [Domain]

## Entities
- **[Entity A]** — First appeared in `brief-1.md`, updated in `brief-5.md`
- **[Entity B]** — First appeared in `brief-2.md`

## Relationships
- Entity A → competes with → Entity B (source: `brief-3.md`)
- Entity A → acquired → Entity C (source: `brief-7.md`)

## Timeline
- YYYY-MM — [Key event] (source: `brief-X.md`)
- YYYY-MM — [Key event] (source: `brief-Y.md`)
```

This turns individual research briefs into compounding intelligence — each new brief adds to the map rather than starting from scratch.

---

## 8. Research Budgeting

For agents with rate-limited API access to search tools:

```markdown
# Research Budget

## Daily Limits
- Web searches: X remaining / Y total
- Page fetches: X remaining / Y total

## Priority Queue
1. [Urgent research — use budget here first]
2. [Important but can wait]
3. [Nice to have — only if budget allows]

## Efficiency Tips
- Batch related queries together
- Check research library before searching (might already have it)
- Use monitoring updates instead of full re-research
- Cache frequently-referenced sources locally
```

---

*Part of the free skill library by [The Agent Ledger](https://theagentledger.com). Subscribe for premium blueprints and the complete agent configuration guide.*

*License: CC-BY-NC-4.0*
