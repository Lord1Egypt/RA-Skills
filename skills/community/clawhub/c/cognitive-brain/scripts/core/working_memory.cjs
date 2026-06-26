#!/usr/bin/env node
/**
 * Cognitive Brain - 工作记忆模块
 * 管理短期活跃上下文，类似人类的工作记忆
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('working_memory');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');
const WORKING_MEMORY_PATH = path.join(SKILL_DIR, '.working-memory.json');

// 工作记忆结构
const workingMemory = {
  // 当前活跃上下文
  activeContext: {
    topic: null,           // 当前话题
    entities: [],          // 活跃实体
    lastMentioned: {},     // 最近提及的实体 { entity: timestamp }
    openQuestions: [],     // 未解决的问题
    pendingTasks: []       // 待处理的任务
  },

  // 注意力焦点
  attention: {
    focus: null,           // 当前焦点
    salience: new Map(),   // 显著性评分
    history: []            // 注意力历史
  },

  // 时间戳
  lastUpdate: Date.now(),

  // 配置
  config: {
    maxEntities: 20,
    maxOpenQuestions: 10,
    maxPendingTasks: 5,
    entityDecayMs: 10 * 60 * 1000, // 10 分钟衰减
    attentionHistorySize: 100
  }
};

/**
 * 加载工作记忆
 */
function load() {
  try {
    if (fs.existsSync(WORKING_MEMORY_PATH)) {
      const data = JSON.parse(fs.readFileSync(WORKING_MEMORY_PATH, 'utf8'));
      workingMemory.activeContext = data.activeContext || workingMemory.activeContext;
      workingMemory.attention = data.attention || workingMemory.attention;
      workingMemory.attention.salience = new Map(Object.entries(data.attention?.salience || {}));
      workingMemory.lastUpdate = data.lastUpdate || Date.now();
    }
  } catch (e) { console.error("[working_memory] 错误:", e.message);
    console.warn('[working-memory] Load failed:', e.message);
  }
}

/**
 * 保存工作记忆
 */
function save() {
  try {
    const data = {
      activeContext: workingMemory.activeContext,
      attention: {
        ...workingMemory.attention,
        salience: Object.fromEntries(workingMemory.attention.salience)
      },
      lastUpdate: Date.now()
    };
    fs.writeFileSync(WORKING_MEMORY_PATH, JSON.stringify(data, null, 2));
  } catch (e) { console.error("[working_memory] 错误:", e.message);
    console.warn('[working-memory] Save failed:', e.message);
  }
}

/**
 * 更新话题
 */
function setTopic(topic) {
  workingMemory.activeContext.topic = topic;
  addToAttentionHistory({ type: 'topic', value: topic });
  save();
}

/**
 * 添加活跃实体
 */
function addEntity(entity, metadata = {}) {
  const entities = workingMemory.activeContext.entities;
  const existing = entities.find(e => e.name === entity);

  if (existing) {
    existing.lastMentioned = Date.now();
    existing.mentionCount++;
    existing.metadata = { ...existing.metadata, ...metadata };
  } else {
    if (entities.length >= workingMemory.config.maxEntities) {
      // 移除最旧的实体
      entities.sort((a, b) => b.lastMentioned - a.lastMentioned);
      entities.pop();
    }
    entities.push({
      name: entity,
      firstMentioned: Date.now(),
      lastMentioned: Date.now(),
      mentionCount: 1,
      metadata
    });
  }

  // 更新显著性
  updateSalience(entity, 0.1);
  save();
}

/**
 * 添加开放问题
 */
function addOpenQuestion(question) {
  const questions = workingMemory.activeContext.openQuestions;
  if (questions.length >= workingMemory.config.maxOpenQuestions) {
    questions.shift();
  }
  questions.push({
    question,
    askedAt: Date.now(),
    resolved: false
  });
  save();
}

/**
 * 解决开放问题
 */
function resolveOpenQuestion(questionPattern) {
  const questions = workingMemory.activeContext.openQuestions;
  for (const q of questions) {
    if (q.question.includes(questionPattern) && !q.resolved) {
      q.resolved = true;
      q.resolvedAt = Date.now();
    }
  }
  save();
}

/**
 * 添加待处理任务
 */
function addPendingTask(task) {
  const tasks = workingMemory.activeContext.pendingTasks;
  if (tasks.length >= workingMemory.config.maxPendingTasks) {
    tasks.shift();
  }
  tasks.push({
    task,
    createdAt: Date.now(),
    status: 'pending'
  });
  save();
}

/**
 * 完成待处理任务
 */
function completePendingTask(taskPattern) {
  const tasks = workingMemory.activeContext.pendingTasks;
  for (const t of tasks) {
    if (t.task.includes(taskPattern) && t.status === 'pending') {
      t.status = 'completed';
      t.completedAt = Date.now();
    }
  }
  save();
}

/**
 * 更新显著性
 */
function updateSalience(entity, delta) {
  const current = workingMemory.attention.salience.get(entity) || 0;
  workingMemory.attention.salience.set(entity, Math.min(1, Math.max(0, current + delta)));
}

/**
 * 添加到注意力历史
 */
function addToAttentionHistory(entry) {
  const history = workingMemory.attention.history;
  history.push({ ...entry, timestamp: Date.now() });
  if (history.length > workingMemory.config.attentionHistorySize) {
    history.shift();
  }
}

/**
 * 设置注意力焦点
 */
function setFocus(focus) {
  workingMemory.attention.focus = focus;
  addToAttentionHistory({ type: 'focus', value: focus });
  updateSalience(focus, 0.2);
  save();
}

/**
 * 获取活跃实体
 */
function getActiveEntities(limit = 5) {
  const now = Date.now();
  const decayMs = workingMemory.config.entityDecayMs;

  return workingMemory.activeContext.entities
    .filter(e => now - e.lastMentioned < decayMs)
    .sort((a, b) => b.mentionCount - a.mentionCount)
    .slice(0, limit);
}

/**
 * 获取上下文摘要
 */
function getContextSummary() {
  const entities = getActiveEntities();
  const unresolvedQuestions = workingMemory.activeContext.openQuestions
    .filter(q => !q.resolved)
    .slice(0, 3);
  const pendingTasks = workingMemory.activeContext.pendingTasks
    .filter(t => t.status === 'pending')
    .slice(0, 3);

  return {
    topic: workingMemory.activeContext.topic,
    activeEntities: entities.map(e => e.name),
    openQuestions: unresolvedQuestions.map(q => q.question),
    pendingTasks: pendingTasks.map(t => t.task),
    currentFocus: workingMemory.attention.focus
  };
}

/**
 * 衰减旧数据（定期调用）
 */
function decay() {
  const now = Date.now();
  const decayMs = workingMemory.config.entityDecayMs;

  // 衰减实体
  workingMemory.activeContext.entities = workingMemory.activeContext.entities
    .filter(e => now - e.lastMentioned < decayMs * 2);

  // 衰减显著性
  for (const [entity, salience] of workingMemory.attention.salience) {
    const newSalience = salience * 0.9;
    if (newSalience < 0.05) {
      workingMemory.attention.salience.delete(entity);
    } else {
      workingMemory.attention.salience.set(entity, newSalience);
    }
  }

  // 清理已解决的开放问题（超过 1 小时）
  workingMemory.activeContext.openQuestions =
    workingMemory.activeContext.openQuestions
      .filter(q => !q.resolved || now - q.resolvedAt < 60 * 60 * 1000);

  // 清理已完成的任务（超过 1 小时）
  workingMemory.activeContext.pendingTasks =
    workingMemory.activeContext.pendingTasks
      .filter(t => t.status !== 'completed' || now - t.completedAt < 60 * 60 * 1000);

  save();
}

/**
 * 重置工作记忆
 */
function reset() {
  workingMemory.activeContext = {
    topic: null,
    entities: [],
    lastMentioned: {},
    openQuestions: [],
    pendingTasks: []
  };
  workingMemory.attention = {
    focus: null,
    salience: new Map(),
    history: []
  };
  save();
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  load();

  switch (action) {
    case 'summary':
      console.log(JSON.stringify(getContextSummary(), null, 2));
      break;

    case 'topic':
      if (args[0]) {
        setTopic(args.join(' '));
        console.log('✅ Topic set:', args.join(' '));
      } else {
        console.log('Current topic:', workingMemory.activeContext.topic);
      }
      break;

    case 'entity':
      if (args[0]) {
        addEntity(args[0]);
        console.log('✅ Entity added:', args[0]);
      } else {
        console.log('Active entities:', getActiveEntities());
      }
      break;

    case 'focus':
      if (args[0]) {
        setFocus(args.join(' '));
        console.log('✅ Focus set:', args.join(' '));
      } else {
        console.log('Current focus:', workingMemory.attention.focus);
      }
      break;

    case 'question':
      if (args[0]) {
        addOpenQuestion(args.join(' '));
        console.log('✅ Question added');
      } else {
        console.log('Open questions:', workingMemory.activeContext.openQuestions);
      }
      break;

    case 'task':
      if (args[0]) {
        addPendingTask(args.join(' '));
        console.log('✅ Task added');
      } else {
        console.log('Pending tasks:', workingMemory.activeContext.pendingTasks);
      }
      break;

    case 'decay':
      decay();
      console.log('✅ Decay completed');
      break;

    case 'reset':
      reset();
      console.log('✅ Working memory reset');
      break;

    default:
      console.log(`
工作记忆模块

用法:
  node working_memory.cjs summary              # 获取上下文摘要
  node working_memory.cjs topic [topic]        # 设置/查看话题
  node working_memory.cjs entity [name]        # 添加/查看实体
  node working_memory.cjs focus [focus]        # 设置/查看焦点
  node working_memory.cjs question [question]  # 添加开放问题
  node working_memory.cjs task [task]          # 添加待处理任务
  node working_memory.cjs decay                # 衰减旧数据
  node working_memory.cjs reset                # 重置工作记忆
      `);
  }
}

main();
