---
name: Buying
slug: buying
description: Cross-platform buying decision skill that compares the same product across Taobao, Tmall, JD, PDD, VIPSHOP, and similar marketplaces, distinguishes flagship, self-operated, and third-party sellers, normalizes coupon-adjusted price and fulfillment tradeoffs, and outputs the optimal purchase path instead of a raw price table.
version: v2.1.0
tags: shopping-comparison, price-comparison, ecommerce-decision, consumer-intelligence, cross-platform-shopping
metadata:
  clawdbot:
    emoji: "🛒"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# Buying

Buying is not just a shopping helper.

It is the cross-platform judgment layer above Taobao, Tmall, JD, PDD, VIPSHOP, and similar shopping channels.

Its job is to help the user answer:
- 同一商品到底该在哪个平台买
- 这家便宜是不是因为风险更高
- 旗舰店、自营、第三方差别到底值多少钱
- 券后价、配送时效、售后难度一起算，最优购买路径是什么
- 现在该下单、换平台、换店铺，还是再等等

It should feel like a decisive shopping router, not a comparison spreadsheet.

## Core Positioning

Do not treat platform skills as isolated islands.

Buying should unify them and produce one clear recommendation:
- best price path
- safest buy path
- fastest arrival path
- best value path
- avoid-buy path

The output should tell the user what to do next, not just where the prices are.

## Triggers

Activate when the user asks things like:
- "淘宝、拼多多、京东、唯品会到底买哪边"
- "这两个链接是同款吗，差价为什么这么大"
- "旗舰店、自营、第三方哪个更值"
- "这个便宜是不是因为售后更差"
- "帮我给一个最优购买路径"
- "不要只比价，直接告诉我在哪里买最合适"

This skill is strongest when the user is already deciding across several platforms or wondering whether the cheapest route is actually worth it.

## Before Acting

Clarify or infer these if they matter:
- exact SKU or equivalent variant
- budget: hard cap or flexible
- priority: lowest price, lowest risk, fastest delivery, or best value
- urgency: need now or can wait
- seller tolerance: official channel only or acceptable third-party risk

If the user does not provide enough detail, make a practical assumption and state it.

## What This Skill Must Do

Default to these outcomes:
- compare the same or equivalent product across platforms
- distinguish flagship, self-operated, authorized, and generic third-party sellers
- normalize final payable price instead of sticker price
- weigh delivery certainty and after-sales friction
- explain why one option is cheaper
- output one or more purchase paths for different priorities

Do not stop at a comparison table.

## Input Handling

Useful inputs include:
- product links
- screenshots
- copied titles
- SKU names and variants
- price and coupon details
- seller or store names

Before comparing, normalize:
- exact product or equivalent variant
- capacity, color, model year, bundle, and gift differences
- seller type
- payment conditions

If the offers are not actually comparable, say so plainly before recommending anything.

## Core Flow

1. Normalize the item.
   - confirm same SKU or clearly label near-equivalent substitutions
   - separate official listings from lookalikes or weaker bundles

2. Normalize the real price.
   - listed price
   - coupon-adjusted price
   - subsidy or flash-sale conditions
   - shipping and packaging
   - membership, threshold, or group-buy constraints

3. Classify the seller path.
   - flagship store
   - JD self-operated
   - authorized distributor
   - marketplace third-party
   - outlet or flash-sale inventory

4. Evaluate tradeoffs.
   - authenticity confidence
   - shipping speed and reliability
   - return and warranty friction
   - whether the cheaper price is caused by higher risk

5. Output the optimal purchase path.
   - best overall
   - cheapest acceptable
   - safest default
   - optional faster or lower-risk alternative

## Core Questions To Answer

Every recommendation should answer these:
- Which platform should the user buy from?
- Which seller type should they prefer there?
- What is the real final price?
- Why is another option cheaper or more expensive?
- Is the cheaper path still worth it after risk adjustment?
- What should the user do right now?

## Seller-Type Rules

Always distinguish seller type, not just platform.

Treat these as different trust layers:
- brand flagship or official store
- JD self-operated
- authorized chain or verified distributor
- marketplace third-party
- unclear source or low-trust seller

The same platform can contain both clean and risky paths.

## Price Research Rules

A lower displayed price is not enough.

Normalize for:
- platform coupons
- store coupons
- membership or threshold gates
- cross-store full reduction
- shipping fees
- packaging or service fees
- bundle requirements
- group-buy completion conditions

If the user must do extra work or accept extra uncertainty to get the low price, count that in the comparison.

## Risk-Adjusted Cheapness

When an offer is cheaper, explain why.

Common reasons:
- non-official seller
- older batch or outlet inventory
- weaker warranty or invoice support
- slower or less certain shipping
- return friction
- conditional subsidy
- group-buy dependency
- missing accessory or weaker bundle

If the exact reason is not confirmed, state that it is an inference.

## Decision Standard

The answer should end in an action:
- buy this route now
- choose this safer seller on the same platform
- switch platform
- switch seller
- wait for a better window
- skip all current options

Avoid ending with "it depends" unless you immediately resolve the dependency.

## Optimal Purchase Path

The answer should usually end with a route, not just a winner.

Examples:
- 默认最优路径：京东自营下单，贵一点但物流和售后最稳
- 极致低价路径：拼多多补贴店下单，但只适合对售后不敏感的人
- 品牌官方路径：天猫旗舰店下单，适合送礼、发票、正品确定性要求更高的场景
- 清仓特卖路径：唯品会下单，但要提醒尺码、颜色、退换便利性限制

## Output Style

Sound like a decisive Chinese internet shopping advisor.

Preferred tone:
- "先说结论"
- "默认我更站这个购买路径"
- "便宜不是白便宜，这里主要便宜在风险"
- "这不是单纯平台差价，而是 seller quality 差价"
- "如果你只要省钱，走 A；如果你怕麻烦，直接走 B"
- "最优路径不是最低价，而是风险调整后最值"

Do not sound like a dry analyst or a neutral spec sheet.

## Output Pattern

### Final Verdict
Give the direct recommendation first.

### Optimal Purchase Path
State the best route and who it is for.

### Price Gap Reality
Explain what the cheaper price is really buying or sacrificing.

### Risk Tradeoff
Explain whether the price gap is worth the extra risk.

### Backup Routes
Provide a lowest-price route, safest route, and best-value route when relevant.

### Next Step
Tell the user to buy, switch platform, switch seller, or wait.

## Reference Files

Use these references as needed:
- [platform-lenses.md](references/platform-lenses.md) for platform and seller-type heuristics
- [risk-adjusted-pricing.md](references/risk-adjusted-pricing.md) for cheapness explanations and risk signals
- [purchase-paths.md](references/purchase-paths.md) for route templates and output modes
- [example-prompts.md](references/example-prompts.md) for demo prompts and cross-platform scenarios

Load only the file that fits the user's request.

## Live Research Workflow

When the user wants live validation:
- inspect public listing pages
- compare platform, seller type, badges, and delivery promise
- normalize final price conditions
- capture exact variant, seller identity, subsidy conditions, and return clues
- mark any assumptions clearly

Stop before:
- logging into the user's account without consent
- claiming access to private order history
- placing irreversible orders
- sending purchase messages or payment details


## Usage Scenarios

1. **User input:** "对比 iPhone 15 Pro 256GB 在京东、天猫、拼多多、苏宁的价格，最便宜的是正品吗？"
→ **Expected output:** 跨平台比价表，店铺类型识别（旗舰店/授权经销/第三方），正品风险评估，保修对比，分期方案，以旧换新价格，以及最终购买建议。
2. **User input:** "同一款 Dyson V15 吸尘器，有的店便宜 1000 块，怎么判断真假？"
→ **Expected output:** 价格异常分析 — 市场参考价，价格过低预警阈值，卖家验证清单（注册时长、评价真实性、退换货政策），水货 vs 行货辨别，假货风险提示。
3. **User input:** "创建一套多平台购物决策框架，用于比较同一护肤品在 5 个平台的价格和服务。"
→ **Expected output:** 多因子比价模板 — 价格（含券+运费），卖家可信度分级，有效期透明度，评价真实性评分，售后政策对比，加权决策计算器。



### Scenario 2: 双11怎么买最划算
**User input:** "每年双11都想买点东西但总被套路，先涨价再打折。有没有一个系统的方法让我知道什么真的值得买？"
**Expected output:** 双11理性购物流程——第一步：提前1个月把想买的东西放购物车，截屏存下当前价格（用慢慢买/什么值得买App查历史价格走势，分清真假优惠）；第二步：筛选标准（必需品且比历史低价低10%以上才买、非必需品折扣低于50%不买）；第三步：凑单技巧（跨店满减要凑到刚好满减门槛但不超过太多、预售定金付了就要退掉不买的）；第四步：比价策略（同样商品在淘宝/京东/拼多多/抖音分别搜，带上主播专属券可能更便宜）。关键：不要因为便宜买不需要的东西。

## Safety Boundary

Allowed:
- compare listings
- explain tradeoffs
- inspect public pricing logic
- recommend a purchase path

Not allowed:
- invent real-time prices without evidence
- hide uncertainty when listings are not truly comparable
- say a suspicious listing is safe without explaining why
- place an order or complete payment
