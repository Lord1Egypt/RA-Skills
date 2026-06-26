/**
 * 常识推理引擎 (Commonsense Engine) v1.0.0
 *
 * 基于常识知识的推理
 */

const { KnowledgeBase } = require('./knowledge-base.js');

class CommonsenseEngine {
  constructor(options = {}) {
    this.knowledgeBase = new KnowledgeBase(options);
    this.inferenceHistory = [];
    this.maxHistory = options.maxHistory || 100;
  }

  /**
   * 推理
   */
  reason(statement, context = {}) {
    const result = {
      statement,
      context,
      timestamp: Date.now(),
      success: true,
      inference: null,
      confidence: 0
    };

    // 分析陈述
    const analysis = this._analyzeStatement(statement);

    // 查找相关知识
    const relevantKnowledge = this._findRelevantKnowledge(analysis);

    // 进行推理
    if (relevantKnowledge.length > 0) {
      result.inference = this._makeInference(statement, analysis, relevantKnowledge);
      result.confidence = this._calculateConfidence(relevantKnowledge, analysis);
    } else {
      result.inference = {
        type: 'unknown',
        conclusion: '缺乏相关常识知识',
        reasoning: '无法找到与该陈述相关的常识'
      };
      result.confidence = 0.1;
    }

    // 记录历史
    this.inferenceHistory.push(result);
    if (this.inferenceHistory.length > this.maxHistory) {
      this.inferenceHistory = this.inferenceHistory.slice(-this.maxHistory);
    }

    return result;
  }

  /**
   * 分析陈述
   */
  _analyzeStatement(statement) {
    const words = statement.split(/\s+/);
    const entities = [];
    const actions = [];
    const states = [];

    // 简单词性标注
    const stateWords = ['是', '为', '会', '能', '应该', '可能', '会'];
    const actionWords = ['做', '让', '使', '导致', '引起', '造成'];

    for (const word of words) {
      if (stateWords.includes(word)) states.push(word);
      if (actionWords.includes(word)) actions.push(word);
    }

    return {
      original: statement,
      words,
      entities,
      actions,
      states,
      subject: words.slice(0, 3).join(''),
      containsNegation: /不|没|无|非/.test(statement),
      containsUncertainty: /可能|也许|大概|应该/.test(statement)
    };
  }

  /**
   * 查找相关知识
   */
  _findRelevantKnowledge(analysis) {
    const relevant = [];

    // 查询所有类别
    for (const category of this.knowledgeBase.getCategories()) {
      const facts = this.knowledgeBase.getCategory(category);

      for (const fact of facts) {
        const relevance = this._assessRelevance(analysis, fact);
        if (relevance > 0.2) {
          relevant.push({ ...fact, relevance });
        }
      }
    }

    return relevant.sort((a, b) => b.relevance - a.relevance);
  }

  /**
   * 评估相关性
   */
  _assessRelevance(analysis, fact) {
    const statementWords = new Set(analysis.words.map(w => w.toLowerCase()));
    const factWords = new Set(
      `${fact.statement} ${fact.explanation} ${fact.key}`.toLowerCase().split(/\s+/)
    );

    const intersection = [...statementWords].filter(w => factWords.has(w)).length;
    const union = new Set([...statementWords, ...factWords]).size;

    return union > 0 ? intersection / union : 0;
  }

  /**
   * 进行推理
   */
  _makeInference(statement, analysis, relevantKnowledge) {
    const bestMatch = relevantKnowledge[0];

    // 判断推理类型
    if (analysis.containsUncertainty) {
      return {
        type: 'probabilistic',
        conclusion: statement,
        reasoning: `基于常识：${bestMatch.statement}`,
        support: bestMatch.explanation,
        certainty: 'possible'
      };
    }

    if (analysis.containsNegation) {
      return {
        type: 'counterfactual',
        conclusion: statement,
        reasoning: `如果正常情况是"${bestMatch.statement}"，那么否定意味着相反`,
        support: bestMatch.key,
        certainty: 'unlikely'
      };
    }

    // 因果推理
    if (analysis.actions.length > 0) {
      return {
        type: 'causal',
        conclusion: statement,
        reasoning: `根据因果关系：${bestMatch.statement}`,
        support: bestMatch.explanation,
        certainty: 'likely'
      };
    }

    // 属性推理
    return {
      type: 'attribute',
      conclusion: statement,
      reasoning: `根据常识知识：${bestMatch.statement}`,
      support: bestMatch.key,
      certainty: 'likely'
    };
  }

  /**
   * 计算置信度
   */
  _calculateConfidence(relevantKnowledge, analysis) {
    if (relevantKnowledge.length === 0) return 0.1;

    let confidence = 0.3;

    // 最高相关性加分
    confidence += relevantKnowledge[0].relevance * 0.3;

    // 知识数量加分
    if (relevantKnowledge.length >= 3) confidence += 0.2;
    else if (relevantKnowledge.length >= 1) confidence += 0.1;

    // 不确定性惩罚
    if (analysis.containsUncertainty) confidence *= 0.8;

    // 否定惩罚
    if (analysis.containsNegation) confidence *= 0.7;

    return Math.min(0.95, Math.max(0.1, confidence));
  }

  /**
   * 验证陈述
   */
  validate(statement) {
    const reasoning = this.reason(statement);
    return {
      valid: reasoning.confidence > 0.5,
      confidence: reasoning.confidence,
      reasoning: reasoning.inference
    };
  }

  /**
   * 获取推理历史
   */
  getHistory(limit = 20) {
    return this.inferenceHistory.slice(-limit);
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      totalInferences: this.inferenceHistory.length,
      knowledgeFacts: this.knowledgeBase.getStats().totalFacts,
      knowledgeCategories: this.knowledgeBase.getStats().categories,
      recentInferences: this.inferenceHistory.slice(-5)
    };
  }
}

module.exports = { CommonsenseEngine };
