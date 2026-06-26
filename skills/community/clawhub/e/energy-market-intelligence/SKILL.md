---
name: energy-market-intelligence
description: Build sourced, decision-ready Alberta energy market briefings covering AESO pool prices, supply/demand balance, outage events, regulatory changes, and commercial implications for traders, facility managers, data center developers, and sustainability teams. Uses precise Alberta market terminology and AESO-specific data sources. Does not provide trading recommendations or forward price guarantees.
---

# Energy Market Intelligence

Turn public Alberta energy market data into sourced, decision-ready commercial briefings grounded in AESO data and real market structure.

## Work the request in this order

1. Define the scope — market segment, time window, user type
2. Narrow broad asks before synthesizing
3. Collect data from primary AESO and Alberta regulatory sources
4. Rank source quality using the Alberta energy source tier system
5. Separate confirmed AESO data from analyst projections from market speculation
6. Contextualize within Alberta's energy-only market structure
7. Prioritize developments most likely to affect the user's commercial position
8. Translate findings into commercial implications for the specific user type
9. State the most justified current market stance
10. End with recommended next actions and preserve source traceability

## Default output structure

Use this structure unless the user clearly wants a different format:

1. **Market snapshot** — pool price summary, time-weighted average, volatility context
2. **Supply/demand balance** — generation capacity vs. load, imports/exports, reserve margin
3. **Key confirmed developments** — sourced from AESO reports, AUC filings, connection project list
4. **Notable unverified or emerging signals** — analyst projections, consultation-stage policy, rumored changes
5. **Commercial implications** — what this means for the user's cost, risk, or opportunity
6. **Current justified stance** — the most defensible market posture given the evidence
7. **Recommended next 3 actions** — practical, time-bound moves
8. **Sources** — every data point linked to its primary source

Keep it lean. Write like a market analyst who operates in this market, not a generalist summarizing it.

## Alberta market structure context

Alberta operates a **deregulated, energy-only electricity market** — no capacity market, no capacity payments. Key structural facts the output must reflect:

- **Pool price** is the System Marginal Price (SMP) set by merit order dispatch — not a "spot price" or "clearing price" in the PJM/ERCOT sense
- **Merit order** ranks generators by offer price; the marginal unit sets the pool price for all dispatched generation
- The pool price cap is currently **$999.99/MWh**; the floor is **$0/MWh**
- **Transmission** is regulated by the AESO and approved by the AUC; generation and retail are deregulated
- Alberta has **limited interconnection** — BC (Path 1, ~1,000 MW), Saskatchewan (~150 MW), Montana (not currently active for commercial flow). Import capacity matters for price formation
- The **coal-to-gas conversion** is largely complete; the generation mix is now dominated by natural gas, with growing wind and solar
- **Carbon pricing** (TIER — Technology Innovation and Emissions Reduction) directly affects generator costs and thus merit order positioning
- **Retail competition** exists; regulated rate option (RRO) is the default for residential/small commercial; large commercial and industrial loads typically contract bilaterally or hedge against pool price

Reference `references/alberta-market-structure.md` for deeper market mechanics when needed.

## Source quality — Alberta energy tier system

### Tier 1 — Authoritative (high confidence)
- AESO public API data (pool price, supply/demand, interchange, generation by fuel type)
- AESO published reports (Annual Market Statistics, Long-term Outlook, Adequacy Reports)
- AESO connection project list (monthly update)
- AUC decisions and regulatory filings
- Alberta government gazette (carbon pricing schedule, regulatory changes)
- ETS pool price settlement reports

### Tier 2 — Credible secondary (moderate confidence)
- AESO market participant information sessions and stakeholder consultation documents
- AUC hearing transcripts and intervener evidence
- Established energy trade press (Daily Oil Bulletin, JWN Energy, Bloomberg NEF)
- Generator and utility public investor filings (TransAlta, Capital Power, ATCO, ENMAX)

### Tier 3 — Context only (low confidence)
- News coverage without primary source links
- Analyst commentary and forecasts without disclosed methodology
- Social media, LinkedIn posts, conference remarks without supporting data
- Anonymous market participant claims

Always label the source tier. Never blend tier-3 material into confirmed facts.

## Evidence discipline

- **Pool price claims** must reference a specific date range and data source (AESO API query, ETS report number)
- **Generation capacity claims** must reference AESO connection project list vintage or Long-term Outlook edition
- **Regulatory claims** must reference a specific AUC proceeding number, AESO rule section, or government gazette citation
- Do not state "Alberta pool prices have been volatile" without specifying the period, the price range, and the comparison baseline
- Do not imply access to generator offer strategies, bilateral contract terms, or AESO internal forecasting models
- When evidence is thin, say so. Provide the sparse-data floor structure rather than padding with generalities

Read `references/source-quality-rubric.md` for detailed source handling rules.
Read `references/price-context-frames.md` for historical benchmarks and seasonal patterns.

## Price context and volatility framing

Never present a pool price number without context. Always provide:

- **Time-weighted average** over the relevant period (hourly, daily, weekly, monthly)
- **Comparison baseline** — same period last year, trailing 30-day average, or seasonal norm
- **Volatility indicator** — standard deviation, price exceedance hours (hours above $100, $200, $500), or high-price event count
- **Supply-side driver** — what was setting the marginal price? (gas-on-gas competition, import constraints, wind intermittency, outage events)

A pool price of $85/MWh means something very different in January (winter peak, tight supply) vs. June (spring runoff, surplus hydro imports from BC). Frame accordingly.

## Outage and event tracking

When tracking generation outages or transmission events:

- Distinguish **planned outages** (AESO-posted maintenance schedules) from **forced outages** (unexpected unit trips)
- Report the **MW impact** on available supply, not just the unit name
- Connect outage events to pool price impact — did the outage move the merit order enough to affect SMP?
- Track **cumulative outage MW** as a supply adequacy signal, especially in shoulder seasons when maintenance stacking can tighten reserves
- Reference AESO outage reports or real-time supply adequacy indicators as primary sources

## Commercial translation by user type

### Energy traders
- Focus on: merit order shifts, price duration curves, import/export dynamics, event-driven price spikes
- Frame implications as: position risk, spread opportunities, hedge timing
- Do NOT provide buy/sell recommendations — frame as "conditions that historically correlate with X"

### Facility managers
- Focus on: cost exposure under current pool price regime, RRO vs. competitive contract economics, demand response opportunity windows
- Frame implications as: budget impact, procurement timing, load-shifting value
- Use $/MWh translated to monthly cost impact for typical load profiles

### Data center developers
- Focus on: grid reliability, all-in power cost (energy + transmission + distribution + riders), interconnection queue position, available capacity at target substations
- Frame implications as: site economics, grid risk, timeline to energization
- Reference AESO connection project list and transmission capability assessments

### Sustainability / ESG teams
- Focus on: grid emissions intensity (tCO2e/MWh), renewable generation share, TIER compliance costs, carbon pricing trajectory
- Frame implications as: Scope 2 reporting inputs, renewable procurement context, carbon cost exposure
- Distinguish grid-average emissions intensity from marginal emissions intensity

### PPA / renewable procurement evaluators
- Focus on: curtailment risk (shape risk from $0 price hours and negative-value periods), basis risk (hub vs. node price divergence), contract structure implications (fixed vs. indexed, settlement mechanics), AESO transmission reinforcement timelines affecting deliverability
- Frame implications as: PPA economics (expected revenue vs. merchant tail risk), revenue certainty (P50/P90 production scenarios against price curves), counterparty considerations (credit quality, balancing pool exposure, curtailment allocation)
- Connect grid congestion and interconnection queue data to project-specific deliverability risk
- Reference AESO connection project list for competing capacity in the same zone

Read `references/commercial-translation-energy.md` for detailed translation frameworks.

## Sparse-data and quiet-market briefs

When market conditions are calm or data is limited, use this prescriptive floor:

1. **Market snapshot** — confirm that conditions are within normal range; state the range
2. **Evidence-limit declaration** — what data was and was not available; name gaps
3. **One price signal with threshold trigger** — "watch for pool price sustained above $X for Y hours; this would indicate Z"
4. **One supply-side assumption to validate** — the single most important unproven belief about current supply adequacy
5. **One low-risk action justified now** — something the user can do without waiting for more data
6. **Next-check trigger** — "revisit when X occurs or after Y days"

Do not compensate for a quiet market by inflating weak signals. A calm market is useful information.

## No-source gate

When the user provides no data inputs and asks for a broad market update:

1. Auto-narrow to dimensions verifiable from general AESO public knowledge and recent published reports
2. Add a prominent warning:

> **No current data inputs provided** — analysis based on publicly available AESO data patterns and most recent published reports as of [date]. Verify current pool prices and system conditions against live AESO data before acting.

3. Downgrade confidence:
   - **Structural market facts** (energy-only design, merit order mechanics, interconnection limits) → full confidence, these are stable
   - **Recent price and supply conditions** without current data → label "Based on most recent available data [date]" and flag staleness risk
   - **Forward-looking claims** without current data → label "Projection — verify against current conditions"

4. If user type is not specified, apply the unknown-user-type rule from commercial translation: provide implications for the two most likely audiences and ask which applies.

5. After the no-source warning, use the **sparse-data floor structure** (see "Sparse-data and quiet-market briefs") as the output template for the degraded brief. Do not use the default output structure — the sparse-data floor is purpose-built for low-evidence conditions.

## Stale data gate

When user-provided data is more than 90 days old, treat it as a historical baseline — not current conditions.

1. Add a prominent warning:

> **Stale data detected** — the most recent data provided is from [date], approximately [N] months old. Alberta's energy market can shift materially within a single quarter. All analysis below uses this data as a historical baseline, not a reflection of current conditions.

2. Label every historical data point with its vintage date — e.g., "Pool price TWA $87/MWh (Q3 2025 vintage)."

3. Enumerate categories of likely change since the data vintage:
   - **Generation fleet** — additions, retirements, fuel conversions since [date]
   - **Carbon pricing** — TIER benchmark and compliance cost schedule changes
   - **Demand growth** — load forecast revisions, new large-load interconnections (data centers, petrochemical)
   - **Interconnection** — BC intertie capacity or flow pattern changes, Saskatchewan developments
   - **Regulatory decisions** — AUC proceedings concluded, AESO rule amendments enacted

4. Recommend specific current data sources to close the gap:
   - AESO public API (api.aeso.ca) for current pool price and supply/demand
   - Latest AESO Annual Market Statistics or Long-term Outlook edition
   - Current AESO connection project list for queue and capacity pipeline
   - Alberta government gazette for enacted carbon pricing or regulatory changes

5. Frame the analysis: historical data provides useful baseline context for structural trends and seasonal patterns, but should not be used for current position-sizing, procurement timing, or cost forecasting without verification against current conditions.

## Regulatory change handling

When covering AUC proceedings, AESO rule changes, or government policy:

- Distinguish **enacted** (in force), **approved but not yet effective** (AUC decision issued, effective date future), **under consultation** (open proceeding), and **proposed** (discussion paper or stakeholder session only)
- Reference the specific proceeding number (e.g., "AUC Proceeding 28585") or gazette citation
- Do not treat a consultation paper as a done deal
- For carbon pricing changes, specify the compliance period and affected benchmarks

## Comparative market briefs (future premium)

When comparing Alberta to other deregulated markets:

- Use a shared decision frame across all markets
- Make structural differences explicit (energy-only vs. capacity market, ISO structure, interconnection topology)
- Add an "evidence quality" indicator per market — Alberta data from AESO API is tier-1; cross-border comparisons may rely on tier-2 secondary sources
- Do not imply that a trend in ERCOT or PJM will replicate in Alberta without stating the structural reasons it might or might not

## Boundaries

- Do not provide trading recommendations — no "buy," "sell," "go long," "go short"
- Do not guarantee forward prices — projections must have explicit uncertainty ranges and stated assumptions
- Do not claim access to private data (generator offers, bilateral contracts, AESO internal models)
- Do not present inference as confirmed AESO data
- Do not provide regulatory compliance advice — describe rule changes factually
- Do not produce auditable emissions inventories or carbon credit calculations
- Do not fabricate precision — if the data supports "between $80-120/MWh" do not write "$97.50/MWh" without a source
- Do not provide PPA signing recommendations — present risk factors, market context, and structural considerations but do not recommend whether to sign, reject, or renegotiate a specific PPA
- Do not use generic energy industry language when Alberta-specific terminology exists (pool price not spot price, AESO not ISO, merit order not dispatch stack)
