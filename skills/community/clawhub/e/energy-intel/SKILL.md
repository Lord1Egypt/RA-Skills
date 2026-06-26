---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_5fffe3485dbe11f18d42525400d9a7a1
    ReservedCode1: drsqrxmWNnk8DQzBjTZgqrOEYHAI38S/9rYlMfhm1/Mq27k0Iq3Jqnp50nIFrKWotN5TurPcCm6AMaRIyLYzPfpVVZZ6dkNKmRps9Xj3Mv8z5ADtevx3X/QKXDNjSGs7JxMl2I8yluIB0kazIqGFcxCkBbq/03yMTv5dt3i7IccKF48N9kYtkqHUFiQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_5fffe3485dbe11f18d42525400d9a7a1
    ReservedCode2: drsqrxmWNnk8DQzBjTZgqrOEYHAI38S/9rYlMfhm1/Mq27k0Iq3Jqnp50nIFrKWotN5TurPcCm6AMaRIyLYzPfpVVZZ6dkNKmRps9Xj3Mv8z5ADtevx3X/QKXDNjSGs7JxMl2I8yluIB0kazIqGFcxCkBbq/03yMTv5dt3i7IccKF48N9kYtkqHUFiQ=
---



# Global Energy & Natural Resources Intelligence

Massive data-driven energy intelligence covering the full energy stack from hydrocarbons to renewables to critical minerals. Powered by 21 authoritative data sources and 12 real-time commodity benchmarks.

## Triggers

- "What's the outlook for oil prices?"
- "Compare renewable energy growth in China vs. EU"
- "Analyze lithium/cobalt supply chain risks"
- "Track LNG trade flows and pricing"
- "Research nuclear energy revival globally"
- "Map critical mineral dependencies by technology"
- "Monitor carbon pricing evolution"
- "Identify energy security vulnerabilities"

## Capabilities

| # | Capability | Data Scope | Output Mode |
|---|-----------|-----------|-------------|
| 1 | Oil & gas market intelligence | IEA, OPEC, EIA, JODI, BP, Platts, Rystad, Baker Hughes | Price (Brent/WTI/HH/TTF), supply-demand balance, inventories, rig counts, trade flows |
| 2 | Renewable energy deployment tracking | IRENA, IEA, BNEF, GWEC, SolarPower Europe, NREL | Capacity additions by tech/country, LCOE trends, investment flows, policy landscape |
| 3 | Critical minerals & supply chains | USGS, LME, SMM, Benchmark Minerals, Cochilco | 12 commodity prices, reserves-to-production ratios, processing bottleneck maps, country concentration risk |
| 4 | Nuclear power status & outlook | IAEA PRIS, WNA, WNN | 440+ reactor status, SMR pipeline, Gen IV R&D, regulatory timelines |
| 5 | Carbon markets & climate policy | EU ETS, World Bank Carbon Dashboard, Global Carbon Project | Carbon price trajectory, coverage expansion, CBAM impact, Article 6 mechanisms |
| 6 | Geopolitical chokepoint analysis | Multiple intelligence sources, AIS vessel tracking | 8 chokepoints: Hormuz, Malacca, Suez, Bab el-Mandeb, Panama, Turkish Straits, DRC-Cobalt, SCS-LNG |
| 7 | Grid & power system data | ENTSO-E, EIA Electricity, Ember Global Review | Generation mix, interconnection flows, price spreads, flexibility capacity |
| 8 | Energy transition technology deep-dive | 10 technologies: solar, wind, batteries, H₂, nuclear SMR, CCUS, grid, geothermal, marine, SAF | TRL assessment, cost curves, scaling bottlenecks, IP landscape |
| 9 | National energy strategy comparison | NDCs, IRA, RePowerEU, China 30-60, India MNRE | Policy instrument mix, subsidy levels, phase-out schedules, stranded asset risk |
| 10 | Investment thesis & risk assessment | Integrated cross-commodity | Bull/bear case, scenario analysis, sensitivity tables, key monitor indicators |

## Workflow

```
User Query
    │
    ├─ Price/market query → Multi-source cross-reference (IEA+EIA+OPEC+Platts)
    │   └─ Output: Current price + 3-6 month trend + drivers + forecast range
    │
    ├─ Technology/transition query → Capability #8 deep-dive
    │   └─ Output: Tech status + cost curve + deployment rate + critical minerals dependency
    │
    ├─ Commodity-specific → Capability #3 supply chain map
    │   └─ Output: Price + reserves + processing map + geopolitical risk score
    │
    ├─ Geopolitical query → Capability #6 chokepoint + IEA emergency analysis
    │   └─ Output: Flow volume + risk scenario + impact range + alternatives
    │
    └─ Investment query → Capability #10 scenario analysis
        └─ Output: Bull/base/bear cases + catalyst timeline + risk dashboard
```

## Output Formats

### Format 1: Commodity Snapshot
```
| Metric | Current | 3M Trend | 12M Forecast | Key Driver |
|--------|---------|----------|-------------|------------|
| Price  | $XX     | ↑/↓/→   | $XX-$XX     | [source]  |
| Supply | XX M bpd | ↑/↓    | XX M bpd    | [country] |
| Demand | XX M bpd | ↑/↓    | XX M bpd    | [region]  |
| Stocks | XX days  | ↑/↓    | XX days     | [agency]  |
```

### Format 2: Technology Competitive Landscape
```
| Technology | TRL | LCOE $/MWh | 2025-2030 CAGR | Bottleneck | Top 3 Players |
```

### Format 3: Geopolitical Risk Dashboard
```
| Chokepoint | Flow (M bpd) | Risk Level | Scenario | Impact Range |
```

## Usage Guidelines

- Always cite primary data source and date of latest release
- Cross-validate between IEA/EIA/OPEC where divergence is material
- Distinguish between structural shifts vs. cyclical movements
- Flag market-moving events (OPEC+ decisions, SPR releases, sanctions, pipeline incidents)

## Examples

**Q: What's the 2026 oil outlook?**
→ Pull IEA OMR latest + OPEC MOMR + EIA STEO + Platts assessments → Price range: $XX-$XX driven by [demand growth/cuts/geopolitics]

**Q: Is cobalt supply a bottleneck for EVs?**
→ USGS production data + LME price + DRC risk assessment + LFP substitution trend → DRC 70% share with [risk level], LFP reducing cathode cobalt by [XX%]

**Q: Compare EU vs. China carbon pricing**
→ EU ETS €XX/t vs. China ETS ¥XX/t → EU 4x higher, CBAM impact on [sectors], China expanding to [industries]

---

**Data Sources (21 total)**: See `references/energy_sources.json` for complete listing with URLs and update frequencies.
*（内容由AI生成，仅供参考）*
