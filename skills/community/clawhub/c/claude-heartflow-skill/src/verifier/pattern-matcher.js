/**
 * 模式匹配验证器 (Pattern Matcher) v1.0.0
 *
 * 使用模式匹配验证输出
 */

class PatternMatcher {
  constructor() {
    this.patterns = new Map();
    this._registerDefaultPatterns();
  }

  /**
   * 注册模式
   */
  registerPattern(name, pattern) {
    this.patterns.set(name, {
      name,
      ...pattern
    });
  }

  /**
   * 匹配输出
   */
  match(output, patternName) {
    const pattern = this.patterns.get(patternName);
    if (!pattern) {
      return { matched: false, error: `未知模式: ${patternName}` };
    }

    return this._matchWithPattern(output, pattern);
  }

  /**
   * 匹配所有注册的模式
   */
  matchAll(output) {
    const results = {};

    for (const [name, pattern] of this.patterns) {
      results[name] = this._matchWithPattern(output, pattern);
    }

    return results;
  }

  /**
   * 使用模式匹配
   */
  _matchWithPattern(output, pattern) {
    const matches = [];
    const patterns = pattern.patterns || [pattern.pattern];

    for (const p of patterns) {
      const regex = this._toRegex(p);
      if (!regex) continue;

      const match = output.match(regex);
      if (match) {
        matches.push({
          pattern: p,
          matched: match[0],
          groups: match.slice(1),
          index: match.index
        });
      }
    }

    const matched = pattern.requireAll
      ? matches.length === patterns.length
      : matches.length > 0;

    return {
      matched,
      pattern: pattern.name,
      matches,
      count: matches.length,
      message: matched
        ? `匹配 ${matches.length} 个模式`
        : `不匹配模式: ${pattern.name}`
    };
  }

  /**
   * 转换为正则
   */
  _toRegex(pattern) {
    if (pattern instanceof RegExp) {
      return pattern;
    }

    if (typeof pattern === 'string') {
      try {
        return new RegExp(pattern, 'gi');
      } catch {
        return null;
      }
    }

    return null;
  }

  /**
   * 注册默认模式
   */
  _registerDefaultPatterns() {
    // 错误模式
    this.registerPattern('errors', {
      name: '错误检测',
      patterns: [
        /\berror[s]?\b/i,
        /\bfail(ed|ure)?\b/i,
        /\bexception[s]?\b/i,
        /\btraceback\b/i
      ],
      requireAll: false
    });

    // 成功模式
    this.registerPattern('success', {
      name: '成功检测',
      patterns: [
        /\bsuccess(ful|fully)?\b/i,
        /\bcompleted?\b/i,
        /\bdone\b/i,
        /\bok\b/i
      ],
      requireAll: false
    });

    // Git 提交模式
    this.registerPattern('git_commit', {
      name: 'Git提交',
      patterns: [
        /\[([a-f0-9]+)\]\s+(.+)/,
        /commit\s+([a-f0-9]+)/i
      ]
    });

    // 文件路径模式
    this.registerPattern('file_paths', {
      name: '文件路径',
      patterns: [
        /\/[\w\-\/\.]+/g
      ]
    });

    // JSON 模式
    this.registerPattern('json', {
      name: 'JSON',
      patterns: [
        /\{[\s\S]*\}/
      ]
    });

    // URL 模式
    this.registerPattern('urls', {
      name: 'URL',
      patterns: [
        /https?:\/\/[^\s<>"]+/gi
      ]
    });

    // 行号模式
    this.registerPattern('line_numbers', {
      name: '行号',
      patterns: [
        /line\s*(\d+)/gi,
        /:(\d+):(\d+)/g
      ]
    });
  }

  /**
   * 提取匹配的内容
   */
  extract(output, patternName) {
    const result = this.match(output, patternName);
    if (!result.matched) return [];

    return result.matches.map(m => m.matched);
  }

  /**
   * 创建自定义匹配器
   */
  static create(patterns) {
    const matcher = new PatternMatcher();
    for (const [name, pattern] of Object.entries(patterns)) {
      matcher.registerPattern(name, pattern);
    }
    return matcher;
  }
}

module.exports = { PatternMatcher };
