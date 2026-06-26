#!/usr/bin/env node
'use strict';
/**
 * CouponClaw — 返利叠加查询
 * 查询某商家在主流返利平台的返利比例，计算叠加后实际到手价
 * 用法: node scripts/cashback.js <商家名> [--spend 消费金额] [--lang zh|en]
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const spendIdx = args.indexOf('--spend');
const spend = spendIdx !== -1 ? parseFloat(args[spendIdx + 1]) : null;
const storeArgs = args.filter((a, i) => {
  if (['--lang', '--spend'].includes(a)) return false;
  if (['--lang', '--spend'].includes(args[i - 1])) return false;
  return true;
});
const store = storeArgs.join(' ').trim();

if (!store) {
  console.error(lang === 'zh'
    ? '用法: node scripts/cashback.js <商家名> [--spend 金额] [--lang zh|en]'
    : 'Usage: node scripts/cashback.js <store> [--spend amount] [--lang zh|en]');
  return;
}

const encoded = encodeURIComponent(store);
const spendNote = spend
  ? (lang === 'zh' ? `\n消费金额：¥/$ ${spend}，请据此计算各平台实际返利金额。` : `\nSpend amount: $${spend} — calculate actual cashback amount for each platform.`)
  : '';

if (lang === 'zh') {
  console.log(`请查询「${store}」在各大返利平台的返利比例，并计算最优叠加方案。${spendNote}

使用 browser 工具导航以下页面：

【中国市场返利】
1. 打开 https://www.fanli.com/search?q=${encoded}
   → 返利网：提取该商家的返利比例（%）和单笔封顶金额
2. 打开 https://search.smzdm.com/?c=home&s=${encoded}&v=b
   → 什么值得买返利：提取返利率和活动说明

【国际市场返利】
3. 打开 https://www.rakuten.com/search?q=${encoded}
   → Rakuten（美/英/日）：提取返利比例，注意是否有提现门槛
4. 打开 https://www.topcashback.co.uk/search/?searchInput=${encoded}
   → TopCashback（英/美）：提取该商家最高返利比例
5. 打开 https://www.shopback.com/search?q=${encoded}
   → ShopBack（新加坡/马来/泰/印尼/澳洲）：提取各国返利比例

【叠加提示】
- 大多数返利平台可与优惠券码叠加（先用券，再通过返利平台入口下单）
- 信用卡积分/返现可在上述两层之上再叠加（提醒用户选择合适的信用卡）
- 注意：部分平台规定"使用优惠码不享受返利"，需单独标注

输出格式：
💰 CouponClaw · ${store} 返利查询
━━━━━━━━━━━━━━━━━━━━━━━
平台           | 返利比例 | 可叠加券码 | 备注
返利网         | X%       | ✅/❌      |
什么值得买     | X%       | ✅/❌      |
Rakuten        | X%       | ✅/❌      | 美/英/日
TopCashback    | X%       | ✅/❌      |
ShopBack       | X%       | ✅/❌      | 东南亚/澳洲

🔢 最优叠加方案${spend ? `（消费 ¥/$ ${spend}）` : ''}
优惠券节省：¥/$ XXX
+ 返利收入：¥/$ XXX（通过 [最高返利平台] 下单）
+ 信用卡返现：¥/$ XXX（建议使用 [适合该平台的卡]）
= 综合节省：¥/$ XXX（折合 X 折 / X% off）
━━━━━━━━━━━━━━━━━━━━━━━`);

} else {
  console.log(`Please look up cashback rates for "${store}" across major cashback platforms and calculate the best stacking strategy.${spendNote}

Use the browser tool to navigate each page:

[China cashback]
1. Open https://www.fanli.com/search?q=${encoded}
   → Fanli.com: extract cashback rate (%) and per-order cap
2. Open https://search.smzdm.com/?c=home&s=${encoded}&v=b
   → smzdm cashback: extract rate and promotion notes

[International cashback]
3. Open https://www.rakuten.com/search?q=${encoded}
   → Rakuten (US/UK/JP): extract cashback rate; note minimum payout threshold
4. Open https://www.topcashback.co.uk/search/?searchInput=${encoded}
   → TopCashback (UK/US): extract highest available cashback rate
5. Open https://www.shopback.com/search?q=${encoded}
   → ShopBack (SG/MY/TH/ID/AU): extract rates by country

[Stacking notes]
- Most cashback platforms stack with coupon codes (use code first, then click through cashback portal)
- Credit card rewards can stack on top of both layers — suggest a suitable card
- Flag any platforms where "using a promo code voids cashback"

Output format:
💰 CouponClaw · ${store} Cashback Lookup
━━━━━━━━━━━━━━━━━━━━━━━
Platform       | Rate  | Stackable | Notes
Fanli (CN)     | X%    | ✅/❌     |
smzdm (CN)     | X%    | ✅/❌     |
Rakuten        | X%    | ✅/❌     | US/UK/JP
TopCashback    | X%    | ✅/❌     |
ShopBack       | X%    | ✅/❌     | SEA/AU

🔢 Best stacking strategy${spend ? ` (spend: $${spend})` : ''}
Coupon savings:  $XXX
+ Cashback:      $XXX (via [highest-rate platform])
+ Card rewards:  $XXX (recommended: [suitable card])
= Total saving:  $XXX (effective X% off)
━━━━━━━━━━━━━━━━━━━━━━━`);
}
