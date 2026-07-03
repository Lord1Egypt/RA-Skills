#!/usr/bin/env node
/**
 * english-daily — 学习进度查看（无文件写入版）
 *
 * 档案与 SRS 进度存于原生 MEMORY.md，由 Agent 维护；本脚本不读写任何文件。
 * 所需字段由 Agent 作为参数传入。若发生升级，脚本会输出一段更新后的
 * MEMORY.md 区块供 Agent 回写；否则只做纯展示。
 *
 * 用法:
 *   node progress.js <userId> [--name <姓名>] [--level A1|A2|B1|B2] \
 *        [--progress '<wordProgress-JSON>'] [--streak <n>] [--longest <n>] \
 *        [--points <n>] [--goal <n>] [--last <YYYY-MM-DD>]
 */

'use strict';

const {
  getWordStats,
  loadWordBank,
  parseProgressArg,
  renderMemoryBlock
} = require('./wordbank');

const VALID_LEVELS = ['A1', 'A2', 'B1', 'B2'];

// ── Security helpers ──────────────────────────────────────────────────────────

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ 无效的 userId：只允许字母、数字、- 和 _，长度 1-128');
    process.exit(1);
  }
  return value;
}

function flag(args, name) {
  const i = args.indexOf(name);
  return (i !== -1 && args[i + 1] !== undefined) ? args[i + 1] : undefined;
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
  return stats.mastered >= threshold.wordsNeeded ? threshold.next : false;
}

function getWeeklyDays(profile) {
  const streak = profile.streak || 0;
  return Math.min(streak, 7);
}

function wordsToNextLevel(profile) {
  const threshold = LEVEL_UP[profile.level];
  if (!threshold || !threshold.next) return 0;
  const stats = getWordStats(profile);
  return Math.max(0, threshold.wordsNeeded - stats.mastered);
}

// ── Main ──────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (!args[0]) {
  console.log(`用法: node progress.js <userId> [--name <姓名>] [--level A1|A2|B1|B2] [--progress '<JSON>'] [--streak <n>] [--longest <n>] [--points <n>] [--goal <n>] [--last <YYYY-MM-DD>]`);
  process.exit(1);
}

const userId = sanitizeId(args[0]);
const num = v => (v === undefined ? undefined : parseInt(v, 10));

let level = (flag(args, '--level') || 'B1').toUpperCase();
if (!VALID_LEVELS.includes(level)) level = 'B1';

const profile = {
  userId,
  name:          flag(args, '--name') || userId,
  level,
  nativeLanguage: 'zh',
  streak:        num(flag(args, '--streak')) || 0,
  longestStreak: num(flag(args, '--longest')) || 0,
  lastStudyDate: flag(args, '--last') || null,
  totalPoints:   num(flag(args, '--points')) || 0,
  preferences: { dailyGoal: num(flag(args, '--goal')) || 5, pushEnabled: false, morningTime: '08:00', channel: 'telegram' },
  wordProgress:  parseProgressArg(flag(args, '--progress'))
};
profile.targetLevel = LEVEL_UP[profile.level] ? LEVEL_UP[profile.level].next || profile.level : profile.level;

// Check for level-up (pure compute — no persistence; agent updates MEMORY.md)
let leveledUp = false;
const newLevel = checkLevelUp(profile);
if (newLevel) {
  leveledUp = true;
  console.log(`\n🎉 恭喜！你已升级至 ${newLevel}！`);
  profile.level = newLevel;
  profile.targetLevel = LEVEL_UP[newLevel] ? LEVEL_UP[newLevel].next || newLevel : newLevel;
  console.log(`等级已更新：→ ${profile.level}（目标 ${profile.targetLevel}）\n`);
}

const stats      = getWordStats(profile);
const bank       = loadWordBank();
const allAtLevel = bank.filter(w =>
  VALID_LEVELS.indexOf(w.lv) <= VALID_LEVELS.indexOf(profile.level)
).length;

const weeklyDays  = getWeeklyDays(profile);
const toNextLevel = wordsToNextLevel(profile);
const threshold   = LEVEL_UP[profile.level];

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
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);

if (leveledUp) {
  console.log('\n📇 你升级了！请用以下区块更新 MEMORY.md（等级已变化）：');
  console.log('```markdown');
  console.log(renderMemoryBlock(profile));
  console.log('```');
}

console.log(`
开始今日学习：node scripts/daily-push.js ${userId} --level ${profile.level} --goal ${profile.preferences.dailyGoal} --progress '<SRS进度JSON>'
开始测验：    node scripts/quiz.js ${userId} --level ${profile.level} --progress '<SRS进度JSON>'
`);
