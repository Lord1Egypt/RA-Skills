/**
 * Affiliate-Marketing-Auto - 联盟营销自动化技能主入口
 * 
 * 功能：
 * - 高佣金产品发现
 * - 自动内容生成
 * - 链接追踪和管理
 * - 收入报告和分析
 */

import ProductFinder from './product-finder.js';
import ContentGenerator from './content-generator.js';
import LinkTracker from './link-tracker.js';
import Analytics from './analytics.js';

class AffiliateMarketingAuto {
  constructor() {
    this.config = null;
    this.productFinder = new ProductFinder();
    this.contentGenerator = new ContentGenerator();
    this.linkTracker = new LinkTracker();
    this.analytics = new Analytics();
  }

  /**
   * 配置联盟平台账户
   * @param {Object} config - 配置对象
   */
  async configure(config) {
    this.config = config;
    
    // 验证配置
    if (!config.platforms) {
      throw new Error('必须配置至少一个联盟平台');
    }

    // 初始化各平台
    await this.productFinder.initialize(config);
    await this.linkTracker.initialize(config);
    await this.analytics.initialize(config);

    console.log('✅ 联盟营销自动化配置完成');
    return { success: true, platforms: Object.keys(config.platforms) };
  }

  /**
   * 发现高佣金产品
   * @param {Object} options - 搜索选项
   * @returns {Promise<Array>} 产品列表
   */
  async findProducts(options = {}) {
    if (!this.config) {
      throw new Error('请先调用 configure() 进行配置');
    }

    const defaults = {
      category: 'all',
      minCommissionRate: 0.05,
      minPrice: 20,
      maxResults: 20,
      sortBy: 'commission'
    };

    const searchOptions = { ...defaults, ...options };
    return await this.productFinder.find(searchOptions);
  }

  /**
   * 获取热门产品
   * @param {string} category - 类别
   * @returns {Promise<Array>} 产品列表
   */
  async getTrendingProducts(category = 'all') {
    return await this.productFinder.getTrending(category);
  }

  /**
   * 分析利基市场
   * @param {Object} options - 分析选项
   * @returns {Promise<Object>} 分析结果
   */
  async analyzeNiche(options = {}) {
    return await this.productFinder.analyzeNiche(options);
  }

  /**
   * 生成推广内容
   * @param {Object} options - 内容选项
   * @returns {Promise<Object>} 生成的内容
   */
  async generateContent(options = {}) {
    if (!options.product) {
      throw new Error('必须提供产品信息');
    }

    const defaults = {
      type: 'review',
      tone: 'professional',
      length: 'medium',
      language: 'zh-CN'
    };

    const contentOptions = { ...defaults, ...options };
    return await this.contentGenerator.generate(contentOptions);
  }

  /**
   * 生成产品评测
   * @param {Object} product - 产品信息
   * @returns {Promise<string>} 评测文章
   */
  async generateReview(product) {
    return await this.contentGenerator.generateReview(product);
  }

  /**
   * 生成社交媒体帖子
   * @param {Object} product - 产品信息
   * @param {Array} platforms - 平台列表
   * @returns {Promise<Array>} 社交媒体帖子
   */
  async generateSocialPosts(product, platforms = ['twitter']) {
    return await this.contentGenerator.generateSocialPosts(product, platforms);
  }

  /**
   * 创建追踪链接
   * @param {Object} options - 链接选项
   * @returns {Promise<Object>} 追踪链接信息
   */
  async createTrackingLink(options = {}) {
    if (!options.productUrl) {
      throw new Error('必须提供产品 URL');
    }

    return await this.linkTracker.create(options);
  }

  /**
   * 获取链接统计
   * @param {string} linkId - 链接 ID
   * @returns {Promise<Object>} 统计信息
   */
  async getLinkStats(linkId) {
    return await this.linkTracker.getStats(linkId);
  }

  /**
   * 获取所有链接统计
   * @returns {Promise<Array>} 链接统计列表
   */
  async getAllLinkStats() {
    return await this.linkTracker.getAllStats();
  }

  /**
   * 获取收入报告
   * @param {Object} options - 报告选项
   * @returns {Promise<Object>} 收入报告
   */
  async getRevenueReport(options = {}) {
    const defaults = {
      startDate: this._getLastMonth(),
      endDate: this._getToday(),
      groupBy: 'product'
    };

    const reportOptions = { ...defaults, ...options };
    return await this.analytics.getReport(reportOptions);
  }

  /**
   * 导出报告
   * @param {Object} report - 报告对象
   * @param {Object} options - 导出选项
   * @returns {Promise<string>} 导出文件路径
   */
  async exportReport(report, options = {}) {
    return await this.analytics.export(report, options);
  }

  /**
   * 获取收入预测
   * @param {number} months - 预测月数
   * @returns {Promise<Object>} 预测结果
   */
  async getPredictions(months = 3) {
    return await this.analytics.predict(months);
  }

  /**
   * 设置自动化工作流
   * @param {Object} config - 自动化配置
   * @returns {Promise<Object>} 自动化任务信息
   */
  async setupAutomation(config) {
    return await this._createAutomation(config);
  }

  /**
   * 获取技能状态
   * @returns {Object} 状态信息
   */
  getStatus() {
    return {
      configured: !!this.config,
      platforms: this.config ? Object.keys(this.config.platforms) : [],
      version: '1.0.0',
      features: {
        productFinder: true,
        contentGenerator: true,
        linkTracker: true,
        analytics: true
      }
    };
  }

  // 辅助方法
  _getToday() {
    return new Date().toISOString().split('T')[0];
  }

  _getLastMonth() {
    const date = new Date();
    date.setMonth(date.getMonth() - 1);
    return date.toISOString().split('T')[0];
  }

  async _createAutomation(config) {
    // 简化实现 - 实际应使用定时任务系统
    console.log('⏰ 自动化任务已设置:', config.schedule);
    return {
      id: `auto_${Date.now()}`,
      schedule: config.schedule,
      tasks: config.tasks,
      status: 'active',
      nextRun: this._getNextRun(config.schedule)
    };
  }

  _getNextRun(schedule) {
    const now = new Date();
    if (schedule === 'daily') {
      now.setDate(now.getDate() + 1);
      now.setHours(9, 0, 0, 0);
    } else if (schedule === 'weekly') {
      now.setDate(now.getDate() + 7);
      now.setHours(9, 0, 0, 0);
    }
    return now.toISOString();
  }
}

// 导出技能实例
export default new AffiliateMarketingAuto();
