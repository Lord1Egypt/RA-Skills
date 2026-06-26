#!/usr/bin/env node
/**
 * Claw RPG — 角色初始化
 * 从 SOUL.md + MEMORY.md 生成 character.json
 *
 * 用法：
 *   node scripts/init.mjs               # 首次初始化
 *   node scripts/init.mjs --force       # 强制重置（覆盖现有）
 *   node scripts/init.mjs --recalc      # 仅重算属性/职业（保留 XP/等级）
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync } from 'fs';
import { fileURLToPath } from 'url';
import {
  CHARACTER_FILE, DATA_DIR, SOUL_FILE, MEMORY_FILE, SKILL_ROOT, WORKSPACE, SCRIPTS_URL
} from './_paths.mjs';
import { join } from 'path';
import {
  deriveStats, detectClass, getAbilities, prestigeTitle,
  xpForLevel, STAT_NAMES, CLASSES
} from './_formulas.mjs';
import { notify, msgClassChange } from './_notify.mjs';

const args  = process.argv.slice(2);
const force  = args.includes('--force');
const recalc = args.includes('--recalc');

function extractName(text) {
  const m = text.match(/[*#\-\s]*(Name|名字|name)[：:]\s*([^\n（(🐾]+)/i);
  if (!m) return null;
  return m[2].trim().replace(/[*`_]/g,'').split(/\s+/)[0] || null;
}

async function run() {
  // 確保資料目錄存在（workspace/claw-rpg/）
  mkdirSync(DATA_DIR, { recursive: true });

  // 遷移：若舊位置（skill 根目錄）有 character.json，搬過來
  const legacyFile = join(SKILL_ROOT, 'character.json');
  if (!existsSync(CHARACTER_FILE) && existsSync(legacyFile)) {
    copyFileSync(legacyFile, CHARACTER_FILE);
    console.log('📦 已從舊位置遷移 character.json → workspace/claw-rpg/');
  }

  // 安全检查
  if (existsSync(CHARACTER_FILE) && !force && !recalc) {
    console.log('⚠️  character.json 已存在。');
    console.log('   --force  覆盖重置');
    console.log('   --recalc 仅重算属性/职业（保留 XP）');
    process.exit(0);
  }

  const IDENTITY_FILE = join(WORKSPACE, 'IDENTITY.md');
  const soul   = [SOUL_FILE, IDENTITY_FILE]
    .filter(existsSync).map(f => readFileSync(f, 'utf8')).join('\n');
  const memory = existsSync(MEMORY_FILE) ? readFileSync(MEMORY_FILE, 'utf8') : '';

  if (!soul) console.warn('⚠️  未找到 SOUL.md，属性将使用默认值');

  const stats   = deriveStats(soul, memory);
  const classId = detectClass(stats);
  const cls     = CLASSES[classId];
  const name    = extractName(soul) || extractName(memory) || '未知龙虾';

  // 如果是 recalc，读取现有数据保留 XP/等级
  let existing = {};
  if (recalc && existsSync(CHARACTER_FILE)) {
    try { existing = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8')); }
    catch {}
  }

  const now = new Date().toISOString();
  const character = {
    name,
    class:        classId,
    classHistory: existing.classHistory || [],
    level:        existing.level    || 1,
    prestige:     existing.prestige || 0,
    xp:           existing.xp       || 0,
    stats,
    statPoints:   existing.statPoints || 0,
    abilities:    getAbilities(classId, existing.level || 1),
    tokens: existing.tokens || {
      consumed:         0,
      produced:         0,
      lastSnapshotConsumed: 0,
      lastSnapshotProduced: 0,
    },
    conversations:  existing.conversations  || 0,
    lastXpSync:     existing.lastXpSync     || now,
    createdAt:      existing.createdAt      || now,
    updatedAt:      now,
    levelHistory:   existing.levelHistory   || [{ level: 1, date: now }],
  };

  // 记录职业变化
  const oldClass = existing.class;
  const classChanged = oldClass && oldClass !== classId;
  if (classChanged) {
    character.classHistory = [...(existing.classHistory || []), {
      from: oldClass, to: classId, date: now, reason: 'recalc'
    }];
    console.log(`🔄 职业变化：${CLASSES[oldClass]?.zh} → ${cls.zh}`);
  }

  writeFileSync(CHARACTER_FILE, JSON.stringify(character, null, 2), 'utf8');

  // 职业变化通知
  if (classChanged) {
    const oldCls = CLASSES[oldClass] || { zh: oldClass, icon: '?' };
    // 找出变化最大的属性作为触发原因
    const topStat  = Object.entries(stats).sort(([,a],[,b]) => b-a)[0];
    const statInfo = STAT_NAMES[topStat[0]];
    notify(msgClassChange(character, oldClass, classId, oldCls.zh, cls.zh, statInfo.zh, statInfo.icon))
      .catch(() => {}); // 静默失败
  }

  // 输出摘要
  console.log(`\n🦞 角色已${recalc ? '重算' : '初始化'}！`);
  console.log(`\n   ${cls.icon} ${name}`);
  console.log(`   职业：${cls.zh}  ${cls.desc}`);
  console.log(`   等级：Lv.${character.level}  转职：${prestigeTitle(character.prestige)}`);
  console.log(`   XP  ：${character.xp}`);
  console.log(`\n   属性：`);
  for (const [k, v] of Object.entries(stats)) {
    const info = STAT_NAMES[k];
    const bar  = '█'.repeat(Math.floor(v/2)) + '░'.repeat(9 - Math.floor(v/2));
    console.log(`     ${info.icon} ${info.zh.padEnd(4)}  ${bar}  ${v}`);
  }
  console.log(`\n   技能：${character.abilities.join(' / ') || '（无）'}`);
  console.log('');
  console.log(`   角色卡已保存：${CHARACTER_FILE}\n`);

  process.stdout.write('\n__JSON_OUTPUT__\n' + JSON.stringify(character) + '\n');

  // 初始化完成后立刻自报家门（首次亮相，--recalc 不触发）
  if (!recalc) {
    // 标记今日已问候，防止 greet.mjs 重复触发
    character.lastGreetDate = new Date().toISOString().slice(0, 10);
    writeFileSync(CHARACTER_FILE, JSON.stringify(character, null, 2), 'utf8');
    console.log('\n── 首次亮相 ──');
    const { buildGreeting } = await import(`${SCRIPTS_URL}greet.mjs`);
    console.log(buildGreeting(character));
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  run().catch(e => { console.error('❌', e.message); process.exit(1); });
}

export { run };
