/**
 * 用户行为模块
 * 记录用户行为模式和任务偏好
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('user_behavior');
const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/skills/cognitive-brain');
const USER_MODEL_PATH = path.join(SKILL_DIR, '.user-model.json');

// 行为数据
let behaviorData = {
  patterns: {
    activeHours: [],
    commonTasks: {},
    interactionFrequency: 0,
    avgSessionLength: 0
  },
  taskPreferences: {
    completedTasks: [],
    taskPatterns: {},
    preferredTools: {},
    taskSequencePatterns: []
  },
  stats: {
    totalInteractions: 0,
    lastInteraction: null,
    sessions: []
  }
};

/**
 * 加载行为数据
 */
function loadBehaviorData() {
  try {
    if (fs.existsSync(USER_MODEL_PATH)) {
      const data = JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'));
      behaviorData = {
        patterns: { ...behaviorData.patterns, ...data.patterns },
        taskPreferences: { ...behaviorData.taskPreferences, ...data.taskPreferences },
        stats: { ...behaviorData.stats, ...data.stats }
      };
    }
  } catch (e) {
    console.error('[user_behavior] 加载失败:', e.message);
  }
}

/**
 * 保存行为数据
 */
function saveBehaviorData() {
  try {
    const existing = fs.existsSync(USER_MODEL_PATH) 
      ? JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'))
      : {};
    fs.writeFileSync(USER_MODEL_PATH, JSON.stringify({
      ...existing,
      patterns: behaviorData.patterns,
      taskPreferences: behaviorData.taskPreferences,
      stats: behaviorData.stats
    }, null, 2));
  } catch (e) {
    console.error('[user_behavior] 保存失败:', e.message);
  }
}

/**
 * 记录交互
 */
function recordInteraction(metadata = {}) {
  behaviorData.stats.totalInteractions++;
  behaviorData.stats.lastInteraction = Date.now();
  
  // 记录活跃时段
  const hour = new Date().getHours();
  if (!behaviorData.patterns.activeHours.includes(hour)) {
    behaviorData.patterns.activeHours.push(hour);
  }
  
  // 记录任务
  if (metadata.task) {
    behaviorData.patterns.commonTasks[metadata.task] = 
      (behaviorData.patterns.commonTasks[metadata.task] || 0) + 1;
  }
  
  saveBehaviorData();
}

/**
 * 记录会话
 */
function recordSession(duration, interactions) {
  behaviorData.stats.sessions.push({
    startedAt: Date.now() - duration,
    endedAt: Date.now(),
    duration,
    interactions
  });

  // 保留最近 30 天
  const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
  behaviorData.stats.sessions = behaviorData.stats.sessions
    .filter(s => s.startedAt > cutoff);

  // 更新平均会话长度
  const avgLength = behaviorData.stats.sessions
    .reduce((sum, s) => sum + s.duration, 0) / behaviorData.stats.sessions.length || 0;
  behaviorData.patterns.avgSessionLength = avgLength;
  behaviorData.patterns.interactionFrequency = behaviorData.stats.sessions.length;

  saveBehaviorData();
}

/**
 * 记录任务偏好
 */
function recordTaskPreference(taskType, duration, success, tools = []) {
  if (!behaviorData.taskPreferences.taskPatterns[taskType]) {
    behaviorData.taskPreferences.taskPatterns[taskType] = {
      count: 0,
      avgDuration: 0,
      successCount: 0
    };
  }
  
  const pattern = behaviorData.taskPreferences.taskPatterns[taskType];
  pattern.count++;
  pattern.avgDuration = (pattern.avgDuration * (pattern.count - 1) + duration) / pattern.count;
  if (success) pattern.successCount++;
  
  // 记录偏好工具
  tools.forEach(tool => {
    behaviorData.taskPreferences.preferredTools[tool] = 
      (behaviorData.taskPreferences.preferredTools[tool] || 0) + 1;
  });
  
  // 记录完成历史
  behaviorData.taskPreferences.completedTasks.push({
    taskType,
    duration,
    success,
    timestamp: Date.now()
  });
  
  // 保留最近100条
  behaviorData.taskPreferences.completedTasks = 
    behaviorData.taskPreferences.completedTasks.slice(-100);
  
  saveBehaviorData();
}

/**
 * 获取行为统计
 */
function getBehaviorStats() {
  const topTasks = Object.entries(behaviorData.patterns.commonTasks)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);
    
  return {
    totalInteractions: behaviorData.stats.totalInteractions,
    avgSessionLength: Math.round(behaviorData.patterns.avgSessionLength / 1000),
    sessionCount: behaviorData.stats.sessions.length,
    topTasks,
    preferredTools: Object.entries(behaviorData.taskPreferences.preferredTools)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
  };
}

module.exports = {
  loadBehaviorData,
  recordInteraction,
  recordSession,
  recordTaskPreference,
  getBehaviorStats
};
