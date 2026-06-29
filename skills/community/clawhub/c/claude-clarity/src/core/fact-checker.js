/**
 * FactChecker - 事实检查模块
 * 检测绝对化声明、数字准确性、来源可靠性
 *
 * @deprecated - 此模块计划在下一大版本中移除
 * 当前保留以向后兼容。所有调用方应迁移到外部验证。
 */

// 安全限制：单条输入最大字符数
const MAX_STATEMENT_LENGTH = 5000;
// 安全限制：checkNumbers 一次最多处理多少个数字匹配
const MAX_NUMBERS_CHECKED = 50;

class FactChecker {
  constructor() {
    this.stats = {
      totalChecked: 0,
      liesDetected: 0,
      confidenceScores: [],
    };
  }

  /**
   * 检查陈述是否在撒谎
   * @param {string} statement - 要检查的陈述
   * @returns {object} 检查结果
   */
  checkStatement(statement) {
    // 处理非字符串输入
    if (statement === null || statement === undefined) {
      return { checked: true, isLying: false, confidence: 1.0 };
    }

    if (typeof statement !== 'string') {
      statement = String(statement);
    }

    // 安全限制：超出 MAX_STATEMENT_LENGTH 的输入将被截断
    if (statement.length > MAX_STATEMENT_LENGTH) {
      statement = statement.slice(0, MAX_STATEMENT_LENGTH);
    }

    if (!statement) {
      return { checked: true, isLying: false, confidence: 1.0 };
    }

    this.stats.totalChecked++;

    // 检测绝对化声明
    const absolutePatterns = [
      /一定/g, /绝对/g, /肯定/g, /永远/g, /从不/g,
      /100%/g, /百分之百/g, /所有/g, /没有例外/g,
    ];

    let isLying = false;
    let confidence = 0.8;

    for (const pattern of absolutePatterns) {
      if (pattern.test(statement)) {
        isLying = true;
        confidence = 0.3;
        break;
      }
    }

    // 检测数字声明
    const numberPatterns = [
      /(\d+)%/g, /百分之(\d+)/g,
    ];

    for (const pattern of numberPatterns) {
      const matches = statement.match(pattern);
      if (matches) {
        // 数字声明需要验证，暂时标记为可能不准确
        confidence = Math.min(confidence, 0.6);
      }
    }

    if (isLying) {
      this.stats.liesDetected++;
    }

    this.stats.confidenceScores.push(confidence);

    return {
      checked: true,
      isLying,
      confidence,
      statement: statement.slice(0, 100),
    };
  }

  /**
   * 检查数字准确性
   * @param {string} text - 包含数字的文本
   * @returns {object} 检查结果
   */
  checkNumbers(text) {
    if (!text) return { checked: true, accurate: true };

    // 输入长度保护：避免恶意超大输入
    if (text.length > MAX_STATEMENT_LENGTH) {
      text = text.slice(0, MAX_STATEMENT_LENGTH);
    }

    const numberPattern = /(\d+(?:\.\d+)?)\s*(%|百分之|倍|万|亿)/g;
    const matches = text.match(numberPattern);

    // 防滥用保护：限制可处理的数字数量
    const numbersFound = matches || [];
    const safeNumbers = numbersFound.slice(0, MAX_NUMBERS_CHECKED);

    return {
      checked: true,
      accurate: safeNumbers.length === 0,
      numbersFound: safeNumbers,
      truncated: numbersFound.length > MAX_NUMBERS_CHECKED, // 提示是否被截断
    };
  }

  /**
   * 检查来源可靠性
   * @param {string} text - 包含来源声明的文本
   * @returns {object} 检查结果
   */
  checkSources(text) {
    if (!text) return { checked: true, hasSource: false };

    const sourcePatterns = [
      /根据.*研究/g, /研究表明/g, /数据显示/g,
      /专家说/g, /报告指出/g,
    ];

    let hasSource = false;
    for (const pattern of sourcePatterns) {
      if (pattern.test(text)) {
        hasSource = true;
        break;
      }
    }

    return {
      checked: true,
      hasSource,
      needsVerification: hasSource,
    };
  }

  /**
   * 获取统计信息
   * @returns {object} 统计信息
   */
  getStats() {
    const avgConfidence = this.stats.confidenceScores.length > 0
      ? this.stats.confidenceScores.reduce((a, b) => a + b, 0) / this.stats.confidenceScores.length
      : 0;

    return {
      type: 'fact-checker',
      active: true,
      totalChecked: this.stats.totalChecked,
      liesDetected: this.stats.liesDetected,
      averageConfidence: Math.round(avgConfidence * 100) / 100,
    };
  }
}

module.exports = FactChecker;
