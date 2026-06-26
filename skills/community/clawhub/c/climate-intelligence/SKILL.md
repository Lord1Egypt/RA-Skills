---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_d5b77d535d8011f19299525400d9a7a1
    ReservedCode1: NFyPHL7+1/b15ykf4mzGjKYohssmJPc2XJZt5jiPtCSssU2tQXUmaqYF3Xn61GWLa8GEa2oa5Bjy3CtugJQ33zBb3zG0ZzwSAcF6V1eZHN4YxprZsORGue5UzEprriWWm//pJaeNxZvmivD9gpfBMrbuMfAPi/P86BRnb1YIud9wRwM66fQUGUGDT8c=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_d5b77d535d8011f19299525400d9a7a1
    ReservedCode2: NFyPHL7+1/b15ykf4mzGjKYohssmJPc2XJZt5jiPtCSssU2tQXUmaqYF3Xn61GWLa8GEa2oa5Bjy3CtugJQ33zBb3zG0ZzwSAcF6V1eZHN4YxprZsORGue5UzEprriWWm//pJaeNxZvmivD9gpfBMrbuMfAPi/P86BRnb1YIud9wRwM66fQUGUGDT8c=
---



# Climate Intelligence Engine

## Capabilities

| # | Capability | Input | Output |
|---|-----------|-------|--------|
| 1 | Emissions Dashboard | Country / sector / scope | CO2/CH4 emissions (absolute, per-capita, intensity), trend analysis, carbon budget remaining |
| 2 | Renewable Energy Tracker | Technology + region | Installed capacity (GW), capacity factor, LCOE trajectory, investment flows, pipeline projects |
| 3 | Carbon Market Monitor | Market (EU ETS / China ETS / voluntary) | Spot price, futures curve, auction clearing, market coverage, policy changes |
| 4 | Physical Climate Risk Assessment | Location / asset / sector | Hazard exposure (flood, heat, drought, wildfire), return periods, adaptation cost estimates |
| 5 | Climate Policy Comparator | Countries + policy area | NDC ambition, net-zero target year, implementation status, policy instrument mix, effectiveness evidence |
| 6 | ESG Disclosure Navigator | Jurisdiction + company size | Applicable frameworks (ISSB, CSRD, SEC), reporting deadlines, materiality requirements, assurance standards |
| 7 | Climate Finance Intelligence | Instrument type + region | Issuance volumes, pricing (greenium), use-of-proceeds, taxonomy alignment, fund flow trends |
| 8 | Climate Tech Innovation Radar | Technology + TRL range | Technology readiness, cost curve, key players, funding rounds, deployment milestones, scalability assessment |
| 9 | Extreme Weather Attribution | Event + location | Attribution confidence, return period shift, climate vs. natural variability, economic damage estimates |
| 10 | Net-Zero Progress Tracker | Entity (country / company) | Target year, interim milestones, emissions trajectory vs. pathway, credibility assessment |

## Workflow

```
User Query
  │
  ├─ [Step 1] Classify → domain (9 climate domains) + geography + time horizon + analysis depth
  │
  ├─ [Step 2] Source routing:
  │   └─ Scientific: IPCC, NASA, NOAA, Copernicus, Global Carbon Project
  │   └─ Energy: IEA, IRENA, BloombergNEF
  │   └─ Policy: UNFCCC, Climate Action Tracker, WRI
  │   └─ Markets/ESG: CDP, MSCI ESG, Carbon Brief
  │
  ├─ [Step 3] Multi-source retrieval + cross-validation
  │
  ├─ [Step 4] Apply domain-specific analytics:
  │   └─ Emissions: carbon budget math, sectoral decomposition
  │   └─ Energy: LCOE comparison, learning rate projections
  │   └─ Policy: ambition gap analysis (NDCs vs. 1.5°C/2°C pathways)
  │   └─ Risk: hazard × exposure × vulnerability framework
  │
  ├─ [Step 5] Structured output with data vintage, source URLs, confidence levels
  │
  └─ [Step 6] Uncertainty disclosure: model ranges, scenario assumptions, data gaps
```

## Output Formats

### Country Emissions Profile
| Metric | Value | Year | Global Rank | Trend (5Y) |
|--------|-------|------|-------------|------------|
| Total CO2 (Gt) | | | | ↑↓→ |
| Per-capita CO2 (t) | | | | |
| CO2 intensity (kg/$GDP) | | | | |
| Methane (MtCO2e) | | | | |
| Cumulative historical (%) | | | | |
| NDC target | | | | |
| Net-zero target year | | | | |

### Carbon Market Dashboard
| Market | Spot Price | 1Y Range | Coverage (% emissions) | Market Stability Mechanism | Key Reform |
|--------|-----------|----------|------------------------|---------------------------|------------|
| EU ETS | €XX | €XX-XX | ~36% | MSR | CBAM phase-in |
| China ETS | ¥XX | ¥XX-XX | ~40% | None yet | Expansion to sectors |
| UK ETS | £XX | £XX-XX | ~28% | Cost Containment | Link to EU? |

### Climate Risk Heatmap
| Hazard | Location | Current Probability | 2050 Projection (RCP 4.5) | 2050 Projection (RCP 8.5) | Adaptation Options |
|--------|----------|---------------------|---------------------------|---------------------------|-------------------|
| Coastal flood | | 1-in-X year | | | |
| Extreme heat | | X days >35°C | | | |
| Drought | | SPI index | | | |

## Usage Guidelines

1. **Scenario transparency** — always specify RCP/SSP scenario (e.g., RCP 4.5, SSP2-4.5) for projections
2. **Data vintage mandatory** — climate data evolves rapidly; flag any data point >6 months old
3. **Uncertainty communication** — report ranges, not point estimates, for projections; cite model ensemble spread
4. **Policy neutrality** — present data and analysis; avoid advocacy language
5. **Multi-language** — search and summarize across English, Chinese, French, Spanish, German, Japanese, Arabic
6. **Scientific integrity** — distinguish between IPCC consensus (high confidence), emerging research, and advocacy positions

## Examples

### Example 1: Country Emissions Deep-Dive
**User**: "Analyze India's emissions trajectory and net-zero credibility"
**Output**: Historical emissions profile, sectoral breakdown (power, industry, transport, agriculture), NDC ambition vs. fair-share benchmarks, renewable deployment rate vs. required pathway, credibility scorecard.

### Example 2: Carbon Market Comparison
**User**: "Compare EU ETS and China ETS — which is more effective?"
**Output**: Side-by-side dashboard (price, coverage, cap trajectory, offset rules, MRV rigor, market stability mechanisms); effectiveness assessment based on emissions reduction in covered sectors.

### Example 3: Climate Tech Scan
**User**: "What's the state of direct air capture (DAC) technology in 2026?"
**Output**: Technology primer, current global capacity (ktCO2/year), cost ($/tCO2) and learning rate, key players (Climeworks, Carbon Engineering, Heirloom), funding (DOE hubs, Frontier buyers club), scalability bottlenecks, 2030 projection.

---

**Data Base**: `references/climate_sources.json` — 15 authoritative sources, 9 climate domains, emissions ranking, Paris Agreement timeline.
**Last Updated**: June 2026
**Free Tier**: Available. This skill aggregates public climate data; no proprietary satellite or commercial data accessed.
*（内容由AI生成，仅供参考）*
