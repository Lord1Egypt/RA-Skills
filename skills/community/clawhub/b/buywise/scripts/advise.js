#!/usr/bin/env node
'use strict';
/**
 * BuyWise — 综合购物决策主入口
 * 输入商品名或链接，输出完整的"买不买、在哪买、等不等"分析报告
 * 用法: node scripts/advise.js <商品名或URL> [--lang zh|en]
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const productArgs = args.filter((a, i) => a !== '--lang' && args[i - 1] !== '--lang');
const product = productArgs.join(' ').trim();

if (!product) {
  console.error(lang === 'zh' ? '用法: node scripts/advise.js <商品名或链接>' : 'Usage: node scripts/advise.js <product name or URL>');
  process.exit(1);
}

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

// 判断是否临近大促节点
function nearPromo() {
  const m = now.getMonth() + 1, d = now.getDate();
  if ((m === 11 && d >= 1) || (m === 6 && d >= 1 && d <= 20)) return true;
  if ((m === 3 && d >= 8 && d <= 15) || (m === 12 && d >= 12 && d <= 13)) return true;
  return false;
}
const promoHint = nearPromo()
  ? (lang === 'zh' ? '\n⚠️ 当前临近大促节点，请重点分析是否值得等待促销，并核查价格是否真实优惠。' : '\n⚠️ Near a major sale event — prioritize analyzing whether waiting is worthwhile and verify if the discount is genuine.')
  : '';

const encoded = encodeURIComponent(product);

if (lang === 'zh') {
  console.log(`请对以下商品进行全面的购物决策分析：「${product}」
当前日期：${dateISO}${promoHint}

## 第一步：多平台比价（用 browser 导航，不要用 web_search 猜价格）
按顺序打开以下 URL，从页面直接提取价格：
1. https://search.smzdm.com/?c=home&s=${encoded}&v=b → 一站获取京东/淘宝/天猫/拼多多聚合价格
2. https://search.jd.com/Search?keyword=${encoded}&enc=utf-8 → 京东直查，取自营商品价格
3. https://www.google.com/search?q=${encoded}&tbm=shop → Google 购物：一站聚合 Amazon/eBay/Walmart 等几十家零售商真实价格，取价格区间和最低价
4. 如 Google 购物无法访问 → 备用 https://www.bing.com/shop?q=${encoded}
5. https://www.amazon.com/s?k=${encoded} → 与 Google Shopping 交叉验证 Amazon 价格
6. https://www.aliexpress.com/wholesale?SearchText=${encoded} → AliExpress 前3条价格
7. web_search「${product} Temu price」→ Temu 补充（无标准搜索 URL）
8. web_search「${product} 闲鱼 价格」→ 二手参考

⚠️ 规则：只记录从页面实际读取到的价格；某平台无法访问则标"无法获取"，不得编造数字。

## 第二步：促销真实性核查（用 browser 查历史价格）
1. https://camelcamelcamel.com/search?search=${encoded} → Amazon 历史最低/均价/是否促销前涨价
2. 在步骤1的 smzdm 商品详情页查看"价格走势图"和"历史低价"
判断：当前价 vs 近90天均价，是否真实低位，是否有先涨后降迹象

## 第三步：评价提炼
- 搜索「${product} 评价」「${product} 使用体验」「${product} 踩坑」
- 从真实用户反馈中提炼：
  ✅ 3个核心优点
  ❌ 3个主要槽点或质量问题
  👤 适合人群 vs 不适合人群
  🚩 红旗警告（若有质量投诉、虚假宣传等）

## 第四步：替代品推荐
- 搜索「${product} 平替」「比 ${product} 更好的」「${product} 竞品」
- 推荐 2-3 个性价比更高或功能更好的替代品，含价格区间

## 第五步：购买时机建议
综合以上信息，给出明确结论：
- 🟢 立即购买：价格处于低位 + 评价良好 + 无更好替代
- 🟡 再等等：临近大促 / 价格有下降空间
- 🔴 不建议：质量问题多 / 有更好替代品 / 性价比低

---

## 输出格式

🛒 BuyWise · ${product}
━━━━━━━━━━━━━━━━━━━━━━━
📊 各平台比价
[价格对比表，含平台、价格、差价]

🔍 促销真实性
[历史价格分析，真优惠 or 假折扣]

⭐ 评价摘要
✅ 优点 | ❌ 槽点 | 👤 适合人群

🔄 替代品推荐
[2-3个替代选项，含价格]

✅ 购买建议
[🟢/🟡/🔴 + 1-2句理由 + 最推荐购买渠道]

🎟️ 优惠券 & 返利
在确认购买前，运行 CouponClaw 查找可用券码和返利叠加方案：
  openclaw run couponclaw find "${product}" --region all
可额外节省的金额请补充到"实际到手价"中。
━━━━━━━━━━━━━━━━━━━━━━━
💡 回复"详细评价"深度分析口碑 · 回复"比价 XX"单独查某平台 · 回复"找券"调用 CouponClaw`);

} else {
  console.log(`Please provide a comprehensive buying decision analysis for: "${product}"
Date: ${dateISO}${promoHint}

## Step 1: Cross-Platform Price Comparison (use browser — do NOT guess prices via web_search)
Open each URL with the browser tool and extract prices directly from the page:
1. https://search.smzdm.com/?c=home&s=${encoded}&v=b → aggregated JD/Taobao/Tmall/Pinduoduo prices in one page
2. https://search.jd.com/Search?keyword=${encoded}&enc=utf-8 → JD direct, first self-operated listing
3. https://www.google.com/search?q=${encoded}&tbm=shop → Google Shopping: aggregates Amazon, eBay, Walmart, Best Buy and dozens more — extract price range and lowest retailer
4. If Google Shopping unavailable → fallback https://www.bing.com/shop?q=${encoded}
5. https://www.amazon.com/s?k=${encoded} → cross-verify Amazon price against Google Shopping
6. https://www.aliexpress.com/wholesale?SearchText=${encoded} → AliExpress top 3 prices
7. web_search "${product} Temu price" → Temu supplement (no standard search URL)
8. web_search "${product} used price" → second-hand reference

⚠️ Rule: only record prices actually read from the page. Mark "unavailable" if a page fails — never invent prices.

## Step 2: Deal Authenticity Check (use browser for real price history)
1. https://camelcamelcamel.com/search?search=${encoded} → Amazon all-time low, 90-day average, pre-sale spike detection
2. In the smzdm product detail page from Step 1, check the price history chart and lowest-ever price
Assess: current price vs 90-day average; genuine low or inflate-then-discount pattern?

## Step 3: Review Analysis
- Search "${product} reviews" "${product} problems" "${product} honest review"
- Extract from real user feedback:
  ✅ 3 core strengths
  ❌ 3 main complaints or quality issues
  👤 Who it's great for vs. who should avoid it
  🚩 Red flags (quality complaints, misleading claims, etc.)

## Step 4: Alternatives
- Search "alternatives to ${product}" "${product} competitors" "better than ${product}"
- Recommend 2-3 alternatives with better value or features, including price range

## Step 5: Buy Timing Recommendation
Synthesize everything into a clear verdict:
- 🟢 Buy now: price is at/near low + good reviews + no better alternative
- 🟡 Wait: near a major sale / price likely to drop
- 🔴 Skip: quality issues / better alternatives exist / poor value

---

## Output Format

🛒 BuyWise · ${product}
━━━━━━━━━━━━━━━━━━━━━━━
📊 Price Comparison
[Table: platform, price, price gap, shipping]

🔍 Deal Authenticity
[Historical price analysis: genuine deal or fake discount]

⭐ Review Summary
✅ Strengths | ❌ Complaints | 👤 Who it's for

🔄 Alternatives
[2-3 alternatives with prices]

✅ Buying Recommendation
[🟢/🟡/🔴 + 1-2 sentence rationale + best platform to buy]

🎟️ Coupons & Cashback
Before finalizing, run CouponClaw to find available promo codes and cashback stacking:
  openclaw run couponclaw find "${product}" --region all
Add any additional savings to the final "effective price" above.
━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply "deep reviews" for in-depth reputation analysis · Reply "find coupons" to run CouponClaw`);
}
