#!/usr/bin/env node
/**
 * daily-brain — 今日脑力训练题目生成器
 * Usage: node scripts/today.js [--difficulty easy|medium|hard] [--category logic|math|memory|word]
 */
const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, '..', 'data');
const puzzles = JSON.parse(fs.readFileSync(path.join(dataDir, 'puzzles.json'), 'utf8'));
const progress = JSON.parse(fs.readFileSync(path.join(dataDir, 'progress.json'), 'utf8'));

// Parse args
const args = process.argv.slice(2);
const getArg = (flag) => { const i = args.indexOf(flag); return i >= 0 ? args[i + 1] : null; };
const difficulty = getArg('--difficulty') || progress.currentDifficulty || 'easy';
const categories = ['logic', 'math', 'memory', 'word'];

// Determine today's category (rotate by day-of-year)
const now = new Date();
const dayOfYear = Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 86400000);
const categoryArg = getArg('--category');
const category = categoryArg && categories.includes(categoryArg) ? categoryArg : categories[dayOfYear % 4];

// Select puzzle using date hash for reproducibility
const pool = puzzles[category].filter(p => p.difficulty === difficulty);
const fallbackPool = pool.length > 0 ? pool : puzzles[category];
const puzzleIndex = dayOfYear % fallbackPool.length;
const puzzle = fallbackPool[puzzleIndex];

const categoryNames = { logic: '逻辑推理', math: '数学速算', memory: '记忆挑战', word: '文字谜题' };
const categoryEmojis = { logic: '🧩', math: '🔢', memory: '🧠', word: '📝' };
const difficultyLabels = { easy: '⭐ 入门', medium: '⭐⭐ 进阶', hard: '⭐⭐⭐ 挑战' };

console.log(`=== DAILY BRAIN — 今日脑力训练 ===
日期：${now.toISOString().split('T')[0]}
题目ID：${puzzle.id}
类别：${categoryEmojis[category]} ${categoryNames[category]}
难度：${difficultyLabels[difficulty]}

请根据以下信息，生成一张精美的脑力训练 HTML 卡片给用户。

📋 题目内容：
${puzzle.question}

📌 选项：
${puzzle.options.join('\n')}

🎨 卡片设计要求：
1. 使用 HTML 格式输出，支持浅色/深色主题切换
2. 顶部显示：日期、类别徽章、难度星标
3. 中间为题目区域，字体清晰易读
4. 选项用卡片式布局，每个选项可点击高亮
5. 底部显示打卡信息：连续 ${progress.currentStreak} 天 | 总计 ${progress.totalSolved} 题 | 正确率 ${progress.totalSolved > 0 ? Math.round(progress.correctCount / progress.totalSolved * 100) : 0}%
6. 配色方案：逻辑=蓝色系, 数学=绿色系, 记忆=紫色系, 文字=橙色系
7. 包含"提交答案"按钮提示

⚠️ 不要在卡片中显示答案！答案将在用户提交后通过 answer.js 揭晓。

📊 用户当前状态：
- 连续打卡：${progress.currentStreak} 天
- 最长连续：${progress.longestStreak} 天
- 当前难度：${difficulty}
- ${categoryNames[category]}正确率：${progress.categoryStats[category].solved > 0 ? Math.round(progress.categoryStats[category].correct / progress.categoryStats[category].solved * 100) : 0}%
`);
