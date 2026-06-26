/**
 * 重要性计算模块
 * 计算内容的重要性和存储层级
 */

const { extractEntities } = require('./entity_extractor.cjs');
const { detectExplicitIntent } = require('./emotion_analyzer.cjs');
const { randomRange } = require('./random.cjs');

/**
 * 基于内容特征计算重要性
 * @param {string} content - 输入内容
 * @param {Object} emotion - 情感分析结果
 * @returns {number} - 重要性分数 (0-1)
 */
function calculateContentImportance(content, emotion) {
  let score = 0.5; // 基准分

  // 1. 信息密度（实体数量）
  const entities = extractEntities(content);
  score += Math.min(0.2, entities.length * 0.02);

  // 2. 情感强度
  if (emotion) {
    score += Math.abs(emotion.valence) * 0.15;
    score += emotion.arousal * 0.1;
    score += emotion.curiosity * 0.05;
    score += emotion.excitement * 0.1;
  }

  // 3. 内容类型特征
  if (/决定|计划|目标|行动|安排|准备|开始|完成/i.test(content)) {
    score += 0.15; // 决策/行动类
  }

  if (/问题|困惑|疑问|不懂|怎么|为什么|如何/i.test(content)) {
    score += 0.1; // 问题/困惑类
  }

  if (/我喜欢|我讨厌|我觉得|我认为|我的|我想/i.test(content)) {
    score += 0.1; // 个人偏好/感受
  }

  if (/发现|明白|原来|才知道|意识到|理解/i.test(content)) {
    score += 0.15; // 知识/洞察类
  }

  // 4. 长度因子
  const charCount = content.length;
  if (charCount >= 20 && charCount <= 200) {
    score += 0.05;
  } else if (charCount < 10) {
    score -= 0.1;
  }

  // 5. 结构化程度
  const hasStructure = /[。！？；，]/.test(content);
  if (hasStructure && charCount > 50) {
    score += 0.05;
  }

  return Math.max(0, Math.min(1, score));
}

/**
 * 综合重要性计算（考虑用户意图）
 * @param {Object} params - 参数
 * @returns {number} - 最终重要性分数
 */
function calculateImportance(params) {
  const content = params.content || '';
  const emotion = params.emotion;
  const explicitIntent = detectExplicitIntent(content);

  // 用户明确指定的重要性
  if (params.importance !== undefined) {
    return Math.max(0, Math.min(1, params.importance));
  }

  // 根据用户意图调整
  if (explicitIntent.intent === 'high') {
    const baseImportance = calculateContentImportance(content, emotion);
    return Math.max(0.7, Math.min(0.95, baseImportance + 0.2));
  }

  if (explicitIntent.intent === 'low') {
    return randomRange(0.1, 0.3);
  }

  return calculateContentImportance(content, emotion);
}

/**
 * 选择存储层级
 * @param {number} importance - 重要性分数
 * @returns {string[]} - 存储层级列表
 */
function selectLayer(importance) {
  if (importance >= 0.8) return ['semantic', 'episodic'];
  if (importance >= 0.5) return ['episodic'];
  if (importance >= 0.3) return ['working'];
  return ['sensory'];
}

module.exports = {
  calculateContentImportance,
  calculateImportance,
  selectLayer
};
