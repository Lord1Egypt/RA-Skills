/**
 * 错误处理工具 - API重试、降级处理、错误日志
 */

const logger = require('./logger');

// API重试配置
const RETRY_CONFIG = {
  maxRetries: 3,
  retryDelay: 1000, // 1秒
  timeout: 10000 // 10秒
};

/**
 * 带重试的fetch
 */
async function fetchWithRetry(url, options = {}, config = RETRY_CONFIG) {
  let lastError;

  for (let attempt = 1; attempt <= config.maxRetries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), config.timeout);

      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return response;

    } catch (error) {
      lastError = error;
      logger.hookWarn(logger.t('errorHandler.apiRetry', { attempt, max: config.maxRetries, error: error.message }), 'errorHandler');

      if (attempt < config.maxRetries) {
        await sleep(config.retryDelay * attempt);
      }
    }
  }

  // 所有重试都失败
  throw lastError;
}

/**
 * 睡眠函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 错误日志记录
 */
function logError(context, error, details = {}) {
  const errorLog = {
    timestamp: new Date().toISOString(),
    context,
    error: error.message || String(error),
    stack: error.stack,
    ...details
  };

  logger.error(logger.t('errorHandler.evaError') + `: ${errorLog.context}`, 'errorHandler', errorLog);

  // 可以扩展为保存到文件
  return errorLog;
}

/**
 * 带错误处理的API调用
 */
async function safeApiCall(apiFn, fallbackValue = null, context = 'API') {
  try {
    return await apiFn();
  } catch (error) {
    logError(context, error);
    return fallbackValue;
  }
}

/**
 * 降级处理 - 当主方案失败时使用备用方案
 */
async function withFallback(primaryFn, fallbackFn, context = 'operation') {
  try {
    return await primaryFn();
  } catch (error) {
    logger.hookWarn(logger.t('errorHandler.primaryFailed') + `: ${context}`, 'errorHandler');
    logError(context + '_fallback', error);

    try {
      return await fallbackFn();
    } catch (fallbackError) {
      logger.fail(logger.t('errorHandler.fallbackFailed') + `: ${context}`, 'errorHandler', fallbackError);
      logError(context + '_fallback_failed', fallbackError);
      return null;
    }
  }
}

/**
 * 缓存工具
 */
class SimpleCache {
  constructor(ttl = 3600000) { // 默认1小时
    this.cache = new Map();
    this.ttl = ttl;
  }

  set(key, value) {
    this.cache.set(key, {
      value,
      timestamp: Date.now()
    });
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }

    return item.value;
  }

  has(key) {
    return this.get(key) !== null;
  }

  clear() {
    this.cache.clear();
  }
}

// 全局缓存实例
const apiCache = new SimpleCache(3600000); // 1小时

module.exports = {
  fetchWithRetry,
  sleep,
  logError,
  safeApiCall,
  withFallback,
  SimpleCache,
  apiCache,
  RETRY_CONFIG
};
