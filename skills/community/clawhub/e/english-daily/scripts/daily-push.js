#!/usr/bin/env node
/**
 * english-daily — 每日学习推送 prompt 生成器（无文件写入版）
 *
 * 由 openclaw cron 驱动，每日早晨执行。档案与 SRS 进度存于原生 MEMORY.md，
 * 由 Agent 维护；本脚本不读写任何文件，所需字段由 Agent 作为参数传入。
 * 脚本更新连续学习(streak)后，输出一段 MEMORY.md 区块供 Agent 回写。
 *
 * 用法:
 *   node daily-push.js <userId> [--name <姓名>] [--level A1|A2|B1|B2] \
 *        [--goal <每日目标>] [--progress '<wordProgress-JSON>'] \
 *        [--streak <n>] [--longest <n>] [--last <YYYY-MM-DD>] [--points <n>]
 */

'use strict';

const {
  getDueWords,
  getNewWordsForUser,
  parseProgressArg,
  renderMemoryBlock,
  todayStr,
  addDays
} = require('./wordbank');

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

// ── Streak update (pure) ────────────────────────────────────────────────────────

function updateStreak(profile) {
  const today     = todayStr();
  const yesterday = addDays(today, -1);
  const last      = profile.lastStudyDate;

  if (last === today) {
    return profile; // already counted today
  } else if (last === yesterday) {
    profile.streak = (profile.streak || 0) + 1;
  } else {
    profile.streak = 1; // broken or first study
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

// ── Core function ───────────────────────────────────────────────────────────────

function runDailyPush(userId, opts = {}) {
  userId = sanitizeId(userId);

  const profile = {
    userId,
    name:          opts.name || userId,
    level:         opts.level || 'B1',
    targetLevel:   opts.targetLevel || opts.level || 'B1',
    nativeLanguage: 'zh',
    streak:        opts.streak || 0,
    longestStreak: opts.longest || 0,
    lastStudyDate: opts.last || null,
    totalPoints:   opts.points || 0,
    preferences: {
      dailyGoal: opts.goal || 5,
      pushEnabled: !!opts.pushEnabled,
      morningTime: opts.morningTime || '08:00',
      channel: opts.channel || 'telegram'
    },
    wordProgress: parseProgressArg(opts.progress)
  };

  // Update streak (pure compute)
  updateStreak(profile);

  const today      = todayStr();
  const dailyGoal  = profile.preferences.dailyGoal;
  const dueWords   = getDueWords(profile);
  const newWords   = getNewWordsForUser(profile, dailyGoal);

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

  // 输出更新后的 MEMORY.md 区块（streak / lastStudyDate 已更新），供 Agent 回写
  console.log('📇 请用以下区块更新 MEMORY.md（已更新连续学习天数）：');
  console.log('```markdown');
  console.log(renderMemoryBlock(profile));
  console.log('```');
  console.log('');
  console.log(`📊 查看进度：node scripts/progress.js ${userId} --name "${profile.name}" --level ${profile.level} --progress '<SRS进度JSON>'`);
  console.log(`📝 开始测验：node scripts/quiz.js ${userId} --level ${profile.level} --progress '<SRS进度JSON>'`);
}

// ── CLI entry ─────────────────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  if (!args[0]) {
    console.log(`用法: node daily-push.js <userId> [--name <姓名>] [--level A1|A2|B1|B2] [--goal <n>] [--progress '<JSON>'] [--streak <n>] [--longest <n>] [--last <YYYY-MM-DD>] [--points <n>]`);
    process.exit(1);
  }
  const num = v => (v === undefined ? undefined : parseInt(v, 10));
  runDailyPush(args[0], {
    name:    flag(args, '--name'),
    level:   flag(args, '--level'),
    goal:    num(flag(args, '--goal')),
    progress: flag(args, '--progress'),
    streak:  num(flag(args, '--streak')),
    longest: num(flag(args, '--longest')),
    last:    flag(args, '--last'),
    points:  num(flag(args, '--points'))
  });
}

module.exports = { runDailyPush, updateStreak };
