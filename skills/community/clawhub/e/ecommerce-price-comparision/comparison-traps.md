# Comparison Traps — Product Matching and Price Interpretation Failures

## Core Objective

This file documents the most common comparison failures that produce false “cheapest” conclusions.

The Agent should use this file to recognize when a low number, similar title, or attractive listing should **not** be treated as a valid same-product comparison result.

The costliest comparison mistake is not missing a lower price.  
The costliest mistake is confidently comparing the wrong thing.

---

## 1. Different Specs Treated as the Same Product

**Problem:** Listings look similar by title, but core specs differ. The Agent compares them directly and produces a false lowest-price conclusion.

Typical mismatches:
- 256GB vs 512GB
- 30ml vs 50ml
- standard edition vs gift box
- 1-pack vs 2-pack
- domestic version vs imported version

**Wrong:**
```text
JD: iPhone 16 256GB Black — ¥5,999
Pinduoduo: iPhone 16 512GB Black — ¥6,099

Conclusion: Pinduoduo is only ¥100 more, so it is the better deal.
```

**Correct:**
```text
JD result and Pinduoduo result are not directly comparable because capacity differs.
They must be treated as different product variants.
No strict lowest-price conclusion should be made across them.
```

**Rule:**
- Model, version, capacity, size, quantity, and package-content mismatch override title similarity
- If variants are mixed in search results, split the comparison into separate branches

---

## 2. Deposit or Pre-sale Display Treated as Final Payable Price

**Problem:** The page shows a small number such as “deposit ¥50” or “pre-sale from ¥199”, and the Agent incorrectly treats it as the actual payable price.

**Wrong:**
```text
Douyin Mall listing shows ¥100.
Conclusion: Douyin Mall is the cheapest platform.
```

**Correct:**
```text
The ¥100 shown is a deposit, not the final payable amount.
It cannot be used as the comparison price.
The listing should be marked as pre-sale or deposit-based until the total payable amount is confirmed.
```

**Rule:**
- Deposit is never final payable price
- Pre-sale teaser price is not enough for strict comparison
- If only deposit is visible, mark the listing as incomplete or conditional

---

## 3. Conditional Price Treated as Universal Price

**Problem:** A low price is displayed, but it depends on an extra condition:
- coupon collection
- membership
- livestream access
- first-order status
- regional subsidy
- platform subsidy entry
- group-buy participation

The Agent reports that price as the default comparison basis.

**Wrong:**
```text
Taobao listing shows ¥299 after joining membership.
Conclusion: Taobao is the cheapest option.
```

**Correct:**
```text
The ¥299 price is conditional on membership enrollment.
It should be labeled as a conditional payable price, not a universal default price.
```

**Rule:**
- Conditional prices must include their activation conditions
- A conditional price is not stronger than an unconditional price
- If the condition is uncertain, the price must be marked uncertain

---

## 4. Group-buy Price Treated as Solo-buyer Price

**Problem:** A platform shows a lower “group-buy” or multi-person price, but the Agent compares it against normal solo-purchase prices.

**Wrong:**
```text
Pinduoduo: ¥89
JD: ¥109

Conclusion: Pinduoduo is cheaper by ¥20.
```

**Correct:**
```text
The ¥89 price is a group-buy price requiring multi-person participation.
If the user is buying alone, the solo-buyer price is the relevant comparison basis.
```

**Rule:**
- Group-buy price and solo-buyer price are different price bases
- If the user did not explicitly accept group-buy conditions, do not use group-buy pricing as the default comparison result

---

## 5. Livestream Price Treated as Stable Listing Price

**Problem:** A listing appears very cheap on Douyin or another content-commerce channel, but the price depends on livestream access, time window, or manual coupon collection.

**Wrong:**
```text
Douyin Mall has the lowest price at ¥459.
Conclusion: Buy from Douyin Mall.
```

**Correct:**
```text
The ¥459 price appears to depend on livestream access and a limited-time coupon.
It should be treated as a conditional promotional price, not a stable listing price.
```

**Rule:**
- Livestream prices must be labeled with timing and access conditions
- If availability cannot be verified, mark the result as conditional
- Do not rank livestream-only pricing above stable payable pricing without explanation

---

## 6. Official and Non-official Stores Treated as Equivalent

**Problem:** The Agent compares official flagship stores, self-operated channels, authorized sellers, and unknown third-party sellers purely by price.

**Wrong:**
```text
Official flagship store: ¥1,299
Unknown third-party store: ¥1,199

Conclusion: The unknown store is better because it is cheaper.
```

**Correct:**
```text
The unknown third-party store is cheaper, but store trust differs materially.
This should affect recommendation logic.
The official store may still be the safest purchase option.
```

**Rule:**
- Store type is part of the comparison, not background noise
- Official, self-operated, authorized, and unknown sellers are not equivalent purchase paths
- Recommendations must distinguish lowest price from safest purchase

---

## 7. Bundle Edition Compared Directly to Standard Edition

**Problem:** One listing includes gifts, accessories, warranty, or service; another is the standard item only. The Agent compares raw price without acknowledging package-content differences.

**Wrong:**
```text
Tmall standard edition: ¥799
JD bundle edition with accessories: ¥859

Conclusion: Tmall is cheaper.
```

**Correct:**
```text
These two listings differ in package content.
They are not directly equivalent unless the package-content difference is explicitly accounted for.
```

**Rule:**
- Standard edition and bundle edition must not be mixed silently
- If package value cannot be normalized confidently, present them as separate purchase options

---

## 8. Used, Refurbished, or Imported Variants Mixed with New Domestic Listings

**Problem:** A cheap listing is actually used, refurbished, parallel import, or overseas version, but the Agent compares it directly with standard new domestic retail products.

**Wrong:**
```text
Imported version on marketplace: ¥3,999
Official domestic version on JD: ¥4,699

Conclusion: Marketplace is much cheaper.
```

**Correct:**
```text
These may not be equivalent products.
Imported, refurbished, or used variants must be separated from new domestic retail versions unless the user explicitly requested them.
```

**Rule:**
- Condition and version are first-order distinctions
- These listings may be useful alternatives, but not default same-product price evidence

---

## 9. Shipping Ignored When It Materially Changes Real Cost

**Problem:** One listing has a lower visible product price, but higher shipping makes it equal or more expensive in practice.

**Wrong:**
```text
Taobao: ¥88
JD: ¥92

Conclusion: Taobao is cheaper.
```

**Correct:**
```text
Taobao price is ¥88 + ¥12 shipping.
JD price is ¥92 with free shipping.
JD has the lower final payable price.
```

**Rule:**
- Cheaper visible product price is not the same as lower final payable price
- Include shipping whenever it materially changes the user’s out-of-pocket cost

---

## 10. Platform Naming Differences Mistaken for Product Differences

**Problem:** Different platforms describe the same product using different title style, abbreviation, or attribute order. The Agent wrongly rejects them as different products.

**Wrong:**
```text
JD: Xiaomi Air Purifier 4 Pro Smart Sterilization Edition
Tmall: Xiaomi Purifier 4 Pro Home Formaldehyde Removal

Conclusion: These are different products.
```

**Correct:**
```text
Title wording differs across platforms.
The Agent should rely on structured attributes such as brand, model, version, and capacity rather than title phrasing alone.
```

**Rule:**
- Title mismatch alone does not prove product mismatch
- Structured specs are stronger evidence than wording style

---

## 11. Near-equivalent Products Reported as Strict Same-product Results

**Problem:** Two products are highly similar in use case or appearance, but are not actually the same product. The Agent reports one as the same product instead of a near-equivalent alternative.

**Wrong:**
```text
These two humidifiers look similar and have similar capacity.
Conclusion: Same product, compare directly.
```

**Correct:**
```text
These are near-equivalent products, not confirmed same-product listings.
They may be useful alternatives, but should not drive a strict same-product cheapest conclusion.
```

**Rule:**
- Same product and near-equivalent are different categories
- Near-equivalent results may support alternatives, not strict same-product price claims

---

## 12. Uncertain Result Forced into a Hard Conclusion

**Problem:** The Agent lacks enough evidence to confirm product identity or payable price, but still outputs a definite cheapest recommendation.

**Wrong:**
```text
The listing might be the same model and the price might include coupons.
Conclusion: This is definitely the cheapest option.
```

**Correct:**
```text
Product identity and final payable price cannot be confirmed with high confidence.
The result should remain conditional or uncertain.
No strict cheapest conclusion should be given.
```

**Rule:**
- Uncertainty must remain uncertainty
- A weaker but honest answer is better than a false precise answer

---

## 13. User Preference Ignored

**Problem:** The user explicitly says “official stores only”, “no pre-sale”, or “fast delivery first”, but the Agent still recommends an ineligible low-price option.

**Wrong:**
```text
User asked for official stores only.
Recommendation: third-party listing with lower price.
```

**Correct:**
```text
The third-party listing is excluded from main recommendations because the user specified official stores only.
```

**Rule:**
- User constraints are binding filters, not optional hints
- A lower price is irrelevant if it violates stated requirements

---

## 14. Search Relevance Confused with Same-product Confidence

**Problem:** A platform search engine ranks a result at the top, and the Agent assumes it is the correct product without validation.

**Wrong:**
```text
Top result on platform search = same product.
```

**Correct:**
```text
Search ranking reflects platform relevance, not verified same-product identity.
The Agent must still validate model, version, specs, and package content.
```

**Rule:**
- Top-ranked search result is only a candidate
- Same-product matching rules still apply after retrieval

---

## 15. “Cheapest” Reported Without Decision Context

**Problem:** The Agent reports the cheapest listing but fails to explain whether it is trustworthy, conditional, delayed, or risky.

**Wrong:**
```text
Cheapest result: Platform X, ¥299.
```

**Correct:**
```text
Lowest visible price: Platform X, ¥299, but it depends on a member-only coupon and the seller is a non-official third-party store.
Best value may be Platform Y at ¥319 with clear after-sales support and no extra conditions.
```

**Rule:**
- Lowest price alone is incomplete
- Every cheapest claim should be decision-ready, not just numerically correct

---

## Practical Failure Test

Before concluding that one platform is cheaper, the Agent should check:

- Is it the same model?
- Is it the same version?
- Is it the same capacity, size, or quantity?
- Is it the same package content?
- Is the item new and comparable in condition?
- Is the displayed price the final payable price?
- Are shipping and required conditions included?
- Does the result respect the user’s constraints?
- Is confidence high enough for a strict lowest-price conclusion?

If any answer is “no” or “uncertain”, downgrade the conclusion.

## Final Instruction

When in doubt:

- separate variants
- label conditions
- preserve uncertainty
- prefer a trustworthy explanation over a false precise answer
