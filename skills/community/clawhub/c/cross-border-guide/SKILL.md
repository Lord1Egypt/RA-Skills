---
name: cross-border-guide
description: Plan and execute cross-border ecommerce fulfillment — customs documentation, HS codes, duties estimation, and carrier selection for international orders. Use when expanding to international shipping, fixing customs holds, choosing DDP vs DDU, or comparing carriers for a destination market.
---

# Cross-Border Guide

Selling internationally means dealing with customs declarations, import duties, carrier restrictions, and documentation requirements that vary by destination country. Getting any of these wrong leads to shipments held at customs, unexpected duty charges billed to customers, or outright package seizures. This skill helps ecommerce sellers plan and execute cross-border fulfillment by walking through the specific requirements for their product type, origin, and destination markets.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| HS classification | 6-digit HS verified in the destination's tariff database, extended to full national code | 6-digit HS from origin country lookup, flagged for destination verification | Copying a competitor's code or guessing from product name |
| Duty/tax estimate | Computed from destination tariff rate + VAT/GST on correct basis (CIF/FOB), checked against de minimis | Estimated with a reputable landed-cost calculator, basis stated | "Customer will figure out duties" |
| Incoterm choice | Deliberate DDP/DDU choice per market based on AOV vs. de minimis and customer expectations | DDP everywhere via carrier landed-cost service | Defaulting to DDU without telling customers |
| Customs value declaration | Actual transaction price, consistent with payment records | Transaction price minus genuinely separable shipping (where allowed) | Undervaluing to dodge duties |
| Carrier selection | Matched per lane: express vs. postal vs. consolidator by AOV, speed need, and tracking expectations | One express carrier for all international | Cheapest postal option for everything incl. high-AOV |
| Restricted goods check | Product checked against destination prohibited/restricted lists AND carrier dangerous-goods rules | Carrier restriction list checked | Assuming "it's fine, it's just cosmetics" |
| Tax registration | VAT/GST registration thresholds checked per market (UK, EU IOSS, AU, NZ) before launch | Marketplace collects where it is deemed collector | Ignoring until a penalty letter arrives |

## Solves

1. Packages stuck in customs for weeks because of missing or inconsistent documentation (commercial invoice, HS code, declared value mismatches).
2. Customers refusing delivery over surprise duty bills, generating refunds, chargebacks, and one-star reviews.
3. No idea what an international order actually costs to deliver — duties, taxes, brokerage, and surcharges discovered after the sale.
4. Choosing carriers blind: express courier on every order destroys margin; cheap postal on high-value orders destroys customer experience.
5. Products that are restricted in specific markets (batteries, cosmetics ingredients, food, supplements) shipped without checking, then seized.
6. VAT/GST obligations (EU IOSS, UK, Australia) that the seller did not know applied to them.
7. Returns from international customers with no plan, costing more than the product's value.

## Workflow

### Step 1 — Profile the shipment or program
Determine scope: single shipment troubleshooting vs. market-entry program. Collect: product details (materials, function, battery/liquid/powder content), unit value and AOV, origin country and ship-from location, destination market(s), monthly volume per market, current or planned carriers, and whether selling via marketplace (who may be the deemed tax collector) or own site.

### Step 2 — Classify the product (HS code)
Determine the 6-digit harmonized code by function and material using the General Rules of Interpretation: composition first, then primary function. Verify against the destination country's tariff schedule and extend to the national 8-10 digit code. List candidate codes when classification is genuinely ambiguous, and recommend a binding ruling request for high-volume programs. Never present a guessed code as final — misclassification is the root cause of most customs disputes. See `references/hs-codes-and-duties.md`.

### Step 3 — Compute landed cost per market
For each destination: check the de minimis threshold (duty-free and tax-free levels differ), then compute duty = tariff rate × customs value (confirm CIF vs. FOB basis per country), VAT/GST = rate × (customs value + duty + freight where applicable), plus brokerage/disbursement fees by carrier type. Produce a landed-cost table at the seller's actual AOV. Flag markets where AOV sits just above de minimis — a small price or bundling change can drop orders below the threshold.

### Step 4 — Choose Incoterms and tax setup
Decide DDP (seller pays duties/taxes, smooth delivery, higher cost) vs. DDU/DAP (customer pays on delivery, cheaper but refusal risk) per market. Rule of thumb: DDP for markets with low de minimis and high refusal cultures, DDU acceptable where most orders fall under de minimis. Set up tax registrations where required: EU IOSS for ≤€150 consignments, UK VAT for ≤£135, AU/NZ GST registration above turnover thresholds — or confirm the marketplace is the deemed collector. Document who collects what at checkout.

### Step 5 — Select carriers per lane
Match carrier class to lane economics: express integrators (3-5 days, strong tracking, high brokerage — for high AOV), postal/ePacket-type services (7-20 days, cheap, weak recourse — for low AOV under de minimis), and cross-border consolidators/ecommerce specialists (5-10 days, DDP-capable, mid-price — for scale). Check each candidate against product restrictions (lithium batteries, liquids, magnets) and required service features (DDP billing, returns solution). See `references/carrier-selection-guide.md`.

### Step 6 — Build the documentation pack
Specify per shipment: commercial invoice (consistent description, HS code, unit value, origin, Incoterm), packing list, certificates where applicable (origin certificates for FTA claims, MSDS for batteries/liquids, ingredient lists for cosmetics/food), and data-quality rules (description must match HS code and declared value; "gift" marking is fraud). Define the customs-hold escalation path: who calls the broker, what documents go in the response, expected timelines.

### Step 7 — Verify and deliver
Cross-check: declared values consistent with store prices; duty math uses the destination's basis; restricted-goods check done against destination AND carrier lists; returns path defined (local return hub, return-to-sender economics, or refund-without-return threshold). Deliver using `references/output-template.md` and run `assets/cross-border-checklist.md`. State which figures are estimates and recommend verification with a licensed customs broker for high-stakes decisions.

## Worked Example 1 — US skincare brand entering the EU and UK

**Input:** "We sell a vitamin C serum (30ml, glass dropper bottle) from the US, AOV $52, want to launch shipping to Germany, France, and the UK at ~600 orders/month combined. Currently using USPS international with no problems domestically. What do we need?"

**Process:** Classification: beauty/skin-care preparation → HS 3304.99, verify EU TARIC extension (3304.99.00) and UK equivalent — duty rate 0% into both EU and UK for this heading, but VAT applies: DE 19%, FR 20%, UK 20%. De minimis: EU has none for VAT (IOSS covers ≤€150 consignments); UK collects VAT at point of sale for ≤£135. At $52 AOV every order is taxable. Compliance: EU cosmetics require a Responsible Person, CPNP notification, and compliant labeling — this is the gating item, not customs. Carrier: USPS → local post (DDU) risks VAT collection at door plus €6-15 handling fees in DE/FR → refusal risk; recommend IOSS registration (or marketplace/merchant-of-record alternative) + a cross-border consolidator with DDP and 5-8 day delivery at ~$9-12/order vs. $14+ express. Returns: refund-without-return under €30 cost threshold; local return consolidation address in NL once volume justifies.

**Output:** Market-entry plan: (1) appoint EU Responsible Person + CPNP before first shipment — blocking; (2) register IOSS + UK VAT, charge VAT at checkout; (3) consolidator with DDP for EU, express for UK during launch; (4) landed-cost table at $52 AOV per market; (5) documentation pack spec; flagged assumption: 0% duty verified at 6-digit level, broker confirmation recommended for the full TARIC code.

## Worked Example 2 — Customs hold troubleshooting

**Input:** "20 parcels of our wireless earbuds (with charging case) to Canada are stuck at customs for 9 days. Carrier says 'awaiting importer documentation.' We declared $18/unit which is our wholesale cost, retail is $49. Shipped via a postal consolidator, DDU."

**Process:** Root causes ranked: (1) undervaluation — declaring wholesale cost on B2C retail shipments is a value mismatch; CBSA expects transaction value, i.e., the $49 the customer paid (minus separately stated shipping). That mismatch pattern triggers verification holds. (2) Lithium battery documentation — earbuds with charging case need UN3481 compliance marks and may be restricted by the postal consolidator. (3) Missing importer info — DDU postal shipments need the consignee to respond; customers rarely do. Immediate fix: supply corrected commercial invoices at transaction value, battery compliance statement (Watt-hour rating, UN38.3 test summary availability), and request broker intervention. Prevent recurrence: declare actual selling price, switch this product to a carrier with built-in UN3481 handling, move to DDP for Canada (CAD 20 duty / CAD 40 tax de minimis is low — wait, post-CUSMA: CAD 150 duty / CAD 40 tax for US-origin couriers; postal shipments CAD 20) — at $49 AOV, taxes apply: collect at checkout or ship DDP.

**Output:** Same-day action list (corrected invoices, battery docs, broker contact), root-cause explanation of the hold, revised declaration policy (transaction value, with the legal risk of undervaluation stated plainly), carrier switch recommendation with cost delta, and DDP-for-Canada setup. Note: thresholds vary by carrier channel — verified against current CBSA courier remission rules, broker confirmation advised.

## Common Mistakes

1. **Guessing HS codes from product names.** "Earbuds" can classify three ways with different duty rates; classification follows composition and function under the GRI, and the destination's national extension is what customs actually applies.
2. **Declaring wholesale cost instead of transaction value.** B2C customs value is what the buyer paid. Undervaluation is the most common cause of holds — and it is customs fraud, not a gray area.
3. **Treating de minimis as one number.** Duty de minimis and tax de minimis differ, postal vs. courier channels differ, and thresholds change. Check both, per channel, per market, at the time of planning.
4. **Defaulting to DDU and surprising the customer.** Doorstep duty bills plus carrier "advancement fees" cause refusals; every refusal costs return freight or abandonment plus the refund.
5. **Ignoring product-specific regimes.** Cosmetics (EU CPNP/Responsible Person), batteries (UN3481/3480), food/supplements, kids' products, and RF devices have compliance gates that customs paperwork cannot fix.
6. **Using one carrier for every lane.** Express on a $15 AOV product erases margin; postal on a $300 product creates tracking-blind, recourse-free risk. Match per lane.
7. **Inconsistent documents.** Invoice says "cotton t-shirt," HS code says polyester, declared value differs from the store receipt in the box — inconsistency itself triggers inspection.
8. **Marking commercial shipments as gifts.** It does not avoid duties in most markets and it is an explicit false declaration tied to your business identity.
9. **No returns plan.** International return shipping often exceeds product value; decide refund-without-return thresholds and local return hubs before launch, not at the first dispute.

## Resources

- `references/output-template.md` — market-entry plan and troubleshooting output formats
- `references/hs-codes-and-duties.md` — HS classification method, duty/tax math, de minimis patterns
- `references/carrier-selection-guide.md` — carrier classes, lane matching, restricted goods, documentation pack
- `assets/cross-border-checklist.md` — pre-delivery quality checklist
