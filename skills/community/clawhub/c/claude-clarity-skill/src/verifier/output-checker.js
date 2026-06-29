/**
 * 输出检查器 (Output Checker) v1.0.0
 *
 * 检查命令输出是否符合预期
 */

class OutputChecker {
  constructor() {
    this.checkers = [];
  }

  /**
   * 添加检查器
   */
  addChecker(checker) {
    this.checkers.push({
      id: `checker-${this.checkers.length}`,
      type: checker.type,
      pattern: checker.pattern,
      expected: checker.expected,
      validate: checker.validate
    });
  }

  /**
   * 检查输出
   */
  check(output, context = {}) {
    const results = [];

    for (const checker of this.checkers) {
      const result = this._runChecker(checker, output, context);
      results.push(result);
    }

    return {
      passed: results.every(r => r.passed),
      results,
      summary: {
        total: results.length,
        passed: results.filter(r => r.passed).length,
        failed: results.filter(r => !r.passed).length
      }
    };
  }

  /**
   * 运行检查器
   */
  _runChecker(checker, output, context) {
    switch (checker.type) {
      case 'contains':
        return this._checkContains(checker, output);

      case 'not_contains':
        return this._checkNotContains(checker, output);

      case 'matches':
        return this._checkMatches(checker, output);

      case 'equals':
        return this._checkEquals(checker, output);

      case 'length':
        return this._checkLength(checker, output);

      case 'json':
        return this._checkJson(checker, output);

      case 'custom':
        return this._runCustomChecker(checker, output, context);

      default:
        return { passed: false, message: `未知检查类型: ${checker.type}` };
    }
  }

  /**
   * 包含检查
   */
  _checkContains(checker, output) {
    const text = checker.expected;
    const caseSensitive = checker.caseSensitive !== false;
    const outputToCheck = caseSensitive ? output : output.toLowerCase();
    const textToCheck = caseSensitive ? text : text.toLowerCase();

    return {
      type: 'contains',
      passed: outputToCheck.includes(textToCheck),
      message: outputToCheck.includes(textToCheck)
        ? `包含 "${text}"`
        : `不包含 "${text}"`
    };
  }

  /**
   * 不包含检查
   */
  _checkNotContains(checker, output) {
    const text = checker.expected;
    const caseSensitive = checker.caseSensitive !== false;
    const outputToCheck = caseSensitive ? output : output.toLowerCase();
    const textToCheck = caseSensitive ? text : text.toLowerCase();

    return {
      type: 'not_contains',
      passed: !outputToCheck.includes(textToCheck),
      message: !outputToCheck.includes(textToCheck)
        ? `不包含 "${text}"`
        : `包含 "${text}"`
    };
  }

  /**
   * 正则匹配检查
   */
  _checkMatches(checker, output) {
    const regex = typeof checker.pattern === 'string'
      ? new RegExp(checker.pattern, 'i')
      : checker.pattern;

    const match = output.match(regex);

    return {
      type: 'matches',
      passed: match !== null,
      message: match !== null
        ? `匹配: ${match[0]}`
        : `不匹配: ${checker.pattern}`,
      match: match ? match[0] : null,
      matches: match
    };
  }

  /**
   * 相等检查
   */
  _checkEquals(checker, output) {
    const expected = checker.expected;
    const caseSensitive = checker.caseSensitive !== false;

    const matches = caseSensitive
      ? output === expected
      : output.toLowerCase().trim() === expected.toLowerCase().trim();

    return {
      type: 'equals',
      passed: matches,
      message: matches ? '内容相等' : '内容不等'
    };
  }

  /**
   * 长度检查
   */
  _checkLength(checker, output) {
    const length = output.trim().length;
    const { min, max } = checker.expected;

    const passed = (!min || length >= min) && (!max || length <= max);

    return {
      type: 'length',
      passed,
      message: passed
        ? `长度符合: ${length}`
        : `长度不符合: ${length}`,
      length
    };
  }

  /**
   * JSON 检查
   */
  _checkJson(checker, output) {
    try {
      const parsed = JSON.parse(output);

      if (checker.expected) {
        // 深度比较
        const matches = this._deepEqual(parsed, checker.expected);
        return {
          type: 'json',
          passed: matches,
          message: matches ? 'JSON 匹配' : 'JSON 不匹配',
          parsed
        };
      }

      return {
        type: 'json',
        passed: true,
        message: '有效的 JSON',
        parsed
      };
    } catch (error) {
      return {
        type: 'json',
        passed: false,
        message: '无效的 JSON',
        error: error.message
      };
    }
  }

  /**
   * 深度比较
   */
  _deepEqual(a, b) {
    if (a === b) return true;
    if (a === null || b === null) return false;
    if (typeof a !== typeof b) return false;

    if (typeof a === 'object') {
      const keysA = Object.keys(a);
      const keysB = Object.keys(b);

      if (keysA.length !== keysB.length) return false;

      for (const key of keysA) {
        if (!this._deepEqual(a[key], b[key])) return false;
      }

      return true;
    }

    return false;
  }

  /**
   * 自定义检查器
   */
  _runCustomChecker(checker, output, context) {
    try {
      const result = checker.validate(output, context);
      return {
        type: 'custom',
        passed: result.passed !== false,
        message: result.message || (result.passed ? '通过' : '失败'),
        details: result.details
      };
    } catch (error) {
      return {
        type: 'custom',
        passed: false,
        message: `检查器错误: ${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 预设检查器
   */
  static presets() {
    return {
      // 检查没有错误
      noErrors: {
        type: 'not_contains',
        expected: 'error',
        caseSensitive: false
      },

      // 检查包含成功信息
      hasSuccess: {
        type: 'contains',
        expected: 'success',
        caseSensitive: false
      },

      // 检查有效的 JSON
      validJson: {
        type: 'json'
      },

      // 检查非空
      notEmpty: {
        type: 'length',
        expected: { min: 1 }
      }
    };
  }
}

module.exports = { OutputChecker };
