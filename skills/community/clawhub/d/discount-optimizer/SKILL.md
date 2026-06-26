---
name: discount-optimizer
description: Calculate optimal discount levels based on unit cost, conversion targets, and inventory velocity so promos move product without destroying margin.
---

# Discount Optimizer

Discounts are a finance decision wearing a marketing costume. Every point off the price comes straight out of contribution margin, and a discount only pays for itself if it lifts unit volume by more than the margin it gives away. This skill builds discount levels from the unit economics upward — unit cost, platform fees, and contribution margin — then computes the break-even volume lift each depth requires, chooses a promo mechanic that fits the goal, and stress-tests against inventory velocity, so promotions move product without quietly destroying profit.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Discount depth basis | Sized off contribution margin and a break-even lift target | Sized off gross margin, fees estimated | Taken off retail price with no margin math |
| Margin floor | Hard post-promo floor set (e.g. ≥15% CM) and enforced | Soft floor, occasional exceptions | "Just don't sell below cost" |
| Break-even volume lift | Computed via lift = d/(m−d) and compared to realistic demand | Rough rule of thumb (e.g. "needs ~2x") | Assumed any discount increases total profit |
| Promo type choice | Mechanic matched to goal (acquisition vs clearance vs AOV) | Default % off used everywhere | Whatever competitor is running |
| Inventory-velocity trigger | Discount depth scales with days-of-cover and holding cost | Discount when stock "feels old" | Same depth regardless of age/velocity |
| Platform-fee accounting | Commission + payment + affiliate + shipping all netted before margin | Commission only | Fees ignored ("they're small") |
| Stacking rules | Max stacked depth capped; coupons + auto-discount modeled together | One promo at a time enforced manually | Uncapped stacking, shopper finds the floor |
| Anchor price integrity | List price held; discounts time-boxed with clear end date | Occasional sales, list mostly stable | Permanent "sale" price = the real price |
| Promo end + exit | Defined end date and post-promo price plan | Vague "couple of weeks" | Open-ended, becomes the new normal |

## Solves

- **"What discount can I actually afford?"** — converts a margin floor into a maximum discount depth, net of all platform fees.
- **"Will this promo make or lose money?"** — computes the exact unit-volume lift a given discount must achieve to break even on profit.
- **"My sale boosted revenue but profit dropped."** — exposes the gap between top-line lift and the much larger lift discounts require.
- **"How deep should I go to clear aging stock?"** — justifies clearance depth against carrying/holding cost instead of guessing.
- **"Which promo mechanic fits this goal?"** — maps % off, $ off, BOGO, bundles, thresholds, and free shipping to acquisition, AOV, or clearance objectives.
- **"My TikTok Shop margins vanished."** — accounts for platform commission, vouchers, and affiliate commission before setting depth.
- **"Customers only buy on sale now."** — diagnoses anchor-price erosion and customer-trained-to-wait dynamics, with structural fixes.

## Workflow

1. **Assemble unit economics.** Pull selling price, COGS (landed unit cost including inbound freight and duties), and every variable cost per order: platform commission, payment processing, fulfillment/pick-pack, outbound shipping (or the shipping subsidy you eat), affiliate/creator commission, and returns reserve. Compute contribution margin in dollars and as a percent of price. This number — not gross margin — is what a discount eats into.

2. **Set the margin floor and the goal.** Decide the minimum acceptable post-promo contribution margin (a dollar and a percent). Separately, name the objective in one sentence: acquire new customers, raise AOV, clear specific inventory, defend share, or hit a launch-velocity threshold. The floor caps how deep you can go; the goal decides which mechanic and which success metric matter.

3. **Compute the break-even volume lift for a candidate discount.** Use **required-lift % = d / (m − d)**, where `m` is contribution margin as a percent of price and `d` is the discount as a percent of price. This is the additional unit volume needed just to hold total contribution flat. If the required lift exceeds what the channel can plausibly deliver, the discount is too deep — shrink `d` or change the mechanic.

4. **Choose the promo mechanic.** Match the mechanic to the goal: % off for broad pull, $ off for high-ticket clarity, BOGO/B2G1 to move volume while protecting per-unit price perception, bundles to raise AOV and blend margin, spend thresholds to lift basket size, free-shipping thresholds to nudge AOV cheaply, flash/limited-time to create urgency without permanent markdown. See the promo-mechanics guide for fit and risks.

5. **Factor platform fees, commissions, and coupons.** Re-net the post-discount price through the full fee stack — commission is charged on the *discounted* price, but creator/affiliate commission and payment fees also apply, and coupons or platform vouchers may stack. Recompute contribution margin *after* the discount and *after* fees; that is the real `m` that must clear the floor. On TikTok Shop especially, model commission + voucher + affiliate together.

6. **Stress-test against inventory velocity.** Compare current days-of-cover (units on hand ÷ daily sell-through) to your target. For fast movers, prefer shallow discounts or none — you'll sell through anyway. For slow movers or aging stock, weigh the discount against the carrying cost of holding (capital, storage, obsolescence/markdown risk); deeper clearance is justified when holding cost over the expected sell-through window exceeds the extra margin a shallower discount would preserve.

7. **Finalize, guardrail, and monitor.** Lock the depth, mechanic, max stacked depth, start/end dates, and post-promo price. Set guardrails (margin floor, inventory cap, spend cap). After launch, track realized lift vs the break-even lift, blended contribution margin, sell-through, return rate, and new-vs-returning mix — and cut the promo if it's below break-even lift with no strategic payoff.

## Example 1 — $39.90 TikTok Shop product, 20% off

**Unit economics (before any discount):**

- Selling price: **$39.90**
- COGS (landed): **$11.00**
- Platform commission ~5%: 0.05 × $39.90 = **$2.00** (rounded; exact $1.995)
- Payment processing ~2%: 0.02 × $39.90 = **$0.80**
- Outbound shipping (eaten): **$4.50**
- Returns reserve ~3% of price: 0.03 × $39.90 = **$1.20**

Total variable cost = 11.00 + 2.00 + 0.80 + 4.50 + 1.20 = **$19.50**

**Contribution margin (CM):**
- CM$ = 39.90 − 19.50 = **$20.40**
- CM% = 20.40 ÷ 39.90 = **0.5113 → 51.1%**

So `m ≈ 51%` of price flows to contribution. Good headroom.

**Break-even volume lift for a 20% discount:**

Using **required-lift = d / (m − d)** with `d = 0.20`, `m = 0.5113`:

required-lift = 0.20 / (0.5113 − 0.20) = 0.20 / 0.3113 = **0.6425 → ~64.3%**

You must sell **~64% more units** just to keep total contribution flat. Verify by units:

- Baseline 100 units: contribution = 100 × $20.40 = **$2,040**
- Discounted price = 39.90 × 0.80 = $31.92. New variable cost shifts a little — commission and payment fall because they're % of the *lower* price; shipping and returns hold roughly flat. Approximate new variable cost: COGS 11.00 + commission (0.05×31.92=1.60) + payment (0.02×31.92=0.64) + shipping 4.50 + returns (0.03×31.92=0.96) = **$18.70**.
- New CM$ = 31.92 − 18.70 = **$13.22** per unit.
- Units needed to match $2,040: 2,040 ÷ 13.22 = **154.3 units → +54.3%**.

Note the fee-driven nuance: the headline formula (which assumes fixed per-unit cost) says **+64%**; once you account for commission/payment scaling down with the lower price, the true break-even is a bit gentler at **+54%**. Either way, the promo needs roughly **half-again to two-thirds more units** to break even on profit. If TikTok Shop demand for this SKU can realistically jump 60%+ during a boosted/affiliate push, the 20% off is defensible; if a sale typically lifts units only 20–30%, this discount **loses money** and you should go shallower (e.g. 10%) or switch to a bundle.

**Sanity check at 10% off** (`d=0.10`, `m=0.5113`): required-lift = 0.10 / 0.4113 = **0.243 → ~24%**. Far more achievable.

## Example 2 — Slow-moving SKU, clearance justified by holding cost

**Situation:** A seasonal accessory, **400 units** on hand, selling only **~10 units/week** → days-of-cover ≈ 400 ÷ (10/7) = **280 days** of stock. The season ends in **~12 weeks**; after that, demand collapses and you'll likely liquidate at a deep loss or write it off.

**Unit economics:**
- Price: **$24.00**, COGS landed: **$7.00**
- Variable selling cost (commission + payment + shipping + returns): **$6.00**
- Current CM$ = 24 − 7 − 6 = **$11.00**, CM% = 11 ÷ 24 = **45.8%**

**Holding cost of doing nothing.** Carrying cost ≈ capital + storage + obsolescence risk. Assume an annual carrying rate of **25%** of unit cost (3% capital + 7% storage/handling + 15% obsolescence/markdown risk). Per unit per year = 0.25 × $7.00 = $1.75 → ~$0.034/week. Over 12 weeks that's only ~$0.40/unit in *pure* carrying — small. **The real cost is obsolescence:** units unsold at season end realize maybe **$3.00 salvage** (a clearance dump or write-down to near scrap), versus $7 cost — a **~$4.00 loss per unsold unit**, plus the lost contribution you'd never recover.

**The trade-off.** At current velocity you'll sell ~120 of 400 units in 12 weeks, leaving **~280 units** facing salvage. Expected end-state if you do nothing:
- 120 units × $11.00 CM = **$1,320** contribution
- 280 units × (salvage $3.00 − cost $7.00) = **−$1,120** loss
- Net ≈ **+$200**

**Now model a 30% clearance discount.** New price = 24 × 0.70 = **$16.80**. Variable cost drops slightly with the lower price (commission/payment are %): assume **$5.40**. New CM$ = 16.80 − 7.00 − 5.40 = **$4.40/unit** (CM% = 26.2%, still well above zero contribution).

Required-lift on the formula (`d=0.30`, `m=0.458`): 0.30 / (0.458 − 0.30) = 0.30 / 0.158 = **1.90 → +190%** just to break even *on contribution alone*. In a vacuum that looks brutal. But the clearance math is different — you're racing a salvage deadline, not protecting steady-state profit. Suppose 30% off triples velocity to **~30 units/week**, selling **~360 units** over 12 weeks:
- 360 units × $4.40 CM = **$1,584** contribution
- Remaining ~40 units × (−$4.00 salvage loss) = **−$160**
- Net ≈ **+$1,424**

**Verdict:** the deep discount nets **~$1,424 vs ~$200** by converting near-worthless future salvage units into positive (if thin) contribution *now*, before obsolescence destroys them. The break-even-lift formula alone would have rejected the 30% cut; the holding-/obsolescence-cost lens correctly justifies it. **The rule:** for aging inventory, the relevant comparison is *discounted contribution now* vs *salvage value later*, not discounted contribution vs full-price contribution.

## Common Mistakes

1. **Discounting off price instead of margin.** "20% off" is 20% of *revenue* but a far bigger bite of *contribution*. At 50% CM, a 20% price cut removes ~40% of contribution per unit. Fix: always express discount depth as a fraction of contribution and run `d/(m−d)`.
2. **Ignoring platform commission and fees.** TikTok Shop commission, payment processing, and affiliate/creator commission can swallow 10–20% before COGS. Fix: net *all* variable costs before computing `m`, and remember commission is charged on the discounted price.
3. **Assuming revenue lift equals profit lift.** A sale that grows revenue 15% while requiring a 60% unit lift to break even is a profit loser dressed as a win. Fix: compare realized unit lift to the break-even lift, not revenue to revenue.
4. **Training customers to wait.** Predictable, frequent sales teach buyers never to pay full price; full-price sell-through collapses between promos. Fix: vary timing, time-box promos, and reserve depth for genuine clearance or acquisition moments.
5. **Eroding the anchor price.** A "list" price nobody pays stops anchoring value, and platforms/regulators may flag fake reference prices. Fix: hold a credible list price, keep sale windows finite, and return to list after each promo.
6. **Uncapped stacking.** Coupon + automatic discount + platform voucher + free shipping can quietly push a unit below the margin floor or below cost. Fix: cap maximum *combined* depth and model the worst-case stack before launch.
7. **Same depth regardless of velocity.** Discounting a fast mover you'd sell anyway just donates margin; under-discounting a dead SKU lets it rot. Fix: scale depth to days-of-cover and obsolescence risk.
8. **Eating shipping silently.** Free/subsidized shipping is a real discount that rarely appears in the discount math. Fix: include the shipping subsidy in variable cost or treat a free-shipping offer as its dollar value off.
9. **Forgetting returns.** A discount that drives marginal buyers often raises return rate, and returns destroy the unit's entire contribution plus reverse logistics. Fix: carry a returns reserve in unit economics and watch return rate during promos.
10. **No end date or exit price.** Open-ended "sales" become the permanent price and reset the anchor. Fix: set start/end dates and the explicit post-promo price before launch.
11. **Confusing markdown % with margin %.** A 40% markdown does not leave 60% margin; it depends entirely on starting margin. Fix: use the markdown-vs-margin lookup in the margin-math guide.
12. **Bundling without blending margin.** Bundles can hide a low-margin item dragging the basket below the floor. Fix: compute blended CM across the whole bundle, not per item.

## Resources

- **[references/output-template.md](references/output-template.md)** — fill-in Discount Plan deliverable: unit economics, objective, proposed discount + mechanic, break-even lift table, guardrails, and results-tracking table.
- **[references/margin-math-guide.md](references/margin-math-guide.md)** — the core math: contribution vs gross vs net margin, the `d/(m−d)` break-even formula with worked lookup tables, markdown-vs-margin confusion, fee/commission accounting, blended bundle margin, and holding-cost reasoning.
- **[references/promo-mechanics-guide.md](references/promo-mechanics-guide.md)** — every promo mechanic (% off, $ off, BOGO, tiered, bundles, free-shipping threshold, flash, coupon vs automatic, loyalty/first-order) with margin impact, best use, risks, and TikTok Shop notes.
- **[assets/quality-checklist.md](assets/quality-checklist.md)** — pre-launch checklist across unit economics, margin floor, break-even math, mechanic, fees/stacking, inventory fit, anchor-price integrity, and monitoring.
