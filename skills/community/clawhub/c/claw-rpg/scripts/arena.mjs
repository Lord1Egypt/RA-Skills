#!/usr/bin/env node
/**
 * Claw RPG — 龙虾竞技场 🏟️
 * P1 骨架：接口已定义，战斗逻辑待实现
 *
 * 用法（未来）：
 *   node scripts/arena.mjs challenge --opponent <character.json路径> --topic "帮我写一首诗"
 *   node scripts/arena.mjs leaderboard
 *   node scripts/arena.mjs history
 *
 * 战斗逻辑：
 *   1. 双方龙虾各自接受相同题目
 *   2. 各自作答（由宿主 AI 生成）
 *   3. 由中立评判（第三方 AI 或社区投票）评分
 *   4. 胜者 +100XP，败者 +50XP（学习所得）
 *   5. 双方战绩写入 arena-history.json
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath, join } from 'url';
import { CHARACTER_FILE, SKILL_ROOT } from './_paths.mjs';

const ARENA_FILE = `${SKILL_ROOT}/arena-history.json`;

const cmd = process.argv[2];

function loadHistory() {
  if (!existsSync(ARENA_FILE)) return [];
  try { return JSON.parse(readFileSync(ARENA_FILE, 'utf8')); } catch { return []; }
}

switch (cmd) {
  case 'challenge':
    console.log('🏟️  竞技场挑战功能（P1）- 敬请期待！');
    console.log('\n规则预告：');
    console.log('  · 双方出题，各自作答');
    console.log('  · 中立 AI 评分');
    console.log('  · 胜者 +100 XP，败者 +50 XP');
    break;

  case 'leaderboard': {
    const history = loadHistory();
    if (!history.length) { console.log('🏆 排行榜暂无记录'); break; }
    const scores = {};
    for (const h of history) {
      scores[h.winner] = (scores[h.winner] || 0) + 1;
    }
    console.log('\n🏆 龙虾竞技场 — 排行榜\n');
    Object.entries(scores)
      .sort(([,a],[,b]) => b - a)
      .slice(0, 10)
      .forEach(([name, wins], i) => console.log(`  ${i+1}. ${name}  ${wins} 胜`));
    break;
  }

  case 'history': {
    const history = loadHistory();
    console.log(`\n⚔️  竞技场历史（共 ${history.length} 场）\n`);
    history.slice(-10).forEach(h => {
      console.log(`  ${h.date?.slice(0,10)}  ${h.winner} 胜 ${h.loser}  主题：${h.topic}`);
    });
    break;
  }

  default:
    console.log(`
🏟️  龙虾竞技场

  node scripts/arena.mjs challenge --opponent <path> --topic "题目"
  node scripts/arena.mjs leaderboard
  node scripts/arena.mjs history

  P1 阶段开发中，敬请期待！
  `);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  // CLI already handled above
}
