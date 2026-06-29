---
name: Carbon & ESG Analyst
slug: carbon-esg-analyst
description: Carbon footprint calculation and ESG reporting assistant. Computes Scope 1/2/3 emissions, generates sustainability reports aligned with GRI/SASB/TCFD standards, and provides decarbonization roadmap recommendations.
version: 1.0.0
author: ai-gaoqian
tags:
  - carbon
  - esg
  - sustainability
  - emissions
  - climate
  - reporting
  - gri
  - net-zero
metadata:
  openclaw:
    requires: openclaw>=2.0.0
---

# Carbon & ESG Analyst - Sustainability Intelligence Skill

## Core Capabilities

| Capability | Description |
|---|---|
| Carbon Accounting | Calculate Scope 1, 2, and 3 emissions from operational data inputs |
| ESG Report Generator | Generate structured sustainability reports per GRI, SASB, TCFD frameworks |
| Net-Zero Roadmap | Create step-by-step decarbonization strategies with milestone tracking |
| Regulatory Check | Cross-check disclosures against latest CSRD, SEC climate rules, ISSB standards |
| Carbon Credit Advisory | Evaluate carbon offset projects and credit quality for compliance markets |
| Peer Benchmarking | Compare ESG metrics against industry peers and sector averages |

## Trigger Scenarios

- "Calculate my company's carbon footprint for 2025"
- "Generate an ESG report aligned with GRI standards"
- "What net-zero targets should a manufacturing SME set?"
- "Compare our emissions with industry benchmarks"
- "Evaluate this carbon offset project for credibility"

## Execution Flow

### Phase 1: Data Collection
- Gather energy consumption, transportation, supply chain, and waste data
- Classify data into Scope 1 (direct), Scope 2 (purchased energy), and Scope 3 (value chain)

### Phase 2: Calculation & Analysis
- Apply emission factors from IPCC, EPA, or national databases
- Calculate total emissions in tCO2e with breakdown by scope and category
- Generate year-over-year comparison if historical data available

### Phase 3: Report Generation
- Produce structured report with executive summary, methodology, data tables, and charts
- Map disclosures to GRI/SASB/TCFD indicator codes
- Include recommendations ranked by cost-effectiveness and impact

## Output Template

```
## ESG Analysis Report
**Entity**: [company name]
**Reporting Period**: [YYYY]
**Framework**: [GRI / SASB / TCFD / ISSB]

### Emissions Summary
| Scope | Emissions (tCO2e) | % of Total |
|-------|-------------------|------------|
| Scope 1 | XXX | XX% |
| Scope 2 | XXX | XX% |
| Scope 3 | XXX | XX% |

### Key Findings
[Analysis highlights]

### Recommendations
[Prioritized actions with estimated impact]

### Compliance Status
[Gap analysis against regulatory requirements]
```

## Notes

- Emission factor databases cover China, EU, and US regions
- Report generation follows latest 2025-2026 regulatory frameworks
- Carbon credit market data updated quarterly
- Free to use; no code execution required
