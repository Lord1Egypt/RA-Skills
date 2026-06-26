---
name: Ad Budget Allocator
description: Distribute advertising budget across channels and campaigns based on ROAS targets, funnel stage, and seasonality. Use when an ecommerce seller has a fixed monthly or quarterly ad budget and needs a data-driven allocation across Google Ads, Meta, TikTok Ads, Amazon PPC, Pinterest and across prospecting, retargeting, and brand defense campaigns.
---

# Ad Budget Allocator

Most ecommerce sellers either spread their advertising budget evenly across channels or dump everything into whichever platform performed best last month. Both approaches leave money on the table. This skill builds a structured budget allocation framework that distributes total ad spend across channels (Google Ads, Meta, TikTok Ads, Amazon PPC, Pinterest), campaign types (prospecting, retargeting, brand defense), and time periods based on ROAS targets, funnel stage priorities, seasonal demand patterns, and current performance data.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Channel split method | Marginal ROAS curves with diminishing returns modeled per channel | Historical ROAS weighted by recency and confidence interval | Flat percentage split based on industry averages |
| Prospecting vs retargeting ratio | 70/20/10 rule applied to current funnel volume with retargeting capped at audience size limit | 60/30/10 with quarterly review | Fixed 50/50 split regardless of funnel stage |
| Seasonality adjustment | Demand index per category multiplied by CPM inflation factor for each peak window | Manual lift of 20-40% during known peak weeks | No seasonal adjustment; same monthly plan all year |
| Budget reserve | 10-15% held back for in-flight reallocation to top performers | 5% test budget for new channels | 0% reserve; all spend committed upfront |
| Brand vs nonbrand search | Brand capped at expected organic cannibalization rate; nonbrand sized to nCAC target | Brand at 15-25% of search spend | Brand search uncapped or zeroed out entirely |
| New channel testing | Iso-budget pilot at 5-8% of total for minimum 4 weeks with predefined kill criteria | One-off test with $1-2k | Add new channels mid-quarter without test plan |
| Reporting cadence | Weekly pacing review with monthly reallocation; quarterly strategic rebalance | Monthly review only | Set-and-forget annual plan |

## Problems this skill solves

This skill addresses sellers who are guessing instead of allocating:

1. A seller with $10,000/month says "should I put more into Google Shopping or Meta?" and needs a model that converts ROAS curves into dollar amounts.
2. A DTC manager wants to know whether prospecting or retargeting deserves more budget this quarter based on funnel stage volume and LTV:CAC targets.
3. A brand team is planning Black Friday or Prime Day and must reallocate baseline budget for elevated CPMs, compressed decision windows, and conversion lift.
4. A founder sees Meta delivering 4.2x and Google delivering 3.1x and asks whether to shift $2k from Google to Meta or whether marginal returns will collapse.
5. A team is launching a new channel (TikTok Shop, Pinterest) and needs an iso-budget pilot plan that doesn't strangle the channels already working.
6. An agency is preparing a Q1 plan for a client with $180k annual spend across five channels and needs a defensible distribution.
7. A seller in a category with strong seasonality (gifting, swimwear, outdoor) needs a month-by-month plan that flexes with demand without overcommitting in trough months.

## Workflow

### Step 1: Collect inputs
Gather total budget for the planning window, current channel-level performance (spend, revenue, ROAS, CPM, CPC, CVR by channel last 30-90 days), business goals (revenue target, blended ROAS target or nCAC target), funnel volume (top, mid, bottom of funnel audience sizes), and seasonal context (planned promos, category demand curves). If anything is missing, see `references/input-checklist.md`.

### Step 2: Establish allocation principles
Set explicit principles before touching numbers. Decide on blended ROAS floor, prospecting/retargeting/brand split target, channel diversification minimums (no channel below 5% if kept; no channel above 60% without rationale), reserve percentage, and risk tolerance. Document each principle with the constraint it imposes.

### Step 3: Model marginal returns per channel
For each channel with 90+ days of history, fit a simple diminishing-returns curve (spend vs revenue). Identify the saturation point where incremental ROAS drops below the blended floor. Channels still on the steep portion of the curve get incremental budget; channels at saturation get held flat or reduced. See `references/marginal-roas-model.md`.

### Step 4: Apply funnel stage logic
Split allocation by funnel stage based on business goal. Growth focus = heavier prospecting (65-75%). Efficiency focus = heavier retargeting and brand (40-50% combined). Defensive period = brand defense gets first dollars. Cap retargeting at audience refresh rate (don't budget more than the audience can absorb without frequency fatigue).

### Step 5: Layer seasonality
Multiply baseline monthly allocation by a demand index per channel per month. Peak weeks (Cyber 5, Prime Day, category-specific events) get a CPM inflation buffer (typically +25-40%) plus a conversion lift assumption. Trough months get budget pulled forward into prep weeks rather than wasted on flat demand.

### Step 6: Build the allocation table
Produce a month-by-month, channel-by-channel allocation table with subtotals by funnel stage and a reserve line. Include expected ROAS, expected revenue, and confidence (high/medium/low) per row. Reconcile to total budget.

### Step 7: Define triggers and kill criteria
For each allocation decision, document the trigger that would cause a mid-quarter reallocation (e.g., "if Meta ROAS drops below 2.8 for two consecutive weeks, shift 20% of Meta budget to Google nonbrand"). For new-channel tests, define the success metric, the test window, and the kill criterion before launching.

## Worked Example 1: $45,000/month DTC apparel brand

**Inputs:** $45k monthly budget. Channels: Meta (current ROAS 3.4x at $22k), Google Shopping (4.1x at $14k), TikTok Ads (2.6x at $5k pilot), Pinterest (3.8x at $4k). Blended ROAS target 3.5x. Q3 plan, gearing up for Q4. New customer focus (60% of revenue from new buyers).

**Allocation principles set:** Blended floor 3.3x. Prospecting 65% / retargeting 25% / brand defense 10%. Reserve 10%. No channel above 55% of total.

**Marginal analysis:** Meta curve is flattening at $22k (incremental ROAS ~2.9x). Google still climbing at $14k (incremental ~3.8x). TikTok early-curve at $5k. Pinterest holding steady at $4k.

**Result:**
- Meta: $20k (held back from current to avoid saturation; -$2k)
- Google Shopping: $18k (+$4k into nonbrand and shopping prospecting)
- TikTok Ads: $7k (+$2k test expansion)
- Pinterest: $4k (held flat)
- Brand search: $1k (no change)
- Reserve: $4.5k (for mid-month reallocation to top performer)

**Funnel split:** Prospecting $29k, retargeting $11.5k, brand defense $4.5k.

**Expected blended ROAS:** 3.55x. Expected revenue: $159.7k.

**Triggers:** If Google ROAS stays above 4.0x in week 2, pull $2k from reserve to Google. If TikTok drops below 2.0x by day 14, freeze test and return funds to Meta.

## Worked Example 2: $120,000 Q4 brand seasonal allocation

**Inputs:** $120k for October-December. Category: home gifting. Channels: Meta (3.2x baseline), Google (3.9x baseline), Amazon PPC (4.5x at $8k baseline), Pinterest (2.9x baseline). Q4 demand index: Oct 1.1, Nov 1.6 (Cyber 5 weighted), Dec 1.3.

**Allocation principles:** Blended floor 3.5x weighted by month. Prospecting 55% / retargeting 35% / brand defense 10% (heavier retargeting in Q4 because consideration windows are short). Reserve 12% concentrated in Cyber 5 week.

**Seasonality layer:** CPM inflation +35% Nov 22-Dec 2; conversion lift +50% same window. Amazon PPC gets an additional Prime-adjacent push in early Oct.

**Result by month:**
- October: $30k (Meta $12k, Google $9k, Amazon $5k, Pinterest $2k, brand $1k, reserve $1k)
- November: $54k (Meta $19k, Google $15k, Amazon $11k, Pinterest $3k, brand $2k, reserve $4k)
- December: $36k (Meta $13k, Google $10k, Amazon $7k, Pinterest $2k, brand $2k, reserve $2k)

**Cyber 5 reallocation rule:** During Nov 24-28, shift all reserve plus 15% of Pinterest into top-ROAS channel measured Nov 22.

**Expected Q4 revenue:** $432k blended ROAS 3.6x.

## Common Mistakes

1. **Treating last month's ROAS as next month's ROAS.** ROAS reflects past spend levels; doubling a channel rarely doubles revenue.
2. **Ignoring marginal vs average ROAS.** A channel at 4x average can still have <2x incremental at higher spend.
3. **Letting brand search soak up budget.** Brand search often cannibalizes organic; cap it at expected lift.
4. **Killing tests too early.** New channels need 3-4 weeks minimum before judgment.
5. **Equal monthly allocation in seasonal categories.** Demand is not uniform; budget shouldn't be either.
6. **No reserve.** With 100% of spend committed upfront, there's nothing to pour into the channel that's winning.
7. **Retargeting at the same rate as prospecting.** Retargeting audience size is finite; over-budgeting just inflates frequency.
8. **Adding new channels by stealing from winners.** Fund tests from reserve or efficiency gains, not from your best performers.
9. **Missing the CPM inflation premium during peak windows.** Same dollar buys 30-40% less reach during Cyber 5.
10. **No kill criteria.** Tests that drift without a defined stop become permanent budget leaks.

## Resources

- `references/input-checklist.md` — Full list of inputs needed before building an allocation plan.
- `references/marginal-roas-model.md` — How to fit a diminishing-returns curve from 90 days of channel data.
- `references/seasonality-playbook.md` — Category demand indices and CPM inflation factors for common peak windows.
- `references/output-template.md` — Allocation table template with funnel and channel rows.
- `assets/quality-checklist.md` — 40-point checklist to validate any allocation plan before delivery.
