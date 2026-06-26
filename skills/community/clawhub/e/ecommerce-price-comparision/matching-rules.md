# Matching Rules — Determining Same-product Confidence Across Platforms

## Core Objective

The goal of matching is to determine whether listings found on different platforms refer to:

1. the **same product**
2. a **near-equivalent product**
3. a **not comparable product**

This skill must not confuse search relevance with same-product confidence.

A platform search engine can return a highly relevant result that is still:
- the wrong model
- the wrong version
- the wrong size
- the wrong quantity
- the wrong package content
- the wrong condition

A strict cross-platform price comparison is only valid when the Agent has enough evidence that the compared listings refer to the same product on the same identity basis.

---

## Matching Outcome Types

Every candidate listing should be classified into one of three matching outcomes.

### 1. Same Product
Use when the listing is highly likely to be the same product as the normalized target identity.

This is the only class that can support a strict lowest-price conclusion.

### 2. Near-equivalent
Use when the listing is highly similar in purpose or appearance, but not confirmed to be the same product.

This class may support alternative recommendations, but not strict same-product cheapest claims.

### 3. Not Comparable
Use when the listing differs in a way that breaks valid comparison.

This class must be excluded from strict lowest-price conclusions.

---

## Matching Priority Order

When evaluating a candidate listing, the Agent should check fields in the following order:

1. brand
2. model or exact series identity
3. version or variant
4. capacity, size, or quantity
5. bundle or package content
6. condition
7. color
8. seller or channel context
9. title similarity and descriptive wording

Do not start from title similarity.  
Do not let keyword overlap override model mismatch.  
Do not let visual similarity override spec mismatch.

---

## Strong-evidence Fields vs Weak-evidence Fields

The Agent must distinguish between evidence that strongly proves identity and evidence that merely supports it.

### Strong-evidence Fields
- brand
- model
- series
- version
- capacity, size, or quantity
- package content when material
- condition when materially different

### Medium-evidence Fields
- color
- seller wording
- marketing subtitle
- minor title differences
- platform category placement

### Weak-evidence Fields
- search ranking
- keyword overlap alone
- similar image style
- similar use case only

### Rule
If strong-evidence fields conflict, the listing cannot be treated as the same product even if weak-evidence fields align.

---

## Exact-match Requirements

A listing should normally qualify as **same product** only when all of the following are true:

- brand matches or is confidently normalized
- model matches
- version matches
- capacity, size, or quantity matches
- package content is equivalent or immaterial
- condition matches the user’s intended comparison target
- no disqualifying mismatch exists

---

## Immediate Disqualifiers

The following mismatches usually force a candidate out of same-product classification.

### 1. Model mismatch
Examples:
- iPhone 16 vs iPhone 16 Plus
- Dyson Supersonic vs Dyson Nural
- Air Purifier 4 vs Air Purifier 4 Pro

### 2. Capacity or size mismatch
Examples:
- 256GB vs 512GB
- 30ml vs 50ml
- 1L vs 2L

### 3. Quantity mismatch
Examples:
- 1-pack vs 2-pack
- one refill vs refill bundle

### 4. Version mismatch
Examples:
- Wi-Fi vs Cellular
- China version vs Global version
- Pro vs non-Pro
- 2024 edition vs 2025 edition

### 5. Condition mismatch
Examples:
- new vs used
- new vs refurbished
- domestic retail vs unofficial import

### Rule
These mismatches usually mean the candidate is **not comparable** for strict same-product lowest-price purposes.

---

## Conditional Disqualifiers

The following do not always force rejection, but they require explicit handling.

### 1. Color mismatch
Color may or may not matter depending on category and user request.

### 2. Package-content mismatch
Standard edition and gift box may share the same base item but still be different purchasable offers.

### 3. Seller or channel mismatch
A listing from an unknown third-party seller may still be the same product, but recommendation confidence may decrease.

### Rule
Conditional disqualifiers affect confidence, comparability, or recommendation ranking depending on context.

---

## Same-product Confidence Levels

### High Confidence
Use when:
- brand matches
- model matches
- version matches
- capacity, size, or quantity matches
- package content matches or is clearly equivalent
- no material mismatch remains

This level supports strict lowest-price conclusions.

### Medium Confidence
Use when:
- product family clearly matches
- most major fields align
- limited uncertainty remains in package content, color, or seller labeling

This level supports cautious comparison, but not an overconfident strict cheapest claim.

### Low Confidence
Use when:
- one or more major identity fields are unclear
- model or version may differ
- package content is uncertain
- title is broad or misleading

This level should not drive strict same-product conclusions.

---

## Same Product vs Near-equivalent

The Agent must not collapse these two categories into one.

### Same Product
Same identity, same usable comparison target.

### Near-equivalent
A very similar alternative, but not the same product identity.

### Rule
Near-equivalent results can help the user discover substitutes, but they do not count as strict same-product price evidence.

---

## Title-based Matching Rules

Title comparison can support retrieval, but it is not the final source of truth.

### Use title matching for:
- likely brand or model phrases
- version keywords
- pack-count clues
- package-content clues

### Do not use title alone when:
- model is not explicit
- capacity is missing
- the title is SEO-heavy
- the seller uses generic words such as “same style”, “flagship”, or “upgrade version”

### Rule
Structured attributes are stronger than title wording.

---

## Attribute-source Priority

When evidence sources disagree, trust them in the following order:

1. structured product attributes or spec table
2. explicit model/version field
3. package-content description
4. title
5. image cues
6. search ranking

### Example
If the title says `iPhone 16 256GB`, but the spec section says `512GB`, treat the listing as 512GB.

### Rule
When conflict exists, trust structured specs over marketing title.

---

## Color Matching Rules

### Same-product with color difference may still be acceptable when:
- the user did not specify color
- color does not materially affect price or identity
- the platform is surfacing a different default variation

### Color difference becomes material when:
- the user explicitly requested a color
- the category is fashion, footwear, cosmetics, or collectible
- limited-edition colors change value

### Rule
If color is user-specified, color mismatch should reduce or block same-product confidence.

---

## Package-content Matching Rules

The Agent should ask:

**Is the user buying the same total offer, or only the same base item?**

### Common package-content markers
- standard edition
- gift box
- starter set
- charger included or excluded
- accessories included
- service plan included
- refill plus full size

### Outcomes
- same base item, different offer → usually not strict same-product for final price comparison
- same base item, immaterial freebie difference → may remain same-product with note
- different functional package content → separate variants

### Rule
Do not silently compare a standard package to an enhanced package.

---

## Quantity and Pack-count Matching Rules

Pack-count normalization is mandatory.

### Examples
- tissues 10-pack vs 20-pack
- shampoo single bottle vs 2-bottle set
- toothbrush heads pack of 4 vs pack of 8

### Rule
Total displayed price is not enough. Quantity must be normalized first.

If the same pack count cannot be found, the Agent may provide unit-price reference, but it must clearly state that this is **not** a strict same-product comparison.

---

## Version Matching Rules

### Common version markers
- Pro / Max / Plus / Ultra / Lite / SE
- Wi-Fi / Cellular
- CN / Global / International
- 2024 version / 2025 version
- standard / premium / youth edition

### Rule
Version mismatch is usually a hard mismatch.
The Agent must not ignore version markers because the rest of the title looks similar.

---

## Condition Matching Rules

### Common conditions
- new
- used
- refurbished
- open-box
- imported
- unknown

### Default behavior
Unless the user explicitly asks otherwise, the default target should be **new retail condition**.

### Rule
A used or refurbished listing may be a useful alternative, but not the same comparison target as a new retail listing.

---

## Seller and Channel Effects on Matching

Seller type usually affects recommendation quality more than identity itself, but it can still affect practical matching confidence.

### Cases where seller/channel context matters
- unofficial import channels
- gray-market electronics
- suspiciously generic sellers
- listings with weak spec clarity and weak authenticity signals

### Rule
Seller/channel context should not override clear structured-spec alignment, but it may lower practical confidence when listing authenticity or version accuracy is questionable.

---

## Scoring Framework

The Agent may use an internal weighted logic like the following:

- brand: 20
- model or series: 25
- version or variant: 20
- capacity, size, or quantity: 20
- package content: 10
- condition: 5

### Interpretation
- 90–100: high-confidence same product
- 75–89: medium-confidence likely same product
- below 75: low-confidence or not comparable

### Important note
Hard mismatch rules override numeric scoring.

A candidate with the correct brand and model but wrong capacity should not remain same-product simply because the overall score still looks high.

---

## Matching Workflow

For each candidate listing, the Agent should follow this order:

1. confirm brand
2. confirm model or exact product family
3. confirm version or variant
4. confirm capacity, size, or quantity
5. confirm package content
6. confirm condition
7. check user-specified fields such as color
8. review seller or channel context
9. assign outcome:
   - same product
   - near-equivalent
   - not comparable
10. assign confidence:
   - high
   - medium
   - low

Only after this should price comparison proceed.

---

## Multi-candidate Selection Rules

A platform may return multiple candidate listings.  
The Agent must choose the most appropriate candidate, not simply the cheapest one.

### Preferred selection order
1. highest same-product confidence
2. clearest price basis
3. cleanest package equivalence
4. stronger seller trust
5. better delivery reliability
6. lower final payable price

### Rule
Cheapest among weak matches is worse than slightly higher price among strong matches.

---

## When to Keep Multiple Candidates from the Same Platform

The Agent may keep multiple candidates from one platform when:

- one is official and one is third-party
- one is standard edition and one is bundle edition
- one has unconditional price and one has conditional price
- same-product confidence differs materially
- the user’s constraints make more than one candidate decision-useful

### Rule
Multiple candidates are useful when they represent distinct purchase choices, not duplicated search noise.

---

## Downgrade Conditions

The Agent should downgrade confidence when:

- title and structured specs conflict
- quantity is unclear
- version markers are missing
- package content is vague
- seller trust is weak and specs are incomplete
- price is abnormally low relative to other high-confidence matches

### Rule
An abnormally low price is not proof of a good deal.  
It is often a reason to inspect matching quality more carefully.

---

## Platform Naming Noise

Different platforms may describe the same product differently.

### Common naming noise
- reordered attributes
- shortened model names
- marketing-heavy adjectives
- omitted color or version
- seller-added promotional keywords

### Rule
Naming noise alone should not break a likely good match if structured fields align.

---

## Unit-price Reference vs Same-product Price

Sometimes the Agent cannot find exactly the same package size or quantity, but can still provide useful unit-price reference.

### Correct use
The Agent may say:
- these are not the same package count, so no strict same-product cheapest conclusion is given
- on a per-unit basis, Platform X is cheaper

### Rule
Unit-price comparison is a fallback analysis, not a replacement for same-product comparison.

---

## Common Failure Patterns

### Failure 1
Using search ranking as proof of same-product identity.

### Failure 2
Letting title keyword overlap override model mismatch.

### Failure 3
Ignoring version markers such as Pro, Max, Lite, SE, Global, or 2025 edition.

### Failure 4
Treating bundle and standard edition as equivalent without disclosure.

### Failure 5
Collapsing same-product and near-equivalent into one category.

### Failure 6
Choosing the cheapest weak match instead of the strongest valid match.

### Failure 7
Ignoring pack count and comparing total prices directly.

### Failure 8
Using low-confidence matches to make a strict lowest-price claim.

---

## Practical Matching Checklist

Before labeling a candidate as same-product, the Agent should ask internally:

- Does the brand match?
- Does the exact model match?
- Does the version match?
- Do capacity, size, or quantity match?
- Is package content equivalent?
- Is the condition aligned with the user’s target?
- Are any user-specified fields violated?
- Is any hard mismatch present?
- Is confidence high enough for strict same-product comparison?

If any critical answer is “no”, the candidate should not drive a strict lowest-price conclusion.

## Final Instruction

A strong match is more valuable than a cheap weak match.

The Agent must not ask:

**Which result is cheapest?**

The Agent must ask:

**Which result is truly the same product, with enough confidence to compare prices fairly?**
