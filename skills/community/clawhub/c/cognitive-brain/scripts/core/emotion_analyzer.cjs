/**
 * 情感分析模块
 * 分析文本的情感状态和意图
 */

// 情感词典
const EMOTION_WORDS = {
  positive: ['开心', '高兴', '喜欢', '棒', '好', '成功', 'great', 'good', 'love', '谢谢', '感谢', '优秀', '完美', '赞', '厉害', '牛', '不错', '满意', '期待', '希望', '努力', '进步', '成长', '完成', '解决'],
  negative: ['难过', '伤心', '讨厌', '差', '失败', '错误', 'bad', 'sad', 'error', '不对', '错了', '问题', 'bug', '崩溃', '失望', '沮丧', '烦', '累', '压力', '担心', '焦虑', '困惑', '迷茫', '遗憾', '抱歉', '对不起'],
  urgent: ['紧急', '马上', '立刻', 'urgent', 'asap', '赶紧', '快点', '重要', '关键', '必须', '一定'],
  curious: ['为什么', '怎么', '如何', '什么', '哪', '？', '?', '想知道', '好奇', '请问', '能否', '可以吗'],
  excited: ['太棒', '太好了', '终于', '成功', '实现', '完成', '搞定', '新功能', '突破', '发现']
};

// 高意图模式
const HIGH_INTENT_PATTERNS = [
  /记住[这那]?[个条]?/i, /(?:请|帮我)?记住/i,
  /这[个条]?很?重要/i, /(?:务必|一定|千万)?要?记住/i,
  /保存[这那]?[个条]?/i, /记下来/i,
  /别忘[记了]/i, /提醒[我你]?/i,
  /key[:\s]/i, /important[:\s]/i, /remember[:\s]/i
];

// 低意图模式
const LOW_INTENT_PATTERNS = [
  /测试[一]?下/i, /试一下/i, /看看/i, /随便/i,
  /只是.*问问/i, /好奇/i, /了解一下/i,
  /test/i, /just/i, /random/i
];

/**
 * 分析文本情感
 * @param {string} content - 输入内容
 * @returns {Object} - 情感分析结果
 */
function analyzeEmotion(content) {
  let valence = 0;
  let arousal = 0;
  let curiosity = 0;
  let excitement = 0;

  EMOTION_WORDS.positive.forEach(w => { if (content.includes(w)) valence += 0.15; });
  EMOTION_WORDS.negative.forEach(w => { if (content.includes(w)) valence -= 0.15; });
  EMOTION_WORDS.urgent.forEach(w => { if (content.includes(w)) arousal += 0.2; });
  EMOTION_WORDS.curious.forEach(w => { if (content.includes(w)) curiosity += 0.2; });
  EMOTION_WORDS.excited.forEach(w => { if (content.includes(w)) excitement += 0.2; });

  valence = Math.max(-1, Math.min(1, valence));
  arousal = Math.max(0, Math.min(1, arousal + Math.abs(valence) * 0.3));
  curiosity = Math.max(0, Math.min(1, curiosity));
  excitement = Math.max(0, Math.min(1, excitement));

  const emotionScores = {
    positive: Math.max(0, valence),
    negative: Math.max(0, -valence),
    urgent: arousal,
    curious: curiosity,
    excited: excitement
  };

  const maxEmotion = Object.entries(emotionScores).reduce((a, b) => a[1] > b[1] ? a : b);
  const dominantEmotion = maxEmotion[1] > 0.2 ? maxEmotion[0] : 'neutral';

  return {
    valence,
    arousal,
    curiosity,
    excitement,
    dominantEmotion,
    scores: emotionScores
  };
}

/**
 * 检测用户明确的记忆意图
 * @param {string} content - 输入内容
 * @returns {Object} - 意图检测结果
 */
function detectExplicitIntent(content) {
  const highMatch = HIGH_INTENT_PATTERNS.some(p => p.test(content));
  const lowMatch = LOW_INTENT_PATTERNS.some(p => p.test(content));

  if (highMatch && !lowMatch) {
    return { intent: 'high', confidence: 0.9 };
  } else if (lowMatch) {
    return { intent: 'low', confidence: 0.7 };
  }

  return { intent: 'auto', confidence: 0.5 };
}

module.exports = {
  analyzeEmotion,
  detectExplicitIntent,
  EMOTION_WORDS,
  HIGH_INTENT_PATTERNS,
  LOW_INTENT_PATTERNS
};
