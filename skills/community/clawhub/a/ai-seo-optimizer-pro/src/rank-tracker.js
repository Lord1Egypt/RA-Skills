/**
 * 排名追踪与报告模块
 */

class RankTracker {
  constructor() {
    this.trackingData = new Map();
    this.historyLimit = 90; // 保留 90 天历史
  }

  /**
   * 追踪关键词排名
   * @param {string[]} keywords - 关键词列表
   * @param {string} domain - 网站域名
   * @returns {Promise<Object>} 排名数据
   */
  async track(keywords, domain) {
    const results = [];
    const timestamp = new Date().toISOString();
    
    for (const keyword of keywords) {
      const ranking = await this._getRanking(keyword, domain);
      results.push({
        keyword,
        domain,
        ...ranking,
        timestamp
      });
      
      // 保存历史数据
      this._saveHistory(keyword, domain, ranking);
    }
    
    return {
      domain,
      trackedKeywords: keywords.length,
      timestamp,
      rankings: results,
      summary: this._generateSummary(results)
    };
  }

  /**
   * 获取排名历史
   * @param {string} keyword - 关键词
   * @param {string} domain - 域名
   * @param {number} days - 天数
   * @returns {Promise<Array>} 历史数据
   */
  async getHistory(keyword, domain, days = 30) {
    const key = `${keyword}:${domain}`;
    const history = this.trackingData.get(key) || [];
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    return history
      .filter(record => new Date(record.timestamp) >= cutoffDate)
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  }

  /**
   * 生成排名报告
   * @param {string} domain - 域名
   * @param {string[]} keywords - 关键词
   * @returns {Promise<Object>} 排名报告
   */
  async generateReport(domain, keywords) {
    const currentRankings = await this.track(keywords, domain);
    
    const report = {
      domain,
      generatedAt: new Date().toISOString(),
      period: 'last_30_days',
      overview: {
        totalKeywords: keywords.length,
        top3Count: 0,
        top10Count: 0,
        top50Count: 0,
        notRanking: 0,
        averagePosition: 0
      },
      changes: {
        improved: 0,
        declined: 0,
        unchanged: 0,
        new: 0
      },
      keywords: [],
      recommendations: []
    };
    
    let totalPosition = 0;
    let rankedCount = 0;
    
    for (const ranking of currentRankings.rankings) {
      const history = await this.getHistory(ranking.keyword, domain, 30);
      const previousPosition = history.length > 0 ? history[history.length - 1].position : null;
      
      const keywordData = {
        keyword: ranking.keyword,
        currentPosition: ranking.position,
        previousPosition,
        change: previousPosition ? previousPosition - ranking.position : null,
        trend: this._calculateTrend(history),
        searchVolume: ranking.searchVolume,
        difficulty: ranking.difficulty,
        url: ranking.url
      };
      
      report.keywords.push(keywordData);
      
      // 统计概览
      if (ranking.position <= 3) report.overview.top3Count++;
      if (ranking.position <= 10) report.overview.top10Count++;
      if (ranking.position <= 50) report.overview.top50Count++;
      if (ranking.position > 50) report.overview.notRanking++;
      
      if (ranking.position <= 50) {
        totalPosition += ranking.position;
        rankedCount++;
      }
      
      // 统计变化
      if (previousPosition) {
        if (keywordData.change > 0) report.changes.improved++;
        else if (keywordData.change < 0) report.changes.declined++;
        else report.changes.unchanged++;
      } else {
        report.changes.new++;
      }
    }
    
    report.overview.averagePosition = rankedCount > 0 
      ? Math.round(totalPosition / rankedCount) 
      : 0;
    
    // 生成建议
    report.recommendations = this._generateRecommendations(report);
    
    return report;
  }

  /**
   * 对比竞争对手
   * @param {string} yourDomain - 你的域名
   * @param {string[]} competitorDomains - 竞争对手域名
   * @param {string[]} keywords - 关键词
   * @returns {Promise<Object>} 对比报告
   */
  async compareCompetitors(yourDomain, competitorDomains, keywords) {
    const comparison = {
      yourDomain,
      competitors: [],
      keywordBreakdown: [],
      opportunities: []
    };
    
    // 获取你的排名
    const yourRankings = await this.track(keywords, yourDomain);
    
    // 获取竞争对手排名
    for (const competitor of competitorDomains) {
      const competitorRankings = await this.track(keywords, competitor);
      comparison.competitors.push({
        domain: competitor,
        rankings: competitorRankings.rankings,
        summary: this._generateSummary(competitorRankings.rankings)
      });
    }
    
    // 关键词级别对比
    for (const keyword of keywords) {
      const yourRank = yourRankings.rankings.find(r => r.keyword === keyword);
      const competitorRanks = comparison.competitors.map(c => ({
        domain: c.domain,
        rank: c.rankings.find(r => r.keyword === keyword)
      }));
      
      comparison.keywordBreakdown.push({
        keyword,
        yourPosition: yourRank?.position || 100,
        competitorPositions: competitorRanks,
        bestCompetitor: competitorRanks.reduce((best, curr) => 
          curr.rank?.position < best.rank?.position ? curr : best
        )
      });
    }
    
    // 发现机会
    comparison.opportunities = this._findOpportunities(comparison);
    
    return comparison;
  }

  /**
   * 获取单个关键词排名
   * @private
   */
  async _getRanking(keyword, domain) {
    // 模拟排名数据
    const position = Math.floor(Math.random() * 100) + 1;
    
    return {
      position,
      previousPosition: position + Math.floor(Math.random() * 10 - 5),
      url: `https://${domain}/page/${keyword.replace(/\s+/g, '-')}`,
      searchVolume: Math.floor(Math.random() * 5000) + 100,
      difficulty: Math.floor(Math.random() * 100),
      serpFeatures: this._getSerpFeatures(position)
    };
  }

  /**
   * 保存历史数据
   * @private
   */
  _saveHistory(keyword, domain, ranking) {
    const key = `${keyword}:${domain}`;
    let history = this.trackingData.get(key) || [];
    
    history.push({
      timestamp: new Date().toISOString(),
      position: ranking.position,
      url: ranking.url
    });
    
    // 限制历史记录长度
    if (history.length > this.historyLimit) {
      history = history.slice(-this.historyLimit);
    }
    
    this.trackingData.set(key, history);
  }

  /**
   * 生成摘要
   * @private
   */
  _generateSummary(rankings) {
    const total = rankings.length;
    const top3 = rankings.filter(r => r.position <= 3).length;
    const top10 = rankings.filter(r => r.position <= 10).length;
    const top50 = rankings.filter(r => r.position <= 50).length;
    
    const totalPosition = rankings
      .filter(r => r.position <= 50)
      .reduce((sum, r) => sum + r.position, 0);
    const rankedCount = rankings.filter(r => r.position <= 50).length;
    
    return {
      total,
      top3,
      top10,
      top50,
      notRanking: total - top50,
      averagePosition: rankedCount > 0 ? (totalPosition / rankedCount).toFixed(1) : 'N/A',
      visibility: ((top3 * 3 + top10 * 2 + top50) / (total * 3) * 100).toFixed(1) + '%'
    };
  }

  /**
   * 计算趋势
   * @private
   */
  _calculateTrend(history) {
    if (history.length < 2) return 'stable';
    
    const recent = history.slice(-7);
    const older = history.slice(-14, -7);
    
    if (older.length === 0) return 'stable';
    
    const recentAvg = recent.reduce((sum, r) => sum + r.position, 0) / recent.length;
    const olderAvg = older.reduce((sum, r) => sum + r.position, 0) / older.length;
    
    const change = olderAvg - recentAvg;
    
    if (change > 2) return 'rising';
    if (change < -2) return 'falling';
    return 'stable';
  }

  /**
   * 获取 SERP 特性
   * @private
   */
  _getSerpFeatures(position) {
    const features = [];
    
    if (position === 1) features.push('featured_snippet');
    if (position <= 3) features.push('top_stories');
    if (position <= 10) features.push('people_also_ask');
    
    if (Math.random() > 0.5) features.push('image_pack');
    if (Math.random() > 0.7) features.push('video_carousel');
    
    return features;
  }

  /**
   * 生成建议
   * @private
   */
  _generateRecommendations(report) {
    const recommendations = [];
    
    // 前 3 名比例低
    if (report.overview.top3Count / report.overview.totalKeywords < 0.1) {
      recommendations.push({
        priority: 'high',
        title: '提升前 3 名排名',
        description: `只有 ${report.overview.top3Count} 个关键词在前 3 名`,
        action: '优化高价值关键词的内容和质量'
      });
    }
    
    // 平均排名低
    if (report.overview.averagePosition > 20) {
      recommendations.push({
        priority: 'high',
        title: '改善平均排名',
        description: `平均排名 ${report.overview.averagePosition}，需要提升`,
        action: '关注排名 11-20 的关键词，推动进入前 10'
      });
    }
    
    // 下降的关键词
    if (report.changes.declined > report.changes.improved) {
      recommendations.push({
        priority: 'medium',
        title: '关注下降关键词',
        description: `${report.changes.declined} 个关键词排名下降`,
        action: '检查下降关键词的内容是否需要更新'
      });
    }
    
    return recommendations;
  }

  /**
   * 发现机会
   * @private
   */
  _findOpportunities(comparison) {
    const opportunities = [];
    
    for (const breakdown of comparison.keywordBreakdown) {
      const yourPos = breakdown.yourPosition;
      const bestCompetitorPos = breakdown.bestCompetitor.rank?.position || 100;
      
      // 你落后但差距不大
      if (yourPos > bestCompetitorPos && yourPos - bestCompetitorPos <= 5 && yourPos <= 20) {
        opportunities.push({
          keyword: breakdown.keyword,
          yourPosition: yourPos,
          competitorPosition: bestCompetitorPos,
          gap: yourPos - bestCompetitorPos,
          opportunity: 'small_improvement_needed',
          action: '小幅优化即可超越竞争对手'
        });
      }
    }
    
    return opportunities.slice(0, 10);
  }
}

module.exports = new RankTracker();
