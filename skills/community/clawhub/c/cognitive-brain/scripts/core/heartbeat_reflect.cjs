#!/usr/bin/env node
/**
 * Cognitive Brain - 心跳反思 v2
 * 收集上下文数据，生成反思提示，等待主 agent 执行真正的思考
 */

const fs = require('fs');
const path = require('path');
const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('heartbeat_reflect');
const { randomChoice } = require('./random.cjs');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const WORKSPACE_DIR = path.join(HOME, '.openclaw/workspace');
const MEMORY_PATH = path.join(WORKSPACE_DIR, 'MEMORY.md');
const PROMPT_PATH = path.join(WORKSPACE_DIR, '.reflection-prompt.md');
const STATE_PATH = path.join(SKILL_DIR, '.heartbeat-state.json');

// 元认知问题库
const METACOGNITIVE_QUESTIONS = {
  high: [
    {
      id: 'self_improvement',
      question: '基于最近的用户反馈，我能立即改进什么？',
      context: '查看最近的错误修复和优化'
    },
    {
      id: 'unused_potential',
      question: '我最近没有充分利用的能力是什么？',
      context: '查看已启用但未使用的功能'
    },
    {
      id: 'recurring_patterns',
      question: '用户行为中有什么重复出现的模式我需要注意？',
      context: '分析用户活跃时段和主题偏好'
    }
  ],
  medium: [
    {
      id: 'gaps',
      question: '我的知识/记忆系统有什么空白需要填补？',
      context: '检查孤立概念和联想密度'
    },
    {
      id: 'efficiency',
      question: '有什么系统化的改进可以节省用户时间？',
      context: '思考自动化机会'
    }
  ],
  low: [
    {
      id: 'curiosity',
      question: '如果我要问用户一个问题，我会问什么？',
      context: '基于已有信息发现的信息缺口'
    }
  ]
};

/**
 * 加载状态
 */
function loadState() {
  try {
    if (fs.existsSync(STATE_PATH)) {
      return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
    }
  } catch (e) {
    logger.error('加载状态失败', { error: e.message });
  }
  return {
    lastRun: 0,
    lastCheck: 0,
    runCount: 0,
    promptsGenerated: 0
  };
}

/**
 * 保存状态
 */
function saveState(state) {
  try {
    fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
  } catch (e) {
    logger.error('保存状态失败', { error: e.message });
  }
}

/**
 * 检查是否应该运行（30分钟间隔）
 */
function shouldRun() {
  const state = loadState();
  const now = Date.now();
  const THIRTY_MINUTES = 30 * 60 * 1000;
  
  if (now - state.lastRun < THIRTY_MINUTES) {
    const remaining = Math.ceil((THIRTY_MINUTES - (now - state.lastRun)) / 60000);
    logger.info(`距离下次运行还有 ${remaining} 分钟`);
    return false;
  }
  
  return true;
}

/**
 * 检查是否有待处理的反思
 */
function hasPendingReflection() {
  return fs.existsSync(PROMPT_PATH);
}

/**
 * 获取系统统计
 */
async function getStats() {
  try {
    const { getPool } = require('./db.cjs');
    const pool = getPool();
    
    if (!pool) {
      return null;
    }
    
    const client = await pool.connect();
    try {
      // 基础统计
      const statsResult = await client.query(`
        SELECT 
          (SELECT COUNT(*) FROM episodes) as memory_count,
          (SELECT COUNT(*) FROM concepts) as concept_count,
          (SELECT COUNT(*) FROM associations) as association_count,
          (SELECT COUNT(*) FROM episodes 
           WHERE created_at > NOW() - INTERVAL '24 hours') as memories_24h
      `);
      
      // 用户活跃统计
      const activeResult = await client.query(`
        SELECT 
          DATE_TRUNC('hour', created_at) as hour,
          COUNT(*) as count
        FROM episodes
        WHERE created_at > NOW() - INTERVAL '7 days'
        GROUP BY hour
        ORDER BY count DESC
        LIMIT 5
      `);
      
      return {
        ...statsResult.rows[0],
        activeHours: activeResult.rows
      };
    } finally {
      client.release();
    }
  } catch (err) {
    logger.error('获取统计失败', { error: err.message });
    return null;
  }
}

/**
 * 收集上下文
 */
async function collectContext() {
  const stats = await getStats();
  const now = new Date();
  
  // 最近记忆摘要
  let recentMemories = [];
  try {
    const { getPool } = require('./db.cjs');
    const pool = getPool();
    if (pool) {
      const client = await pool.connect();
      try {
        const result = await client.query(`
          SELECT content, type, importance, created_at
          FROM episodes
          ORDER BY created_at DESC
          LIMIT 5
        `);
        recentMemories = result.rows;
      } finally {
        client.release();
      }
    }
  } catch (e) {
    logger.warn('获取最近记忆失败', { error: e.message });
  }
  
  return {
    timestamp: now.toISOString(),
    hour: now.getHours(),
    stats,
    recentMemories: recentMemories.map(m => ({
      type: m.type,
      content: m.content?.substring(0, 100) + '...',
      importance: m.importance
    }))
  };
}

/**
 * 选择元认知问题
 */
function selectQuestions(context) {
  const selected = [];
  
  // 根据上下文选择问题
  if (context.stats?.memories_24h > 10) {
    selected.push(...METACOGNITIVE_QUESTIONS.high.slice(0, 2));
  } else if (context.stats?.memories_24h > 0) {
    selected.push(METACOGNITIVE_QUESTIONS.high[0]);
    selected.push(randomChoice(METACOGNITIVE_QUESTIONS.medium));
  } else {
    selected.push(METACOGNITIVE_QUESTIONS.medium[0]);
    selected.push(METACOGNITIVE_QUESTIONS.low[0]);
  }
  
  return selected;
}

/**
 * 生成反思提示
 */
async function generateReflectionPrompt() {
  const context = await collectContext();
  const questions = selectQuestions(context);
  
  const prompt = `# 🧠 反思提示 [${new Date().toLocaleString('zh-CN')}]

## 当前上下文

**时间**: ${context.hour}:00 (24小时制)

**系统状态**:
${context.stats ? `- 记忆总数: ${context.stats.memory_count}
- 概念总数: ${context.stats.concept_count}
- 联想总数: ${context.stats.association_count}
- 24h新增: ${context.stats.memories_24h}` : '- 统计暂不可用'}

**最近记忆**:
${context.recentMemories.map(m => `- [${m.type}] ${m.content} (重要性: ${m.importance?.toFixed(2) || 'N/A'})`).join('\n') || '- 无'}

## 元认知问题

${questions.map((q, i) => `${i + 1}. **${q.question}**
   - 上下文: ${q.context}
   - 优先级: ${i === 0 ? '高' : i === 1 ? '中' : '低'}`).join('\n\n')}

## 如何回答

1. 看数据 - 从上面的统计中发现模式，不是泛泛而谈
2. 回答具体问题 - 元认知问题需要具体答案
3. 提出行动 - 有什么可以立即改进的？
4. 记录价值 - 洞察要写下来，但不要重复

**回答后删除此文件**。
`;
  
  return prompt;
}

/**
 * 保存反思提示
 */
function savePrompt(prompt) {
  try {
    fs.writeFileSync(PROMPT_PATH, prompt);
    logger.info('反思提示已保存');
    return true;
  } catch (e) {
    logger.error('保存反思提示失败', { error: e.message });
    return false;
  }
}

/**
 * 检查模式
 */
async function checkMode() {
  logger.info('=== 反思提示检查 ===');
  
  if (hasPendingReflection()) {
    logger.info('有反思提示待处理');
    return;
  }
  
  if (!shouldRun()) {
    logger.info('未到运行时间');
    return;
  }
  
  logger.info('生成新的反思提示...');
  const prompt = await generateReflectionPrompt();
  if (savePrompt(prompt)) {
    const state = loadState();
    state.lastRun = Date.now();
    state.promptsGenerated++;
    saveState(state);
    logger.info('反思提示生成完成');
  }
}

/**
 * 查看模式
 */
async function viewMode() {
  if (hasPendingReflection()) {
    const content = fs.readFileSync(PROMPT_PATH, 'utf8');
    process.stdout.write(content);
  } else {
    logger.info('没有待处理的反思提示');
  }
}

/**
 * 主入口
 */
async function main() {
  const command = process.argv[2] || 'check';
  
  switch (command) {
    case 'check':
      await checkMode();
      break;
    case 'view':
      await viewMode();
      break;
    case 'force':
      logger.info('强制生成反思提示...');
      const prompt = await generateReflectionPrompt();
      savePrompt(prompt);
      break;
    default:
      logger.info('用法: node heartbeat_reflect.cjs [check|view|force]');
  }
}

// 导出供其他模块使用
module.exports = {
  generateReflectionPrompt,
  hasPendingReflection,
  shouldRun,
  getStats
};

// 主入口
if (require.main === module) {
  main();
}

