/**
 * 重规划触发器 (Replan Trigger) v1.0.0
 *
 * 决定何时需要重新规划
 */

class ReplanTrigger {
  constructor(options = {}) {
    this.thresholds = {
      maxRetries: options.maxRetries || 3,
      maxErrors: options.maxErrors || 5,
      errorRateThreshold: options.errorRateThreshold || 0.3,
      timeLimit: options.timeLimit || 300000, // 5分钟
      confidenceThreshold: options.confidenceThreshold || 0.5
    };

    this.counters = new Map();
  }

  /**
   * 判断是否需要重规划
   */
  shouldReplan(executionResult, currentPlan, context = {}) {
    // 任务完全失败
    if (executionResult.success === false) {
      return true;
    }

    // 错误数超过阈值
    const errorCount = executionResult.errors?.length || 0;
    if (errorCount >= this.thresholds.maxErrors) {
      return true;
    }

    // 步骤失败数超过阈值
    const failedSteps = executionResult.stepResults
      ? Object.values(executionResult.stepResults).filter(r => r.status === 'failed').length
      : 0;

    if (failedSteps >= this.thresholds.maxRetries) {
      return true;
    }

    // 错误率过高
    const totalSteps = currentPlan.steps?.length || 1;
    const errorRate = (errorCount + failedSteps) / totalSteps;
    if (errorRate > this.thresholds.errorRateThreshold) {
      return true;
    }

    // 执行超时
    if (executionResult.duration && executionResult.duration > this.thresholds.timeLimit) {
      return true;
    }

    // 置信度过低
    if (executionResult.confidence && executionResult.confidence < this.thresholds.confidenceThreshold) {
      return true;
    }

    // 检查特定错误模式
    if (this._hasCriticalErrors(executionResult)) {
      return true;
    }

    // 检查步骤依赖问题
    if (this._hasDependencyIssues(executionResult, currentPlan)) {
      return true;
    }

    return false;
  }

  /**
   * 是否有严重错误
   */
  _hasCriticalErrors(executionResult) {
    const errors = executionResult.errors || [];
    const criticalPatterns = [
      /FATAL|CRITICAL|panic/i,
      /segmentation fault|segfault/i,
      /out of memory|oom/i,
      /stack overflow/i,
      /deadlock/i
    ];

    return errors.some(error =>
      criticalPatterns.some(pattern => pattern.test(error))
    );
  }

  /**
   * 是否有依赖问题
   */
  _hasDependencyIssues(executionResult, currentPlan) {
    const errors = executionResult.errors || [];

    // 检查依赖错误
    const dependencyErrors = errors.filter(e =>
      /cannot find module|import error|dependency.*not found/i.test(e)
    );

    if (dependencyErrors.length > 0) {
      return true;
    }

    // 检查步骤顺序问题
    if (executionResult.stepResults) {
      for (const [stepId, result] of Object.entries(executionResult.stepResults)) {
        if (result.status === 'failed' && result.dependencyFailed) {
          return true;
        }
      }
    }

    return false;
  }

  /**
   * 获取重规划原因
   */
  getReplanReasons(executionResult, currentPlan, context = {}) {
    const reasons = [];

    if (executionResult.success === false) {
      reasons.push('任务执行完全失败');
    }

    const errorCount = executionResult.errors?.length || 0;
    if (errorCount >= this.thresholds.maxErrors) {
      reasons.push(`错误数 (${errorCount}) 超过阈值 (${this.thresholds.maxErrors})`);
    }

    const failedSteps = executionResult.stepResults
      ? Object.values(executionResult.stepResults).filter(r => r.status === 'failed').length
      : 0;

    if (failedSteps >= this.thresholds.maxRetries) {
      reasons.push(`失败步骤数 (${failedSteps}) 超过阈值 (${this.thresholds.maxRetries})`);
    }

    const totalSteps = currentPlan.steps?.length || 1;
    const errorRate = (errorCount + failedSteps) / totalSteps;
    if (errorRate > this.thresholds.errorRateThreshold) {
      reasons.push(`错误率 (${(errorRate * 100).toFixed(1)}%) 超过阈值 (${(this.thresholds.errorRateThreshold * 100).toFixed(1)}%)`);
    }

    if (executionResult.duration && executionResult.duration > this.thresholds.timeLimit) {
      reasons.push(`执行时间 (${executionResult.duration}ms) 超过限制 (${this.thresholds.timeLimit}ms)`);
    }

    if (this._hasCriticalErrors(executionResult)) {
      reasons.push('存在严重错误');
    }

    if (this._hasDependencyIssues(executionResult, currentPlan)) {
      reasons.push('存在依赖问题');
    }

    return reasons;
  }

  /**
   * 更新计数器
   */
  incrementCounter(key) {
    const current = this.counters.get(key) || 0;
    this.counters.set(key, current + 1);
    return current + 1;
  }

  /**
   * 重置计数器
   */
  resetCounter(key) {
    this.counters.delete(key);
  }

  /**
   * 重置所有计数器
   */
  resetAllCounters() {
    this.counters.clear();
  }

  /**
   * 获取计数器值
   */
  getCounter(key) {
    return this.counters.get(key) || 0;
  }

  /**
   * 更新阈值
   */
  updateThresholds(newThresholds) {
    this.thresholds = {
      ...this.thresholds,
      ...newThresholds
    };
  }
}

module.exports = { ReplanTrigger };
