/**
 * AI-SEO-Optimizer - 主入口
 * 专业 SEO 分析与优化引擎
 */

const SEOEngine = require('./src/seo-engine');

// 创建 SEO 引擎实例
const seoEngine = new SEOEngine({
  maxKeywords: 20,
  minSearchVolume: 100,
  competitionThreshold: 0.7
});

/**
 * 处理 SEO 相关请求
 * @param {string} action - 操作类型
 * @param {Object} params - 参数
 * @returns {Promise<Object>} 结果
 */
async function handle(action, params) {
  try {
    switch (action) {
      case 'analyze':
        return await seoEngine.analyze(params.url, params.keywords);
      
      case 'keyword_research':
        return await seoEngine.keywordOpportunity(params.keyword);
      
      case 'optimize_content':
        return await seoEngine.optimizeContent(params.content, params.keywords);
      
      case 'track_rankings':
        return await seoEngine.trackRankings(params.keywords, params.domain);
      
      case 'internal_links':
        return await require('./src/internal-linker').suggest(params.url, params.content);
      
      case 'competitor_analysis':
        return await require('./src/rank-tracker').compareCompetitors(
          params.yourDomain,
          params.competitors,
          params.keywords
        );
      
      default:
        throw new Error(`未知操作：${action}`);
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
      action,
      params
    };
  }
}

// 导出模块
module.exports = {
  handle,
  analyze: (url, keywords) => seoEngine.analyze(url, keywords),
  keywordResearch: (keyword) => seoEngine.keywordOpportunity(keyword),
  optimizeContent: (content, keywords) => seoEngine.optimizeContent(content, keywords),
  trackRankings: (keywords, domain) => seoEngine.trackRankings(keywords, domain),
  suggestInternalLinks: (url, content) => require('./src/internal-linker').suggest(url, content),
  SEOEngine
};
