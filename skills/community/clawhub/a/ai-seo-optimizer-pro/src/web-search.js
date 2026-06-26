/**
 * Web 搜索模块 - 用于 SEO 数据获取
 */

class WebSearch {
  constructor() {
    this.cache = new Map();
    this.cacheExpiry = 3600000; // 1 小时
  }

  /**
   * 搜索关键词
   * @param {string} query - 搜索查询
   * @param {number} limit - 结果数量
   * @returns {Promise<Array>} 搜索结果
   */
  async search(query, limit = 10) {
    const cacheKey = `search:${query}:${limit}`;
    
    // 检查缓存
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheExpiry) {
        return cached.results;
      }
    }
    
    // 实际实现会调用 web_search 工具
    const results = await this._performSearch(query, limit);
    
    // 缓存结果
    this.cache.set(cacheKey, {
      results,
      timestamp: Date.now()
    });
    
    return results;
  }

  /**
   * 获取 SERP 数据
   * @param {string} keyword - 关键词
   * @returns {Promise<Object>} SERP 数据
   */
  async getSerpData(keyword) {
    const searchResults = await this.search(keyword, 20);
    
    return {
      keyword,
      totalResults: searchResults.length,
      topResults: searchResults.slice(0, 10).map((result, index) => ({
        position: index + 1,
        title: result.title,
        url: result.url,
        domain: this._extractDomain(result.url),
        snippet: result.snippet
      })),
      serpFeatures: this._detectSerpFeatures(searchResults),
      competitors: this._extractCompetitors(searchResults)
    };
  }

  /**
   * 执行搜索
   * @private
   */
  async _performSearch(query, limit) {
    // 模拟搜索结果
    const mockResults = [];
    const domains = [
      'baike.baidu.com',
      'zhihu.com',
      'jianshu.com',
      'csdn.net',
      'segmentfault.com',
      'oschina.net',
      'github.com',
      'medium.com'
    ];
    
    for (let i = 0; i < limit; i++) {
      mockResults.push({
        title: `${query} - 第${i + 1}个结果`,
        url: `https://${domains[i % domains.length]}/page/${i + 1}`,
        snippet: `这是关于${query}的详细内容介绍...`,
        domain: domains[i % domains.length]
      });
    }
    
    return mockResults;
  }

  /**
   * 提取域名
   * @private
   */
  _extractDomain(url) {
    try {
      const urlObj = new URL(url);
      return urlObj.hostname.replace('www.', '');
    } catch {
      return 'unknown';
    }
  }

  /**
   * 检测 SERP 特性
   * @private
   */
  _detectSerpFeatures(results) {
    const features = [];
    
    // 检测是否有视频
    if (results.some(r => r.url.includes('youtube') || r.url.includes('bilibili'))) {
      features.push('video');
    }
    
    // 检测是否有图片
    if (results.some(r => r.url.includes('image') || r.url.includes('pic'))) {
      features.push('images');
    }
    
    // 检测是否有新闻
    if (results.some(r => r.url.includes('news'))) {
      features.push('news');
    }
    
    // 检测是否有问答
    if (results.some(r => r.url.includes('zhihu') || r.url.includes('quora'))) {
      features.push('people_also_ask');
    }
    
    return features;
  }

  /**
   * 提取竞争对手
   * @private
   */
  _extractCompetitors(results) {
    const domainCount = new Map();
    
    for (const result of results) {
      const domain = this._extractDomain(result.url);
      domainCount.set(domain, (domainCount.get(domain) || 0) + 1);
    }
    
    return Array.from(domainCount.entries())
      .map(([domain, count]) => ({
        domain,
        appearances: count,
        visibility: (count / results.length * 100).toFixed(1) + '%'
      }))
      .sort((a, b) => b.appearances - a.appearances)
      .slice(0, 10);
  }
}

module.exports = new WebSearch();
