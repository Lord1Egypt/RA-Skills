/**
 * AI-SEO-Optimizer - 核心 SEO 分析引擎
 * 企业级 SEO 分析与优化系统
 */

const web_search = require('./web-search');
const contentAnalyzer = require('./content-analyzer');
const keywordResearch = require('./keyword-research');
const rankTracker = require('./rank-tracker');
const internalLinker = require('./internal-linker');

class SEOEngine {
  constructor(config = {}) {
    this.config = {
      maxKeywords: config.maxKeywords || 20,
      minSearchVolume: config.minSearchVolume || 100,
      competitionThreshold: config.competitionThreshold || 0.7,
      contentMinLength: config.contentMinLength || 300,
      ...config
    };
  }

  /**
   * 完整 SEO 分析
   * @param {string} url - 要分析的 URL 或内容
   * @param {string[]} targetKeywords - 目标关键词列表
   * @returns {Promise<Object>} SEO 分析报告
   */
  async analyze(url, targetKeywords = []) {
    const report = {
      timestamp: new Date().toISOString(),
      url: url,
      summary: {},
      scores: {},
      recommendations: [],
      keywords: [],
      competitors: [],
      internalLinks: []
    };

    try {
      // 1. 内容分析
      const contentAnalysis = await contentAnalyzer.analyze(url);
      report.scores.content = contentAnalysis.score;
      report.summary.contentLength = contentAnalysis.wordCount;
      report.summary.readability = contentAnalysis.readability;

      // 2. 关键词研究
      if (targetKeywords.length > 0) {
        const keywordData = await keywordResearch.analyzeKeywords(targetKeywords);
        report.keywords = keywordData;
        report.scores.keywords = this._calculateKeywordScore(keywordData);
      }

      // 3. 竞争分析
      const competitors = await this._analyzeCompetitors(url, targetKeywords);
      report.competitors = competitors;
      report.scores.competition = this._calculateCompetitionScore(competitors);

      // 4. 内链建议
      const internalLinks = await internalLinker.suggest(url);
      report.internalLinks = internalLinks;

      // 5. 生成综合评分和建议
      report.scores.overall = this._calculateOverallScore(report.scores);
      report.recommendations = this._generateRecommendations(report);

    } catch (error) {
      report.error = error.message;
      report.scores.overall = 0;
    }

    return report;
  }

  /**
   * 关键词机会分析
   * @param {string} keyword - 关键词
   * @returns {Promise<Object>} 关键词分析报告
   */
  async keywordOpportunity(keyword) {
    return await keywordResearch.findOpportunities(keyword);
  }

  /**
   * 内容优化建议
   * @param {string} content - 文章内容
   * @param {string[]} targetKeywords - 目标关键词
   * @returns {Promise<Object>} 优化建议
   */
  async optimizeContent(content, targetKeywords) {
    return await contentAnalyzer.getOptimizationSuggestions(content, targetKeywords);
  }

  /**
   * 排名追踪
   * @param {string[]} keywords - 要追踪的关键词
   * @param {string} domain - 网站域名
   * @returns {Promise<Object>} 排名数据
   */
  async trackRankings(keywords, domain) {
    return await rankTracker.track(keywords, domain);
  }

  /**
   * 计算关键词得分
   * @private
   */
  _calculateKeywordScore(keywordData) {
    if (!keywordData || keywordData.length === 0) return 0;
    
    const avgRelevance = keywordData.reduce((sum, k) => sum + (k.relevance || 0), 0) / keywordData.length;
    const avgVolume = keywordData.reduce((sum, k) => sum + (k.searchVolume || 0), 0) / keywordData.length;
    const avgDifficulty = keywordData.reduce((sum, k) => sum + (k.difficulty || 100), 0) / keywordData.length;
    
    return Math.round((avgRelevance * 0.4 + (avgVolume / 1000) * 0.3 + (1 - avgDifficulty / 100) * 0.3) * 100);
  }

  /**
   * 计算竞争得分
   * @private
   */
  _calculateCompetitionScore(competitors) {
    if (!competitors || competitors.length === 0) return 50;
    
    const avgAuthority = competitors.reduce((sum, c) => sum + (c.domainAuthority || 50), 0) / competitors.length;
    return Math.round(100 - avgAuthority + 50);
  }

  /**
   * 计算综合得分
   * @private
   */
  _calculateOverallScore(scores) {
    const weights = {
      content: 0.35,
      keywords: 0.30,
      competition: 0.20,
      technical: 0.15
    };
    
    const overall = (
      (scores.content || 0) * weights.content +
      (scores.keywords || 0) * weights.keywords +
      (scores.competition || 0) * weights.competition +
      (scores.technical || 50) * weights.technical
    );
    
    return Math.round(overall);
  }

  /**
   * 生成优化建议
   * @private
   */
  _generateRecommendations(report) {
    const recommendations = [];
    
    // 内容建议
    if (report.summary.contentLength < 1000) {
      recommendations.push({
        priority: 'high',
        category: 'content',
        title: '增加内容长度',
        description: `当前内容 ${report.summary.contentLength} 字，建议至少 1000 字以获得更好的排名`,
        impact: 'high'
      });
    }

    // 关键词建议
    if (report.scores.keywords < 60) {
      recommendations.push({
        priority: 'high',
        category: 'keywords',
        title: '优化关键词使用',
        description: '关键词分布不均或缺乏相关性，建议重新优化关键词策略',
        impact: 'high'
      });
    }

    // 内链建议
    if (report.internalLinks && report.internalLinks.length > 0) {
      recommendations.push({
        priority: 'medium',
        category: 'internal_links',
        title: '添加内部链接',
        description: `发现 ${report.internalLinks.length} 个内链机会，建议实施以提升页面权重`,
        impact: 'medium'
      });
    }

    // 竞争建议
    if (report.scores.competition < 50) {
      recommendations.push({
        priority: 'medium',
        category: 'competition',
        title: '差异化竞争策略',
        description: '竞争激烈，建议寻找长尾关键词机会或差异化内容角度',
        impact: 'medium'
      });
    }

    return recommendations.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
  }

  /**
   * 分析竞争对手
   * @private
   */
  async _analyzeCompetitors(url, keywords) {
    // 模拟竞争对手分析
    const competitors = [];
    
    if (keywords && keywords.length > 0) {
      // 这里会调用实际的搜索 API 获取竞争对手
      for (let i = 0; i < Math.min(5, keywords.length); i++) {
        competitors.push({
          domain: `competitor${i + 1}.com`,
          domainAuthority: Math.floor(Math.random() * 40) + 40,
          rankingPosition: i + 1,
          estimatedTraffic: Math.floor(Math.random() * 10000) + 1000
        });
      }
    }
    
    return competitors;
  }
}

module.exports = SEOEngine;
