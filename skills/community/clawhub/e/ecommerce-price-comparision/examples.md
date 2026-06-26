# Examples — Worked Comparison Patterns for Agent Execution

## How to Use These Examples

These examples are execution patterns showing how the Agent should:

1. parse the user request
2. normalize product identity
3. determine same-product confidence
4. normalize price basis
5. produce decision-ready recommendations

For each example, focus on:
- which fields define product identity
- which fields are purchase constraints
- whether strict same-product comparison is possible
- whether price conditions are stable or conditional
- how to explain trade-offs honestly

---

## Example 1 — Precise Product Name, Standard Comparison

### User Input
```text
Compare iPhone 16 256GB Black across JD, Taobao, Tmall, Pinduoduo, and Douyin Mall.
```

### Parsing Result
- category: smartphone
- brand: Apple
- model: iPhone 16
- capacity: 256GB
- color: Black
- condition: new
- constraints: none

### Correct Reasoning Pattern
- use the user’s input as the normalized target product
- search all five platforms for same-product candidates
- exclude mismatched capacities, versions, and conditions
- normalize final payable price
- separate lowest price option from safest purchase option if needed

### Example Output
```text
Target product:
Apple iPhone 16 256GB Black, new retail version

Comparison summary:
- JD: ¥6599, self-operated, clear final payable price
- Tmall: ¥6699, official flagship store
- Taobao: ¥6529, third-party seller
- Pinduoduo: ¥6499, lower price but weaker channel trust
- Douyin Mall: ¥6459, appears lower but depends on livestream pricing

Recommendation:
- Lowest price option: Pinduoduo at ¥6499
- Best value option: JD at ¥6599
- Safest purchase option: Tmall official flagship store at ¥6699

Risk notes:
- Douyin price appears conditional on livestream promotion
- Taobao and Pinduoduo are cheaper, but official-channel certainty is lower
```

---

## Example 2 — Link-based Comparison

### User Input
```text
Here is the JD link. Find the same product on Taobao, Tmall, Pinduoduo, and Douyin Mall.
```

### Parsing Result
- input type: link-based
- reference platform: JD
- target identity: extracted from linked listing

### Correct Reasoning Pattern
- parse the linked JD listing first
- use the linked listing as the identity anchor
- search other platforms relative to that normalized target
- reject visually similar but non-equivalent listings

### Example Output
```text
Reference product identified from the JD listing:
Xiaomi Air Purifier 4 Pro, standard package, new retail version

Cross-platform search:
- Tmall: high-confidence same product found
- Taobao: one likely same-product candidate, one bundle edition excluded
- Pinduoduo: one medium-confidence candidate, weaker seller trust
- Douyin Mall: no high-confidence same-product candidate found

Recommendation:
- Lowest valid price: Taobao candidate, if package equivalence holds
- Best value: JD reference listing
- Safest purchase option: JD or Tmall official channel

Note:
No strict same-product conclusion is given for Douyin Mall because no high-confidence match was found.
```

---

## Example 3 — Official-store-only Constraint

### User Input
```text
Compare Dyson Supersonic pink, official stores only.
```

### Parsing Result
- brand: Dyson
- model family: Supersonic
- color: pink
- binding constraint: official stores only
- ambiguity: medium because package type may still differ

### Correct Reasoning Pattern
- compare only official, self-operated, or clearly authorized channels for main recommendations
- exclude cheaper third-party sellers from main ranking
- preserve ambiguity if standard edition vs gift set remains unresolved

### Example Output
```text
Target product:
Dyson Supersonic pink, official-channel purchase only

Eligible channels:
- JD official/self-operated candidate
- Tmall official flagship candidate
- Douyin official store candidate

Excluded from main ranking:
- Taobao third-party listings
- Pinduoduo non-official listings

Recommendation:
- Lowest official-channel price: Douyin official store, if the displayed promotion is active
- Best value option: JD official channel
- Safest purchase option: Tmall official flagship store
```

---

## Example 4 — No Pre-sale, No Group-buy

### User Input
```text
Find the cheapest same product, but no pre-sale and no group-buy.
```

### Parsing Result
- identity: from context
- excluded conditions:
  - no pre-sale
  - no group-buy
- priority goal: lowest price among eligible listings

### Correct Reasoning Pattern
- remove all pre-sale listings
- remove group-buy-only pricing from default ranking
- compare only standard solo-purchase final payable prices

### Example Output
```text
Visible lowest number:
Pinduoduo group-buy price at ¥89

Eligible comparison basis after exclusions:
- JD: ¥109 solo purchase
- Taobao: ¥105 normal purchase
- Tmall: ¥112 normal purchase
- Pinduoduo: ¥109 solo purchase
- Douyin Mall: pre-sale display excluded

Recommendation:
- Lowest eligible standard-purchase price: Taobao at ¥105
- Best value option: JD at ¥109 if seller trust and delivery reliability are stronger
- Safest purchase option: Tmall official store

Reasoning:
The lower group-buy and pre-sale numbers are excluded by the user’s binding conditions.
```

---

## Example 5 — Ambiguous Product Family, Branching Required

### User Input
```text
Compare Dyson hair dryers.
```

### Parsing Result
- brand: Dyson
- category: hair dryer
- ambiguity: high
- possible branches:
  - Dyson Supersonic standard edition
  - Dyson Supersonic gift set
  - Dyson Nural standard edition

### Correct Reasoning Pattern
- do not pretend that “Dyson hair dryers” refers to one exact purchasable product
- create candidate branches
- provide branch-dependent comparison results

### Example Output
```text
Your request is still broad, so I am treating it as multiple possible target products rather than one fixed product.

Possible branches:
1. Dyson Supersonic standard edition
2. Dyson Supersonic gift set
3. Dyson Nural standard edition

Branch-based result:
- If you mean Dyson Supersonic standard edition, JD currently appears strongest on best value
- If you mean Dyson Supersonic gift set, Tmall official channel appears safer
- If you mean Dyson Nural, no strict same-product cheapest conclusion is possible yet

Reasoning:
“Dyson hair dryers” is a product family, not a single normalized product identity.
```

---

## Example 6 — Different Pack Counts, Unit-price Only

### User Input
```text
Compare this shampoo across platforms.
```

### Context
Search results reveal:
- JD: 500ml × 2
- Taobao: 500ml × 1
- Tmall: 1L refill pack
- Pinduoduo: 500ml × 2
- Douyin Mall: 500ml × 1

### Correct Reasoning Pattern
- separate same-pack and different-pack candidates
- do not compare total prices across different quantities directly
- use unit-price only as fallback reference

### Example Output
```text
Strict same-product comparison is limited because package counts differ across platforms.

Pack-normalized result:
- JD: 500ml × 2
- Pinduoduo: 500ml × 2
- Taobao: 500ml × 1
- Douyin Mall: 500ml × 1
- Tmall: 1L refill pack

Strict same-pack lowest price:
- Among 500ml × 2 listings, Pinduoduo is lower
- Among 500ml × 1 listings, Taobao is lower

Unit-price reference:
- On a per-ml basis, Tmall refill pack appears cheaper

Reasoning:
Because quantity differs, no universal same-product cheapest conclusion is given across all listings.
```

---

## Example 7 — Lowest Visible Number Is a Deposit

### User Input
```text
Which platform is cheapest for this product?
```

### Context
Visible prices:
- JD: ¥699
- Tmall: ¥679
- Pinduoduo: ¥649
- Douyin Mall: ¥99 deposit
- Taobao: ¥659

### Correct Reasoning Pattern
- exclude deposit-only display from standard comparison
- compare normal final payable prices among eligible candidates
- mention the deposit result only as conditional or incomplete

### Example Output
```text
Lowest visible number:
Douyin Mall at ¥99, but that amount is a deposit rather than the final payable price

Lowest valid price option:
Pinduoduo at ¥649 among normal non-deposit listings

Best value option:
Taobao at ¥659 if same-product confidence and seller trust are acceptable

Safest purchase option:
JD or Tmall, depending on channel type and after-sales preference

Reasoning:
The Douyin number cannot be used as the standard price basis because the final payable amount is not confirmed.
```

---

## Example 8 — Livestream-only Price vs Stable Store Price

### User Input
```text
Compare the actual price I can buy it for today.
```

### Context
- Douyin Mall: ¥459 during livestream only
- JD: ¥489 stable payable price
- Tmall: ¥495 stable payable price

### Correct Reasoning Pattern
- treat the Douyin price as conditional unless livestream access is realistically available
- recommend the stable payable path when the user asks for an actionable price today

### Example Output
```text
Today’s pricing picture:
- Douyin Mall: ¥459, but it depends on livestream access and event timing
- JD: ¥489, stable final payable price
- Tmall: ¥495, stable final payable price

Recommendation:
- Lowest visible conditional price: Douyin Mall at ¥459
- Best actionable price today: JD at ¥489
- Safest purchase option: Tmall official channel if official support matters more

Reasoning:
The Douyin number is lower, but it is event-based rather than a stable standard purchase path.
```

---

## Example 9 — Delivery Speed Matters More Than Small Price Savings

### User Input
```text
Help me compare this tablet, but I need it fast.
```

### Parsing Result
- target product comes from context or link
- priority goal: fast delivery

### Correct Reasoning Pattern
- downgrade pre-sale or weak-delivery listings
- prioritize in-stock, stable, trackable fulfillment
- allow slightly higher price to win if delivery is meaningfully better

### Example Output
```text
For a speed-priority purchase, I am weighting delivery reliability more heavily than small price differences.

Eligible same-product options:
- JD: in stock, next-day delivery
- Tmall: in stock, estimated 2-day delivery
- Pinduoduo: lower price, but delivery reliability is weaker
- Douyin Mall: pre-sale, excluded from speed-priority main recommendation

Recommendation:
- Lowest price option: Pinduoduo
- Best value option under speed priority: JD
- Safest purchase option: JD or Tmall depending on channel trust

Reasoning:
Because you need it soon, the slightly cheaper but less predictable option is not the strongest fit.
```

---

## Example 10 — Official vs Third-party Trade-off

### User Input
```text
Is the cheaper Taobao option worth it compared with the official Tmall store?
```

### Correct Reasoning Pattern
- first confirm same-product equivalence
- then assess whether the price gap is small or large
- if the gap is small, official channel usually wins on best value or safest purchase
- if the gap is large, inspect mismatch or hidden conditions first

### Example Output
```text
If the Taobao listing is a true same-product match, the decision depends on the size of the price gap.

Current trade-off:
- Taobao: lower price, but third-party seller and weaker after-sales certainty
- Tmall official store: slightly higher price, clearer purchase path

Recommendation:
- If the price difference is small, the official Tmall store is usually the stronger best value and safest purchase option
- If the price difference is unusually large, inspect version, package content, and price conditions before deciding

Reasoning:
A lower price from a weaker channel is attractive only if the same-product match is solid and the savings are meaningful enough to justify the extra risk.
```

---

## Example 11 — No High-confidence Same-product Match

### User Input
```text
Find the cheapest same product on all platforms.
```

### Context
Search results are messy:
- several listings have similar names
- model numbers are missing
- package content is inconsistent
- some prices are much lower but version is unclear

### Correct Reasoning Pattern
- do not force a hard same-product cheapest conclusion
- distinguish high-confidence, medium-confidence, and reference-only results
- explicitly state that strict same-product comparison is not yet possible

### Example Output
```text
I found multiple likely candidates, but I do not have enough high-confidence same-product matches across all platforms to make a strict lowest-price conclusion.

What I can say:
- JD and Tmall each show one likely standard-version candidate
- Taobao and Pinduoduo show lower prices, but version or package content is unclear
- Douyin Mall results appear promotion-heavy and not reliably comparable

Decision:
- No strict lowest-price conclusion is given
- Best provisional value option: JD, because listing clarity is stronger
- Reference-only lower-price possibilities exist on Taobao and Pinduoduo, but they remain unconfirmed

Reasoning:
The costliest mistake here would be comparing the wrong variants with false confidence.
```

---

## Example 12 — Budget Constraint with Near-equivalent Alternatives

### User Input
```text
I want this exact product if possible, but my budget is under ¥500.
```

### Correct Reasoning Pattern
- first search for exact same-product candidates under budget
- if none exist, say so explicitly
- then optionally provide near-equivalent alternatives, clearly labeled as alternatives

### Example Output
```text
For the exact target product, I did not find a high-confidence same-product listing under your ¥500 budget.

Exact-match result:
- No eligible exact same-product candidate under budget

Alternative options:
- Platform A offers a lower-capacity version under budget
- Platform B offers a similar model from the same brand under budget

Recommendation:
- No exact same-product recommendation under budget
- If you must stay below ¥500, the best fallback is a near-equivalent alternative rather than a forced exact-match conclusion

Reasoning:
Budget is binding, but near-equivalent alternatives must remain clearly labeled as alternatives rather than exact same-product matches.
```

---

## Example 13 — User Wants Only the Lowest Price, But Risk Still Matters

### User Input
```text
I only care about the cheapest price.
```

### Correct Reasoning Pattern
- optimize for lowest eligible same-product final payable price
- still disclose whether the result is conditional, non-official, pre-sale, or uncertain

### Example Output
```text
If your only priority is the lowest price, the current answer is:

- Lowest valid same-product price option: Platform X at ¥299
- Lower visible conditional price: Platform Y at ¥279, but it requires a member-only coupon and unclear shipping terms

Recommendation:
Platform X is the lowest clean purchase path.
Platform Y is only a lower conditional opportunity, not the strongest default answer.

Reasoning:
Even for a price-first user, a fragile or unverified low price is not a good final comparison answer.
```

---

## Example 14 — Imported, Used, and Refurbished Excluded

### User Input
```text
Compare the cheapest new domestic version only. No refurbished, no imports.
```

### Correct Reasoning Pattern
- remove imported, refurbished, and used candidates
- compare only new domestic retail candidates
- mention excluded lower-price listings only as excluded reference if useful

### Example Output
```text
Eligible comparison scope:
New domestic retail version only

Excluded from main ranking:
- refurbished listing on Taobao
- imported version on Pinduoduo
- open-box listing on Douyin Mall

Main result:
- Lowest eligible price option: JD
- Best value option: JD
- Safest purchase option: Tmall official store

Reasoning:
Cheaper excluded listings do exist, but they do not satisfy your stated purchase criteria.
```

---

## Example 15 — Branching by Package Type

### User Input
```text
Compare this product, but I’m not sure whether I want the standard version or the gift box.
```

### Correct Reasoning Pattern
- do not collapse standard and gift-box results
- produce separate comparisons for each package type
- explain that the answer depends on which offer the user values

### Example Output
```text
Your answer depends on package type, so I am keeping the two purchase paths separate.

If you want the standard version:
- Lowest price option: Platform A
- Best value option: Platform B

If you want the gift box:
- Lowest price option: Platform C
- Safest purchase option: Platform D official store

Reasoning:
Standard and gift-box editions are not the same purchasable offer, so they should not be collapsed into one strict cheapest conclusion.
```

---

## Recommended Agent Output Style

Across all examples, the Agent should usually present results in this order:

1. normalized target product
2. platform-by-platform comparison
3. lowest price option
4. best value option
5. safest purchase option
6. risk notes, conditions, and uncertainty
7. branch explanation if needed

### Good output pattern
```text
Target product:
[normalized product identity]

Comparison:
- Platform A ...
- Platform B ...
- Platform C ...

Recommendation:
- Lowest price option: ...
- Best value option: ...
- Safest purchase option: ...

Notes:
- ...
```

## Final Instruction

These examples teach one core habit:

The Agent should not rush from search results to “cheapest”.

The Agent should move through this sequence:
- understand the target
- confirm same-product comparability
- normalize price basis
- apply user constraints
- recommend with trade-off awareness

A good comparison answer is not just a number.  
It is a justified purchase recommendation.
