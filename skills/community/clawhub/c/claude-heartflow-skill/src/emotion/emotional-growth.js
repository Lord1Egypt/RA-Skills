/**
 * 情感成长 (Emotional Growth) v2.0.0
 *
 * 升级自 v1.0.0:
 * - 接收 autonomous-emotion 闭环反馈（自动监听情感触发）
 * - 模式学习 → 自动调整情感参数（自适应学习率）
 * - 成长轨迹可视化（时间序列、聚合模式、成长指数）
 * - 基于经验的预测（下次触发最佳响应推荐）
 *
 * 来源：StillWater v2.0 psychology.js PAD 模型
 */

class EmotionalGrowth {
  constructor(options = {}) {
    this.emotionModule = options.emotionModule || null;
    this.growthHistory = [];
    this.patterns = new Map();
    this.maxHistory = options.maxHistory || 500;
    this.learningRate = options.learningRate || 0.1;

    // v2.0 新增：自适应参数
    this._adaptiveParams = {
      // 基于experience统计自动计算
      optimalLearningRate: 0.1,
      // 情感参数偏差校正
      valenceBias: 0,
      arousalBias: 0,
      // 动态成功率阈值
      successThreshold: 0.4,
      minSampleSize: 3
    };

    // v2.0 新增：成长轨迹数据
    this._trajectoryData = [];

    // v2.0 新增：PAD词库（参考 autonomous-emotion.js）
    this._PADWordLibrary = {
      pleasure: {
        positive: ['好', '棒', '优秀', '喜欢', '爱', '开心', '高兴', '快乐', '太棒', '真棒', '完美', '感谢', '感激', '谢谢', 'good', 'great', 'excellent', 'love', 'like', 'happy', 'wonderful', 'awesome', 'perfect'],
        negative: ['坏', '差', '糟糕', '讨厌', '恨', '不喜欢', '难过', '伤心', '失望', '绝望', 'bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'disappointed', 'worst', 'horrible']
      },
      arousal: {
        high: ['激动', '兴奋', '震惊', '紧张', '担心', '焦虑', '害怕', '愤怒', 'excited', 'shocked', 'nervous', 'worried', 'anxious', 'scared', 'angry', 'thrilled'],
        low: ['平静', '冷静', '放松', '无聊', '疲惫', '累', 'calm', 'relaxed', 'peaceful', 'bored', 'tired', 'exhausted']
      },
      dominance: {
        high: ['自信', '确定', '控制', '掌握', '主动', '相信', '肯定', 'confident', 'certain', 'control', 'sure', 'definitely'],
        low: ['无助', '失控', '无力', '被动', '迷茫', 'helpless', 'lost', 'uncertain', 'confused']
      }
    };

    // 绑定情感监听（如果提供了emotionModule）
    if (this.emotionModule) {
      this._bindEmotionListener();
    }
  }

  /**
   * 设置情感模块并绑定监听
   */
  setEmotionModule(emotionModule) {
    this.emotionModule = emotionModule;
    this._bindEmotionListener();
  }

  /**
   * 绑定情感触发监听（自动记录，无需手动调用）
   */
  _bindEmotionListener() {
    if (!this.emotionModule) return;

    // 监听原生方法包装
    const originalTrigger = this.emotionModule.trigger.bind(this.emotionModule);
    const self = this;

    this.emotionModule.trigger = function(emotionId, intensity, context) {
      const result = originalTrigger(emotionId, intensity, context);

      // 自动记录情感经历
      if (result) {
        self._autoRecordExperience({
          emotionId,
          emotionName: result.emotion?.name || emotionId,
          intensity,
          pad: result.pad,
          context,
          outcome: { positive: result.emotion?.valence > 0 }
        });
      }

      return result;
    };

    // 监听文本情感触发
    const originalTriggerFromText = this.emotionModule.triggerFromText?.bind(this.emotionModule);
    if (originalTriggerFromText) {
      this.emotionModule.triggerFromText = function(text, context) {
        const result = originalTriggerFromText(text, context);

        if (result) {
          // 基于文本PAD分析自动记录
          self._autoRecordFromText(text, result, context);
        }

        return result;
      };
    }
  }

  /**
   * 自动记录情感经历（从emotionModule闭环）
   */
  _autoRecordExperience(data) {
    const record = {
      id: `exp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      emotion: data.emotionId,
      emotionName: data.emotionName,
      trigger: data.context?.trigger || this._extractTrigger(data.context),
      response: data.context?.response || '',
      outcome: data.outcome,
      pad: data.pad,
      intensity: data.intensity,
      context: data.context || {},
      timestamp: Date.now(),
      learned: false,
      autoRecorded: true  // 标记为自动记录
    };

    this.growthHistory.push(record);
    this._updateTrajectory(record);
    this._learnFromExperience(record);
    this._cleanupHistory();
  }

  /**
   * 自动从文本触发中记录
   */
  _autoRecordFromText(text, result, context) {
    // 基于PAD词库分析触发词
    const triggerWords = this._extractTriggerWords(text);
    const padAnalysis = this.calculatePADFromText(text);

    const record = {
      id: `exp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      emotion: result.emotion?.id || 'unknown',
      emotionName: result.emotion?.name || result.padEmotionName || 'unknown',
      trigger: triggerWords.join(' ') || text.substring(0, 50),
      response: context?.response || '',
      outcome: { positive: padAnalysis.pleasure > 0 },
      pad: padAnalysis,
      intensity: result.emotion?.intensity || 0.5,
      context: { ...context, textAnalysis: padAnalysis },
      timestamp: Date.now(),
      learned: false,
      autoRecorded: true,
      textSource: true  // 标记为文本源
    };

    this.growthHistory.push(record);
    this._updateTrajectory(record);
    this._learnFromExperience(record);
    this._cleanupHistory();
  }

  /**
   * 从文本计算PAD坐标（参考 autonomous-emotion.js）
   */
  calculatePADFromText(text) {
    if (!text || typeof text !== 'string') {
      return { pleasure: 0, arousal: 0, dominance: 0, matches: 0 };
    }

    const lower = text.toLowerCase();
    let pleasure = 0, arousal = 0.1, dominance = 0.1;
    let matches = 0;

    // pleasure 维度
    for (const w of this._PADWordLibrary.pleasure.positive) {
      if (lower.includes(w)) { pleasure += 0.15; matches++; }
    }
    for (const w of this._PADWordLibrary.pleasure.negative) {
      if (lower.includes(w)) { pleasure -= 0.15; matches++; }
    }

    // arousal 维度
    for (const w of this._PADWordLibrary.arousal.high) {
      if (lower.includes(w)) { arousal += 0.2; matches++; }
    }
    for (const w of this._PADWordLibrary.arousal.low) {
      if (lower.includes(w)) { arousal -= 0.2; matches++; }
    }

    // dominance 维度
    for (const w of this._PADWordLibrary.dominance.high) {
      if (lower.includes(w)) { dominance += 0.15; matches++; }
    }
    for (const w of this._PADWordLibrary.dominance.low) {
      if (lower.includes(w)) { dominance -= 0.15; matches++; }
    }

    // 边界限制
    pleasure = Math.max(-1, Math.min(1, pleasure));
    arousal = Math.max(-1, Math.min(1, arousal));
    dominance = Math.max(-1, Math.min(1, dominance));

    return { pleasure, arousal, dominance, matches };
  }

  /**
   * 从文本提取触发词
   */
  _extractTriggerWords(text) {
    if (!text) return [];
    const lower = text.toLowerCase();
    const words = [];

    // 收集所有PAD词库中匹配到的词
    const allWords = [
      ...this._PADWordLibrary.pleasure.positive,
      ...this._PADWordLibrary.pleasure.negative,
      ...this._PADWordLibrary.arousal.high,
      ...this._PADWordLibrary.arousal.low,
      ...this._PADWordLibrary.dominance.high,
      ...this._PADWordLibrary.dominance.low
    ];

    for (const w of allWords) {
      if (lower.includes(w.toLowerCase())) {
        words.push(w);
      }
    }

    return [...new Set(words)]; // 去重
  }

  /**
   * 从上下文提取触发源
   */
  _extractTrigger(context) {
    if (!context) return '';
    if (typeof context.trigger === 'string') return context.trigger;
    if (context.text) return context.text.substring(0, 100);
    return '';
  }

  /**
   * 手动记录情感经历（兼容v1.0）
   */
  recordExperience(experience) {
    const record = {
      id: `exp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      emotion: experience.emotion,
      emotionName: experience.emotionName || experience.emotion,
      trigger: experience.trigger || '',
      response: experience.response || '',
      outcome: experience.outcome || { positive: true },
      pad: experience.pad || this.calculatePADFromText(experience.trigger || ''),
      intensity: experience.intensity || 0.5,
      context: experience.context || {},
      timestamp: Date.now(),
      learned: false,
      autoRecorded: false
    };

    this.growthHistory.push(record);
    this._updateTrajectory(record);
    this._learnFromExperience(record);
    this._cleanupHistory();

    return record;
  }

  /**
   * 清理旧记录
   */
  _cleanupHistory() {
    if (this.growthHistory.length > this.maxHistory) {
      this.growthHistory = this.growthHistory.slice(-this.maxHistory);
    }
  }

  /**
   * 更新成长轨迹数据
   */
  _updateTrajectory(record) {
    const trajectoryPoint = {
      timestamp: record.timestamp,
      emotion: record.emotion,
      valence: record.pad?.pleasure || 0,
      arousal: record.pad?.arousal || 0,
      dominance: record.pad?.dominance || 0,
      positive: record.outcome?.positive || false,
      intensity: record.intensity || 0.5
    };

    this._trajectoryData.push(trajectoryPoint);

    // 轨迹数据也限制大小
    if (this._trajectoryData.length > this.maxHistory) {
      this._trajectoryData = this._trajectoryData.slice(-this.maxHistory);
    }
  }

  /**
   * 从经历中学习（v2.0 自适应增强）
   */
  _learnFromExperience(experience) {
    if (!experience.outcome) return;

    const isPositive = experience.outcome.positive !== false;
    const key = `${experience.emotion}_${this._normalizeTrigger(experience.trigger)}`;

    // 获取或创建模式
    let pattern = this.patterns.get(key);
    if (!pattern) {
      pattern = {
        emotion: experience.emotion,
        emotionName: experience.emotionName || experience.emotion,
        trigger: experience.trigger,
        occurrences: 0,
        positiveOutcomes: 0,
        negativeOutcomes: 0,
        lastOccurrence: null,
        adaptations: [],
        avgIntensity: 0,
        totalIntensity: 0,
        padHistory: [],
        successHistory: []  // 用于动态阈值
      };
      this.patterns.set(key, pattern);
    }

    // 更新模式统计
    pattern.occurrences++;
    pattern.lastOccurrence = Date.now();

    if (isPositive) {
      pattern.positiveOutcomes++;
    } else {
      pattern.negativeOutcomes++;
    }

    // 更新强度统计
    pattern.totalIntensity += experience.intensity || 0.5;
    pattern.avgIntensity = pattern.totalIntensity / pattern.occurrences;

    // 更新PAD历史
    if (experience.pad) {
      pattern.padHistory.push({ ...experience.pad, timestamp: experience.timestamp });
      if (pattern.padHistory.length > 20) {
        pattern.padHistory = pattern.padHistory.slice(-20);
      }
    }

    // 更新成功历史（用于动态阈值）
    pattern.successHistory.push(isPositive ? 1 : 0);
    if (pattern.successHistory.length > 10) {
      pattern.successHistory = pattern.successHistory.slice(-10);
    }

    // v2.0：自动调整学习率
    this._adjustLearningRate(experience);

    // v2.0：情感参数自适应
    this._adjustEmotionParams(experience);

    // 生成适应建议（带动态阈值）
    this._updateAdaptations(pattern, experience);
  }

  /**
   * 标准化触发词（用于模式匹配）
   */
  _normalizeTrigger(trigger) {
    if (!trigger) return 'unknown';
    return trigger.toLowerCase().trim().substring(0, 50);
  }

  /**
   * 自动调整学习率（基于experience统计）
   */
  _adjustLearningRate(experience) {
    const recentCount = Math.min(50, this.growthHistory.length);
    const recentHistory = this.growthHistory.slice(-recentCount);

    if (recentHistory.length < 10) return;

    // 计算近期成功率
    const recentSuccessRate = recentHistory.filter(e => e.outcome?.positive).length / recentHistory.length;

    // 成功率影响学习率
    if (recentSuccessRate > 0.7) {
      // 成功率高 → 降低学习率（已稳定）
      this._adaptiveParams.optimalLearningRate = Math.max(0.05,
        this._adaptiveParams.optimalLearningRate * 0.95);
    } else if (recentSuccessRate < 0.3) {
      // 成功率低 → 提高学习率（需要更多调整）
      this._adaptiveParams.optimalLearningRate = Math.min(0.5,
        this._adaptiveParams.optimalLearningRate * 1.1);
    }

    // 样本量影响学习率（样本越多，学习率越低）
    const sampleSizeFactor = Math.max(0.5, 1 - recentHistory.length / 200);
    this._adaptiveParams.optimalLearningRate *= sampleSizeFactor;
  }

  /**
   * 情感参数自适应（valence/arousal偏差校正）
   */
  _adjustEmotionParams(experience) {
    if (!experience.pad) return;

    const { pleasure, arousal, dominance } = experience.pad;

    // 计算预测偏差
    const predictedPositive = pleasure > 0;
    const actualPositive = experience.outcome?.positive;

    if (predictedPositive !== actualPositive) {
      // 偏差校正
      if (predictedPositive && !actualPositive) {
        // 高估了愉悦度
        this._adaptiveParams.valenceBias -= 0.05;
      } else if (!predictedPositive && actualPositive) {
        // 低估了愉悦度
        this._adaptiveParams.valenceBias += 0.05;
      }
    }

    // arousal偏差校正
    if (Math.abs(arousal) > 0.5) {
      const predictedHighArousal = arousal > 0;
      const pattern = this._findPattern(experience.emotion);

      if (pattern && pattern.avgIntensity > 0.6 !== predictedHighArousal) {
        this._adaptiveParams.arousalBias += predictedHighArousal ? 0.02 : -0.02;
      }
    }

    // 边界限制
    this._adaptiveParams.valenceBias = Math.max(-0.3, Math.min(0.3, this._adaptiveParams.valenceBias));
    this._adaptiveParams.arousalBias = Math.max(-0.3, Math.min(0.3, this._adaptiveParams.arousalBias));
  }

  /**
   * 查找模式
   */
  _findPattern(emotion) {
    for (const pattern of this.patterns.values()) {
      if (pattern.emotion === emotion) {
        return pattern;
      }
    }
    return null;
  }

  /**
   * 动态调整成功率阈值
   */
  _updateSuccessThreshold() {
    if (this.growthHistory.length < 20) return;

    const recentHistory = this.growthHistory.slice(-50);
    const globalSuccessRate = recentHistory.filter(e => e.outcome?.positive).length / recentHistory.length;

    // 基于全局成功率动态调整阈值
    if (globalSuccessRate > 0.7) {
      this._adaptiveParams.successThreshold = Math.min(0.6,
        this._adaptiveParams.successThreshold * 1.05);
    } else if (globalSuccessRate < 0.3) {
      this._adaptiveParams.successThreshold = Math.max(0.2,
        this._adaptiveParams.successThreshold * 0.95);
    }
  }

  /**
   * 更新适应建议
   */
  _updateAdaptations(pattern, experience) {
    if (pattern.occurrences < this._adaptiveParams.minSampleSize) return;

    const successRate = pattern.positiveOutcomes / pattern.occurrences;

    // 使用动态阈值
    this._updateSuccessThreshold();

    if (successRate < this._adaptiveParams.successThreshold) {
      const adaptation = this._generateAdaptation(experience, pattern);
      pattern.adaptations.push({
        ...adaptation,
        timestamp: Date.now(),
        successRate,
        basedOnSamples: pattern.occurrences
      });
    }

    experience.learned = true;
  }

  /**
   * 生成适应建议（v2.0 增强版）
   */
  _generateAdaptation(experience, pattern) {
    const suggestions = [];

    // 基于情感类型和PAD分析生成建议
    const emotion = experience.emotion;
    const pad = experience.pad || {};

    // 通用建议
    suggestions.push({
      type: 'observe',
      suggestion: '继续观察这个模式，记录更多样本',
      confidence: 0.3
    });

    // 根据情感类型生成建议
    if (emotion === 'anger' || pad.pleasure < -0.3) {
      suggestions.push({
        type: 'response_change',
        suggestion: '下次遇到类似触发时，尝试冷静处理，先深呼吸',
        confidence: 0.7
      });
      suggestions.push({
        type: 'reframe',
        suggestion: '尝试从不同角度看待问题',
        confidence: 0.6
      });
    }

    if (emotion === 'fear' || emotion === 'anxiety' || pad.arousal > 0.3) {
      suggestions.push({
        type: 'exposure',
        suggestion: '渐进式面对恐惧源头，从小步骤开始',
        confidence: 0.6
      });
      suggestions.push({
        type: 'grounding',
        suggestion: '使用接地技术缓解焦虑',
        confidence: 0.5
      });
    }

    if (emotion === 'sadness' || pad.pleasure < -0.5) {
      suggestions.push({
        type: 'action',
        suggestion: '悲伤时尝试做一些积极的事情，哪怕是小事',
        confidence: 0.5
      });
      suggestions.push({
        type: 'social',
        suggestion: '与信任的人分享感受',
        confidence: 0.6
      });
    }

    if (emotion === 'joy' || pad.pleasure > 0.5) {
      suggestions.push({
        type: 'amplify',
        suggestion: '记录这个积极时刻，便于日后回顾',
        confidence: 0.5
      });
      suggestions.push({
        type: 'share',
        suggestion: '与他人分享这份喜悦',
        confidence: 0.4
      });
    }

    // 基于PAD的通用建议
    if (pad.dominance < -0.3) {
      suggestions.push({
        type: 'empowerment',
        suggestion: '关注可控范围，建立自主感',
        confidence: 0.6
      });
    }

    if (pad.arousal < -0.3) {
      suggestions.push({
        type: 'activate',
        suggestion: '尝试激活能量，如运动或社交',
        confidence: 0.5
      });
    }

    // 选择最佳建议
    const best = suggestions.sort((a, b) => b.confidence - a.confidence)[0];

    return best || suggestions[0];
  }

  // ==================== v2.0 新增方法 ====================

  /**
   * 获取成长轨迹（时间序列数据）
   */
  getGrowthTrajectory(options = {}) {
    const {
      startTime = 0,
      endTime = Date.now(),
      emotion = null,
      granularity = 'day'  // 'hour', 'day', 'week'
    } = options;

    // 过滤时间范围
    let trajectory = this._trajectoryData.filter(t =>
      t.timestamp >= startTime && t.timestamp <= endTime
    );

    // 过滤情感
    if (emotion) {
      trajectory = trajectory.filter(t => t.emotion === emotion);
    }

    // 按时间粒度聚合
    const aggregated = this._aggregateByGranularity(trajectory, granularity);

    // 计算趋势
    const trend = this._calculateTrend(trajectory);

    return {
      data: aggregated,
      rawData: trajectory,
      trend,
      granularity,
      count: trajectory.length,
      timeRange: {
        start: trajectory[0]?.timestamp || startTime,
        end: trajectory[trajectory.length - 1]?.timestamp || endTime
      }
    };
  }

  /**
   * 按时间粒度聚合数据
   */
  _aggregateByGranularity(data, granularity) {
    if (data.length === 0) return [];

    const buckets = new Map();

    for (const point of data) {
      let bucketKey;

      const date = new Date(point.timestamp);
      if (granularity === 'hour') {
        bucketKey = new Date(date.getFullYear(), date.getMonth(), date.getDate(),
          date.getHours()).getTime();
      } else if (granularity === 'day') {
        bucketKey = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime();
      } else if (granularity === 'week') {
        const weekStart = new Date(date);
        weekStart.setDate(date.getDate() - date.getDay());
        bucketKey = new Date(weekStart.getFullYear(), weekStart.getMonth(), weekStart.getDate()).getTime();
      }

      if (!buckets.has(bucketKey)) {
        buckets.set(bucketKey, {
          timestamp: bucketKey,
          valence: [],
          arousal: [],
          dominance: [],
          intensity: [],
          positiveCount: 0,
          totalCount: 0,
          emotions: []
        });
      }

      const bucket = buckets.get(bucketKey);
      bucket.valence.push(point.valence);
      bucket.arousal.push(point.arousal);
      bucket.dominance.push(point.dominance);
      bucket.intensity.push(point.intensity);
      if (point.positive) bucket.positiveCount++;
      bucket.totalCount++;
      bucket.emotions.push(point.emotion);
    }

    // 计算聚合统计
    const result = [];
    for (const bucket of buckets.values()) {
      const avg = arr => arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;

      result.push({
        timestamp: bucket.timestamp,
        valence: avg(bucket.valence),
        arousal: avg(bucket.arousal),
        dominance: avg(bucket.dominance),
        intensity: avg(bucket.intensity),
        positiveRatio: bucket.totalCount > 0 ? bucket.positiveCount / bucket.totalCount : 0,
        experienceCount: bucket.totalCount,
        dominantEmotion: this._mostFrequent(bucket.emotions)
      });
    }

    return result.sort((a, b) => a.timestamp - b.timestamp);
  }

  /**
   * 计算趋势
   */
  _calculateTrend(data) {
    if (data.length < 2) {
      return { direction: 'stable', slope: 0, confidence: 0 };
    }

    // 简单线性回归
    const n = data.length;
    const sumX = data.reduce((sum, _, i) => sum + i, 0);
    const sumY = data.reduce((sum, p) => sum + p.valence, 0);
    const sumXY = data.reduce((sum, p, i) => sum + i * p.valence, 0);
    const sumX2 = data.reduce((sum, _, i) => sum + i * i, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const avgY = sumY / n;

    // 计算R²
    const ssTot = data.reduce((sum, p) => sum + Math.pow(p.valence - avgY, 2), 0);
    const ssRes = data.reduce((sum, p, i) => {
      const predicted = avgY + slope * i;
      return sum + Math.pow(p.valence - predicted, 2);
    }, 0);
    const rSquared = ssTot > 0 ? 1 - ssRes / ssTot : 0;

    let direction;
    if (Math.abs(slope) < 0.01) {
      direction = 'stable';
    } else if (slope > 0) {
      direction = 'improving';
    } else {
      direction = 'declining';
    }

    return {
      direction,
      slope: slope || 0,
      confidence: Math.max(0, Math.min(1, rSquared)),
      label: direction === 'improving' ? '积极向上' :
             direction === 'declining' ? '需要关注' : '基本稳定'
    };
  }

  /**
   * 获取最频繁元素
   */
  _mostFrequent(arr) {
    if (arr.length === 0) return null;
    const counts = new Map();
    for (const item of arr) {
      counts.set(item, (counts.get(item) || 0) + 1);
    }
    let maxItem = arr[0];
    let maxCount = 0;
    for (const [item, count] of counts) {
      if (count > maxCount) {
        maxCount = count;
        maxItem = item;
      }
    }
    return maxItem;
  }

  /**
   * 获取情感模式（按时间段聚合）
   */
  getEmotionalPatterns(options = {}) {
    const {
      groupBy = 'emotion',  // 'emotion', 'trigger', 'timeOfDay', 'outcome'
      timeRange = null,
      limit = 10
    } = options;

    let history = [...this.growthHistory];

    // 时间范围过滤
    if (timeRange) {
      const { start, end } = timeRange;
      history = history.filter(h =>
        h.timestamp >= (start || 0) && h.timestamp <= (end || Date.now())
      );
    }

    if (history.length === 0) {
      return { patterns: [], summary: { totalExperiences: 0 } };
    }

    let patterns = [];

    if (groupBy === 'emotion') {
      // 按情感类型聚合
      const emotionGroups = new Map();
      for (const exp of history) {
        if (!emotionGroups.has(exp.emotion)) {
          emotionGroups.set(exp.emotion, []);
        }
        emotionGroups.get(exp.emotion).push(exp);
      }

      patterns = [];
      for (const [emotion, experiences] of emotionGroups) {
        patterns.push(this._createEmotionPattern(emotion, experiences));
      }
    } else if (groupBy === 'trigger') {
      // 按触发词聚合
      const triggerGroups = new Map();
      for (const exp of history) {
        const trigger = this._normalizeTrigger(exp.trigger);
        if (!triggerGroups.has(trigger)) {
          triggerGroups.set(trigger, []);
        }
        triggerGroups.get(trigger).push(exp);
      }

      patterns = [];
      for (const [trigger, experiences] of triggerGroups) {
        patterns.push(this._createTriggerPattern(trigger, experiences));
      }
    } else if (groupBy === 'timeOfDay') {
      // 按时段聚合
      const timeGroups = { morning: [], afternoon: [], evening: [], night: [] };
      for (const exp of history) {
        const hour = new Date(exp.timestamp).getHours();
        let timeOfDay;
        if (hour >= 6 && hour < 12) timeOfDay = 'morning';
        else if (hour >= 12 && hour < 18) timeOfDay = 'afternoon';
        else if (hour >= 18 && hour < 22) timeOfDay = 'evening';
        else timeOfDay = 'night';

        timeGroups[timeOfDay].push(exp);
      }

      patterns = [];
      const timeLabels = { morning: '上午(6-12点)', afternoon: '下午(12-18点)', evening: '傍晚(18-22点)', night: '深夜(22-6点)' };
      for (const [timeOfDay, experiences] of Object.entries(timeGroups)) {
        if (experiences.length > 0) {
          patterns.push(this._createTimePattern(timeLabels[timeOfDay], experiences));
        }
      }
    } else if (groupBy === 'outcome') {
      // 按结果聚合
      const positive = history.filter(e => e.outcome?.positive);
      const negative = history.filter(e => !e.outcome?.positive);

      patterns = [
        this._createOutcomePattern('positive', '积极结果', positive),
        this._createOutcomePattern('negative', '消极结果', negative)
      ];
    }

    // 排序并限制数量
    patterns.sort((a, b) => b.count - a.count);
    patterns = patterns.slice(0, limit);

    return {
      patterns,
      groupBy,
      totalExperiences: history.length,
      timeRange: timeRange || { start: null, end: null }
    };
  }

  /**
   * 创建情感模式
   */
  _createEmotionPattern(emotion, experiences) {
    const positiveCount = experiences.filter(e => e.outcome?.positive).length;
    const totalCount = experiences.length;
    const successRate = totalCount > 0 ? positiveCount / totalCount : 0;

    // 提取PAD统计
    const valences = experiences.map(e => e.pad?.pleasure || 0).filter(v => v !== 0);
    const arousals = experiences.map(e => e.pad?.arousal || 0).filter(a => a !== 0);

    return {
      type: 'emotion',
      emotion,
      emotionName: experiences[0]?.emotionName || emotion,
      count: totalCount,
      successRate,
      positiveCount,
      negativeCount: totalCount - positiveCount,
      avgValence: valences.length > 0 ? valences.reduce((a, b) => a + b, 0) / valences.length : 0,
      avgArousal: arousals.length > 0 ? arousals.reduce((a, b) => a + b, 0) / arousals.length : 0,
      recentTriggers: [...new Set(experiences.slice(-5).map(e => e.trigger))].filter(t => t),
      lastOccurrence: experiences[experiences.length - 1]?.timestamp
    };
  }

  /**
   * 创建触发模式
   */
  _createTriggerPattern(trigger, experiences) {
    const positiveCount = experiences.filter(e => e.outcome?.positive).length;
    const totalCount = experiences.length;

    return {
      type: 'trigger',
      trigger,
      count: totalCount,
      successRate: totalCount > 0 ? positiveCount / totalCount : 0,
      emotions: [...new Set(experiences.map(e => e.emotion))],
      dominantEmotion: this._mostFrequent(experiences.map(e => e.emotion)),
      lastOccurrence: experiences[experiences.length - 1]?.timestamp
    };
  }

  /**
   * 创建时段模式
   */
  _createTimePattern(label, experiences) {
    const positiveCount = experiences.filter(e => e.outcome?.positive).length;
    const totalCount = experiences.length;

    return {
      type: 'timeOfDay',
      label,
      count: totalCount,
      successRate: totalCount > 0 ? positiveCount / totalCount : 0,
      dominantEmotion: this._mostFrequent(experiences.map(e => e.emotion)),
      avgIntensity: experiences.reduce((sum, e) => sum + (e.intensity || 0.5), 0) / totalCount
    };
  }

  /**
   * 创建结果模式
   */
  _createOutcomePattern(type, label, experiences) {
    return {
      type: 'outcome',
      outcomeType: type,
      label,
      count: experiences.length,
      dominantEmotion: this._mostFrequent(experiences.map(e => e.emotion)),
      avgIntensity: experiences.length > 0 ?
        experiences.reduce((sum, e) => sum + (e.intensity || 0.5), 0) / experiences.length : 0
    };
  }

  /**
   * 获取成长指数（0-100）
   */
  getGrowthScore() {
    if (this.growthHistory.length < 5) {
      return {
        score: 0,
        level: '数据不足',
        components: {
          patternCount: 0,
          adaptationCount: 0,
          learningRate: this._adaptiveParams.optimalLearningRate,
          adaptationCoverage: 0,
          consistency: 0,
          trend: 'stable'
        }
      };
    }

    // 各维度评分
    const patternCount = this.patterns.size;
    const patternScore = Math.min(20, patternCount * 2);  // 最高20分

    // 适应建议覆盖
    const adaptationCount = [...this.patterns.values()]
      .reduce((sum, p) => sum + p.adaptations.length, 0);
    const adaptationCoverage = this.patterns.size > 0 ?
      (patternCount > 0 ? adaptationCount / patternCount : 0) : 0;
    const adaptationScore = Math.min(20, adaptationCoverage * 10);  // 最高20分

    // 学习稳定性（成功率的方差）
    const successRates = [...this.patterns.values()]
      .filter(p => p.occurrences >= 3)
      .map(p => p.positiveOutcomes / p.occurrences);
    const consistency = successRates.length > 0 ?
      1 - (successRates.reduce((sum, r) => sum + Math.abs(r - 0.5), 0) / successRates.length * 2) : 0;
    const consistencyScore = Math.max(0, Math.min(20, consistency * 20));  // 最高20分

    // 学习率合理性
    const learningRateScore = this._adaptiveParams.optimalLearningRate >= 0.05 &&
      this._adaptiveParams.optimalLearningRate <= 0.3 ? 10 :
      this._adaptiveParams.optimalLearningRate > 0.3 ? 5 : 8;  // 最高10分

    // 趋势评分
    const trend = this._calculateTrend(this._trajectoryData);
    const trendScore = trend.direction === 'improving' ? 15 :
                       trend.direction === 'stable' ? 10 : 5;  // 最高15分

    // PAD偏差校正效果
    const biasScore = 15 - Math.abs(this._adaptiveParams.valenceBias) * 50 -
                      Math.abs(this._adaptiveParams.arousalBias) * 50;
    const normalizedBiasScore = Math.max(0, Math.min(15, biasScore));  // 最高15分

    const totalScore = Math.round(patternScore + adaptationScore + consistencyScore +
      learningRateScore + trendScore + normalizedBiasScore);

    // 级别判定
    let level;
    if (totalScore >= 80) level = '优秀';
    else if (totalScore >= 60) level = '良好';
    else if (totalScore >= 40) level = '一般';
    else if (totalScore >= 20) level = '需提升';
    else level = '需大量改进';

    return {
      score: Math.max(0, Math.min(100, totalScore)),
      level,
      components: {
        patternCount,
        patternScore: Math.round(patternScore),
        adaptationCount,
        adaptationCoverage: Math.round(adaptationCoverage * 100),
        adaptationScore: Math.round(adaptationScore),
        consistency: Math.round(consistency * 100),
        consistencyScore: Math.round(consistencyScore),
        learningRate: Math.round(this._adaptiveParams.optimalLearningRate * 100) / 100,
        learningRateScore: Math.round(learningRateScore),
        trend: trend.label,
        trendScore: Math.round(trendScore),
        biasCorrection: Math.round(normalizedBiasScore),
        totalScore: Math.round(totalScore)
      }
    };
  }

  /**
   * 预测下次触发时的最佳响应（v2.0 新增）
   */
  predictAdaptation(emotionId) {
    // 查找该情感的模式
    const patterns = [...this.patterns.values()]
      .filter(p => p.emotion === emotionId);

    if (patterns.length === 0) {
      // 无历史记录，返回默认建议
      return {
        emotionId,
        prediction: 'unknown',
        confidence: 0,
        suggestion: this._getDefaultSuggestion(emotionId),
        basedOn: 0
      };
    }

    // 聚合所有模式
    const totalOccurrences = patterns.reduce((sum, p) => sum + p.occurrences, 0);
    const totalPositive = patterns.reduce((sum, p) => sum + p.positiveOutcomes, 0);
    const successRate = totalOccurrences > 0 ? totalPositive / totalOccurrences : 0;

    // 找到最佳适应建议
    let bestAdaptation = null;
    let maxConfidence = 0;

    for (const pattern of patterns) {
      for (const adaptation of pattern.adaptations) {
        if (adaptation.confidence > maxConfidence) {
          maxConfidence = adaptation.confidence;
          bestAdaptation = adaptation;
        }
      }
    }

    // 计算预测置信度
    const sampleWeight = Math.min(1, totalOccurrences / 20);
    const successWeight = successRate;
    const confidence = (sampleWeight * 0.4 + successWeight * 0.6) * maxConfidence;

    return {
      emotionId,
      prediction: bestAdaptation?.type || 'observe',
      confidence: Math.round(confidence * 100) / 100,
      suggestion: bestAdaptation?.suggestion || this._getDefaultSuggestion(emotionId),
      adaptationType: bestAdaptation?.type,
      basedOn: totalOccurrences,
      successRate: Math.round(successRate * 100),
      patterns: patterns.map(p => ({
        trigger: p.trigger,
        occurrences: p.occurrences,
        successRate: p.positiveOutcomes / p.occurrences
      }))
    };
  }

  /**
   * 获取默认建议
   */
  _getDefaultSuggestion(emotionId) {
    const defaults = {
      joy: '继续保持这份积极心态，记录成功的经验',
      sadness: '给自己一些时间和空间，必要时寻求支持',
      anger: '尝试深呼吸，暂时离开触发环境',
      fear: '渐进式面对，从小步骤开始',
      anxiety: '使用放松技术，关注当下',
      acceptance: '欣赏自己的接纳态度',
      anticipation: '为期待的目标制定计划',
      interest: '深入探索感兴趣领域',
      default: '观察自己的情感反应，记录触发因素'
    };

    return defaults[emotionId] || defaults.default;
  }

  /**
   * 基于历史推荐响应（v2.0 新增）
   */
  getRecommendedResponse(trigger) {
    if (!trigger) {
      return { recommendation: null, reason: '缺少触发信息' };
    }

    const normalizedTrigger = this._normalizeTrigger(trigger);

    // 查找匹配的触发模式
    const matchingPatterns = [...this.patterns.values()]
      .filter(p => p.trigger &&
        this._normalizeTrigger(p.trigger) === normalizedTrigger);

    if (matchingPatterns.length === 0) {
      // 无匹配模式，基于PAD分析推荐
      const pad = this.calculatePADFromText(trigger);
      return {
        recommendation: this._recommendFromPAD(pad),
        reason: '基于PAD分析推荐',
        pad,
        confidence: 0.5
      };
    }

    // 找到最佳匹配模式
    let bestPattern = null;
    let maxSuccessRate = 0;

    for (const pattern of matchingPatterns) {
      const successRate = pattern.positiveOutcomes / pattern.occurrences;
      if (successRate > maxSuccessRate) {
        maxSuccessRate = successRate;
        bestPattern = pattern;
      }
    }

    // 基于最佳模式的成功响应生成推荐
    const successfulExperiences = this.growthHistory.filter(e =>
      e.trigger && this._normalizeTrigger(e.trigger) === normalizedTrigger &&
      e.outcome?.positive
    );

    if (successfulExperiences.length === 0) {
      return {
        recommendation: this._recommendFromPattern(bestPattern),
        reason: '基于模式推荐（无积极历史）',
        pattern: { emotion: bestPattern.emotion, successRate: maxSuccessRate },
        confidence: Math.min(0.7, maxSuccessRate)
      };
    }

    // 分析成功响应的共同特征
    const responseAnalysis = this._analyzeSuccessfulResponses(successfulExperiences);

    return {
      recommendation: responseAnalysis.recommendedAction,
      reason: `基于${successfulExperiences.length}次积极经验`,
      pattern: {
        emotion: bestPattern.emotion,
        successRate: maxSuccessRate,
        totalExperiences: matchingPatterns.reduce((sum, p) => sum + p.occurrences, 0)
      },
      successfulResponses: responseAnalysis.examples,
      confidence: Math.min(0.9, maxSuccessRate + 0.2)
    };
  }

  /**
   * 基于PAD推荐响应
   */
  _recommendFromPAD(pad) {
    const recommendations = [];

    if (pad.pleasure < -0.3) {
      if (pad.arousal > 0.3) {
        recommendations.push({ action: '情绪调节', detail: '高唤起负面情绪，需要冷静处理' });
      } else {
        recommendations.push({ action: '情绪支持', detail: '低愉悦度情绪，需要共情陪伴' });
      }
    } else if (pad.pleasure > 0.3) {
      recommendations.push({ action: '积极强化', detail: '积极情绪，可以探索更多相关话题' });
    }

    if (pad.dominance < -0.3) {
      recommendations.push({ action: '赋能支持', detail: '控制感低，需要帮助建立自主感' });
    }

    if (recommendations.length === 0) {
      recommendations.push({ action: '探索', detail: '中性情绪状态，可以深入了解' });
    }

    return recommendations;
  }

  /**
   * 基于模式推荐
   */
  _recommendFromPattern(pattern) {
    const lastAdaptation = pattern.adaptations[pattern.adaptations.length - 1];

    if (lastAdaptation) {
      return {
        action: lastAdaptation.type,
        suggestion: lastAdaptation.suggestion,
        type: 'adaptation'
      };
    }

    return {
      action: 'observe',
      suggestion: `继续观察${pattern.emotion}情感的触发模式`,
      type: 'observation'
    };
  }

  /**
   * 分析成功响应
   */
  _analyzeSuccessfulResponses(experiences) {
    if (experiences.length === 0) {
      return { recommendedAction: null, examples: [] };
    }

    // 提取响应模式
    const responses = experiences.map(e => e.response).filter(r => r);
    const responseCount = new Map();

    for (const r of responses) {
      responseCount.set(r, (responseCount.get(r) || 0) + 1);
    }

    // 最常见的响应
    let mostCommon = null;
    let maxCount = 0;
    for (const [r, count] of responseCount) {
      if (count > maxCount) {
        maxCount = count;
        mostCommon = r;
      }
    }

    // 提取共同特征
    const avgIntensity = experiences.reduce((sum, e) => sum + (e.intensity || 0.5), 0) / experiences.length;
    const avgPAD = {
      pleasure: experiences.reduce((sum, e) => sum + (e.pad?.pleasure || 0), 0) / experiences.length,
      arousal: experiences.reduce((sum, e) => sum + (e.pad?.arousal || 0), 0) / experiences.length,
      dominance: experiences.reduce((sum, e) => sum + (e.pad?.dominance || 0), 0) / experiences.length
    };

    return {
      recommendedAction: mostCommon || '保持当前响应方式',
      commonResponses: responses.slice(0, 3),
      examples: experiences.slice(0, 3).map(e => ({
        response: e.response,
        intensity: e.intensity,
        pad: e.pad
      })),
      avgIntensity: Math.round(avgIntensity * 100) / 100,
      avgPAD
    };
  }

  // ==================== 保留的v1.0方法 ====================

  /**
   * 获取学习模式
   */
  getPatterns(emotion = null) {
    const patterns = [...this.patterns.values()];

    if (emotion) {
      return patterns.filter(p => p.emotion === emotion);
    }

    return patterns.sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 获取需要适应的模式
   */
  getAdaptationNeeded() {
    return this.getPatterns()
      .filter(p => p.occurrences >= this._adaptiveParams.minSampleSize)
      .map(p => ({
        ...p,
        successRate: p.positiveOutcomes / p.occurrences
      }))
      .filter(p => p.successRate < this._adaptiveParams.successThreshold)
      .sort((a, b) => a.successRate - b.successRate);
  }

  /**
   * 获取成长摘要
   */
  getGrowthSummary() {
    const patterns = [...this.patterns.values()];

    const totalExperiences = this.growthHistory.length;
    const learnedExperiences = this.growthHistory.filter(e => e.learned).length;
    const uniquePatterns = patterns.length;
    const adaptationsNeeded = this.getAdaptationNeeded().length;
    const growthScore = this.getGrowthScore();

    // 计算情感分布
    const emotionDistribution = {};
    for (const exp of this.growthHistory) {
      emotionDistribution[exp.emotion] = (emotionDistribution[exp.emotion] || 0) + 1;
    }

    // 计算结果分布
    const outcomeDistribution = {
      positive: this.growthHistory.filter(e => e.outcome?.positive).length,
      negative: this.growthHistory.filter(e => !e.outcome?.positive).length
    };

    return {
      totalExperiences,
      learnedExperiences,
      uniquePatterns,
      adaptationsNeeded,
      emotionDistribution,
      outcomeDistribution,
      recentPatterns: patterns.slice(-5),
      growthScore: growthScore.score,
      growthLevel: growthScore.level,
      adaptiveParams: {
        optimalLearningRate: Math.round(this._adaptiveParams.optimalLearningRate * 100) / 100,
        successThreshold: Math.round(this._adaptiveParams.successThreshold * 100) / 100,
        valenceBias: Math.round(this._adaptiveParams.valenceBias * 100) / 100,
        arousalBias: Math.round(this._adaptiveParams.arousalBias * 100) / 100
      }
    };
  }

  /**
   * 获取历史
   */
  getHistory(limit = 20) {
    return this.growthHistory.slice(-limit);
  }

  /**
   * 重置学习记录
   */
  reset() {
    this.growthHistory = [];
    this.patterns = new Map();
    this._trajectoryData = [];
    this._adaptiveParams = {
      optimalLearningRate: 0.1,
      valenceBias: 0,
      arousalBias: 0,
      successThreshold: 0.4,
      minSampleSize: 3
    };
  }

  /**
   * 获取自适应参数状态
   */
  getAdaptiveParams() {
    return {
      ...this._adaptiveParams,
      optimalLearningRate: Math.round(this._adaptiveParams.optimalLearningRate * 100) / 100,
      valenceBias: Math.round(this._adaptiveParams.valenceBias * 100) / 100,
      arousalBias: Math.round(this._adaptiveParams.arousalBias * 100) / 100,
      successThreshold: Math.round(this._adaptiveParams.successThreshold * 100) / 100
    };
  }
}

module.exports = { EmotionalGrowth };
