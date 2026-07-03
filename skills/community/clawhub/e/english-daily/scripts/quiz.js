#!/usr/bin/env node
/**
 * english-daily — 测验/练习生成器（无文件写入版）
 *
 * 档案与 SRS 进度存于原生 MEMORY.md，由 Agent 维护；本脚本不读写任何文件。
 * 测验题目为纯计算生成；记分时脚本更新 SRS 进度后，输出一段 MEMORY.md
 * 区块供 Agent 回写。
 *
 * 用法:
 *   node quiz.js <userId> [type] [--level A1|A2|B1|B2] [--progress '<JSON>']
 *   node quiz.js <userId> --score <points> [--name <姓名>] [--level ...] \
 *        [--progress '<JSON>'] [--streak <n>] [--longest <n>] [--points <n>] \
 *        [--goal <n>] [--last <YYYY-MM-DD>]
 *
 * type: vocab | sentence | mixed（默认 mixed）
 *
 * 生成5道题（含答案），由 Claude 逐题互动呈现。
 * 答题完成后 Claude 调用：node quiz.js <userId> --score <points> --progress '<JSON>' ...
 */

'use strict';

const path = require('path');
const {
  getNewWordsForUser,
  updateWordProgress,
  loadWordBank,
  parseProgressArg,
  renderMemoryBlock,
  todayStr
} = require('./wordbank');

const QUESTIONS_PER_QUIZ = 5;
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

// ── Helpers ───────────────────────────────────────────────────────────────────

/** Simple deterministic pseudo-shuffle based on date + userId seed */
function shuffle(arr, seed) {
  const a = arr.slice();
  let s = seed;
  for (let i = a.length - 1; i > 0; i--) {
    s = ((s * 1664525) + 1013904223) & 0xffffffff;
    const j = Math.abs(s) % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function dateSeed(userId) {
  const today = todayStr().replace(/-/g, '');
  let hash = 0;
  const str = userId + today;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

/** Get the pool of words a user has studied + due words + new words */
function getQuizPool(profile) {
  const bank = loadWordBank();
  const progress = profile.wordProgress || {};

  const studied = bank.filter(w => !!progress[w.w]);

  let pool = studied.length >= QUESTIONS_PER_QUIZ
    ? studied
    : [...studied, ...getNewWordsForUser(profile, QUESTIONS_PER_QUIZ - studied.length)];

  const seen = new Set();
  pool = pool.filter(w => {
    if (seen.has(w.w)) return false;
    seen.add(w.w);
    return true;
  });

  return { pool };
}

/** Pick wrong answers for multiple choice (3 distractors) */
function getDistractors(correctEntry, bank, seed) {
  const others = bank.filter(w => w.w !== correctEntry.w && w.zh !== correctEntry.zh);
  const shuffled = shuffle(others, seed + 1);
  return shuffled.slice(0, 3).map(w => w.zh);
}

/** Build a vocab question (word → Chinese, multiple choice) */
function buildVocabQuestion(entry, bank, qNum, seed) {
  const distractors = getDistractors(entry, bank, seed + qNum);
  const options = shuffle([entry.zh, ...distractors], seed + qNum * 13);
  const correctIdx = options.indexOf(entry.zh);
  const labels = ['A', 'B', 'C', 'D'];

  const optionStr = options.map((o, i) => `${labels[i]}. ${o}`).join('  ');
  const answer    = labels[correctIdx];
  const example   = entry.ex && entry.ex[0] ? entry.ex[0][0] : '';

  return {
    type: 'vocab',
    word: entry.w,
    question: `Q${qNum}. What does "${entry.w}" mean?\n${entry.p}  ${entry.t}\n${optionStr}`,
    answer: `Answer: ${answer} | 解析: ${entry.w} = ${entry.zh}${example ? '，例：' + example : ''}`
  };
}

/** Build a sentence (fill-in-the-blank) question */
function buildSentenceQuestion(entry, qNum) {
  const exPair = entry.ex && entry.ex.length > 0 ? entry.ex[0] : null;
  if (!exPair) {
    return {
      type: 'sentence',
      word: entry.w,
      question: `Q${qNum}. 用 "${entry.zh}" 填空：_____ is important in life.\n（提示：${entry.p}  ${entry.t}）`,
      answer: `Answer: ${entry.w} | 全句: ${entry.w} is important in life.`
    };
  }

  const [enSentence, zhSentence] = exPair;
  const wordLower = entry.w.toLowerCase();
  const regex     = new RegExp(`\\b${wordLower}(?:ed|ing|s|d|es)?\\b`, 'i');
  const match     = enSentence.match(regex);

  if (!match) {
    return {
      type: 'sentence',
      word: entry.w,
      question: `Q${qNum}. 翻译成英文（${zhSentence}）\n（提示：核心词 = ${entry.zh}，${entry.p}）`,
      answer: `Answer: ${entry.w} | 参考译文: ${enSentence}`
    };
  }

  const blanked = enSentence.replace(match[0], '_____');
  return {
    type: 'sentence',
    word: entry.w,
    question: `Q${qNum}. 填空 (${entry.zh})：\n${blanked}\n中文提示：${zhSentence}`,
    answer: `Answer: ${match[0]} | 全句: ${enSentence}`
  };
}

/** Generate quiz questions */
function generateQuiz(profile, type, seed) {
  const bank = loadWordBank();
  const { pool } = getQuizPool(profile);

  if (pool.length < QUESTIONS_PER_QUIZ) {
    return null;
  }

  const words   = shuffle(pool, seed).slice(0, QUESTIONS_PER_QUIZ);
  const questions = [];

  words.forEach((entry, idx) => {
    const qNum = idx + 1;
    let q;
    if (type === 'vocab') {
      q = buildVocabQuestion(entry, bank, qNum, seed);
    } else if (type === 'sentence') {
      q = buildSentenceQuestion(entry, qNum);
    } else {
      q = idx % 2 === 0
        ? buildVocabQuestion(entry, bank, qNum, seed)
        : buildSentenceQuestion(entry, qNum);
    }
    questions.push(q);
  });

  return { words: words.map(w => w.w), questions };
}

// ── Score recording (pure — prints MEMORY.md block, no fs) ──────────────────────

function buildProfileFromArgs(userId, args) {
  const num = v => (v === undefined ? undefined : parseInt(v, 10));
  let level = (flag(args, '--level') || 'B1').toUpperCase();
  if (!VALID_LEVELS.includes(level)) level = 'B1';
  return {
    userId,
    name:          flag(args, '--name') || userId,
    level,
    targetLevel:   flag(args, '--target') || level,
    nativeLanguage: 'zh',
    streak:        num(flag(args, '--streak')) || 0,
    longestStreak: num(flag(args, '--longest')) || 0,
    lastStudyDate: flag(args, '--last') || null,
    totalPoints:   num(flag(args, '--points')) || 0,
    preferences: {
      dailyGoal: num(flag(args, '--goal')) || 5,
      pushEnabled: false, morningTime: '08:00', channel: 'telegram'
    },
    wordProgress:  parseProgressArg(flag(args, '--progress'))
  };
}

function recordScore(userId, rawPoints, args) {
  userId = sanitizeId(userId);
  const points = parseInt(rawPoints, 10);
  if (isNaN(points) || points < 0 || points > 500) {
    console.error('❌ 无效积分值（0-500）');
    process.exit(1);
  }

  const profile = buildProfileFromArgs(userId, args);
  profile.totalPoints = (profile.totalPoints || 0) + points;

  const correct = Math.round(points / 10);

  // Update word quality for the quiz words (same deterministic pool as generation)
  const { pool } = getQuizPool(profile);
  const seed = dateSeed(userId);
  const quizWords = shuffle(pool, seed).slice(0, QUESTIONS_PER_QUIZ).map(w => w.w);

  quizWords.forEach((word, idx) => {
    const quality = idx < correct ? 3 : 1;
    updateWordProgress(profile, word, quality);
  });

  profile.wordsLearned = Object.keys(profile.wordProgress).length;

  console.log(`
✅ 本次得分：+${points}分
累计积分：${profile.totalPoints}分
已掌握单词：${profile.wordsLearned}个

继续加油！🎉
`);

  // 输出更新后的 MEMORY.md 区块（积分 + SRS进度已更新），供 Agent 回写
  console.log('📇 请用以下区块更新 MEMORY.md（积分与 SRS 进度已更新）：');
  console.log('```markdown');
  console.log(renderMemoryBlock(profile));
  console.log('```');
}

// ── CLI entry ─────────────────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);

  if (!args[0]) {
    console.log(`用法:
  node quiz.js <userId> [type] [--level A1|A2|B1|B2] [--progress '<JSON>']   生成测验（type: vocab/sentence/mixed）
  node quiz.js <userId> --score <pts> --level ... --progress '<JSON>' ...    记录本次得分（10分/题）`);
    process.exit(1);
  }

  // --score mode
  const scoreIdx = args.indexOf('--score');
  if (scoreIdx !== -1) {
    const pts = args[scoreIdx + 1];
    if (!pts) {
      console.error('❌ --score 后需要跟积分数值');
      process.exit(1);
    }
    recordScore(args[0], pts, args);
    process.exit(0);
  }

  // Generate quiz
  const userId = sanitizeId(args[0]);
  const rawType = (args[1] && !args[1].startsWith('--') ? args[1] : 'mixed').toLowerCase();
  const validTypes = ['vocab', 'sentence', 'mixed'];
  if (!validTypes.includes(rawType)) {
    console.error(`❌ 无效的测验类型：${rawType}。支持：${validTypes.join('/')}`);
    process.exit(1);
  }

  const profile = buildProfileFromArgs(userId, args);
  const seed    = dateSeed(userId);
  const quiz    = generateQuiz(profile, rawType, seed);

  if (!quiz) {
    console.log(`
❌ 单词量不足（需要至少 ${QUESTIONS_PER_QUIZ} 个已学单词或新单词）。
请先完成今日学习：node daily-push.js ${userId} --level ${profile.level} --goal ${profile.preferences.dailyGoal} --progress '<JSON>'
`);
    process.exit(0);
  }

  const typeNames = { vocab: '词义选择', sentence: '句子填空', mixed: '综合练习' };
  console.log(`
📝 英语测验 — ${profile.name}（${profile.level}）
类型：${typeNames[rawType]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);

  quiz.questions.forEach(q => {
    console.log(q.question);
    console.log(q.answer);
    console.log('');
  });

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('【Claude 操作指南】');
  console.log('请将以上题目逐题呈现给用户，等待回答后再显示答案。');
  console.log('所有题目完成后，根据正确题数运行以下命令记录积分（带上 MEMORY.md 里的进度）：');
  console.log(`  node ${path.join(__dirname, 'quiz.js')} ${userId} --score <正确题数×10> --level ${profile.level} --progress '<SRS进度JSON>' --points ${profile.totalPoints}`);
  console.log('例如答对3题：--score 30');
  console.log('脚本会输出更新后的 MEMORY.md 区块，请回写到原生记忆。');
}

module.exports = { generateQuiz, recordScore };
