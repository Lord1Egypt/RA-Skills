#!/usr/bin/env node
/**
 * Claw RPG — 角色卡（終端）v2.0.0
 * D&D 3.5 標準顯示格式
 *
 * 用法：
 *   node scripts/sheet.mjs
 *   node scripts/sheet.mjs --json   # 僅輸出 JSON
 */

import { readFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { CHARACTER_FILE } from './_paths.mjs';
import {
  xpToNextLevel, levelProgress, prestigeTitle,
  CLASSES, STAT_NAMES, proficiencyBonus, abilityMod
} from './_formulas.mjs';

const jsonOnly = process.argv.includes('--json');

function statBar(val, max = 20) {
  const filled = Math.round((val / max) * 10);
  return '█'.repeat(Math.max(0, filled)) + '░'.repeat(Math.max(0, 10 - filled));
}

function xpBar(progress, width = 24) {
  const filled = Math.round((progress / 100) * width);
  return '▓'.repeat(filled) + '░'.repeat(width - filled);
}

function signStr(n) {
  return (n >= 0 ? '+' : '') + n;
}

function run() {
  if (!existsSync(CHARACTER_FILE)) {
    console.error('❌ 角色卡未找到，請先運行：node scripts/init.mjs');
    process.exit(1);
  }

  const char     = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8'));
  const cls      = CLASSES[char.class] || {};
  const title    = prestigeTitle(char.prestige);
  const progress = levelProgress(char.xp);
  const toNext   = xpToNextLevel(char.xp);
  const prof     = proficiencyBonus(char.level);
  const bar      = xpBar(progress);

  if (jsonOnly) {
    process.stdout.write(JSON.stringify(char, null, 2) + '\n');
    return char;
  }

  const W = 54;
  const dline = '═'.repeat(W);

  console.log(`\n╔${dline}╗`);
  console.log(`║  🦞  CLAW RPG  ─  角色卡  D&D 3.5 v2.0.0${' '.repeat(W - 43)}║`);
  console.log(`╠${dline}╣`);

  // 基本信息
  const clsStr = `${cls.icon || '?'} ${cls.zh || char.class}`;
  console.log(`║  ${char.name.padEnd(16)}  ${clsStr.padEnd(14)}  ║`);
  console.log(`║  稱號: ${title.padEnd(14)}  轉職: x${String(char.prestige).padEnd(2)}              ║`);
  console.log(`║  等級: Lv.${String(char.level).padEnd(3)}  精通加成: +${prof}  BAB: +${String(char.bab ?? '?').padEnd(4)}       ║`);
  console.log(`╠${dline}╣`);

  // XP 進度
  const pct = String(progress).padStart(3);
  console.log(`║  XP  ${bar}  ${pct}%  ║`);
  const xpStr = `${char.xp.toLocaleString()} XP${toNext > 0 ? '  還差 ' + toNext.toLocaleString() : '  【滿級】'}`;
  console.log(`║  ${xpStr.padEnd(W)}║`);
  console.log(`╠${dline}╣`);

  // 屬性區（D&D 3.5 格式）
  console.log(`║  ── 能力值 ${'─'.repeat(W - 10)}║`);
  for (const [k, info] of Object.entries(STAT_NAMES)) {
    const val    = char.stats?.[k] ?? 10;
    const mod    = abilityMod(val);
    const modStr = signStr(mod);
    const b      = statBar(val);
    const label  = `${info.zh}(${info.dnd})`.padEnd(10);
    console.log(`║  ${info.icon} ${label} [${b}] ${String(val).padStart(2)} (${modStr.padStart(2)})  ║`);
  }
  console.log(`╠${dline}╣`);

  // 衍生數值區
  console.log(`║  ── 衍生數值 ${'─'.repeat(W - 12)}║`);
  const hp   = char.hp   ?? '?';
  const ac   = char.ac   ?? '?';
  const init = char.initiative !== undefined ? signStr(char.initiative) : '?';
  const fort = char.saves?.fort !== undefined ? signStr(char.saves.fort) : '?';
  const ref  = char.saves?.ref  !== undefined ? signStr(char.saves.ref)  : '?';
  const will = char.saves?.will !== undefined ? signStr(char.saves.will) : '?';
  console.log(`║  ❤️  HP: ${String(hp).padEnd(5)}  🛡️ AC: ${String(ac).padEnd(5)}  ⚡ 先攻: ${init.padEnd(5)}         ║`);
  console.log(`║  💪 韌性(Fort): ${fort.padEnd(4)}  🏃 反射(Ref): ${ref.padEnd(4)}  🧘 意志(Will): ${will.padEnd(4)} ║`);
  console.log(`╠${dline}╣`);

  // 職業特性
  console.log(`║  ── 職業特性 ${'─'.repeat(W - 12)}║`);
  const abilities = char.abilities || [];
  if (abilities.length === 0) {
    console.log(`║  （暫無特性）${' '.repeat(W - 13)}║`);
  } else {
    for (let i = 0; i < abilities.length; i += 3) {
      const row = abilities.slice(i, i+3).join('  ·  ');
      console.log(`║  ${row.padEnd(W)}║`);
    }
  }
  console.log(`╠${dline}╣`);

  // 專長區
  console.log(`║  ── 專長 (Feats) ${'─'.repeat(W - 16)}║`);
  const feats = char.feats || [];
  if (feats.length === 0) {
    console.log(`║  （暫無專長）${' '.repeat(W - 13)}║`);
  } else {
    for (let i = 0; i < feats.length; i += 2) {
      const pair = feats.slice(i, i+2);
      const col1 = pair[0]?.padEnd(27) ?? '';
      const col2 = pair[1] ?? '';
      const row  = (col1 + col2).padEnd(W);
      console.log(`║  ${row}║`);
    }
  }
  console.log(`╠${dline}╣`);

  // 戰績統計
  const totalConv = char.conversations || 0;
  const tokIn  = (char.tokens?.consumed || 0).toLocaleString();
  const tokOut = (char.tokens?.produced || 0).toLocaleString();
  console.log(`║  ── 戰績 ${'─'.repeat(W - 8)}║`);
  console.log(`║  對話次數: ${String(totalConv).padEnd(8)} 消耗 Token: ${tokIn.padEnd(10)}    ║`);
  console.log(`║  職業歷史: ${(char.classHistory?.length || 0)} 次變化   產出 Token: ${tokOut.padEnd(10)}   ║`);
  console.log(`╚${dline}╝\n`);

  process.stdout.write('\n__JSON_OUTPUT__\n' + JSON.stringify({
    name: char.name, class: char.class, level: char.level,
    xp: char.xp, progress, stats: char.stats,
    hp: char.hp, ac: char.ac, bab: char.bab,
    saves: char.saves, initiative: char.initiative,
    abilities: char.abilities, feats: char.feats
  }) + '\n');

  return char;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  run();
}

export { run };
