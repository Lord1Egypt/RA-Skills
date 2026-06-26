#!/usr/bin/env node
/**
 * english-daily — 每日学习推送 prompt 生成器
 *
 * 用法:
 *   node daily-push.js <userId>
 *
 * 由 openclaw cron 驱动，每日早晨执行。
 * 输出结构化文本，由 Claude 格式化呈现给用户。
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const {
  getDueWords,
  getNewWordsForUser,
  todayStr,
  addDays
} = require('./wordbank');

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

// ── Streak update ─────────────────────────────────────────────────────────────

function updateStreak(profile) {
  const today     = todayStr();
  const yesterday = addDays(today, -1);
  const last      = profile.lastStudyDate;

  if (last === today) {
    // Already counted today, no change
    return profile;
  } else if (last === yesterday) {
    profile.streak = (profile.streak || 0) + 1;
  } else {
    // Streak broken (or first study)
    profile.streak = 1;
  }

  if (profile.streak > (profile.longestStreak || 0)) {
    profile.longestStreak = profile.streak;
  }

  profile.lastStudyDate = today;
  return profile;
}

// ── Format helpers ────────────────────────────────────────────────────────────

function formatWord(entry) {
  const ex = entry.ex && entry.ex[0] ? `${entry.ex[0][0]} / ${entry.ex[0][1]}` : '';
  return `${entry.w} | ${entry.p} | ${entry.t} | ${entry.zh}${ex ? ' | ' + ex : ''}`;
}

function formatWordFull(entry) {
  const lines = [`${entry.w} | ${entry.p} | ${entry.t} | ${entry.zh}`];
  if (entry.ex) {
    entry.ex.forEach(([en, zh]) => lines.push(`  例: ${en} | ${zh}`));
  }
  return lines.join('\n');
}

// ── Core function (exportable for cron) ───────────────────────────────────────

function runDailyPush(userId) {
  userId = sanitizeId(userId);
  const profile = loadUser(userId);

  // Update streak
  updateStreak(profile);

  const today      = todayStr();
  const dailyGoal  = profile.preferences && profile.preferences.dailyGoal ? profile.preferences.dailyGoal : 5;
  const dueWords   = getDueWords(profile);
  const newWords   = getNewWordsForUser(profile, dailyGoal);

  // Save updated profile (streak + lastStudyDate)
  saveUser(userId, profile);

  // Format date nicely
  const dateObj = new Date(today + 'T12:00:00Z');
  const dateDisplay = dateObj.toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long',
    timeZone: 'Asia/Shanghai'
  });

  // ── Output ─────────────────────────────────────────────────────────────────
  console.log(`=== 今日英语学习 · ${dateDisplay} ===`);
  console.log(`用户：${profile.name} | 等级：${profile.level} | 连续学习：${profile.streak}天 | 积分：${profile.totalPoints || 0}`);
  console.log('');

  if (dueWords.length > 0) {
    console.log(`【复习】（${dueWords.length}个需要复习的单词）`);
    dueWords.forEach(w => console.log(formatWord(w)));
    console.log('');
  } else {
    console.log('【复习】今日无需复习的单词 ✅');
    console.log('');
  }

  if (newWords.length > 0) {
    console.log(`【今日新词】（目标：${dailyGoal}个）`);
    newWords.forEach(w => console.log(formatWordFull(w)));
    console.log('');
  } else {
    console.log(`【今日新词】当前等级（${profile.level}）的单词已全部学完！请尝试提升等级。`);
    console.log('');
  }

  console.log('【学习建议】');
  console.log('- 先复习旧词，再学新词');
  console.log('- 每个单词至少造一个句子');
  console.log('- 回复"测验"开始今日练习');
  console.log('');
  console.log(`📊 查看进度：node scripts/progress.js ${userId}`);
  console.log(`📝 开始测验：node scripts/quiz.js ${userId}`);
}

// ── CLI entry ─────────────────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  if (!args[0]) {
    console.log('用法: node daily-push.js <userId>');
    process.exit(1);
  }
  runDailyPush(args[0]);
}

module.exports = { runDailyPush };
