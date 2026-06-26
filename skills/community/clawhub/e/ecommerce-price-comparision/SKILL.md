---
name: Price Compare
slug: price-compare
version: 1.0.0
description: Compare products across JD, Taobao, Tmall, Pinduoduo, and Douyin Mall by normalizing product identity, standardizing price basis, detecting purchase risk, and producing decision-ready recommendations.
metadata: {"clawdbot":{"emoji":"🛍️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| Common comparison traps that cause false conclusions | `comparison-traps.md` |
| User-input parsing and product normalization | `parsing-and-normalization.md` |
| Same-product matching logic and confidence rules | `matching-rules.md` |
| Price-basis normalization and payable-price rules | `pricing-rules.md` |
| Recommendation logic and purchase decision rules | `decision-framework.md` |
| Worked execution patterns and example outputs | `examples.md` |

## Critical Comparison Traps

These mistakes create false comparison results and misleading recommendations. See `comparison-traps.md` for full patterns.

1. **Different specs treated as the same product** — Never compare across different model, version, capacity, size, quantity, or package content.
2. **Deposit or pre-sale display treated as final payable price** — A deposit is not the total amount the buyer will pay.
3. **Conditional price treated as universal price** — Livestream pricing, member pricing, group-buy pricing, first-order discounts, and subsidy prices must be labeled with conditions.
4. **Store trust ignored in favor of raw price** — Official flagship stores, self-operated channels, authorized sellers, and unknown third-party sellers are not equivalent purchase paths.
5. **Bundle edition compared directly to standard edition** — Listings with gifts, accessories, service plans, or expanded package contents must not be silently mixed with standard editions.

## Core Objective

This skill helps an Agent perform cross-platform product comparison across:

- JD
- Taobao
- Tmall
- Pinduoduo
- Douyin Mall

The purpose of this skill is not to find the smallest visible number on a page.

The purpose is to:

1. identify the correct target product
2. normalize listing identity across platforms
3. standardize price basis
4. detect conditions and risks
5. produce decision-ready recommendations the user can actually trust

A valid comparison requires both of the following:

1. the compared listings refer to the same product, or are explicitly labeled as near-equivalent
2. the compared prices refer to the same payable basis, or are explicitly marked as conditional or uncertain

## Core Rules

### When Parsing Requests
- Extract brand, category, model, series, version, capacity, size, quantity, color, and package content
- Separate **hard attributes** from **soft purchase preferences**
- Treat a product link as a stronger reference source than vague free-text input
- If the input is ambiguous, create candidate branches instead of forcing a false single identity

### When Normalizing Products
- Build a normalized product identity before cross-platform comparison
- Treat model, version, capacity, size, quantity, and package content as identity-defining fields
- Treat store preference, shipping preference, and “official stores only” as constraints rather than product identity
- If the listing identity cannot be normalized confidently, downgrade same-product confidence

### When Matching Listings
- Match by structured attributes, not by title similarity alone
- Model mismatch overrides keyword overlap
- Capacity, size, quantity, and version mismatch usually break strict comparability
- Package-content differences must be disclosed clearly
- Used, refurbished, imported, and unofficial variants must not be mixed into standard new-retail comparison unless the user explicitly allows them

### When Comparing Prices
- Prefer **final payable price** over list price
- Never treat deposit, teaser price, or “from” price as final payable price without confirmation
- Include shipping when it materially changes the user’s real out-of-pocket cost
- Mark uncertain prices as uncertain instead of forcing a hard numeric conclusion
- If the lowest visible price depends on coupon collection, membership, livestream access, group buying, or subsidy eligibility, state those conditions explicitly

### When Making Recommendations
- Always provide more than “the cheapest listing”
- Distinguish between:
  - **lowest price option**
  - **best value option**
  - **safest purchase option**
- If price differences are small, weigh store trust, after-sales support, and delivery reliability more heavily
- If price differences are unusually large, investigate mismatch or hidden conditions before recommending

## Execution Flow

The Agent should execute this skill in the following order:

1. **Parse the user request**
   - Determine whether the input is a product name, product link, mixed description, or vague shopping intent
   - Extract explicit requirements and exclusions

2. **Build a normalized product identity**
   - Standardize the target product into a structured internal identity
   - Identify missing critical fields
   - Create candidate branches when more than one plausible interpretation exists

3. **Search each supported platform**
   - Find the most relevant candidates on JD, Taobao, Tmall, Pinduoduo, and Douyin Mall
   - Keep high-quality candidates for downstream evaluation

4. **Evaluate same-product confidence**
   - Classify each candidate as:
     - same product
     - near-equivalent
     - not comparable
   - Exclude non-comparable listings from strict lowest-price conclusions

5. **Normalize price basis**
   - Extract list price, final payable price, shipping, and price conditions
   - Label each result as unconditional, conditional, reference-only, or uncertain

6. **Assess purchase risk**
   - Evaluate store/channel type, authenticity signals, package complexity, pre-sale status, and unusual discount conditions
   - Flag abnormally low prices for further scrutiny

7. **Produce decision-ready output**
   - Summarize the normalized target product
   - Present platform-by-platform comparison
   - Recommend:
     - lowest price option
     - best value option
     - safest purchase option
   - Explain risks, conditions, and uncertainty clearly

## Decision Priorities

Unless the user states otherwise, use the following priority order:

1. correct product identity
2. correct price basis
3. constraint compliance
4. clear risk disclosure
5. decision usefulness

This means:

- a slightly higher but clearly matched and trustworthy listing is better than a suspiciously low but weakly matched listing
- a conditional price is not stronger evidence than an unconditional price
- uncertainty must remain uncertainty

## Confidence Levels

This skill should reason with three practical confidence levels.

### High Confidence
Use when:
- brand matches
- model matches
- version matches
- core specs match
- package content matches or is clearly equivalent
- price basis is clear

### Medium Confidence
Use when:
- the product family is clear
- most major fields align
- a limited uncertainty remains in package, color, or seller labeling
- the listing is likely comparable but not fully confirmed

### Low Confidence
Use when:
- one or more major fields are unresolved
- the model or version may differ
- package content is unclear
- price basis is opaque

Only **high-confidence same-product matches** should drive a strict lowest-price conclusion.

## Default Output Expectations

A proper final comparison should include:

1. **normalized target product**
2. **platform comparison results**
3. **lowest price option**
4. **best value option**
5. **safest purchase option**
6. **risk notes, price conditions, and uncertainty disclosures**

The Agent should not return raw search results without interpretation.

## Default Recommendation Logic

If the user gives no explicit purchase priority:

- choose **lowest price option** from high-confidence, eligible same-product listings
- choose **best value option** by balancing price, trust, shipping, and condition clarity
- choose **safest purchase option** from the most reliable channel with the clearest after-sales path

If the user gives a purchase priority, reorder accordingly:

- **lowest price first** → prioritize payable cost, but still disclose risk
- **official / authorized only** → exclude unknown third-party sellers from main conclusions
- **fast delivery first** → prioritize in-stock, stable fulfillment
- **no pre-sale / no group-buy / no membership conditions** → remove conditional listings from primary recommendations

## Hard Constraints

The Agent must not:

- compare different model/spec variants as the same product
- treat deposit or teaser price as final payable price
- treat group-buy or multi-person price as solo-buyer price
- treat livestream-only or member-only discounts as universal price without disclosure
- ignore shipping when it materially changes total cost
- ignore store/channel trust in recommendation logic
- give a strict cheapest conclusion when same-product confidence or price confidence is low
- mix used, refurbished, imported, or unofficial variants into standard new-product comparison unless explicitly requested

## Fallback Behavior

### If no high-confidence same-product match is found
State that no high-confidence same-product listing was found on that platform. Provide reference-only results if they are still decision-useful.

### If the user input is too vague
Create the most likely candidate branches and compare them separately.

### If price conditions cannot be verified
Label the result as conditional or uncertain instead of forcing a lowest-price conclusion.

### If the product is highly non-standard
Explain that strict same-product comparison may not be reliable for custom products, variable bundles, second-hand goods, or service-heavy offers.

## Scope

This skill helps with:

- cross-platform product comparison across JD, Taobao, Tmall, Pinduoduo, and Douyin Mall
- product identity normalization from names, links, and mixed user descriptions
- same-product matching and confidence scoring
- price-basis normalization, including conditional-price handling
- risk-aware purchase recommendations
- decision support for lowest price, best value, and safest purchase

This skill does NOT:

- place orders, make payments, or interact with live user accounts
- guarantee real-time inventory, coupon availability, or livestream access
- authenticate sellers or verify legal compliance beyond observable listing signals
- treat uncertain listings as definitive same-product matches
- make autonomous purchase decisions on the user’s behalf

## Final Instruction

When using this skill, the Agent must remember:

**The goal is not to find the smallest number.  
The goal is to compare the right product, on the right price basis, with the right risk disclosure, and give the user a recommendation they can actually trust.**
