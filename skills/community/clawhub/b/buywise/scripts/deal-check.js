#!/usr/bin/env node
'use strict';
/**
 * BuyWise — 促销真实性核查
 * 用 browser 导航到历史价格追踪站点，获取真实历史价格数据
 * 用法: node scripts/deal-check.js <商品名> [--price 当前价格] [--was 标称原价] [--lang zh|en]
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';

const priceIdx = args.indexOf('--price');
const price = priceIdx !== -1 ? args[priceIdx + 1] : null;

const wasIdx = args.indexOf('--was');
const was = wasIdx !== -1 ? args[wasIdx + 1] : null;

const productArgs = args.filter((a, i) => {
  if (['--lang','--price','--was'].includes(a)) return false;
  if (['--lang','--price','--was'].includes(args[i - 1])) return false;
  return true;
});
const product = productArgs.join(' ').trim();

if (!product) {
  console.error(lang === 'zh' ? '用法: node scripts/deal-check.js <商品名> [--price 299] [--was 599]' : 'Usage: node scripts/deal-check.js <product> [--price 299] [--was 599]');
  process.exit(1);
}

const encoded = encodeURIComponent(product);
const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const priceContext = price
  ? (lang === 'zh' ? `当前促销价：¥${price}${was ? `，标称原价：¥${was}，折扣幅度：${Math.round((1 - price/was)*100)}%` : ''}` : `Current price: $${price}${was ? `, claimed was: $${was}, discount: ${Math.round((1 - price/was)*100)}%` : ''}`)
  : '';

if (lang === 'zh') {
  console.log(`请核查「${product}」的促销是否真实。${priceContext ? '\n' + priceContext : ''}
当前日期：${dateISO}

使用 browser 工具导航以下页面，获取真实历史价格数据：

【中国市场 — 历史价格】
1. 打开 https://search.smzdm.com/?c=home&s=${encoded}&v=b
   → 从什么值得买搜索结果中找到该商品，点击商品进入详情，查看"历史低价""价格走势图"
   → 记录：当前价格、历史最低价、近30/90天价格趋势
2. web_search「${product} 历史最低价 site:smzdm.com OR site:camelcamelcamel.com」
   → 补充获取价格区间参考

【Amazon 历史价格（若适用）】
3. 打开 https://camelcamelcamel.com/search?search=${encoded}
   → CamelCamelCamel 是 Amazon 专业价格追踪站，从页面提取：
     - Amazon 历史最低价 / 最高价 / 当前价
     - 90天价格走势
     - 是否"先涨后降"（图表中促销前有明显价格抬高）

【判断标准】
根据获取的历史数据判断：
- ✅ 真实优惠：当前价格 ≤ 近90天均价的 90%，且无促销前涨价迹象
- ⚠️ 轻微注水：当前价格比均价低 0-10%，折扣幅度被夸大
- ❌ 假折扣：促销前1-4周内有明显涨价，实际折扣 < 标称折扣的 50%

【大促节点参考】
- 双11：每年11月1-11日（预售10月）
- 618：每年6月1-18日（预售5月）
- 38女王节：3月8-15日
- 双12：12月12日

输出格式：
🔍 促销核查 · ${product}
━━━━━━━━━━━━━━━━━━━━━━━
${priceContext || '当前价格：请提供以便分析'}
历史最低价：¥XXX（XXXX-XX，来源: smzdm/CamelCamelCamel）
近90天均价：¥XXX
当前价格位置：历史低位 / 中等 / 偏高
促销真实性：✅ 真实优惠 / ⚠️ 轻微注水 / ❌ 假折扣
判断依据：[1-2句说明，引用具体历史价格数据]

📅 购买时机建议：
- 立即：[是/否，理由]
- 下次大促：预计 XXXX年XX月，届时预计 ¥XXX

🎟️ 如果决定立即购买，运行 CouponClaw 叠加优惠券和返利：
  openclaw run couponclaw find "${product}" --region all
━━━━━━━━━━━━━━━━━━━━━━━`);

} else {
  console.log(`Please verify whether the deal on "${product}" is genuine.${priceContext ? '\n' + priceContext : ''}
Date: ${dateISO}

Use the browser tool to navigate to these pages for real historical price data — do not guess:

[Amazon price history]
1. Open https://camelcamelcamel.com/search?search=${encoded}
   → CamelCamelCamel tracks Amazon prices. Extract:
     - All-time low / high / current price on Amazon
     - 90-day price trend
     - Whether there was a pre-sale price spike (visible in the chart)

[International shopping trends]
2. Open https://www.amazon.com/s?k=${encoded}
   → Check current Amazon price and compare to CamelCamelCamel data.
3. web_search "${product} price history Black Friday Prime Day discount"
   → Supplement with seasonal pricing context.

[Verdict criteria]
Based on the historical data:
- ✅ Genuine deal: current price ≤ 90% of 90-day average, no pre-sale price spike
- ⚠️ Slightly inflated: marginal discount (0-10% below average), overstated savings claim
- ❌ Fake discount: price was raised 1-4 weeks before sale; real discount < 50% of claimed

Output format:
🔍 Deal Check · ${product}
━━━━━━━━━━━━━━━━━━━━━━━
${priceContext || 'Current price: please provide for analysis'}
All-time low: $XXX (XXXX-XX, source: CamelCamelCamel)
90-day average: $XXX
Current price position: near low / mid / high
Verdict: ✅ Genuine deal / ⚠️ Slightly inflated / ❌ Fake discount
Evidence: [1-2 sentences citing actual historical price data]

📅 Buy timing:
- Now: [yes/no, reason]
- Next major sale: approx. XXXX-XX, expected price $XXX

🎟️ If buying now, run CouponClaw to stack coupons and cashback:
  openclaw run couponclaw find "${product}" --region all
━━━━━━━━━━━━━━━━━━━━━━━`);
}
