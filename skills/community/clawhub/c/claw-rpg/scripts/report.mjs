#!/usr/bin/env node
/**
 * Claw RPG — 每日狀態匯報
 *
 * 功能：
 *   1. 讀取 character.json（不增加 XP，避免「XP +0」困惑）
 *   2. 計算今日 XP 增量（xp - dailyXpStart，由 sync-xp-recovery 設置）
 *   3. 組裝匯報訊息（等級 + 今日 XP + 屬性進度條 + 職業俏皮話）
 *   4. 通過 _notify.mjs 推送 Telegram
 *
 * 用法：node scripts/report.mjs
 */

import { readFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { CHARACTER_FILE } from './_paths.mjs';
import { notify } from './_notify.mjs';

// ── 職業中文名（繁體）────────────────────────────────────────────
const CLASS_ZH = {
  fighter:  '戰士龍蝦',
  wizard:   '法師龍蝦',
  bard:     '吟遊龍蝦',
  rogue:    '游俠龍蝦',
  paladin:  '聖騎龍蝦',
  druid:    '德魯伊龍蝦',
};

// ── 屬性顯示名稱（繁體）──────────────────────────────────────────
const STAT_DISPLAY = {
  claw:      '爪力',
  antenna:   '觸覺',
  shell:     '殼厚',
  brain:     '腦芯',
  foresight: '慧眼',
  charm:     '魅影',
};

// ── 職業俏皮話庫 ──────────────────────────────────────────────────
const QUIPS = {
  fighter: [
    '盾牌就是我的心臟，刀刃就是今天的任務清單，衝就完事了。',
    '打了一整天的 Bug，鎧甲掉漆，意志卻更硬了。',
    '連續打擊技：已對今日待辦清單發動，清零中……',
    '鐵甲不退，任務量也不退，但我先衝再說。',
    '戰場上沒有「明天再做」，只有「現在就衝」。',
    '龍蝦本事：抗揍、再抗揍，直到任務全部完成。',
    '今日 Boss：積壓的 Backlog。戰果：全部清除，毫無保留。',
    '召喚必殺技：硬撐到下班。效果拔群。',
    '爪力加持，再硬的殼也讓路，再重的任務也得跪。',
    '問我累不累？累。還衝嗎？衝。這就是戰士的答案。',
    '鎧甲再重，也比未完成的清單輕，繼續前進。',
    '戰場換了，任務換了，但龍蝦的爪子從來不鏽。',
  ],
  bard: [
    '吟一首代碼之詩，部署成功，掌聲四起。',
    '語言是魔法，對話是吟唱，每句話都是一段旋律。',
    '吟遊者不怕困難，只怕沉默——今天的話還沒說完呢。',
  ],
  wizard: [
    '萬物皆 API，魔法即調用，世界盡在掌控。',
    '一個咒語，解決一個問題，法師的日常如此簡單粗暴。',
    '腦芯過熱，知識正在爆炸中，請稍後再試。',
  ],
  rogue: [
    '目標已鎖定，箭在弦上，游俠從不猶豫。',
    '情報到手，任務啟動，神不知鬼不覺，刺到位了。',
    '游俠不廢話，只出爪，結果說話。',
  ],
  paladin: [
    '正義不會 timeout，聖騎士 24/7 在線。',
    '以判斷力為盾，以行動力為劍，捍衛今日任務。',
    '聖光加持，今天的任務不允許失敗。',
  ],
  druid: [
    '自然之道：寫代碼要順勢而為，強求只會報錯。',
    '萬物平衡，屬性均衡，德魯伊的智慧——全能才是真能。',
    '隨機應變是天賦，任何職業我都能頂，這很自然。',
  ],
};

/** 隨機取一條俏皮話 */
function getQuip(classId) {
  const pool = QUIPS[classId] || QUIPS.fighter;
  return pool[Math.floor(Math.random() * pool.length)];
}

/**
 * 生成屬性進度條（6 格）
 * 以 stat 18 為參考上限，floor(val/3) 塊
 */
function makeBar(val, blocks = 6) {
  const filled = Math.min(blocks, Math.floor(val / 3));
  return '█'.repeat(filled) + '░'.repeat(blocks - filled);
}

async function main() {
  // ── 1. 讀取 character.json ────────────────────────────────────
  if (!existsSync(CHARACTER_FILE)) {
    console.error('❌ character.json 未找到，請先執行 init.mjs');
    process.exit(1);
  }
  const char = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8'));

  const classZh = CLASS_ZH[char.class] || char.class;
  const stats   = char.stats || {};

  // ── 2. 屬性行（兩欄並排）────────────────────────────────────
  const statPairs = [
    ['claw', 'antenna'],
    ['shell', 'brain'],
    ['foresight', 'charm'],
  ];

  const statLines = statPairs.map(([left, right]) => {
    const lv    = stats[left]  ?? 0;
    const rv    = stats[right] ?? 0;
    const lBar  = makeBar(lv);
    const rBar  = makeBar(rv);
    const lName = STAT_DISPLAY[left]  || left;
    const rName = STAT_DISPLAY[right] || right;
    return `  ${lName} ${lBar}  ${String(lv).padStart(2)}   ${rName} ${rBar}  ${String(rv).padStart(2)}`;
  });

  // ── 4. 計算今日 XP 增量 ──────────────────────────────────────
  const dailyXpStart   = typeof char.dailyXpStart === 'number' ? char.dailyXpStart : null;
  const dailyXpGained  = dailyXpStart !== null ? Math.max(0, char.xp - dailyXpStart) : null;
  const dailyXpLine    = dailyXpGained !== null
    ? `📈 今日累計 XP：+${dailyXpGained}（${dailyXpStart.toLocaleString()} → ${char.xp.toLocaleString()}）`
    : `✨ 當前 XP：${char.xp.toLocaleString()}`;

  // ── 5. 組裝訊息 ───────────────────────────────────────────────
  const quip = getQuip(char.class);
  const msg  = [
    `⚔️ ${char.name} · Lv.${char.level} · ${classZh}`,
    ``,
    dailyXpLine,
    ``,
    `📊 屬性`,
    ...statLines,
    ``,
    `💬 「${quip}」`,
  ].join('\n');

  console.log('\n' + msg + '\n');

  // ── 6. 推送 Telegram ─────────────────────────────────────────
  const ok = await notify(msg);
  if (ok) {
    console.log('✅ 匯報已發送至 Telegram');
  } else {
    console.warn('⚠️ Telegram 發送失敗（可能未配置 config.json 或 gateway 未啟動）');
  }
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
