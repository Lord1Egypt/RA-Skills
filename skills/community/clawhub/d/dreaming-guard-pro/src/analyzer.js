/**
 * Dreaming Guard Pro - Analyzer Module
 * 
 * 趋势分析器：根据监控数据预测增长趋势
 * 计算指标：增长率、预计满盘时间、风险等级
 * 检测异常模式：突然加速、周期性波动
 * 
 * 纯Node.js实现，零外部依赖
 */

// 风险等级定义
const RISK_LEVELS = {
  GREEN: 'green',    // 安全
  YELLOW: 'yellow',  // 警告
  RED: 'red'         // 危险
};

// 默认配置
const DEFAULT_CONFIG = {
  // 容量阈值（字节）
  thresholds: {
    green: 524288000,    // 500MB - 安全
    yellow: 1073741824,   // 1GB - 警告
    red: 2147483648       // 2GB - 危险
  },
  // 增长率阈值（KB/min）
  growthRate: {
    low: 10,      // <10KB/min 正常
    medium: 100,  // 10-100KB/min 中等
    high: 500     // >500KB/min 高速
  },
  // 预测参数
  prediction: {
    minSamples: 3,        // 最少样本数
    maxSamples: 60,       // 最大样本数
    confidenceThreshold: 0.7  // 置信度阈值
  },
  // 异常检测参数
  anomaly: {
    spikeMultiplier: 3,      // 突增倍数
    volatilityThreshold: 0.5  // 波动率阈值
  }
};

/**
 * Analyzer类 - 趋势分析器
 */
class Analyzer {
  constructor(options = {}) {
    this.config = this._mergeConfig(DEFAULT_CONFIG, options);
    
    // 绑定日志器
    this.logger = options.logger || {
      debug: (...args) => console.debug('[Analyzer]', ...args),
      info: (...args) => console.info('[Analyzer]', ...args),
      warn: (...args) => console.warn('[Analyzer]', ...args),
      error: (...args) => console.error('[Analyzer]', ...args)
    };
    
    // 分析缓存
    this.cache = {
      lastAnalysis: null,
      lastTimestamp: 0,
      cacheTTL: 30000  // 30秒缓存
    };
  }

  /**
   * 合并配置
   * @param {object} defaultConfig - 默认配置
   * @param {object} userConfig - 用户配置
   * @returns {object} 合并后的配置
   */
  _mergeConfig(defaultConfig, userConfig) {
    const result = { ...defaultConfig };
    for (const key of Object.keys(userConfig)) {
      if (userConfig[key] && typeof userConfig[key] === 'object' && !Array.isArray(userConfig[key])) {
        result[key] = this._mergeConfig(defaultConfig[key] || {}, userConfig[key]);
      } else if (userConfig[key] !== undefined) {
        result[key] = userConfig[key];
      }
    }
    return result;
  }

  /**
   * 分析历史数据
   * @param {array} historyData - 历史快照数组
   * @returns {object} 分析结果
   */
  analyze(historyData) {
    // 检查缓存
    const now = Date.now();
    if (this.cache.lastAnalysis && (now - this.cache.lastTimestamp) < this.cache.cacheTTL) {
      return this.cache.lastAnalysis;
    }

    // 验证输入
    if (!Array.isArray(historyData) || historyData.length < this.config.prediction.minSamples) {
      return {
        valid: false,
        reason: `Insufficient data: need ${this.config.prediction.minSamples}, got ${historyData?.length || 0}`,
        riskLevel: RISK_LEVELS.GREEN,
        recommendation: 'wait'
      };
    }

    // 提取有效数据
    const samples = historyData
      .filter(s => s && typeof s.totalSize === 'number')
      .slice(-this.config.prediction.maxSamples);

    if (samples.length < this.config.prediction.minSamples) {
      return {
        valid: false,
        reason: `Insufficient valid samples`,
        riskLevel: RISK_LEVELS.GREEN,
        recommendation: 'wait'
      };
    }

    // 计算基础指标
    const currentSize = samples[samples.length - 1].totalSize;
    const currentFiles = samples[samples.length - 1].totalFiles || 0;
    const growthRate = this._calculateGrowthRate(samples);
    const avgGrowthRate = this._calculateAverageGrowthRate(samples);

    // 计算预测
    const prediction = this.predict(growthRate, currentSize, this.config.thresholds.red);

    // 检测异常模式
    const anomalies = this._detectAnomalies(samples, avgGrowthRate);

    // 计算波动率
    const volatility = this._calculateVolatility(samples);

    // 确定风险等级
    const status = {
      currentSize,
      currentFiles,
      growthRate,
      avgGrowthRate,
      prediction,
      anomalies,
      volatility
    };
    const riskLevel = this.getRiskLevel(status);

    // 构建结果
    const result = {
      valid: true,
      timestamp: now,
      currentSize,
      currentFiles,
      growthRate,           // 当前增长率 (bytes/min)
      avgGrowthRate,        // 平均增长率 (bytes/min)
      growthRateKB: growthRate / 1024,  // KB/min
      prediction,
      anomalies,
      volatility,
      riskLevel,
      recommendation: this._getRecommendation(riskLevel, anomalies),
      samples: samples.length,
      timeSpan: samples.length > 1 
        ? (samples[samples.length - 1].timestamp - samples[0].timestamp) / 1000 
        : 0
    };

    // 更新缓存
    this.cache.lastAnalysis = result;
    this.cache.lastTimestamp = now;

    this.logger.debug('Analysis complete', { 
      riskLevel, 
      growthRateKB: result.growthRateKB.toFixed(2),
      timeToFull: prediction.timeToFull 
    });

    return result;
  }

  /**
   * 预测满盘时间
   * @param {number} growthRate - 增长率 (bytes/min)
   * @param {number} currentSize - 当前大小 (bytes)
   * @param {number} maxSize - 最大容量 (bytes)
   * @returns {object} 预测结果
   */
  predict(growthRate, currentSize, maxSize) {
    // 无增长或负增长
    if (growthRate <= 0) {
      return {
        timeToFull: Infinity,
        estimatedTime: null,
        confidence: 1.0,
        trend: 'stable',
        remainingCapacity: maxSize - currentSize,
        percentUsed: (currentSize / maxSize) * 100
      };
    }

    // 计算剩余空间
    const remainingCapacity = maxSize - currentSize;
    const percentUsed = (currentSize / maxSize) * 100;

    // 计算预计满盘时间（分钟）
    const timeToFullMinutes = remainingCapacity / growthRate;
    const timeToFull = timeToFullMinutes * 60 * 1000; // 转换为毫秒

    // 确定趋势
    let trend = 'growing';
    if (growthRate < 1024) {  // < 1KB/min
      trend = 'slow';
    } else if (growthRate > 1024 * 100) {  // > 100KB/min
      trend = 'rapid';
    }

    // 估算置信度（基于增长率稳定性）
    const confidence = Math.min(1.0, Math.max(0.1, 1 - (percentUsed / 200)));

    return {
      timeToFull,              // 毫秒
      timeToFullMinutes,       // 分钟
      timeToFullHours: timeToFullMinutes / 60,  // 小时
      timeToFullDays: timeToFullMinutes / 1440,  // 天
      estimatedTime: timeToFull < Infinity 
        ? new Date(Date.now() + timeToFull).toISOString() 
        : null,
      confidence,
      trend,
      remainingCapacity,
      percentUsed
    };
  }

  /**
   * 获取风险等级
   * @param {object} status - 状态对象
   * @returns {string} 风险等级 (green/yellow/red)
   */
  getRiskLevel(status) {
    const { currentSize, growthRate, anomalies, prediction } = status;

    // 检查当前大小阈值
    if (currentSize >= this.config.thresholds.red) {
      return RISK_LEVELS.RED;
    }
    if (currentSize >= this.config.thresholds.yellow) {
      return RISK_LEVELS.YELLOW;
    }

    // 检查增长率
    const growthRateKB = growthRate / 1024;
    if (growthRateKB >= this.config.growthRate.high) {
      return RISK_LEVELS.RED;
    }
    if (growthRateKB >= this.config.growthRate.medium) {
      return RISK_LEVELS.YELLOW;
    }

    // 检查预测
    if (prediction && prediction.timeToFullMinutes) {
      // 预计1小时内满盘
      if (prediction.timeToFullMinutes <= 60) {
        return RISK_LEVELS.RED;
      }
      // 预计6小时内满盘
      if (prediction.timeToFullMinutes <= 360) {
        return RISK_LEVELS.YELLOW;
      }
    }

    // 检查异常
    if (anomalies && anomalies.length > 0) {
      const hasCriticalAnomaly = anomalies.some(a => a.severity === 'critical');
      if (hasCriticalAnomaly) {
        return RISK_LEVELS.RED;
      }
      const hasWarningAnomaly = anomalies.some(a => a.severity === 'warning');
      if (hasWarningAnomaly) {
        return RISK_LEVELS.YELLOW;
      }
    }

    return RISK_LEVELS.GREEN;
  }

  /**
   * 计算增长率
   * @param {array} samples - 样本数组
   * @returns {number} 增长率 (bytes/min)
   */
  _calculateGrowthRate(samples) {
    if (samples.length < 2) return 0;

    const latest = samples[samples.length - 1];
    const previous = samples[samples.length - 2];
    const timeDiff = (latest.timestamp - previous.timestamp) / 1000; // 秒

    if (timeDiff <= 0) return 0;

    const sizeDiff = latest.totalSize - previous.totalSize;
    return (sizeDiff / timeDiff) * 60; // bytes/sec -> bytes/min
  }

  /**
   * 计算平均增长率
   * @param {array} samples - 样本数组
   * @returns {number} 平均增长率 (bytes/min)
   */
  _calculateAverageGrowthRate(samples) {
    if (samples.length < 2) return 0;

    let totalGrowth = 0;
    let totalTime = 0;

    for (let i = 1; i < samples.length; i++) {
      const timeDiff = (samples[i].timestamp - samples[i - 1].timestamp) / 1000;
      if (timeDiff > 0) {
        const sizeDiff = samples[i].totalSize - samples[i - 1].totalSize;
        totalGrowth += sizeDiff;
        totalTime += timeDiff;
      }
    }

    if (totalTime <= 0) return 0;
    return (totalGrowth / totalTime) * 60; // bytes/sec -> bytes/min
  }

  /**
   * 检测异常模式
   * @param {array} samples - 样本数组
   * @param {number} avgGrowthRate - 平均增长率
   * @returns {array} 异常列表
   */
  _detectAnomalies(samples, avgGrowthRate) {
    const anomalies = [];

    if (samples.length < 3) return anomalies;

    // 检测突然加速
    const recentSamples = samples.slice(-5);
    for (let i = 1; i < recentSamples.length; i++) {
      const timeDiff = (recentSamples[i].timestamp - recentSamples[i - 1].timestamp) / 1000;
      if (timeDiff > 0) {
        const sizeDiff = recentSamples[i].totalSize - recentSamples[i - 1].totalSize;
        const instantRate = (sizeDiff / timeDiff) * 60;

        // 检测突增（增长率超过平均的N倍）
        if (avgGrowthRate > 0 && instantRate > avgGrowthRate * this.config.anomaly.spikeMultiplier) {
          anomalies.push({
            type: 'spike',
            severity: instantRate > avgGrowthRate * 5 ? 'critical' : 'warning',
            timestamp: recentSamples[i].timestamp,
            rate: instantRate,
            avgRate: avgGrowthRate,
            multiplier: instantRate / avgGrowthRate
          });
        }
      }
    }

    // 检测周期性波动
    if (samples.length >= 10) {
      const volatility = this._calculateVolatility(samples);
      if (volatility > this.config.anomaly.volatilityThreshold) {
        // 检测周期性（简化：检查是否有重复模式）
        const pattern = this._detectPeriodicPattern(samples);
        if (pattern.detected) {
          anomalies.push({
            type: 'periodic',
            severity: 'info',
            period: pattern.period,
            amplitude: pattern.amplitude
          });
        }
      }
    }

    // 检测突然下降（可能的数据清理）
    for (let i = 1; i < samples.length; i++) {
      const sizeDiff = samples[i].totalSize - samples[i - 1].totalSize;
      if (sizeDiff < -1024 * 100) {  // 下降超过100KB
        anomalies.push({
          type: 'drop',
          severity: 'info',
          timestamp: samples[i].timestamp,
          amount: Math.abs(sizeDiff)
        });
      }
    }

    return anomalies;
  }

  /**
   * 计算波动率
   * @param {array} samples - 样本数组
   * @returns {number} 波动率 (0-1)
   */
  _calculateVolatility(samples) {
    if (samples.length < 3) return 0;

    // 计算增长率的标准差
    const rates = [];
    for (let i = 1; i < samples.length; i++) {
      const timeDiff = (samples[i].timestamp - samples[i - 1].timestamp) / 1000;
      if (timeDiff > 0) {
        const sizeDiff = samples[i].totalSize - samples[i - 1].totalSize;
        rates.push((sizeDiff / timeDiff) * 60);
      }
    }

    if (rates.length < 2) return 0;

    // 计算标准差
    const mean = rates.reduce((a, b) => a + b, 0) / rates.length;
    const variance = rates.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / rates.length;
    const stdDev = Math.sqrt(variance);

    // 归一化为波动率
    return Math.min(1, Math.max(0, stdDev / (Math.abs(mean) + 1)));
  }

  /**
   * 检测周期性模式
   * @param {array} samples - 样本数组
   * @returns {object} 模式检测结果
   */
  _detectPeriodicPattern(samples) {
    // 简化的周期性检测：检查是否有规律的高低交替
    if (samples.length < 10) {
      return { detected: false };
    }

    const values = samples.map(s => s.totalSize);
    const peaks = [];
    const valleys = [];

    for (let i = 1; i < values.length - 1; i++) {
      if (values[i] > values[i - 1] && values[i] > values[i + 1]) {
        peaks.push(i);
      } else if (values[i] < values[i - 1] && values[i] < values[i + 1]) {
        valleys.push(i);
      }
    }

    // 如果有足够的峰谷交替，认为有周期性
    if (peaks.length >= 2 && valleys.length >= 2) {
      const peakIntervals = [];
      for (let i = 1; i < peaks.length; i++) {
        const interval = samples[peaks[i]].timestamp - samples[peaks[i - 1]].timestamp;
        peakIntervals.push(interval);
      }

      const avgInterval = peakIntervals.reduce((a, b) => a + b, 0) / peakIntervals.length;
      
      // 计算振幅
      const peakValues = peaks.map(i => values[i]);
      const valleyValues = valleys.map(i => values[i]);
      const amplitude = (Math.max(...peakValues) - Math.min(...valleyValues)) / 2;

      return {
        detected: true,
        period: avgInterval / 1000 / 60, // 分钟
        amplitude
      };
    }

    return { detected: false };
  }

  /**
   * 获取建议
   * @param {string} riskLevel - 风险等级
   * @param {array} anomalies - 异常列表
   * @returns {string} 建议
   */
  _getRecommendation(riskLevel, anomalies) {
    switch (riskLevel) {
      case RISK_LEVELS.RED:
        if (anomalies.some(a => a.type === 'spike' && a.severity === 'critical')) {
          return 'emergency_action';
        }
        return 'immediate_action';
      case RISK_LEVELS.YELLOW:
        if (anomalies.some(a => a.type === 'spike')) {
          return 'monitor_closely';
        }
        return 'plan_action';
      case RISK_LEVELS.GREEN:
      default:
        return 'continue_monitoring';
    }
  }

  /**
   * 清除缓存
   */
  clearCache() {
    this.cache.lastAnalysis = null;
    this.cache.lastTimestamp = 0;
  }

  /**
   * 更新配置
   * @param {object} newConfig - 新配置
   */
  updateConfig(newConfig) {
    this.config = this._mergeConfig(this.config, newConfig);
    this.clearCache();
  }
}

// 导出
module.exports = Analyzer;
module.exports.RISK_LEVELS = RISK_LEVELS;