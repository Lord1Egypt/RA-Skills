#!/usr/bin/env node
/**
 * english-daily — 学习进度查看
 *
 * 用法:
 *   node progress.js <userId>
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const { getWordStats, loadWordBank, todayStr, addDays } = require('./wordbank');

const USERS_DIR = path.join(__dirname, '../data/users');

// ── Security helpers ──────────────────────────────────────────────────────────

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ 无效的 userId：只允许字母、数字、- 和 _，长度 1-128');
    process.exit(1);
  }
  return value;
}

function safeUserPath(userId) {
  const resolved = path.resolve(USERS_DIR, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(USERS_DIR) + path.sep)) {
    console.error('❌ 非法路径');
    process.exit(1);
  }
  return resolved;
}

function loadUser(userId) {
  const f = safeUserPath(userId);
  if (!fs.existsSync(f)) {
    console.error(`❌ 未找到用户：${userId}。请先注册：node register.js ${userId} <姓名>`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function saveUser(userId, data) {
  fs.mkdirSync(USERS_DIR, { recursive: true });
  fs.writeFileSync(safeUserPath(userId), JSON.stringify(data, null, 2), 'utf8');
}

// ── Level-up thresholds ───────────────────────────────────────────────────────

const LEVEL_UP = {
  A1: { wordsNeeded: 40,  next: 'A2' },
  A2: { wordsNeeded: 90,  next: 'B1' },
  B1: { wordsNeeded: 130, next: 'B2' },
  B2: { wordsNeeded: Infinity, next: null }
};

function checkLevelUp(profile) {
  const threshold = LEVEL_UP[profile.level];
  if (!threshold || !threshold.next) return false;

  const stats = getWordStats(profile);
  if (stats.mastered >= threshold.wordsNeeded) {
    return threshold.next;
  }
  return false;
}

// ── Weekly study days ─────────────────────────────────────────────────────────

function getWeeklyDays(profile) {
  // Count study days in the last 7 calendar days
  // We only track lastStudyDate precisely; use streak as proxy
  const streak = profile.streak || 0;
  return Math.min(streak, 7);
}

// ── Words to next level ───────────────────────────────────────────────────────

function wordsToNextLevel(profile) {
  const threshold = LEVEL_UP[profile.level];
  if (!threshold || !threshold.next) return 0;
  const stats = getWordStats(profile);
  return Math.max(0, threshold.wordsNeeded - stats.mastered);
}

// ── Main ──────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (!args[0]) {
  console.log('用法: node progress.js <userId>');
  process.exit(1);
}

const userId  = sanitizeId(args[0]);
const profile = loadUser(userId);

// Check for level-up
const newLevel = checkLevelUp(profile);
if (newLevel) {
  console.log(`\n🎉 恭喜！你已升级至 ${newLevel}！`);
  profile.level = newLevel;
  profile.targetLevel = LEVEL_UP[newLevel] ? LEVEL_UP[newLevel].next || newLevel : newLevel;
  saveUser(userId, profile);
  console.log(`等级已更新：${profile.level} → 目标 ${profile.targetLevel}\n`);
}

const stats      = getWordStats(profile);
const bank       = loadWordBank();
const allAtLevel = bank.filter(w => {
  const levels = ['A1','A2','B1','B2'];
  return levels.indexOf(w.lv) <= levels.indexOf(profile.level);
}).length;

const weeklyDays   = getWeeklyDays(profile);
const toNextLevel  = wordsToNextLevel(profile);
const threshold    = LEVEL_UP[profile.level];

console.log(`
📊 学习进度 — ${profile.name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 连续学习：${profile.streak || 0}天（最长：${profile.longestStreak || 0}天）
⭐ 总积分：${profile.totalPoints || 0}
📚 已学单词：${Object.keys(profile.wordProgress || {}).length} / ${allAtLevel}
🎯 当前等级：${profile.level} → 目标：${profile.targetLevel || profile.level}

词汇详情：
  已掌握（间隔≥7天）：${stats.mastered}个
  学习中（间隔<7天）：${stats.learning}个
  待复习（今日到期）：${stats.due}个

📅 本周学习：${weeklyDays}/7天
${threshold && threshold.next
  ? `💡 距离下一等级（${threshold.next}）：还需掌握 ${toNextLevel} 个单词`
  : '🏆 已达到最高等级 B2！'}

${stats.due > 0 ? `⚠️  今日有 ${stats.due} 个单词需要复习！` : '✅ 今日无待复习单词'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
开始今日学习：node scripts/daily-push.js ${userId}
开始测验：    node scripts/quiz.js ${userId}
`);
