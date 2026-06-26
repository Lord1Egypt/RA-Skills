#!/usr/bin/env node
'use strict';
/**
 * CouponClaw — 主入口：查询商品或店铺的优惠券 + 返利叠加策略
 * 用法: node scripts/find.js <商品名或店铺名> [--region cn|us|uk|au|sea|all] [--lang zh|en]
 */

const ALLOWED_REGIONS = new Set(['cn', 'us', 'uk', 'au', 'sea', 'all']);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const regionIdx = args.indexOf('--region');
const rawRegion = regionIdx !== -1 ? args[regionIdx + 1] : 'all';
const region = ALLOWED_REGIONS.has(rawRegion) ? rawRegion : 'all';
const queryArgs = args.filter((a, i) => {
  if (['--lang', '--region'].includes(a)) return false;
  if (['--lang', '--region'].includes(args[i - 1])) return false;
  return true;
});
const query = queryArgs.join(' ').trim();

if (!query) {
  console.error(lang === 'zh'
    ? '用法: node scripts/find.js <商品或店铺> [--region cn|us|uk|au|sea|all] [--lang zh|en]'
    : 'Usage: node scripts/find.js <product or store> [--region cn|us|uk|au|sea|all] [--lang zh|en]');
  return;
}

const encoded = encodeURIComponent(query);

// ── 区域数据源配置 ──────────────────────────────────────────────────────────
const sources = {
  cn: [
    { label: '什么值得买优惠券专区', url: `https://search.smzdm.com/?c=home&s=${encoded}&v=b`, note: '筛选"优惠券"标签，提取券码、面额、有效期、适用商品' },
    { label: '京东领券中心', url: `https://coupon.jd.com/`, note: '搜索「${query}」相关优惠券，提取可领取的券面额和使用门槛' },
    { label: '淘宝聚划算', url: `https://ju.taobao.com/jusp/index.html?spm=a21bo.jianhua.201867-main.1.5af911d9mZFx5p&keyword=${encoded}`, note: '提取限时折扣和专属优惠' },
    { label: '折800', url: `https://www.zhe800.com/search?keyword=${encoded}`, note: '提取优惠码和返利信息' },
  ],
  us: [
    { label: 'RetailMeNot', url: `https://www.retailmenot.com/search#query=${encoded}`, note: '提取验证通过的优惠码、折扣幅度、到期时间、成功率' },
    { label: 'Slickdeals', url: `https://slickdeals.net/newsearch.php?q=${encoded}&searchin=first&sort=newest`, note: '从社区验证热门优惠中提取当前有效的券和折扣' },
    { label: 'Amazon Coupons', url: `https://www.amazon.com/coupons#search=${encoded}`, note: '提取可直接 clip 的 Amazon 官方券，标注节省金额' },
    { label: 'Dealmoon (华人专区)', url: `https://www.dealmoon.com/search?q=${encoded}`, note: '提取北美华人社区精选优惠，标注是否仍有效' },
  ],
  uk: [
    { label: 'VoucherCodes UK', url: `https://www.vouchercodes.co.uk/search/?q=${encoded}`, note: '提取券码、折扣幅度、到期日' },
    { label: 'HotUKDeals', url: `https://www.hotukdeals.com/search?q=${encoded}&type=deals`, note: '社区热帖中的最新折扣，提取温度值（热度）和链接' },
    { label: 'MyVoucherCodes UK', url: `https://www.myvouchercodes.co.uk/search?q=${encoded}`, note: '补充验证英国券码' },
  ],
  au: [
    { label: 'OzBargain', url: `https://www.ozbargain.com.au/search?q=${encoded}&action=search`, note: '提取澳洲社区验证优惠，标注是否有效及过期时间' },
    { label: 'Cashrewards AU', url: `https://www.cashrewards.com.au/stores?q=${encoded}`, note: '提取澳洲返利比例' },
  ],
  sea: [
    { label: 'ShopBack', url: `https://www.shopback.com/search?q=${encoded}`, note: '提取新加坡/马来/泰/菲/印尼返利比例和优惠' },
    { label: 'iPrice', url: `https://iprice.my/search/?q=${encoded}`, note: '东南亚价格+优惠聚合' },
  ],
};

// 选择要查的区域
let activeSources = [];
if (region === 'all') {
  activeSources = [...sources.cn, ...sources.us, ...sources.uk, ...sources.au, ...sources.sea];
} else {
  activeSources = sources[region] || [];
}

// 返利平台（全局叠加）
const cashbackSources = region === 'cn' ? [
  { label: '返利网', url: `https://www.fanli.com/search?q=${encoded}` },
  { label: '什么值得买返利', url: `https://search.smzdm.com/?c=home&s=${encoded}&v=b` },
] : [
  { label: 'Rakuten (US/UK/JP)', url: `https://www.rakuten.com/search?q=${encoded}` },
  { label: 'TopCashback', url: `https://www.topcashback.co.uk/search/?searchInput=${encoded}` },
  { label: 'ShopBack (SEA/AU)', url: `https://www.shopback.com/search?q=${encoded}` },
];

// DTC 品牌检测提示
const dtcHint = `如「${query}」是品牌官网直销（DTC）商品，额外执行：
- 搜索 [商品名] site:retailmenot.com OR site:slickdeals.net coupon code 获取品牌专属券码
- browser 导航品牌官网首页，检查是否有订阅弹窗优惠（通常首单 10-15% off）或顶部 banner 促销
- 搜索 [商品名] first order discount newsletter signup`;

if (lang === 'zh') {
  const sourceList = activeSources.map((s, i) =>
    `${i + 1}. 打开 ${s.url}\n   → ${s.label}：${s.note}`
  ).join('\n\n');

  const cashbackList = cashbackSources.map((s, i) =>
    `${activeSources.length + i + 1}. 打开 ${s.url}\n   → ${s.label}：查询该商品/商家的返利比例`
  ).join('\n\n');

  console.log(`请为「${query}」查找所有可用优惠券，并制定最优叠加省钱方案。

使用 browser 工具依次导航以下页面，直接从页面提取真实有效的券码和折扣信息。

═══ 第一层：优惠券查询 ═══

${sourceList}

═══ 第二层：返利叠加查询 ═══

${cashbackList}

═══ 第三层：DTC 品牌检测 ═══

${dtcHint}

提取规则：
- 只记录**当前有效**的券码（标注到期时间；若已过期，标注"已过期"不列入推荐）
- 注明每个券的：券码（若有）、面额/折扣幅度、使用门槛、到期时间、来源平台
- 某页面无法访问则标"无法获取"，不得编造券码
- 无券码的平台折扣（如直接打折）也列出，标注"无需码/直接享"

输出格式：

🎟️ CouponClaw · ${query}
━━━━━━━━━━━━━━━━━━━━━━━
🏷️ 可用券码 & 折扣

[按节省金额从高到低排列]
① [来源] 券码: XXXXXX | 满¥/$ XX 减¥/$ XX | 到期: XXXX-XX-XX | ✅有效
② [来源] 券码: XXXXXX | X折 / X% off | 到期: XXXX-XX-XX | ✅有效
③ ...

💰 返利叠加
[平台] 返利比例 X% / 返¥XXX（可与以上券码叠加 ✅ / 不可叠加 ❌）

🔢 最优叠加方案
用券 ① + [返利平台] 返利 = 实际节省 ¥/$ XXX（原价 ¥/$ XXX → 到手价 ¥/$ XXX）

📌 数据来源：${activeSources.map(s => s.label).join(' / ')}
━━━━━━━━━━━━━━━━━━━━━━━
💡 回复"每日优惠"订阅每日推送 · 回复"比价"跳转 BuyWise 查最低价`);

} else {
  const sourceList = activeSources.map((s, i) =>
    `${i + 1}. Open ${s.url}\n   → ${s.label}: ${s.note}`
  ).join('\n\n');

  const cashbackList = cashbackSources.map((s, i) =>
    `${activeSources.length + i + 1}. Open ${s.url}\n   → ${s.label}: find cashback rate for this merchant`
  ).join('\n\n');

  console.log(`Please find all available coupons for "${query}" and recommend the best stacking strategy.

Use the browser tool to navigate each page below and extract real, currently-valid coupons.

═══ Layer 1: Coupon Search ═══

${sourceList}

═══ Layer 2: Cashback Stacking ═══

${cashbackList}

═══ Layer 3: DTC Brand Check ═══

If "${query}" is a DTC brand:
- Search: [product name] site:retailmenot.com OR site:slickdeals.net coupon code
- browser navigate to brand's official homepage, check for signup popup offer (usually 10-15% off first order) or banner promotions
- Search: [product name] first order discount newsletter signup

Extraction rules:
- Only record **currently valid** coupons (note expiry; mark expired ones as such — do not recommend them)
- For each coupon: code (if any), discount amount/%, minimum spend, expiry date, source
- Mark "unavailable" if a page fails to load — never fabricate coupon codes
- Platform-wide sales with no code (auto-applied) should also be listed as "no code needed"

Output format:

🎟️ CouponClaw · ${query}
━━━━━━━━━━━━━━━━━━━━━━━
🏷️ Available Coupons & Deals

[sorted by savings, highest first]
① [Source] Code: XXXXXX | $XX off $XX+ | Expires: XXXX-XX-XX | ✅ Valid
② [Source] Code: XXXXXX | X% off | Expires: XXXX-XX-XX | ✅ Valid
③ ...

💰 Cashback Stacking
[Platform] X% cashback / $XXX back (stackable with above codes ✅ / not stackable ❌)

🔢 Best Stacking Strategy
Code ① + [cashback platform] = total saving $XXX (original $XXX → final price $XXX)

📌 Sources: ${activeSources.map(s => s.label).join(' / ')}
━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply "daily deals" to subscribe · Reply "compare prices" to jump to BuyWise`);
}
