#!/usr/bin/env node
/**
 * Cognitive Brain - 用户建模模块（重构版）
 * 构建和维护用户画像
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('user_model');
const fs = require('fs');
const path = require('path');
const { resolveModule } = require('../module_resolver.cjs');

// 导入拆分的模块
const { loadProfile, updateBasic, recordInterest, getPreferences, getProfileSummary } = require('./user_profile.cjs');
const { loadBehaviorData, recordInteraction, recordSession, recordTaskPreference, getBehaviorStats } = require('./user_behavior.cjs');
const { loadEmotionData, recordEmotion, getEmotionAnalysis } = require('./user_emotions.cjs');
const { loadInteractionData, recordInteractionHistory, detectContextSwitch, recordExpression, getInteractionContext } = require('./user_interactions.cjs');

// 初始化
function init() {
  loadProfile();
  loadBehaviorData();
  loadEmotionData();
  loadInteractionData();
}

/**
 * 获取完整画像
 */
function getFullProfile() {
  return {
    profile: getProfileSummary(),
    preferences: getPreferences(),
    behavior: getBehaviorStats(),
    emotions: getEmotionAnalysis(),
    interactions: getInteractionContext()
  };
}

/**
 * 预测用户需求
 */
function predictNeeds() {
  const context = getInteractionContext();
  const behavior = getBehaviorStats();
  const profile = getProfileSummary();
  
  const needs = [];
  
  // 基于活跃时段
  const hour = new Date().getHours();
  if (hour >= 9 && hour <= 18) {
    needs.push({ type: 'productivity', description: '工作时间，可能需要效率工具' });
  } else {
    needs.push({ type: 'relaxation', description: '非工作时间，可能需要轻松对话' });
  }
  
  // 基于历史任务
  if (behavior.topTasks.length > 0) {
    const topTask = behavior.topTasks[0][0];
    needs.push({ type: 'continuation', description: `可能继续${topTask}相关任务` });
  }
  
  // 基于情绪
  const emotion = getEmotionAnalysis();
  if (emotion && emotion.trend === 'declining') {
    needs.push({ type: 'support', description: '情绪趋势下降，可能需要支持' });
  }
  
  return needs;
}

/**
 * 推断沟通风格
 */
function inferCommunicationStyle(messages = []) {
  if (messages.length === 0) {
    return getPreferences().communicationTone;
  }
  
  const totalLength = messages.reduce((sum, m) => sum + (m.content?.length || 0), 0);
  const avgLength = totalLength / messages.length;
  
  // 分析标点使用
  const punctuationCounts = messages.reduce((acc, m) => {
    const content = m.content || '';
    acc.exclamation += (content.match(/!/g) || []).length;
    acc.question += (content.match(/\?/g) || []).length;
    return acc;
  }, { exclamation: 0, question: 0 });
  
  let style = 'casual';
  
  if (avgLength > 200 && punctuationCounts.question < 2) {
    style = 'formal';
  } else if (punctuationCounts.exclamation > messages.length * 0.3) {
    style = 'enthusiastic';
  } else if (punctuationCounts.question > messages.length * 0.5) {
    style = 'inquisitive';
  }
  
  return style;
}

// 命令行接口
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  init();
  
  switch (command) {
    case 'profile':
      console.log(JSON.stringify(getFullProfile(), null, 2));
      break;
    case 'predict':
      console.log(JSON.stringify(predictNeeds(), null, 2));
      break;
    case 'init':
      console.log('✅ 用户模型已初始化');
      break;
    default:
      console.log('用法: node user_model.cjs [profile|predict|init]');
  }
}

// 导出函数
module.exports = {
  init,
  getFullProfile,
  predictNeeds,
  inferCommunicationStyle,
  // 从子模块导出
  updateBasic,
  recordInterest,
  recordInteraction,
  recordSession,
  recordTaskPreference,
  recordEmotion,
  recordInteractionHistory,
  detectContextSwitch,
  recordExpression,
  getPreferences,
  getBehaviorStats,
  getEmotionAnalysis,
  getInteractionContext
};

// 主入口
if (require.main === module) {
  main();
}
