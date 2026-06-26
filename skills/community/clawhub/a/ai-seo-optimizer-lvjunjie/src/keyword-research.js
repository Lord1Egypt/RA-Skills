/**
 * 关键词研究与竞争分析模块
 */

class KeywordResearch {
  constructor() {
    this.keywordDatabase = new Map();
    this.competitionCache = new Map();
  }

  /**
   * 分析关键词列表
   * @param {string[]} keywords - 关键词列表
   * @returns {Promise<Array>} 关键词分析结果
   */
  async analyzeKeywords(keywords) {
    const results = [];
    
    for (const keyword of keywords) {
      const analysis = await this._analyzeSingleKeyword(keyword);
      results.push(analysis);
    }
    
    return results.sort((a, b) => b.opportunityScore - a.opportunityScore);
  }

  /**
   * 寻找关键词机会
   * @param {string} seedKeyword - 种子关键词
   * @returns {Promise<Object>} 机会分析报告
   */
  async findOpportunities(seedKeyword) {
    const relatedKeywords = await this._findRelatedKeywords(seedKeyword);
    const opportunities = [];
    
    for (const keyword of relatedKeywords) {
      const analysis = await this._analyzeSingleKeyword(keyword);
      
      // 高机会：高搜索量 + 低竞争
      if (analysis.searchVolume > 500 && analysis.difficulty < 40) {
        opportunities.push({
          ...analysis,
          opportunityType: 'low_competition',
          priority: 'high'
        });
      }
      
      // 长尾机会
      if (keyword.split(' ').length >= 3 && analysis.difficulty < 50) {
        opportunities.push({
          ...analysis,
          opportunityType: 'long_tail',
          priority: 'medium'
        });
      }
    }
    
    return {
      seedKeyword,
      totalOpportunities: opportunities.length,
      highPriority: opportunities.filter(o => o.priority === 'high').length,
      opportunities: opportunities.slice(0, 20)
    };
  }

  /**
   * 获取长尾关键词
   * @param {string} keyword - 主关键词
   * @param {number} limit - 返回数量
   * @returns {Promise<string[]>} 长尾关键词列表
   */
  async getLongTailKeywords(keyword, limit = 10) {
    const patterns = [
      `最佳 ${keyword}`,
      `${keyword} 教程`,
      `${keyword} 指南`,
      `如何 ${keyword}`,
      `${keyword} 技巧`,
      `${keyword} 工具`,
      `${keyword} 2026`,
      `${keyword} 对比`,
      `${keyword} 推荐`,
      `免费 ${keyword}`,
      `${keyword} 步骤`,
      `${keyword} 方法`,
      `${keyword} 示例`,
      `${keyword} 案例`,
      `${keyword} 策略`
    ];
    
    return patterns.slice(0, limit);
  }

  /**
   * 分析单个关键词
   * @private
   */
  async _analyzeSingleKeyword(keyword) {
    // 检查缓存
    if (this.keywordDatabase.has(keyword)) {
      return this.keywordDatabase.get(keyword);
    }
    
    // 模拟关键词分析数据
    const analysis = {
      keyword,
      searchVolume: this._estimateSearchVolume(keyword),
      difficulty: this._estimateDifficulty(keyword),
      cpc: this._estimateCPC(keyword),
      trend: this._analyzeTrend(keyword),
      relevance: this._calculateRelevance(keyword),
      opportunityScore: 0,
      relatedKeywords: []
    };
    
    // 计算机会分数
    analysis.opportunityScore = this._calculateOpportunityScore(analysis);
    
    // 获取相关关键词
    analysis.relatedKeywords = await this.getLongTailKeywords(keyword, 5);
    
    // 缓存结果
    this.keywordDatabase.set(keyword, analysis);
    
    return analysis;
  }

  /**
   * 估算搜索量
   * @private
   */
  _estimateSearchVolume(keyword) {
    const length = keyword.split(' ').length;
    const baseVolume = 5000;
    
    // 长尾关键词搜索量较低
    const lengthFactor = length === 1 ? 1 : length === 2 ? 0.5 : 0.2;
    
    // 根据关键词类型调整
    const typeFactors = {
      '教程': 0.8,
      '指南': 0.7,
      '如何': 0.9,
      '最佳': 1.2,
      '免费': 1.5,
      '工具': 1.1,
      '对比': 0.6,
      '推荐': 0.8
    };
    
    let typeFactor = 1;
    for (const [type, factor] of Object.entries(typeFactors)) {
      if (keyword.includes(type)) {
        typeFactor = factor;
        break;
      }
    }
    
    return Math.floor(baseVolume * lengthFactor * typeFactor * (0.5 + Math.random()));
  }

  /**
   * 估算竞争难度
   * @private
   */
  _estimateDifficulty(keyword) {
    const length = keyword.split(' ').length;
    
    // 短词竞争更高
    let baseDifficulty = length === 1 ? 70 : length === 2 ? 50 : 30;
    
    // 商业意图关键词竞争更高
    const commercialTerms = ['购买', '价格', '便宜', '优惠', '折扣', '品牌'];
    const hasCommercialIntent = commercialTerms.some(term => keyword.includes(term));
    
    if (hasCommercialIntent) {
      baseDifficulty += 20;
    }
    
    return Math.min(100, Math.max(0, baseDifficulty + Math.floor(Math.random() * 20 - 10)));
  }

  /**
   * 估算点击成本
   * @private
   */
  _estimateCPC(keyword) {
    const commercialTerms = ['购买', '价格', '服务', '公司', '软件', '工具'];
    const hasCommercialIntent = commercialTerms.some(term => keyword.includes(term));
    
    const baseCPC = hasCommercialIntent ? 2.5 : 0.8;
    return parseFloat((baseCPC * (0.5 + Math.random())).toFixed(2));
  }

  /**
   * 分析趋势
   * @private
   */
  _analyzeTrend(keyword) {
    const trends = ['rising', 'stable', 'declining', 'seasonal'];
    const weights = [0.3, 0.4, 0.1, 0.2];
    
    const random = Math.random();
    let cumulative = 0;
    
    for (let i = 0; i < trends.length; i++) {
      cumulative += weights[i];
      if (random <= cumulative) {
        return trends[i];
      }
    }
    
    return 'stable';
  }

  /**
   * 计算相关性
   * @private
   */
  _calculateRelevance(keyword) {
    // 基于关键词质量评估相关性
    const qualityIndicators = [
      '如何', '教程', '指南', '技巧', '方法',
      '最佳', '推荐', '对比', '评测'
    ];
    
    const hasQualityIndicator = qualityIndicators.some(ind => keyword.includes(ind));
    
    if (hasQualityIndicator) {
      return 0.8 + Math.random() * 0.2;
    }
    
    return 0.5 + Math.random() * 0.3;
  }

  /**
   * 计算机会分数
   * @private
   */
  _calculateOpportunityScore(analysis) {
    const volumeScore = Math.min(100, analysis.searchVolume / 100);
    const difficultyScore = 100 - analysis.difficulty;
    const trendScore = {
      'rising': 100,
      'stable': 70,
      'seasonal': 60,
      'declining': 30
    }[analysis.trend];
    
    return Math.round(
      volumeScore * 0.4 +
      difficultyScore * 0.4 +
      trendScore * 0.2
    );
  }

  /**
   * 查找相关关键词
   * @private
   */
  async _findRelatedKeywords(seedKeyword) {
    const related = new Set([seedKeyword]);
    
    // 添加问题型关键词
    const questionStarters = ['什么是', '为什么', '怎么做', '如何', '哪些'];
    questionStarters.forEach(starter => {
      related.add(`${starter}${seedKeyword}`);
    });
    
    // 添加长尾变体
    const longTails = await this.getLongTailKeywords(seedKeyword, 15);
    longTails.forEach(kw => related.add(kw));
    
    return Array.from(related);
  }
}

module.exports = new KeywordResearch();
