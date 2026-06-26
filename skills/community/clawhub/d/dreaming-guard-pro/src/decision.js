/**
 * Dreaming Guard Pro - Decision Module
 * 
 * 决策引擎：根据分析结果决定执行什么动作
 * 动作类型：no_action → notify → archive → compress → emergency
 * 决策规则可配置
 * 
 * 纯Node.js实现，零外部依赖
 */

// 动作类型定义（按优先级排序）
const ACTION_TYPES = {
  NO_ACTION: 'no_action',
  NOTIFY: 'notify',
  ARCHIVE: 'archive',
  COMPRESS: 'compress',
  EMERGENCY: 'emergency'
};

// 动作优先级
const ACTION_PRIORITY = {
  no_action: 0,
  notify: 1,
  archive: 2,
  compress: 3,
  emergency: 4
};

// 默认决策规则
const DEFAULT_RULES = {
  // 按风险等级的默认动作
  riskActions: {
    green: ACTION_TYPES.NO_ACTION,
    yellow: ACTION_TYPES.NOTIFY,
    red: ACTION_TYPES.ARCHIVE
  },
  // 容量阈值规则（字节）
  capacityThresholds: {
    // 容量使用率阈值
    archive: 0.7,     // 70%时考虑归档
    compress: 0.85,   // 85%时考虑压缩
    emergency: 0.95   // 95%时紧急处理
  },
  // 时间规则（分钟）
  timeThresholds: {
    // 预计满盘时间阈值
    archive: 360,     // 6小时内满盘
    compress: 60,      // 1小时内满盘
    emergency: 10      // 10分钟内满盘
  },
  // 增长率规则（KB/min）
  growthThresholds: {
    low: 10,
    medium: 100,
    high: 500,
    emergency: 1000
  },
  // 冷却规则
  cooldown: {
    enabled: true,
    durations: {
      no_action: 0,
      notify: 5 * 60 * 1000,      // 5分钟
      archive: 30 * 60 * 1000,     // 30分钟
      compress: 60 * 60 * 1000,    // 1小时
      emergency: 10 * 60 * 1000    // 10分钟
    }
  },
  // 联动规则
  chaining: {
    enabled: true,
    // 自动升级：如果同一风险等级持续，逐步升级动作
    autoEscalate: true,
    escalateAfter: 3,  // 3次检测后升级
    // 降级：风险降低后降级动作
    autoDowngrade: true
  }
};

/**
 * Decision类 - 决策引擎
 */
class Decision {
  constructor(options = {}) {
    this.config = this._mergeConfig(DEFAULT_RULES, options.rules || {});
    
    // 绑定日志器
    this.logger = options.logger || {
      debug: (...args) => console.debug('[Decision]', ...args),
      info: (...args) => console.info('[Decision]', ...args),
      warn: (...args) => console.warn('[Decision]', ...args),
      error: (...args) => console.error('[Decision]', ...args)
    };
    
    // 动作执行器（外部注入）
    this.actionHandlers = options.actionHandlers || {};
    
    // 决策历史
    this.history = [];
    this.maxHistory = 100;
    
    // 状态跟踪
    this.state = {
      lastAction: null,
      lastActionTime: 0,
      consecutiveCount: 0,
      lastRiskLevel: null,
      escalated: false
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
   * 根据分析结果做出决策
   * @param {object} analysis - 分析结果
   * @returns {object} 决策结果
   */
  decide(analysis) {
    // 验证分析结果
    if (!analysis || !analysis.valid) {
      return {
        action: ACTION_TYPES.NO_ACTION,
        reason: 'Invalid or insufficient analysis data',
        confidence: 0
      };
    }

    const { riskLevel, currentSize, growthRate, prediction, anomalies } = analysis;
    
    // 确定基础动作
    let baseAction = this.config.riskActions[riskLevel] || ACTION_TYPES.NO_ACTION;
    
    // 根据详细规则调整动作
    const adjustedAction = this._adjustAction(baseAction, analysis);
    
    // 检查冷却时间
    if (this._isInCooldown(adjustedAction)) {
      const cooldownAction = this._getCooldownAction(adjustedAction);
      return {
        action: cooldownAction,
        reason: `Action ${adjustedAction} in cooldown, using ${cooldownAction}`,
        cooldownRemaining: this._getCooldownRemaining(adjustedAction),
        confidence: 0.8
      };
    }
    
    // 检查是否需要升级
    const finalAction = this._checkEscalation(adjustedAction, riskLevel);
    
    // 更新状态
    this._updateState(finalAction, riskLevel);
    
    // 构建决策结果
    const result = {
      action: finalAction,
      riskLevel,
      reason: this._getReason(finalAction, analysis),
      confidence: this._calculateConfidence(analysis),
      currentSize,
      growthRateKB: growthRate / 1024,
      timeToFull: prediction?.timeToFullMinutes,
      anomalies: anomalies?.length || 0,
      recommendation: analysis.recommendation,
      actionPlan: this.getActionPlan(finalAction)
    };
    
    // 记录决策
    this._recordDecision(result);
    
    this.logger.debug('Decision made', { 
      action: finalAction, 
      riskLevel, 
      reason: result.reason 
    });
    
    return result;
  }

  /**
   * 根据详细规则调整动作
   * @param {string} baseAction - 基础动作
   * @param {object} analysis - 分析结果
   * @returns {string} 调整后的动作
   */
  _adjustAction(baseAction, analysis) {
    const { prediction, anomalies, growthRate } = analysis;
    let action = baseAction;
    
    // 检查预计满盘时间
    if (prediction && prediction.timeToFullMinutes) {
      const ttf = prediction.timeToFullMinutes;
      
      if (ttf <= this.config.timeThresholds.emergency) {
        action = ACTION_TYPES.EMERGENCY;
      } else if (ttf <= this.config.timeThresholds.compress) {
        action = this._selectHigherAction(action, ACTION_TYPES.COMPRESS);
      } else if (ttf <= this.config.timeThresholds.archive) {
        action = this._selectHigherAction(action, ACTION_TYPES.ARCHIVE);
      }
    }
    
    // 检查增长率
    const growthRateKB = growthRate / 1024;
    if (growthRateKB >= this.config.growthThresholds.emergency) {
      action = ACTION_TYPES.EMERGENCY;
    } else if (growthRateKB >= this.config.growthThresholds.high) {
      action = this._selectHigherAction(action, ACTION_TYPES.COMPRESS);
    }
    
    // 检查异常
    if (anomalies && anomalies.length > 0) {
      const criticalAnomalies = anomalies.filter(a => a.severity === 'critical');
      if (criticalAnomalies.length > 0) {
        action = this._selectHigherAction(action, ACTION_TYPES.EMERGENCY);
      }
    }
    
    return action;
  }

  /**
   * 选择优先级更高的动作
   * @param {string} action1 - 动作1
   * @param {string} action2 - 动作2
   * @returns {string} 优先级更高的动作
   */
  _selectHigherAction(action1, action2) {
    const priority1 = ACTION_PRIORITY[action1] || 0;
    const priority2 = ACTION_PRIORITY[action2] || 0;
    return priority1 >= priority2 ? action1 : action2;
  }

  /**
   * 检查是否在冷却期
   * @param {string} action - 动作
   * @returns {boolean} 是否在冷却期
   */
  _isInCooldown(action) {
    if (!this.config.cooldown.enabled) return false;
    
    const duration = this.config.cooldown.durations[action] || 0;
    if (duration === 0) return false;
    
    const elapsed = Date.now() - this.state.lastActionTime;
    return elapsed < duration;
  }

  /**
   * 获取冷却期的替代动作
   * @param {string} action - 原动作
   * @returns {string} 替代动作
   */
  _getCooldownAction(action) {
    // 降级到通知或无动作
    if (action === ACTION_TYPES.EMERGENCY) {
      return ACTION_TYPES.NOTIFY;
    }
    if (action === ACTION_TYPES.COMPRESS || action === ACTION_TYPES.ARCHIVE) {
      return ACTION_TYPES.NOTIFY;
    }
    return ACTION_TYPES.NO_ACTION;
  }

  /**
   * 获取剩余冷却时间
   * @param {string} action - 动作
   * @returns {number} 剩余时间（毫秒）
   */
  _getCooldownRemaining(action) {
    const duration = this.config.cooldown.durations[action] || 0;
    const elapsed = Date.now() - this.state.lastActionTime;
    return Math.max(0, duration - elapsed);
  }

  /**
   * 检查是否需要升级
   * @param {string} action - 当前动作
   * @param {string} riskLevel - 风险等级
   * @returns {string} 最终动作
   */
  _checkEscalation(action, riskLevel) {
    if (!this.config.chaining.enabled || !this.config.chaining.autoEscalate) {
      return action;
    }
    
    // 检查是否同一风险等级持续
    if (this.state.lastRiskLevel === riskLevel) {
      this.state.consecutiveCount++;
      
      // 达到升级阈值
      if (this.state.consecutiveCount >= this.config.chaining.escalateAfter) {
        // 升级到下一级动作
        const escalation = this._escalateAction(action);
        if (escalation !== action) {
          this.logger.info('Escalating action', { from: action, to: escalation });
          return escalation;
        }
      }
    } else {
      // 风险等级变化，重置计数
      this.state.consecutiveCount = 1;
      
      // 风险降低时降级
      if (this.config.chaining.autoDowngrade) {
        if (this._isRiskLower(riskLevel, this.state.lastRiskLevel)) {
          const downgrade = this._downgradeAction(action);
          if (downgrade !== action) {
            this.logger.info('Downgrading action', { from: action, to: downgrade });
            return downgrade;
          }
        }
      }
    }
    
    return action;
  }

  /**
   * 升级动作
   * @param {string} action - 当前动作
   * @returns {string} 升级后的动作
   */
  _escalateAction(action) {
    const escalationMap = {
      [ACTION_TYPES.NO_ACTION]: ACTION_TYPES.NOTIFY,
      [ACTION_TYPES.NOTIFY]: ACTION_TYPES.ARCHIVE,
      [ACTION_TYPES.ARCHIVE]: ACTION_TYPES.COMPRESS,
      [ACTION_TYPES.COMPRESS]: ACTION_TYPES.EMERGENCY,
      [ACTION_TYPES.EMERGENCY]: ACTION_TYPES.EMERGENCY
    };
    return escalationMap[action] || action;
  }

  /**
   * 降级动作
   * @param {string} action - 当前动作
   * @returns {string} 降级后的动作
   */
  _downgradeAction(action) {
    const downgradeMap = {
      [ACTION_TYPES.EMERGENCY]: ACTION_TYPES.COMPRESS,
      [ACTION_TYPES.COMPRESS]: ACTION_TYPES.ARCHIVE,
      [ACTION_TYPES.ARCHIVE]: ACTION_TYPES.NOTIFY,
      [ACTION_TYPES.NOTIFY]: ACTION_TYPES.NO_ACTION,
      [ACTION_TYPES.NO_ACTION]: ACTION_TYPES.NO_ACTION
    };
    return downgradeMap[action] || action;
  }

  /**
   * 比较风险等级是否更低
   * @param {string} level1 - 等级1
   * @param {string} level2 - 等级2
   * @returns {boolean} level1是否低于level2
   */
  _isRiskLower(level1, level2) {
    const riskOrder = { green: 0, yellow: 1, red: 2 };
    return (riskOrder[level1] || 0) < (riskOrder[level2] || 0);
  }

  /**
   * 更新状态
   * @param {string} action - 动作
   * @param {string} riskLevel - 风险等级
   */
  _updateState(action, riskLevel) {
    this.state.lastAction = action;
    this.state.lastActionTime = Date.now();
    this.state.lastRiskLevel = riskLevel;
  }

  /**
   * 获取决策原因
   * @param {string} action - 动作
   * @param {object} analysis - 分析结果
   * @returns {string} 原因
   */
  _getReason(action, analysis) {
    const { riskLevel, prediction, anomalies, growthRate } = analysis;
    const growthRateKB = growthRate / 1024;
    
    const reasons = [];
    
    if (riskLevel) {
      reasons.push(`risk:${riskLevel}`);
    }
    
    if (prediction && prediction.timeToFullMinutes) {
      if (prediction.timeToFullMinutes <= 60) {
        reasons.push(`full_in_${Math.round(prediction.timeToFullMinutes)}min`);
      } else {
        reasons.push(`full_in_${Math.round(prediction.timeToFullMinutes / 60)}h`);
      }
    }
    
    if (growthRateKB > 100) {
      reasons.push(`growth:${Math.round(growthRateKB)}KB/min`);
    }
    
    if (anomalies && anomalies.length > 0) {
      reasons.push(`anomalies:${anomalies.length}`);
    }
    
    return reasons.join(', ') || action;
  }

  /**
   * 计算决策置信度
   * @param {object} analysis - 分析结果
   * @returns {number} 置信度 (0-1)
   */
  _calculateConfidence(analysis) {
    const { prediction, samples, anomalies } = analysis;
    
    let confidence = 1.0;
    
    // 样本数影响置信度
    if (samples < 5) {
      confidence *= 0.6;
    } else if (samples < 10) {
      confidence *= 0.8;
    }
    
    // 预测置信度
    if (prediction && prediction.confidence !== undefined) {
      confidence *= prediction.confidence;
    }
    
    // 异常数量影响
    if (anomalies && anomalies.length > 2) {
      confidence *= 0.7;
    }
    
    return Math.max(0.1, Math.min(1.0, confidence));
  }

  /**
   * 获取动作执行计划
   * @param {string} action - 动作类型
   * @returns {object} 执行计划
   */
  getActionPlan(action) {
    const plans = {
      [ACTION_TYPES.NO_ACTION]: {
        type: ACTION_TYPES.NO_ACTION,
        description: 'No action required',
        steps: ['continue_monitoring'],
        estimatedTime: 0,
        impact: 'none'
      },
      [ACTION_TYPES.NOTIFY]: {
        type: ACTION_TYPES.NOTIFY,
        description: 'Send notification',
        steps: [
          'collect_status',
          'format_message',
          'send_alert'
        ],
        estimatedTime: 5000,  // 5秒
        impact: 'minimal'
      },
      [ACTION_TYPES.ARCHIVE]: {
        type: ACTION_TYPES.ARCHIVE,
        description: 'Archive old data',
        steps: [
          'identify_candidates',
          'select_archive_level',
          'create_archive',
          'verify_integrity',
          'cleanup_source'
        ],
        estimatedTime: 60000,  // 1分钟
        impact: 'moderate'
      },
      [ACTION_TYPES.COMPRESS]: {
        type: ACTION_TYPES.COMPRESS,
        description: 'Compress data to reduce size',
        steps: [
          'analyze_content',
          'select_strategy',
          'apply_compression',
          'verify_data',
          'update_index'
        ],
        estimatedTime: 120000,  // 2分钟
        impact: 'significant'
      },
      [ACTION_TYPES.EMERGENCY]: {
        type: ACTION_TYPES.EMERGENCY,
        description: 'Emergency action - immediate cleanup',
        steps: [
          'stop_non_essential',
          'emergency_archive',
          'emergency_compress',
          'clear_temp_files',
          'notify_administrator'
        ],
        estimatedTime: 30000,  // 30秒
        impact: 'critical'
      }
    };
    
    return plans[action] || plans[ACTION_TYPES.NO_ACTION];
  }

  /**
   * 执行动作
   * @param {string} action - 动作类型
   * @param {object} context - 执行上下文
   * @returns {Promise<object>} 执行结果
   */
  async executeAction(action, context = {}) {
    const handler = this.actionHandlers[action];
    
    if (!handler) {
      this.logger.warn(`No handler for action: ${action}`);
      return {
        success: false,
        action,
        error: `No handler registered for action: ${action}`
      };
    }
    
    this.logger.info('Executing action', { action, context });
    
    try {
      const result = await handler(context);
      
      // 记录执行结果
      this._recordDecision({
        action,
        executed: true,
        success: result?.success !== false,
        timestamp: Date.now(),
        context: context
      });
      
      return {
        success: true,
        action,
        result
      };
    } catch (error) {
      this.logger.error('Action execution failed', { action, error: error.message });
      
      this._recordDecision({
        action,
        executed: true,
        success: false,
        error: error.message,
        timestamp: Date.now()
      });
      
      return {
        success: false,
        action,
        error: error.message
      };
    }
  }

  /**
   * 注册动作处理器
   * @param {string} action - 动作类型
   * @param {function} handler - 处理函数
   */
  registerHandler(action, handler) {
    if (typeof handler !== 'function') {
      throw new Error('Handler must be a function');
    }
    this.actionHandlers[action] = handler;
    this.logger.debug('Handler registered', { action });
  }

  /**
   * 记录决策
   * @param {object} decision - 决策对象
   */
  _recordDecision(decision) {
    this.history.push({
      ...decision,
      timestamp: decision.timestamp || Date.now()
    });
    
    // 限制历史大小
    if (this.history.length > this.maxHistory) {
      this.history = this.history.slice(-this.maxHistory);
    }
  }

  /**
   * 获取决策历史
   * @param {number} limit - 限制数量
   * @returns {array} 决策历史
   */
  getHistory(limit = 20) {
    return this.history.slice(-limit);
  }

  /**
   * 获取上次决策
   * @returns {object|null} 上次决策
   */
  getLastDecision() {
    return this.history.length > 0 ? this.history[this.history.length - 1] : null;
  }

  /**
   * 重置状态
   */
  resetState() {
    this.state = {
      lastAction: null,
      lastActionTime: 0,
      consecutiveCount: 0,
      lastRiskLevel: null,
      escalated: false
    };
    this.logger.debug('State reset');
  }

  /**
   * 更新规则
   * @param {object} newRules - 新规则
   */
  updateRules(newRules) {
    this.config = this._mergeConfig(this.config, newRules);
    this.logger.debug('Rules updated');
  }
}

// 导出
module.exports = Decision;
module.exports.ACTION_TYPES = ACTION_TYPES;
module.exports.ACTION_PRIORITY = ACTION_PRIORITY;