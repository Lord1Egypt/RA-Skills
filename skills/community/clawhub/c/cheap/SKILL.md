---
name: cheap
description: Find the cheapest meaningful visible price for a product across major Chinese shopping platforms
version: 1.0.0
tags: shopping, price-comparison, savings, cross-platform, ecommerce, china
---

# Cheap

Find the cheapest meaningful visible price for a product across major Chinese shopping platforms. Use when the user provides a product name and wants the lowest current visible price, the cheapest platform, or a quick cross-platform price comparison. Ask questions like "哪个最便宜", "哪里买最便宜", "帮我比价", "全网找最低价", "哪个平台便宜", "哪里下单最划算", or "帮我找最低价".

## Usage Scenarios

### Scenario 1: Cross-Platform Price Comparison
**User input:** "帮我比价小米手环 8 Pro，哪个平台最便宜？"
**Expected output:** The skill searches across Taobao, Tmall, JD.com, Pinduoduo, and other relevant platforms. Compares like-for-like listings (same model, specs, bundle). Returns: Cheapest Found (platform and price), Comparable Options with prices on other platforms, Match Confidence (whether listings look like the same product), Caveats (variant match, coupon pricing, shipping), and Final Advice.

### Scenario 2: Ambiguous Product Name
**User input:** "哪里买 iPhone 最便宜？"
**Expected output:** The skill identifies the product as too broad (iPhones have many models), asks one short clarifying question: "您具体想看哪个型号？比如 iPhone 15 Pro, iPhone 15, 还是 iPhone 14？不同型号价格差异很大。" Then proceeds with the comparison once clarified.

### Scenario 3: Price-Limited Mode (Weak Results)
**User input:** "帮我找这款小众耳机的全网最低价，只有一个淘宝店在卖"
**Expected output:** The skill attempts cross-platform search. If only one platform has this product (Price-limited mode), switches to Mode 2. Outputs: Current Best Signal (the single available price), Why No Strong Cheapest Claim (product too niche for cross-platform comparison), What Remains Unverified (whether other platforms may have it at different prices), and Final Advice with cautious conclusion.
### Scenario 4: 想买便宜机票
**User input:** "想去成都玩几天，从深圳出发，怎么买机票最便宜？什么时候买最划算？"
**Expected output:** 推荐比价策略：同时查去哪儿、携程、飞猪、航司官网（如南航、深航）的价格，注意含税总价。建议提前3-4周购票，选中周三/周四出发。使用各平台的'低价日历'和'预约提醒'功能。给出深圳到成都的近期待票价区间参考，并建议关注航司会员日（如南航每月28号）。

## Workflow

1. Identify the product.
   - Accept a product name.
   - If the product is too broad or ambiguous, ask one short clarifying question for the most decision-relevant detail, such as brand, model, size, or key variant.

2. Check price accessibility.
   - Search across relevant Chinese platforms.
   - Decide which mode applies:
     - **Mode 1** if enough visible price evidence is accessible and comparable.
     - **Mode 2** if platform access, listing clarity, or price conditions are too weak for a strong cheapest-price claim.

3. If Mode 1, compare meaningful prices.
   - Prefer Taobao, Tmall, JD.com, Pinduoduo, and other clearly relevant platforms.
   - Use only currently visible price evidence.
   - Match comparable listings by brand, model, specs, quantity, version, and bundle contents.
   - Distinguish straightforward visible price from coupon-only, member-only, deposit/pre-sale, bundle-distorted, or variant-mismatched prices.

4. If Mode 2, do not fake precision.
   - State that the currently accessible evidence is too weak for a strong cheapest-price claim.
   - Explain whether the issue is platform access, weak product matching, or distorted price conditions.
   - Give only a limited conclusion when still useful.

5. Give the result.
   Cover:
   - cheapest platform or listing found when supportable
   - visible price evidence actually available
   - comparable alternatives when supportable
   - matching confidence
   - any caveats about variants, bundles, coupons, seller trust, or access limits

## Output

Use this structure unless the user asks for something else.

### Mode 1 output
Use when enough price evidence is accessible.

#### Cheapest Found
State the lowest meaningful visible price found and on which platform.

#### Comparable Options
List the main comparable prices found on other platforms.

#### Match Confidence
State whether the compared listings look like the same product:
- High
- Medium
- Low

#### Caveats
State any important risks, such as:
- unclear variant match
- bundle differences
- coupon or membership pricing
- deposit or pre-sale pricing
- seller quality concerns
- incomplete platform access

#### Final Advice
Give a direct buying suggestion in plain language.

### Mode 2 output
Use when accessible evidence is too weak for a strong lowest-price claim.

#### Current Best Signal
State the weakest still-usable price clue, if any.

#### Why No Strong Cheapest Claim
Explain whether the issue is:
- platform access limits
- weak listing comparability
- unclear price conditions
- incomplete platform coverage

#### What Remains Unverified
State what cannot yet be confirmed.

#### Final Advice
Give a cautious conclusion without pretending a definitive lowest price was found.

## Quality bar

Do:
- compare like-for-like listings
- say when the cheapest visible option may not be the best option
- distinguish real low price from misleading low price
- be explicit when matching confidence is weak

Do not:
- compare different variants as if they were the same item
- treat coupon-only or pre-sale prices as normal prices without warning
- claim full-market coverage when platform access is incomplete
- invent prices or listing details

## Limitation handling

If the product is too ambiguous:
- ask one short clarifying question

If platform access is incomplete:
- switch to Mode 2 unless a narrower Mode 1 comparison is still supportable
- say which platforms were actually checked
- avoid claiming a definitive all-platform lowest price
- do not present a partial platform scan as a full-market cheapest-price result

If listing comparability is weak:
- lower confidence
- explain what may not match cleanly

If the visible lowest number depends on unclear conditions:
- do not present it as the straightforward cheapest option without warning
