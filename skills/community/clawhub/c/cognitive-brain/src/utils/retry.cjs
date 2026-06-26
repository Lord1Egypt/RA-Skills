/**
 * 重试工具
 * 带指数退避的重试机制
 */

/**
 * 执行函数带重试
 * @param {Function} fn - 要执行的函数
 * @param {Object} options - 配置选项
 * @returns {Promise<any>}
 */
async function withRetry(fn, options = {}) {
  const {
    maxRetries = 3,
    initialDelay = 100,
    maxDelay = 5000,
    backoffFactor = 2,
    retryableErrors = []
  } = options;

  let lastError;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // 最后一次尝试失败，抛出错误
      if (attempt === maxRetries) {
        throw error;
      }
      
      // 检查是否应该重试
      if (retryableErrors.length > 0) {
        const shouldRetry = retryableErrors.some(e => 
          error.message?.includes(e) || error.code === e
        );
        if (!shouldRetry) {
          throw error;
        }
      }
      
      // 计算延迟时间（指数退避）
      const delay = Math.min(
        initialDelay * Math.pow(backoffFactor, attempt),
        maxDelay
      );
      
      console.log(`[retry] 第 ${attempt + 1} 次尝试失败，${delay}ms 后重试...`);
      await sleep(delay);
    }
  }
  
  throw lastError;
}

/**
 * 睡眠函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 事务执行带重试
 */
async function transactionWithRetry(pool, fn, options = {}) {
  const { maxRetries = 3 } = options;
  
  return await withRetry(
    async () => {
      const { UnitOfWork } = require('../repositories/UnitOfWork');
      return await UnitOfWork.withTransaction(pool, fn);
    },
    {
      maxRetries,
      retryableErrors: [' deadlock ', 'lock timeout', 'connection terminated'],
      ...options
    }
  );
}

module.exports = {
  withRetry,
  sleep,
  transactionWithRetry
};
