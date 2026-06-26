#!/usr/bin/env node
/**
 * blind-box series — show all available series and rarity rates
 * Usage: node series.js [--lang zh|en]
 */

const lang = process.argv.includes('--lang')
  ? process.argv[process.argv.indexOf('--lang') + 1]
  : 'zh';

const isZh = lang === 'zh';

console.log(`
${isZh ? '🎁 盲盒系列大全' : '🎁 Blind Box Series Catalogue'}
${'═'.repeat(50)}

${isZh ? '📦 可用系列' : '📦 Available Series'}
${'─'.repeat(50)}

  🐱  ${isZh ? '猫咪日常系列' : 'Daily Cat Series'}
      ${isZh ? '12款 · 隐藏款2款 · 限定款1款' : '12 figures · 2 hidden · 1 limited'}
      ${isZh ? '慵懒、傲娇、武士、月食...' : 'Lazy, tsundere, samurai, lunar eclipse...'}

  🚀  ${isZh ? '宇宙探险系列' : 'Space Explorer Series'}
      ${isZh ? '10款 · 隐藏款2款 · 限定款1款' : '10 figures · 2 hidden · 1 limited'}
      ${isZh ? '宇航员、外星人、黑洞旅行者...' : 'Astronaut, alien, black hole traveler...'}

  🍜  ${isZh ? '美食精灵系列' : 'Food Spirit Series'}
      ${isZh ? '10款 · 隐藏款1款 · 限定款1款' : '10 figures · 1 hidden · 1 limited'}
      ${isZh ? '拉面精灵、寿司师傅、甜品仙子...' : 'Ramen spirit, sushi master, dessert fairy...'}

  🌸  ${isZh ? '四季精灵系列' : 'Season Spirit Series'}
      ${isZh ? '8款 · 隐藏款2款 · 限定款1款' : '8 figures · 2 hidden · 1 limited'}
      ${isZh ? '春雨精灵、夏日仙子、秋叶武士...' : 'Spring rain, summer fairy, autumn warrior...'}

  ⚔️  ${isZh ? '古风仙侠系列' : 'Wuxia Series'}
      ${isZh ? '12款 · 隐藏款3款 · 限定款1款' : '12 figures · 3 hidden · 1 limited'}
      ${isZh ? '剑客、仙人、魔君、神龙使者...' : 'Swordsman, immortal, demon king, dragon envoy...'}

${'─'.repeat(50)}
${isZh ? '💎 稀有度概率' : '💎 Rarity Rates'}
${'─'.repeat(50)}

  ⚪  ${isZh ? '普通款' : 'Common'}      55%
  🔵  ${isZh ? '稀有款 ★' : 'Rare ★'}       25%
  🟡  ${isZh ? '超稀有 ★★' : 'Super Rare ★★'}  12%
  🟠  ${isZh ? '史诗款 ★★★' : 'Epic ★★★'}     6%
  🟣  ${isZh ? '隐藏款 ✦' : 'Hidden ✦'}      1.5%
  🔴  ${isZh ? '限定款 ✦✦' : 'Limited ✦✦'}     0.5%

${'─'.repeat(50)}
${isZh ? '🎮 使用方法' : '🎮 How to Use'}
${'─'.repeat(50)}

  # ${isZh ? '随机系列单抽' : 'Random series single pull'}
  node pull.js

  # ${isZh ? '指定系列' : 'Choose a series'}
  node pull.js --series cat
  node pull.js --series space
  node pull.js --series food
  node pull.js --series spirit
  node pull.js --series wuxia

  # ${isZh ? '十连抽' : '10-pull'}
  node pull.js --series cat --count 10

  # ${isZh ? '英文版' : 'English version'}
  node pull.js --lang en

  # ${isZh ? '查看每日限免' : 'Daily free pull'}
  node daily.js
`);
