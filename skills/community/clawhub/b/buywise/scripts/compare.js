#!/usr/bin/env node
'use strict';
/**
 * BuyWise — 多平台比价
 * 使用 browser 工具导航到真实比价页，不依赖 web_search 盲猜价格
 * 用法: node scripts/compare.js <商品名> [--lang zh|en]
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const productArgs = args.filter((a, i) => a !== '--lang' && args[i - 1] !== '--lang');
const product = productArgs.join(' ').trim();

if (!product) {
  console.error(lang === 'zh' ? '用法: node scripts/compare.js <商品名>' : 'Usage: node scripts/compare.js <product>');
  process.exit(1);
}

const encoded = encodeURIComponent(product);

if (lang === 'zh') {
  console.log(`请对「${product}」进行真实价格比对。使用 browser 工具依次导航以下 URL，从页面直接提取价格，不要用 web_search 猜测价格。

【中国市场 — 一站聚合】
1. 打开 https://search.smzdm.com/?c=home&s=${encoded}&v=b
   → 什么值得买已聚合京东/淘宝/天猫/拼多多价格，直接从页面提取各平台最低价和商品标题。

【中国市场 — 补充直查】
2. 打开 https://search.jd.com/Search?keyword=${encoded}&enc=utf-8
   → 从京东搜索结果提取价格（第一屏自营商品优先）。
3. 如商品在京东有自营链接，可进入商品详情页获取精确价格。

【国际市场 — Google Shopping 一站聚合】
4. 打开 https://www.google.com/search?q=${encoded}&tbm=shop
   → Google 购物页面聚合 Amazon、eBay、Walmart、Best Buy 等几十家零售商真实价格，
   → 从结果列表提取：商品名、各零售商价格、是否包邮。这是国际市场最高效的单一来源。
5. 如 Google 购物无法访问，备用：打开 https://www.bing.com/shop?q=${encoded}
   → Bing 购物同样聚合多家零售商，效果类似。

【国际市场 — 专项直查】
6. 打开 https://www.amazon.com/s?k=${encoded}
   → 从 Amazon 搜索结果提取前3条价格（含 Prime 标识），与 Google Shopping 数据交叉验证。
7. 打开 https://www.aliexpress.com/wholesale?SearchText=${encoded}
   → 从 AliExpress 提取前3条价格（美元），AliExpress 通常比 Amazon/eBay 便宜。
8. web_search「${product} Temu price」— Temu 无标准搜索 URL，用搜索补充。

【二手】
9. web_search「${product} 闲鱼 成色好 价格」— 获取二手参考价。

提取规则：
- 只取有明确数字的价格，不要写"价格不详"或编造数字
- 如某平台页面无法访问或加载失败，标注"无法获取"而非填假数据
- 价格含税含运费（若可判断）
- Google Shopping 结果中同一商品多家零售商报价，取最低价和最高价区间

输出格式：
🛒 ${product} · 全平台比价
━━━━━━━━━━━━━━━━━━━━━━━
平台          | 价格         | 包邮 | 来源
京东(自营)    | ¥XXX        | ✓   | smzdm / 京东直查
淘宝/天猫     | ¥XXX        | -   | smzdm
拼多多        | ¥XXX        | ✓   | smzdm
──────────────────────────────────
Google Shopping| $XXX~$XXX  | -   | 多家零售商区间
Amazon        | $XXX        | -   | Google Shopping / 直查
eBay          | $XXX        | -   | Google Shopping
Walmart/其他  | $XXX        | -   | Google Shopping
AliExpress    | $XXX        | -   | 直查
Temu          | $XXX        | -   | 搜索
──────────────────────────────────
闲鱼(二手)    | ¥XXX        | 协议 | 搜索
━━━━━━━━━━━━━━━━━━━━━━━
💰 全球最低价：[平台] ¥/$ XXX
💰 国内最低价：[平台] ¥XXX
💡 综合推荐：[综合价格+配送+保障的最佳选择]
📌 数据来源：browser 直取（smzdm / Google Shopping / Amazon / AliExpress）+ 搜索补充（Temu / 闲鱼）`);

} else {
  console.log(`Please compare real prices for "${product}" across all major platforms. Use the browser tool to navigate to actual pricing pages — do NOT use web_search to guess prices.

[China market — aggregated]
1. Open https://search.smzdm.com/?c=home&s=${encoded}&v=b
   → smzdm.com already aggregates JD / Taobao / Tmall / Pinduoduo prices. Extract prices and product titles directly from the page.

[China market — direct check]
2. Open https://search.jd.com/Search?keyword=${encoded}&enc=utf-8
   → Extract price from the first JD official/self-operated listing.

[International — Google Shopping (single best source)]
3. Open https://www.google.com/search?q=${encoded}&tbm=shop
   → Google Shopping aggregates real prices from Amazon, eBay, Walmart, Best Buy, and dozens more.
   → Extract: retailer names, prices, shipping status. This covers most international retailers in one page.
4. If Google Shopping is inaccessible, fallback: open https://www.bing.com/shop?q=${encoded}
   → Bing Shopping provides similar multi-retailer aggregation.

[International — direct spot-check]
5. Open https://www.amazon.com/s?k=${encoded}
   → Verify Amazon price against Google Shopping data; note Prime eligibility.
6. Open https://www.aliexpress.com/wholesale?SearchText=${encoded}
   → AliExpress is typically cheapest for unbranded/generic items; extract top 3 prices.
7. web_search "${product} Temu price" — Temu has no standard search URL.

[Second-hand]
8. web_search "${product} used price good condition" — reference only.

Extraction rules:
- Only record prices actually read from the page; mark "unavailable" if a page fails — never invent prices
- For Google Shopping, note the price range (lowest to highest) across retailers
- Note whether price includes tax/shipping when determinable

Output format:
🛒 ${product} · Price Comparison
━━━━━━━━━━━━━━━━━━━━━━━
Platform        | Price      | Shipping | Source
JD (official)   | ¥XXX      | Free     | smzdm / direct
Taobao/Tmall    | ¥XXX      | -        | smzdm
Pinduoduo       | ¥XXX      | Free     | smzdm
────────────────────────────────────
Google Shopping | $XXX~$XXX | -        | multi-retailer range
Amazon          | $XXX      | -        | G.Shopping / direct
eBay            | $XXX      | -        | G.Shopping
Walmart/others  | $XXX      | -        | G.Shopping
AliExpress      | $XXX      | -        | direct
Temu            | $XXX      | -        | search
────────────────────────────────────
Used            | $XXX      | Varies   | search
━━━━━━━━━━━━━━━━━━━━━━━
💰 Global best price: [retailer] $XXX
💰 China best price: [platform] ¥XXX
💡 Best overall: [price + delivery + buyer protection]
📌 Sources: browser-direct (smzdm / Google Shopping / Amazon / AliExpress) + search (Temu / used)`);
}
