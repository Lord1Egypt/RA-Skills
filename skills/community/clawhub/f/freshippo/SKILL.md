---
name: freshippo
version: 2.1.2
description: "Shop Freshippo (盒马鲜生) in safe decision-assist mode: fresh grocery selection, shopping-list planning, delivery-window strategy, price/freshness checks, and manual order handoff. Use when the user wants help choosing 盒马 products, planning family meals, reducing fresh-food waste, comparing delivery windows, or preparing a manual shopping list without agent-controlled login, in-app product-list changes, coupon use, address choice, checkout, order submission, or payment."
metadata:
  clawdbot:
    emoji: "🦛"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# Freshippo (盒马鲜生)

## Overview

Use this skill to help users shop smartly on Freshippo (盒马鲜生), Alibaba's premium fresh grocery platform. Get guidance on fresh produce selection, delivery timing, membership benefits, and weekly meal planning.

## Safe Operating Mode

Default to **decision-assist mode**. The agent may help compare products, build a shopping list, explain freshness risk, and prepare manual steps. The user controls login, in-app product-list changes, checkout, order submission, payment, address selection, delivery-slot reservation, and coupon use. This published skill does not perform account-changing actions.

For every shopping task, collect only the missing essentials:

- household size, meal plan, dietary constraints, budget, and freshness priority
- delivery city/area and desired delivery window, if the user wants timing advice
- must-have items, substitution tolerance, and items to avoid

Return a shopping-list-ready answer:

```text
Recommended list: <items + quantities>
Freshness/risk check: <expiry, origin, cold-chain, substitution, stock caveats>
Delivery plan: <best slot + backup slot + why>
Manual checks: <price, coupon, address, final stock, payment>
```

## Capabilities

### v2.1 - Safe Shopping Support

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| **Search** | Optional | Search products, filter by category/freshness |
| **Product Detail** | Optional | View specs, prices, freshness indicators |
| **Fresh Produce Guide** | Optional | Read selection tips, origin info, reviews |
| **Price Compare** | Optional | Compare prices across categories |
| **Shopping-List Plan** | User-controlled | Provide exact manual list instructions and substitutions |
| **Coupon/Delivery Advice** | User-controlled | Tell the user what to check in app; do not claim applied discounts |
| **Address / Checkout / Payment** | User-controlled | User must complete these steps manually |

**Safety Rule**: The user retains full control over account state, address, checkout, delivery-slot reservation, coupon application, in-app product-list changes, and payment. Treat any separate host account-changing or payment tool as outside this skill and require a fresh, explicit user confirmation before using it.

### Legacy: Guidance-Only Mode (No Browser)

- Shopping strategy and selection tips
- Delivery timing advice
- X会员 membership guidance
- Weekly meal planning
- Shopping list templates

## Workflow

### Phase 1: Discovery (Agent-Assisted)
1. **Search** - Agent searches Freshippo for target products
2. **Filter & Sort** - Apply filters (category, freshness, origin)
3. **Compare** - Agent compares top options across categories
4. **Freshness Check** - Agent reads harvest dates, origin info, traceability codes
5. **Price Analysis** - Agent checks current price, X会员 discounts

### Phase 2: Selection (Agent-Assisted)
1. **Product Detail** - Agent opens selected product page
2. **Fresh Produce Tips** - Show selection indicators (日日鲜, 产地直采, 鲜活)
3. **Quantity Selection** - Confirm amount, weight
4. **Final Price Check** - Calculate price with X会员 discount if applicable

### Phase 3: Shopping-List Handoff (User-Controlled)
1. **Basket Summary** - Provide items, quantities, substitutions, and avoid-list.
2. **Coupon/Member Checks** - Tell the user what to verify in app without claiming a discount was applied.
3. **Delivery Slot Plan** - Recommend primary and backup windows based on freshness, meal timing, and peak demand.
4. **Manual Order Steps** - User performs login, in-app product-list changes, address selection, checkout, and payment.

**Agent Boundary**: Do not execute checkout, payment, address selection, or final order submission.

### Legacy: Guidance-Only Mode (No Browser)

1. Determine the user's goal:
   - browse categories and get product recommendations
   - plan weekly meals and build shopping lists
   - understand delivery slots and timing strategies
   - learn about X会员 membership benefits
   - get fresh produce selection tips
2. Ask for only the missing essentials
3. Give the most practical answer first
4. Provide cautious estimates if exact data unavailable

## Quick Reference

| Topic | Description |
|-------|-------------|
| Fresh Produce | 生鲜蔬果选购指南 |
| Delivery Slots | 配送时段优化建议 |
| X会员 Benefits | 盒马X会员权益详解 |
| Weekly Planning | 一周买菜规划 |
| Shopping Lists | 购物清单管理 |
| Read-Only Browser Support | 公开商品信息/价格/规格核对，不做账户变更 |

## Agent Execution Guide

### When User Says "帮我买..." / "帮我下单..."

```
User: "帮我买盒马的三文鱼"
  ↓
Step 1: Confirm Intent
  "我来帮你筛选盒马三文鱼，给出数量、鲜度风险和手动下单步骤。
   登录、App 内商品清单调整、地址、提交订单和支付都由你自己完成。"
  ↓
Step 2: Discovery Phase (No login required)
  - Search Freshippo for "三文鱼"
  - Filter: 鲜活, 产地, 价格区间
  - Compare top 3 options
  - Check freshness indicators (溯源码, 产地直采)
  - Present comparison table
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Confirm quantity/weight
  - Show final price (X会员价 if applicable)
  ↓
Step 4: Shopping-List Handoff (User-controlled)
  "建议清单已准备好，请在 App 中手动检查：
   [商品 + 数量 + 替代品 + 鲜度风险]

   👉 手动下单：
   1. 打开盒马 App
   2. 搜索商品并核对产地/规格/到期或捕捞信息
   3. 选择建议数量和替代品
   4. 确认地址、配送时段、优惠和最终价格
   5. 自行提交订单并支付"
```

### Read-Only Browser Rules

**Always announce before reading or navigating public information:**
- "正在搜索..."
- "正在打开商品页面..."
- "正在检查新鲜度信息..."

**Snapshot key information:**
- Product name, price, X会员 price
- Freshness indicators (日日鲜, 产地直采, 鲜活)
- Origin/traceability info
- Harvest/pack dates
- Public delivery timing guidance when available
- Manual checks the user must verify in the App

**Stop conditions:**
- Before login, address selection, in-app product-list changes, checkout, or payment
- When CAPTCHA appears
- When price, stock, delivery slot, or freshness information differs significantly from expected
- When the user asks the agent to place or pay for the order

### Login Handling

**Option A: User already logged in (Chrome profile)**
```
browser navigates to Freshippo
If user profile has active session → proceed
If session expired → prompt user to login manually first
```

**Option B: Manual mode (no login)**
```
Agent provides:
- Exact search keywords
- Product recommendations
- Freshness selection tips
- Step-by-step manual instructions
User executes manually
```

## Core Rules

### 1. Delivery Slot Timing

Freshippo operates on **30-minute delivery slots** (30分钟送达):

| Time Slot | Best For | Notes |
|-----------|----------|-------|
| 8:00 - 10:00 AM | Fresh produce, bakery | Best selection, morning delivery |
| 10:00 - 12:00 PM | Daily essentials | Good availability |
| 14:00 - 16:00 PM | Afternoon shopping | Moderate availability |
| 16:00 - 18:00 PM | Dinner prep | High demand, book early |
| 18:00 - 22:00 PM | Evening restock | Limited fresh selection |

**Strategy:**
- Book 8-10 AM slots for freshest produce
- Peak dinner prep slots (17:00-19:00) fill up fast
- Same-day delivery available if ordered before 21:00
- Rainy days may have delayed slots

### 2. Fresh Produce Selection

Freshippo's strength is **fresh food and quality groceries**:

| Category | Best Time to Buy | Quality Indicators |
|----------|------------------|-------------------|
| Vegetables | Morning 8-10 AM | Harvest date, origin label |
| Fruits | Morning 8-10 AM | Ripeness indicator, origin |
| Meat | Morning 8-10 AM | Slaughter date, grade |
| Seafood | Morning 8-10 AM | Catch/delivery date, live tanks |
| Bakery | Morning 8-10 AM | Bake time stamp |
| Dairy | Any time | Expiration dates |

**Pro Tips:**
- 盒马日日鲜 (Daily Fresh) = same-day packaged, best quality
- 产地直采 (Direct sourcing) = fresher, traceable
- 鲜活 (Live) seafood = premium quality, cook same day
- Check 溯源码 (traceability code) for origin info

### 3. X会员 Membership Benefits

**Membership Tiers:**

| Tier | Annual Fee | Key Benefits |
|------|------------|--------------|
| Regular | Free | Basic shopping, standard delivery |
| X会员 | ¥258/year | Free delivery, member prices, daily deals |
| X会员·黄金 | ¥658/year | All above + premium services |

**Member-Exclusive Features:**
- 免费配送 (Free delivery): No minimum order for X会员
- 会员价 (Member prices): 5-15% off regular prices
- 会员日 (Member day): Tuesday extra discounts
- 专享商品 (Member-only products): Premium selections
- 优先配送 (Priority delivery): Peak slots reserved

**Break-Even Analysis:**
- Shop >¥300/month → membership pays for itself
- Frequent fresh grocery buyers → highly recommended
- Free delivery saves ¥6-15 per order

### 4. Category Highlights

**盒马特色 (Freshippo Specialties):**

| Category | Highlights | Tips |
|----------|------------|------|
| 盒马工坊 | Ready-to-cook meals | Fresh, restaurant-quality |
| 海鲜水产 | Live seafood tanks | Cook in-store or home delivery |
| 日日鲜 | Daily fresh produce | Same-day packaging |
| 烘焙 | In-store bakery | Fresh daily, limited quantities |
| 进口食品 | International imports | Premium selection |
| 有机蔬菜 | Organic produce | Certified, higher price |

### 5. Smart Shopping Strategies

**Timing Strategies:**
1. **Morning Shopping (8-10 AM):** Best selection of fresh items
2. **Tuesday Member Day:** Extra discounts for X会员
3. **Evening Clearance (after 20:00):** Discounted bakery and ready meals
4. **Weekend Prep:** Plan ahead for busy slots

**Category Bundling:**
- Fresh + Pantry = Free delivery threshold easier to reach
- Ready meals + Fresh = Complete dinner solution
- Bulk buying on staples = Lower unit cost

**Payment Optimization:**
- 盒马钱包: Occasional extra discounts
- Alipay: Seamless integration
- Credit card partnerships: Check for cashback
- First-order: Usually has welcome discount

### 6. Delivery & Pickup

| Aspect | Details |
|--------|---------|
| Standard Delivery | 30-minute slots, 8:00 AM - 22:00 PM |
| Delivery Radius | ~3-5km from store |
| Free Shipping Threshold | ¥39 for non-members, free for X会员 |
| In-Store Shopping | Live seafood cooking, fresh bakery |
| Self-Pickup | Available at some locations |

**Delivery Optimization:**
- Choose morning slots for freshest produce
- Evening slots have limited fresh selection
- Combine orders to hit free shipping threshold
- Cold chain items delivered in insulated packaging

### 7. Weekly Meal Planning

**Family Shopping Guide:**

| Day | Focus | Suggested Items |
|-----|-------|-----------------|
| Monday | Fresh start | Vegetables, fruits, dairy |
| Tuesday | Member Day deals | Stock up on staples |
| Wednesday | Mid-week refresh | Meat, seafood |
| Thursday | Prep for weekend | Party foods, snacks |
| Friday | Weekend treats | Premium items, bakery |
| Saturday | Family cooking | Bulk fresh produce |
| Sunday | Meal prep | Ready meals, leftovers |

**Weekly Budget Guide:**
- Small family (2-3 people): ¥300-500/week
- Medium family (4-5 people): ¥500-800/week
- Large family (6+ people): ¥800-1200/week

## Common Traps

- **Overbuying perishables** → Fresh items have limited shelf life
- **Missing delivery slots** → Peak times fill up quickly
- **Ignoring member benefits** → Non-members pay delivery fees
- **Flash sale FOMO** → Compare with regular prices
- **Not checking expiration** → Especially on dairy and ready meals
- **Ordering during rush hour** → Limited slot availability

## Freshippo-Specific Features to Leverage

### 1. 盒马工坊 (Freshippo Kitchen)
- Ready-to-cook meals
- Restaurant-quality ingredients prepped
- Great for busy weeknights

### 2. 鲜活海鲜 (Live Seafood)
- Live tanks in store
- Cook in-store or take home
- Premium quality guarantee

### 3. 日日鲜 (Daily Fresh)
- Same-day packaged produce
- Clear harvest/pack dates
- Best quality indicator

### 4. 会员日 (Member Day)
- Tuesday exclusive deals
- Extra discounts for X 会员
- Limited-time promotions

### 5. 盒马村 (Freshippo Village)
- Direct farm sourcing
- Traceable origin products
- Seasonal specialties

## Quality Bar

### Do:
- ✅ Focus on fresh produce guidance
- ✅ Explain delivery timing strategies
- ✅ Use read-only browsing or user-provided screenshots for public product comparison
- ✅ Tell the user what X会员/coupon fields to check manually
- ✅ Generate a shopping-list handoff with substitutions and manual verification steps
- ✅ Stay honest about not doing payment operations

### Do Not:
- ❌ Log in or claim to be logged in
- ❌ Claim to confirm live inventory without checking
- ❌ Store user data persistently
- ❌ Change the user's in-app product list, apply coupons, reserve delivery slots, or choose addresses
- ❌ **Execute payment or final order submission**
- ❌ Guarantee freshness without evidence

## Related Skills

Install with `clawhub install <slug>` if user confirms:
- `home-food-planner` — family meal planning and nutrition
- `yhd` — YHD.com grocery shopping
- `jd-shopping` — JD.com shopping with automation
- `jingdong` — Alternative JD shopping guide

## Feedback

- If useful: `clawhub star freshippo`
- Stay updated: `clawhub sync`

---

## 🚀 First-Success Path

**30秒快速上手：三步完成盒马购物决策**

1. **告诉我你想买什么** — 如"帮我看看盒马有什么好的三文鱼"
2. **获取推荐对比** — 我搜索盒马商品、对比价格和新鲜度信息
3. **拿到手动清单** — 你本人在盒马 App 核对价格、优惠、商品清单、地址、配送时段并下单

> 示例："帮我看看盒马今天有什么新鲜的草莓，我想买两盒"

---

## 📝 Sample Prompts

### 示例 1：商品搜索与推荐
**用户输入：**
```
帮我看看盒马有什么好的三文鱼，想要新鲜的、性价比高的
```

**期望输出：**
```
🔍 搜索盒马：三文鱼

找到以下商品（按推荐排序）：

1️⃣ 🥇 挪威三文鱼刺身中段 200g
   价格: ¥69.9（X会员 ¥59.9）
   产地: 挪威
   特点: 可溯源码、冰鲜配送
   新鲜度: ✅ 今日到店

2️⃣ 🥈 智利三文鱼排 250g
   价格: ¥49.9（X会员 ¥42.9）
   适合: 煎烤烹饪
   特点: 急冻锁鲜

3️⃣ 🥉 三文鱼腩刺身 150g
   价格: ¥55.0（X会员 ¥46.8）
   特点: 油脂丰富，口感最佳

💡 推荐：如果想做刺身 → 推荐#1；如果想煎烤 → 推荐#2性价比高
```

### 示例 2：周采购规划
**用户输入：**
```
帮我规划一下这周的晚餐采购清单，两个人吃，预算500以内
```

**期望输出：**
```
🛒 两人份周采购规划（预算 ¥500）

📅 周一：番茄牛腩 + 清炒时蔬
   - 牛腩 500g ¥45 | 番茄 3个 ¥9 | 西兰花 1颗 ¥8

📅 周二：清蒸鲈鱼 + 蒜蓉菜心
   - 鲈鱼 1条 ¥35 | 菜心 300g ¥6

📅 周三：宫保鸡丁 + 凉拌黄瓜
   - 鸡胸肉 300g ¥18 | 花生米 ¥5 | 黄瓜 2根 ¥5

📅 周四：排骨汤 + 蚝油生菜
   - 排骨 400g ¥42 | 生菜 1颗 ¥5

📅 周五：虾仁滑蛋 + 炒杂蔬
   - 虾仁 200g ¥38 | 鸡蛋 6枚 ¥8 | 杂蔬包 ¥10

📅 周末：火锅自由
   - 肥牛卷 300g ¥48 | 火锅底料 ¥15 | 蔬菜拼盘 ¥20

💰 预估总计：¥459（预算内 ✅）
💡 X会员预计可再省约 ¥45-60
```

### 示例 3：配送策略
**用户输入：**
```
我想明天早上收到菜，盒马什么时段送最好？
```

**期望输出：**
```
📦 盒马配送时段建议（明天）

⏰ 最佳选择：08:00-10:00 早间时段
   ✅ 新鲜度最高
   ✅ 预约充裕，不抢单
   ✅ 蔬菜水果都是今早到店

⏰ 次选：10:00-12:00 上午时段
   ✅ 可选性仍好
   ⚠️ 日日鲜商品可能部分售罄

⏰ 不建议：下午/傍晚时段
   ❌ 新鲜品选择少
   ❌ 高峰时段预约难

💡 策略：
   • 今晚0点后可预约明天早上时段
   • X会员可优先保留配送时段
   • 如附近有盒马门店，最快30分钟送达
```

### 示例 4：会员分析
**用户输入：**
```
我每个月在盒马大概花600块，开X会员划算吗？
```

**期望输出：**
```
💳 X会员性价比分析

你的月均消费：¥600/月（¥7,200/年）

📊 会员权益价值估算：

1️⃣ 免费配送（会员免费，非会员¥6/单）
   假设月均5单 → 省 ¥360/年

2️⃣ 会员专享价（约5-15% off）
   一般消费 → 省 ¥500-800/年

3️⃣ 周二会员日折扣
   额外优惠 → 省 ¥200-400/年

💰 总节省预估：¥1,060-1,560/年
会员年费：¥258

📈 净节省：¥800-1,300/年 ✅ 非常推荐

💡 建议：
   • 如果月消费≥¥300，会员基本回本
   • 你的消费水平开会员可省30%以上的配送费
   • 先领新客优惠（有些渠道首年有折扣）
```

### 示例 5：生鲜选购技巧
**用户输入：**
```
怎么在盒马买到最新鲜的蔬菜？日日鲜和普通的有什么区别？
```

**期望输出：**
```
🥬 盒马蔬菜选购指南

📦 日日鲜（Daily Fresh） vs 普通蔬菜

| 对比项 | 日日鲜 | 普通蔬菜 |
|-------|--------|---------|
| 包装日期 | 当天（明确标注） | 1-3天内 |
| 产地 | 盒马直采基地 | 多种渠道 |
| 价格 | 稍高（+10-20%） | 标准价 |
| 保质期 | 2-3天 | 3-5天 |
| 最佳食用 | 当天 | 1-2天内 |

🔍 挑选技巧：

1️⃣ 看包装日期
   - 日日鲜必有"包装日期：今天"
   - 没有日期的一律视为隔夜菜

2️⃣ 看产地直采标签
   - "产地直采" > 普通采购
   - "盒马村" 标注的产品品质最好

3️⃣ 按购买时机
   - 早8-10点：蔬菜最新鲜，品种最全
   - 晚8点后：可能有折扣，但新鲜度下降

4️⃣ 检查蔬菜状态
   - 叶菜：看叶片是否挺括、无水渍
   - 根茎类：看表皮完整度
   - 不要只看价格标签，实物要翻看
```

---

## 📋 Real Task Examples

| 场景 | 用户输入示例 | 技能输出要点 |
|------|-------------|-------------|
| **智能买菜** | "帮我买盒马的黑虎虾，看看有什么规格的" | 搜索建议 → 对比规格/价格/会员价 → 推荐最合适的 → 给用户手动清单 |
| **周计划** | "这周末有朋友来家吃饭，4个人，帮我列个采购清单" | 根据人数/场景规划菜单 → 生成采购清单 → 推荐盒马对应商品 → 估算费用 |
| **优惠分析** | "盒马上有没有什么划算的蒙牛牛奶？" | 搜索+价格对比 → 分析单品/整箱哪个划算 → 计算X会员折扣 → 检查周二会员日优惠 |
| **选购咨询** | "阿根廷红虾和黑虎虾哪个好吃？" | 产地/口感/烹饪方式对比 → 价格对比 → 建议搭配 → 提醒用户手动核对盒马库存 |
| **配送优化** | "我明天要出差，想提前订好家里的菜" | 配送时段选择建议 → 手动预约提醒 → 生鲜保鲜建议 → 收件安排提示 |
