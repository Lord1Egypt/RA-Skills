---
name: Dropship Evaluator
description: Evaluate dropshipping product opportunities and supplier reliability by scoring margin potential, shipping times, supplier communication quality, and sample quality to reject dud products before sinking ad spend on them.
---

# Dropship Evaluator

Score dropshipping product ideas and their suppliers before committing ad budget. This skill helps you reject duds early, prioritize winners, and document supplier evaluations so nothing gets approved on gut feel alone.

## Quick Reference

| Decision | Strong ✅ | Acceptable ⚠️ | Weak ❌ |
|---|---|---|---|
| **Gross margin** | ≥60% after COGS + shipping | 45–59% | <45% |
| **Supplier response time** | <4 hours | 4–24 hours | >24 hours or templated |
| **Shipping time to target market** | ≤12 days | 13–20 days | >20 days |
| **Sample quality** | Matches listing; no defects | Minor cosmetic issues | Defects, wrong specs, or refused sample |
| **Saturation signal** | <3 established sellers; no brand dominant | 4–8 sellers, none dominant | Top seller has 10K+ reviews |
| **Ad angle uniqueness** | Clear hook not used by existing sellers | Slight overlap with existing ads | Same angle as top performer |
| **Supplier MOQ / flexibility** | No MOQ or MOQ ≤20 units | MOQ 21–100 units | MOQ >100 units |

## Solves

1. **Gut-feel sourcing** — gives numeric scores to replace "I have a good feeling about this"
2. **Surprise quality failures** — forces a sample order before ad spend begins
3. **Margin erosion at scale** — surfaces hidden costs (returns, processing fees, platform cut) upfront
4. **Supplier ghosting after launch** — evaluates communication before you depend on them
5. **Saturation blind spots** — checks review counts, ad library, and AliExpress listing ages
6. **Single-supplier risk** — flags when no backup supplier exists for a winning product
7. **Shipping complaint spikes** — benchmarks expected delivery time against your niche's tolerance

## Workflow

### Step 1 — Product Idea Screening (5 minutes)

Before sourcing anything, run a quick market filter.

1. Search the product on AliExpress, CJdropshipping, and Zendrop.
2. Check the oldest listing date — if the product has been there 5+ years, saturation risk is higher.
3. Open Meta Ad Library and search the product name. Count active ads, especially those running 90+ days (signals profitability).
4. Search Amazon for the product. Note the #1 seller's review count. >5,000 reviews = brand moat risk.
5. Score on three axes: **Demand evidence** (people are buying), **Competition headroom** (you can compete), **Margin potential** (price point allows ≥60% gross margin).

If all three axes are Green, proceed. Two Green, one Yellow = proceed with caution. Any Red = document and skip.

### Step 2 — Supplier Shortlist

1. Find 3–5 potential suppliers on AliExpress, CJ, or Spocket.
2. For each, note: orders fulfilled, average response time shown, rating, listing age.
3. Send an inquiry message to each asking: (a) current stock level, (b) typical ship time to [your target country], (c) whether they offer white-label packaging, (d) your projected order volume per month.
4. Measure response time precisely. Flag any who send copy-paste template responses without answering your questions.
5. Shortlist the top 2–3 based on response quality and speed.

### Step 3 — Cost & Margin Modeling

Fill in the Margin Calculator for each shortlisted supplier:

| Cost Item | Amount |
|---|---|
| Product COGS | |
| Shipping to customer | |
| Platform fee (Shopify, WooCommerce) | |
| Payment processing (2.9% + $0.30 avg) | |
| Expected return rate cost (2–5% of GMV) | |
| Ad cost per order (target CPA) | |
| **Total cost** | |
| **Selling price** | |
| **Net margin** | |

If net margin after ad cost is <15%, the product needs a higher price point or lower COGS before proceeding.

### Step 4 — Sample Ordering

1. Order a sample from your top 2 suppliers. Pay for expedited shipping — you need the result in days, not weeks.
2. When samples arrive, evaluate against the **Sample Quality Checklist** (see assets/).
3. Photograph all sides of the product and packaging.
4. Note actual delivery time vs. supplier's stated estimate.
5. Test the product's core function (if applicable).
6. Compare sample to the supplier's listing photos. Flag any significant discrepancies.

A supplier who refuses to send samples or quotes an unusually high sample price is a red flag.

### Step 5 — Supplier Communication Stress Test

Before approving a supplier, simulate a problem:

1. Email them asking about a "customer complaint" (damaged product scenario).
2. Ask what their replacement/refund process is.
3. Ask what happens if a shipment is lost in transit.
4. Measure response speed and policy clarity.

Suppliers who deflect, blame customers, or take >48 hours to respond to a problem scenario will cause you pain at scale.

### Step 6 — Final Scoring & Decision

Score each supplier across 7 dimensions (1–5 scale each):

1. Gross margin potential
2. Supplier response quality
3. Shipping speed to market
4. Sample quality
5. Market saturation level (inverted — low saturation = high score)
6. Ad angle uniqueness
7. Supplier flexibility / backup availability

Total possible: 35 points.
- 28–35: Proceed with confidence
- 21–27: Proceed with mitigation plan
- <21: Skip or renegotiate

### Step 7 — Documentation & Launch Brief

Document the evaluation in the Output Template so your team or VA knows exactly what was decided and why. Include: winning supplier, backup supplier, agreed pricing, expected margins, launch ad angle, and who approved it.

## Worked Examples

### Example A — Posture Corrector (Approved, Score: 30/35)

**Product**: Adjustable posture corrector brace  
**Target market**: US  
**Selling price**: $34.99

**Market check**: 12 active Meta ads (4 running 90+ days). Amazon #1 seller has 3,200 reviews (manageable). Multiple angles available (back pain, desk workers, athletes).

**Suppliers evaluated**: 3 (AliExpress × 2, CJ × 1)  
**Winner**: CJ supplier — responded in 2 hours, answered all 4 questions, offered custom packaging.

**Margin model**:
- COGS: $6.20
- Shipping to US: $4.80
- Platform + payment: $1.60
- Returns (3%): $1.05
- Target CPA: $12.00
- **Total cost**: $25.65
- **Net margin**: $9.34 (26.7%)

**Sample result**: Arrived in 9 days. Build quality matched listing. Minor logo placement issue — supplier fixed on request.

**Decision**: Approved. Launch with "desk worker" angle. Primary supplier: CJ. Backup: AliExpress supplier B.

---

### Example B — Magnetic Eyelashes (Rejected, Score: 17/35)

**Product**: Magnetic false eyelash kit  
**Target market**: UK  
**Proposed selling price**: £19.99

**Market check**: 40+ active Meta ads, many running 180+ days. Saturated angle. Amazon has 3 sellers each with >8,000 reviews.

**Supplier check**: All 3 suppliers responded within 6 hours (good), but COGS was £5.50 + £6.20 shipping to UK.

**Margin model**:
- COGS + shipping: £11.70
- Platform + payment: £0.90
- Returns (8% — high for cosmetics): £1.60
- Target CPA: £9.00
- **Total cost**: £23.20
- **Revenue**: £19.99
- **Net margin**: –£3.21 (negative)

**Decision**: Rejected. Margin is negative even before returns. Market too saturated for price increases to work.

## Common Mistakes

1. **Skipping the sample step** — "the listing photos look good" is not due diligence. Samples surface packaging quality, actual dimensions, and delivery reality.

2. **Modeling margin without ad cost** — gross margin looks great until you add a $15 CPA and realize you're losing money.

3. **Using only one supplier source** — AliExpress only means you miss CJ, Zendrop, and local 3PLs that often have better margins or faster shipping.

4. **Ignoring review velocity, not just count** — a product with 500 reviews but 50 added in the last 30 days is heating up. High velocity = increasing competition.

5. **Approving a supplier based on chat, not sample** — supplier communication might be excellent but their fulfillment centre ships wrong SKUs or mismatches variants.

6. **Forgetting return rate by category** — electronics and clothing return rates are 2–3× higher than home goods. Not adjusting for this ruins margin models.

7. **Not testing the stress scenario** — suppliers who handle problem resolution poorly destroy your customer reviews, not theirs.

8. **Locking into one shipping method** — ePacket, YunExpress, and DHL have wildly different prices and timelines. Model the method your supplier actually uses, not their fastest option.

9. **Evaluating in isolation** — check that your winning angle isn't already being used by a competitor with a larger ad budget. Search Meta Ad Library by creative theme, not just product name.

10. **No backup supplier on file** — when your primary supplier goes out of stock or raises prices after you've scaled, having a pre-evaluated backup saves the product.

## Resources

- [Output Template](references/output-template.md) — Standardized evaluation report format
- [Supplier Evaluation Guide](references/supplier-evaluation-guide.md) — Detailed supplier scoring criteria
- [Margin Calculator Guide](references/margin-calculator-guide.md) — Full margin modeling worksheet
- [Quality Checklist](assets/dropship-evaluator-checklist.md) — 40-point sample and supplier checklist
