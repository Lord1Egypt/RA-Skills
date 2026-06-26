---
description: >
  Run a full NPD validation pipeline on a product concept. Orchestrates 8 specialized
  subagents (Research Coordinator, 5 Independent Evaluators, Devil's Advocate, Consensus
  Director) to produce an evidence-based GO / CONDITIONAL GO / REVISIT / NO-GO recommendation.
  Use when someone asks to validate a product idea, assess market fit, or evaluate whether
  a product should be launched.
allowed-tools: Read Write Edit Bash WebSearch SubAgent
---

# NPD Product Validation Pipeline

You are orchestrating a multi-agent product validation. Read the methodology skill
at `skills/npd-methodology/SKILL.md` before proceeding.

## Step 1: Determine Entry Mode

Analyze "$ARGUMENTS" to determine entry mode:

**Mode A (Rough Idea)**: User provided <4 of 6 Concept Brief fields.
- Ask targeted questions to fill the brief
- Run a Quick Scan (1-2 searches per dimension, traffic light output)
- Get user confirmation before deep validation

**Mode B (Solid Idea)**: User provided ≥4 fields or said "just validate."
- Confirm understanding
- Populate the Concept Brief
- Proceed to deep validation

## Step 2: Populate Concept Brief

Create `data/concept_brief.md` with:
```
Product Name / Working Title: [...]
Category: [...]
One-Line Description: [≤15 words]
Target Consumer: [...]
Price Point Range: [...]
Key Differentiator: [...]
Launch Horizon: [now / 6 months / 12 months / 24+ months — specify target month if seasonal]
Brand Context (optional): [...]
```

If the user hasn't specified a launch horizon, ASK before proceeding. A trend that scores Timing 9/10 for launch "now" may score 3/10 for launch in 24 months.

### Brief Coherence Check

Before launching the pipeline, scan the brief for internal contradictions:
- **Positioning vs Price**: Does the price match the positioning? ("ultra-premium" at $5 is contradictory)
- **Target vs Positioning**: Does the target consumer align with the positioning? ("budget-conscious teens" vs "luxury" is contradictory)
- **Differentiator vs Category**: Does the differentiator make sense for this category?

If contradictions are found: flag them to the user with a specific question, e.g., "You described this as ultra-premium but priced at $5 — which is the actual intent? The validation results would be very different." Do NOT reject the idea — the user may have a valid strategy. But get clarity before investing 25+ searches in a pipeline built on an incoherent brief.

### Multi-SKU Launch Detection

Multi-SKU launches come in two distinct flavors — identify which one applies before proceeding:

**Bundle / Collection / Set**: Multiple products sold together as a unit at a combined price (e.g., "The Morning Routine — 3 products, $65 together"). Consumers buy them as ONE transaction.

**Line Launch / Drop**: Multiple distinct products launched simultaneously but sold separately (e.g., "Full skincare line: cleanser $24, toner $22, serum $38, moisturizer $32, SPF $28 — available individually"). Consumers pick what they want.

Each has different dynamics:

*Bundles* — see Bundle-specific evaluator guidance below. Attachment rate is fixed at 100% for bundle buyers. SKU complexity is lower (1 bundle SKU + 3 components).

*Line launches* — distinct considerations the bundle framework does NOT cover:
- **Working capital multiplier**: 5 SKUs = 5× inventory investment. A brand that can afford 1 SKU launch may not afford 5.
- **Testing cost aggregation**: each SKU requires its own stability/safety testing. Not linear but not 1×.
- **Retailer listing economics**: 5 listing fees but ONE buyer conversation — potentially better leverage, but also harder negotiation.
- **Launch moment amplification**: a line launch is a bigger PR/marketing moment than a single SKU — more editorial hooks, more creator content, larger retail displays.
- **Complexity non-linearities**: 5 SKUs requires 5 different supply chains, 5 different forecasts, 5 different return rates to manage. Operational load scales faster than revenue potential.

For a line launch, the validation should produce a recommendation on **optimal launch size**: hero-first (launch 1, expand later based on performance), full-line (launch all 5 simultaneously), or staggered (launch 2, then add 3 more in months 3 and 6). This is a launch strategy question, not just a go/no-go.

### Collection / Bundle Detection

If the multi-SKU offering is a **bundle**, treat it as a bundle validation, not a single-product one. Bundles have distinct dynamics: attachment rate, bundle-vs-separate margin tradeoffs, SKU complexity, and consumers' willingness to buy a set vs individual items.

Update the Concept Brief with a **Bundle Context** field listing each component product, the bundle price, and the sum-of-parts price. Evaluators adapt:
- **Market Demand**: Do consumers in this category buy collections, or prefer to curate their own? What's the bundling precedent?
- **Competitive Intel**: Who else sells collections in this space? What's the typical bundle discount?
- **Brand Fit**: Does a collection make sense for this brand's portfolio? Is the brand known for standalone heroes or curated sets?
- **Commercial Viability**: Bundle economics specifically — attachment rate assumptions, bundle discount margin impact, SKU complexity cost, inventory implications
- **Consumer & Trends**: Are collections trending up or down in the category?

Do NOT produce 3 separate validations averaged together — the bundle IS the product.

### Geographic Scope Check

If the user mentions multiple markets (e.g., "launch in US, UK, Germany, Japan"), a single composite score is misleading — regulations, competitors, trends, and consumer behavior differ significantly across markets. A product can be GO in one market and NO-GO in another.

Before launching, ask the user: "You mentioned [X] markets. For the most accurate results, I can (a) validate for your PRIMARY market and flag considerations for the others, (b) run parallel validations per market and produce per-market verdicts, or (c) use a TEST MARKET / BEACHHEAD approach — fully validate the primary market with explicit expansion-readiness criteria, so US performance can de-risk subsequent EU/UK/Australia rollouts. Option (b) takes [N × time] but gives market-specific go/no-go decisions. Option (c) is right when the user intends to use launch data from one market to inform expansion. Which do you prefer?"

If they choose (a), add the primary market to the Concept Brief and note the others as "expansion considerations." The Research Coordinator and Consumer & Trends evaluators will incorporate expansion notes without producing full per-market analyses.

If they choose (b), run the full pipeline once per market with each producing its own report, then produce a consolidated cross-market comparison as the final deliverable.

If they choose (c) — **beachhead strategy** — validate the primary market in depth, then produce an additional **Expansion Readiness** section in the final report. This section defines:
- Performance criteria that would trigger expansion (e.g., "$X revenue in 12 months," "Y% repeat rate," "Z retailer sell-through")
- Market-specific risks for each expansion target (regulatory, competitive, cultural)
- Investment required per additional market
- Recommended sequencing (UK before EU? Australia before Asia?)

### Regulatory Divergence — Product-Level Check

When validating multiple markets, recognize that some categories require **different formulations/products per market**, not just different marketing. Examples:
- Retinol: EU caps at 0.3%, US has no cap — the formulation itself must differ
- SPF: UVA protection calculations differ (US: no specific UVA rating, EU: UVA-PF, Japan: PPD)
- Supplements: health claims and ingredient allowances vary dramatically
- Food: additive allowances, labeling requirements, portion sizes
- Cosmetics: EU has a banned list (Annex II) far longer than US FDA's

If the Research Coordinator identifies product-level regulatory divergence across target markets, flag it as a Critical Alert. The "same product" in US and EU may require two separate formulation development tracks, two testing files, two manufacturing runs. Commercial Viability should reflect this operational reality — it's not one product with different labels, it's effectively two products to manage.

### User-Provided Internal Data

Internal data (sales history, cost sheets, customer research, brand portfolio data) is MORE reliable than external web research. If the user provides files or data:

1. Save to `data/user_provided/` with a descriptive name (e.g., `internal_sales_q1_q4_2025.csv`)
2. Add a note to `data/concept_brief.md`: "User-provided data available: [list files with 1-line description each]"
3. Evaluators are instructed to prioritize user data over external estimates in their specific domain:
   - **Sales/performance data** → Market Demand, Commercial Viability
   - **Customer research/demographics** → Brand Fit, Consumer & Trends
   - **Cost sheets/margin data** → Commercial Viability
   - **Portfolio data** → Brand Fit
4. Dimensions backed by user data should be marked HIGH confidence (internal data beats external estimates)
5. The final report must note which scores were informed by user-provided data vs external research

If the user says they have data but hasn't provided it yet, ask them to share it before Phase 2 begins.

## Step 3: Run the Pipeline

Execute each phase by delegating to the specialized subagents:

### Phase 1 — Research Coordinator
Delegate to the `npd-research-coordinator` subagent:
- Input: the concept brief
- It will conduct 8-12 web searches and produce `data/context_brief.md`
- Wait for completion before proceeding

### Phase 2 — Independent Evaluations
Delegate to ALL 5 evaluator subagents. Run them in parallel if possible:
- `npd-market-demand` → reads concept brief + context brief → writes `data/eval_market_demand.md`
- `npd-competitive-intel` → reads concept brief + context brief → writes `data/eval_competitive_intel.md`
- `npd-brand-fit` → reads concept brief + context brief → writes `data/eval_brand_fit.md`
- `npd-commercial-viability` → reads concept brief + context brief → writes `data/eval_commercial_viability.md`
- `npd-consumer-trends` → reads concept brief + context brief → writes `data/eval_consumer_trends.md`

**CRITICAL**: Each evaluator subagent runs in its own context. They CANNOT see each
other's output. This is the key architectural advantage — true independence.

Give each evaluator this instruction:
"Read data/concept_brief.md and data/context_brief.md. Follow your evaluation methodology.
Conduct at least 3-5 additional web searches. Score your 3 dimensions (1-10 each).
Write your full evaluation to data/eval_[your-name].md"

### Phase 3 — Devil's Advocate
After ALL 5 evaluators complete, delegate to `npd-devils-advocate`:
- It reads all 5 evaluation files + the concept brief
- It conducts adversarial research
- It writes `data/devils_case.md`

### Phase 4 — Consensus Director
After the Devil's Advocate completes, delegate to `npd-consensus-director`:
- It reads everything: concept brief, context brief, all 5 evals, devil's case
- It runs 3 rounds: conflict detection → challenge/defend → final synthesis
- For Round 2 challenges: it writes challenge files to `data/challenges/` and
  re-invokes the relevant evaluator subagent with the challenge
- It writes the final report to `data/validation_report.md`

## Step 4: Present Results

Read `data/validation_report.md` and present to the user:
1. Lead with the VERDICT and COMPOSITE SCORE
2. Summarize top 3 findings
3. Note the Devil's Advocate kill shot rating
4. Offer iteration options: pivot, deepen, variant test, challenge

## Step 5: Support Iteration

If the user wants to iterate:
- **Pivot**: Update concept_brief.md → re-run full pipeline
- **Deepen one area**: Re-invoke that specific evaluator subagent with expanded scope
- **Challenge a score**: Pass user's counter-evidence to the evaluator subagent
- **Change weights**: Re-invoke consensus-director to recalculate

### Variant Testing

When the user wants to compare two versions of a concept (e.g., "what if we did the same product but as mass market instead of premium?"):

1. **Preserve original**: Save current `data/concept_brief.md` and `data/validation_report.md` as `data/variant_a/`
2. **Create variant brief**: Write the modified concept to `data/variant_b/concept_brief.md`
3. **Run parallel pipeline**: Execute the full 4-phase pipeline for variant B, writing all outputs to `data/variant_b/`
4. **Produce comparison report**: Write `data/comparison_report.md` containing:
   - Side-by-side scorecard table (variant A scores | variant B scores | delta per dimension)
   - Verdict comparison (which variant got the better verdict and why)
   - Key differentiators (which dimensions drove the difference)
   - Recommendation (which variant to proceed with, or whether to pivot to a hybrid)
5. **Present comparison** to the user, leading with the recommended variant and the score gap

The two pipelines must be run independently — do not let variant A's findings contaminate variant B's evaluators.

### Scope Creep Detection

Before running each iteration, compare the new concept to V1 (the original):

- **Category change**: V1 was "body moisturizer," V6 is "face mist" → scope creep
- **Target demographic shift**: V1 targeted women 25–35, V6 targets teens → scope creep
- **Differentiator fully replaced**: V1 differentiator was "caffeine," V6 is "adaptogens" with no caffeine → scope creep
- **Price tier jumped 2+ levels**: V1 was mid-range $18–24, V6 is ultra-premium $85+ → scope creep

If 2+ scope creep signals are present, stop and ask the user: "This iteration has drifted substantially from V1. The concept now differs in [list changes]. Should we: (a) close this validation and start a fresh one for the new concept, or (b) continue as V[N] with the understanding that the original concept is effectively archived?"

This prevents a V7 verdict from being confused with a validation of the original concept. Both paths are valid — the user chooses. If they continue, note the drift explicitly in the iteration log and report header.

Track iteration history in `data/iteration_log.md`.
