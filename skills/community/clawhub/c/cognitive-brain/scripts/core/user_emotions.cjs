/**
 * 用户情绪模块
 * 记录和分析用户情绪模式
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('user_emotions');
const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/skills/cognitive-brain');
const USER_MODEL_PATH = path.join(SKILL_DIR, '.user-model.json');

// 情绪数据
let emotionData = {
  history: [],
  dominantEmotions: {},
  emotionTriggers: {},
  emotionalTrend: 'stable'
};

/**
 * 加载情绪数据
 */
function loadEmotionData() {
  try {
    if (fs.existsSync(USER_MODEL_PATH)) {
      const data = JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'));
      emotionData = {
        history: data.emotionPatterns?.history || [],
        dominantEmotions: data.emotionPatterns?.dominantEmotions || {},
        emotionTriggers: data.emotionPatterns?.emotionTriggers || {},
        emotionalTrend: data.emotionPatterns?.emotionalTrend || 'stable'
      };
    }
  } catch (e) {
    console.error('[user_emotion] 加载失败:', e.message);
  }
}

/**
 * 保存情绪数据
 */
function saveEmotionData() {
  try {
    const existing = fs.existsSync(USER_MODEL_PATH) 
      ? JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'))
      : {};
    fs.writeFileSync(USER_MODEL_PATH, JSON.stringify({
      ...existing,
      emotionPatterns: emotionData
    }, null, 2));
  } catch (e) {
    console.error('[user_emotion] 保存失败:', e.message);
  }
}

/**
 * 记录情绪
 */
function recordEmotion(emotion, context = {}) {
  const entry = {
    timestamp: Date.now(),
    emotion,
    context: context.description || ''
  };
  
  // 添加到历史
  emotionData.history.push(entry);
  emotionData.history = emotionData.history.slice(-50);
  
  // 更新主导情绪统计
  emotionData.dominantEmotions[emotion] = 
    (emotionData.dominantEmotions[emotion] || 0) + 1;
  
  // 记录触发因素
  if (context.trigger) {
    emotionData.emotionTriggers[context.trigger] = 
      (emotionData.emotionTriggers[context.trigger] || 0) + 1;
  }
  
  // 分析趋势
  analyzeEmotionTrend();
  
  saveEmotionData();
}

/**
 * 分析情绪趋势
 */
function analyzeEmotionTrend() {
  const recent = emotionData.history.slice(-10);
  if (recent.length < 3) return;
  
  const positiveEmotions = ['positive', 'excited', 'curious'];
  const negativeEmotions = ['negative', 'frustrated', 'anxious'];
  
  let positiveCount = 0;
  let negativeCount = 0;
  
  recent.forEach(e => {
    if (positiveEmotions.includes(e.emotion)) positiveCount++;
    if (negativeEmotions.includes(e.emotion)) negativeCount++;
  });
  
  if (positiveCount > negativeCount * 2) {
    emotionData.emotionalTrend = 'improving';
  } else if (negativeCount > positiveCount * 2) {
    emotionData.emotionalTrend = 'declining';
  } else {
    emotionData.emotionalTrend = 'stable';
  }
}

/**
 * 获取情绪分析
 */
function getEmotionAnalysis() {
  const total = emotionData.history.length;
  if (total === 0) return null;
  
  const recent = emotionData.history.slice(-10);
  const dominant = Object.entries(emotionData.dominantEmotions)
    .sort((a, b) => b[1] - a[1])[0];
  
  return {
    trend: emotionData.emotionalTrend,
    dominantEmotion: dominant ? dominant[0] : 'neutral',
    recentMood: recent.length > 0 ? recent[recent.length - 1].emotion : 'unknown',
    topTriggers: Object.entries(emotionData.emotionTriggers)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([t, c]) => t)
  };
}

module.exports = {
  loadEmotionData,
  recordEmotion,
  analyzeEmotionTrend,
  getEmotionAnalysis
};

