/**
 * 对话总结模块
 * 负责生成对话摘要和要点
 */

/**
 * 总结对话内容
 * @param {string} content - 对话内容
 * @param {Object} options - 选项
 * @returns {Object} 总结结果
 */
function summarize(content, options = {}) {
  const {
    topic = null,
    maxLength = 500
  } = options;
  
  // 提取关键句子
  const sentences = extractSentences(content);
  
  // 如果指定了主题，过滤相关内容
  let relevantSentences = sentences;
  if (topic) {
    relevantSentences = filterByTopic(sentences, topic);
  }
  
  // 生成要点
  const keyPoints = generateKeyPoints(relevantSentences);
  
  // 识别主题
  const identifiedTopic = identifyTopic(content);
  
  // 提取关键结论
  const conclusions = extractConclusions(content);
  
  return {
    topic: identifiedTopic,
    keyPoints: keyPoints.slice(0, 5),
    conclusions: conclusions,
    summary: generateSummary(keyPoints, maxLength)
  };
}

/**
 * 提取句子
 * @param {string} text - 文本
 * @returns {Array<string>} 句子列表
 */
function extractSentences(text) {
  // 简单的句子分割
  return text
    .split(/(?<=[。！？.!?])\s*|\n+/)
    .map(s => s.trim())
    .filter(s => s.length > 10 && s.length < 200);
}

/**
 * 按主题过滤句子
 * @param {Array<string>} sentences - 句子列表
 * @param {string} topic - 主题关键词
 * @returns {Array<string>} 过滤后的句子
 */
function filterByTopic(sentences, topic) {
  const keywords = topic.toLowerCase().split(/\s+/);
  
  return sentences.filter(sentence => {
    const lowerSentence = sentence.toLowerCase();
    return keywords.some(keyword => lowerSentence.includes(keyword));
  });
}

/**
 * 生成关键要点
 * @param {Array<string>} sentences - 句子列表
 * @returns {Array<string>} 要点列表
 */
function generateKeyPoints(sentences) {
  // 提取包含关键词的句子作为要点
  const indicatorWords = [
    '需要', '应该', '必须', '要', '决定', '确定', '选择',
    '方案', '计划', '目标', '重点', '关键', '主要',
    '首先', '其次', '然后', '最后',
    '建议', '推荐', '考虑', '注意'
  ];
  
  const scored = sentences.map(sentence => {
    let score = 0;
    const lower = sentence.toLowerCase();
    
    // 包含指示词加分
    indicatorWords.forEach(word => {
      if (lower.includes(word)) score += 2;
    });
    
    // 短句加分
    if (sentence.length < 50) score += 1;
    
    // 包含数字加分（可能是具体信息）
    if (/\d+/.test(sentence)) score += 1;
    
    return { sentence, score };
  });
  
  // 按分数排序，取前几名
  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, 10)
    .map(item => item.sentence);
}

/**
 * 识别对话主题
 * @param {string} content - 对话内容
 * @returns {string} 识别的主题
 */
function identifyTopic(content) {
  const topicKeywords = {
    '项目': ['项目', '开发', '产品', '功能', '需求', '迭代'],
    '技术': ['技术', '代码', '编程', '框架', '语言', '工具'],
    '学习': ['学习', '教程', '课程', '知识', '理解', '掌握'],
    '工作': ['工作', '任务', '会议', '汇报', '进度'],
    '生活': ['生活', '日常', '习惯', '健康', '运动'],
    '创意': ['创意', '想法', '灵感', '设计', '艺术']
  };
  
  const scores = {};
  const lowerContent = content.toLowerCase();
  
  Object.entries(topicKeywords).forEach(([topic, keywords]) => {
    scores[topic] = keywords.reduce((count, keyword) => {
      const regex = new RegExp(keyword, 'g');
      const matches = lowerContent.match(regex);
      return count + (matches ? matches.length : 0);
    }, 0);
  });
  
  // 找到得分最高的主题
  const maxScore = Math.max(...Object.values(scores));
  if (maxScore === 0) return '综合讨论';
  
  const matchedTopics = Object.entries(scores)
    .filter(([_, score]) => score === maxScore)
    .map(([topic]) => topic);
  
  return matchedTopics.join(' / ');
}

/**
 * 提取关键结论
 * @param {string} content - 对话内容
 * @returns {Array<string>} 结论列表
 */
function extractConclusions(content) {
  const conclusionIndicators = [
    '所以', '因此', '于是', '最终', '结论',
    '决定', '确定', '采用', '选择', '同意',
    '就这样', '好了', 'ok', '好的'
  ];
  
  const sentences = extractSentences(content);
  
  return sentences
    .filter(sentence => {
      const lower = sentence.toLowerCase();
      return conclusionIndicators.some(indicator => lower.startsWith(indicator) || lower.includes(indicator));
    })
    .slice(0, 5);
}

/**
 * 生成摘要文本
 * @param {Array<string>} keyPoints - 要点列表
 * @param {number} maxLength - 最大长度
 * @returns {string} 摘要文本
 */
function generateSummary(keyPoints, maxLength) {
  const summary = keyPoints.slice(0, 3).join('。');
  
  if (summary.length <= maxLength) {
    return summary;
  }
  
  return summary.substring(0, maxLength - 3) + '...';
}

/**
 * 格式化总结输出
 * @param {Object} summaryData - 总结数据
 * @returns {string} 格式化的输出
 */
function formatSummary(summaryData) {
  const { topic, keyPoints, conclusions } = summaryData;
  
  let output = `📊 对话总结\n\n`;
  output += `**主题**：${topic}\n\n`;
  output += `**核心要点**：\n`;
  
  keyPoints.forEach((point, index) => {
    output += `${index + 1}. ${point}\n`;
  });
  
  if (conclusions.length > 0) {
    output += `\n**关键结论**：\n`;
    conclusions.forEach((conclusion, index) => {
      output += `- ${conclusion}\n`;
    });
  }
  
  return output;
}

module.exports = {
  summarize,
  formatSummary,
  extractSentences,
  identifyTopic,
  extractConclusions
};
