const { spawn } = require('child_process');

/**
 * AutoThink Engine v2
 * 支持持久化思考模式的智能切换器
 */

class AutoThinkEngine {
  constructor() {
    // 会话状态存储 (sessionId -> thinkingLevel)
    this.sessionStates = new Map();
    
    // 全局默认（未设置时为 high）
    this.defaultThinking = 'high';
    
    // 复杂度分析阈值（仅在 autoAnalyze=true 时使用）
    this.thresholds = {
      shortLength: 50,
      mediumLength: 200,
      complexKeywords: [
        '分析', '设计', '架构', '复杂', '详细', '深入', '解释',
        '为什么', '如何', '比较', '评估', '推理', '证明', '算法',
        '优化', '重构', '总结', '策略', '方案', '实现', '调试',
        '原理', '机制', '流程', '步骤', '方法', '理论', '模型'
      ],
      techKeywords: [
        '代码', '程序', '系统', '数据库', 'API', '前端', '后端',
        '部署', '安全', '性能', '并发', '分布式', '微服务', '容器',
        'Kubernetes', 'Docker', '架构图', '流程图', '数据库设计',
        '缓存', '队列', '消息', '中间件', '网关', '负载均衡',
        'Redis', 'MySQL', 'PostgreSQL', 'MongoDB', 'Elasticsearch'
      ],
      questionMarkBonus: 1,
      codeBlockBonus: 2,
      multilineBonus: 1
    };
  }

  /**
   * 分析消息复杂度（可选功能）
   */
  analyzeComplexity(message) {
    const text = message.trim();
    let score = 0;

    // 1. 长度权重
    const length = text.length;
    if (length > 500) score += 3;
    else if (length > 200) score += 2;
    else if (length > 100) score += 1;
    else if (length < 30) score -= 1;

    // 2. 关键词检测
    const hasComplexKeyword = this.thresholds.complexKeywords.some(kw =>
      text.includes(kw)
    );
    const hasTechKeyword = this.thresholds.techKeywords.some(kw =>
      text.includes(kw)
    );

    if (hasComplexKeyword) score += 2;
    if (hasTechKeyword) score += 1;

    // 3. 问号数量
    const questionMarks = (text.match(/\?/g) || []).length;
    score += Math.min(questionMarks, this.thresholds.questionMarkBonus);

    // 4. 代码块检测
    const hasCodeBlock = text.includes('```') || text.includes('`');
    if (hasCodeBlock) score += this.thresholds.codeBlockBonus;

    // 5. 多行消息
    const lines = text.split('\n').length;
    if (lines > 5) score += this.thresholds.multilineBonus;

    let recommendedLevel;
    let reason;

    if (score >= 4) {
      recommendedLevel = 'high';
      reason = '高复杂度（长文本、关键词丰富、涉及技术细节）';
    } else if (score >= 2) {
      recommendedLevel = 'medium';
      reason = '中等复杂度（需要一定推理）';
    } else {
      recommendedLevel = 'low';
      reason = '低复杂度（简短、直接的问题）';
    }

    return { level: recommendedLevel, reason, score };
  }

  /**
   * 处理消息：返回处理建议
   * @param {string} message - 原始消息
   * @param {string} sessionId - 会话ID（用于状态记忆）
   * @param {boolean} autoAnalyze - 是否启用自动复杂度分析
   */
  processMessage(message, sessionId = null, autoAnalyze = false) {
    const cleanedMessage = this.cleanPrefix(message);
    const thinkingMode = this.detectThinkingMode(message, sessionId, autoAnalyze);

    // 如果检测到模式切换，更新会话状态
    if (this.isModeSwitch(message) && sessionId) {
      const newMode = this.extractModeFromPrefix(message);
      this.setSessionThinking(sessionId, newMode);
    }

    return {
      sessionId,
      thinkingLevel: thinkingMode,
      originalMessage: message,
      cleanedMessage,
      autoAnalyzed: autoAnalyze && !this.isModeSwitch(message)
    };
  }

  /**
   * 检测当前应该使用的 thinking 模式
   */
  detectThinkingMode(message, sessionId, autoAnalyze) {
    // 1. 检查是否有手动前缀覆盖
    if (this.isModeSwitch(message)) {
      return this.extractModeFromPrefix(message);
    }

    // 2. 检查会话是否已有持久设置
    if (sessionId && this.sessionStates.has(sessionId)) {
      return this.sessionStates.get(sessionId);
    }

    // 3. 自动分析（如果启用）
    if (autoAnalyze) {
      const analysis = this.analyzeComplexity(message);
      return analysis.level;
    }

    // 4. 默认使用 high
    return this.defaultThinking;
  }

  /**
   * 是否为模式切换指令
   */
  isModeSwitch(message) {
    const prefixes = ['-h ', '--high ', '-l ', '--low ', '-m ', '--medium '];
    return prefixes.some(prefix => message.startsWith(prefix));
  }

  /**
   * 从前缀提取模式
   */
  extractModeFromPrefix(message) {
    if (message.startsWith('-h ') || message.startsWith('--high ')) {
      return 'high';
    }
    if (message.startsWith('-l ') || message.startsWith('--low ')) {
      return 'low';
    }
    if (message.startsWith('-m ') || message.startsWith('--medium ')) {
      return 'medium';
    }
    return this.defaultThinking;
  }

  /**
   * 设置会话的 thinking 模式（持久化）
   */
  setSessionThinking(sessionId, level) {
    if (sessionId) {
      this.sessionStates.set(sessionId, level);
      if (process.env.AUTOTHINK_DEBUG) {
        console.log(`[AutoThink] Session ${sessionId.substring(0, 8)}... -> thinking=${level} (persisted)`);
      }
    }
  }

  /**
   * 获取会话当前模式
   */
  getSessionThinking(sessionId) {
    return sessionId ? this.sessionStates.get(sessionId) : null;
  }

  /**
   * 清除会话状态
   */
  clearSessionState(sessionId) {
    if (sessionId) {
      this.sessionStates.delete(sessionId);
    }
  }

  /**
   * 移除前缀标记
   */
  cleanPrefix(message) {
    const prefixes = ['-h ', '--high ', '-l ', '--low ', '-m ', '--medium '];
    for (const prefix of prefixes) {
      if (message.startsWith(prefix)) {
        return message.slice(prefix.length);
      }
    }
    return message;
  }

  /**
   * 设置全局默认模式
   */
  setDefaultThinking(level) {
    if (['low', 'medium', 'high'].includes(level)) {
      this.defaultThinking = level;
    }
  }

  /**
   * 获取当前会话状态摘要（调试用）
   */
  getStatus(sessionId) {
    return {
      sessionId: sessionId || 'none',
      currentThinking: sessionId ? this.sessionStates.get(sessionId) || this.defaultThinking : this.defaultThinking,
      defaultThinking: this.defaultThinking,
      autoAnalyze: false, // v2 关闭自动分析
      activeSessions: this.sessionStates.size
    };
  }
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { AutoThinkEngine };
}

// 独立测试
if (require.main === module) {
  const engine = new AutoThinkEngine();

  console.log('AutoThink v2 测试\n');
  console.log('=== 基础功能 ===');
  const tests = [
    { msg: '你好', sid: 'sess1' },
    { msg: '-h 帮我设计系统', sid: 'sess1' },
    { msg: '现在几点了', sid: 'sess1' }, // 应该沿用 high
    { msg: '-l 简单问题', sid: 'sess2' },
    { msg: '另一个问题', sid: 'sess2' }, // 应该沿用 low
    { msg: '复杂分析', sid: 'sess3' }, // 默认 high
  ];

  for (const { msg, sid } of tests) {
    const result = engine.processMessage(msg, sid, false);
    console.log(`[${sid}] "${msg}" -> ${result.thinkingLevel}`);
  }

  console.log('\n=== 状态摘要 ===');
  console.log(engine.getStatus('sess1'));
  console.log(engine.getStatus('sess2'));
  console.log(engine.getStatus('sess3'));
}
