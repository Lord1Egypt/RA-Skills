---
name: research-assistant
version: "1.0.0"
description: Structured web research framework for AI agents. Teaches your agent to conduct multi-source research, synthesize findings into actionable briefs, maintain a research library, and track evolving topics over time. Use when you need market research, competitor analysis, topic deep-dives, or ongoing monitoring of trends and news. Works with any agent that has web search capabilities.
tags: [research, web-search, analysis, monitoring, intelligence]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Research Assistant

**By [The Agent Ledger](https://theagentledger.com)** — Subscribe for more agent skills and premium blueprints.

Turn your AI agent into a structured research analyst. No more copy-pasting search results — your agent learns to plan research, cross-reference sources, synthesize findings, and maintain an evolving knowledge base.

---

## What This Skill Does

- **Structured Research Protocol** — Plan → Search → Evaluate → Synthesize → Store
- **Research Brief Format** — Consistent, scannable output for every research task
- **Source Quality Scoring** — Teaches your agent to evaluate and rank sources
- **Research Library** — Organized storage for findings that persists across sessions
- **Topic Monitoring** — Track evolving topics with periodic re-research
- **Competitor/Market Analysis Templates** — Ready-to-use frameworks

---

## Setup (5 Minutes)

### Step 1: Create Research Directory

```
research/
├── README.md          ← Library index (auto-maintained)
├── briefs/            ← Completed research briefs
├── monitoring/        ← Topics being tracked over time
└── templates/         ← Custom research templates (optional)
```

### Step 2: Create `research/README.md`

```markdown
# Research Library

## Recent Briefs
<!-- Agent maintains this list automatically -->

## Monitored Topics
<!-- Topics being tracked with periodic updates -->

## Quick Stats
- Total briefs: 0
- Active monitors: 0
- Last research: never
```

### Step 3: Add to Your Agent Instructions

Add to your `AGENTS.md`, `SOUL.md`, or system prompt:

```
## Research Protocol

When asked to research something:
1. Read `research/README.md` for existing work on this topic
2. Follow the Research Protocol below
3. Save the brief to `research/briefs/YYYY-MM-DD-<slug>.md`
4. Update `research/README.md` index
```

---

## Research Protocol

### Phase 1: Plan

Before searching, define:
- **Research Question** — What specifically are we trying to answer?
- **Scope** — Broad survey or deep dive? Time range? Geography?
- **Sources Needed** — How many independent sources for confidence?
- **Output Format** — Brief, comparison table, recommendation, or raw dump?

### Phase 2: Search & Collect

Execute searches with these principles:
- **Multiple queries** — Rephrase the question 2-3 ways for coverage
- **Source diversity** — Mix official sources, industry analysis, community discussion
- **Recency check** — Note publication dates; flag anything older than 6 months
- **Contradiction hunting** — Actively look for sources that disagree

### Phase 3: Evaluate Sources

Score each source on:

| Factor | Weight | Criteria |
|--------|--------|----------|
| Authority | High | Known publication? Expert author? Official source? |
| Recency | High | Published within relevant timeframe? |
| Specificity | Medium | Concrete data/examples vs. vague claims? |
| Corroboration | Medium | Do other sources confirm this? |
| Bias Check | Low | Obvious commercial or political motivation? |

Drop sources scoring poorly on Authority + Recency. Flag but keep sources with clear bias if they contain unique data.

### Phase 4: Synthesize

Structure findings into a Research Brief (see format below). Key rules:
- **Lead with the answer** — Don't bury the conclusion
- **Quantify when possible** — Numbers > adjectives
- **Flag uncertainty** — Clearly mark low-confidence claims
- **Note gaps** — What couldn't you find? What needs deeper research?

### Phase 5: Store & Index

Save to `research/briefs/YYYY-MM-DD-<slug>.md` and update the library index.

---

## Research Brief Format

```markdown
# [Research Question]

**Date:** YYYY-MM-DD
**Requested by:** [context]
**Confidence:** High / Medium / Low
**Staleness risk:** [when this research might become outdated]

## TL;DR
[2-3 sentence executive summary with the key finding]

## Key Findings

### Finding 1: [Title]
[Detail with supporting evidence]
- Source: [name] ([link]) — [date]
- Confidence: High/Medium/Low

### Finding 2: [Title]
[Detail with supporting evidence]
- Source: [name] ([link]) — [date]
- Confidence: High/Medium/Low

[Continue as needed]

## Data Points
| Metric | Value | Source | Date |
|--------|-------|--------|------|
| [key stat] | [value] | [source] | [date] |

## Contradictions & Caveats
- [Any conflicting information found]
- [Limitations of this research]

## Knowledge Gaps
- [What we couldn't find]
- [What needs deeper investigation]

## Sources
1. [Full citation with URL and access date]
2. [...]

## Recommendations
- [Actionable next steps based on findings]

---
*Research conducted by AI agent using the Research Assistant skill by [The Agent Ledger](https://theagentledger.com)*
```

---

## Topic Monitoring

For topics that evolve over time (market trends, competitor moves, regulatory changes):

### Setup a Monitor

Create `research/monitoring/<topic-slug>.md`:

```markdown
# Monitoring: [Topic Name]

**Started:** YYYY-MM-DD
**Frequency:** [daily / weekly / bi-weekly]
**Search queries:** 
- "[query 1]"
- "[query 2]"
**Alert triggers:** [what constitutes a notable change]

## Updates

### YYYY-MM-DD
- [What changed since last check]
- [New data points]
- [Assessment: significant / minor / no change]
```

### Periodic Check Protocol

When running a monitoring check:
1. Read the monitor file for context and previous findings
2. Run the saved search queries
3. Compare new results against last update
4. Only log if something changed or enough time has passed
5. Flag significant changes prominently

### Integration with Heartbeats/Cron

Add to your `HEARTBEAT.md` or set up a cron:

```
## Research Monitors
Check research/monitoring/ for topics due for refresh.
Only check topics whose frequency interval has elapsed.
```

---

## Specialized Templates

### Competitor Analysis

```markdown
# Competitor Analysis: [Company/Product]

**Date:** YYYY-MM-DD

## Overview
| Factor | Competitor | Us |
|--------|-----------|-----|
| Pricing | | |
| Features | | |
| Market position | | |
| Strengths | | |
| Weaknesses | | |

## Their Recent Moves
- [Latest product launches, pivots, funding]

## Opportunities
- [Gaps we can exploit]

## Threats
- [Where they're ahead]
```

### Market Sizing

```markdown
# Market Analysis: [Market Name]

**Date:** YYYY-MM-DD

## Market Size
- **TAM:** $X ([source])
- **SAM:** $X ([source])
- **SOM:** $X (our estimate)
- **Growth rate:** X% CAGR ([source])

## Key Players
| Player | Est. Share | Notes |
|--------|-----------|-------|
| | | |

## Trends
1. [Trend + supporting evidence]

## Entry Barriers
- [What makes this hard]

## Our Angle
- [How we'd compete]
```

### Decision Research

```markdown
# Decision: [What we're deciding]

**Date:** YYYY-MM-DD
**Decision needed by:** YYYY-MM-DD

## Options
### Option A: [Name]
- **Pros:** 
- **Cons:**
- **Cost:** 
- **Risk level:** High/Medium/Low

### Option B: [Name]
- **Pros:**
- **Cons:**
- **Cost:**
- **Risk level:** High/Medium/Low

## Recommendation
[Which option and why]

## What would change our mind
[Conditions that would flip the recommendation]
```

---

## Customization

### Adjust Research Depth

Add to your agent instructions:

```
Research depth levels:
- **Quick scan** — 3-5 sources, 5 minutes, key facts only
- **Standard brief** — 8-12 sources, full brief format
- **Deep dive** — 15+ sources, include academic/primary sources, extended analysis
Default to standard unless specified.
```

### Domain-Specific Research

For specialized fields, add context:

```
When researching [your domain]:
- Prioritize sources from: [trusted sources list]
- Key metrics to always check: [domain-specific KPIs]
- Common pitfalls: [domain-specific biases to watch for]
```

### Citation Style

```
Citation preference: [choose one]
- Inline links (default) — [Source Name](url)
- Numbered footnotes — [1], [2], etc.
- Academic — Author (Year). Title. Publication.
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Research is too surface-level | Increase depth level; add "find primary sources" to prompt |
| Too many sources, no synthesis | Emphasize Phase 4; ask for "TL;DR first, then details" |
| Findings are outdated | Add recency filter: "only sources from last 6 months" |
| Agent dumps raw search results | Reinforce the brief format; remind to synthesize, not copy |
| Monitor checks too frequent | Adjust frequency in monitor file; use staleness risk to guide |
| Research library getting messy | Run periodic cleanup: archive briefs older than 6 months |

---

## Integration with Other Agent Ledger Skills

- **[Solopreneur Assistant](https://theagentledger.com)** — Feed research into business decisions and opportunity scoring
- **[Daily Briefing](https://theagentledger.com)** — Include monitor alerts in daily briefings
- **[Project Tracker](https://theagentledger.com)** — Link research briefs to project milestones
- **[Memory OS](https://theagentledger.com)** — Store key research insights in long-term memory

---

*Part of the free skill library by [The Agent Ledger](https://theagentledger.com). Subscribe for premium blueprints, playbooks, and the complete agent configuration guide.*

*License: CC-BY-NC-4.0*

> *DISCLAIMER: This skill was created by an AI agent. It is provided "as is" for informational and educational purposes only. It does not constitute professional, financial, legal, or technical advice. Review all generated files before use. The Agent Ledger assumes no liability for outcomes resulting from use. Use at your own risk.*
