# CartPilot Skill

`CartPilot`

One-line positioning:

It does not just help users find cheaper items. It calculates the best final checkout path.

CartPilot does not solve only one question such as "where is it cheaper?"

It solves the harder set of questions that appear right before checkout:
- should this order stay together or be split
- which coupon is the best one to use
- whether a threshold discount is really worth chasing
- whether the user should optimize for the cheapest total, the easiest route, or the fastest arrival
- how to rebalance the basket under the same budget

## Core Positioning

CartPilot is a checkout-strategy skill, not a generic price-comparison skill.

It behaves more like a checkout tactician:
- calculates the real payable total
- decides whether to merge or split baskets
- separates genuine savings from fake threshold wins
- decides which coupon belongs on which cart
- ends with one clear ordering path

By default it tries to converge on three outcomes:
- `Lowest Total Price Plan`
- `Lowest-Friction Plan`
- `Fastest Arrival Plan`

## What Kinds Of Questions It Fits

- "Should I split this order?"
- "Is it worth adding one more item just to reach the threshold?"
- "Which of these two coupons is actually better?"
- "How should I rebalance this basket under the same budget?"
- "This Meituan route is cheaper but 25 minutes slower. Is that worth it?"
- "Taobao, JD, and PDD each have one cheaper part. What is the best final combination?"
- "Do not just compare prices. Tell me how to place the order."

## How It Helps Users

It does not stop at promotion explanation.

It tries to give direct action advice such as:
- keep the order as-is and place it now
- do not force the threshold
- split one item into a separate order
- save the coupon for a different basket
- pay a little more for a faster and cleaner fulfillment path
- redesign the basket for better value under the same budget

## Why This Kind Of Skill Is Worth Building

Many shopping skills solve an information problem.

CartPilot solves a transaction-decision problem.

In many cases the user already has:
- the products
- the prices
- the coupons
- the campaign mechanics

What they still do not have is a trustworthy checkout judgment.

That is why this skill sits closer to actual purchase completion than a standard comparison tool.

## Where It Works Best

### E-commerce Platforms

- Taobao
- Tmall
- JD
- PDD
- VIPSHOP

For these platforms it is especially useful for:
- cart threshold optimization
- cross-platform split ordering
- coupon allocation
- same-budget redesign

### Instant Retail And Local Delivery

- Meituan
- elm

For these platforms it is especially useful for:
- deciding whether red packets and threshold discounts create real savings
- checking whether delivery and packaging fees erase the promo
- deciding whether a small savings gap is worth a much longer ETA
- judging whether a threshold filler item is actually useful

## Typical Output

- `Final Call`
- `Lowest Total Price Plan`
- `Lowest-Friction Plan`
- `Fastest Arrival Plan`
- `Why These Plans Differ`
- `Next Step`

## How It Differs From A Standard Comparison Skill

A normal comparison skill is usually answering:
- which side is cheaper
- where the price gap comes from

CartPilot answers:
- how the final order should be placed
- which plan saves the most
- which plan is the least annoying to execute
- which plan gets the order fastest
- which "cheap" path only looks cheap on the surface

In other words, it is a checkout decision layer rather than an information comparison layer.

## Safety Boundary

| Action | Agent | User |
|------|-------|------|
| Read carts, compare coupons, calculate threshold math, judge split orders | yes | - |
| Recommend checkout plans from public pages or user screenshots | yes | - |
| Log in, read private account-only discounts, claim coupons automatically | no | yes |
| Submit orders or pay | no | yes |

## Install

```bash
clawhub install cartpilot
```

## Short Marketplace Description

Calculate the best final ordering path for a cart: whether to split the order, which coupon is worth using, whether a threshold discount should be chased, and how the cheapest, easiest, and fastest routes compare.

## Version

- `v1.0.0`: initial release of CartPilot as a checkout-path optimization skill

## License

MIT
