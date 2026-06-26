# Commercial Translation — Energy Market Intelligence

## Purpose

Bridge the gap between AESO market data and actionable commercial decisions for each target user type. The skill output must not stop at market summary — it must explain what the data means for the user's specific cost, risk, or opportunity.

## Translation frameworks by user type

### Energy traders

**What they care about:** Position risk, spread opportunities, hedge timing, event-driven alpha.

**Translation pattern:**
- Market condition → merit order implication → price duration impact → position consideration
- Always frame as "conditions that have historically correlated with X" — never as "you should do Y"
- Connect supply/demand tightness to **price duration curves** — how many hours above/below key thresholds?
- Flag **import/export dynamics** — BC hydro availability is a key spread driver

**Example translation:**
> "2,400 MW of planned outages with load forecast at 11,200 MW leaves a reserve margin of ~1,800 MW — tighter than the trailing 30-day average of 2,500 MW. Historically, reserve margins below 2,000 MW in winter have correlated with >25% of peak hours pricing above $200/MWh."

### Facility managers

**What they care about:** Budget predictability, contract timing, load-shifting savings, rate class exposure.

**Translation pattern:**
- Pool price trend → all-in cost impact → budget variance → procurement timing signal
- Always translate $/MWh to $/month for their load profile
- Flag the difference between energy cost (varies with pool price) and demand charges (don't)

**Example calculation:**
> For a 5 MW baseload facility: $10/MWh pool price increase = ~$36,500/month additional energy cost (5 MW × 730 hours × $10/MWh). Transmission and distribution charges (~$40-60/MWh) are unaffected by pool price movements.

### Data center developers

**What they care about:** All-in power cost, grid reliability, interconnection timeline, carbon intensity.

**Translation pattern:**
- Pool price economics → all-in $/MWh for baseload profile → cost comparison frame → site-specific risks
- Connection project list → queue pressure → energization timeline risk
- Grid emissions intensity → Scope 2 implications

**Key metrics to provide:**
- All-in electricity cost at current pool price levels (energy + transmission + distribution + riders)
- Interconnection queue depth at target substation (MW pending vs. available capacity)
- Grid emissions intensity (tCO2e/MWh) for Scope 2 reporting
- Estimated energization timeline based on AESO connection process stages

### Sustainability / ESG teams

**What they care about:** Grid emissions intensity, renewable share, carbon cost exposure, PPA landscape.

**Translation pattern:**
- Generation mix data → grid emissions intensity → Scope 2 calculation inputs
- Carbon pricing → cost pass-through to electricity → budget exposure
- Renewable build-out → future emissions trajectory → forward Scope 2 positioning

**Important distinctions:**
- Grid-average emissions intensity ≠ marginal emissions intensity
- Contracted renewable energy (PPA) may not change Scope 2 accounting depending on methodology
- Alberta TIER carbon price ≠ federal backstop price; track the applicable mechanism

## Rules

1. Every commercial implication must connect to a specific data point from the brief.
2. Cost calculations must state all assumptions (load factor, time period, which cost components included).
3. Never reduce "commercial implication" to "this could increase costs" — quantify the magnitude or range.
4. When the user type is unknown, provide implications for the two most likely audiences and ask which applies.
