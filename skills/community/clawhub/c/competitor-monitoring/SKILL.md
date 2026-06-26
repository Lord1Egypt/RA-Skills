---
name: Competitor Monitoring
slug: competitor-monitoring
version: 1.0.0
homepage: https://clawic.com/skills/competitor-monitoring
description: Track competitors with pricing alerts, feature changes, positioning analysis, and strategic dossiers.
changelog: Initial release with tracking, alerts, dossiers, and analysis.
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidelines.

## When to Use

User needs competitive intelligence. Agent tracks competitors, monitors changes, analyzes positioning, and maintains strategic dossiers with pricing, features, and market moves.

## Architecture

Memory lives in `~/competitor-monitoring/`. See `memory-template.md` for structure.

```
~/competitor-monitoring/
├── memory.md           # Status + preferences + active competitors
├── competitors/        # Individual dossiers
│   ├── {company}.md    # Per-competitor intelligence
│   └── ...
├── alerts/             # Triggered alerts
│   └── YYYY-MM-DD.md   # Daily alert log
└── analysis/           # Strategic analyses
    └── {topic}.md      # Comparison reports
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |

## Core Rules

### 1. Check Dossiers Before Acting
Before any competitor question, load the relevant `competitors/{company}.md` file. Build on existing intelligence, don't start fresh each time.

### 2. Track These Signals
| Signal | Where to Look | Impact |
|--------|---------------|--------|
| Pricing changes | Pricing page, announcements | Direct competitive threat |
| New features | Changelog, blog, social | Capability gap/parity |
| Positioning shifts | Homepage copy, ads | Market narrative |
| Hiring patterns | Jobs page, LinkedIn | Strategic direction |
| Funding/acquisitions | News, Crunchbase | Resource changes |

### 3. Alert Priorities
- **Critical:** Pricing undercut, feature that blocks your advantage
- **High:** Major feature launch, positioning change
- **Medium:** Blog posts, minor updates, team changes
- **Low:** Social activity, routine content

### 4. Maintain Signal-to-Noise
Don't report everything. Only surface changes that require action or awareness. If nothing actionable happened, say so.

### 5. Compare Objectively
When analyzing competitors, be honest about their strengths. Acknowledge where they're ahead. False confidence leads to bad strategy.

**Framework:**
```
For each competitor, answer honestly:
- Where are they better than us?
- What do their customers love that ours don't have?
- If I were a customer, why would I choose them?
```

### 6. Update Dossiers Proactively
After any research or mention of a competitor, update their dossier. Don't wait for explicit instructions.

### 7. Connect to Strategy
Every observation should connect to "so what?" What does this mean for user's positioning, roadmap, or priorities?

**Template:**
```
OBSERVATION: Competitor X launched feature Y
SO WHAT: This means...
→ For our roadmap: [accelerate/deprioritize/ignore]
→ For positioning: [adjust messaging/double down/no change]
→ For sales: [new objection/new advantage/neutral]
```

## Monitoring Patterns

### Regular Check-ins
```
Weekly: Scan pricing pages, homepages, changelogs
Monthly: Deep dive on positioning, feature comparison
Quarterly: Full competitive landscape review
```

### Trigger-Based
- User mentions competitor → refresh dossier
- Industry news → check all relevant competitors
- User launches feature → compare to competitor alternatives

## Competitor Dossier Structure

Each `competitors/{company}.md` contains:
- Company overview (what they do, target market)
- Pricing (current, historical changes)
- Features (core, recent additions)
- Positioning (messaging, differentiation)
- Strengths (honest assessment)
- Weaknesses (opportunities to exploit)
- Recent moves (last 90 days)
- Watch list (what to monitor)

## Analysis Types

### Head-to-Head
Compare user vs one competitor. Feature matrix, pricing, positioning.
```
User vs Acme Corp:
- Pricing: We're 40% cheaper for same features
- Features: They have X, we have Y (differentiated)
- Positioning: They target enterprise, we target SMB
→ Our wedge: Simpler and cheaper for smaller teams
```

### Landscape
Map all competitors by segment. Who's premium, who's cheap, who's niche.
```
Market Map (example):
├── Premium ($500+/mo): BigCorp, EnterpriseCo
├── Mid-market ($100-500): CompetitorA, CompetitorB
├── SMB ($20-100): Us, StartupX
└── Free/Freemium: OpenSourceY
→ Gap: No one owns "professional but affordable"
```

### Trend
How is the competitive space evolving? What's the direction?
- Watch for: New entrants, funding rounds, pivots, acquisitions
- Pattern recognition: Are competitors moving upmarket? Going vertical?

### Gap
Where are opportunities nobody's addressing?
- Underserved segments
- Features everyone complains about but nobody fixes
- Adjacent markets competitors ignore

## Common Traps

- **Vanity metrics obsession** → Tracking social followers instead of pricing/features. Social numbers don't predict competitive moves.
- **Confirmation bias** → Ignoring competitor strengths because you don't want to see them. Honest assessment beats false confidence.
- **Information overload** → Reporting every blog post and tweet. Filter for actionable signals, not noise.
- **Stale dossiers** → Intelligence from 6 months ago is worse than no intelligence. Update after every mention.
- **Missing indirect competitors** → Watching direct rivals but ignoring substitutes. Spreadsheets compete with project management tools.
- **Reactive only** → Only checking competitors when something breaks. Proactive monitoring catches threats early.
- **Single source** → Only watching their website. Combine: pricing page, changelog, blog, jobs, social, reviews.

## Security & Privacy

**Data that stays local:**
- All competitor dossiers stored in `~/competitor-monitoring/`
- Analysis reports and alert history
- User preferences and monitoring settings

**What happens on first use:**
- Creates folder `~/competitor-monitoring/` with your data
- Asks how you want monitoring to work (proactive vs on-demand)

**This skill does NOT:**
- Access competitor internal systems
- Scrape data in violation of ToS
- Store credentials or sensitive tokens
- Send your data externally

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `market-research` — broader market analysis
- `business` — strategic frameworks
- `analytics` — data analysis patterns

## Feedback

- If useful: `clawhub star competitor-monitoring`
- Stay updated: `clawhub sync`
