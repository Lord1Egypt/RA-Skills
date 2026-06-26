---
name: cart-optimizer
description: Optimize shopping-cart top-up plans for Taobao, JD, PDD, Tmall, and local ecommerce promotions
version: 1.0.0
tags: shopping, ecommerce, coupons, savings, cart-optimization, china
---

# Cart Optimizer - 凑单优化器

Optimize shopping-cart top-up plans for Taobao, JD, PDD, Tmall, and local ecommerce promotions. Use when the user asks about 凑单, 满减, 优惠券, 跨店满减, coupon stacking, discount thresholds, add-on item selection, or the cheapest way to reach a promotion tier.

## Usage Scenarios

### Scenario 1: Basic Top-Up Calculation
**User input:** "凑单 250 满 300 减 30"
**Expected output:** The skill calculates the minimum extra spend (￥50 needed), computes the effective savings rate, and recommends the best approach. If the user has candidate add-on items, evaluates each option and suggests the most cost-effective one. Output includes: best plan, final payment, extra spend, discount captured.

### Scenario 2: Multi-Tier Promotion Comparison
**User input:** "购物车 286，满 300 减 40，可选凑单品：纸巾 12，牙线 18，收纳盒 35。帮我选最划算方案"
**Expected output:** The skill evaluates each add-on item: adds 纸巾 (subtotal 298, doesn't reach threshold), adds 牙线 (subtotal 304, reaches 300 threshold, cost 18), adds both 纸巾+牙线 (subtotal 316, extra cost 30). Recommends adding 牙线 alone as the cheapest way to trigger the promotion, and calculates the final payment, savings rate, and whether the filler item is worth keeping.

### Scenario 3: Multi-Coupon Stacking Check
**User input:** "当前 420，平台满 500 减 80，店铺券满 399 减 30，品类券满 450 减 20，哪些能叠加？"
**Expected output:** The skill analyzes each coupon: 店铺券满399减30 is already triggered (current 420 > 399). 品类券满450减20 is not yet triggered (need 30 more). 平台券满500减80 is not yet triggered (need 80 more). If the user adds an item to reach 500, checks whether all three can stack (platform + store + category). Outputs caveats about platform stacking rules and recommends whether to pursue the higher threshold.
### Scenario 4: 凑单满减被凑坑了
**User input:** "淘宝618凑了300减50，结果发现凑的单品没法退，硬花了200块买了一堆没用的，下次怎么凑才不亏？"
**Expected output:** 分析凑单反被套路的常见原因：凑单品属于'不支持单独退款'类目。推荐正确的凑单策略：优先选天猫超市的日用品当凑单品（可单独退）；利用价保工具退差价；使用购物车分摊工具计算最优凑单倍数。建议在付款前截图对比凑单前后的实际折扣率。

## Best Use Cases

- 淘宝/天猫/京东/拼多多满减凑单
- 跨店满减、店铺券、平台券、品类券叠加判断
- Compare 满200减20, 满300减40, 满500减80 promotion tiers
- Decide whether to add a low-price filler item or upgrade an existing item
- Find the minimum extra spend needed before checkout
- Explain why a higher threshold is or is not worth chasing

## 功能特性

- 🎯 支持多种优惠类型：满减、折扣、优惠券
- 🧮 智能算法：最小额外支出、最大优惠利用率
- 🛒 多平台支持：淘宝、京东、拼多多
- 📊 实时计算：输入商品自动推荐凑单
- 💡 智能建议：推荐高性价比凑单品

## Inputs to Collect

- Current cart subtotal before discounts
- Promotion rule, such as 满300减40
- Available coupons and whether they can stack
- Candidate add-on items with prices and usefulness
- Shipping fee, return constraints, or category restrictions if relevant

## 使用方式

### 基础凑单
```
凑单 250 满 300 减 30
```

### 带购物车商品
```
购物车 250，凑满 300 减 30
```

### 多档优惠对比
```
对比凑单方案 250：满200减20 vs 满300减40
```

### 候选凑单品选择
```
购物车 286，满 300 减 40，可选凑单品：纸巾 12，牙线 18，收纳盒 35。帮我选最划算方案。
```

### 多券叠加检查
```
当前 420，平台满 500 减 80，店铺券满 399 减 30，品类券满 450 减 20，哪些能叠加？
```

## Output Format

Return:

1. Best plan and final estimated payment
2. Extra spend required
3. Discount captured and effective savings rate
4. Items to add or avoid
5. Caveats about platform rules, categories, shipping, and coupon stacking

If the user does not provide candidate add-on items, suggest the missing price band instead of inventing exact products.

## 核心算法

- 背包问题变种
- 动态规划优化
- 贪心算法备选

## Checkout Caveats

- Always ask the user to verify final checkout rules on the platform.
- Do not assume all coupons stack.
- Do not recommend buying an item that has no use unless the user explicitly optimizes only for price.
- Prefer reusable household items as filler suggestions when the user asks for examples.
