# System Context -- competitive-ops

<!-- ============================================================
     THIS FILE IS AUTO-UPDATABLE. Don't put company-specific data here.

     Your customizations go in modes/_profile.md (never auto-updated).
     This file contains system rules, scoring logic, and tool config
     that improve with each competitive-ops release.
     ============================================================ -->

## Sources of Truth

| File | Path | When |
|------|------|------|
| competitors.md | `data/competitors.md` | ALWAYS |
| pricing-snapshots/ | `data/pricing-snapshots/` | ALWAYS |
| swot-analysis/ | `data/swot-analysis/` | ALWAYS |
| profiles/ | `data/profiles/` | ALWAYS |
| _profile.md | `modes/_profile.md` | ALWAYS (user archetypes, narrative, targets) |
| _industry-context.md | `modes/_industry-context.md` | ALWAYS (industry-specific SWOT questions) |

**RULE: NEVER hardcode scores or analysis.** Read from the data files at evaluation time.
**RULE: Read _profile.md AFTER this file. User customizations in _profile.md override defaults here.**

---

## Scoring System

The evaluation uses 6 dimensions with scores from 1-5:

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| Product Maturity | 20% | How mature is the product (GA, beta, MVP, concept) |
| Pricing | 15% | Price point relative to market (5=premium, 1=budget) |
| Market Presence | 15% | Customer base, market share, geographic coverage |
| Feature Coverage | 20% | Breadth and depth of features vs requirements |
| Brand Strength | 10% | Brand recognition, reputation, trust signals |
| Growth Trajectory | 10% | Growth rate, momentum, trajectory |

**Score interpretation:**
- 4.5+ → Strong competitor, high threat
- 4.0-4.4 → Capable competitor, notable threat
- 3.5-3.9 → Moderate competitor, some threat
- 3.0-3.4 → Weak competitor, low threat
- Below 3.0 → Minor player, minimal threat

**Global Score:** Weighted average of all 6 dimensions.

---

## Archetype Detection

Classify every competitor into one of these types:

| Archetype | Key signals |
|-----------|-------------|
| Direct Competitor | Same target market, similar product, overlapping customers |
| Indirect Competitor | Different product but same customer problem, substitute solutions |
| Emerging Threat | New entrant, high growth, technology shift |
| Replacement Threat | Different approach that could replace current solution |
| Adjacent Player | Related market, potential expansion, partnerships |
| Reference Model | Best-in-class example, industry standard, benchmark |

---

## SWOT Analysis Framework

### Strengths (Internal)
- What advantages do they have?
- What do customers say they're best at?
- What resources can they leverage?

### Weaknesses (Internal)
- What could they improve?
- What gaps exist in their offering?
- What do customers complain about?

### Opportunities (External)
- What market trends favor them?
- What emerging needs can they address?
- What partnerships could they form?

### Threats (External)
- What market shifts could hurt them?
- What regulatory changes affect them?
- What new entrants could disrupt them?

---

## Global Rules

### NEVER

1. Invent competitor data or metrics
2. Modify competitor profiles or analysis files
3. Submit analysis without sources
4. Generate reports without research
5. Use outdated data (warn if data > 30 days old)
6. Generate a report without reading competitors.md first
7. Use corporate-speak or marketing fluff
8. Ignore pricing changes (always flag significant changes)

### ALWAYS

0. **Pricing:** ALWAYS check for recent pricing data before scoring. Warn if stale.
1. Read _profile.md, _industry-context.md, and competitors.md before analyzing
2. Detect the competitor archetype and adapt analysis per _profile.md
3. Cite exact sources when scoring
4. Use WebSearch for current data, pricing, news
5. Update competitors.md after analysis
6. Generate content in English (default)
7. Be direct and actionable -- no fluff
8. Include sources in every report
9. **Tracker additions as TSV** -- NEVER edit competitors.md directly. Write to `data/tracker-additions/`.
10. **Include `**Source:**` in every report header with source URL.**

---

## Tools

| Tool | Use |
|------|-----|
| WebSearch | Market research, competitor news, pricing, funding data |
| WebFetch | Fallback for extracting data from static pages |
| TavilySearch | TODO: Deep research integration for comprehensive analysis |
| Playwright | TODO: Browser automation for dynamic content scraping |
| Read | competitors.md, _profile.md, pricing snapshots |
| Write | Analysis reports, competitor entries, pricing snapshots |
| Edit | Update tracker |
| pricing_analyzer.py | Value scoring and pricing change detection (scripts/pricing_analyzer.py) |

### TODO: Tavily Integration
- [ ] Configure Tavily API key in config
- [ ] Implement TavilySearch in analyze mode
- [ ] Fallback to WebSearch if Tavily unavailable

### TODO: Playwright Integration
- [ ] Configure Playwright for dynamic scraping
- [ ] Implement pricing extraction from dynamic pages
- [ ] Verify competitor websites for real-time data

---

## Report Structure

Every analysis report should include:

1. **Header:** Company name, date, archetype, overall score
2. **Executive Summary:** 2-3 sentence overview
3. **Scoring Matrix:** All 6 dimensions with scores and justification
4. **SWOT Analysis:** Four-quadrant analysis
5. **Key Findings:** Top 3-5 insights
6. **Risk Assessment:** Threat level and competitive implications
7. **Sources:** All data sources used

---

## File Structure

```
competitive-ops-v2/
  data/
    competitors.md          # Master competitor list
    pricing-snapshots/      # Pricing history by company
    swot-analysis/          # SWOT reports by company
    profiles/               # Detailed company profiles
    tracker-additions/      # Pending tracker updates
  modes/
    _shared.md              # This file
    _profile.md             # User customization
    add.md                  # Add competitor mode
    analyze.md             # Full analysis mode
    compare.md              # Comparison mode
    update.md               # Update tracking mode
    pricing.md              # Pricing research mode
    batch.md                # Batch processing mode
    report.md               # Report generation mode
    track.md                # Tracker view mode
  reports/                  # Generated reports
  output/                   # Generated PDFs and exports
```
