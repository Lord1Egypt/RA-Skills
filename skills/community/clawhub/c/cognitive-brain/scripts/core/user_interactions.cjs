/**
 * 用户交互历史模块
 * 管理用户交互历史和上下文
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('user_interactions');
const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/skills/cognitive-brain');
const USER_MODEL_PATH = path.join(SKILL_DIR, '.user-model.json');

// 交互数据
let interactionData = {
  recentInteractions: [],
  lastTopics: [],
  contextSwitches: 0,
  commonExpressions: {
    phrases: {},
    greetings: [],
    questions: [],
    commands: []
  }
};

/**
 * 加载交互数据
 */
function loadInteractionData() {
  try {
    if (fs.existsSync(USER_MODEL_PATH)) {
      const data = JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'));
      interactionData = {
        recentInteractions: data.interactionHistory?.recentInteractions || [],
        lastTopics: data.interactionHistory?.lastTopics || [],
        contextSwitches: data.interactionHistory?.contextSwitches || 0,
        commonExpressions: { ...interactionData.commonExpressions, ...data.commonExpressions }
      };
    }
  } catch (e) {
    console.error('[user_interactions] 加载失败:', e.message);
  }
}

/**
 * 保存交互数据
 */
function saveInteractionData() {
  try {
    const existing = fs.existsSync(USER_MODEL_PATH) 
      ? JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'))
      : {};
    fs.writeFileSync(USER_MODEL_PATH, JSON.stringify({
      ...existing,
      interactionHistory: {
        recentInteractions: interactionData.recentInteractions,
        lastTopics: interactionData.lastTopics,
        contextSwitches: interactionData.contextSwitches
      },
      commonExpressions: interactionData.commonExpressions
    }, null, 2));
  } catch (e) {
    console.error('[user_interactions] 保存失败:', e.message);
  }
}

/**
 * 记录交互历史
 */
function recordInteractionHistory(topic, action, result) {
  interactionData.recentInteractions.push({
    timestamp: Date.now(),
    topic,
    action,
    result
  });
  
  // 保留最近20条
  interactionData.recentInteractions = interactionData.recentInteractions.slice(-20);
  
  // 更新话题历史
  if (topic && !interactionData.lastTopics.includes(topic)) {
    interactionData.lastTopics.unshift(topic);
    interactionData.lastTopics = interactionData.lastTopics.slice(0, 10);
  }
  
  saveInteractionData();
}

/**
 * 检测上下文切换
 */
function detectContextSwitch(currentTopic) {
  if (interactionData.lastTopics.length === 0) return false;
  
  const lastTopic = interactionData.lastTopics[0];
  
  // 简单判断是否相关
  const isRelated = currentTopic.includes(lastTopic) || 
                    lastTopic.includes(currentTopic) ||
                    calculateSimilarity(currentTopic, lastTopic) > 0.5;
  
  if (!isRelated) {
    interactionData.contextSwitches++;
    saveInteractionData();
    return true;
  }
  
  return false;
}

/**
 * 简单相似度计算
 */
function calculateSimilarity(str1, str2) {
  const words1 = new Set(str1.split(/\s+/));
  const words2 = new Set(str2.split(/\s+/));
  const intersection = new Set([...words1].filter(w => words2.has(w)));
  return intersection.size / Math.max(words1.size, words2.size);
}

/**
 * 记录常用表达
 */
function recordExpression(text) {
  // 记录短语
  const phrases = text.split(/[，。！？、；]/);
  phrases.forEach(phrase => {
    const trimmed = phrase.trim();
    if (trimmed.length >= 2 && trimmed.length <= 20) {
      interactionData.commonExpressions.phrases[trimmed] = 
        (interactionData.commonExpressions.phrases[trimmed] || 0) + 1;
    }
  });
  
  // 分类记录
  if (/^(你好|嗨|哈喽|早安|晚安|再见|谢谢)/i.test(text)) {
    interactionData.commonExpressions.greetings.push(text);
    interactionData.commonExpressions.greetings = 
      interactionData.commonExpressions.greetings.slice(-10);
  }
  
  if (/[?？]/.test(text)) {
    interactionData.commonExpressions.questions.push(text);
    interactionData.commonExpressions.questions = 
      interactionData.commonExpressions.questions.slice(-10);
  }
  
  saveInteractionData();
}

/**
 * 获取交互上下文
 */
function getInteractionContext() {
  return {
    recentTopics: interactionData.lastTopics,
    contextSwitches: interactionData.contextSwitches,
    recentInteractions: interactionData.recentInteractions.slice(-5),
    commonPhrases: Object.entries(interactionData.commonExpressions.phrases)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([p]) => p)
  };
}

module.exports = {
  loadInteractionData,
  recordInteractionHistory,
  detectContextSwitch,
  recordExpression,
  getInteractionContext
};

