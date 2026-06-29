/**
 * PAD 文本分析共享工具 (PAD Text Analysis Shared Utilities)
 *
 * 统一的 PAD (Pleasure/Arousal/Dominance) 词库与文本分析函数。
 * 消除 emotional-growth.js 与 autonomous-emotion.js 之间的重复实现，
 * 确保同一文本在任何模块中产生一致的 PAD 评分。
 *
 * 来源：StillWater v2.0 psychology.js PAD 模型
 */

/**
 * PAD 词库（合并自 emotional-growth.js 与 autonomous-emotion.js，已去重）
 */
const PADWordLibrary = {
  pleasure: {
    positive: [
      '好', '棒', '优秀', '喜欢', '爱', '开心', '高兴', '快乐',
      '太棒', '真棒', '完美', '感谢', '感激', '谢谢',
      'good', 'great', 'excellent', 'love', 'like', 'happy',
      'wonderful', 'awesome', 'perfect', 'thanks', 'thankful'
    ],
    negative: [
      '坏', '差', '糟糕', '讨厌', '恨', '不喜欢', '难过', '伤心',
      '失望', '绝望',
      'bad', 'terrible', 'awful', 'hate', 'dislike', 'sad',
      'disappointed', 'worst', 'horrible'
    ]
  },
  arousal: {
    high: [
      '激动', '兴奋', '震惊', '紧张', '担心', '焦虑', '害怕', '愤怒',
      'excited', 'shocked', 'nervous', 'worried', 'anxious', 'scared',
      'angry', 'thrilled'
    ],
    low: [
      '平静', '冷静', '放松', '无聊', '疲惫', '累',
      'calm', 'relaxed', 'peaceful', 'bored', 'tired', 'exhausted'
    ]
  },
  dominance: {
    high: [
      '自信', '确定', '控制', '掌握', '主动', '相信', '肯定',
      'confident', 'certain', 'control', 'sure', 'definitely'
    ],
    low: [
      '无助', '失控', '无力', '被动', '迷茫',
      'helpless', 'lost', 'uncertain', 'confused'
    ]
  }
};

/**
 * 从文本计算 PAD 坐标
 *
 * 遍历词库中的正面/负面、高唤醒/低唤醒、高控制/低控制词汇，
 * 根据匹配数量累加各维度得分，最终限制在 [-1, 1] 区间。
 *
 * @param {string} text - 待分析文本
 * @returns {{ pleasure: number, arousal: number, dominance: number, matches: number }}
 */
function calculatePADFromText(text) {
  if (!text || typeof text !== 'string') {
    return { pleasure: 0, arousal: 0, dominance: 0, matches: 0 };
  }

  const lower = text.toLowerCase();
  let pleasure = 0, arousal = 0, dominance = 0;
  let matches = 0;

  // pleasure 维度
  for (const w of PADWordLibrary.pleasure.positive) {
    if (lower.includes(w)) { pleasure += 0.15; matches++; }
  }
  for (const w of PADWordLibrary.pleasure.negative) {
    if (lower.includes(w)) { pleasure -= 0.15; matches++; }
  }

  // arousal 维度
  for (const w of PADWordLibrary.arousal.high) {
    if (lower.includes(w)) { arousal += 0.2; matches++; }
  }
  for (const w of PADWordLibrary.arousal.low) {
    if (lower.includes(w)) { arousal -= 0.2; matches++; }
  }

  // dominance 维度
  for (const w of PADWordLibrary.dominance.high) {
    if (lower.includes(w)) { dominance += 0.15; matches++; }
  }
  for (const w of PADWordLibrary.dominance.low) {
    if (lower.includes(w)) { dominance -= 0.15; matches++; }
  }

  // 边界限制
  pleasure = Math.max(-1, Math.min(1, pleasure));
  arousal = Math.max(-1, Math.min(1, arousal));
  dominance = Math.max(-1, Math.min(1, dominance));

  return { pleasure, arousal, dominance, matches };
}

module.exports = { PADWordLibrary, calculatePADFromText };
