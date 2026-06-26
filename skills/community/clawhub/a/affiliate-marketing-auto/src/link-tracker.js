/**
 * 链接追踪模块
 * 
 * 功能：
 * - 短链生成
 * - UTM 参数管理
 * - 点击率追踪
 * - 转化率监控
 * - A/B 测试
 */

class LinkTracker {
  constructor() {
    this.links = new Map();
    this.stats = new Map();
    this.config = null;
  }

  /**
   * 初始化配置
   * @param {Object} config - 配置对象
   */
  async initialize(config) {
    this.config = config.tracking || {};
    console.log('🔗 链接追踪模块已初始化');
  }

  /**
   * 创建追踪链接
   * @param {Object} options - 链接选项
   * @returns {Promise<Object>} 追踪链接信息
   */
  async create(options) {
    const {
      productUrl,
      campaign,
      source,
      medium,
      content,
      term
    } = options;

    // 生成唯一 ID
    const linkId = `link_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    // 构建 UTM 参数
    const utmParams = this._buildUTMParams({ campaign, source, medium, content, term });
    
    // 生成完整追踪 URL
    const trackingUrl = this._appendParams(productUrl, utmParams);
    
    // 生成短链（简化实现）
    const shortUrl = this._generateShortUrl(linkId);

    const linkData = {
      id: linkId,
      originalUrl: productUrl,
      trackingUrl: trackingUrl,
      shortUrl: shortUrl,
      utmParams: utmParams,
      campaign: campaign || 'default',
      source: source || 'unknown',
      medium: medium || 'organic',
      content: content || '',
      term: term || '',
      createdAt: new Date().toISOString(),
      status: 'active',
      clicks: 0,
      conversions: 0,
      revenue: 0
    };

    // 存储链接
    this.links.set(linkId, linkData);
    
    // 初始化统计数据
    this.stats.set(linkId, {
      clicks: [],
      conversions: [],
      referrers: {},
      devices: {},
      locations: {},
      hourlyStats: {}
    });

    console.log(`✅ 创建追踪链接：${shortUrl}`);
    return linkData;
  }

  /**
   * 获取链接统计
   * @param {string} linkId - 链接 ID
   * @returns {Promise<Object>} 统计信息
   */
  async getStats(linkId) {
    const link = this.links.get(linkId);
    const stats = this.stats.get(linkId);

    if (!link) {
      throw new Error(`链接不存在：${linkId}`);
    }

    const linkStats = this.stats.get(linkId) || {
      clicks: [],
      conversions: []
    };

    return {
      linkId: link.id,
      originalUrl: link.originalUrl,
      trackingUrl: link.trackingUrl,
      shortUrl: link.shortUrl,
      campaign: link.campaign,
      createdAt: link.createdAt,
      status: link.status,
      performance: {
        totalClicks: linkStats.clicks.length,
        uniqueClicks: this._countUnique(linkStats.clicks),
        totalConversions: linkStats.conversions.length,
        conversionRate: this._calculateConversionRate(linkStats),
        totalRevenue: link.revenue,
        averageOrderValue: this._calculateAOV(linkStats.conversions)
      },
      traffic: {
        byReferrer: linkStats.referrers,
        byDevice: linkStats.devices,
        byLocation: linkStats.locations
      },
      trends: {
        hourly: linkStats.hourlyStats,
        daily: this._aggregateDaily(linkStats.clicks)
      }
    };
  }

  /**
   * 获取所有链接统计
   * @returns {Promise<Array>} 链接统计列表
   */
  async getAllStats() {
    const allStats = [];
    
    for (const linkId of this.links.keys()) {
      const stats = await this.getStats(linkId);
      allStats.push(stats);
    }

    return allStats.sort((a, b) => 
      b.performance.totalClicks - a.performance.totalClicks
    );
  }

  /**
   * 记录点击
   * @param {string} linkId - 链接 ID
   * @param {Object} clickData - 点击数据
   */
  async recordClick(linkId, clickData = {}) {
    const stats = this.stats.get(linkId);
    if (!stats) return;

    const click = {
      timestamp: Date.now(),
      ip: clickData.ip || 'unknown',
      userAgent: clickData.userAgent || 'unknown',
      referrer: clickData.referrer || 'direct',
      device: this._detectDevice(clickData.userAgent),
      location: clickData.location || 'unknown',
      ...clickData
    };

    stats.clicks.push(click);
    
    // 更新引用来源统计
    stats.referrers[click.referrer] = (stats.referrers[click.referrer] || 0) + 1;
    
    // 更新设备统计
    stats.devices[click.device] = (stats.devices[click.device] || 0) + 1;
    
    // 更新位置统计
    stats.locations[click.location] = (stats.locations[click.location] || 0) + 1;
    
    // 更新小时统计
    const hour = new Date(click.timestamp).getHours();
    stats.hourlyStats[hour] = (stats.hourlyStats[hour] || 0) + 1;

    // 更新链接点击数
    const link = this.links.get(linkId);
    if (link) {
      link.clicks++;
    }
  }

  /**
   * 记录转化
   * @param {string} linkId - 链接 ID
   * @param {Object} conversionData - 转化数据
   */
  async recordConversion(linkId, conversionData = {}) {
    const stats = this.stats.get(linkId);
    if (!stats) return;

    const conversion = {
      timestamp: Date.now(),
      revenue: conversionData.revenue || 0,
      orderId: conversionData.orderId || `order_${Date.now()}`,
      productId: conversionData.productId,
      ...conversionData
    };

    stats.conversions.push(conversion);

    // 更新链接转化数和收入
    const link = this.links.get(linkId);
    if (link) {
      link.conversions++;
      link.revenue += conversion.revenue;
    }
  }

  /**
   * 更新链接
   * @param {string} linkId - 链接 ID
   * @param {Object} updates - 更新内容
   * @returns {Promise<Object>} 更新后的链接
   */
  async update(linkId, updates) {
    const link = this.links.get(linkId);
    if (!link) {
      throw new Error(`链接不存在：${linkId}`);
    }

    Object.assign(link, updates);
    this.links.set(linkId, link);

    console.log(`✅ 更新链接：${linkId}`);
    return link;
  }

  /**
   * 删除链接
   * @param {string} linkId - 链接 ID
   * @returns {Promise<boolean>} 是否成功删除
   */
  async delete(linkId) {
    const deleted = this.links.delete(linkId);
    this.stats.delete(linkId);
    
    if (deleted) {
      console.log(`🗑️  删除链接：${linkId}`);
    }
    
    return deleted;
  }

  /**
   * 创建 A/B 测试
   * @param {Object} options - 测试选项
   * @returns {Promise<Object>} A/B 测试信息
   */
  async createABTest(options) {
    const { variants, trafficSplit = 50 } = options;
    
    const testId = `ab_${Date.now()}`;
    const variants_ = variants.map((variant, index) => ({
      id: `variant_${index}`,
      url: variant.url,
      name: variant.name || `Variant ${index}`,
      clicks: 0,
      conversions: 0
    }));

    const abTest = {
      id: testId,
      variants: variants_,
      trafficSplit,
      status: 'active',
      createdAt: new Date().toISOString(),
      winner: null
    };

    console.log(`🧪 创建 A/B 测试：${testId}`);
    return abTest;
  }

  /**
   * 分析 A/B 测试结果
   * @param {string} testId - 测试 ID
   * @returns {Promise<Object>} 测试结果
   */
  async analyzeABTest(testId) {
    // 简化实现
    return {
      testId,
      status: 'running',
      variants: [],
      recommendation: '继续测试'
    };
  }

  // 辅助方法
  _buildUTMParams({ campaign, source, medium, content, term }) {
    const params = {};
    if (campaign) params.utm_campaign = campaign;
    if (source) params.utm_source = source;
    if (medium) params.utm_medium = medium;
    if (content) params.utm_content = content;
    if (term) params.utm_term = term;
    return params;
  }

  _appendParams(url, params) {
    const urlObj = new URL(url);
    Object.entries(params).forEach(([key, value]) => {
      urlObj.searchParams.set(key, value);
    });
    return urlObj.toString();
  }

  _generateShortUrl(linkId) {
    // 简化实现 - 实际应使用短链服务
    return `https://short.link/${linkId}`;
  }

  _countUnique(clicks) {
    const uniqueIPs = new Set(clicks.map(c => c.ip));
    return uniqueIPs.size;
  }

  _calculateConversionRate(stats) {
    if (stats.clicks.length === 0) return 0;
    return ((stats.conversions.length / stats.clicks.length) * 100).toFixed(2);
  }

  _calculateAOV(conversions) {
    if (conversions.length === 0) return 0;
    const total = conversions.reduce((sum, c) => sum + (c.revenue || 0), 0);
    return (total / conversions.length).toFixed(2);
  }

  _detectDevice(userAgent) {
    if (!userAgent) return 'unknown';
    const ua = userAgent.toLowerCase();
    if (/mobile/i.test(ua)) return 'mobile';
    if (/tablet/i.test(ua)) return 'tablet';
    return 'desktop';
  }

  _aggregateDaily(clicks) {
    const daily = {};
    clicks.forEach(click => {
      const date = new Date(click.timestamp).toISOString().split('T')[0];
      daily[date] = (daily[date] || 0) + 1;
    });
    return daily;
  }
}

export default LinkTracker;
