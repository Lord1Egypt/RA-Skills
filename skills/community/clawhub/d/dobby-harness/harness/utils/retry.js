/**
 * Retry - 重试工具
 * 
 * 提供指数退避、可配置重试策略
 */

/**
 * 延迟函数
 */
export function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 重试配置
 */
export const RetryConfig = {
  FIXED: 'fixed',
  LINEAR: 'linear',
  EXPONENTIAL: 'exponential',
};

/**
 * 默认配置
 */
const DEFAULT_RETRY_CONFIG = {
  maxAttempts: 3,
  strategy: RetryConfig.EXPONENTIAL,
  initialDelay: 1000,    // 1 秒
  maxDelay: 30000,       // 30 秒
  retryableErrors: null, // null = 所有错误都重试
};

/**
 * 计算延迟时间
 */
function calculateDelay(attempt, config) {
  const { strategy, initialDelay, maxDelay } = config;

  let delayMs;

  switch (strategy) {
    case RetryConfig.FIXED:
      delayMs = initialDelay;
      break;

    case RetryConfig.LINEAR:
      delayMs = initialDelay * attempt;
      break;

    case RetryConfig.EXPONENTIAL:
    default:
      delayMs = initialDelay * Math.pow(2, attempt - 1);
      break;
  }

  return Math.min(delayMs, maxDelay);
}

/**
 * 判断错误是否可重试
 */
function isRetryable(error, retryableErrors) {
  if (!retryableErrors) return true; // 默认所有错误都可重试
  
  // 检查错误码
  if (error.code && retryableErrors.includes(error.code)) {
    return true;
  }
  
  // 检查错误消息
  if (error.message) {
    for (const retryable of retryableErrors) {
      if (error.message.includes(retryable)) {
        return true;
      }
    }
  }
  
  return false;
}

/**
 * 带重试执行函数
 * 
 * @param {Function} fn - 要执行的异步函数
 * @param {Object} config - 重试配置
 * @returns {Promise<any>} 函数执行结果
 * 
 * @example
 * const result = await withRetry(
 *   () => fetch('https://api.example.com/data'),
 *   { maxAttempts: 3, initialDelay: 1000 }
 * );
 */
export async function withRetry(fn, config = {}) {
  const retryConfig = { ...DEFAULT_RETRY_CONFIG, ...config };
  const { maxAttempts, retryableErrors } = retryConfig;

  let lastError;

  for (let attempt = 1; attempt <= maxAttempts + 1; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // 检查是否可重试
      const canRetry = attempt <= maxAttempts && isRetryable(error, retryableErrors);
      
      if (canRetry) {
        const delayMs = calculateDelay(attempt, retryConfig);
        console.log(`[Retry] Attempt ${attempt} failed: ${error.message}. Retrying in ${delayMs}ms...`);
        await delay(delayMs);
      } else {
        console.error(`[Retry] Attempt ${attempt} failed: ${error.message}. No more retries.`);
        break;
      }
    }
  }

  // 所有重试都失败了
  const error = new Error(`Failed after ${maxAttempts + 1} attempts: ${lastError.message}`);
  error.code = 'MAX_RETRIES_EXCEEDED';
  error.cause = lastError;
  throw error;
}

/**
 * 带超时和重试执行函数
 * 
 * @param {Function} fn - 要执行的异步函数
 * @param {Object} options - 配置
 * @returns {Promise<any>}
 * 
 * @example
 * const result = await withTimeoutAndRetry(
 *   () => slowOperation(),
 *   { timeout: 5000, maxAttempts: 3 }
 * );
 */
export async function withTimeoutAndRetry(fn, options = {}) {
  const { timeout = 30000, ...retryConfig } = options;

  return withRetry(async () => {
    return Promise.race([
      fn(),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), timeout)
      ),
    ]);
  }, retryConfig);
}

/**
 * 重试装饰器（用于类方法）
 * 
 * @param {Object} config - 重试配置
 * @returns {Function} 装饰器函数
 * 
 * @example
 * class ApiService {
 *   @retry({ maxAttempts: 3 })
 *   async fetchData() {
 *     // ...
 *   }
 * }
 */
export function retry(config = {}) {
  return function (target, propertyKey, descriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args) {
      return withRetry(() => originalMethod.apply(this, args), config);
    };

    return descriptor;
  };
}

export default withRetry;
