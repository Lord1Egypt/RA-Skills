# Carrier Selection & Documentation Guide

## 1. Carrier classes

| Class | Transit | Cost | Tracking/recourse | Best for |
|---|---|---|---|---|
| Express integrators (DHL/FedEx/UPS) | 3-6 days | High ($25-60+ typical) | Excellent; built-in brokerage | AOV >$80, time-sensitive, B2B samples |
| Postal network (origin post → destination post) | 7-25 days | Low ($8-20) | Weak; claims slow, DDU handling fees at door | AOV <$40 under de minimis, low urgency |
| Cross-border consolidators / ecommerce carriers | 5-12 days | Mid ($10-20) | Good; DDP options, ecommerce returns | Scale programs 500+ orders/month per region |
| Freight forward + local last mile (bulk pre-position) | 2-5 days local | Lowest per unit at volume | Local-grade | Sustained volume justifying overseas inventory |

**Lane-matching rules:** margin guardrail — total delivery cost (shipping + duties if DDP + brokerage) should stay under 25-30% of AOV for sustainable economics; tracking expectation — markets with high WISMO/chargeback rates need full tracking regardless of AOV; refusal-risk markets favor DDP via consolidator; once a single lane exceeds ~500 orders/month, get consolidator quotes — the discount vs. retail express is typically 30-50%.

## 2. Restricted and regulated goods

Check BOTH the destination country's prohibited/restricted list AND each carrier's own rules — carriers are routinely stricter than the law.

| Category | Issue | Action |
|---|---|---|
| Lithium batteries | UN3480 (standalone, widely banned from post) / UN3481 (in/with equipment, allowed with limits) | Watt-hour limits, UN38.3 test summary on file, proper marks; choose battery-certified carriers |
| Cosmetics/skincare | Ingredient bans, notification regimes (EU CPNP, ASEAN), labeling | Compliance gate before shipping plan |
| Food/supplements | Import permits, ingredient restrictions, registration (e.g., FDA, health authorities) | Often easier via local distributor |
| Liquids/aerosols/perfume | Flammability = dangerous goods; many postal bans | DG-capable carriers only; perfume is the classic seizure item |
| Magnets, power banks, e-cigs | Aviation rules; e-cigs banned in many destination markets entirely | Check per market before listing |
| Wireless/RF devices | Type approval (FCC/CE equivalents) per market | Compliance gate |

## 3. Documentation pack (per shipment)

**Commercial invoice — required fields:** seller and consignee details; customs-grade product description (material + function, not marketing name); HS code; quantity; unit and total transaction value with currency; country of origin (manufacture, not ship-from); Incoterm (DDP/DAP); shipment weight; invoice number tying to the order record.

**Consistency rules (inspection triggers if violated):**
- Description ↔ HS code ↔ declared value must tell one coherent story.
- Declared value = checkout receipt = payment record.
- Origin = manufacturing country, never the warehouse country.
- No "gift" marking on commercial shipments; no vague descriptions ("accessories", "samples").

**Add when applicable:** packing list (multi-carton), certificate of origin (only when claiming FTA preference), MSDS/UN38.3 (batteries, liquids), ingredient/compliance documents (cosmetics, food), import permits (consignee-obtained, confirm before shipping).

**Electronic data:** most channels now require pre-arrival electronic data (e.g., postal EAD, ICS2 in the EU). Garbage descriptions in electronic data cause holds even when paper is perfect — map your product catalog to customs descriptions once, centrally.

## 4. Customs hold escalation SOP

1. Day 0-1: get the specific hold reason from the carrier (not "in customs" — the code/reason). 
2. Identify the defect class: documentation / valuation / classification / regulated goods / consignee non-response / random exam.
3. Respond with the exact missing artifact, through the carrier's broker or your own. Corrected invoices must match payment evidence.
4. Day 7+ without movement: escalate to carrier's clearance team lead; for express carriers invoke their clearance SLA; consider a local broker intervention.
5. Decision point (typically day 14-21): clearance vs. return-to-sender vs. abandonment — compare RTS cost vs. product value vs. re-ship.
6. Log every hold with cause; two holds with the same cause = process fix, not bad luck.

## 5. Returns architecture

- **Refund-without-return threshold:** when return shipping > X% of product value (commonly 60-80%), refund and let the customer keep it; set X explicitly.
- **Local return hubs:** consolidator return address per region; batch return freight monthly. Justified at roughly >50 returns/month per region.
- **Return-to-sender:** express RTS often costs as much as outbound; postal RTS is slow and lossy. Never default to it silently.
- **Exchanges:** ship the replacement immediately on evidence (photo), don't gate on the return arriving — international return transit kills the customer experience.
