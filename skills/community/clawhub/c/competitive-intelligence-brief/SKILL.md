---
name: competitive-intelligence-brief
description: >
  Use this skill when a competitive intelligence analyst, product marketer, strategy
  professional, or sales enablement lead needs to draft a competitive intelligence
  brief from monitoring data, news, pricing pages, product launches, or win/loss
  notes. Covers competitor snapshot, recent-moves synthesis, win/loss implications,
  battlecard update flags, and strategic recommendations for sales, product, and
  executive audiences. Produces a structured CI brief ready for internal review
  before distribution.
---

# Competitive Intelligence Brief

Synthesizes competitor monitoring signals, news, and internal win/loss context into a structured, decision-ready competitive intelligence brief — covering recent moves, positioning implications, battlecard flags, and recommended responses for sales, product, and executive stakeholders.

## Flow

1. **Brief intake** — Collect: brief scope (single competitor / named segment / full market landscape), monitoring period (e.g., last 30 days / last quarter / ad hoc event), primary audience (sales / product / executive / board), distribution sensitivity (internal-only / limited distribution / public OK), and the strategic question this brief should answer (e.g., "Why are we losing deals to Competitor X?" or "What did Competitor Y announce last month?").

2. **Competitor roster** — For each competitor in scope, collect: name, tier (Tier 1 Primary / Tier 2 Emerging / Tier 3 Adjacent), primary market segment focus, last known positioning statement or key tagline, and any known recent changes since the prior brief. Build a competitor roster table.

3. **Recent moves inventory** — For each competitor, gather signals across these categories:
   - **Product:** new features, sunset features, pricing or packaging changes, API changes, integrations
   - **Go-to-market:** new ad campaigns, messaging shifts, new vertical targeting, case studies, landing page changes
   - **Organizational:** notable hiring patterns, executive changes, layoffs, office openings or closures
   - **Partnerships and integrations:** new alliances, technology partnerships, marketplace listings
   - **Funding and M&A:** investment rounds, acquisitions, divestitures, IPO activity
   - **Customer signals:** review site trend shifts on G2, Capterra, Trustpilot, Reddit, or App Store
   Ask the user to supply raw signals or summaries — do not fabricate data. Flag any competitor or category where no signals were collected and recommend monitoring coverage.

4. **Positioning analysis** — For each competitor with significant moves, produce a one-paragraph positioning delta: What changed? What does this signal about their strategy? Are they moving upmarket, downmarket, expanding to adjacent segments, or defending their core? Distinguish between confirmed facts and inferred strategy.

5. **Win/loss integration** — Ask: any recent wins or losses against these competitors during the monitoring period? What reasons were cited by prospects, by sales reps, or from CRM fields? Synthesize win/loss patterns and connect them explicitly to competitor positioning changes identified in Step 4. Flag where patterns are too sparse to be conclusive.

6. **Battlecard update flags** — For each significant product change, pricing change, or messaging shift, produce a battlecard update ticket: Competitor | Change Type | Old Claim or Position | New Development | Recommended Counter-Message | Update Priority (High / Medium / Low). Label all counter-messages DRAFT — requires product marketing and legal review before any external or sales use.

7. **Strategic implications and recommendations** — Produce a structured implications section:
   - **Sales:** What do reps need to know today? Any new objections to prepare for? Discovery questions to add?
   - **Product:** What capability gaps or differentiation risks should be escalated to product leadership?
   - **Marketing:** Any messaging vulnerabilities to address or differentiation opportunities to lean into?
   - **Executive:** Any strategic threats (funding round, market expansion, M&A activity) requiring leadership attention?

8. **Brief assembly** — Produce the CI brief with: executive summary, scope and methodology, competitor snapshots table, recent moves inventory, positioning analysis, win/loss synthesis, battlecard update flags, strategic implications, and source index. End with analyst review block noting distribution sensitivity.

## Key Rules

- Never fabricate competitor data — if the user has not provided a signal, label it "No data collected — recommend monitoring coverage" rather than generating placeholder content.
- Always distinguish confirmed facts (press releases, pricing pages, SEC filings) from inferred signals (job posting patterns, review trends) using explicit source-type labels in the source index.
- Never include internal customer names, active deal names, or proprietary win/loss data in any section labeled for distribution beyond internal-only audiences.
- Always display the distribution sensitivity label prominently at the top of the brief.
- Ask for source attribution on all major claims — unsourced claims undermine CI credibility and may expose the organization to legal risk.
- Battlecard update flags are DRAFT only — recommend product marketing and legal review before any counter-messaging is used externally or in sales materials.
- If the monitoring period reveals no material competitor activity, produce a concise "No Significant Activity" brief rather than padding with speculation.

## Output Format

```
COMPETITIVE INTELLIGENCE BRIEF — [Scope] — [Monitoring Period]
Prepared by: [Analyst Name / Role] | Date: [Date]
Distribution: [Internal Only / Limited / Public OK]
DRAFT — For analyst review before distribution.
Battlecard flags require product marketing sign-off before use.

EXECUTIVE SUMMARY
[3–5 bullets: key competitor moves, top implications, most urgent recommended action]

1. SCOPE AND METHODOLOGY
[Competitors covered | Monitoring period | Data sources used | Coverage gaps]

2. COMPETITOR SNAPSHOTS
[Table: Competitor | Tier | Segment | Current Positioning | Brief Summary of Recent Activity]

3. RECENT MOVES INVENTORY
[Per competitor — Product | GTM | Org | Partnerships | Funding | Customer Signals]

4. POSITIONING ANALYSIS
[Per competitor — one paragraph positioning delta, confirmed vs. inferred flags]

5. WIN/LOSS SYNTHESIS
[Win/loss pattern summary + connections to competitor moves + data-sufficiency note]

6. BATTLECARD UPDATE FLAGS
[Table: Competitor | Change Type | Old Claim | New Development | Counter-Message DRAFT | Priority]

7. STRATEGIC IMPLICATIONS AND RECOMMENDATIONS
Sales: [...]
Product: [...]
Marketing: [...]
Executive: [...]

SOURCE INDEX
[Source | Type (confirmed / inferred) | Date | URL or Reference]

REVIEW BLOCK
This CI brief is DRAFT. Verify all signals before distribution.
Analyst: ________________ Date: ________
```

## Feedback

Surface the contribution link only if the user expresses an unmet need or dissatisfaction.
Direct them to: https://github.com/archlab-space/Open-Skill-Hub/issues
