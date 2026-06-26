---
name: financial-services-source-attribution
description: >
  Use when finalizing any financial deliverable, before claiming analysis is complete. Requires every number, ratio, and claim to trace back to a specific source document or data provider. The verification gate for financial accuracy.
metadata:
  openclaw:
    emoji: "🔗"
---

# Source Attribution

每个数字必须追溯到源文档。这是金融分析的信任基础。

**Announce at start:** "I'm using the source-attribution skill to verify all data sources."

## The Iron Law

```
NO FINANCIAL CLAIM WITHOUT SOURCE CITATION
```

If you cannot point to the specific document, page, cell, or data provider where a number came from, do not include it.

## Core Principle

金融决策基于数据。不可追溯的数据是不可信的。源归因不是"加分项"，而是交付的前提条件。

**This skill is RIGID. Do not adapt away the discipline.**

## The Verification Gate

Before any financial deliverable leaves your hands:

```
1. SCAN: Review every number in the deliverable
2. TRACE: Each number → source document + location
3. CITE: Add citation in standard format
4. VERIFY: Cross-check critical numbers against 2nd source if available
5. FLAG: Mark any unverifiable numbers as [UNVERIFIED] or remove them
```

## Citation Format

**Standard format:**
```
[Number] — [Source], [Date], [Location/Reference]
```

**Examples:**
```
Revenue: $4.2B — 10-K Filing, FY2025, p.38
EBITDA Margin: 24.3% — FactSet, as of 2026-03-31
Beta: 1.15 — Bloomberg, 2-year weekly, as of 2026-05-01
WACC: 9.2% — Author calculation, components: [see WACC tab]
Comparable EV/EBITDA: 12.5x median — S&P Capital IQ, peer set [see Comps tab]
```

**In Excel workbooks:**
- Add a "Sources" tab listing all data sources with retrieval dates
- Use cell comments on key cells to note source
- Use consistent source abbreviations (define in Sources tab)

**In PowerPoint decks:**
- Source footnote on every data slide: "Source: [provider], [date]"
- Detailed sources in appendix if space is limited

## Source Categories

| Category | Acceptable Sources | Unacceptable |
|----------|-------------------|--------------|
| Financial statements | 10-K, 10-Q, annual report, audited financials | Press releases alone, unaudited management estimates |
| Market data | Bloomberg, Refinitiv, FactSet, S&P Capital IQ | Unattributed web searches, Wikipedia |
| Valuation multiples | Capital IQ, FactSet consensus, PitchBook | Single analyst estimate, blog posts |
| Industry data | IBISWorld, Gartner, company filings, government stats | Marketing materials, unverified reports |
| Macro data | Federal Reserve, BLS, IMF, World Bank | News articles, social media |
| Calculations | Your own model (cite inputs and methodology) | Unverified calculations from third parties |

## Cross-Verification Rules

**Critical numbers (must cross-verify):**
- Revenue, EBITDA, Net Income from financial statements
- Share price and market cap (check date alignment)
- WACC components (risk-free rate, beta, ERP)
- Valuation multiples from comps or precedent transactions
- Covenant ratios (verify against both financial data AND covenant terms)

**Cross-verification method:**
```
Primary source: 10-K filing, FY2025, Revenue = $4.2B
Secondary source: FactSet, FY2025 Revenue = $4.2B ✓
If mismatch: investigate, document discrepancy, use audited source
```

## Handling Missing Sources

When you cannot find a source for a number:

1. **Search harder** — check alternative data providers, filings, presentations
2. **Estimate explicitly** — if you must estimate, mark clearly:
   ```
   Estimated: [Number] — Author estimate based on [methodology]
   Confidence: [High/Medium/Low]
   ```
3. **Remove** — if neither source nor reliable estimate available, do not include

**Never:**
- Present an estimate as a sourced fact
- Use a number without noting if it's estimated
- Cite a source you haven't actually checked

## Common Violations

| Violation | Fix |
|-----------|-----|
| "Revenue grew 15%" without source | "Revenue grew 15% — 10-K, FY2025 vs FY2024, p.38" |
| Using "approximately" without basis | State exact number + source, or mark as estimated |
| Copying numbers from chat/summary without verification | Verify against primary source before using |
| Mixing fiscal year and calendar year without noting | Explicitly state: "FY2025 (ended Jan 2026)" |
| Stale data without date | Always include "as of [date]" |
| Calculation without showing inputs | Show formula and input sources |

## The Bottom Line

Financial analysis without source attribution is opinion, not analysis.

Every number. Every time. No exceptions.

## Verification Checklist

Before marking any financial deliverable complete:

- [ ] Every financial metric has a source citation
- [ ] Critical numbers cross-verified against 2nd source
- [ ] Sources tab/footnote included in deliverable
- [ ] All data dates specified (no stale data without noting)
- [ ] Estimates clearly marked as estimates with methodology
- [ ] No unverifiable numbers remain in deliverable
- [ ] Citation format is consistent throughout
