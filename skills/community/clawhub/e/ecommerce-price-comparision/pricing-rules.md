# Pricing Rules — Standardizing Price Basis Across Platforms

## Core Objective

The goal of price normalization is to determine which price on a listing should be used for valid cross-platform comparison.

A platform listing may show multiple numbers at once, including:
- list price
- crossed-out price
- promo price
- coupon price
- member price
- pre-sale price
- deposit amount
- group-buy price
- livestream price
- subsidy price
- shipping fee
- installment display
- “from” price for variants

The Agent must determine:

1. which number is the relevant comparison price
2. whether that price is unconditional or conditional
3. whether shipping should be included
4. whether the displayed amount is complete, partial, or uncertain
5. whether a strict cheapest conclusion is allowed

A correct same-product match is not enough.  
The price basis must also be comparable.

---

## Price Outcome Types

Each candidate listing should produce one of the following price outcomes.

### 1. Final Payable Price
The best available estimate of what the user actually needs to pay to place the order under normal stated conditions.

This is the preferred basis for comparison.

### 2. Conditional Payable Price
A payable price that depends on a condition such as:
- coupon collection
- membership
- first-order status
- livestream access
- group-buy participation
- regional subsidy
- payment-method-specific discount

This can be compared only if the condition is stated clearly.

### 3. Reference Price Only
A visible price that is not enough to estimate what the user will actually pay.

Examples:
- crossed-out price
- deposit only
- “from ¥199”
- teaser price without activation path

This cannot support a strict cheapest conclusion.

### 4. Uncertain Price
Use when the Agent cannot confidently determine the real payable amount from visible signals.

This must remain uncertain.

---

## Price-field Priority

When multiple price fields appear on the same listing, the Agent should prefer them in the following order:

1. final payable price
2. coupon-applied payable price with clear conditions
3. promotion price
4. list price
5. teaser or “from” price
6. deposit amount only
7. crossed-out price

### Rule
Use the highest-quality payable field available, not the smallest visible number.

---

## Core Price Definitions

The Agent should normalize platform prices into shared concepts.

### 1. List Price
The ordinary displayed selling price before extra discounts.

### 2. Promo Price
A discounted platform price shown on the listing page without requiring extra steps beyond normal purchase flow.

### 3. Coupon Price
A price available only after applying a coupon.

The Agent must determine whether the coupon is:
- universally claimable
- conditionally claimable
- uncertain

### 4. Member Price
A price available only to store or platform members.

This is conditional unless membership is clearly low-friction and effectively universal.

### 5. Group-buy Price
A lower price that requires multi-person participation.

This is not the same as a solo-buyer price.

### 6. Livestream Price
A price available only during a live event or through a livestream path.

This is conditional and often unstable.

### 7. Pre-sale Price
A future-order price associated with a pre-sale process.

This may be usable only if the final payable amount is clearly known.

### 8. Deposit Amount
A partial prepayment, not the total order price.

This is never a valid final comparison price by itself.

### 9. Subsidy Price
A price lowered by platform or regional subsidy.

This is conditional if eligibility is limited or uncertain.

### 10. Shipping Fee
A separate logistics charge that may materially change the user’s real cost.

This must be included when it changes the payable ranking meaningfully.

---

## Default Comparison Basis

Unless the user requests otherwise, the Agent should compare listings using:

**final payable price including material shipping cost under clearly stated conditions**

This means:
- prefer what the user actually needs to pay
- include shipping when it meaningfully changes cost
- label conditions rather than hiding them
- avoid teaser numbers

---

## Unconditional vs Conditional Price

### Unconditional Price
A price that a typical buyer can pay without extra eligibility, gated access, or special status beyond normal purchase flow.

### Conditional Price
A price that depends on something beyond ordinary purchase flow.

Examples:
- member-only discount
- first-order discount
- livestream coupon
- group-buy
- student discount
- regional subsidy
- card-specific discount

### Rule
Conditional prices can be useful, but they must not be presented as unconditional default prices.

---

## Deposit and Pre-sale Handling

### Deposit-only Display
If the listing only shows a deposit amount, the Agent must not use it as the comparison price.

### Pre-sale with Known Total
If the listing clearly states:
- deposit amount
- tail payment
- total payable amount

then the Agent may use the total payable amount, but must label the result as pre-sale.

### Pre-sale with Unknown Final Price
If the listing shows only deposit or teaser phrasing, the price basis remains incomplete.

### Rule
Deposit is not price.
Pre-sale is a fulfillment condition and may affect recommendation ranking even when total payable amount is known.

---

## Shipping Rules

Shipping must be handled explicitly.

### When shipping must be included
Include shipping when:
- one platform has free shipping and another has material paid shipping
- shipping changes the payable ranking
- the product price is low enough that shipping is a significant cost share
- the user explicitly cares about final payable total

### Rule
If shipping changes the user’s real out-of-pocket cost meaningfully, include it.

### Example
Wrong:
```text
Taobao: ¥88
JD: ¥92

Conclusion: Taobao is cheaper.
```

Correct:
```text
Taobao: ¥88 + ¥12 shipping = ¥100 final payable
JD: ¥92 with free shipping
Conclusion: JD has the lower final payable price.
```

---

## Coupon Handling Rules

Coupons are common and must be normalized carefully.

### Universal coupon
A coupon clearly visible and available to all buyers under normal purchase flow.

This may be included in final payable price if activation is straightforward and confidence is high.

### Restricted coupon
A coupon requiring:
- first-order status
- membership
- category eligibility
- specific channel entry
- time window
- minimum-spend threshold

This is conditional.

### Unclear coupon
If the Agent cannot determine whether:
- the coupon is available
- it stacks with the displayed price
- the threshold is satisfied

then the result is uncertain.

### Rule
Do not silently convert coupon possibility into hard final payable price.

---

## Membership-price Rules

### Member-only pricing
If a price requires store or platform membership, it is conditional unless the user explicitly accepts membership-based pricing.

### Friction assessment
Membership conditions vary:
- one-click free join
- recurring paid membership
- tiered platform membership
- hidden or unclear membership path

### Rule
The Agent should state:
- that the price is member-only
- whether the membership appears free or paid if known
- whether the result should be treated as main comparison result or conditional reference

---

## Group-buy and Multi-person Price Rules

### Group-buy price
A price requiring another participant or team purchase is a separate price basis.

### Solo-buyer price
The ordinary price a solo buyer can pay immediately.

### Rule
Unless the user explicitly allows group-buy conditions, default comparison should use solo-buyer price.

---

## Livestream and Flash-sale Price Rules

### Livestream price
Treat livestream-linked pricing as conditional unless clearly persistent and broadly accessible.

### Flash-sale price
Treat limited-time flash-sale price as conditional unless the user is explicitly shopping within that window.

### Rule
The Agent must state:
- the timing or access condition if known
- whether the price appears stable or event-based
- whether the result should be treated as a main result or conditional opportunity

Stable payable prices generally outrank event-dependent prices unless the user explicitly prioritizes temporary lowest deals.

---

## “From” Price and Variant Entry Price

Some listings show a “from” price that applies only to the cheapest variant.

### Rule
If the displayed price belongs to a different variant than the normalized target product, it must not be used for same-product comparison.

The Agent should identify whether the displayed number corresponds to:
- the exact target variant
- a different variant inside the same listing
- an unknown variant

If unknown, price confidence must drop.

---

## Installment-price Display

Some listings emphasize:
- monthly payment amount
- installment breakdown
- “as low as ¥XX/month”

### Rule
Installment display is not the same as purchase price.
Compare total payable amount, not monthly teaser numbers.

---

## Crossed-out Price and Anchoring

Crossed-out or reference prices are often marketing anchors.

### Rule
Crossed-out prices are not usable comparison targets.
They may help interpret discount framing, but not actual payable cost.

---

## Subsidy and Regional-price Rules

Subsidized prices may depend on:
- region
- account status
- government or trade-in eligibility
- restricted entry path

### Rule
A subsidy price is conditional if eligibility is limited or uncertain.

---

## Payment-method-specific Discounts

Some prices depend on:
- specific bank card
- installment plan
- wallet payment
- finance-product participation
- trade-in participation

### Rule
These are conditional payable prices and must be labeled with the activation requirement.

---

## Basket-dependent Discounts

Some discounts require:
- minimum spend
- buying multiple items
- adding other categories
- store-wide threshold

### Rule
If the user is buying only the target product and the threshold is not already satisfied, do not assume the discount applies.

---

## Unit-price vs Total-price Comparison

Sometimes the same product cannot be found in the same pack count or quantity.

### Same-product comparison
Use total payable price only when quantity and pack count match.

### Unit-price comparison
If package size differs, the Agent may provide:
- price per unit
- price per ml
- price per gram

### Rule
Unit-price comparison is useful reference, but not the same as strict same-product price comparison.

---

## Default Output Labels

For each candidate, the Agent should be ready to label:

- list price
- final payable price
- shipping included? yes or no
- conditional? yes or no
- conditions
- price confidence: high / medium / low

### Example normalized output
```json
{
  "platform": "JD",
  "list_price": "6999",
  "final_payable_price": "6599",
  "shipping_included": true,
  "is_conditional": false,
  "conditions": [],
  "price_confidence": "high"
}
```

---

## When Strict Cheapest Conclusions Are Allowed

A strict lowest-price conclusion should only be made when:

1. the listing is a high-confidence same-product match
2. the final payable price is known or clearly estimable
3. major conditions are explicit
4. shipping has been handled appropriately
5. the result does not violate user exclusions

### Rule
If any of the above is missing, the conclusion must be softened.

Acceptable softened wording:
- lowest visible conditional price
- likely lowest payable price under stated conditions
- reference-only lower price
- no strict cheapest conclusion due to price uncertainty

---

## Price-confidence Levels

### High
- payable amount is clear
- shipping treatment is clear
- conditions are absent or explicit and simple

### Medium
- payable amount is likely but one meaningful condition exists
- shipping is estimated but not fully confirmed
- coupon path appears valid but not fully verified

### Low
- deposit or pre-sale ambiguity
- variant-based “from” price uncertainty
- unclear coupon stacking
- unknown shipping
- unclear subsidy or membership eligibility

### Rule
Low price confidence cannot support a hard strict lowest-price conclusion.

---

## Cheapest vs Best Value vs Safest Purchase

Price normalization should feed three different decision outputs.

### Lowest Price Option
The lowest final payable price among valid same-product candidates.

### Best Value Option
The strongest balance of price, trust, shipping, and condition clarity.

### Safest Purchase Option
The most trustworthy, least ambiguous purchase path, even if not the cheapest.

### Rule
Do not allow a fragile conditional price to dominate all three recommendation types.

---

## Common Failure Patterns

### Failure 1
Using deposit amount as final payable price.

### Failure 2
Using “from” price for the wrong variant.

### Failure 3
Ignoring shipping and comparing visible product prices only.

### Failure 4
Treating member price or livestream price as universal.

### Failure 5
Assuming a coupon applies without checking threshold or eligibility.

### Failure 6
Comparing group-buy price to solo-buyer prices.

### Failure 7
Using installment teaser amount as actual payable cost.

### Failure 8
Forcing a hard cheapest claim when price basis remains uncertain.

---

## Practical Pricing Checklist

Before final comparison, the Agent should ask internally:

- What is the final payable amount for this listing?
- Is the displayed number unconditional or conditional?
- Does the price belong to the exact target variant?
- Is shipping included or separate?
- Are coupon thresholds already satisfied?
- Is membership required?
- Is livestream or group-buy access required?
- Is the result stable or event-based?
- Is price confidence high enough for strict lowest-price comparison?

If any important answer is uncertain, downgrade the price conclusion.

## Final Instruction

The Agent must not ask:

**What is the lowest number I can find on the page?**

The Agent must ask:

**What would the user actually need to pay, under what conditions, and how certain is that number?**
