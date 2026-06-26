---
name: npd-methodology
description: >
  Reference documentation for the NPD validation methodology including scoring rubrics,
  dimension definitions, verdict thresholds, and report templates. Loaded by evaluator
  subagents and the orchestrator. Do not invoke directly — use /npd-validator:validate-product instead.
disable-model-invocation: true
---

# NPD Validation Methodology Reference

## Scoring Framework — 15 Dimensions

| Evaluator | Dim 1 | Dim 2 | Dim 3 |
|---|---|---|---|
| Market Demand | Category Size & Growth | Demand Signals | Timing |
| Competitive Intel | White Space | Competitor Weakness | Barriers to Entry |
| Brand Fit | Brand Alignment | Portfolio Coherence | Audience Fit |
| Commercial Viability | Pricing Power | Unit Economics | Channel Fit |
| Consumer & Trends | Social Sentiment | Trend Momentum | Cultural Fit |

Each dimension scored 1–10 with confidence rating (HIGH/MEDIUM/LOW).
Minimum 150 words reasoning per dimension with cited sources.

## Composite Score Weights (default)

| Perspective | Weight |
|---|---|
| Market Demand | 25% |
| Competitive Intelligence | 20% |
| Brand Fit | 15% |
| Commercial Viability | 25% |
| Consumer & Trends | 15% |

**Custom weights**: If the user specifies different priorities (e.g., "brand fit matters more for us"), adjust weights accordingly. When custom weights are used: (1) document them in the report header alongside the composite score, (2) note the default weights for comparison, (3) recalculating with new weights does NOT require re-running evaluators — only the Consensus Director needs to re-synthesize.

## Verdict Thresholds

| Composite | Verdict | Action |
|---|---|---|
| 7.5–10.0 | **GO** | Proceed to development |
| 5.5–7.4 | **CONDITIONAL GO** | Proceed if conditions met |
| 3.5–5.4 | **REVISIT** | Significant rework needed |
| 1.0–3.4 | **NO-GO** | Redirect resources |

## Override Rules

- **Fatal Flaw Override**: Any dimension ≤2 after deliberation AND devil's kill shot ≥7 → downgrade one level
- **Confidence Override**: >50% dimensions LOW confidence → append "(LOW CONFIDENCE)" to verdict
- **Devil's Advocate Override**: Kill shot ≥8 AND composite in CONDITIONAL range → downgrade to REVISIT

**Stacking**: Overrides do NOT compound. Apply all against the original mechanical verdict, take the most conservative result. Max one level downgrade from overrides.

## Research Depth Standards

- Research Coordinator: 8–12 web searches
- Each Evaluator: 3–5 additional web searches minimum
- Devil's Advocate: 3–5 adversarial searches
- Total per validation: 25–40+ searches
- Cross-reference claims across multiple sources
- Cite everything with URLs
- Mark LOW confidence when evidence is thin

## Concept Brief Template

```
PRODUCT CONCEPT BRIEF
═════════════════════
Product Name / Working Title: [...]
Category:                     [...]
One-Line Description:         [≤15 words]
Target Consumer:              [...]
Price Point Range:            [...]
Key Differentiator:           [...]
Launch Horizon:               [now / 6 months / 12 months / 24+ months — specify target month if seasonal]
Brand Context (optional):     [...]
```

**Launch Horizon** is critical for the Timing dimension. A trend that looks perfect to enter "now" may have peaked 18 months before a late 2027 launch. Always capture this — if the user doesn't specify, ask before running the pipeline.

## B2B vs B2C Products

The methodology applies to both, but **B2B products require evaluator adaptation**. Detect B2B when the Target Consumer is another business (manufacturers, retailers, distributors, professional users like salons/dentists/labs) rather than end consumers.

When validating B2B products:
- **Market Demand** — size the B2B buyer market (how many potential customers exist), not the end-consumer market
- **Competitive Intel** — analyze competing suppliers/vendors, not consumer brands. Pricing is typically per-kg/per-MT/per-seat, not retail
- **Brand Fit** — B2B credibility comes from industry certifications, trade show presence, partnerships, case studies, and white papers — NOT consumer brand alignment
- **Commercial Viability** — B2B has long sales cycles, volume-based pricing, contract terms (MOQ, payment terms, exclusivity), channel partner margins
- **Consumer & Trends** — "social sentiment" for B2B lives in trade publications, LinkedIn, industry conferences (Cosmoprof, in-cosmetics for beauty B2B), formulator forums — NOT TikTok or Reddit consumer threads

The scoring rubrics and dimensions are the same; the RESEARCH TARGETS shift. If the brief doesn't make B2B vs B2C clear, ask before launching the pipeline.

## Evaluation Output Template

Each evaluator writes their output in this format:

```markdown
# [Perspective] Evaluation
Product: [Name]
Date: [Date]

## Scores Summary
| Dimension | Score | Confidence |
|---|---|---|
| [Dim 1] | [X]/10 | [H/M/L] |
| [Dim 2] | [X]/10 | [H/M/L] |
| [Dim 3] | [X]/10 | [H/M/L] |
| **Subtotal** | **[avg]/10** | |

## Detailed Assessment
### [Dim 1]: [X]/10 [Confidence]
[150+ words with evidence and sources]

### [Dim 2]: [X]/10 [Confidence]
[150+ words with evidence and sources]

### [Dim 3]: [X]/10 [Confidence]
[150+ words with evidence and sources]

## Key Findings
- [Top 3 findings]

## Risks & Uncertainties
- [What could change this assessment]

## Sources
- [Source](URL)
```

For detailed evaluator instructions, see the individual agent prompt files in
`skills/npd-methodology/agents/`.
