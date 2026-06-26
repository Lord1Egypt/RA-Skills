# Margin Analysis Framework for Product Bundles

This framework provides a step-by-step method for modeling bundle economics, from component-level costs through cannibalization risk to portfolio-level impact. Use it alongside the main Bundle Strategy workflow (Steps 2 and 4) for rigorous financial analysis.

---

## 1. Component-Level Cost Buildup

Before modeling bundle margins, establish the true landed cost of each component SKU. Many sellers undercount costs, leading to margin models that look good on paper but disappoint in practice.

### Cost Categories to Include

| Cost Category | Description | Example |
|---|---|---|
| **Product COGS** | Raw manufacturing or wholesale purchase price | $5.80 per unit |
| **Inbound freight** | Shipping from supplier to your warehouse, per unit | $0.45 per unit |
| **Customs / duties** | Import duties if sourcing internationally | $0.30 per unit (6% duty rate) |
| **Warehousing** | Storage cost allocated per unit per month | $0.12 per unit/month |
| **Pick and pack** | Labor and materials to pick, pack, and label one unit | $1.20 per unit |
| **Packaging materials** | Box, tissue, insert card, tape | $0.80 per unit |
| **Quality inspection** | Inbound QC sampling cost amortized | $0.05 per unit |

### Bundle-Specific Additional Costs

| Cost Category | Description | Example |
|---|---|---|
| **Kitting labor** | Labor to assemble bundle from components | $0.75-2.00 per bundle |
| **Bundle-specific packaging** | Custom sleeve, box, or wrap for the bundle | $1.00-3.50 per bundle |
| **Bonus item cost** | Landed cost of the free bonus item | $1.40 per bundle |
| **Bundle insert** | Printed card with usage instructions, cross-sell | $0.15 per bundle |

### Formula: True Landed Cost per Bundle

```
Bundle Landed Cost = SUM(Component Landed Costs) + Kitting Labor + Bundle Packaging + Bonus Item Cost + Bundle Insert
```

### Example Calculation

| Component | Product COGS | Freight | Pick/Pack | Subtotal |
|---|---|---|---|---|
| Gentle Cleanser | $5.80 | $0.45 | $1.20 | $7.45 |
| Vitamin C Serum | $8.20 | $0.45 | $1.20 | $9.85 |
| Daily Moisturizer SPF 30 | $7.40 | $0.45 | $1.20 | $9.05 |
| **Component subtotal** | | | | **$26.35** |
| Kitting labor | | | | $1.25 |
| Custom sleeve | | | | $1.80 |
| Bamboo face cloth (bonus) | | | | $1.40 |
| Printed routine card | | | | $0.15 |
| **Total bundle landed cost** | | | | **$30.95** |

Note: If the three items were shipped as separate orders, pick/pack would be $3.60 total. Kitting consolidates into a single pick, but adds kitting labor ($1.25). Net fulfillment savings from bundling: $3.60 - ($1.20 pick for one package + $1.25 kitting) = $1.15 saved. Factor this into the margin model as a bundling efficiency gain.

---

## 2. Margin Modeling at Multiple Price Points

Test at least three price points to understand the margin sensitivity curve. Use these three standard tiers as a starting framework, then adjust based on competitive positioning and customer segment data.

### Margin Table Template

| Metric | Tier 1 (15% off) | Tier 2 (20% off) | Tier 3 (25% off) |
|---|---|---|---|
| Sum of component retail prices | $94.00 | $94.00 | $94.00 |
| Bundle price | $79.90 | $75.00 | $70.50 |
| Bundle landed cost | $30.95 | $30.95 | $30.95 |
| Gross margin ($) | $48.95 | $44.05 | $39.55 |
| Gross margin (%) | 61.3% | 58.7% | 56.1% |
| Platform/marketplace fee (if applicable, 15%) | $11.99 | $11.25 | $10.58 |
| Net margin ($) after platform fee | $36.96 | $32.80 | $28.97 |
| Net margin (%) after platform fee | 46.3% | 43.7% | 41.1% |

### Channel-Specific Margin Floors

Different channels have different acceptable margin floors based on their cost structures:

| Channel | Minimum Acceptable Gross Margin | Rationale |
|---|---|---|
| DTC (own website) | 55% | Must cover CAC, site ops, returns |
| Amazon / Marketplace | 35% | Platform fees included; lower CAC |
| Wholesale to retail | 25% | No fulfillment or CAC; retailer takes margin |
| Subscription bundle | 45% | Lower CAC on repeat but higher churn risk |

If your bundle margin at any price point falls below the channel floor, do one of:
1. Remove or swap the lowest-margin component.
2. Reduce the discount tier.
3. Increase the bundle price and strengthen perceived value through bonus items or premium packaging.

---

## 3. Incremental Margin Per Order Analysis

The most important question is not "What is the bundle margin?" but "Does the bundle generate more margin dollars per order than the current average order?"

### Calculation

```
Current Average Margin per Order = Current AOV x Current Average Margin %

Bundle Margin per Order = Bundle Price x Bundle Margin %

Incremental Margin = Bundle Margin per Order - Current Average Margin per Order

Incremental Margin % = Incremental Margin / Current Average Margin per Order x 100
```

### Example

| Metric | Current (Solo Serum) | Bundle (Morning Glow Kit) |
|---|---|---|
| Order value | $42.00 | $75.00 |
| Margin % | 80.5% | 58.7% |
| Margin $ per order | $33.81 | $44.05 |
| **Incremental margin** | -- | **+$10.24 (+30.3%)** |

Even though the bundle has a lower margin percentage (58.7% vs. 80.5%), it generates $10.24 more absolute margin per order. This is the metric that matters. Percentage margin is a vanity metric when comparing single-item orders to bundle orders.

### When Incremental Margin Is Negative

If the bundle generates fewer margin dollars per order than the current average, the bundle is destroying value unless it:
- Drives enough net-new customers to offset the per-order loss.
- Clears distressed inventory that would otherwise be marked down further.
- Seeds a consumable repurchase cycle with high LTV.

Document the strategic rationale explicitly if proceeding with a negative-incremental-margin bundle.

---

## 4. Break-Even Volume Analysis

How many bundles must you sell to recover any fixed setup costs (photography, packaging design, listing creation, ad spend for launch)?

### Formula

```
Break-Even Units = Fixed Launch Costs / Margin per Bundle

Time to Break-Even = Break-Even Units / Projected Monthly Bundle Velocity
```

### Example

| Fixed Cost | Amount |
|---|---|
| Product photography (bundle shot) | $350 |
| Custom sleeve design | $200 |
| Sleeve printing (MOQ 1,000 units) | $1,200 |
| Launch ad spend (first 14 days) | $2,000 |
| Listing creation / copywriting | $250 |
| **Total fixed costs** | **$4,000** |

Margin per bundle (at $75.00 price): $44.05

Break-even: $4,000 / $44.05 = **91 bundles**

Projected velocity: 400 bundles/month

Time to break-even: 91 / 400 = **6.8 days**

If break-even takes longer than 60 days, scrutinize the fixed costs or increase projected velocity through stronger promotion.

---

## 5. Cannibalization Risk Model

Cannibalization occurs when bundle sales replace solo sales of the anchor product at a lower margin per unit. The goal is to ensure total category margin (solo + bundle combined) exceeds the pre-bundle baseline.

### Step-by-Step Cannibalization Analysis

**Step 1**: Record current monthly baseline for the anchor SKU.

| Metric | Baseline Value |
|---|---|
| Monthly solo units | 1,800 |
| Solo margin per unit | $33.81 |
| Total monthly solo margin | $60,858 |

**Step 2**: Define scenario parameters.

| Parameter | Conservative | Expected | Worst Case |
|---|---|---|---|
| % of solo buyers switching to bundle | 15% | 20% | 30% |
| Net-new bundle buyers (as % of switch volume) | 80% | 50% | 0% |

"Net-new" means customers who would not have bought anything without the bundle. An 80% net-new rate is optimistic; 0% is the stress test.

**Step 3**: Calculate each scenario.

For the Expected scenario:
- Solo units lost to switching: 1,800 x 20% = 360
- Bundle units from switchers: 360
- Net-new bundle units: 360 x 50% = 180
- Total bundle units: 360 + 180 = 540
- Remaining solo units: 1,800 - 360 = 1,440

| Revenue Stream | Units | Margin/Unit | Total Margin |
|---|---|---|---|
| Solo serum sales | 1,440 | $33.81 | $48,686 |
| Bundle sales | 540 | $44.05 | $23,787 |
| **Total** | | | **$72,473** |
| **vs. Baseline** | | | **+$11,615 (+19.1%)** |

**Step 4**: Identify the kill threshold.

Find the switching rate at which total margin equals the baseline (the "break-even switching rate"):

```
Break-even switching rate = Baseline margin / (Solo margin/unit x Current units - Bundle net margin gain per switched unit)
```

If the break-even switching rate is below 40%, the bundle is robust. If it is below 20%, the bundle is risky and depends on net-new acquisition.

### Cannibalization Monitoring After Launch

Track these weekly during the first 30 days:

| Metric | How to Measure | Red Flag |
|---|---|---|
| Anchor solo unit trend | Compare to same period last year (seasonality-adjusted) | > 15% decline in solo units not offset by bundle volume |
| Bundle attach rate | Bundle orders / (bundle orders + anchor solo orders) | > 40% attach rate (too many switchers, too few net-new) |
| Total category margin | Solo margin + bundle margin combined | Declining vs. pre-launch baseline |
| Customer overlap | % of bundle buyers who previously bought anchor solo | > 70% overlap means you are discounting existing customers |

---

## 6. Portfolio-Level Margin Impact

When running multiple bundles simultaneously, analyze the aggregate impact on your product portfolio.

### Portfolio Margin Dashboard

| Bundle | Monthly Units | Revenue | Margin $ | Margin % | Solo Cannibalization | Net Margin Impact |
|---|---|---|---|---|---|---|
| Morning Glow Kit | 512 | $38,400 | $22,554 | 58.7% | -$4,114 | +$18,440 |
| Night Repair Duo | 340 | $18,360 | $9,914 | 54.0% | -$2,200 | +$7,714 |
| Travel Essentials Set | 280 | $11,200 | $5,600 | 50.0% | -$840 | +$4,760 |
| **Portfolio total** | **1,132** | **$67,960** | **$38,068** | **56.0%** | **-$7,154** | **+$30,914** |

### Cross-Bundle Cannibalization

Check whether multiple bundles cannibalize each other, not just solo products. If the Morning Glow Kit and Night Repair Duo share the Vitamin C Serum, a customer choosing one bundle may skip the other. Track:

- Percentage of customers buying 2+ bundles (low cross-bundle cannibalization if > 5%).
- Whether introducing Bundle B decreased Bundle A sales.

### Portfolio Mix Target

As a rule of thumb, bundles should represent 15-30% of total SKU revenue. Below 15%, bundles are not contributing meaningfully to AOV. Above 30%, your catalog may be over-reliant on discounted combinations, and solo product pricing power erodes.

---

## 7. Margin Sensitivity Checklist

Before finalizing a bundle, stress-test the margin model against these scenarios:

| Scenario | How to Test | Acceptable Outcome |
|---|---|---|
| Component cost increases 10% | Recalculate margin at current bundle price | Margin stays above channel floor |
| Return rate doubles | Add return processing cost ($5-8/unit) to 10% of bundles | Total margin still exceeds baseline |
| Platform fee increases 2 points | Recalculate net margin at 17% fee | Margin stays above floor |
| Discount creep (competitors force price match) | Model margin at 5% deeper discount | Margin stays above floor |
| Shipping cost surge (peak season) | Add $2-3/unit to fulfillment cost | Margin stays above floor |
| Exchange rate moves 8% (imported goods) | Recalculate COGS with 8% currency shift | Margin stays above floor |

If more than two scenarios breach the margin floor, the bundle is fragile. Strengthen it by:
- Swapping in a higher-margin component.
- Reducing the discount tier.
- Negotiating better supplier pricing at bundle-projected volumes.
- Pre-buying inventory to lock in current costs.

---

## 8. Margin Model Template (Spreadsheet-Ready)

Use these column headers to build a margin model in your spreadsheet tool:

```
SKU | Product Name | Retail Price | COGS | Freight | Pick/Pack | Landed Cost |
Standalone Margin % | Bundle Role | Quantity in Bundle

Bundle Name | Sum Retail | Discount % | Bundle Price | Total Landed Cost |
Kitting Cost | Packaging Cost | Bonus Item Cost | Total Bundle Cost |
Gross Margin $ | Gross Margin % | Platform Fee % | Platform Fee $ |
Net Margin $ | Net Margin % |
Solo Anchor Margin $/Order | Incremental Margin $ | Incremental Margin %

Scenario | Switch Rate | Net New Rate | Solo Units | Bundle Units |
Solo Margin Total | Bundle Margin Total | Combined Margin | vs. Baseline $ | vs. Baseline %
```

Populate one row per discount tier, one row per cannibalization scenario. This gives you a single-sheet view of the full margin picture.
