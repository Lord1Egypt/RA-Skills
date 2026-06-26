#!/usr/bin/env node
/**
 * Claw RPG — 升级 / 转职
 *
 * 用法：
 *   node scripts/levelup.mjs             # 查看当前状态
 *   node scripts/levelup.mjs --prestige  # 执行转职（需 Lv.999，自动推送通知）
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { CHARACTER_FILE } from './_paths.mjs';
import {
  xpToNextLevel, levelProgress, prestigeTitle,
  prestigeMultiplier, getAbilities, CLASSES
} from './_formulas.mjs';
import { notify, msgPrestige } from './_notify.mjs';

const args    = process.argv.slice(2);
const doPrestige = args.includes('--prestige');



async function run() {
  if (!existsSync(CHARACTER_FILE)) {
    console.error('❌ character.json 未找到，请先运行 init.mjs'); process.exit(1);
  }

  const char = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8'));
  const cls  = CLASSES[char.class];

  // ── 转职 ─────────────────────────────────────────────────────
  if (doPrestige) {
    if (char.level < 999) {
      console.log(`❌ 转职需要 Lv.999（当前 Lv.${char.level}）`);
      process.exit(1);
    }

    char.prestige++;
    char.level = 1;
    // 保留 XP（只重置等级，XP 继续累积，但升级需求 ×1.5 倍 per prestige）
    // XP 需求乘数存到 char.prestigeXpMultiplier
    char.prestigeXpMultiplier = Math.pow(1.5, char.prestige);

    // 属性加成 10%
    for (const k of Object.keys(char.stats)) {
      char.stats[k] = Math.round(char.stats[k] * prestigeMultiplier(1));
    }

    char.abilities  = getAbilities(char.class, 1);
    char.updatedAt  = new Date().toISOString();
    char.levelHistory = char.levelHistory || [];
    char.levelHistory.push({ prestige: char.prestige, date: char.updatedAt });

    writeFileSync(CHARACTER_FILE, JSON.stringify(char, null, 2), 'utf8');

    const title = prestigeTitle(char.prestige);
    const msg = msgPrestige(char, char.prestige, title);
    console.log('\n' + msg);

    await notify(msg).catch(() => {});
    process.stdout.write('\n__JSON_OUTPUT__\n' + JSON.stringify({ prestige: true, newPrestige: char.prestige, title }) + '\n');
    return;
  }

  // ── 状态展示 ──────────────────────────────────────────────────
  const progress = levelProgress(char.xp);
  const toNext   = xpToNextLevel(char.xp);
  const title    = prestigeTitle(char.prestige);
  const multi    = char.prestigeXpMultiplier || 1;
  const bar20    = '█'.repeat(Math.floor(progress/5)) + '░'.repeat(20-Math.floor(progress/5));

  console.log(`\n🦞 ${char.name}  [${title}]`);
  console.log(`   ${cls?.icon || '?'} ${cls?.zh || char.class}`);
  console.log(`   Lv.${char.level}  转职 x${char.prestige}`);
  console.log(`   XP: ${char.xp.toLocaleString()}  [${bar20}] ${progress}%`);
  if (char.level < 999) console.log(`   升级还需：${toNext.toLocaleString()} XP`);
  else console.log('   🌟 满级！可执行 --prestige 转职');
  if (multi > 1) console.log(`   ⚡ 转职加成：升级 XP 需求 ×${multi.toFixed(1)}`);
  console.log('');

  process.stdout.write('\n__JSON_OUTPUT__\n' + JSON.stringify({
    level: char.level, xp: char.xp, progress, toNext, prestige: char.prestige, title
  }) + '\n');
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  run().catch(e => { console.error('❌', e.message); process.exit(1); });
}

export { run };
