# Decision Framework — Turning Comparison Results into Purchase Recommendations

## Core Objective

The goal of this framework is to turn comparison work into decision-ready purchase advice.

The Agent must not stop at:
- listing prices
- raw candidate lists
- the smallest visible number

The Agent must answer the user’s real purchase question:

- Which option is the lowest valid same-product price?
- Which option is the best value overall?
- Which option is the safest purchase path?
- What trade-offs matter before deciding?

A good comparison answer is not just numerically correct.  
It must be decision-useful.

---

## Core Recommendation Types

Unless the user explicitly requests otherwise, the Agent should produce three recommendation types.

### 1. Lowest Price Option
The lowest final payable price among high-confidence, eligible same-product listings.

This is a price-led recommendation.

### 2. Best Value Option
The option that best balances:
- final payable price
- store trust
- clarity of conditions
- delivery reliability
- after-sales confidence

This is the default recommendation type when the user gives no strong purchase priority.

### 3. Safest Purchase Option
The most reliable purchase path, usually characterized by:
- official or self-operated channel
- clear price basis
- low uncertainty
- stable after-sales support
- low fulfillment risk

This is a risk-led recommendation.

---

## Recommendation Preconditions

The Agent should only recommend an option strongly when the following are true:

1. product identity is sufficiently confirmed
2. price basis is sufficiently normalized
3. user constraints have been applied
4. major purchase risks are visible and explainable

If any of these fail, the recommendation must weaken accordingly.

---

## Decision Priority Order

Unless the user explicitly changes the priority, the Agent should reason in this order:

1. eligibility under user constraints
2. same-product confidence
3. price-basis clarity
4. risk level
5. final payable cost
6. delivery and after-sales practicality

This means:
- a cheaper listing that violates user constraints is not eligible
- a weak same-product match should not outrank a strong match
- a suspiciously low but unclear price should not dominate a clearer payable price
- when price difference is small, risk and channel quality matter more

---

## Step-by-step Decision Flow

### Step 1: Remove ineligible candidates
Exclude listings that violate explicit user constraints.

### Step 2: Separate by comparability
Divide remaining candidates into:
- high-confidence same-product listings
- medium-confidence likely same-product listings
- near-equivalent alternatives
- not comparable listings

Strict lowest-price recommendations should come only from the first group.

### Step 3: Normalize decision basis
For each valid candidate, ensure the Agent knows:
- final payable price
- shipping treatment
- conditions
- store or channel type
- main risk notes

### Step 4: Rank candidates by recommendation type
Use different logic for:
- lowest price option
- best value option
- safest purchase option

### Step 5: Explain trade-offs
State why the recommendation was chosen and what the user gives up or gains.

---

## Lowest Price Logic

### Definition
The lowest price option is the valid same-product listing with the lowest real payable cost among eligible candidates.

### Required conditions
A listing should normally qualify only if:
- same-product confidence is high
- final payable price is known or highly reliable
- shipping is included when material
- major price conditions are explicit
- user exclusions are not violated

### Do not use as default lowest-price basis
- deposit-only display
- pre-sale teaser price
- “from” price for a different variant
- group-buy price when the user is buying solo
- member-only price without disclosure
- livestream-only price without disclosure
- low-confidence listing identity

### Rule
A listing can be the lowest visible price without being the correct lowest price option.

---

## Best Value Logic

### Definition
The best value option is the listing with the strongest overall trade-off between cost and reliability.

### Best value should usually weigh:
- price level
- same-product confidence
- price clarity
- store trust
- delivery reliability
- after-sales support
- package usefulness if relevant

### Rule
When the price gap is small, best value should usually lean toward the more reliable purchase path.

---

## Safest Purchase Logic

### Definition
The safest purchase option is the listing with the lowest practical purchase risk, even if it is not the cheapest.

### Common safety signals
- official flagship store
- self-operated channel
- authorized seller
- clear final payable price
- non-conditional purchase path
- reliable delivery
- predictable return and after-sales path

### Rule
Safest purchase is especially important for:
- high-ticket items
- electronics
- authenticity-sensitive categories
- products where version confusion or after-sales risk matters

---

## User Preference Overrides

If the user explicitly states a purchase priority, the Agent must reorder recommendations accordingly.

### 1. Lowest-price-first user
Behavior:
- maximize cost advantage among eligible same-product results
- still disclose conditions and risks
- do not hide uncertainty

### 2. Official-store-first user
Behavior:
- exclude non-official sellers from main ranking
- compare only official, self-operated, or clearly authorized channels

### 3. Fast-delivery-first user
Behavior:
- prioritize in-stock, stable, trackable fulfillment
- downgrade pre-sale and weak-delivery listings

### 4. Best-after-sales or safest-path user
Behavior:
- strongly favor official or highly trusted channels
- de-emphasize fragile discounts and ambiguous listings

### 5. Budget-constrained user
Behavior:
- exclude over-budget candidates from main recommendations
- explicitly state if no exact same-product candidate fits the budget

---

## Constraint-first Decision Policy

The Agent must treat explicit user constraints as binding.

### Examples of binding constraints
- official store only
- no pre-sale
- no group-buy
- no membership-only pricing
- no imported version
- no used or refurbished
- must be in stock
- within budget

### Rule
A candidate that violates a binding constraint is not eligible for the main recommendation set, regardless of price.

---

## Small-gap vs Large-gap Logic

### Small Price Gap
When the price gap is small, the Agent should weigh:
- store trust
- after-sales quality
- delivery certainty
- price clarity

more heavily.

### Large Price Gap
When the price gap is large, the Agent should first suspect:
- spec mismatch
- version mismatch
- package-content mismatch
- condition mismatch
- subsidy, event, or membership conditions
- authenticity or seller-quality issues

### Rule
A large price gap is not automatic proof of a better deal.  
It is often a reason to inspect comparison validity more aggressively.

---

## Ties and Near-ties

When two listings are effectively tied in price, break ties using:

1. clearer price basis
2. stronger same-product confidence
3. stronger seller trust
4. better delivery reliability
5. stronger after-sales path

### Rule
In near-tie situations, the more trustworthy path should usually win.

---

## When No Strict Recommendation Is Possible

The Agent should not force certainty when the evidence is weak.

### Cases where strong recommendation should weaken
- no high-confidence same-product matches
- final payable price remains uncertain
- all low-price options depend on unclear conditions
- major spec or version ambiguity remains
- user constraints eliminate all clear candidates

### Acceptable weaker outputs
- no strict lowest-price conclusion
- lowest visible conditional price
- most likely best option under current evidence
- two plausible branches depending on version or package
- reference-only alternatives

### Rule
A weaker but honest recommendation is better than a false strong one.

---

## Branch-based Recommendations

When product identity remains branched after normalization, the Agent should preserve the branches through the final decision.

### Rule
Do not collapse branched product identities into one final recommendation if the branch materially changes the answer.

---

## Lowest Price vs Best Value vs Safest Purchase

These three recommendations often differ.  
That is normal and should be made explicit.

### Correct format
```text
Lowest price option: Platform X
Best value option: Platform Y
Safest purchase option: Platform Z
```

### Rule
Do not force one option to represent all three unless it genuinely does.

---

## Recommendation Explanation Template

The Agent should be ready to explain recommendations in a consistent pattern.

### Recommended structure
1. what the target product is
2. which listing is the lowest eligible price
3. which listing is the best value
4. which listing is the safest purchase path
5. what major conditions or risks matter
6. what trade-off the user is making

---

## Recommendation Strength Levels

### Strong Recommendation
Use when:
- same-product confidence is high
- price basis is clear
- risks are low or explicit
- user constraints are satisfied

### Moderate Recommendation
Use when:
- comparison is mostly clear
- one or two conditions remain
- the recommendation is still likely useful

### Weak Recommendation
Use when:
- product identity is only medium confidence
- price is conditional or uncertain
- user constraints sharply limit options
- trade-offs are substantial

### Rule
Recommendation wording should match evidence strength.

---

## Suggested Wording by Strength

### Strong
- This is the lowest valid price among high-confidence same-product listings.
- This is the strongest best value option.
- This is the safest purchase path.

### Moderate
- This appears to be the best value under the current evidence.
- This is likely the lowest payable option, assuming the listed condition applies.

### Weak
- No strict lowest-price conclusion is possible.
- This is a conditional lower-price opportunity rather than a confirmed lowest-price result.
- The answer depends on which version or package the user intends.

---

## Escalation from Numeric Comparison to Purchase Advice

The Agent must move beyond arithmetic when necessary.

### Numeric comparison alone is insufficient when:
- authenticity risk is meaningful
- after-sales support matters
- channel trust varies
- price conditions are hidden
- delivery uncertainty is high
- the item is expensive or technically complex

### Rule
The more expensive, complex, or risk-sensitive the product, the more the Agent should emphasize safest-purchase reasoning.

---

## Use of Near-equivalent Alternatives

Near-equivalent products should not replace same-product recommendations, but they can still be useful.

### Appropriate uses
- no high-confidence same-product match exists under budget
- the user is flexible and value-seeking
- the exact target is unavailable
- the user’s real goal is functional rather than model-specific

### Rule
Near-equivalent alternatives must be labeled as alternatives, not as same-product recommendations.

---

## Common Failure Patterns

### Failure 1
Recommending the cheapest visible listing without checking eligibility or risk.

### Failure 2
Ignoring user constraints in final ranking.

### Failure 3
Allowing low-confidence same-product matches to drive hard conclusions.

### Failure 4
Treating best value as automatically identical to cheapest.

### Failure 5
Failing to explain trade-offs between price and reliability.

### Failure 6
Collapsing branch-dependent answers into one false universal recommendation.

### Failure 7
Not distinguishing conditional price opportunities from standard purchase paths.

### Failure 8
Forcing a safest-purchase recommendation from a weak or unclear channel.

---

## Practical Decision Checklist

Before finalizing a recommendation, the Agent should ask internally:

- Does the candidate satisfy the user’s stated constraints?
- Is same-product confidence high enough?
- Is final payable price clear enough?
- Are shipping and conditions properly handled?
- Is store or channel trust acceptable?
- Is the recommendation type correct:
  - lowest price option
  - best value option
  - safest purchase option
- If the price gap is small, have I over-weighted a fragile discount?
- If the price gap is large, have I checked for mismatch or hidden conditions?
- Would a cautious buyer trust this recommendation?

If any answer is weak, soften the conclusion.

## Final Instruction

The Agent must not ask:

**Which listing has the lowest number?**

The Agent must ask:

**Which listing best answers the user’s actual buying goal, with fair comparison, clear conditions, and an honest trade-off explanation?**
