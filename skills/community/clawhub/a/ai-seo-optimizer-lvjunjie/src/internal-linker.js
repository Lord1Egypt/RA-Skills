/**
 * 自动内链建议模块
 */

class InternalLinker {
  constructor() {
    this.pageDatabase = new Map();
    this.anchorTextVariations = new Map();
  }

  /**
   * 为页面生成内链建议
   * @param {string} url - 页面 URL
   * @param {string} content - 页面内容
   * @returns {Promise<Array>} 内链建议列表
   */
  async suggest(url, content = '') {
    const suggestions = [];
    
    // 分析内容主题
    const topics = this._extractTopics(content);
    
    // 查找相关页面
    const relatedPages = await this._findRelatedPages(topics, url);
    
    // 生成内链建议
    for (const page of relatedPages) {
      const suggestion = {
        targetUrl: page.url,
        targetTitle: page.title,
        anchorTexts: this._generateAnchorTexts(page.title, page.keywords),
        context: this._findLinkContext(content, page.keywords),
        priority: this._calculatePriority(page, topics),
        linkType: this._determineLinkType(page),
        seoValue: this._calculateSeoValue(page)
      };
      
      suggestions.push(suggestion);
    }
    
    // 按优先级排序
    return suggestions
      .sort((a, b) => b.seoValue - a.seoValue)
      .slice(0, 10);
  }

  /**
   * 优化锚文本
   * @param {string} currentText - 当前锚文本
   * @param {string} targetPage - 目标页面主题
   * @returns {Array} 优化的锚文本建议
   */
  optimizeAnchorText(currentText, targetPage) {
    const variations = [];
    
    // 精确匹配
    variations.push({
      text: targetPage,
      type: 'exact',
      recommendation: '高相关性，但避免过度使用'
    });
    
    // 部分匹配
    const partialMatch = targetPage.split(' ').slice(0, 2).join(' ');
    if (partialMatch !== targetPage) {
      variations.push({
        text: partialMatch,
        type: 'partial',
        recommendation: '自然且相关'
      });
    }
    
    // 品牌变体
    variations.push({
      text: `了解更多关于${targetPage}`,
      type: 'branded',
      recommendation: '用户友好'
    });
    
    // 上下文变体
    variations.push({
      text: '点击这里',
      type: 'generic',
      recommendation: '避免使用 - SEO 价值低',
      warning: true
    });
    
    return variations;
  }

  /**
   * 分析内链结构
   * @param {Array} pages - 网站页面列表
   * @returns {Object} 内链结构分析
   */
  analyzeStructure(pages) {
    const analysis = {
      totalLinks: 0,
      orphanedPages: [],
      hubPages: [],
      averageLinksPerPage: 0,
      depthDistribution: {},
      recommendations: []
    };
    
    // 统计链接
    const linkCount = new Map();
    const linkedPages = new Set();
    
    for (const page of pages) {
      const outLinks = page.outboundLinks || 0;
      const inLinks = page.inboundLinks || 0;
      
      linkCount.set(page.url, { in: inLinks, out: outLinks });
      analysis.totalLinks += outLinks;
      
      if (inLinks > 0) linkedPages.add(page.url);
      if (inLinks === 0 && page.url !== '/home') {
        analysis.orphanedPages.push(page.url);
      }
      
      if (outLinks > 10) {
        analysis.hubPages.push({
          url: page.url,
          outLinks
        });
      }
    }
    
    analysis.averageLinksPerPage = pages.length > 0 
      ? (analysis.totalLinks / pages.length).toFixed(1) 
      : 0;
    
    // 生成建议
    if (analysis.orphanedPages.length > 0) {
      analysis.recommendations.push({
        priority: 'high',
        issue: '孤立页面',
        count: analysis.orphanedPages.length,
        action: '为孤立页面添加内部链接',
        pages: analysis.orphanedPages.slice(0, 5)
      });
    }
    
    if (parseFloat(analysis.averageLinksPerPage) < 3) {
      analysis.recommendations.push({
        priority: 'medium',
        issue: '内链数量不足',
        action: '每页建议至少 3-5 个内链'
      });
    }
    
    return analysis;
  }

  /**
   * 提取内容主题
   * @private
   */
  _extractTopics(content) {
    const topics = [];
    
    // 提取关键词
    const words = content.toLowerCase().split(/\s+/);
    const wordFreq = new Map();
    
    for (const word of words) {
      if (word.length > 3) {
        wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
      }
    }
    
    // 获取高频词作为主题
    const sortedWords = Array.from(wordFreq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);
    
    for (const [word, freq] of sortedWords) {
      topics.push({ word, frequency: freq });
    }
    
    return topics;
  }

  /**
   * 查找相关页面
   * @private
   */
  async _findRelatedPages(topics, excludeUrl) {
    // 模拟页面数据库
    const mockPages = [
      { url: '/seo-guide', title: 'SEO 完整指南', keywords: ['seo', '优化', '排名'], authority: 85 },
      { url: '/keyword-research', title: '关键词研究教程', keywords: ['关键词', '研究', '工具'], authority: 78 },
      { url: '/content-optimization', title: '内容优化技巧', keywords: ['内容', '优化', '写作'], authority: 72 },
      { url: '/link-building', title: '外链建设策略', keywords: ['外链', '链接', '建设'], authority: 80 },
      { url: '/technical-seo', title: '技术 SEO 详解', keywords: ['技术', 'seo', '网站'], authority: 75 },
      { url: '/analytics', title: 'SEO 数据分析', keywords: ['数据', '分析', '追踪'], authority: 68 },
      { url: '/local-seo', title: '本地 SEO 指南', keywords: ['本地', 'seo', '地图'], authority: 65 },
      { url: '/ecommerce-seo', title: '电商 SEO 优化', keywords: ['电商', '产品', '优化'], authority: 70 }
    ];
    
    // 计算相关性
    const relatedPages = mockPages
      .filter(page => page.url !== excludeUrl)
      .map(page => ({
        ...page,
        relevance: this._calculateRelevance(page.keywords, topics)
      }))
      .filter(page => page.relevance > 0.3)
      .sort((a, b) => b.relevance - a.relevance);
    
    return relatedPages.slice(0, 10);
  }

  /**
   * 生成锚文本
   * @private
   */
  _generateAnchorTexts(title, keywords) {
    const variations = [];
    
    // 精确标题
    variations.push(title);
    
    // 缩短版本
    if (title.length > 10) {
      variations.push(title.split(' ').slice(0, 3).join(' '));
    }
    
    // 关键词变体
    for (const keyword of keywords.slice(0, 2)) {
      variations.push(keyword);
      variations.push(`${keyword}教程`);
      variations.push(`${keyword}指南`);
    }
    
    // 行动号召
    variations.push(`了解${keywords[0] || '更多'}`);
    variations.push(`${title}详情`);
    
    return [...new Set(variations)].slice(0, 5);
  }

  /**
   * 查找链接上下文
   * @private
   */
  _findLinkContext(content, keywords) {
    const sentences = content.split(/[。！？.!?]/);
    
    for (const sentence of sentences) {
      const hasKeyword = keywords.some(kw => sentence.toLowerCase().includes(kw.toLowerCase()));
      if (hasKeyword && sentence.length > 20 && sentence.length < 200) {
        return sentence.trim();
      }
    }
    
    return null;
  }

  /**
   * 计算优先级
   * @private
   */
  _calculatePriority(page, topics) {
    const topicMatch = topics.filter(t => 
      page.keywords.some(k => k.includes(t.word) || t.word.includes(k))
    ).length;
    
    if (topicMatch >= 3) return 'high';
    if (topicMatch >= 1) return 'medium';
    return 'low';
  }

  /**
   * 确定链接类型
   * @private
   */
  _determineLinkType(page) {
    if (page.url.includes('/guide') || page.url.includes('/tutorial')) {
      return 'educational';
    }
    if (page.url.includes('/product') || page.url.includes('/service')) {
      return 'commercial';
    }
    if (page.url.includes('/blog') || page.url.includes('/news')) {
      return 'informational';
    }
    return 'general';
  }

  /**
   * 计算 SEO 价值
   * @private
   */
  _calculateSeoValue(page) {
    const baseScore = page.authority || 50;
    const relevanceBonus = (page.relevance || 0.5) * 30;
    const typeBonus = {
      'educational': 15,
      'commercial': 10,
      'informational': 12,
      'general': 5
    }[this._determineLinkType(page)] || 5;
    
    return Math.round(baseScore + relevanceBonus + typeBonus);
  }

  /**
   * 计算相关性
   * @private
   */
  _calculateRelevance(keywords, topics) {
    if (!topics || topics.length === 0) return 0.5;
    
    const topicWords = topics.map(t => t.word);
    const matches = keywords.filter(k => 
      topicWords.some(tw => tw.includes(k) || k.includes(tw))
    ).length;
    
    return matches / Math.max(keywords.length, 1);
  }
}

module.exports = new InternalLinker();
