# Patent Report Auto-Research System
**Started:** April 4, 2026 - 17:45 UTC  
**Duration:** 12 hours  
**Iterations:** Up to 7  

---

## Research Framework

### Goal
Iteratively improve the DMG Mori Patent Intelligence Report using data-driven hypotheses and independent review.

### Process
```
Hypothesis → Data Gathering → Implementation → Review → Decision → Next Iteration
```

### Success Criteria
1. **Quantifiable metrics** (not subjective opinions)
2. **Independent review** (separate agent evaluation)
3. **Persistent storage** (Obsidian vault for cross-referencing)
4. **R&D head relevance** (strategic value, not just cosmetic)

---

## Iteration Log

### Iteration 1: Time-Series Competitor Analysis
**Hypothesis:** Adding historical patent publishing trends by competitor will help R&D heads understand which competitors are accelerating/decelerating innovation in specific technology areas.

**Data Needed:**
- Multi-week patent collection from same competitors
- Publication date analysis
- Technology categorization over time
- Competitor velocity metrics

**Implementation:**
- Modify report generator to include trend charts
- Add competitor activity timeline
- Create "accelerating/decelerating" indicators

**Review Criteria:**
- Does it provide actionable intelligence?
- Is the data presentation clear?
- Would an R&D head use this for strategic decisions?

---

## Storage Locations

### Obsidian Vault
- **Patent Analysis:** `vault/PPS/Patents/YYYY-MM-DD_[patent_id].md`
- **Competitor Profiles:** `vault/PPS/Competitors/[company_name].md`
- **Technology Trends:** `vault/PPS/Trends/[category].md`
- **Iteration Notes:** `vault/PPS/Research/iteration-N.md`

### Database
- Primary: `data/patents.db` (SQLite)
- Analysis: To be extended with trend tables

---

## Review Agent Instructions

The review agent will:
1. Compare current vs. previous report version
2. Score on 5 criteria (1-10 scale):
   - Actionability for R&D decisions
   - Data clarity
   - Strategic insight value
   - Visual presentation
   - Completeness
3. Provide specific improvement suggestions
4. Make KEEP/DISCARD recommendation
5. NOT know which version is newer (blind review)

---

## Current Status

**Baseline (Iteration 0):**
- 48 patents from 10+ companies
- Static weekly snapshot
- Company statistics (count only)
- Basic patent cards with abstracts
- Espacenet links working

**Next:** Begin Iteration 1 - Hypothesis testing for time-series analysis