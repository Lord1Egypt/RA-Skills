/**
 * 熔断器 (Circuit Breaker)
 * 防止级联故障
 */

const { createLogger } = require('./logger.cjs');
const logger = createLogger('circuit-breaker');

class CircuitBreaker {
  constructor(name, options = {}) {
    this.name = name;
    this.failureThreshold = options.failureThreshold || 5;
    this.successThreshold = options.successThreshold || 3;
    this.timeout = options.timeout || 60000; // 熔断后冷却时间
    
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.nextAttempt = Date.now();
  }

  async execute(fn, ...args) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error(`Circuit breaker '${this.name}' is OPEN`);
      }
      this.state = 'HALF_OPEN';
      logger.info(`[${this.name}] 熔断器进入 HALF_OPEN 状态`);
    }

    try {
      const result = await fn(...args);
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    
    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= this.successThreshold) {
        this.state = 'CLOSED';
        this.successCount = 0;
        logger.info(`[${this.name}] 熔断器关闭 (CLOSED)`);
      }
    }
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
      logger.warn(`[${this.name}] 熔断器打开 (OPEN)，${this.timeout}ms后尝试恢复`);
    }
  }

  getState() {
    return {
      name: this.name,
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount
    };
  }
}

// 熔断器管理器
class CircuitBreakerRegistry {
  constructor() {
    this.breakers = new Map();
  }

  get(name, options) {
    if (!this.breakers.has(name)) {
      this.breakers.set(name, new CircuitBreaker(name, options));
    }
    return this.breakers.get(name);
  }

  health() {
    const report = {};
    for (const [name, breaker] of this.breakers) {
      report[name] = breaker.getState();
    }
    return report;
  }
}

const registry = new CircuitBreakerRegistry();

module.exports = {
  CircuitBreaker,
  CircuitBreakerRegistry,
  registry,
  getCircuitBreaker: (name, options) => registry.get(name, options)
};
