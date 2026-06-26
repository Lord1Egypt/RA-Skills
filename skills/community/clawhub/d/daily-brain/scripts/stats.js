#!/usr/bin/env node
/**
 * daily-brain — 训练统计面板
 * Usage: node scripts/stats.js
 */
const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, '..', 'data');
const progress = JSON.parse(fs.readFileSync(path.join(dataDir, 'progress.json'), 'utf8'));

const categoryNames = { logic: '逻辑推理', math: '数学速算', memory: '记忆挑战', word: '文字谜题' };
const achievementDefs = {
  first_solve: { name: '初试锋芒', emoji: '🌟', desc: '完成第一道脑力题' },
  week_streak: { name: '七日不辍', emoji: '🔥', desc: '连续训练7天' },
  month_streak: { name: '月度达人', emoji: '👑', desc: '连续训练30天' },
  perfect_five: { name: '五连全对', emoji: '💎', desc: '连续5题全部答对' }
};

const overallRate = progress.totalSolved > 0 ? Math.round(progress.correctCount / progress.totalSolved * 100) : 0;

const catStats = Object.entries(progress.categoryStats).map(([key, val]) => {
  const rate = val.solved > 0 ? Math.round(val.correct / val.solved * 100) : 0;
  return `  ${categoryNames[key]}：${val.solved} 题，正确率 ${rate}%`;
}).join('\n');

const earnedAchievements = progress.achievements.map(id => {
  const def = achievementDefs[id];
  return def ? `  ${def.emoji} ${def.name} — ${def.desc}` : `  🎖️ ${id}`;
}).join('\n') || '  暂无成就，继续加油！';

console.log(`=== DAILY BRAIN — 训练统计 ===

请根据以下数据，生成一张精美的统计面板 HTML 卡片：

📊 总览：
- 总计完成：${progress.totalSolved} 题
- 总正确率：${overallRate}%
- 连续打卡：${progress.currentStreak} 天
- 最长连续：${progress.longestStreak} 天
- 当前难度：${progress.currentDifficulty}

📈 分类统计：
${catStats}

🏆 已获成就：
${earnedAchievements}

🎨 面板设计要求：
1. HTML 格式，支持浅色/深色主题切换 + 字体大小控件
2. 用圆形进度条展示总正确率
3. 用柱状图展示四类题目的完成数量
4. 连续天数用火焰图标强调
5. 成就徽章用金色/银色质感卡片展示
6. 底部显示"今日还未训练"或"今日已完成"状态
7. 配色方案：逻辑=蓝, 数学=绿, 记忆=紫, 文字=橙

上次训练日期：${progress.lastPlayedDate || '从未训练'}
`);
