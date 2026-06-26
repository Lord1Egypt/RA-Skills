#!/usr/bin/env node
/**
 * LLM Gateway v1.0 - 统一模型调用网关
 * 
 * 核心职责：熔断 + 限流 + 缓存 + 监控
 * 
 * 第一性原理：
 * - 所有 Agent 调用模型必须通过统一入口
 * - 熔断 = 防止雪崩，保护系统
 * - 限流 = 防止超额，控制成本
 * - 缓存 = 避免重复，节省 Token
 * 
 * 架构：
 * Agent → LLM Gateway → [缓存检查] → [限流检查] → [熔断器] → Model
 */

const { getPromptCache } = require('./prompt-cache');

/**
 * 内置熔断器（简化版）
 */
class SimpleCircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 60000;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.stats = { state: 'CLOSED', failures: 0, successes: 0 };
  }
  
  get isOpen() {
    if (this.state === 'OPEN') {
      // 检查是否可以转为 HALF_OPEN
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        this.state = 'HALF_OPEN';
        this.stats.state = 'HALF_OPEN';
        return false;
      }
      return true;
    }
    return false;
  }
  
  async execute(fn) {
    if (this.isOpen) {
      throw new Error('Circuit breaker is OPEN');
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
    this.stats.state = 'CLOSED';
    this.stats.successes++;
  }
  
  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    this.stats.failures++;
    
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.stats.state = 'OPEN';
    }
  }
}

class LLMGateway {
  constructor(options = {}) {
    // 缓存
    this.cache = getPromptCache(options.cache);
    
    // 熔断器（内置简化版）
    this.breaker = new SimpleCircuitBreaker({
      failureThreshold: options.failureThreshold || 5,
      resetTimeout: options.resetTimeout || 60000,
      ...options.breaker
    });
    
    // 限流配置
    this.rateLimit = {
      max: options.rateLimitMax || 100,        // 最大请求数
      window: options.rateLimitWindow || 60000, // 时间窗口（毫秒）
      ...options.rateLimit
    };
    this.requestCount = 0;
    this.lastReset = Date.now();
    
    // Token 预算
    this.tokenBudget = {
      daily: options.dailyTokenBudget || 1000000, // 每日预算
      used: 0,
      resetAt: this.getNextDayStart()
    };
    
    // 模型配置
    this.models = options.models || {
      'default': { provider: 'openai', model: 'gpt-4o-mini' },
      'planner': { provider: 'openai', model: 'gpt-4o-mini' },
      'executor': { provider: 'openai', model: 'gpt-4o-mini' },
      'reviewer': { provider: 'openai', model: 'gpt-4o-mini' }
    };
    
    // 统计
    this.stats = {
      totalCalls: 0,
      cacheHits: 0,
      cacheMisses: 0,
      rateLimitHits: 0,
      breakerTrips: 0,
      budgetExceeded: 0,
      totalTokens: 0
    };
    
    // 调用日志
    this.callLog = [];
    this.maxLogSize = options.maxLogSize || 1000;
  }

  /**
   * 统一调用入口（核心方法）
   * @param {string} prompt - 提示词
   * @param {object} options - 选项
   * @returns {Promise<object>} 响应
   */
  async call(prompt, options = {}) {
    const startTime = Date.now();
    const modelType = options.modelType || 'default';
    const modelConfig = this.models[modelType] || this.models.default;
    
    // 记录调用
    this.stats.totalCalls++;
    
    try {
      // 1. 检查 Token 预算
      if (!this.checkBudget(options.estimatedTokens || 0)) {
        this.stats.budgetExceeded++;
        throw new Error('Token budget exceeded');
      }
      
      // 2. 检查缓存
      if (!options.skipCache) {
        const cached = this.cache.get(prompt, { model: modelConfig.model });
        if (cached !== null) {
          this.stats.cacheHits++;
          this.logCall(prompt, 'cache_hit', 0, startTime);
          console.log(`[LLMGateway] 缓存命中 (model: ${modelConfig.model})`);
          return cached;
        }
      }
      
      this.stats.cacheMisses++;
      
      // 3. 检查限流
      if (!this.checkRateLimit()) {
        this.stats.rateLimitHits++;
        throw new Error('Rate limit exceeded');
      }
      
      // 4. 通过熔断器调用
      const result = await this.breaker.execute(async () => {
        return await this.rawCall(prompt, { ...options, ...modelConfig });
      });
      
      // 5. 缓存结果
      if (!options.skipCache && result) {
        this.cache.set(prompt, result, { model: modelConfig.model });
      }
      
      // 6. 更新统计
      const tokens = this.estimateTokens(prompt, result);
      this.stats.totalTokens += tokens;
      this.tokenBudget.used += tokens;
      
      this.logCall(prompt, 'success', tokens, startTime);
      
      return result;
      
    } catch (error) {
      this.logCall(prompt, 'error', 0, startTime, error.message);
      
      if (error.message.includes('Circuit breaker')) {
        this.stats.breakerTrips++;
      }
      
      throw error;
    }
  }

  /**
   * 检查 Token 预算
   */
  checkBudget(estimatedTokens) {
    // 检查是否需要重置
    if (Date.now() > this.tokenBudget.resetAt) {
      this.tokenBudget.used = 0;
      this.tokenBudget.resetAt = this.getNextDayStart();
    }
    
    return this.tokenBudget.used + estimatedTokens <= this.tokenBudget.daily;
  }

  /**
   * 检查限流
   */
  checkRateLimit() {
    const now = Date.now();
    
    // 重置计数器
    if (now - this.lastReset > this.rateLimit.window) {
      this.requestCount = 0;
      this.lastReset = now;
    }
    
    return ++this.requestCount <= this.rateLimit.max;
  }

  /**
   * 原始调用（由具体实现覆盖）
   */
  async rawCall(prompt, options) {
    // 默认实现：返回占位符
    // 实际使用时应覆盖此方法
    console.warn('[LLMGateway] rawCall 未实现，请覆盖此方法');
    return {
      content: `[LLM Gateway] 收到请求，请实现 rawCall 方法`,
      model: options.model,
      provider: options.provider
    };
  }

  /**
   * 估算 Token 数量
   */
  estimateTokens(prompt, result) {
    // 简单估算：字符数 / 4（中英文混合平均）
    const promptTokens = Math.ceil(prompt.length / 4);
    const resultTokens = result ? Math.ceil(JSON.stringify(result).length / 4) : 0;
    return promptTokens + resultTokens;
  }

  /**
   * 获取下一个零点时间
   */
  getNextDayStart() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0);
    return tomorrow.getTime();
  }

  /**
   * 记录调用日志
   */
  logCall(prompt, status, tokens, startTime, error = null) {
    const entry = {
      timestamp: Date.now(),
      duration: Date.now() - startTime,
      promptPreview: prompt.substring(0, 100),
      status,
      tokens,
      error
    };
    
    this.callLog.push(entry);
    
    // 限制日志大小
    if (this.callLog.length > this.maxLogSize) {
      this.callLog.shift();
    }
  }

  /**
   * 批量调用
   */
  async batch(prompts, options = {}) {
    const results = [];
    
    for (const prompt of prompts) {
      try {
        const result = await this.call(prompt, options);
        results.push(result);
      } catch (error) {
        results.push({ error: error.message });
      }
    }
    
    return results;
  }

  /**
   * 流式调用（需要实现）
   */
  async stream(prompt, options = {}, onChunk) {
    // 默认实现：不支持流式
    const result = await this.call(prompt, options);
    onChunk(result);
    return result;
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const total = this.stats.cacheHits + this.stats.cacheMisses;
    const cacheHitRate = total > 0 
      ? (this.stats.cacheHits / total * 100).toFixed(1) 
      : 0;
    
    return {
      ...this.stats,
      cacheHitRate: cacheHitRate + '%',
      budgetUsage: (this.tokenBudget.used / this.tokenBudget.daily * 100).toFixed(1) + '%',
      budgetRemaining: this.tokenBudget.daily - this.tokenBudget.used,
      breakerStatus: this.breaker.stats?.state || 'unknown'
    };
  }

  /**
   * 获取调用日志
   */
  getCallLog(limit = 100) {
    return this.callLog.slice(-limit);
  }

  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalCalls: 0,
      cacheHits: 0,
      cacheMisses: 0,
      rateLimitHits: 0,
      breakerTrips: 0,
      budgetExceeded: 0,
      totalTokens: 0
    };
    this.callLog = [];
  }

  /**
   * 注册模型
   */
  registerModel(type, config) {
    this.models[type] = config;
    console.log(`[LLMGateway] 注册模型: ${type} → ${config.provider}/${config.model}`);
  }

  /**
   * 设置 Token 预算
   */
  setBudget(daily) {
    this.tokenBudget.daily = daily;
    console.log(`[LLMGateway] 设置预算: ${daily} tokens/天`);
  }

  /**
   * 健康检查
   */
  healthCheck() {
    const stats = this.getStats();
    
    const issues = [];
    
    if (parseFloat(stats.cacheHitRate) < 20) {
      issues.push('缓存命中率过低（<20%）');
    }
    
    if (this.breaker.isOpen) {
      issues.push('熔断器已打开');
    }
    
    if (parseFloat(stats.budgetUsage) > 80) {
      issues.push('Token 预算使用超过 80%');
    }
    
    return {
      healthy: issues.length === 0,
      issues,
      stats
    };
  }
}

// 单例导出
let instance = null;

function getLLMGateway(options = {}) {
  if (!instance) {
    instance = new LLMGateway(options);
  }
  return instance;
}

module.exports = {
  LLMGateway,
  getLLMGateway
};