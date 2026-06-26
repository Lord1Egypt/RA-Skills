/**
 * EventBus - 事件总线核心实现
 * 
 * 设计模式：事件驱动架构 (EDA)
 * 来源：2026-04-09 23:00 小时学习
 */

const EventEmitter = require('events');
const crypto = require('crypto');

/**
 * 事件 Schema 验证器
 */
class EventValidator {
  constructor(schemaRegistry = {}) {
    this.schemaRegistry = schemaRegistry;
  }

  registerSchema(eventName, schema) {
    this.schemaRegistry[eventName] = schema;
  }

  validate(eventName, payload) {
    const schema = this.schemaRegistry[eventName];
    if (!schema) return true; // 无 schema 则跳过验证

    // 简单类型检查
    for (const [key, type] of Object.entries(schema)) {
      if (payload[key] === undefined && schema.required?.includes(key)) {
        throw new Error(`Missing required field: ${key}`);
      }
      if (payload[key] !== undefined && typeof payload[key] !== type) {
        throw new Error(`Invalid type for ${key}: expected ${type}, got ${typeof payload[key]}`);
      }
    }
    return true;
  }
}

/**
 * 事件总线
 */
class EventBus extends EventEmitter {
  constructor(options = {}) {
    super();
    this.eventHistory = [];
    this.maxHistorySize = options.maxHistorySize || 1000;
    this.validator = new EventValidator();
    this.middlewareChain = [];
    this.subscribers = new Map();
  }

  /**
   * 注册事件 Schema
   */
  registerSchema(eventName, schema) {
    this.validator.registerSchema(eventName, schema);
  }

  /**
   * 注册中间件
   */
  use(middleware) {
    this.middlewareChain.push(middleware);
  }

  /**
   * 订阅事件
   */
  subscribe(eventName, handler, options = {}) {
    const subscriberId = crypto.randomBytes(8).toString('hex');
    const subscriber = {
      id: subscriberId,
      handler,
      priority: options.priority || 0,
      filter: options.filter || null,
      once: options.once || false
    };

    if (!this.subscribers.has(eventName)) {
      this.subscribers.set(eventName, []);
    }
    this.subscribers.get(eventName).push(subscriber);
    
    // 按优先级排序
    this.subscribers.get(eventName).sort((a, b) => b.priority - a.priority);

    return subscriberId;
  }

  /**
   * 取消订阅
   */
  unsubscribe(eventName, subscriberId) {
    if (!this.subscribers.has(eventName)) return false;
    
    const subscribers = this.subscribers.get(eventName);
    const index = subscribers.findIndex(s => s.id === subscriberId);
    
    if (index !== -1) {
      subscribers.splice(index, 1);
      return true;
    }
    return false;
  }

  /**
   * 发布事件
   */
  async publish(eventName, payload = {}, metadata = {}) {
    const eventId = crypto.randomBytes(16).toString('hex');
    const timestamp = Date.now();
    
    const event = {
      id: eventId,
      name: eventName,
      payload,
      metadata: {
        timestamp,
        correlationId: metadata.correlationId || eventId,
        causationId: metadata.causationId || null,
        retryCount: metadata.retryCount || 0
      },
      timestamp
    };

    // 验证事件
    try {
      this.validator.validate(eventName, payload);
    } catch (error) {
      throw new Error(`Event validation failed: ${error.message}`);
    }

    // 执行中间件链
    let shouldContinue = true;
    for (const middleware of this.middlewareChain) {
      try {
        const result = await middleware(event);
        if (result === false) {
          shouldContinue = false;
          break;
        }
      } catch (error) {
        console.error(`Middleware error: ${error.message}`);
      }
    }

    if (!shouldContinue) {
      return { eventId, status: 'skipped', reason: 'middleware_blocked' };
    }

    // 记录到历史
    this._addToHistory(event);

    // 通知订阅者
    const subscribers = this.subscribers.get(eventName) || [];
    const results = [];
    
    for (const subscriber of subscribers) {
      // 应用过滤器
      if (subscriber.filter && !subscriber.filter(payload)) {
        continue;
      }

      try {
        const result = await subscriber.handler(event);
        results.push({ subscriberId: subscriber.id, result, status: 'success' });
        
        // 处理 once 订阅
        if (subscriber.once) {
          this.unsubscribe(eventName, subscriber.id);
        }
      } catch (error) {
        results.push({ subscriberId: subscriber.id, error: error.message, status: 'failed' });
      }
    }

    // 发出原生事件（兼容 Node.js EventEmitter）
    super.emit(eventName, event);

    return {
      eventId,
      status: 'published',
      timestamp,
      subscriberResults: results
    };
  }

  /**
   * 添加到历史记录
   */
  _addToHistory(event) {
    this.eventHistory.push(event);
    if (this.eventHistory.length > this.maxHistorySize) {
      this.eventHistory.shift();
    }
  }

  /**
   * 获取事件历史
   */
  getHistory(limit = 100, eventName = null) {
    let history = this.eventHistory;
    if (eventName) {
      history = history.filter(e => e.name === eventName);
    }
    return history.slice(-limit);
  }

  /**
   * 清空历史
   */
  clearHistory() {
    this.eventHistory = [];
  }

  /**
   * 获取订阅者统计
   */
  getSubscriberStats() {
    const stats = {};
    for (const [eventName, subscribers] of this.subscribers.entries()) {
      stats[eventName] = subscribers.length;
    }
    return stats;
  }
}

module.exports = { EventBus, EventValidator };
