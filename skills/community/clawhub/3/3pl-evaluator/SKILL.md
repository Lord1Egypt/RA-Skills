---
name: 3pl-evaluator
description: Systematically evaluate and compare third-party logistics (3PL) fulfillment partners against your order volume, product characteristics, and growth stage. Use when shortlisting 3PLs, comparing rate cards, auditing a current provider, or deciding between self-fulfillment, 3PL, and FBA.
---

# 3PL Evaluator

Choosing the wrong third-party logistics provider costs ecommerce businesses money through hidden fees, slow shipping, and poor inventory visibility — but comparing 3PLs is difficult because pricing structures, service levels, and technology stacks vary widely. This skill helps sellers systematically evaluate and compare 3PL fulfillment partners against their specific operational needs, order volume, product characteristics, and growth stage so they can make an informed decision rather than relying on sales pitches.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Cost comparison basis | Fully-loaded landed cost per order modeled from YOUR order profile (weights, zones, peak mix) | Side-by-side rate card comparison with major fee lines | Comparing headline pick fees only |
| Fee discovery | Written quote against a 25+ item fee schedule including surcharges and renewals | Asking "are there any other fees?" and logging the answer | Trusting the proposal PDF as complete |
| SLA evaluation | Contractual SLAs with credits: order accuracy ≥99.5%, same-day cut-off, dock-to-stock ≤48h | Published performance targets without credits | Verbal promises from the sales rep |
| Tech fit | Live demo with your own store connected in a sandbox; API/webhook docs reviewed | Confirmed native integration with your platform | "We integrate with everything" |
| References | 2-3 current clients in your category and volume band, interviewed | Case studies plus one reference call | Logos on the website |
| Volume fit | Your monthly orders within the provider's sweet spot (not bottom 10% of client sizes) | Slightly below sweet spot with a growth plan | Being their smallest or largest client |
| Contract terms | Month-to-month or ≤12 months, no minimums first 6 months, clear exit/data clauses | 12 months with volume-based minimums you'll clear by month 3 | Multi-year lock-in with auto-renewal and onboarding fees |

## Solves

1. Rate cards that are impossible to compare because each 3PL structures pricing differently (per-pick vs. per-order vs. bundled tiers).
2. Hidden fees — receiving, long-term storage, peak surcharges, account management, returns processing — that surface only after signing.
3. No objective way to weigh a cheaper quote against better technology, faster SLAs, or closer warehouse locations.
4. Outgrowing self-fulfillment without knowing the volume threshold where a 3PL actually saves money.
5. A current 3PL underperforming, with no benchmark to decide between renegotiating and switching.
6. Sales-led evaluations where the seller asks the questions the 3PL wants to answer instead of the ones that predict failure.
7. Switching costs discovered too late: data migration, inventory transfer, integration rebuild, customer disruption during cutover.

## Workflow

### Step 1 — Profile the operation
Capture the seller's profile: monthly order volume and growth rate, SKU count, product characteristics (size, weight, fragility, lot/expiry tracking, hazmat/batteries), sales channels and platforms, destination mix (domestic zones, international share), returns rate, peak seasonality multiplier, and current fulfillment cost per order if known. This profile drives every later step — a 3PL that is excellent for 5,000 light parcels/month is often wrong for 300 oversized items.

### Step 2 — Define requirements and disqualifiers
Translate the profile into must-haves (e.g., Shopify + TikTok Shop native integration, lot tracking, 2-day ground coverage to 90% of customers, kitting) and disqualifiers (e.g., no battery handling, 3-day receiving SLA, no Sunday processing). Weight the evaluation criteria: typical weighting is cost 30%, service/SLA 25%, technology 20%, scalability/fit 15%, contract flexibility 10% — adjust to the seller's stated priorities and record the weights.

### Step 3 — Normalize pricing into landed cost per order
Build a representative order basket from the seller's actual data (e.g., 70% single-item 0.4kg, 20% two-item, 10% heavy/oversized; zone distribution; 15% of annual volume in November). For each candidate, compute: receiving + storage (avg months on shelf) + pick/pack + packaging + shipping rates for the basket + returns processing + tech/account fees, divided by monthly orders. Use the full fee schedule in `references/fee-glossary-and-pricing-models.md` to force out unlisted fees. Model regular month AND peak month.

### Step 4 — Score non-price factors
Score each candidate 1-5 on: SLA strength (cut-off times, accuracy, dock-to-stock, with credits), technology (real-time inventory, returns portal, API quality, EDI if needed), warehouse network fit (proximity to customer density, multi-node options), category experience, scalability headroom, and support model (dedicated rep vs. ticket queue). Use the scoring guidance in `references/evaluation-scorecard-guide.md`. Verify claims with the diligence questions — never score from the sales deck alone.

### Step 5 — Check references and stress-test
Interview 2-3 current clients in the same category and volume band. Key questions: invoice accuracy, peak season performance, error resolution speed, fee creep after year one, and what they would negotiate differently. Stress-test the finalists: how were the last two peak seasons handled, what happens at 3x volume, what is the disaster/backlog protocol.

### Step 6 — Compute weighted scores and total cost of switching
Combine normalized cost (converted to a 1-5 score against the cheapest) with the weighted non-price scores. Separately estimate one-time switching costs: inventory transfer freight, overlap period running two providers (typically 4-8 weeks), integration setup, onboarding fees, and team time. A 10% cheaper provider with a $25k switch cost has a payback period — show it.

### Step 7 — Deliver recommendation
Produce the comparison using `references/output-template.md`: weighted scorecard, landed cost per order table (regular + peak), red flags found, negotiation levers for the preferred candidate (fee caps, minimum waivers, SLA credits, rate review clauses), and a transition plan outline. Run `assets/3pl-evaluation-checklist.md` before delivering. State assumptions where the seller's data was incomplete.

## Worked Example 1 — First 3PL for a growing Shopify brand

**Input:** "DTC skincare brand on Shopify, 2,800 orders/month growing 8%/month, 35 SKUs, light parcels (0.2-0.6kg), 60% of customers on US coasts, 18% November peak share, 4% returns. Currently self-fulfilling from a garage at ~$4.10/order all-in labor+materials+shipping. Quotes from three 3PLs attached."

**Process:** Profile favors a 2-node (East+West) network. Quote A (big national 3PL): $2.95 pick/pack + storage but $500/month account minimum and 2-day receiving — landed cost $7.84/order including shipping. Quote B (mid-size, beauty-focused): $3.40 pick/pack, no minimums, lot tracking included, landed $7.62. Quote C (cheap regional, single Midwest node): landed $7.15 but average zone 4.6 → 3.8-day delivery vs. 2.1 for B, and no peak surcharge cap. Weighted scores (cost 30/service 25/tech 20/fit 15/contract 10): B 4.2, A 3.6, C 3.1. Reference calls on B confirm 99.6% accuracy but flag invoice errors in months 1-2 — add invoice audit to transition plan. Self-fulfillment comparison: at 2,800 orders the seller's $4.10 excludes shipping (~$4.20 avg), so true current cost ≈ $8.30 — 3PL B saves ~$0.68/order now and scales.

**Output:** Recommend B; negotiate November surcharge cap at 15%, waive onboarding fee against 12-month term with 6-month out clause, SLA credits at <99.3% accuracy. Switching cost ≈ $6,800; payback ≈ 3.6 months at current volume.

## Worked Example 2 — Audit of an underperforming incumbent

**Input:** "We do 12,000 orders/month on Amazon FBM + Walmart + own site. Our 3PL keeps missing the 2pm cut-off and we got hit with $9,400 in 'peak surcharges' we never saw coming. Contract renews in 90 days. Should we leave?"

**Process:** Benchmark the incumbent against the standard fee schedule and SLA norms: cut-off misses (claimed same-day at 2pm, actual 78% same-day ship rate vs. 95%+ norm), surcharges legal per contract clause 7.3 but uncapped — that's a negotiation failure, not fraud. Landed cost currently $6.92/order; two market quotes normalize to $6.55 and $7.10. The 5% saving from the cheaper rival is wiped out for ~5 months by an estimated $31k switching cost (12k orders, 9 channel integrations, inventory transfer). Incumbent scores 2/5 on SLA performance but 4/5 on tech and 4/5 on network fit.

**Output:** Recommend renegotiate-with-credible-alternative: present the rival quote, demand (1) surcharge cap at 12% of monthly invoice, (2) 95% same-day-ship SLA with 2% monthly credits per point below, (3) quarterly business reviews with performance data access, (4) 60-day exit clause. Set a 2-quarter performance gate: if same-day ship <93% by then, execute the switch plan (included, with cutover timed to February volume trough).

## Common Mistakes

1. **Comparing pick fees instead of landed cost per order.** A $0.50 cheaper pick fee is irrelevant if storage, receiving, and packaging fees add $0.90. Always model the full basket.
2. **Evaluating with average orders only.** Peak month economics (surcharges, capacity guarantees, temp labor quality) are where 3PL relationships die. Model November explicitly.
3. **Ignoring zone shift.** Moving inventory from your garage to a single far warehouse can add 1-2 zones to most shipments — shipping costs can rise more than fulfillment fees fall.
4. **Letting the 3PL define the questions.** Demos showcase dashboards; failures happen in receiving docks and exception handling. Ask about the worst order of last December.
5. **Being the smallest client.** Bottom-10% clients get the worst dock priority, the slowest support, and the first capacity cuts at peak.
6. **Signing multi-year terms for an unproven relationship.** Insist on a 3-6 month trial or early-exit clause; a 3PL confident in its service will accept it.
7. **Skipping the exit terms.** Data export format, inventory release timelines, and wind-down fees only matter when leaving — which is exactly when you have no leverage. Negotiate them at signing.
8. **Treating FBA and 3PL as either/or.** Hybrid (FBA for Prime velocity SKUs, 3PL for everything else plus FBA prep) frequently beats both pure options; always check the hybrid case.
9. **Not auditing invoices after onboarding.** First-90-day invoices contain errors at most 3PLs; an invoice audit habit pays for itself immediately.

## Resources

- `references/output-template.md` — comparison scorecard and recommendation format
- `references/evaluation-scorecard-guide.md` — criteria definitions, 1-5 scoring anchors, weighting guidance
- `references/fee-glossary-and-pricing-models.md` — complete 3PL fee schedule, pricing model patterns, landed-cost math
- `assets/3pl-evaluation-checklist.md` — pre-delivery quality checklist
