---
name: Customs Duty Calculator
description: Estimate import duties, tariffs, and landed costs for cross-border ecommerce shipments by HS code and destination. Use when an ecommerce seller is pricing a product for a new export market, considering DDP vs DDU shipping, or trying to reconcile unexpected duty bills on past shipments.
---

# Customs Duty Calculator

Cross-border ecommerce sellers frequently face unexpected costs when shipping products internationally. Import duties, tariffs, value-added taxes, and various customs surcharges can erode profit margins if not properly estimated before pricing products for foreign markets. This skill helps ecommerce operators estimate the full landed cost of their products by calculating applicable duties and taxes based on Harmonized System (HS) codes, product values, shipping costs, and destination country regulations.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| HS code accuracy | 10-digit code validated against destination country tariff schedule with binding ruling where stakes warrant | 6-digit code with documented logic | Guessed from product name |
| Customs valuation | CIF (Cost + Insurance + Freight) where required; FOB elsewhere; reconciled against the country's WTO Valuation Code interpretation | Product cost + estimated freight | Wholesale price only |
| VAT / sales tax | Applied per destination at correct rate; threshold rules respected (EU IOSS, UK £135 rule, US Section 321) | Applied at standard rate without thresholds | Ignored entirely |
| FTA / preferential treatment | Verified origin documented with Certificate of Origin; FTA invoked only when eligible | FTA assumed and noted to verify | Standard MFN rate used everywhere |
| DDP vs DDU | DDP when duties under USD 50 or buyer-experience matters; DDU when duties large and uncertain | DDU with prepay option | No explicit choice; buyer surprised at delivery |
| Surcharges | All of: MPF, HMF (US); brokerage; carrier disbursement fee; consumption tax included | Brokerage included; surcharges noted | Only base duty + VAT |
| Margin model | Landed cost compared against destination retail in local currency net of platform fees, returns reserve, FX margin | Landed cost vs retail | Wholesale cost only |
| Documentation retention | Commercial invoice, packing list, HS code, declared value, customs paperwork retained 5+ years | 1-2 years | None |

## Problems this skill solves

1. A US seller is pricing for the EU and needs to know the all-in landed cost (duty + VAT + brokerage) per unit.
2. A brand is comparing DDP vs DDU for AE and JP and needs the margin impact of each option.
3. A seller got hit with a USD 4,200 unexpected duty bill on a UK shipment and needs to understand whether HS code, valuation, or VAT was the cause.
4. A founder is choosing between Mexico via USMCA preferential rate and an existing carrier with its own Mexico duty estimate, and wants to confirm which is correct.
5. A team is launching into 5 EU markets and needs a single sheet showing per-SKU landed cost in each.
6. A reseller wants to know the de minimis threshold by country to plan small-parcel shipments below the duty line.
7. A brand needs to model the impact of a tariff change (e.g. US Section 301 increases) on its China-sourced SKUs.

## Workflow

### Step 1: Lock down HS code per SKU
HS codes determine duty rates, surcharges, and FTA eligibility. The first 6 digits are global; digits 7-10 vary by country. Where money matters, get a binding tariff classification ruling from the destination customs authority. See `references/hs-code-guide.md`.

### Step 2: Establish the customs valuation method
Most countries follow the WTO Valuation Code. Default is transaction value (the price paid) but it must be adjusted for cost elements per the country's rules. EU and many others use CIF (cost + insurance + freight); US uses FOB on most entries. Get this right or every downstream number is wrong.

### Step 3: Calculate base duty
Duty = customs value × duty rate for the HS code. Check whether the country has an FTA with the country of origin; if eligible, use the preferential rate. Document the origin rule met (substantial transformation, regional value content, etc.).

### Step 4: Add VAT / GST / consumption tax
VAT applies on (customs value + duty + relevant surcharges). The rate varies by country and product category. Check threshold regimes: EU IOSS (consignment value ≤€150), UK £135 rule, US Section 321 ($800 de minimis as of date of writing — verify currentness), and similar.

### Step 5: Layer in surcharges and broker fees
US adds Merchandise Processing Fee (MPF) and Harbor Maintenance Fee (HMF). Most countries add a carrier disbursement / brokerage fee. Express carriers (DHL, FedEx, UPS) charge their own brokerage. Cumulative effect on small parcels can exceed the duty itself.

### Step 6: Decide Incoterm and pricing model
DDP (Delivered Duty Paid) means the seller pays duty and VAT at clearance. Pros: clean buyer experience, retained margin control. Cons: cash flow, refund complexity. DDU (Delivered Duty Unpaid) means the buyer pays at delivery. Pros: cleaner seller P&L. Cons: surprise fees, refused parcels, NPS damage. See `references/incoterm-tradeoffs.md`.

### Step 7: Reconcile and document
Compare expected landed cost vs invoice once entry clears. Identify any variance. Retain the HS code, declared value, FTA documentation, and customs paperwork for the required period (often 5 years).

## Worked Example 1: US apparel brand shipping to EU consumer

**Inputs:** Single SKU, 100% cotton T-shirt. Wholesale cost USD 8. Retail target EUR 35. Shipping to a German consumer via DHL Express.

**Calculation:**
- HS code 6109.10 (cotton T-shirts, knitted)
- EU duty rate (MFN, no FTA with US): 12%
- Customs value: CIF = USD 8 + freight USD 4 + insurance USD 0.5 = USD 12.5 → EUR ~11.55 (FX 1.08)
- Duty: 11.55 × 12% = EUR 1.39
- VAT base: 11.55 + 1.39 = EUR 12.94
- DE VAT rate: 19%
- VAT: 12.94 × 19% = EUR 2.46
- DHL brokerage: EUR 2.50 (small-package handling)
- **Total landed cost: EUR 17.85** (vs EUR 11.55 cost + freight + insurance)
- **Effective margin at EUR 35 retail: 49%** (before platform fees, FX, returns reserve)

DDP decision: yes, because EUR 6.30 of fees + duty per shirt is poor buyer experience as a surprise.

## Worked Example 2: Brand modeling Section 301 tariff change on China-sourced electronics

**Inputs:** China-sourced wireless earbuds, FOB China USD 22. US destination. Annual volume 50,000 units.

**Before tariff change:**
- HS code 8518.30 (headphones and earphones)
- Standard MFN duty: 4.9%
- Section 301 list 4A: 7.5% (current rate at date of evaluation)
- Combined duty: 12.4%
- Per unit: 22 × 12.4% = USD 2.73
- Plus MPF (0.3464%, min ~USD 32, max ~USD 634): negligible per unit at this volume
- Annual duty: USD 136,500

**After hypothetical Section 301 increase to 25% (announced):**
- Combined duty: 29.9%
- Per unit: 22 × 29.9% = USD 6.58
- Annual duty: USD 329,000
- Incremental annual cost: USD 192,500

**Decision input:** Either absorb (margin impact $192k), raise retail by $4 (consumer impact), or shift sourcing to Vietnam or Indonesia (HS code may classify identically; new origin rules apply). Plan sourcing diversification before the rate takes effect.

## Common Mistakes

1. **Wrong HS code.** A small classification difference can swing duty 5-15 percentage points.
2. **Using FOB where CIF is required.** EU and many others require CIF; missing freight from the customs value underdeclares.
3. **Ignoring VAT.** Duty is often the smaller number; VAT 19-25% on the duty-inclusive base is usually larger.
4. **Forgetting brokerage and carrier disbursement fees.** Small parcels can have 20-30% of total fees come from non-duty line items.
5. **Assuming FTA without proof of origin.** USMCA / CPTPP / etc. require documentation; without it, the MFN rate applies.
6. **Misreading de minimis.** The US $800 de minimis (Section 321) and EU €150 IOSS threshold are real but bounded by anti-stacking and recent enforcement changes; verify currentness.
7. **DDP without monitoring.** DDP is great until duty rates change; rebill or re-price quarterly.
8. **No documentation retention.** Customs audits look back 3-5 years; missing paperwork means accepting the auditor's number.
9. **Mixing currencies.** Customs value in destination currency, retail in destination currency, cost in source currency — declare each conversion explicitly.
10. **Ignoring product-category surcharges.** Alcohol, tobacco, batteries, hazardous goods, and food often carry additional duty schedules or regulatory fees.

## Resources

- `references/hs-code-guide.md` — How to find and validate HS codes, with examples and a binding-ruling primer.
- `references/incoterm-tradeoffs.md` — DDP vs DDU comparison with margin and NPS implications.
- `references/de-minimis-table.md` — De minimis thresholds and VAT thresholds for top 20 markets.
- `references/output-template.md` — Per-SKU landed-cost worksheet template.
- `assets/quality-checklist.md` — 40-point checklist to validate any duty estimate before publication.
