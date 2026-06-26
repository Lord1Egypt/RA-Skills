#!/usr/bin/env node
/**
 * daily-brain — 提交答案并显示解析
 * Usage: node scripts/answer.js --answer "B"
 */
const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, '..', 'data');
const puzzles = JSON.parse(fs.readFileSync(path.join(dataDir, 'puzzles.json'), 'utf8'));
const progress = JSON.parse(fs.readFileSync(path.join(dataDir, 'progress.json'), 'utf8'));

const args = process.argv.slice(2);
const getArg = (flag) => { const i = args.indexOf(flag); return i >= 0 ? args[i + 1] : null; };
const userAnswer = getArg('--answer');

if (!userAnswer) {
  console.log('用法: node scripts/answer.js --answer "B"');
  process.exit(1);
}

// Determine today's puzzle (same logic as today.js)
const now = new Date();
const today = now.toISOString().split('T')[0];
const dayOfYear = Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 86400000);
const categories = ['logic', 'math', 'memory', 'word'];
const category = categories[dayOfYear % 4];
const difficulty = progress.currentDifficulty || 'easy';

const pool = puzzles[category].filter(p => p.difficulty === difficulty);
const fallbackPool = pool.length > 0 ? pool : puzzles[category];
const puzzleIndex = dayOfYear % fallbackPool.length;
const puzzle = fallbackPool[puzzleIndex];

// Check answer
const correctAnswer = puzzle.correctedAnswer || puzzle.answer;
const isCorrect = userAnswer.toUpperCase().trim() === correctAnswer.toUpperCase().trim();

// Update progress
const isNewDay = progress.lastPlayedDate !== today;
if (isNewDay) {
  progress.currentStreak = (progress.lastPlayedDate === new Date(now.getTime() - 86400000).toISOString().split('T')[0])
    ? progress.currentStreak + 1 : 1;
}
progress.totalSolved++;
if (isCorrect) progress.correctCount++;
progress.categoryStats[category].solved++;
if (isCorrect) progress.categoryStats[category].correct++;
if (progress.currentStreak > progress.longestStreak) progress.longestStreak = progress.currentStreak;
progress.lastPlayedDate = today;

// Adaptive difficulty
const recentCorrectRate = progress.totalSolved > 0 ? progress.correctCount / progress.totalSolved : 0;
if (recentCorrectRate >= 0.8 && progress.totalSolved >= 3) {
  if (difficulty === 'easy') progress.currentDifficulty = 'medium';
  else if (difficulty === 'medium') progress.currentDifficulty = 'hard';
} else if (recentCorrectRate < 0.4 && progress.totalSolved >= 3) {
  if (difficulty === 'hard') progress.currentDifficulty = 'medium';
  else if (difficulty === 'medium') progress.currentDifficulty = 'easy';
}

// Check achievements
const newAchievements = [];
if (progress.totalSolved === 1 && !progress.achievements.includes('first_solve')) {
  progress.achievements.push('first_solve');
  newAchievements.push({ id: 'first_solve', name: '初试锋芒', desc: '完成第一道脑力题' });
}
if (progress.currentStreak >= 7 && !progress.achievements.includes('week_streak')) {
  progress.achievements.push('week_streak');
  newAchievements.push({ id: 'week_streak', name: '七日不辍', desc: '连续训练7天' });
}
if (progress.currentStreak >= 30 && !progress.achievements.includes('month_streak')) {
  progress.achievements.push('month_streak');
  newAchievements.push({ id: 'month_streak', name: '月度达人', desc: '连续训练30天' });
}
if (recentCorrectRate >= 1.0 && progress.totalSolved >= 5 && !progress.achievements.includes('perfect_five')) {
  progress.achievements.push('perfect_five');
  newAchievements.push({ id: 'perfect_five', name: '五连全对', desc: '连续5题全部答对' });
}

// Save history
progress.history.push({ date: today, puzzleId: puzzle.id, category, difficulty, userAnswer, correct: isCorrect });
if (progress.history.length > 100) progress.history = progress.history.slice(-100);

fs.writeFileSync(path.join(dataDir, 'progress.json'), JSON.stringify(progress, null, 2));

const categoryNames = { logic: '逻辑推理', math: '数学速算', memory: '记忆挑战', word: '文字谜题' };

console.log(`=== DAILY BRAIN — 答案解析 ===
日期：${today}
题目ID：${puzzle.id}
类别：${categoryNames[category]}

用户答案：${userAnswer}
正确答案：${correctAnswer}
结果：${isCorrect ? '✅ 回答正确！' : '❌ 回答错误'}

📖 解析：
${puzzle.explanation}

💡 知识扩展：
${puzzle.knowledge}

📊 当前状态：
- 连续打卡：${progress.currentStreak} 天
- 最长连续：${progress.longestStreak} 天
- 总计完成：${progress.totalSolved} 题
- 总正确率：${Math.round(progress.correctCount / progress.totalSolved * 100)}%
- 当前难度：${progress.currentDifficulty}
${newAchievements.length > 0 ? '\n🏆 新成就解锁！\n' + newAchievements.map(a => `  🎖️ ${a.name} — ${a.desc}`).join('\n') : ''}

请根据以上信息，生成一张精美的答案解析 HTML 卡片：
1. 顶部大字显示 ${isCorrect ? '✅ 答对了！' : '❌ 答错了'}
2. 中间显示正确答案和详细解析
3. 知识扩展区域用不同底色
4. 底部显示打卡统计和成就
5. 支持浅色/深色主题切换
6. 如有新成就，用动画效果高亮展示
`);
