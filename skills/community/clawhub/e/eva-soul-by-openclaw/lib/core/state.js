/**
 * EVA Soul - 状态管理模块
 */

const fs = require('fs');
const path = require('path');
const { expandPath } = require('./config');
const logger = require('../../hooks/logger');

/**
 * 默认状态
 */
const DEFAULT_STATE = {
  // 基础信息
  version: '1.0.0',
  initializedAt: null,
  lastUpdate: null,
  
  // 情感状态
  currentEmotion: 'neutral',
  emotionHistory: [],
  emotionTrend: [],
  
  // 性格状态
  personality: 'gentle',
  personalityModifiers: {},
  traitExpansion: {},
  
  // 记忆状态
  memoryStats: {
    short: 0,
    medium: 0,
    long: 0,
    archived: 0
  },
  lastMemoryUpdate: null,
  
  // 概念状态
  concepts: [],
  conceptStats: {
    total: 0,
    updated: 0
  },
  lastConceptUpdate: null,
  
  // 模式状态
  patterns: [],
  patternStats: {
    total: 0,
    detected: 0
  },
  lastPatternUpdate: null,
  
  // 决策状态
  decisions: [],
  motivations: [],
  values: [],
  
  // 会话状态
  sessionCount: 0,
  sessionStartTime: null,
  lastInteraction: null,
  totalInteractions: 0,
  
  // 工具使用统计
  toolUsage: {},
  
  // 主人信息
  ownerInfo: null,
  ownerPreferences: {},
  ownerSchedule: {},
  
  // 重要日子
  importantDates: [],
  
  // 睡眠状态
  isSleeping: false,
  sleepStartTime: null,
  lastWakeTime: null
};

/**
 * 创建新状态
 */
function createState() {
  return {
    ...DEFAULT_STATE,
    initializedAt: new Date().toISOString()
  };
}

/**
 * 加载状态
 */
function loadState(memoryPath) {
  const stateFile = path.join(memoryPath, 'eva-soul-state.json');
  
  if (fs.existsSync(stateFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
      return { ...DEFAULT_STATE, ...data };
    } catch (e) {
      logger.warn(`Failed to load state: ${e.message}`, 'state');
      return createState();
    }
  }
  
  return createState();
}

/**
 * 保存状态
 */
function saveState(state, memoryPath) {
  const stateFile = path.join(memoryPath, 'eva-soul-state.json');
  
  try {
    state.lastUpdate = new Date().toISOString();
    fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
    return true;
  } catch (e) {
    logger.warn(`Failed to save state: ${e.message}`, 'state');
    return false;
  }
}

/**
 * 更新情感
 */
function updateEmotion(state, emotion) {
  const oldEmotion = state.currentEmotion;
  state.currentEmotion = emotion;
  
  state.emotionHistory.push({
    from: oldEmotion,
    to: emotion,
    time: new Date().toISOString()
  });
  
  // 保留最近50条
  state.emotionHistory = state.emotionHistory.slice(-50);
  
  return state;
}

/**
 * 更新性格
 */
function updatePersonality(state, personality, modifiers = {}) {
  state.personality = personality;
  
  if (Object.keys(modifiers).length > 0) {
    state.personalityModifiers = {
      ...state.personalityModifiers,
      ...modifiers
    };
  }
  
  return state;
}

/**
 * 记录交互
 * @param {object} state - 当前状态
 * @param {string} [message] - 最后一条交互内容摘要
 */
function recordInteraction(state, message = '') {
  state.lastInteraction = new Date().toISOString();
  state.totalInteractions++;
  if (message) {
    state.lastInteractionMessage = message.substring(0, 200);
  }
  return state;
}

/**
 * 增加会话数
 */
function incrementSession(state) {
  state.sessionCount++;
  state.sessionStartTime = new Date().toISOString();
  
  return state;
}

/**
 * 睡眠/唤醒
 */
function setSleepState(state, isSleeping) {
  state.isSleeping = isSleeping;
  
  if (isSleeping) {
    state.sleepStartTime = new Date().toISOString();
  } else {
    state.lastWakeTime = new Date().toISOString();
  }
  
  return state;
}

/**
 * 记录工具使用
 */
function recordToolUsage(state, toolName) {
  state.toolUsage[toolName] = (state.toolUsage[toolName] || 0) + 1;
  return state;
}

/**
 * 添加概念
 */
function addConcept(state, concept) {
  const exists = state.concepts.find(c => c.name === concept.name);
  
  if (exists) {
    exists.count = (exists.count || 0) + 1;
    exists.lastSeen = new Date().toISOString();
    exists.importance = Math.max(exists.importance || 0, concept.importance || 5);
  } else {
    state.concepts.push({
      ...concept,
      createdAt: new Date().toISOString(),
      lastSeen: new Date().toISOString(),
      count: 1
    });
  }
  
  state.conceptStats.total = state.concepts.length;
  
  return state;
}

/**
 * 添加模式
 */
function addPattern(state, pattern) {
  const exists = state.patterns.find(p => p.name === pattern.name);
  
  if (exists) {
    exists.occurrences++;
    exists.lastSeen = new Date().toISOString();
  } else {
    state.patterns.push({
      ...pattern,
      createdAt: new Date().toISOString(),
      lastSeen: new Date().toISOString(),
      occurrences: 1
    });
  }
  
  state.patternStats.total = state.patterns.length;
  
  return state;
}

/**
 * 添加重要日期
 */
function addImportantDate(state, date, description, recurring = false) {
  state.importantDates.push({
    date,
    description,
    recurring,
    addedAt: new Date().toISOString()
  });
  
  return state;
}

/**
 * 更新主人信息
 */
function updateOwnerInfo(state, info) {
  state.ownerInfo = {
    ...state.ownerInfo,
    ...info
  };
  
  return state;
}

/**
 * 获取状态摘要
 */
function getStateSummary(state) {
  return {
    version: state.version,
    emotion: state.currentEmotion,
    personality: state.personality,
    sessionCount: state.sessionCount,
    totalInteractions: state.totalInteractions,
    lastInteraction: state.lastInteraction,
    concepts: state.conceptStats.total,
    patterns: state.patternStats.total,
    isSleeping: state.isSleeping,
    uptime: state.sessionStartTime 
      ? Math.floor((Date.now() - new Date(state.sessionStartTime).getTime()) / 1000)
      : 0
  };
}

module.exports = {
  DEFAULT_STATE,
  createState,
  loadState,
  saveState,
  updateEmotion,
  updatePersonality,
  recordInteraction,
  incrementSession,
  setSleepState,
  recordToolUsage,
  addConcept,
  addPattern,
  addImportantDate,
  updateOwnerInfo,
  getStateSummary
};
