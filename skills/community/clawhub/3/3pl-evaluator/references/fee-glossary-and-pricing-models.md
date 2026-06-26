# 3PL Fee Glossary & Pricing Models

Use this schedule to force every candidate quote into the same shape. Any line a 3PL cannot quote in writing is a question to escalate, not a zero.

## Complete fee schedule (ask for every line)

### Inbound / receiving
- Receiving per pallet / per carton / per unit (varies 3x between providers)
- Container unload (20ft/40ft, floor-loaded vs. palletized)
- Non-compliant shipment fee (missing labels, mixed cartons)
- Appointment no-show / dock detention pass-through

### Storage
- Pallet / bin / shelf per month — and whether billed on calendar month or daily average
- Cubic-foot billing alternative (often cheaper for small goods)
- Long-term storage surcharge (typically after 180 or 365 days)
- Peak-season storage premium (Q4 multipliers of 1.5-3x exist)

### Outbound / fulfillment
- Pick fee: first item vs. additional items (the spread matters for multi-item orders)
- Pack fee or per-order fee (sometimes merged with first pick)
- Packaging materials: box/mailer/dunnage at cost, cost-plus, or flat
- Branded packaging / inserts / kitting per touch
- Oversized / heavy / fragile handling surcharges
- B2B/wholesale order handling (case pick, pallet build, routing guide compliance, EDI)

### Shipping
- Rate card basis: published-minus-discount vs. cost-plus vs. marked-up retail
- DIM weight divisor used (139 vs. 166 changes everything for light bulky goods)
- Residential, fuel, delivery-area surcharges passed through
- Peak surcharges: capped or uncapped (get the cap in writing)

### Returns
- Return receiving + inspection per unit
- Restock vs. dispose vs. quarantine handling
- Return shipping label pass-through or markup

### Account / technology
- Onboarding / implementation fee
- Monthly account minimum or management fee
- Software/integration fee per channel or per order
- Reporting or API access tiers
- Special projects hourly rate (cycle counts, relabeling, photo audits)

### Exit
- Wind-down / inventory release fee
- Data export provision
- Final invoice timing and dispute window

## Pricing model patterns

**Per-activity (à la carte).** Every touch billed. Transparent but invoices are complex; good for unusual order profiles. Watch the additional-pick fee and packaging markups.

**Bundled per-order.** One fee covers pick+pack+materials. Simple, good for uniform single-item orders; bad for multi-item or variable baskets (the bundle prices in the worst case).

**Tiered volume pricing.** Rates step down at volume thresholds. Confirm whether tiers apply retroactively to all orders or only marginal orders, and what happens in a slow month.

**Cost-plus shipping.** 3PL passes carrier invoice plus fixed %. Aligns incentives; demand carrier invoice visibility.

**All-in landed pricing.** Single quoted price per shipped order including shipping by zone band. Easiest to compare, rarest in practice; verify what bursts it (DIM, surcharges, peak).

## Landed cost per order — the math

1. Build the basket: from real order data take item-count mix, weight bands, and zone distribution (e.g., 70% 1-item ≤0.5kg, 20% 2-item, 10% ≥2kg; zones: 25% z2, 35% z4, 30% z5, 10% z7-8).
2. Per candidate: receiving cost ÷ units per inbound × units per order + storage per unit-month × average months on shelf + pick/pack for the basket + materials + shipping basket average + returns rate × return handling + (account fees + minimums + tech fees) ÷ monthly orders.
3. Compute twice: regular month and peak month (apply surcharges, peak storage, and the seller's peak volume multiplier).
4. Sanity bands: typical DTC light-parcel landed cost runs $6-11/order domestic US all-in; sub-$5 quotes usually hide shipping markups or assume unrealistic zone profiles — recheck.

## Volume thresholds (rules of thumb, flag as heuristics)

- <400 orders/month: most 3PLs' minimums make self-fulfillment or merchant-of-record platforms cheaper.
- 400-2,000: regional 3PLs and startup-friendly providers; avoid big nationals' minimums.
- 2,000-20,000: sweet spot for mid-size 3PLs; two-node networks start paying for themselves around 5,000+ orders/month with coastal customer density.
- >20,000: enterprise tier; custom pricing, dedicated space, quarterly business reviews are standard — negotiate everything.
