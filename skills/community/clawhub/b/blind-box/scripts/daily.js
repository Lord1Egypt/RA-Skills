#!/usr/bin/env node
/**
 * blind-box daily — one free pull per day, themed to today's date
 * Usage: node daily.js [--lang zh|en]
 */

const lang = process.argv.includes('--lang')
  ? process.argv[process.argv.indexOf('--lang') + 1]
  : 'zh';

const now   = new Date();
const today = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const seed  = now.getFullYear() * 10000 + (now.getMonth()+1) * 100 + now.getDate();
const isZh  = lang === 'zh';

// Date-based lucky series (rotate by day of week)
const daySeries = ['cat','space','food','spirit','wuxia','cat','space'];
const todaySeries = daySeries[now.getDay()];

const dayNames_zh = ['周日','周一','周二','周三','周四','周五','周六'];
const dayNames_en = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

// Bump daily rarity (daily pulls are slightly luckier)
const DAILY_RARITY = [
  { name_zh: '限定款 ✦✦', name_en: 'Limited ✦✦',   color: '🔴', threshold: 0.008 },
  { name_zh: '隐藏款 ✦',  name_en: 'Hidden ✦',     color: '🟣', threshold: 0.030 },
  { name_zh: '史诗款 ★★★',name_en: 'Epic ★★★',     color: '🟠', threshold: 0.100 },
  { name_zh: '超稀有 ★★', name_en: 'Super Rare ★★', color: '🟡', threshold: 0.250 },
  { name_zh: '稀有款 ★',  name_en: 'Rare ★',        color: '🔵', threshold: 0.500 },
  { name_zh: '普通款',    name_en: 'Common',         color: '⚪', threshold: 1.000 },
];

function lcg(s) {
  return Math.abs(((s * 1664525 + 1013904223) & 0x7fffffff)) / 0x7fffffff;
}

const r = lcg(seed);
const rarity = DAILY_RARITY.find(t => r < t.threshold) || DAILY_RARITY[DAILY_RARITY.length-1];

console.log(`
${isZh
  ? `🎁 每日盲盒 — ${today} ${dayNames_zh[now.getDay()]}`
  : `🎁 Daily Blind Box — ${today} ${dayNames_en[now.getDay()]}`
}
${'═'.repeat(50)}

${isZh
  ? `今日主题系列：${['🐱 猫咪日常','🚀 宇宙探险','🍜 美食精灵','🌸 四季精灵','⚔️ 古风仙侠','🐱 猫咪日常','🚀 宇宙探险'][now.getDay()]}`
  : `Today's series: ${['🐱 Daily Cat','🚀 Space Explorer','🍜 Food Spirit','🌸 Season Spirit','⚔️ Wuxia','🐱 Daily Cat','🚀 Space Explorer'][now.getDay()]}`
}
${isZh ? '每日一次免费抽取，明天可再抽！' : 'One free pull per day — come back tomorrow!'}

DAILY PULL INSTRUCTIONS FOR AI:
  Date:         ${today}
  Day seed:     ${seed}
  Series:       ${todaySeries}
  Rarity roll:  ${r.toFixed(4)}
  Result:       ${isZh ? rarity.name_zh : rarity.name_en} ${rarity.color}
  Language:     ${lang}

${isZh ? `
呈现方式：
1. 先显示"🎁 今日盲盒正在开启..." 的期待感文字（2-3行）
2. 显示今日日期和星期对应的特别祝福语
3. 揭晓盲盒，使用上方稀有度结果
4. 根据稀有度给出今日运气评价：
   - 普通款：今天是平平无奇的幸运日，稳稳的幸福 🍀
   - 稀有款：今天运气不错！✨ 适合做决定
   - 超稀有：今天超级幸运！🌟 大事可成
   - 史诗款：今天是史诗级幸运日！🔥 冲冲冲
   - 隐藏款：隐藏款降临！🌙 今天必有好事发生！
   - 限定款：宇宙级幸运！🎆 买彩票去！！
5. 最后附上分享语："我今天的每日盲盒是 [名字] [稀有度]！ #每日盲盒"
` : `
Presentation:
1. Show opening suspense text "🎁 Opening today's blind box..."
2. Show today's special blessing based on day of week
3. Reveal the box with the rarity above
4. Add luck reading based on rarity:
   - Common: A calm and steady lucky day 🍀
   - Rare: Pretty lucky today! ✨ Good for decisions
   - Super Rare: Super lucky day! 🌟 Go for it
   - Epic: Epic luck! 🔥 Nothing can stop you
   - Hidden: Hidden edition! 🌙 Something good is coming!
   - Limited: Universe-level luck! 🎆 Play the lottery!!
5. End with: "Today's blind box: [name] [rarity]! #DailyBlindBox"
`}

Generate the full daily blind box reveal experience now!
`);
