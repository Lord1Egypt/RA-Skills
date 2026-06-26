/**
 * errors.ts — 错误分类与处理
 *
 * 三类错误，不同策略：
 *   retryable: 网络/超时/DB忙 → 调用方可重试
 *   fatal:     代码错误/参数错误 → 立即返回错误
 *   degraded:  非核心模块失败 → 跳过继续主流程
 */

export type ErrorCategory = 'retryable' | 'fatal' | 'degraded'

const RETRYABLE_PATTERNS = /timeout|ETIMEDOUT|ECONNREFUSED|ECONNRESET|SQLITE_BUSY|rate.?limit|ENOTFOUND|socket hang up/i
const FATAL_PATTERNS = /TypeError|ReferenceError|SyntaxError|Cannot read|is not a function|is not defined|required|validation failed/i
const DEGRADABLE_CONTEXTS = ['body', 'persona', 'emotion', 'flow', 'epistemic', 'behavior', 'deep-understand', 'cin', 'avatar', 'absence', 'prospective', 'lorebook']

export function classifyError(err: any, context: string): ErrorCategory {
  const msg = err?.message || String(err)

  if (RETRYABLE_PATTERNS.test(msg)) return 'retryable'
  if (FATAL_PATTERNS.test(msg)) return 'fatal'
  if (DEGRADABLE_CONTEXTS.some(c => context.includes(c))) return 'degraded'

  return 'degraded'  // 未知错误默认降级（不崩溃）
}

/**
 * 处理错误并返回分类。调用方根据返回值决定重试/中止/降级。
 */
export function handleError(err: any, context: string): ErrorCategory {
  const category = classifyError(err, context)

  switch (category) {
    case 'retryable':
      console.warn(`[cc-soul][${context}] ⟳ retryable: ${err?.message || err}`)
      break
    case 'fatal':
      console.error(`[cc-soul][${context}] ✗ FATAL: ${err?.message || err}`)
      break
    case 'degraded':
      // 降级时不打 error，打 debug 级别（减少日志噪音）
      console.log(`[cc-soul][${context}] ↓ degraded: ${err?.message || err}`)
      break
  }

  return category
}
