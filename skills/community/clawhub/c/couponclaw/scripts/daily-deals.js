#!/usr/bin/env node
'use strict';
/**
 * CouponClaw — 每日热门优惠推送
 * 由 openclaw cron 驱动，每日早晨执行
 * 用法: node scripts/daily-deals.js [--region cn|us|uk|au|sea|all] [--lang zh|en]
 */

const ALLOWED_REGIONS = new Set(['cn', 'us', 'uk', 'au', 'sea', 'all']);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const regionIdx = args.indexOf('--region');
const rawRegion = regionIdx !== -1 ? args[regionIdx + 1] : 'all';
const region = ALLOWED_REGIONS.has(rawRegion) ? rawRegion : 'all';

const now = new Date();
const WEEKDAYS_ZH = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
const WEEKDAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const dateZH = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS_ZH[now.getDay()]}`;
const dateEN = `${WEEKDAYS_EN[now.getDay()]}, ${MONTHS_EN[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;

// 按区域配置今日热门优惠来源
const dealSources = {
  cn: [
    { label: '什么值得买今日热门', url: 'https://www.smzdm.com/', note: '首页"今日最热"板块，提取评论数最多的前5个优惠' },
    { label: '什么值得买优惠券', url: 'https://www.smzdm.com/fenlei/youhuiquan/', note: '今日新上优惠券，取前5条，标注来源平台和有效期' },
    { label: '京东秒杀', url: 'https://miaosha.jd.com/', note: '提取今日限时秒杀中折扣力度最大的3-5个商品' },
  ],
  us: [
    { label: 'Slickdeals Frontpage', url: 'https://slickdeals.net/', note: 'frontpage 热门优惠，提取当前投票数最高的前5个' },
    { label: 'Dealmoon', url: 'https://www.dealmoon.com/', note: '华人社区精选，提取编辑推荐的前3-5个优惠' },
    { label: 'DealNews', url: 'https://dealnews.com/', note: '编辑精选今日最值优惠，提取前3条' },
  ],
  uk: [
    { label: 'HotUKDeals', url: 'https://www.hotukdeals.com/', note: '英国社区热帖，提取温度值最高的前5个优惠' },
  ],
  au: [
    { label: 'OzBargain', url: 'https://www.ozbargain.com.au/', note: '澳洲社区热帖，提取投票数最高的前5个优惠' },
  ],
  sea: [
    { label: 'ShopBack 今日优惠', url: 'https://www.shopback.com/all-deals', note: '东南亚今日精选优惠，提取前5条' },
  ],
};

const activeSources = region === 'all'
  ? Object.values(dealSources).flat()
  : (dealSources[region] || []);

if (lang === 'zh') {
  const sourceList = activeSources.map((s, i) =>
    `${i + 1}. 打开 ${s.url}\n   → ${s.label}：${s.note}`
  ).join('\n\n');

  console.log(`请抓取今日全球热门优惠，生成每日优惠简报。
当前日期：${dateZH}

使用 browser 工具导航以下页面，提取真实有效的今日热门优惠：

${sourceList}

整理规则：
- 共选取 8-10 条今日最值优惠，覆盖不同品类
- 每条含：商品/品牌、折扣幅度或券码、原价→现价、来源平台、有效期（若有）
- 优先标注：限时抢购（今日截止）、隐藏券、叠加返利机会
- 已过期或库存售罄的优惠不列入

输出格式：
🎟️ CouponClaw · 今日优惠 · ${dateZH}
━━━━━━━━━━━━━━━━━━━━━━━

🇨🇳 国内热门
[条目：商品 | 折扣 | 券码（若有）| 平台 | ⏰截止时间]

🌍 海外热门
[条目：商品 | 折扣 | 券码（若有）| 平台 | ⏰截止时间]

💎 今日最值 TOP 3
① [最值优惠，附简短理由]
② ...
③ ...

━━━━━━━━━━━━━━━━━━━━━━━
💡 回复商品名查专属券 · 回复"比价"跳转 BuyWise`);

} else {
  const sourceList = activeSources.map((s, i) =>
    `${i + 1}. Open ${s.url}\n   → ${s.label}: ${s.note}`
  ).join('\n\n');

  console.log(`Please fetch today's top deals and generate a daily deals briefing.
Date: ${dateEN}

Use the browser tool to navigate each page below and extract real, currently-valid hot deals:

${sourceList}

Rules:
- Select 8-10 best deals of the day across different categories
- Each entry: product/brand, discount amount or promo code, original → current price, platform, expiry (if applicable)
- Highlight: today-only flash sales, hidden coupons, stackable cashback opportunities
- Do not include expired or sold-out deals

Output format:
🎟️ CouponClaw · Daily Deals · ${dateEN}
━━━━━━━━━━━━━━━━━━━━━━━

🇨🇳 China Deals
[item: product | discount | code (if any) | platform | ⏰ expires]

🌍 International Deals
[item: product | discount | code (if any) | platform | ⏰ expires]

💎 Today's Top 3 Picks
① [best deal with brief reason]
② ...
③ ...

━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply with a product name to find its coupons · Reply "compare" to jump to BuyWise`);
}
