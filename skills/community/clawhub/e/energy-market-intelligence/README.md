# energy-market-intelligence

Turn public Alberta energy market data into sourced, decision-ready commercial briefings grounded in AESO data and real market structure.

## What it does

This skill builds practitioner-grade Alberta energy market briefings from public AESO data and regulatory sources. It separates confirmed data from analyst projections and market speculation, contextualizes within Alberta's energy-only market structure, and translates findings into commercial implications for specific user types. Every data point is tied to a primary source with explicit confidence tiering.

## Who it's for

- **Energy traders** — merit order shifts, price duration curves, event-driven price spikes
- **Facility managers** — cost exposure, RRO vs. competitive contract economics, demand response windows
- **Data center developers** — all-in power cost, grid reliability, interconnection queue, carbon intensity
- **Sustainability / ESG teams** — grid emissions intensity, renewable share, TIER compliance costs
- **PPA / renewable procurement evaluators** — curtailment risk, basis risk, contract structure implications

## Install

```bash
clawhub install energy-market-intelligence
```

## Usage

Trigger the skill by asking for an Alberta energy market briefing, pool price analysis, supply/demand update, or commercial energy assessment. Examples:

**Market briefing:**
> Build an Alberta energy market briefing for the current week. I'm a facility manager with a 5 MW baseload in Calgary.

**Pool price analysis:**
> What's driving Alberta pool prices this month? Focus on merit order changes and import dynamics. Audience: energy trading desk.

**Data center site assessment:**
> Assess Alberta grid conditions for a 50 MW data center development. Cover all-in power cost, interconnection timeline, and carbon intensity for Scope 2 reporting.

**Regulatory update:**
> Summarize recent AUC proceedings and AESO rule changes that affect large industrial electricity consumers in Alberta.

**Quiet market / sparse data:**
> Give me an Alberta energy market update. I don't have current data — just need the structural picture and what to watch for.

## Output structure

The default briefing includes:

1. **Market snapshot** — pool price summary, time-weighted average, volatility context
2. **Supply/demand balance** — generation capacity vs. load, imports/exports, reserve margin
3. **Key confirmed developments** — sourced from AESO reports, AUC filings, connection project list
4. **Notable unverified or emerging signals** — analyst projections, consultation-stage policy
5. **Commercial implications** — what this means for the user's cost, risk, or opportunity
6. **Current justified stance** — the most defensible market posture given the evidence
7. **Recommended next 3 actions** — practical, time-bound moves
8. **Sources** — every data point linked to its primary source

## Key principles

- **Alberta-specific terminology**: pool price (not spot price), merit order (not dispatch stack), AESO (not ISO)
- **Three-tier source system**: AESO/AUC primary data (tier 1), credible trade press (tier 2), unverified claims (tier 3) — never blended
- **Evidence discipline**: every price claim needs a date range, source, and comparison baseline
- **No-source gate**: when no current data is provided, the skill auto-narrows scope and applies explicit confidence downgrades
- **Stale data gate**: data older than 90 days is treated as historical baseline with enumerated change categories
- **No trading recommendations**: conditions and correlations, never buy/sell/hold

## Reference files

The skill loads supporting references as needed:

| File | Used when |
|------|-----------|
| `alberta-market-structure.md` | Market mechanics, terminology, entity roles |
| `source-quality-rubric.md` | Source tiering and evidence handling rules |
| `price-context-frames.md` | Historical benchmarks, seasonal patterns, volatility framing |
| `commercial-translation-energy.md` | Translating market data into user-specific commercial implications |

## Version

v0.2.0 — First public release. Practitioner-grade Alberta energy market briefings with AESO-specific source tiering, merit order context, pool price framing, and commercial translation. 43/45 median QA score across 12 test cases.

## License

Published by NorthlineAILabs.
