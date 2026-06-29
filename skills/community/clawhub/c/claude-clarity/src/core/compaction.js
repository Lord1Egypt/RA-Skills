/**
 * AutoCompactionEngine - 上下文窗口自动压缩引擎
 * 来源: mark-heartflow-skill v2.0.37 → claude-clarity 吸收
 *
 * 功能:
 * 1. 中文 Token 估算 (1 token ≈ 1.5 汉字, 0.5 英文词)
 * 2. 自动压缩触发 (80% 预警, 90% 强制压缩)
 * 3. 压缩策略: trim(保留最新N条) + summarize(伪摘要)
 * 4. 压缩统计 (效率趋势、节省token、连续压缩计数)
 */

class SimpleTokenizer {
  constructor() {
    this.cnStopWords = new Set([
      '的', '了', '是', '在', '和', '与', '对', '为', '以', '上', '中', '下', '将', '把', '被',
      '啊', '呢', '吧', '吗', '呀', '哦', '嗯', '这个', '那个', '什么', '怎么',
    ]);
  }

  /** 估算文本的 token 数量 */
  estimate(text) {
    if (!text || typeof text !== 'string') return 0;
    let tokens = 0;
    const cnChars = (text.match(/[一-龥]/g) || []).length;
    tokens += cnChars * 1.5;
    const enWords = (text.match(/[a-zA-Z]+/g) || []).length;
    tokens += enWords * 0.5;
    const otherChars = text.replace(/[一-龥a-zA-Z\s]/g, '').length;
    tokens += otherChars * 0.5;
    return Math.ceil(tokens);
  }

  /** 估算消息数组的总 token */
  estimateMessages(messages) {
    if (!Array.isArray(messages)) return 0;
    return messages.reduce((sum, msg) => {
      const content = typeof msg === 'string' ? msg : (msg.content || '');
      const role = msg.role || '';
      return sum + this.estimate(role) + this.estimate(content);
    }, 0);
  }
}

class TrimStrategy {
  constructor(options = {}) {
    this.keepLatest = options.keepLatest || 10;
    this.keepSystem = options.keepSystem !== false;
  }

  compress(messages, maxTokens, tokenizer) {
    if (!messages || messages.length === 0) {
      return { compacted: [], summary: '[无历史消息]', dropped: 0 };
    }
    const systemMsgs = this.keepSystem ? messages.filter(m => m.role === 'system') : [];
    const nonSystemMsgs = messages.filter(m => m.role !== 'system');
    const dropped = Math.max(0, nonSystemMsgs.length - this.keepLatest);

    let compacted = [...systemMsgs];
    let accumulatedTokens = tokenizer.estimateMessages(systemMsgs);

    for (let i = nonSystemMsgs.length - 1; i >= 0 && compacted.length < this.keepLatest + systemMsgs.length; i--) {
      const msg = nonSystemMsgs[i];
      const msgTokens = tokenizer.estimate(msg.content || msg);
      if (accumulatedTokens + msgTokens <= maxTokens) {
        compacted.push(msg);
        accumulatedTokens += msgTokens;
      } else {
        break;
      }
    }

    const summary = dropped > 0
      ? `[已压缩 ${dropped} 条早期消息，保留最近 ${compacted.length - systemMsgs.length} 条]`
      : '[无压缩]';

    return { compacted, summary, dropped };
  }
}

class SummarizeStrategy {
  constructor(options = {}) {
    this.maxSummaryLength = options.maxSummaryLength || 200;
    this.keepRecent = options.keepRecent || 5;
  }

  compress(messages, maxTokens, tokenizer) {
    if (!messages || messages.length === 0) {
      return { compacted: [], summary: '[无历史消息]', dropped: 0 };
    }

    const systemMsgs = messages.filter(m => m.role === 'system');
    const nonSystemMsgs = messages.filter(m => m.role !== 'system');
    const recentMsgs = nonSystemMsgs.slice(-this.keepRecent);
    const oldMsgs = nonSystemMsgs.slice(0, -this.keepRecent);
    const dropped = oldMsgs.length;

    const summary = this._generatePseudoSummary(oldMsgs);
    const summaryMsg = {
      role: 'system',
      content: `[历史摘要] ${summary}\n\n注: 详细内容已压缩，此摘要仅保留关键信息。`,
      isSummary: true,
      originalCount: oldMsgs.length,
    };

    let compacted = [...systemMsgs, summaryMsg, ...recentMsgs];
    let tokenCount = tokenizer.estimateMessages(compacted);

    if (tokenCount > maxTokens) {
      const trimmer = new TrimStrategy({ keepLatest: 3, keepSystem: true });
      return trimmer.compress(compacted, maxTokens, tokenizer);
    }

    return { compacted, summary, dropped };
  }

  _generatePseudoSummary(messages) {
    if (!messages || messages.length === 0) return '[无历史]';
    const topics = [];
    messages.forEach(msg => {
      const content = typeof msg === 'string' ? msg : (msg.content || '');
      const questions = content.match(/[?？][^?？]*$/gm);
      if (questions) {
        questions.forEach(q => {
          const clean = q.replace(/[?？]/g, '').trim();
          if (clean.length > 2 && clean.length < 50) topics.push(clean);
        });
      }
    });
    return topics.length > 0
      ? `[摘要] 讨论了 ${topics.slice(0, 3).join('、')} 等主题。`
      : '[摘要] 一般性讨论。';
  }
}

class AutoCompactionEngine {
  constructor(options = {}) {
    this.tokenizer = new SimpleTokenizer();
    this.config = {
      warningThreshold: options.warningThreshold || 0.80,
      compactionThreshold: options.compactionThreshold || 0.90,
      maxContextTokens: options.maxContextTokens || 100000,
      strategy: options.strategy || 'trim',
      autoCompact: options.autoCompact !== false,
      onCompactionStart: options.onCompactionStart || null,
      onCompactionEnd: options.onCompactionEnd || null,
      onWarning: options.onWarning || null,
      ...options,
    };
    this.stats = {
      totalRuns: 0, warnings: 0, compactions: 0, totalDropped: 0,
      lastCompaction: null, strategyUsed: null,
      compressionRatios: [], compressionEfficiency: [], totalSavedTokens: 0,
      maxConsecutiveCompactions: 0,
    };
    this._compactionHistory = [];
    this._consecutiveCompactions = 0;
  }

  /** 检查是否需要压缩 */
  check(messages) {
    const tokenCount = this.tokenizer.estimateMessages(messages);
    const ratio = tokenCount / this.config.maxContextTokens;
    let level = 'ok';
    if (ratio >= this.config.compactionThreshold) level = 'critical';
    else if (ratio >= this.config.warningThreshold) level = 'warning';

    return {
      needsCompaction: level === 'critical',
      level, tokenCount, ratio,
      maxTokens: this.config.maxContextTokens,
    };
  }

  /** 执行压缩 */
  compact(messages, options = {}) {
    const strategy = options.strategy || this.config.strategy;
    const maxTokens = options.maxTokens || (this.config.maxContextTokens * this.config.compactionThreshold);

    if (this.config.onCompactionStart) {
      try {
        this.config.onCompactionStart({
          messageCount: messages.length,
          tokenCount: this.tokenizer.estimateMessages(messages),
          strategy,
        });
      } catch (e) { /* 忽略回调错误 */ }
    }

    const startTime = Date.now();
    let result;
    if (strategy === 'summarize') {
      const summarizer = new SummarizeStrategy(options.summarizeOptions);
      result = summarizer.compress(messages, maxTokens, this.tokenizer);
    } else {
      const trimmer = new TrimStrategy(options.trimOptions);
      result = trimmer.compress(messages, maxTokens, this.tokenizer);
    }

    const duration = Date.now() - startTime;
    const originalTokenCount = this.tokenizer.estimateMessages(messages);
    const compactedTokenCount = this.tokenizer.estimateMessages(result.compacted);
    const savedTokens = Math.max(0, originalTokenCount - compactedTokenCount);
    const efficiency = originalTokenCount > 0 ? savedTokens / originalTokenCount : 0;
    const beforeRatio = originalTokenCount / this.config.maxContextTokens;

    this.stats.totalRuns++;
    this.stats.compactions++;
    this.stats.totalDropped += result.dropped;
    this.stats.lastCompaction = Date.now();
    this.stats.strategyUsed = strategy;
    this.stats.compressionRatios.push(beforeRatio);
    this.stats.compressionEfficiency.push(efficiency);
    this.stats.totalSavedTokens += savedTokens;
    this._consecutiveCompactions++;
    if (this._consecutiveCompactions > this.stats.maxConsecutiveCompactions) {
      this.stats.maxConsecutiveCompactions = this._consecutiveCompactions;
    }

    this._compactionHistory.push({
      timestamp: Date.now(), originalCount: messages.length,
      compactedCount: result.compacted.length, dropped: result.dropped,
      strategy, duration,
    });
    if (this._compactionHistory.length > 100) this._compactionHistory.shift();

    if (this.config.onCompactionEnd) {
      try { this.config.onCompactionEnd({ ...result, duration, strategy }); }
      catch (e) { /* 忽略回调错误 */ }
    }

    return {
      ...result,
      stats: {
        originalMessages: messages.length,
        compactedMessages: result.compacted.length,
        dropped: result.dropped, strategy, duration,
        tokenCount: this.tokenizer.estimateMessages(result.compacted),
      },
    };
  }

  /** 在 agent 运行前自动检查并压缩 */
  preFlightCheck(messages, options = {}) {
    const checkResult = this.check(messages);
    if (checkResult.level === 'warning') {
      this.stats.warnings++;
      if (this.config.onWarning) {
        try { this.config.onWarning(checkResult); }
        catch (e) { /* 回调异常不影响压缩流程 */ }
      }
    }
    if (checkResult.needsCompaction || (this.config.autoCompact && checkResult.level !== 'ok')) {
      const result = this.compact(messages, options);
      return { shouldProceed: true, messages: result.compacted, checkResult, compactionResult: result, compressed: true };
    }
    return { shouldProceed: true, messages, checkResult, compactionResult: null, compressed: false };
  }

  /** 获取统计 */
  getStats() {
    const avgEff = this.stats.compressionEfficiency.length > 0
      ? this.stats.compressionEfficiency.reduce((a, b) => a + b, 0) / this.stats.compressionEfficiency.length
      : 0;
    return {
      ...this.stats,
      historyLength: this._compactionHistory.length,
      averageCompressionEfficiency: Number(avgEff.toFixed(4)),
      compressionRatios: this.stats.compressionRatios.slice(-10),
      compressionEfficiency: this.stats.compressionEfficiency.slice(-10),
    };
  }

  /** 获取状态报告 */
  getStatus() {
    const recent = this._compactionHistory.slice(-5);
    return {
      config: {
        maxContextTokens: this.config.maxContextTokens,
        warningThreshold: this.config.warningThreshold,
        compactionThreshold: this.config.compactionThreshold,
        strategy: this.config.strategy,
        autoCompact: this.config.autoCompact,
      },
      stats: this.getStats(),
      recentCompactions: recent.map(h => ({
        timestamp: new Date(h.timestamp).toISOString(),
        dropped: h.dropped, strategy: h.strategy, duration: h.duration,
      })),
    };
  }

  /** 重置统计 */
  resetStats() {
    this.stats = {
      totalRuns: 0, warnings: 0, compactions: 0, totalDropped: 0,
      lastCompaction: null, strategyUsed: null,
      compressionRatios: [], compressionEfficiency: [], totalSavedTokens: 0,
      maxConsecutiveCompactions: 0,
    };
    this._compactionHistory = [];
    this._consecutiveCompactions = 0;
  }
}

module.exports = {
  AutoCompactionEngine,
  SimpleTokenizer,
  TrimStrategy,
  SummarizeStrategy,
};
