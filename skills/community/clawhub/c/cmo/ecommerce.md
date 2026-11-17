# Ecommerce and DTC — Margin, MER, Promos, Marketplaces

Applies when `motion` is `ecommerce` or `consumer-app`. The differences from B2B that change every decision: purchases are immediate and repeated, gross margin is the binding constraint, and the platform-reported ROAS on your screen is not profit.

## Contribution Margin Is the Only Scoreboard

```
contribution margin per order = price − COGS − shipping and fulfilment − payment fees − returns provision − variable ad cost
```

Scale only what has a positive contribution margin at the *marginal* order, not the average one. A blended 3× ROAS hides a top-of-funnel campaign losing money on every unit.

- **MER** (marketing efficiency ratio) = total revenue ÷ total advertising spend. Crude, unattributable, and the number most operators trust because it cannot be gamed by attribution windows. Track it daily against a target derived from your margin, not from a benchmark.
- **aMER / new-customer MER** = new-customer revenue ÷ total ad spend. This is the honest acquisition metric; blended MER improves whenever repeat customers grow, which flatters bad acquisition.
- **First-order profitability vs. LTV betting**: paying more than the first order returns is a financing decision. Only make it with a repeat rate you have measured on your own cohorts, and state the payback window in months (`operations.md`).
- Returns are a marketing metric, not just an operations one: a channel or creative with a high return rate is buying revenue you refund. Report net of returns by channel.

## Creative Is the Media Buy

In consumer paid social, targeting is largely delegated to the platform's optimizer, so creative volume and variety are the controllable levers (`paid.md`). Practical implications: a standing production pipeline beats occasional campaigns; user-generated and creator content usually outperforms studio content on cost per acquisition; and hooks in the first seconds decide the whole result. Test concepts, not colours.

## Promo Calendar

Retail calendars are real demand events; they are also where margin dies. Build the year's calendar in advance with each event's *purpose* and *floor*:

- Purpose per event: acquire new customers, clear inventory, reward existing customers, or defend share. The purpose sets the depth and the audience.
- Floor: the discount depth that still leaves positive contribution margin, computed with the break-even lift formula — `break-even lift = d ÷ (m − d)` in margin points (`pricing.md`). 20% off at 50% margin needs 67% more units to stand still.
- Do not discount to the same list on a predictable rhythm; buyers learn it and stop paying full price.
- Prefer bundles, gift-with-purchase, and free shipping thresholds over headline price cuts: they raise average order value instead of resetting the price anchor.
- Measure incrementality on the big events with a holdout audience (`measurement.md`) — most promo revenue is pulled forward from customers who would have bought anyway.

## Retention Economics

Repeat purchase, not acquisition, decides whether a consumer brand survives its own growth.

- Segment by cohort and count **second-order rate** within a defined window (choose the window from your own repurchase curve, and keep the same window forever). The move from first to second order is the largest single drop in the customer lifetime.
- Subscription or replenishment offers convert a purchase into a relationship — but only when consumption is genuinely periodic; forced subscriptions produce chargebacks and complaints, and cancellation must be as easy as signup (`compliance.md`).
- Lifecycle email and SMS carry a disproportionate share of DTC profit because they have no media cost; deliverability and consent rules apply exactly as in `lifecycle.md`.
- Post-purchase is the highest-attention moment you will ever get: shipping notifications are read more than any campaign. Use them for education and cross-sell, not for a discount.

## Site and Merchandising Levers

Ordered by usual impact: product page clarity (photos, sizing, honest delivery dates) → checkout friction (guest checkout, wallets, local payment methods) → shipping cost and threshold shown early → search and filtering → reviews on the page → cross-sell placement. Cart abandonment is mostly a *pricing surprise* problem: total cost visible early beats any recovery email.

## Marketplaces and Retail

| Channel | Buying | Cost |
|---------|--------|------|
| Own store | The customer relationship, the data, the margin | You pay for all traffic |
| Large marketplaces | Existing demand and trust | Fees, ad fees, and no customer relationship |
| Retail / wholesale | Distribution and physical availability (`brand.md`) | Margin, terms, and losing pricing control |
| Social commerce | Impulse demand where attention already is | Platform dependence, thin data |

Rule: build the owned channel with the margin the other channels generate, not the other way round. A brand that only exists inside someone else's marketplace has rented its entire business, and the landlord can see its numbers.

## Consumer-Specific Compliance Traps

Price-comparison and "was/now" claims are regulated in many markets and require the earlier price to have genuinely applied for a set period; countdown timers that reset are treated as misleading; subscription auto-renewal disclosures and easy cancellation are enforced in an increasing number of jurisdictions; and influencer posts require conspicuous disclosure of the commercial relationship. Details and jurisdiction handling in `compliance.md` — do not improvise these, the penalties are public.
