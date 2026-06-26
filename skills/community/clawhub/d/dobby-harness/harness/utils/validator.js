/**
 * Validator - 验证工具
 * 
 * 提供结果质量验证、完整性检查、一致性验证
 */

/**
 * 验证结果类型
 */
export const ValidationResult = {
  VALID: 'valid',
  INVALID: 'invalid',
  WARNING: 'warning',
};

/**
 * 创建验证器
 * 
 * @param {Object} rules - 验证规则
 * @returns {Function} 验证函数
 * 
 * @example
 * const validator = createValidator({
 *   required: ['output', 'metadata'],
 *   minItems: 1,
 *   custom: [(result) => result.output !== null]
 * });
 */
export function createValidator(rules = {}) {
  const {
    required = [],
    minItems = 0,
    maxItems = Infinity,
    custom = [],
  } = rules;

  return function validate(result) {
    const issues = [];

    // 检查必需字段
    for (const field of required) {
      if (result[field] === undefined || result[field] === null) {
        issues.push({
          type: 'MISSING_FIELD',
          field,
          message: `Missing required field: ${field}`,
          severity: 'error',
        });
      }
    }

    // 检查数组长度
    if (Array.isArray(result.outputs)) {
      if (result.outputs.length < minItems) {
        issues.push({
          type: 'TOO_FEW_ITEMS',
          message: `Expected at least ${minItems} items, got ${result.outputs.length}`,
          severity: 'error',
        });
      }
      if (result.outputs.length > maxItems) {
        issues.push({
          type: 'TOO_MANY_ITEMS',
          message: `Expected at most ${maxItems} items, got ${result.outputs.length}`,
          severity: 'warning',
        });
      }
    }

    // 自定义验证
    for (const rule of custom) {
      const issue = rule(result);
      if (issue) {
        issues.push(issue);
      }
    }

    return {
      valid: issues.length === 0,
      issues,
      result,
    };
  };
}

/**
 * 验证完整性
 * 
 * @param {Object} aggregated - 聚合结果
 * @param {Object} expected - 期望结构
 * @returns {Object} 验证结果
 */
export function validateCompleteness(aggregated, expected = {}) {
  const issues = [];
  const { stats, outputs } = aggregated;

  // 检查成功率
  if (stats && stats.total > 0) {
    const successRate = stats.completed / stats.total;
    if (successRate < (expected.successRate || 0.8)) {
      issues.push({
        type: 'LOW_SUCCESS_RATE',
        message: `Success rate ${successRate.toFixed(2)} is below threshold ${expected.successRate || 0.8}`,
        severity: 'warning',
      });
    }
  }

  // 检查输出数量
  if (outputs && expected.minOutputs && outputs.length < expected.minOutputs) {
    issues.push({
      type: 'INSUFFICIENT_OUTPUTS',
      message: `Expected at least ${expected.minOutputs} outputs, got ${outputs.length}`,
      severity: 'error',
    });
  }

  // 检查错误数量
  if (aggregated.errors && aggregated.errors.length > (expected.maxErrors || 0)) {
    issues.push({
      type: 'TOO_MANY_ERRORS',
      message: `Too many errors: ${aggregated.errors.length}`,
      severity: 'error',
    });
  }

  return {
    complete: issues.length === 0,
    issues,
  };
}

/**
 * 验证一致性
 * 
 * @param {Array} outputs - 多个输出
 * @param {Function} comparator - 比较函数
 * @returns {Object} 验证结果
 */
export function validateConsistency(outputs, comparator = null) {
  const issues = [];

  if (!outputs || outputs.length < 2) {
    return { consistent: true, issues };
  }

  // 默认比较：检查类型一致性
  const compareFn = comparator || ((a, b) => typeof a === typeof b);

  for (let i = 1; i < outputs.length; i++) {
    if (!compareFn(outputs[0], outputs[i])) {
      issues.push({
        type: 'INCONSISTENT_OUTPUT',
        message: `Output ${i} is inconsistent with output 0`,
        severity: 'warning',
        index: i,
      });
    }
  }

  return {
    consistent: issues.length === 0,
    issues,
  };
}

/**
 * 验证质量评分
 * 
 * @param {Object} result - 执行结果
 * @param {Array} criteria - 评分标准
 * @returns {Object} 评分结果
 */
export function calculateQualityScore(result, criteria = []) {
  const scores = [];
  const details = [];

  for (const criterion of criteria) {
    const { name, weight = 1, check } = criterion;
    const passed = check(result);
    const score = passed ? weight : 0;
    
    scores.push(score);
    details.push({
      name,
      passed,
      weight,
      score,
    });
  }

  const totalWeight = criteria.reduce((sum, c) => sum + c.weight, 0);
  const totalScore = scores.reduce((sum, s) => sum + s, 0);
  const normalizedScore = totalWeight > 0 ? totalScore / totalWeight : 0;

  return {
    score: normalizedScore,
    maxScore: 1,
    details,
    passed: normalizedScore >= 0.8, // 80% 阈值
  };
}

/**
 * 常用验证器工厂
 */
export const validators = {
  /**
   * 验证至少有一个成功
   */
  atLeastOneSuccess: () => (result) => {
    if (result.stats?.completed > 0) return null;
    return {
      type: 'NO_SUCCESS',
      message: 'No successful results',
      severity: 'error',
    };
  },

  /**
   * 验证无错误
   */
  noErrors: () => (result) => {
    if (!result.errors || result.errors.length === 0) return null;
    return {
      type: 'HAS_ERRORS',
      message: `${result.errors.length} errors occurred`,
      severity: 'error',
    };
  },

  /**
   * 验证执行时间
   */
  withinTimeLimit: (maxMs) => (result) => {
    const duration = result.metadata?.totalTime || result.totalDuration;
    if (!duration || duration <= maxMs) return null;
    return {
      type: 'TIMEOUT',
      message: `Execution took ${duration}ms, exceeded limit ${maxMs}ms`,
      severity: 'warning',
    };
  },

  /**
   * 验证输出非空
   */
  outputNotEmpty: () => (result) => {
    const outputs = result.outputs || result.finalOutput;
    if (!outputs) {
      return {
        type: 'NO_OUTPUT',
        message: 'No output produced',
        severity: 'error',
      };
    }
    if (Array.isArray(outputs) && outputs.length === 0) {
      return {
        type: 'EMPTY_OUTPUT',
        message: 'Output array is empty',
        severity: 'warning',
      };
    }
    return null;
  },
};

export default {
  createValidator,
  validateCompleteness,
  validateConsistency,
  calculateQualityScore,
  validators,
};
