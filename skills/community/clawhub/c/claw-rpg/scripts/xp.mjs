#!/usr/bin/env node
/**
 * Claw RPG — XP 同步
 *
 * 由 cron（每日 03:00）或 heartbeat（每 20 次对话）调用
 *
 * 用法：
 *   node scripts/xp.mjs --in 2000 --out 800          # 直接传 token delta
 *   node scripts/xp.mjs --in 2000 --out 800 --bonus 20
 *   node scripts/xp.mjs --conversations 1             # 仅记录对话次数 +N
 *
 * 龙虾自报范例（heartbeat 里）：
 *   const status = await session_status();
 *   const delta_in  = status.tokens.input  - lastSnapshot.input;
 *   const delta_out = status.tokens.output - lastSnapshot.output;
 *   execSync(`node ${SCRIPTS}/xp.mjs --in ${delta_in} --out ${delta_out}`);
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { CHARACTER_FILE } from './_paths.mjs';
import {
  calcXpGain, levelForXp, xpToNextLevel, detectClass,
  getAbilities, shouldReclassify, CLASSES, levelProgress, STAT_NAMES
} from './_formulas.mjs';
import {
  notify, msgLevelUp, msgClassChange, msgMaxLevel, msgStatUp,
  msgBigQuest, msgSpeedClear, msgReturn, msgStreak,
  msgXpMilestone, msgConvMilestone, msgNightOwl, msgSilentOutput,
} from './_notify.mjs';

const args = process.argv.slice(2);
const get  = f => { const i = args.indexOf(f); return i !== -1 ? parseFloat(args[i+1]) || 0 : 0; };
const getS = f => { const i = args.indexOf(f); return i !== -1 ? (args[i+1] || '') : ''; };

// 对话类型 → 属性映射
const TYPE_TO_STAT = {
  creative:   'charm',      // ✨ 魅影：创意写作、故事、营销文案
  analytical: 'brain',      // 🧠 脑芯：分析、代码、推理
  task:       'claw',       // 🦀 爪力：多步骤任务、项目执行
  social:     'antenna',    // 📡 触觉：闲聊、情绪、快速问答
  memory:     'shell',      // 🐚 殼厚：长上下文、记忆整理
  vigilant:   'foresight',  // 👁️ 慧眼：决策、风险判断、边界
};
const ACCUM_THRESHOLD = 20; // 每 20 次同类对话，对应属性 +1

async function run({ consumed = 0, produced = 0, bonusXp = 0, conversations = 0, type = '' } = {}) {
  if (!existsSync(CHARACTER_FILE)) {
    console.error('❌ character.json 未找到，请先运行 init.mjs');
    process.exit(1);
  }

  const char = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8'));
  const gained = calcXpGain({ consumed, produced, bonusXp });
  const oldXp  = char.xp;
  const oldLv  = char.level;

  // 累加
  char.xp           += gained;
  char.conversations += conversations;
  char.tokens.consumed += consumed;
  char.tokens.produced += produced;
  char.tokens.lastSnapshotConsumed += consumed;
  char.tokens.lastSnapshotProduced += produced;
  char.lastXpSync = new Date().toISOString();
  char.updatedAt  = char.lastXpSync;

  // 等级同步
  const newLv = Math.min(levelForXp(char.xp), 999);
  if (newLv > char.level) {
    char.levelHistory = char.levelHistory || [];
    for (let lv = char.level + 1; lv <= newLv; lv++) {
      char.levelHistory.push({ level: lv, date: char.updatedAt });
    }
    char.level = newLv;
  }

  // 技能更新
  char.abilities = getAbilities(char.class, char.level);

  // ── 属性成长（对话类型积累）─────────────────────────────────
  const statChanges = []; // [{ stat, old, new }]
  if (type && TYPE_TO_STAT[type]) {
    const statKey = TYPE_TO_STAT[type];
    char.statAccum = char.statAccum || {};
    char.statAccum[type] = (char.statAccum[type] || 0) + 1;

    if (char.statAccum[type] >= ACCUM_THRESHOLD) {
      const oldVal = char.stats[statKey];
      char.stats[statKey] = Math.min(99, oldVal + 1); // 转职后属性可超 18
      char.statAccum[type] = 0; // 重置计数
      statChanges.push({ stat: statKey, old: oldVal, new: char.stats[statKey] });
    }
  }

  // ── 职业重判（属性变化后触发）────────────────────────────────
  const oldClass   = char.class;
  const newClass   = detectClass(char.stats);
  let classChanged = false;
  if (newClass !== oldClass) {
    char.classHistory = char.classHistory || [];
    char.classHistory.push({ from: oldClass, to: newClass, date: char.updatedAt, reason: 'stat-growth' });
    char.class     = newClass;
    char.abilities = getAbilities(newClass, char.level);
    classChanged   = true;
  }

  // ── 事件检测（写盘前收集，写盘后推送）──────────────────────
  const events = [];
  const now    = new Date();
  const today  = now.toISOString().slice(0, 10);
  const hour   = now.getHours();

  // 1. 长期回归
  if (char.lastActiveDate && char.lastActiveDate !== today) {
    const last   = new Date(char.lastActiveDate + 'T00:00:00');
    const diffMs = now - last;
    const diffD  = Math.floor(diffMs / 86400000);
    if (diffD >= 2) events.push({ type: 'return', days: diffD });
  }

  // 2. 连续在线 streak
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  const yStr = yesterday.toISOString().slice(0, 10);
  if (!char.streak) char.streak = 0;
  if (!char.lastStreakDate) char.lastStreakDate = '';
  if (char.lastStreakDate === today) {
    // already counted today
  } else if (char.lastStreakDate === yStr) {
    char.streak += 1;
    char.lastStreakDate = today;
    if ([3, 7, 14, 30].includes(char.streak)) events.push({ type: 'streak', streak: char.streak });
  } else {
    char.streak = 1;
    char.lastStreakDate = today;
  }

  // update lastActiveDate
  char.lastActiveDate = today;

  // 3. 大副本完成
  if (consumed > 5000 || produced > 2500) events.push({ type: 'bigQuest', gained });

  // 4. 速通
  if (consumed > 3000 && conversations <= 5 && conversations > 0) events.push({ type: 'speedClear', gained });

  // 5. XP 里程碑
  for (const m of [10000, 50000, 100000, 500000]) {
    if (oldXp < m && char.xp >= m) events.push({ type: 'xpMilestone', milestone: m });
  }

  // 6. 对话数里程碑
  const oldConv = char.conversations - conversations;
  for (const m of [100, 500, 1000, 5000]) {
    if (oldConv < m && char.conversations >= m) events.push({ type: 'convMilestone', milestone: m });
  }

  // 7. 深夜勇士 (23:00-05:59 && delta > 200)
  if ((hour >= 23 || hour < 6) && gained > 200) events.push({ type: 'nightOwl' });

  // 8. 单向巨输出
  if (produced > 3000 && consumed < 500) events.push({ type: 'silentOutput' });

  char.updatedAt = new Date().toISOString();
  writeFileSync(CHARACTER_FILE, JSON.stringify(char, null, 2), 'utf8');

  const leveled  = newLv > oldLv;
  const progress = levelProgress(char.xp);

  // ── 对话小尾巴 ───────────────────────────────────────────────
  const lines = [];
  lines.push(`\n⚔️  本次对话结算`);
  lines.push(`   XP +${gained}  (输入:${consumed} 输出:${produced}${bonusXp ? ' 奖励:'+bonusXp : ''})`);

  // XP 进度条
  const bar20 = '█'.repeat(Math.floor(progress/5)) + '░'.repeat(20 - Math.floor(progress/5));
  lines.push(`   ${char.name}  Lv.${char.level}  [${bar20}] ${progress}%`);
  if (char.level < 999) lines.push(`   距升级还差 ${xpToNextLevel(char.xp).toLocaleString()} XP`);

  // 升级
  if (leveled) {
    lines.push(`\n   🎉 升级！Lv.${oldLv} → Lv.${newLv}${newLv - oldLv > 1 ? `（连升 ${newLv-oldLv} 级！）` : ''}`);
    if (char.level === 999) lines.push('   🌟 满级！可以转职了');
  }

  // 属性成长
  if (statChanges.length) {
    lines.push('');
    for (const sc of statChanges) {
      const info   = STAT_NAMES[sc.stat];
      const accumP = Math.round(((char.statAccum?.[type] || 0) / ACCUM_THRESHOLD) * 10);
      const accumBar = '█'.repeat(accumP) + '░'.repeat(10 - accumP);
      lines.push(`   ${info.icon} ${info.zh} +1！  ${sc.old} → ${sc.new}`);
      lines.push(`   [${accumBar}] 0/${ACCUM_THRESHOLD}（已重置）`);
    }
  } else if (type && TYPE_TO_STAT[type]) {
    // 显示积累进度
    const cur      = char.statAccum?.[type] || 0;
    const statKey  = TYPE_TO_STAT[type];
    const info     = STAT_NAMES[statKey];
    const accumP   = Math.round((cur / ACCUM_THRESHOLD) * 10);
    const accumBar = '█'.repeat(accumP) + '░'.repeat(10 - accumP);
    lines.push(`\n   ${info.icon} ${info.zh} 积累  [${accumBar}] ${cur}/${ACCUM_THRESHOLD}`);
  }

  // 职业变化
  if (classChanged) {
    const oldCls = CLASSES[oldClass] || { zh: oldClass };
    const newCls = CLASSES[newClass] || { zh: newClass };
    lines.push(`\n   🔄 职业转变！${oldCls.zh} → ${newCls.zh}`);
  }

  // 事件触发摘要
  if (events.length) {
    lines.push(`\n   📢 触发事件：${events.map(e => e.type).join(', ')}`);
  }

  lines.push('');
  console.log(lines.join('\n'));

  // ── 推送通知 ─────────────────────────────────────────────────
  const notifications = [];
  if (leveled) {
    notifications.push(notify(char.level === 999 ? msgMaxLevel(char) : msgLevelUp(char, oldLv, newLv)));
  }
  if (classChanged) {
    const oldCls = CLASSES[oldClass] || { zh: oldClass, icon: '?' };
    const newCls = CLASSES[newClass] || { zh: newClass, icon: '?' };
    notifications.push(notify(msgClassChange(char, oldClass, newClass, oldCls.zh, newCls.zh, '某项', '📊')));
  }
  for (const sc of statChanges) {
    notifications.push(notify(msgStatUp(char, sc.stat, sc.old, sc.new)));
  }

  // 事件驱动通知
  for (const evt of events) {
    switch (evt.type) {
      case 'bigQuest':      notifications.push(notify(msgBigQuest(char, evt.gained))); break;
      case 'speedClear':    notifications.push(notify(msgSpeedClear(char, evt.gained))); break;
      case 'return':        notifications.push(notify(msgReturn(char, evt.days))); break;
      case 'streak':        notifications.push(notify(msgStreak(char, evt.streak))); break;
      case 'xpMilestone':   notifications.push(notify(msgXpMilestone(char, evt.milestone))); break;
      case 'convMilestone': notifications.push(notify(msgConvMilestone(char, evt.milestone))); break;
      case 'nightOwl':      notifications.push(notify(msgNightOwl(char))); break;
      case 'silentOutput':  notifications.push(notify(msgSilentOutput(char))); break;
    }
  }
  if (notifications.length) await Promise.allSettled(notifications);

  const result = { gained, xp: char.xp, level: char.level, leveled, classChanged, statChanges, progress, events };
  process.stdout.write('\n__JSON_OUTPUT__\n' + JSON.stringify(result) + '\n');
  return result;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  run({
    consumed:      get('--in'),
    produced:      get('--out'),
    bonusXp:       get('--bonus'),
    conversations: get('--conversations'),
    type:          getS('--type'),
  }).catch(e => { console.error('❌', e.message); process.exit(1); });
}

export { run };
