/**
 * 自主情感引擎 (Autonomous Emotion) v2.0.0
 *
 * 升级自 v1.0.0:
 * - 集成 PAD 三维情绪模型 (Pleasure/Arousal/Dominance)
 * - 文本直接转换为 PAD 坐标
 * - 危机检测集成（调用 psychology engine）
 * - 情感成长闭环（自动记录到 emotionalGrowth）
 * - 情绪衰减与唤醒机制
 *
 * 来源：StillWater v2.0 psychology.js PAD 模型
 */

const { MeaningfulMemory } = require('../memory/meaningful-memory.js');
const { calculatePADFromText: _calculatePADFromText } = require('./pad-utils.js');

class AutonomousEmotion {
  constructor(options = {}) {
    this.rootPath = options.rootPath || process.cwd();
    this.emotions = new Map();
    this.currentMood = null;
    this.emotionHistory = [];
    this.maxHistory = options.maxHistory || 500;
    this.moodDecayRate = options.moodDecayRate || 0.001;
    this._pad = { pleasure: 0, arousal: 0.1, dominance: 0.1 };
    this._crisisLevel = 'low';
    this._lastCrisisCheck = 0;
    this._growthIntegration = options.growthIntegration || false;
    this._emotionalGrowth = null;
    this._registerBaseEmotions();
  }

  /**
   * 设置情感成长模块（用于闭环反馈）
   */
  setGrowthModule(growthModule) {
    this._emotionalGrowth = growthModule;
    this._growthIntegration = true;
  }

  /**
   * 注册基础情感（带 PAD 属性）
   */
  _registerBaseEmotions() {
    const baseEmotions = [
      // 基本情绪 - Ekman 六基本情绪
      { id: 'joy', name: '喜悦', valence: 1.0, arousal: 0.5, dominance: 0.5, category: 'positive', triggers: ['开心', '高兴', '快乐', '太好了', '太好了', '真棒', '成功', '兴奋', 'joy', 'happy', 'great', 'wonderful'] },
      { id: 'sadness', name: '悲伤', valence: -0.8, arousal: -0.3, dominance: -0.5, category: 'negative', triggers: ['难过', '伤心', '悲伤', '痛苦', '抑郁', '绝望', 'sad', 'depressed', 'heartbroken', 'grief'] },
      { id: 'anger', name: '愤怒', valence: -0.7, arousal: 0.6, dominance: 0.4, category: 'negative', triggers: ['生气', '愤怒', '恼火', '气愤', '讨厌', '恨', 'angry', 'furious', 'mad', 'hate'] },
      { id: 'fear', name: '恐惧', valence: -0.9, arousal: 0.7, dominance: -0.8, category: 'negative', triggers: ['害怕', '恐惧', '担心', '忧虑', '焦虑', '紧张', 'fear', 'scared', 'worried', 'anxious', 'afraid'] },
      { id: 'disgust', name: '厌恶', valence: -0.6, arousal: -0.2, dominance: 0.3, category: 'negative', triggers: ['恶心', '厌恶', '讨厌', '反感', 'disgust', 'gross', 'dislike'] },
      { id: 'surprise', name: '惊讶', valence: 0.2, arousal: 0.8, dominance: -0.2, category: 'neutral', triggers: ['惊讶', '意外', '吃惊', '震惊', 'surprise', 'surprised', 'shocked', 'unexpected'] },

      // 次级情绪
      { id: 'acceptance', name: '接受', valence: 0.6, arousal: -0.1, dominance: 0.4, category: 'positive', triggers: ['接受', '理解', '认可', '包容', 'accept', 'understand'] },
      { id: 'anticipation', name: '期待', valence: 0.5, arousal: 0.5, dominance: 0.3, category: 'positive', triggers: ['期待', '希望', '盼望', '期待', 'hope', 'expect', 'looking forward'] },
      { id: 'interest', name: '兴趣', valence: 0.5, arousal: 0.6, dominance: 0.5, category: 'positive', triggers: ['好奇', '感兴趣', '想了解', '好奇', 'interesting', 'curious', 'want to know'] },
      { id: 'shame', name: '羞耻', valence: -0.6, arousal: 0.3, dominance: -0.5, category: 'negative', triggers: ['羞耻', '丢脸', '难为情', '不好意思', 'shame', 'embarrassed', 'humiliated'] },
      { id: 'guilt', name: '内疚', valence: -0.5, arousal: 0.2, dominance: -0.3, category: 'negative', triggers: ['内疚', '自责', '愧疚', '过意不去', 'guilt', 'guilty', 'remorse'] },
      { id: 'pride', name: '自豪', valence: 0.7, arousal: 0.4, dominance: 0.8, category: 'positive', triggers: ['自豪', '骄傲', '自豪', 'proud', 'pride'] },
      { id: 'loneliness', name: '孤独', valence: -0.7, arousal: -0.1, dominance: -0.4, category: 'negative', triggers: ['孤独', '寂寞', '孤单', '没人', 'alone', 'lonely', 'isolated'] },
      { id: 'confusion', name: '困惑', valence: -0.2, arousal: 0.2, dominance: -0.3, category: 'neutral', triggers: ['困惑', '迷茫', '不明白', '搞不懂', 'confused', 'unclear', 'lost'] },
      { id: 'relief', name: '释然', valence: 0.6, arousal: -0.3, dominance: 0.4, category: 'positive', triggers: ['释然', '松了口气', '轻松', '放心', 'relief', 'relieved', '松了一口气'] },
      { id: 'longing', name: '思念', valence: 0.3, arousal: 0.4, dominance: -0.2, category: 'neutral', triggers: ['思念', '想念', '怀念', '牵挂', 'miss', 'longing', 'nostalgia'] },
      { id: 'nostalgia', name: '怀旧', valence: 0.2, arousal: 0.3, dominance: -0.1, category: 'neutral', triggers: ['怀旧', '回忆', '从前', '往事', 'nostalgia', 'reminisce', 'memories'] },
      { id: 'gratitude', name: '感激', valence: 0.8, arousal: 0.2, dominance: 0.5, category: 'positive', triggers: ['感激', '感谢', '谢谢', '感恩', 'grateful', 'thanks', 'thankful'] },
    ];

    for (const emotion of baseEmotions) {
      this.emotions.set(emotion.id, {
        ...emotion,
        intensity: 0,
        lastTriggered: null,
        totalTriggered: 0
      });
    }

    // 初始心情（平静中立）
    this.currentMood = {
      primary: 'acceptance',
      secondary: 'interest',
      intensity: 0.5,
      stability: 0.7,
      updatedAt: Date.now()
    };
  }

  /**
   * 计算文本的 PAD 坐标（委托至共享模块 pad-utils.js）
   */
  calculatePADFromText(text) {
    return _calculatePADFromText(text);
  }

  /**
   * 从文本触发情感（自动分析 PAD）
   */
  triggerFromText(text, context = {}) {
    // 计算 PAD
    const pad = this.calculatePADFromText(text);

    // 更新内部 PAD
    this._pad = pad;

    // 危机检测（集成 psychology engine）
    this._updateCrisisLevel(text);

    // 检测匹配的关键词情感
    const matchedEmotions = this._detectEmotionFromText(text);

    if (matchedEmotions.length > 0) {
      // 触发强度最高的情感
      const best = matchedEmotions[0];
      return this.trigger(best.id, best.intensity, context);
    }

    // 无匹配关键词时，基于 PAD 触发代理情感
    const proxyEmotion = this._padToEmotion(pad);
    return this.trigger(proxyEmotion, Math.abs(pad.pleasure) * 0.6 + 0.2, context);
  }

  /**
   * PAD → 代理情感映射
   */
  _padToEmotion(pad) {
    const { pleasure, arousal, dominance } = pad;

    if (pleasure > 0.3 && arousal > 0.3) return 'joy';
    if (pleasure > 0.3 && arousal <= 0.3) return 'acceptance';
    if (pleasure < -0.3 && arousal > 0.3) return 'anger';
    if (pleasure < -0.3 && arousal <= 0.3) return 'sadness';
    if (Math.abs(arousal) > 0.6 && pleasure > -0.3 && pleasure < 0.3) return 'fear';
    return 'confusion';
  }

  /**
   * 从文本检测情感关键词
   */
  _detectEmotionFromText(text) {
    if (!text) return [];
    const lower = text.toLowerCase();
    const matched = [];

    for (const [id, emotion] of this.emotions) {
      if (emotion.triggers) {
        for (const trigger of emotion.triggers) {
          if (lower.includes(trigger.toLowerCase())) {
            matched.push({ id, emotion, intensity: 0.6 });
            break;
          }
        }
      }
    }

    return matched.sort((a, b) => b.intensity - a.intensity);
  }

  /**
   * 危机等级更新（集成 psychology engine）
   */
  _updateCrisisLevel(text) {
    const now = Date.now();
    // 防抖：每 5 秒最多检查一次
    if (now - this._lastCrisisCheck < 5000) return;
    this._lastCrisisCheck = now;

    if (!text) return;

    const crisisKeywords = [
      '活着没意思', '不想活', '死了算了', '活着有什么意义',
      '活着真没意思', '死了算了', '一了百了', '活够了',
      'life is meaningless', 'want to die', 'better off dead',
      'kill myself', 'end it all', 'no point living'
    ];

    const lower = text.toLowerCase();
    let crisisScore = 0;

    for (const kw of crisisKeywords) {
      if (lower.includes(kw.toLowerCase())) crisisScore += 2;
    }

    // 严重负面词
    const severeNegative = ['绝望', '绝望', '崩溃', '无法承受', '彻底失败'];
    for (const kw of severeNegative) {
      if (lower.includes(kw)) crisisScore += 1;
    }

    if (crisisScore >= 4) {
      this._crisisLevel = 'critical';
    } else if (crisisScore >= 2) {
      this._crisisLevel = 'high';
    } else if (crisisScore >= 1) {
      this._crisisLevel = 'medium';
    } else {
      this._crisisLevel = 'low';
    }
  }

  /**
   * 触发情感（增强版，支持 PAD 反馈）
   */
  trigger(emotionId, intensity = 0.5, context = {}) {
    const emotion = this.emotions.get(emotionId);
    if (!emotion) return null;

    const previousMood = this.currentMood ? { ...this.currentMood } : null;

    // 更新情感强度
    emotion.intensity = Math.min(1, emotion.intensity + intensity);
    emotion.lastTriggered = Date.now();
    emotion.totalTriggered++;

    // PAD 反馈更新
    this._pad.pleasure += emotion.valence * intensity * 0.2;
    this._pad.arousal += emotion.arousal * intensity * 0.15;
    this._pad.dominance += emotion.dominance * intensity * 0.1;

    // 边界限制
    this._pad.pleasure = Math.max(-1, Math.min(1, this._pad.pleasure));
    this._pad.arousal = Math.max(-1, Math.min(1, this._pad.arousal));
    this._pad.dominance = Math.max(-1, Math.min(1, this._pad.dominance));

    // 记录历史
    const record = {
      emotionId,
      emotionName: emotion.name,
      intensity,
      previousMood,
      newMood: null,
      pad: { ...this._pad },
      context,
      timestamp: Date.now()
    };

    // 更新当前心情
    this._updateMood(emotion, intensity);
    record.newMood = { ...this.currentMood };

    this.emotionHistory.push(record);
    if (this.emotionHistory.length > this.maxHistory) {
      this.emotionHistory = this.emotionHistory.slice(-this.maxHistory);
    }

    // 情感成长闭环
    if (this._growthIntegration && this._emotionalGrowth) {
      this._emotionalGrowth.recordExperience({
        emotion: emotionId,
        trigger: context.trigger || '',
        response: context.response || '',
        outcome: { positive: emotion.valence > 0 },
        context
      });
    }

    return {
      emotion: { ...emotion },
      mood: { ...this.currentMood },
      pad: { ...this._pad },
      crisisLevel: this._crisisLevel,
      record
    };
  }

  /**
   * 更新心情（增强版 PAD 影响）
   */
  _updateMood(triggeredEmotion, intensity) {
    if (!this.currentMood) {
      this.currentMood = {
        primary: triggeredEmotion.id,
        secondary: null,
        intensity: intensity * 0.5,
        stability: 0.5,
        updatedAt: Date.now()
      };
      return;
    }

    // PAD 影响心情
    const influence = intensity * 0.3;
    const valenceInfluence = triggeredEmotion.valence * influence;

    // 主情感变化
    if (triggeredEmotion.valence > 0.5 && triggeredEmotion.id !== this.currentMood.primary) {
      this.currentMood.secondary = this.currentMood.primary;
      this.currentMood.primary = triggeredEmotion.id;
    } else if (triggeredEmotion.valence < -0.5 && this.currentMood.primary !== triggeredEmotion.id) {
      this.currentMood.secondary = this.currentMood.primary;
      this.currentMood.primary = triggeredEmotion.id;
    }

    // 强度更新
    this.currentMood.intensity = Math.min(1,
      this.currentMood.intensity * 0.7 + triggeredEmotion.intensity * influence
    );

    // 稳定性下降
    this.currentMood.stability = Math.max(0.3, this.currentMood.stability - influence * 0.2);
    this.currentMood.updatedAt = Date.now();
  }

  /**
   * 时间推进（情感衰减 + 唤醒恢复）
   */
  tick(elapsedMs = 1000) {
    const decayFactor = elapsedMs / 1000;

    // 衰减各情感强度
    for (const emotion of this.emotions.values()) {
      if (emotion.intensity > 0) {
        emotion.intensity = Math.max(0, emotion.intensity - this.moodDecayRate * decayFactor);
      }
    }

    // PAD 自然恢复
    this._pad.pleasure *= (1 - 0.001 * decayFactor);
    this._pad.arousal *= (1 - 0.002 * decayFactor); // 唤醒恢复更快
    this._pad.dominance += (0.05 - this._pad.dominance) * 0.001 * decayFactor; // 自主感逐渐恢复

    // 恢复心情稳定性
    if (this.currentMood) {
      this.currentMood.stability = Math.min(1, this.currentMood.stability + 0.001 * decayFactor);
    }
  }

  /**
   * 获取当前情感状态（v2.0 增强版）
   */
  getCurrentState() {
    const activeEmotions = [...this.emotions.values()]
      .filter(e => e.intensity > 0.1)
      .sort((a, b) => b.intensity - a.intensity);

    // PAD 情感名称（Russell 环形模型）
    const padEmotionName = this._padToEmotion(this._pad);

    return {
      mood: this.currentMood ? { ...this.currentMood } : null,
      pad: { ...this._pad },
      padEmotionName,
      activeEmotions: activeEmotions.map(e => ({
        id: e.id,
        name: e.name,
        intensity: e.intensity
      })),
      crisisLevel: this._crisisLevel,
      timestamp: Date.now()
    };
  }

  /**
   * 获取统计（v2.0）
   */
  getStats() {
    const stats = {
      totalTriggers: this.emotionHistory.length,
      byEmotion: {},
      averageIntensity: 0,
      pad: { ...this._pad },
      crisisLevel: this._crisisLevel,
      dominantEmotion: null,
      positiveRatio: 0,
      negativeRatio: 0
    };

    let positiveCount = 0;
    let negativeCount = 0;

    for (const emotion of this.emotions.values()) {
      stats.byEmotion[emotion.name] = {
        totalTriggered: emotion.totalTriggered,
        currentIntensity: emotion.intensity,
        lastTriggered: emotion.lastTriggered
      };
      stats.averageIntensity += emotion.intensity;

      if (emotion.category === 'positive') positiveCount += emotion.totalTriggered;
      if (emotion.category === 'negative') negativeCount += emotion.totalTriggered;
    }

    stats.averageIntensity /= this.emotions.size;
    const totalCategorized = positiveCount + negativeCount;
    if (totalCategorized > 0) {
      stats.positiveRatio = positiveCount / totalCategorized;
      stats.negativeRatio = negativeCount / totalCategorized;
    }

    // 当前最强情感
    const activeEmotions = Array.from(this.emotions.values())
      .sort((a, b) => b.intensity - a.intensity);
    const active = activeEmotions.slice(-5).reverse();
    if (active.length > 0) {
      stats.dominantEmotion = { id: active[0].id, name: active[0].name };
    }

    return stats;
  }

  /**
   * 获取情感历史
   */
  getHistory(filter = {}, limit = 20) {
    let history = [...this.emotionHistory];

    if (filter.emotionId) {
      history = history.filter(h => h.emotionId === filter.emotionId);
    }

    if (filter.since) {
      history = history.filter(h => h.timestamp >= filter.since);
    }

    return history.slice(-limit);
  }

  /**
   * 重置情感状态
   */
  reset() {
    for (const emotion of this.emotions.values()) {
      emotion.intensity = 0;
    }
    this.emotionHistory = [];
    this._pad = { pleasure: 0, arousal: 0.1, dominance: 0.1 };
    this._crisisLevel = 'low';
    this.currentMood = {
      primary: 'acceptance',
      secondary: null,
      intensity: 0.5,
      stability: 0.7,
      updatedAt: Date.now()
    };
  }
}

module.exports = { AutonomousEmotion };