---
name: ESG Sustainability Analyzer
slug: esg-sustainability-analyzer
description: Enterprise ESG and sustainability analysis skill. Generates ESG reports with carbon footprint calculation, regulatory compliance checks across GRI/CSRD/ISSB frameworks, supply chain sustainability scoring, and peer benchmarking against industry leaders.
version: 1.0.0
author: ai-gaoqian
tags:
  - esg
  - sustainability
  - carbon-footprint
  - compliance
  - corporate-governance
metadata:
  openclaw:
    requires: "python>=3.10, openclaw>=0.9.0"
---

# ESG Sustainability Analyzer

Enterprise-grade Environmental, Social, and Governance (ESG) analysis skill. Helps organizations measure, report, and improve their sustainability performance across all three ESG pillars.

## Usage

```
esg: analyze company [Company Name] for fiscal year 2025
esg: calculate carbon footprint from [data file or URL]
esg: check compliance with CSRD requirements
esg: benchmark against [Industry] peers
esg: generate sustainability report
```

## Execution Flow

1. **Data Collection** — Gather company disclosures, emission data, energy usage, social metrics, governance policies from uploaded documents or public filings
2. **Carbon Footprint** — Calculate Scope 1/2/3 emissions using GHG Protocol methodology; identify emission hotspots
3. **Regulatory Check** — Cross-reference against CSRD (EU), ISSB (global), SEC climate rules (US), TCFD recommendations; flag gaps
4. **Social Scoring** — Evaluate diversity metrics, labor practices, community impact, human rights policies
5. **Governance Audit** — Board composition, executive compensation, shareholder rights, anti-corruption measures
6. **Benchmarking** — Compare scores against industry averages and top-quartile performers
7. **Report Generation** — Structured ESG report with scores, visualizations, compliance gaps, and improvement roadmap

## Output Format

```markdown
# ESG Sustainability Report: [Company Name]
**Reporting Period**: FY2025
**Framework**: GRI + CSRD + ISSB

## Overall ESG Score: 72/100 (Bronze)

### Environmental (E): 68/100
- Scope 1: 1,200 tCO2e
- Scope 2: 3,450 tCO2e
- Scope 3: 12,800 tCO2e (estimated)
- Energy Mix: 35% renewable

### Social (S): 75/100
- Gender Diversity: 38% women in leadership
- Employee Turnover: 12%
- Community Investment: $2.3M

### Governance (G): 73/100
- Independent Directors: 67%
- ESG Committee: Yes
- Whistleblower Policy: Yes

## Compliance Gaps
- CSRD: Missing double materiality assessment
- ISSB: Scope 3 disclosure incomplete

## Improvement Roadmap
1. Implement double materiality assessment (Q3 2026)
2. Increase renewable energy to 60% by 2027
3. ...
```

## Notes

- Data quality determines report accuracy; flag assumptions clearly
- Regulatory frameworks are updated quarterly; check for latest versions
- Benchmarking requires industry classification and peer selection
- Supports PDF report export with charts and infographics
