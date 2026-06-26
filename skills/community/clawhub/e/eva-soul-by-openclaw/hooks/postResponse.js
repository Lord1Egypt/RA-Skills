/**
 * Post-Response Hook - 回复后自动记忆和情感更新
 */

const fs = require('fs');
const path = require('path');
const { fetchWithRetry } = require('./errorHandler');
const logger = require('./logger');

const SILICONFLOW_KEY = process.env.SILICONFLOW_API_KEY;

// 对话压缩配置
const COMPRESS_CONFIG = {
  triggerTurns: 20,       // 每 N 轮触发一次压缩
  keepRecentTurns: 5,     // 压缩后保留最近 N 轮
  summaryMaxAge: 30,      // 摘要保质期（天）
  summariesFile: 'conversations/summaries.json'
};

const MEMORY_CONFIG = {
  short: { file: 'short/short.json', days: 7 },
  medium: { file: 'medium/medium.json', days: 30 },
  long: { file: 'long/long.json', days: 90 }
};

// ============================================================
// 对话轮次计数器
// ============================================================

function getTurnCount(memoryPath) {
  const counterFile = path.join(memoryPath, 'conversations', '.turn_counter.json');
  if (fs.existsSync(counterFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(counterFile, 'utf8'));
      return data.turns || 0;
    } catch (e) {
      return 0;
    }
  }
  return 0;
}

function incrementTurnCount(memoryPath) {
  const counterFile = path.join(memoryPath, 'conversations', '.turn_counter.json');
  const dir = path.dirname(counterFile);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  let data = { turns: 0, lastCompress: null };
  if (fs.existsSync(counterFile)) {
    try { data = JSON.parse(fs.readFileSync(counterFile, 'utf8')); } catch (e) {}
  }
  data.turns = (data.turns || 0) + 1;
  fs.writeFileSync(counterFile, JSON.stringify(data, null, 2));
  return data.turns;
}

// ============================================================
// 对话压缩核心逻辑
// ============================================================

/**
 * 提取对话中的关键信息，生成摘要
 */
function extractKeyInfo(dialogues) {
  const facts = [];
  const decisions = [];
  const emotions = [];
  const tasks = [];
  const preferences = [];

  const keywordMap = {
    fact:    ['记得', '记住', '我是', '我叫', '生日', '住', '在', '来自'],
    decision: ['决定', '选择', '安排', '计划', '同意', '就这样', '算了', '不再'],
    task:    ['帮我', '提醒', '记得', '别忘了', '下次', '待会'],
    preference: ['喜欢', '讨厌', '爱吃', '怕', '想要', '不要', 'prefer', 'hate']
  };

  for (const d of dialogues) {
    const text = (d.content || '').toLowerCase();
    for (const kw of keywordMap.fact)    if (text.includes(kw)) facts.push(text);
    for (const kw of keywordMap.decision)  if (text.includes(kw)) decisions.push(text);
    for (const kw of keywordMap.task)    if (text.includes(kw)) tasks.push(text);
    for (const kw of keywordMap.preference) if (text.includes(kw)) preferences.push(text);
  }

  // 去重 + 截断
  const dedup = arr => [...new Set(arr)].slice(0, 3).map(t => t.replace(/^(user:|assistant:)/, '').trim());

  return {
    facts:      dedup(facts),
    decisions:  dedup(decisions),
    tasks:     dedup(tasks),
    preferences: dedup(preferences)
  };
}

/**
 * 生成压缩摘要文本
 */
function buildSummaryText(info, turns, startTime, endTime) {
  const lines = [
    `【对话摘要 | ${turns}轮 | ${startTime} → ${endTime}】`
  ];

  if (info.facts.length > 0) {
    lines.push('🔑 关键事实:');
    info.facts.forEach(f => lines.push(`  - ${f}`));
  }
  if (info.decisions.length > 0) {
    lines.push('✅ 决策/结论:');
    info.decisions.forEach(d => lines.push(`  - ${d}`));
  }
  if (info.tasks.length > 0) {
    lines.push('📌 待办/提醒:');
    info.tasks.forEach(t => lines.push(`  - ${t}`));
  }
  if (info.preferences.length > 0) {
    lines.push('💡 偏好/习惯:');
    info.preferences.forEach(p => lines.push(`  - ${p}`));
  }
  if (lines.length === 1) {
    lines.push('（本次对话以闲聊为主，无特殊摘要');
  }

  return lines.join('\n');
}

/**
 * 压缩对话：读取短期对话 → 生成摘要 → 存入长期记忆 → 删除已压缩对话
 */
async function compressConversations(memoryPath) {
  const shortFile = path.join(memoryPath, 'short', 'short.json');
  if (!fs.existsSync(shortFile)) return null;

  let dialogues = [];
  try {
    dialogues = JSON.parse(fs.readFileSync(shortFile, 'utf8'));
  } catch (e) {
    return null;
  }

  if (dialogues.length <= COMPRESS_CONFIG.keepRecentTurns * 2) {
    return null; // 对话不够，不压缩
  }

  // 取最近 COMPRESS_CONFIG.keepRecentTurns*2 轮之前的所有对话
  const toCompress = dialogues.slice(0, -COMPRESS_CONFIG.keepRecentTurns * 2);
  const toKeep    = dialogues.slice(-COMPRESS_CONFIG.keepRecentTurns * 2);

  if (toCompress.length === 0) return null;

  const startTime = toCompress[0].timestamp
    ? new Date(toCompress[0].timestamp).toLocaleString('zh-CN')
    : 'unknown';
  const endTime = toCompress[toCompress.length - 1].timestamp
    ? new Date(toCompress[toCompress.length - 1].timestamp).toLocaleString('zh-CN')
    : 'unknown';

  // 提取关键信息
  const info = extractKeyInfo(toCompress);
  const summaryText = buildSummaryText(info, toCompress.length, startTime, endTime);

  // 保存摘要到长期记忆
  const summariesFile = path.join(memoryPath, COMPRESS_CONFIG.summariesFile);
  const summariesDir = path.dirname(summariesFile);
  if (!fs.existsSync(summariesDir)) fs.mkdirSync(summariesDir, { recursive: true });

  let summaries = [];
  if (fs.existsSync(summariesFile)) {
    try { summaries = JSON.parse(fs.readFileSync(summariesFile, 'utf8')); } catch (e) {}
  }

  const summaryEntry = {
    id: `summary_${Date.now()}`,
    content: summaryText,
    turns: toCompress.length,
    startTime: toCompress[0].timestamp,
    endTime: toCompress[toCompress.length - 1].timestamp,
    importance: 7,
    type: 'conversation_summary',
    createdAt: new Date().toISOString()
  };

  summaries.push(summaryEntry);
  // 保留最近30个摘要
  if (summaries.length > 30) summaries = summaries.slice(-30);
  fs.writeFileSync(summariesFile, JSON.stringify(summaries, null, 2));

  // 覆盖短期对话文件，只保留最近的
  fs.writeFileSync(shortFile, JSON.stringify(toKeep, null, 2));

  // 重置轮次计数器
  const counterFile = path.join(memoryPath, 'conversations', '.turn_counter.json');
  if (fs.existsSync(counterFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(counterFile, 'utf8'));
      data.turns = COMPRESS_CONFIG.keepRecentTurns * 2;
      data.lastCompress = new Date().toISOString();
      fs.writeFileSync(counterFile, JSON.stringify(data, null, 2));
    } catch (e) {}
  }

  logger.hook(
    `对话压缩完成: ${toCompress.length}轮 → 摘要已存入长期记忆，当前保留${toKeep.length}轮`,
    'postResponse'
  );

  return { compressed: toCompress.length, kept: toKeep.length, summaryId: summaryEntry.id };
}

/**
 * 手动触发压缩（供 eva_compress 工具调用）
 */
async function manualCompress(memoryPath) {
  return compressConversations(memoryPath);
}

/**
 * 获取压缩摘要列表
 */
function getSummaries(memoryPath, limit = 10) {
  const summariesFile = path.join(memoryPath, COMPRESS_CONFIG.summariesFile);
  if (!fs.existsSync(summariesFile)) return [];
  try {
    const data = JSON.parse(fs.readFileSync(summariesFile, 'utf8'));
    return data.slice(-limit).reverse();
  } catch (e) {
    return [];
  }
}

// ============================================================
// 向量生成
// ============================================================

async function generateEmbedding(text) {
  if (!SILICONFLOW_KEY) return null;
  try {
    const response = await fetchWithRetry('https://api.siliconflow.cn/v1/embeddings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${SILICONFLOW_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ model: 'BAAI/bge-m3', input: text })
    });
    const data = await response.json();
    return data.data?.[0]?.embedding || null;
  } catch (e) {
    logger.hookWarn(`Embedding error: ${e.message}`, 'postResponse');
    return null;
  }
}

// ============================================================
// 保存对话到记忆
// ============================================================

async function saveDialogueToShortTerm(memoryPath, userMsg, assistantMsg) {
  const file = path.join(memoryPath, 'short', 'short.json');
  let memories = [];
  if (fs.existsSync(file)) {
    try { memories = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) {}
  }
  memories.push({
    id: `mem_${Date.now()}`,
    content: `user: ${userMsg}\nassistant: ${assistantMsg}`,
    timestamp: new Date().toISOString(),
    type: 'dialogue'
  });
  fs.writeFileSync(file, JSON.stringify(memories, null, 2));
}

async function saveConversationToStore(memoryPath, userMsg, assistantMsg) {
  try {
    const storePath = path.join(memoryPath, 'conversations');
    const rawDir = path.join(storePath, 'raw');
    const vecDir = path.join(storePath, 'vectors');
    [storePath, rawDir, vecDir].forEach(d => { if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true }); });

    const id = `conv_${Date.now()}`;
    const messages = [
      { role: 'user', content: userMsg },
      { role: 'assistant', content: assistantMsg }
    ];

    // 保存原始
    fs.writeFileSync(path.join(rawDir, `${id}.json`), JSON.stringify({ id, messages }, null, 2));

    // 生成向量
    const text = messages.map(m => `${m.role}: ${m.content}`).join('\n');
    const embedding = await generateEmbedding(text);
    if (embedding) {
      fs.writeFileSync(path.join(vecDir, `${id}.json`), JSON.stringify({ id, embedding, text: text.substring(0, 500) }, null, 2));
    }
  } catch (e) {
    logger.hookWarn(`对话存储失败: ${e.message}`, 'postResponse');
  }
}

// ============================================================
// 主 Hook
// ============================================================

async function postResponseHook(ctx, plugin) {
  const userMessage = ctx.userMessage || '';
  const assistantMessage = ctx.assistantMessage || '';
  if (!userMessage) return ctx;

  const memoryPath = plugin.config?.memoryPath
    || path.join(process.env.HOME || '/root', '.openclaw/workspace/memory');

  // 1. 保存对话
  await saveDialogueToShortTerm(memoryPath, userMessage, assistantMessage);
  await saveConversationToStore(memoryPath, userMessage, assistantMessage);

  // 2. 轮次 +1
  const turns = incrementTurnCount(memoryPath);

  // 3. 达到压缩阈值则自动压缩
  if (turns >= COMPRESS_CONFIG.triggerTurns) {
    await compressConversations(memoryPath);
  }

  return ctx;
}

// 导出供外部调用
module.exports = {
  postResponseHook,
  manualCompress,
  getSummaries,
  COMPRESS_CONFIG
};
