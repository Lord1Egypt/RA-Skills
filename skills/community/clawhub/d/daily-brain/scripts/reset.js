#!/usr/bin/env node
/**
 * daily-brain — 重置进度
 * Usage: node scripts/reset.js --confirm
 */
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
if (!args.includes('--confirm')) {
  console.log('⚠️ 此操作将清除所有训练进度、打卡记录和成就。');
  console.log('确认重置请运行: node scripts/reset.js --confirm');
  process.exit(0);
}

const dataDir = path.join(__dirname, '..', 'data');
const initial = {
  currentStreak: 0,
  longestStreak: 0,
  totalSolved: 0,
  correctCount: 0,
  currentDifficulty: "easy",
  categoryStats: {
    logic: { solved: 0, correct: 0 },
    math: { solved: 0, correct: 0 },
    memory: { solved: 0, correct: 0 },
    word: { solved: 0, correct: 0 }
  },
  lastPlayedDate: null,
  achievements: [],
  history: []
};

fs.writeFileSync(path.join(dataDir, 'progress.json'), JSON.stringify(initial, null, 2));
console.log('✅ 训练进度已重置。所有数据已清零。');
