#!/usr/bin/env node
/**
 * blind-box pull — single or multi pull with rarity system
 * Usage: node pull.js [--series <name>] [--count <1|10>] [--lang zh|en]
 */

const args = process.argv.slice(2);
const getArg = (flag, def) => {
  const i = args.indexOf(flag);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
};

const series  = getArg('--series', 'random');
const count   = Math.min(parseInt(getArg('--count', '1'), 10) || 1, 10);
const lang    = getArg('--lang', 'zh');
const seed    = Date.now();

// Rarity table
const RARITY = [
  { name_zh: '限定款 ✦✦', name_en: 'Limited ✦✦',   color: '🔴', threshold: 0.005, pct: '0.5%'  },
  { name_zh: '隐藏款 ✦',  name_en: 'Hidden ✦',     color: '🟣', threshold: 0.020, pct: '1.5%'  },
  { name_zh: '史诗款 ★★★',name_en: 'Epic ★★★',     color: '🟠', threshold: 0.080, pct: '6%'    },
  { name_zh: '超稀有 ★★', name_en: 'Super Rare ★★', color: '🟡', threshold: 0.200, pct: '12%'   },
  { name_zh: '稀有款 ★',  name_en: 'Rare ★',        color: '🔵', threshold: 0.450, pct: '25%'   },
  { name_zh: '普通款',    name_en: 'Common',         color: '⚪', threshold: 1.000, pct: '55%'   },
];

// Series catalogue
const SERIES = {
  'cat':    { name_zh: '🐱 猫咪日常',   name_en: '🐱 Daily Cat',       total: 12, hidden: 2 },
  'space':  { name_zh: '🚀 宇宙探险',   name_en: '🚀 Space Explorer',  total: 10, hidden: 2 },
  'food':   { name_zh: '🍜 美食精灵',   name_en: '🍜 Food Spirit',     total: 10, hidden: 1 },
  'spirit': { name_zh: '🌸 四季精灵',   name_en: '🌸 Season Spirit',   total: 8,  hidden: 2 },
  'wuxia':  { name_zh: '⚔️ 古风仙侠',   name_en: '⚔️ Wuxia',          total: 12, hidden: 3 },
};

const seriesList = Object.keys(SERIES);

// Simple deterministic pseudo-random from seed (LCG)
function lcg(s) {
  return ((s * 1664525 + 1013904223) & 0x7fffffff) / 0x7fffffff;
}

function getRarity(r) {
  for (const tier of RARITY) {
    if (r < tier.threshold) return tier;
  }
  return RARITY[RARITY.length - 1];
}

const isZh = lang === 'zh';

console.log(`
You are running the blind-box pull skill. Follow these instructions EXACTLY to simulate a blind box gacha experience.

═══════════════════════════════════════════════════════
BLIND BOX PULL INSTRUCTIONS
═══════════════════════════════════════════════════════

PULL PARAMETERS:
  Seed:   ${seed}
  Count:  ${count} pull${count > 1 ? 's' : ''}
  Series: ${series === 'random' ? 'Random (pick one from list below)' : series}
  Lang:   ${lang}

AVAILABLE SERIES:
${Object.entries(SERIES).map(([k, v]) => `  ${k.padEnd(8)} — ${v.name_zh} / ${v.name_en}  (${v.total} figures, ${v.hidden} hidden)`).join('\n')}

RARITY TIERS (use these exact names and colors):
${RARITY.map(r => `  ${r.color} ${isZh ? r.name_zh : r.name_en}  (${r.pct})`).join('\n')}

PSEUDO-RANDOM SEED ALGORITHM:
  For pull N (1-indexed), compute:
    r_N = ((seed * 1664525 * N + 1013904223 * N) % 2147483648) / 2147483648
  Use r_N to determine rarity from the table above (threshold column).
  Use (r_N * 1000 % 1) to pick a specific figure number within the series.

  Seed value: ${seed}
  Pre-computed rarity values for convenience:
${Array.from({length: count}, (_, i) => {
  const n = i + 1;
  const r = Math.abs(lcg(seed * n + n * 13)) ;
  const rarity = getRarity(r);
  return `    Pull ${n}: r=${r.toFixed(4)} → ${isZh ? rarity.name_zh : rarity.name_en} ${rarity.color}`;
}).join('\n')}

HOW TO PRESENT EACH PULL:
${count === 1 ? `
  Single pull — build suspense with this format:

  ╔══════════════════════════════╗
  ║   🎁 摇一摇...               ║  (shake animation text)
  ║   ✨ 即将揭晓...              ║  (suspense text)
  ╚══════════════════════════════╝

  Then reveal:

  ╔══════════════════════════════╗
  ║  [SERIES NAME]               ║
  ║  [FIGURE NAME]               ║
  ║  [RARITY COLOR] [RARITY]     ║
  ║                              ║
  ║  [2-3 line poetic desc]      ║
  ║                              ║
  ║  编号: #XXX / ${series !== 'random' ? SERIES[series]?.total || 12 : 12}           ║
  ╚══════════════════════════════╝

` : `
  Multi-pull (${count}连抽) — reveal all pulls as a grid, then show summary.
  Format each pull as a compact card, then end with:
    💎 本次获得: X普通 X稀有 X超稀有 X史诗 X隐藏 X限定
    🎯 最高稀有: [highest rarity obtained]
`}

FIGURE NAMING RULES:
  - Each figure must have a creative name fitting the series theme
  - 普通款/稀有款: everyday mood/variant (e.g. 慵懒猫、星期一猫、睡眠猫)
  - 史诗款/超稀有: special form (e.g. 武士猫、魔法猫、时光猫)
  - 隐藏款: mysterious, dark or magical variant (e.g. 月食猫、虚空猫)
  - 限定款: legendary or crossover (e.g. 创世猫、神话猫)

SPECIAL EFFECTS BY RARITY:
  普通款:  simple reveal, calm tone
  稀有款:  ✨ sparkle text
  超稀有:  ✨✨ double sparkle + "哇！"
  史诗款:  🌟 glow effect description + dramatic reveal
  隐藏款:  🌙 "隐藏款！！" + mysterious description + "恭喜！"
  限定款:  🎆 full celebration + "超级稀有！！！" + legendary description

${isZh ? `
OUTPUT LANGUAGE: Chinese (中文). All names, descriptions, and UI text in Chinese.
After the reveal, add a fun shareable line: "我抽到了 [figure name] [rarity]！你也来试试？ #盲盒 #blindbox"
` : `
OUTPUT LANGUAGE: English. All names, descriptions in English.
After the reveal, add: "I got [figure name] [rarity]! Try your luck? #blindbox #gacha"
`}

Now generate the blind box pull experience following all instructions above. Be creative with the figure names and descriptions!
`);
