#!/usr/bin/env node
/**
 * english-daily — 用户注册脚本（无文件写入版）
 *
 * 档案存放在原生 MEMORY.md 中，由 Agent 维护；本脚本不读写任何文件。
 * 它只做纯计算并输出一段 <!-- english-daily:profile:<userId> --> 区块，
 * 由 Agent 写入 MEMORY.md，跨会话保留。
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

const { getNewWordsForUser, renderMemoryBlock } = require('./wordbank');

const VALID_LEVELS = ['A1', 'A2', 'B1', 'B2'];

// ── Security helpers ──────────────────────────────────────────────────────────

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ 无效的 userId：只允许字母、数字、- 和 _，长度 1-128');
    process.exit(1);
  }
  return value;
}

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

// Count available words at their level (pure compute)
const availableWords = getNewWordsForUser(profile, 9999).length;

console.log(`
✅ 学习档案已生成！

用户ID：${userId}
姓名：  ${name}
等级：  ${level}（目标：${profile.targetLevel}）
每日目标：${dailyGoal} 个新单词

📚 当前等级可学单词：${availableWords} 个
`);

// 输出 MEMORY.md 区块，供 Agent 写入原生记忆（脚本不落盘，符合 clawhub 无文件写入规范）
console.log('📇 请将以下档案写入 MEMORY.md（原生记忆，跨会话保留）：');
console.log('```markdown');
console.log(renderMemoryBlock(profile));
console.log('```');
console.log(`
💡 下一步（把 MEMORY.md 中的 等级/每日目标/SRS进度 作为参数传入脚本）：
   查看今日学习  → node scripts/daily-push.js ${userId} --level ${level} --goal ${dailyGoal} --progress '{}'
   开始测验      → node scripts/quiz.js ${userId} --level ${level} --progress '{}'
   查看进度      → node scripts/progress.js ${userId} --name "${name}" --level ${level} --progress '{}'
   开启每日推送  → node scripts/push-toggle.js on ${userId} --level ${level} --goal ${dailyGoal}
`);

module.exports = { nextLevel };
