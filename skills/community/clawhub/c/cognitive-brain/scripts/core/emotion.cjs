#!/usr/bin/env node
/**
 * Cognitive Brain - 情感识别模块
 * 分析用户输入的情感和情绪状态
 */

// 情感词汇表
const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('emotion');
const EMOTION_VOCAB = {
  positive: {
    happy: ['开心', '高兴', '快乐', '幸福', '愉快', '哈哈', '嘻嘻', '😄', '😊', 'happy', 'glad', 'joy'],
    excited: ['兴奋', '激动', '期待', '太好了', '棒极了', '太棒了', '🎉', 'awesome', 'excited'],
    grateful: ['谢谢', '感谢', '感激', '辛苦了', '麻烦你了', 'thanks', 'thank you', '🙏'],
    satisfied: ['满意', '不错', '很好', '好的', '行', '可以', '完美', 'great', 'perfect'],
    hopeful: ['希望', '期待', '相信', '应该可以', '能行', 'hope', 'wish']
  },

  negative: {
    angry: ['生气', '愤怒', '火大', '烦死了', '气死', '😡', 'angry', 'mad', 'hate'],
    sad: ['难过', '伤心', '失望', '沮丧', '郁闷', '😢', '😭', 'sad', 'upset', 'depressed'],
    anxious: ['担心', '焦虑', '紧张', '害怕', '恐惧', '不安', 'anxious', 'worried', 'nervous'],
    frustrated: ['烦', '崩溃', '无语', '受不了', '要疯了', 'frustrated', 'annoyed'],
    disappointed: ['失望', '遗憾', '可惜', '唉', '叹气', 'disappointed', 'unfortunately']
  },

  neutral: {
    curious: ['好奇', '想知道', '疑问', '？', '吗', '呢', 'curious', 'wonder'],
    confused: ['困惑', '不明白', '不懂', '啥意思', '搞不懂', 'confused', 'confusing'],
    surprised: ['惊讶', '意外', '没想到', '居然', '竟然', 'surprised', 'wow']
  }
};

// 情感强度修饰词
const INTENSITY_MODIFIERS = {
  intensifiers: ['非常', '特别', '很', '超级', '极其', '太', '真', '好', 'really', 'very', 'so', 'extremely'],
  diminishers: ['有点', '稍微', '一点', '略', '还算', 'kind of', 'a bit', 'slightly']
};

// 否定词
const NEGATION_WORDS = ['不', '没', '别', '非', '未', '不是', '没有', "don't", "not", "no"];

/**
 * 分析情感
 */
function analyzeSentiment(text) {
  const result = {
    text,
    sentiment: 'neutral',
    confidence: 0,
    emotions: [],
    intensity: 1,
    negated: false,
    details: {}
  };

  // 检测否定
  result.negated = detectNegation(text);

  // 检测强度修饰
  result.intensity = detectIntensity(text);

  // 统计各类情感词汇
  for (const [sentimentType, emotionGroups] of Object.entries(EMOTION_VOCAB)) {
    result.details[sentimentType] = { count: 0, emotions: {} };

    for (const [emotion, words] of Object.entries(emotionGroups)) {
      let matchCount = 0;

      for (const word of words) {
        if (text.toLowerCase().includes(word.toLowerCase())) {
          matchCount++;

          // 记录匹配的词
          if (!result.details[sentimentType].emotions[emotion]) {
            result.details[sentimentType].emotions[emotion] = [];
          }
          result.details[sentimentType].emotions[emotion].push(word);
        }
      }

      if (matchCount > 0) {
        result.details[sentimentType].count += matchCount;
        result.emotions.push({
          emotion,
          type: sentimentType,
          count: matchCount,
          score: matchCount * result.intensity * (result.negated ? -1 : 1)
        });
      }
    }
  }

  // 计算总体情感
  const positiveCount = result.details.positive?.count || 0;
  const negativeCount = result.details.negative?.count || 0;
  const neutralCount = result.details.neutral?.count || 0;

  const total = positiveCount + negativeCount + neutralCount;

  if (total === 0) {
    result.sentiment = 'neutral';
    result.confidence = 0.5;
  } else {
    // 如果有否定，可能反转情感
    const adjustedPositive = result.negated ? negativeCount : positiveCount;
    const adjustedNegative = result.negated ? positiveCount : negativeCount;

    if (adjustedPositive > adjustedNegative) {
      result.sentiment = 'positive';
      result.confidence = adjustedPositive / total;
    } else if (adjustedNegative > adjustedPositive) {
      result.sentiment = 'negative';
      result.confidence = adjustedNegative / total;
    } else {
      result.sentiment = 'neutral';
      result.confidence = 0.5;
    }
  }

  // 排序情感
  result.emotions.sort((a, b) => Math.abs(b.score) - Math.abs(a.score));

  return result;
}

/**
 * 检测否定
 */
function detectNegation(text) {
  for (const word of NEGATION_WORDS) {
    if (text.includes(word)) {
      return true;
    }
  }
  return false;
}

/**
 * 检测强度
 */
function detectIntensity(text) {
  let intensity = 1;

  for (const word of INTENSITY_MODIFIERS.intensifiers) {
    if (text.includes(word)) {
      intensity *= 1.5;
    }
  }

  for (const word of INTENSITY_MODIFIERS.diminishers) {
    if (text.includes(word)) {
      intensity *= 0.5;
    }
  }

  return intensity;
}

/**
 * 获取情感趋势
 */
function getEmotionTrend(history) {
  if (!history || history.length === 0) {
    return { trend: 'stable', average: 0 };
  }

  const sentiments = history.map(h => {
    switch (h.sentiment) {
      case 'positive': return 1;
      case 'negative': return -1;
      default: return 0;
    }
  });

  const average = sentiments.reduce((a, b) => a + b, 0) / sentiments.length;

  // 计算趋势
  if (sentiments.length >= 3) {
    const recent = sentiments.slice(-3);
    const older = sentiments.slice(-6, -3);

    if (older.length > 0) {
      const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
      const olderAvg = older.reduce((a, b) => a + b, 0) / older.length;

      if (recentAvg - olderAvg > 0.2) {
        return { trend: 'improving', average };
      } else if (recentAvg - olderAvg < -0.2) {
        return { trend: 'declining', average };
      }
    }
  }

  return { trend: 'stable', average };
}

/**
 * 推断用户情绪状态
 */
function inferUserState(recentSentiments) {
  if (!recentSentiments || recentSentiments.length === 0) {
    return { state: 'unknown', confidence: 0 };
  }

  const lastSentiment = recentSentiments[recentSentiments.length - 1];
  const trend = getEmotionTrend(recentSentiments);

  // 基于最近的情感和趋势判断状态
  if (lastSentiment.sentiment === 'negative') {
    if (trend.trend === 'declining') {
      return { state: 'distressed', confidence: 0.8, suggestion: '需要安慰和支持' };
    }
    return { state: 'upset', confidence: 0.7, suggestion: '可能需要帮助' };
  }

  if (lastSentiment.sentiment === 'positive') {
    if (trend.trend === 'improving') {
      return { state: 'happy', confidence: 0.8, suggestion: '保持积极互动' };
    }
    return { state: 'content', confidence: 0.6, suggestion: '正常互动即可' };
  }

  if (lastSentiment.emotions.some(e => e.emotion === 'curious')) {
    return { state: 'curious', confidence: 0.7, suggestion: '提供详细信息' };
  }

  if (lastSentiment.emotions.some(e => e.emotion === 'confused')) {
    return { state: 'confused', confidence: 0.7, suggestion: '需要更清晰的解释' };
  }

  return { state: 'neutral', confidence: 0.5, suggestion: '正常互动' };
}

/**
 * 建议响应风格
 */
function suggestResponseStyle(sentimentResult) {
  const { sentiment, emotions, intensity } = sentimentResult;

  const style = {
    tone: 'neutral',
    formality: 'casual',
    empathy: 'low',
    proactivity: 'normal'
  };

  if (sentiment === 'negative') {
    style.tone = 'supportive';
    style.empathy = 'high';

    if (emotions.some(e => e.emotion === 'angry')) {
      style.formality = 'polite';
      style.proactivity = 'low'; // 不要激怒用户
    }

    if (emotions.some(e => e.emotion === 'sad')) {
      style.tone = 'comforting';
      style.empathy = 'very_high';
    }

    if (emotions.some(e => e.emotion === 'frustrated')) {
      style.tone = 'helpful';
      style.proactivity = 'high'; // 快速解决问题
    }
  }

  if (sentiment === 'positive') {
    style.tone = 'friendly';

    if (emotions.some(e => e.emotion === 'grateful')) {
      style.tone = 'warm';
      style.formality = 'polite';
    }

    if (emotions.some(e => e.emotion === 'excited')) {
      style.tone = 'enthusiastic';
    }
  }

  // 强度调整
  if (intensity > 1.2) {
    style.empathy = 'high'; // 强烈情感需要更多关注
  }

  return style;
}

// ===== 主函数 =====
async function main() {
  const text = process.argv.slice(2).join(' ');

  if (!text) {
    console.log(`
情感识别模块

用法:
  node emotion.cjs "用户输入文本"

示例:
  node emotion.cjs "今天太开心了！"
  node emotion.cjs "真烦，又出错了"
  node emotion.cjs "不太明白这是什么意思"
    `);
    return;
  }

  const result = analyzeSentiment(text);

  console.log('📝 输入:', text);
  console.log('\n🎯 情感分析:');
  console.log(`   总体情感: ${result.sentiment}`);
  console.log(`   置信度: ${(result.confidence * 100).toFixed(1)}%`);
  console.log(`   强度: ${result.intensity.toFixed(2)}x`);
  console.log(`   是否否定: ${result.negated ? '是' : '否'}`);

  if (result.emotions.length > 0) {
    console.log('\n😊 检测到的情感:');
    result.emotions.slice(0, 5).forEach(e => {
      console.log(`   ${e.emotion}: ${e.count} 次 (${e.type})`);
    });
  }

  const style = suggestResponseStyle(result);
  console.log('\n💬 建议响应风格:');
  console.log(`   语调: ${style.tone}`);
  console.log(`   正式度: ${style.formality}`);
  console.log(`   同理心: ${style.empathy}`);
  console.log(`   主动性: ${style.proactivity}`);
}

main();

