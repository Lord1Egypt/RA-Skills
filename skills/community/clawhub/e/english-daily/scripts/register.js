#!/usr/bin/env node
/**
 * english-daily — 用户注册脚本
 *
 * 用法:
 *   node register.js <userId> <name> [level] [dailyGoal]
 *
 * 参数:
 *   userId     - 用户ID（字母/数字/连字符/下划线，1-128字符）
 *   name       - 用户名称
 *   level      - 起始等级 A1/A2/B1/B2（默认 B1）
 *   dailyGoal  - 每日新单词目标 1-20（默认 5）
 *
 * 示例:
 *   node register.js 123456 张三
 *   node register.js 123456 张三 A2 8
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const { getWordsByLevel, getNewWordsForUser } = require('./wordbank');

const USERS_DIR = path.join(__dirname, '../data/users');

const VALID_LEVELS = ['A1', 'A2', 'B1', 'B2'];

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

// ── I/O helpers ───────────────────────────────────────────────────────────────

function saveUser(userId, data) {
  fs.mkdirSync(USERS_DIR, { recursive: true });
  fs.writeFileSync(safeUserPath(userId), JSON.stringify(data, null, 2), 'utf8');
}

function loadUser(userId) {
  const f = safeUserPath(userId);
  if (!fs.existsSync(f)) return null;
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

// ── Target level map ──────────────────────────────────────────────────────────

function nextLevel(level) {
  const idx = VALID_LEVELS.indexOf(level);
  return idx < VALID_LEVELS.length - 1 ? VALID_LEVELS[idx + 1] : level;
}

// ── Main ──────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);

if (args.length < 2) {
  console.log(`
用法:
  node register.js <userId> <name> [level] [dailyGoal]

参数:
  userId     用户ID（字母/数字/连字符/下划线，1-128字符）
  name       用户名称
  level      起始等级 A1/A2/B1/B2（默认 B1）
  dailyGoal  每日新单词目标 1-20（默认 5）

示例:
  node register.js telegram_123 张三
  node register.js telegram_123 张三 A2 8
`);
  process.exit(1);
}

const rawId      = args[0];
const rawName    = args[1];
const rawLevel   = (args[2] || 'B1').toUpperCase();
const rawGoal    = args[3];

// Validate
const userId = sanitizeId(rawId);

if (!rawName || rawName.trim().length === 0) {
  console.error('❌ 用户名称不能为空');
  process.exit(1);
}
const name = rawName.trim().slice(0, 64);

if (!VALID_LEVELS.includes(rawLevel)) {
  console.error(`❌ 无效的等级：${rawLevel}。支持：${VALID_LEVELS.join('/')}`);
  process.exit(1);
}
const level = rawLevel;

let dailyGoal = 5;
if (rawGoal !== undefined) {
  dailyGoal = parseInt(rawGoal, 10);
  if (isNaN(dailyGoal) || dailyGoal < 1 || dailyGoal > 20) {
    console.error('❌ dailyGoal 必须是 1-20 的整数');
    process.exit(1);
  }
}

// Check existing
const existing = loadUser(userId);
if (existing) {
  console.log(`⚠️  用户 ${userId} 已存在（${existing.name}，等级 ${existing.level}）`);
  console.log('如需更新，请直接修改 data/users/<userId>.json 或重新注册（将覆盖原有进度）。');
  process.exit(0);
}

const now = new Date().toISOString();

const profile = {
  userId,
  name,
  level,
  targetLevel: nextLevel(level),
  nativeLanguage: 'zh',
  streak: 0,
  longestStreak: 0,
  lastStudyDate: null,
  totalPoints: 0,
  wordsLearned: 0,
  preferences: {
    dailyGoal,
    pushEnabled: false,
    morningTime: '08:00',
    channel: 'telegram'
  },
  wordProgress: {},
  createdAt: now
};

saveUser(userId, profile);

// Count available words at their level
const availableWords = getNewWordsForUser(profile, 9999).length;

console.log(`
✅ 注册成功！

用户ID：${userId}
姓名：  ${name}
等级：  ${level}（目标：${profile.targetLevel}）
每日目标：${dailyGoal} 个新单词

📚 当前等级可学单词：${availableWords} 个

💡 下一步：
   查看今日学习  → node scripts/daily-push.js ${userId}
   开始测验      → node scripts/quiz.js ${userId}
   查看进度      → node scripts/progress.js ${userId}
   开启每日推送  → node scripts/push-toggle.js on ${userId}
`);

module.exports = { saveUser, loadUser, sanitizeId, safeUserPath };
