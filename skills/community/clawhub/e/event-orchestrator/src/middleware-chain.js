/**
 * Middleware Chain - 中间件链实现
 * 
 * 设计模式：Middleware 链模式
 * 来源：2026-04-09 13:00 小时学习（DeerFlow 架构）
 */

/**
 * 日志中间件
 */
class LoggingMiddleware {
  constructor(options = {}) {
    this.logLevel = options.logLevel || 'info';
    this.logger = options.logger || console;
  }

  async handle(event) {
    const logEntry = {
      timestamp: new Date(event.timestamp).toISOString(),
      eventId: event.id,
      eventName: event.name,
      correlationId: event.metadata.correlationId
    };

    switch (this.logLevel) {
      case 'debug':
        this.logger.debug('[EVENT]', JSON.stringify(logEntry), 'Payload:', event.payload);
        break;
      case 'info':
        this.logger.info('[EVENT]', event.name, '→', event.id);
        break;
      case 'warn':
      case 'error':
        // 只记录警告和错误
        break;
    }

    return true; // 继续处理
  }
}

/**
 * 验证中间件
 */
class ValidationMiddleware {
  constructor(validatorFn) {
    this.validatorFn = validatorFn;
  }

  async handle(event) {
    try {
      const isValid = await this.validatorFn(event);
      if (!isValid) {
        return false; // 阻止事件处理
      }
      return true;
    } catch (error) {
      console.error('Validation error:', error.message);
      return false;
    }
  }
}

/**
 * 重试中间件
 */
class RetryMiddleware {
  constructor(options = {}) {
    this.maxRetries = options.maxRetries || 3;
    this.retryDelay = options.retryDelay || 1000;
  }

  async handle(event) {
    const { retryCount } = event.metadata;
    
    if (retryCount >= this.maxRetries) {
      console.warn(`Event ${event.name} exceeded max retries (${this.maxRetries})`);
      return false;
    }

    return true;
  }

  async retry(event, handler) {
    let lastError;
    
    for (let i = 0; i < this.maxRetries; i++) {
      try {
        return await handler(event);
      } catch (error) {
        lastError = error;
        console.warn(`Retry ${i + 1}/${this.maxRetries} for event ${event.name}`);
        await this._delay(this.retryDelay * (i + 1)); // 指数退避
      }
    }

    throw lastError;
  }

  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

/**
 * 速率限制中间件
 */
class RateLimitMiddleware {
  constructor(options = {}) {
    this.maxEvents = options.maxEvents || 100;
    this.windowMs = options.windowMs || 60000; // 1 分钟
    this.eventCounts = new Map();
  }

  async handle(event) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // 清理过期计数
    for (const [key, timestamps] of this.eventCounts.entries()) {
      const validTimestamps = timestamps.filter(t => t > windowStart);
      if (validTimestamps.length === 0) {
        this.eventCounts.delete(key);
      } else {
        this.eventCounts.set(key, validTimestamps);
      }
    }

    // 检查速率限制
    const currentCount = (this.eventCounts.get(event.name) || []).length;
    if (currentCount >= this.maxEvents) {
      console.warn(`Rate limit exceeded for event ${event.name}`);
      return false;
    }

    // 记录事件
    if (!this.eventCounts.has(event.name)) {
      this.eventCounts.set(event.name, []);
    }
    this.eventCounts.get(event.name).push(now);

    return true;
  }
}

/**
 * 中间件链执行器
 */
class MiddlewareChainExecutor {
  constructor() {
    this.middlewares = [];
  }

  use(middleware) {
    this.middlewares.push(middleware);
  }

  async execute(event) {
    for (const middleware of this.middlewares) {
      try {
        const result = typeof middleware.handle === 'function'
          ? await middleware.handle(event)
          : await middleware(event);
        
        if (result === false) {
          return { stopped: true, at: middleware.constructor.name };
        }
      } catch (error) {
        console.error(`Middleware ${middleware.constructor.name} error:`, error.message);
        // 继续执行下一个中间件
      }
    }
    return { stopped: false };
  }
}

module.exports = {
  LoggingMiddleware,
  ValidationMiddleware,
  RetryMiddleware,
  RateLimitMiddleware,
  MiddlewareChainExecutor
};
