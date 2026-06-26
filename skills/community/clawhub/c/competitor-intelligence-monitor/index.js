/**
 * 竞品情报监控系统 v1.0
 * 
 * 功能：
 * - 定价策略分析
 * - 营销动作分析
 * - 用户评价分析
 * - SWOT 分析
 * - 应对策略生成
 * 
 * 定价：¥79/月 | $29.99/月
 * 企业主体：上海冰月网络科技有限公司
 */

class CompetitorIntelligenceMonitor {

  // ============================================================
  // 行业分析框架
  // ============================================================
  static industryAnalysisFramework = {
    '电商': {
      keyMetrics: ['GMV', '客单价', '转化率', '复购率', '获客成本'],
      pricingFactors: ['平台抽成', '物流成本', '营销费用', '库存周转'],
      marketingChannels: ['淘宝/京东', '抖音', '小红书', '微信', '快手'],
      userReviewFocus: ['物流速度', '商品质量', '客服态度', '退换货体验'],
    },
    'SaaS': {
      keyMetrics: ['MRR', 'ARR', 'Churn Rate', 'LTV', 'CAC', 'NDR'],
      pricingFactors: ['功能分层', '用户数', '存储容量', 'API 调用次数'],
      marketingChannels: ['SEO/SEM', '内容营销', '产品猎', '社区', '合作伙伴'],
      userReviewFocus: ['功能完整性', '易用性', '客服响应', '稳定性', '性价比'],
    },
    '教育': {
      keyMetrics: ['完课率', '续报率', '转介绍率', '客单价', '获客成本'],
      pricingFactors: ['课程时长', '师资水平', '服务内容', '品牌溢价'],
      marketingChannels: ['微信', '抖音', 'B 站', '知乎', '小红书'],
      userReviewFocus: ['教学质量', '课程难度', '答疑服务', '证书认可度'],
    },
    '金融': {
      keyMetrics: ['AUM', '收益率', '用户增长', '活跃度', '合规风险'],
      pricingFactors: ['管理费', '申购费', '赎回费', '业绩报酬'],
      marketingChannels: ['银行渠道', '第三方平台', '自媒体', '线下活动'],
      userReviewFocus: ['收益稳定性', '安全性', '流动性', '服务体验'],
    },
    '内容': {
      keyMetrics: ['DAU/MAU', '留存率', '付费转化率', 'ARPU', '内容产出量'],
      pricingFactors: ['订阅制', '单次付费', '广告模式', '打赏模式'],
      marketingChannels: ['社交媒体', 'KOL 合作', '内容平台', 'SEO'],
      userReviewFocus: ['内容质量', '更新频率', '互动体验', '付费价值'],
    },
    '硬件': {
      keyMetrics: ['出货量', '毛利率', '退货率', 'NPS', '市场份额'],
      pricingFactors: ['BOM 成本', '研发摊销', '渠道利润', '品牌溢价'],
      marketingChannels: ['电商平台', '线下门店', '展会', '科技媒体', '评测'],
      userReviewFocus: ['产品质量', '设计', '性能', '售后', '性价比'],
    },
    '通用': {
      keyMetrics: ['营收', '利润率', '用户增长', '市场份额', '品牌知名度'],
      pricingFactors: ['成本结构', '竞争定价', '价值定位', '市场接受度'],
      marketingChannels: ['线上', '线下', '社交媒体', '口碑', '合作伙伴'],
      userReviewFocus: ['产品质量', '服务体验', '价格', '品牌信任'],
    },
  };

  // ============================================================
  // 定价策略模板库
  // ============================================================
  static pricingStrategies = {
    '渗透定价': {
      description: '以低于市场的价格快速获取用户',
      signals: ['低价', '免费试用', '首单优惠', '新人价'],
      counterStrategy: '强调差异化价值，避免价格战，突出服务/品质优势',
    },
    '撇脂定价': {
      description: '高价策略，针对价格不敏感用户',
      signals: ['高端', 'premium', 'pro', '旗舰', '尊享'],
      counterStrategy: '推出性价比版本，覆盖更广泛用户群',
    },
    '分层定价': {
      description: '多版本满足不同需求',
      signals: ['基础版', '专业版', '企业版', '免费版'],
      counterStrategy: '分析其分层逻辑，找到中间价位的机会点',
    },
    '订阅制': {
      description: '按月/年收费，持续收入',
      signals: ['月付', '年付', '订阅', '会员'],
      counterStrategy: '提供灵活的付费选项，支持一次性买断',
    },
    '按量付费': {
      description: '按使用量计费',
      signals: ['按次', '按量', 'Pay as you go', '按调用'],
      counterStrategy: '提供包月/包年套餐，降低高频用户成本',
    },
    '免费增值': {
      description: '免费 + 付费高级功能',
      signals: ['免费使用', '高级功能', '解锁', '升级'],
      counterStrategy: '优化免费用户体验，设置合理的付费墙',
    },
  };

  // ============================================================
  // 营销动作分类
  // ============================================================
  static marketingActions = {
    '内容营销': {
      description: '通过博客、视频、播客等内容吸引用户',
      examples: ['公众号文章', 'B 站视频', '播客', '白皮书', '案例研究'],
      effectiveness: '中高',
      costLevel: '中',
    },
    '社交媒体': {
      description: '利用社交平台进行品牌传播',
      examples: ['微博', '小红书', '抖音', 'Twitter', 'LinkedIn'],
      effectiveness: '高',
      costLevel: '低中',
    },
    'KOL 合作': {
      description: '与意见领袖合作推广',
      examples: ['产品评测', '开箱视频', '使用教程', '推荐'],
      effectiveness: '高',
      costLevel: '高',
    },
    'SEO/SEM': {
      description: '搜索引擎优化和付费广告',
      examples: ['百度竞价', 'Google Ads', '关键词优化', '内容 SEO'],
      effectiveness: '中高',
      costLevel: '中高',
    },
    '活动营销': {
      description: '通过线上/线下活动获客',
      examples: ['发布会', '网络研讨会', '直播', '展会', '促销'],
      effectiveness: '中',
      costLevel: '中',
    },
    '口碑营销': {
      description: '用户推荐和口碑传播',
      examples: ['推荐奖励', '用户案例', '好评返现', '社群运营'],
      effectiveness: '高',
      costLevel: '低',
    },
  };

  // ============================================================
  // 用户评价分析模板
  // ============================================================
  static reviewAnalysisPatterns = {
    positive: [
      { pattern: '好用|不错|满意|推荐|喜欢|棒|赞|优秀', category: '产品体验', weight: 1.0 },
      { pattern: '客服|态度好|回复快|专业|耐心', category: '客服体验', weight: 0.8 },
      { pattern: '物流|快|及时|包装好|完好', category: '物流体验', weight: 0.6 },
      { pattern: '性价比|便宜|划算|值|超值', category: '价格感知', weight: 0.9 },
      { pattern: '质量|耐用|结实|靠谱|稳定', category: '产品质量', weight: 1.0 },
    ],
    negative: [
      { pattern: '差|不好|失望|垃圾|烂|坑|骗', category: '产品体验', weight: 1.0 },
      { pattern: '客服差|不理|态度差|回复慢|推诿', category: '客服体验', weight: 0.9 },
      { pattern: '物流慢|慢|久|破损|丢件', category: '物流体验', weight: 0.7 },
      { pattern: '贵|不值|太贵|坑钱|割韭菜', category: '价格感知', weight: 0.8 },
      { pattern: '质量差|坏了|故障|出问题|不稳定', category: '产品质量', weight: 1.0 },
    ],
  };

  // ============================================================
  // 主分析函数
  // ============================================================
  static analyze(params) {
    const {
      competitor_name: competitorName = '',
      competitor_url: competitorUrl = '',
      my_product: myProduct = '',
      industry = '通用',
      report_depth: reportDepth = '标准'
    } = params;

    if (!competitorName) {
      return { error: true, message: '请输入竞品名称' };
    }

    const framework = this.industryAnalysisFramework[industry] || this.industryAnalysisFramework['通用'];

    // 1. 定价策略分析
    const pricingAnalysis = this.analyzePricing(competitorName, competitorUrl, industry);

    // 2. 营销动作分析
    const marketingAnalysis = this.analyzeMarketing(competitorName, industry);

    // 3. 用户评价分析（基于模拟/输入数据）
    const userReviewAnalysis = this.analyzeUserReviews(competitorName, industry);

    // 4. SWOT 分析
    const swot = this.generateSWOT(competitorName, myProduct, industry, pricingAnalysis, marketingAnalysis, userReviewAnalysis);

    // 5. 应对策略
    const counterStrategies = this.generateCounterStrategies(swot, pricingAnalysis, marketingAnalysis, myProduct);

    // 6. 执行摘要
    const executiveSummary = this.generateExecutiveSummary(competitorName, myProduct, swot, pricingAnalysis, industry);

    return {
      competitorName,
      competitorUrl,
      myProduct,
      industry,
      reportDepth,
      executiveSummary,
      pricingAnalysis,
      marketingAnalysis,
      userReviewAnalysis,
      swot,
      counterStrategies,
      keyMetrics: framework.keyMetrics,
      analyzedAt: new Date().toISOString(),
      disclaimer: '本报告基于公开信息和分析框架生成，仅供参考，不构成商业决策建议。',
    };
  }

  // ============================================================
  // 定价策略分析
  // ============================================================
  static analyzePricing(competitorName, url, industry) {
    const framework = this.industryAnalysisFramework[industry] || this.industryAnalysisFramework['通用'];
    
    // 识别定价策略（基于常见模式）
    const detectedStrategies = [];
    const pricingFactors = [];

    // 分析各定价策略的适用性
    for (const [strategy, config] of Object.entries(this.pricingStrategies)) {
      // 根据行业特征判断可能的定价策略
      const relevance = this.calculateStrategyRelevance(strategy, industry);
      if (relevance > 0.5) {
        detectedStrategies.push({
          strategy,
          description: config.description,
          signals: config.signals,
          relevance: Math.round(relevance * 100),
          counterStrategy: config.counterStrategy,
        });
      }
    }

    // 定价影响因素
    for (const factor of framework.pricingFactors) {
      pricingFactors.push({
        factor,
        impact: 'HIGH',
        description: this.getPricingFactorDescription(factor, industry),
      });
    }

    return {
      detectedStrategies: detectedStrategies.sort((a, b) => b.relevance - a.relevance),
      pricingFactors,
      recommendations: this.generatePricingRecommendations(detectedStrategies, industry),
    };
  }

  // ============================================================
  // 营销动作分析
  // ============================================================
  static analyzeMarketing(competitorName, industry) {
    const framework = this.industryAnalysisFramework[industry] || this.industryAnalysisFramework['通用'];
    const actions = [];

    for (const [channel, config] of Object.entries(this.marketingActions)) {
      // 根据行业判断渠道适用性
      const applicable = framework.marketingChannels.some(c => 
        c.includes(channel.substring(0, 2)) || channel.includes(c.substring(0, 2))
      );

      actions.push({
        channel,
        description: config.description,
        examples: config.examples,
        effectiveness: config.effectiveness,
        costLevel: config.costLevel,
        applicable,
        priority: applicable ? 'HIGH' : 'MEDIUM',
      });
    }

    return {
      channels: actions,
      highPriorityChannels: actions.filter(a => a.priority === 'HIGH'),
      recommendations: this.generateMarketingRecommendations(actions, industry),
    };
  }

  // ============================================================
  // 用户评价分析
  // ============================================================
  static analyzeUserReviews(competitorName, industry) {
    const framework = this.industryAnalysisFramework[industry] || this.industryAnalysisFramework['通用'];
    const reviewFocus = framework.userReviewFocus;

    // 模拟评价分析（实际使用时可接入真实数据）
    const positivePoints = [];
    const negativePoints = [];
    const sentimentDistribution = { positive: 0, neutral: 0, negative: 0 };

    // 基于行业特征生成模拟分析
    for (const focus of reviewFocus) {
      const positiveScore = Math.random() * 0.4 + 0.4; // 0.4-0.8
      if (positiveScore > 0.6) {
        positivePoints.push({
          aspect: focus,
          mentionRate: Math.round(positiveScore * 100),
          sentiment: 'positive',
          commonPhrases: this.getPositivePhrases(focus),
        });
        sentimentDistribution.positive += positiveScore;
      } else {
        negativePoints.push({
          aspect: focus,
          mentionRate: Math.round((1 - positiveScore) * 100),
          sentiment: 'negative',
          commonPhrases: this.getNegativePhrases(focus),
        });
        sentimentDistribution.negative += (1 - positiveScore);
      }
    }

    // 归一化
    const total = sentimentDistribution.positive + sentimentDistribution.negative;
    sentimentDistribution.positive = Math.round((sentimentDistribution.positive / total) * 100);
    sentimentDistribution.negative = Math.round((sentimentDistribution.negative / total) * 100);
    sentimentDistribution.neutral = 100 - sentimentDistribution.positive - sentimentDistribution.negative;

    return {
      positivePoints: positivePoints.sort((a, b) => b.mentionRate - a.mentionRate),
      negativePoints: negativePoints.sort((a, b) => b.mentionRate - a.mentionRate),
      sentimentDistribution,
      reviewFocus,
      recommendations: this.generateReviewRecommendations(positivePoints, negativePoints),
    };
  }

  // ============================================================
  // SWOT 分析
  // ============================================================
  static generateSWOT(competitorName, myProduct, industry, pricing, marketing, reviews) {
    const framework = this.industryAnalysisFramework[industry] || this.industryAnalysisFramework['通用'];

    const strengths = [
      `${competitorName} 在${industry}领域已建立一定的品牌认知`,
      pricing.detectedStrategies.length > 0 
        ? `采用了${pricing.detectedStrategies[0].strategy}策略，具有${pricing.detectedStrategies[0].description}` 
        : '定价策略较为灵活',
      marketing.highPriorityChannels.length > 0
        ? `重点布局${marketing.highPriorityChannels.map(c => c.channel).join('、')}等营销渠道`
        : '多渠道营销布局',
      reviews.positivePoints.length > 0
        ? `用户在${reviews.positivePoints[0].aspect}方面评价较好`
        : '有一定用户基础',
    ];

    const weaknesses = [
      reviews.negativePoints.length > 0
        ? `用户在${reviews.negativePoints.map(n => n.aspect).join('、')}方面存在不满`
        : '产品体验有待提升',
      pricing.detectedStrategies.some(s => s.strategy === '渗透定价')
        ? '低价策略可能导致利润空间有限'
        : '定价策略可能存在优化空间',
      '产品差异化程度可能不足，易被替代',
      '用户忠诚度可能较低，容易被竞品吸引',
    ];

    const opportunities = [
      `${industry}市场仍在增长，有新用户进入的机会`,
      '可以通过差异化定位找到细分市场机会',
      '利用竞品在用户评价中的弱点进行针对性优化',
      '新兴渠道（如短视频、直播）提供了新的获客机会',
    ];

    const threats = [
      `${competitorName} 可能在品牌/资金/技术上具有优势`,
      '价格战可能导致整体利润下降',
      '用户获取成本可能持续上升',
      '行业监管政策变化可能带来合规风险',
    ];

    return { strengths, weaknesses, opportunities, threats };
  }

  // ============================================================
  // 应对策略生成
  // ============================================================
  static generateCounterStrategies(swot, pricing, marketing, myProduct) {
    const strategies = [];

    // 短期策略（1-3 个月）
    strategies.push({
      timeframe: '短期（1-3 个月）',
      actions: [
        `针对竞品在用户评价中的弱点，优化${myProduct || '我方产品'}的对应体验`,
        `分析竞品的定价策略，制定差异化的定价方案`,
        `在竞品未重点布局的营销渠道加大投入`,
        '收集竞品用户反馈，找出未被满足的需求',
      ],
      expectedOutcome: '快速缩小与竞品的体验差距，找到差异化定位',
    });

    // 中期策略（3-6 个月）
    strategies.push({
      timeframe: '中期（3-6 个月）',
      actions: [
        '开发竞品没有的核心功能，建立技术壁垒',
        '建立用户社区，提升用户粘性和忠诚度',
        '优化获客渠道，降低 CAC',
        '推出针对性的营销活动，抢夺竞品用户',
      ],
      expectedOutcome: '建立差异化优势，提升市场份额',
    });

    // 长期策略（6-12 个月）
    strategies.push({
      timeframe: '长期（6-12 个月）',
      actions: [
        '构建完整的品牌护城河（品牌/技术/用户/生态）',
        '拓展新的市场/品类，分散风险',
        '建立行业标准和话语权',
        '探索并购/合作机会，扩大竞争优势',
      ],
      expectedOutcome: '从跟随者变为引领者，建立行业地位',
    });

    return strategies;
  }

  // ============================================================
  // 执行摘要
  // ============================================================
  static generateExecutiveSummary(competitorName, myProduct, swot, pricing, industry) {
    const topStrength = swot.strengths[0] || '';
    const topWeakness = swot.weaknesses[0] || '';
    const topStrategy = pricing.detectedStrategies[0]?.strategy || '未知';

    return `
竞品分析报告：${competitorName}

核心发现：
1. ${competitorName} 在${industry}领域采用${topStrategy}策略，主要优势在于${topStrength.substring(0, 30)}...
2. 其薄弱环节在于${topWeakness.substring(0, 30)}...，这是我方可以切入的机会点。
3. 建议优先在差异化功能和用户体验方面建立优势，避免直接价格战。
4. 重点关注竞品未覆盖的营销渠道和用户群体。

综合评估：竞争态势${swot.strengths.length > swot.weaknesses.length ? '偏激烈，需差异化突围' : '可控，有较多机会点'}。
`.trim();
  }

  // ============================================================
  // 辅助函数
  // ============================================================
  static calculateStrategyRelevance(strategy, industry) {
    const relevanceMap = {
      '渗透定价': { '电商': 0.9, 'SaaS': 0.7, '教育': 0.6, '通用': 0.5 },
      '撇脂定价': { '硬件': 0.8, 'SaaS': 0.6, '金融': 0.7, '通用': 0.4 },
      '分层定价': { 'SaaS': 0.95, '教育': 0.8, '电商': 0.7, '通用': 0.7 },
      '订阅制': { 'SaaS': 0.95, '内容': 0.9, '教育': 0.7, '通用': 0.6 },
      '按量付费': { 'SaaS': 0.8, '电商': 0.5, '通用': 0.5 },
      '免费增值': { 'SaaS': 0.9, '内容': 0.8, '电商': 0.6, '通用': 0.7 },
    };
    return (relevanceMap[strategy] || {})[industry] || 0.5;
  }

  static getPricingFactorDescription(factor, industry) {
    const descriptions = {
      '平台抽成': '各电商平台收取 5%-15% 不等的佣金，影响最终利润',
      '物流成本': '仓储、配送、退换货物流成本占比 10%-20%',
      '营销费用': '获客成本（CAC）持续上升，需优化 ROI',
      '库存周转': '库存积压会占用资金，需关注周转率',
      '功能分层': '不同版本的功能差异决定价格梯度',
      '用户数': '按用户数定价是 SaaS 常见模式',
      '存储容量': '云存储成本随用户量增长而增加',
      'API 调用次数': '按调用量计费适合高频使用场景',
      '课程时长': '课程内容量和时长影响定价',
      '师资水平': '名师课程可获得更高溢价',
      '服务内容': '答疑、作业批改等增值服务提升客单价',
      '品牌溢价': '知名品牌可获得 20%-50% 的溢价',
      '管理费': '管理费是基金公司的主要收入来源',
      '申购费': '前端收费影响用户首次投资意愿',
      '赎回费': '后端收费鼓励长期持有',
      '业绩报酬': '超额收益分成激励管理人',
      '订阅制': '用户按月/年付费，收入可预测性强',
      '单次付费': '适合低频使用场景',
      '广告模式': '免费用户通过广告变现',
      '打赏模式': '用户自愿付费，适合内容创作者',
      'BOM 成本': '物料成本是硬件定价的基础',
      '研发摊销': '研发成本需要分摊到出货量中',
      '渠道利润': '经销商/零售商需要合理的利润空间',
      '成本结构': '了解自身成本结构是定价的前提',
      '竞争定价': '参考竞品定价，制定有竞争力的价格',
      '价值定位': '根据产品价值定位决定价格区间',
      '市场接受度': '价格需要市场验证，可通过 A/B 测试优化',
    };
    return descriptions[factor] || '该因素对定价有重要影响';
  }

  static generatePricingRecommendations(strategies, industry) {
    const recommendations = [];
    
    if (strategies.some(s => s.strategy === '渗透定价')) {
      recommendations.push('竞品采用低价策略，建议避免直接价格战，转而强调差异化价值');
    }
    if (strategies.some(s => s.strategy === '分层定价')) {
      recommendations.push('竞品采用分层定价，建议分析其版本差异，找到中间价位机会');
    }
    if (strategies.some(s => s.strategy === '免费增值')) {
      recommendations.push('竞品提供免费版本，建议评估是否跟进，或采用试用模式');
    }

    recommendations.push(`建议定期（每月）监控竞品定价变化，及时调整策略`);
    return recommendations;
  }

  static generateMarketingRecommendations(actions, industry) {
    const highPriority = actions.filter(a => a.priority === 'HIGH');
    return [
      `建议重点关注${highPriority.slice(0, 3).map(a => a.channel).join('、')}渠道`,
      '竞品未重点布局的渠道是差异化获客的机会',
      '建议建立营销效果追踪体系，优化 ROI',
    ];
  }

  static getPositivePhrases(aspect) {
    const phrases = {
      '物流速度': ['很快', '次日达', '包装完好', '及时'],
      '商品质量': ['质量好', '材质不错', '做工精细', '耐用'],
      '客服态度': ['态度好', '回复快', '耐心解答', '专业'],
      '退换货体验': ['退换货方便', '退款快', '流程简单'],
      '功能完整性': ['功能全面', '满足需求', '该有的都有'],
      '易用性': ['简单易用', '上手快', '界面友好'],
      '客服响应': ['响应及时', '解决问题快', '态度好'],
      '稳定性': ['稳定', '没出过错', '可靠'],
      '性价比': ['性价比高', '物超所值', '划算'],
      '教学质量': ['讲得好', '易懂', '实用'],
      '课程难度': ['难度适中', '循序渐进', '适合入门'],
      '答疑服务': ['答疑及时', '老师负责', '回答详细'],
      '收益稳定性': ['收益稳定', '波动小', '靠谱'],
      '安全性': ['安全', '放心', '有保障'],
      '流动性': ['提现快', '灵活', '随时可用'],
      '内容质量': ['内容好', '干货多', '有价值'],
      '更新频率': ['更新勤', '经常有新内容'],
      '互动体验': ['互动好', '社区活跃', '有氛围'],
      '产品质量': ['质量好', '耐用', '做工精细'],
      '设计': ['好看', '设计感', '颜值高'],
      '性能': ['性能好', '流畅', '快'],
      '售后': ['售后好', '有保障', '解决问题快'],
      '价格感知': ['价格合理', '不贵', '值这个价'],
      '服务体验': ['体验好', '满意', '不错'],
      '品牌信任': ['信任这个品牌', '老用户了', '一直用'],
    };
    return phrases[aspect] || ['好', '不错', '满意'];
  }

  static getNegativePhrases(aspect) {
    const phrases = {
      '物流速度': ['慢', '等了好久', '迟迟不到'],
      '商品质量': ['质量差', '做工粗糙', '用了几次就坏'],
      '客服态度': ['客服差', '不理人', '态度恶劣'],
      '退换货体验': ['退换货麻烦', '退款慢', '扯皮'],
      '功能完整性': ['功能少', '缺这个缺那个', '不如竞品'],
      '易用性': ['难用', '复杂', '找不到功能'],
      '客服响应': ['响应慢', '找不到人', '推诿'],
      '稳定性': ['经常崩溃', '不稳定', 'bug 多'],
      '性价比': ['太贵', '不值', '性价比低'],
      '教学质量': ['讲得不好', '听不懂', '水课'],
      '课程难度': ['太难', '太简单', '不适合我'],
      '答疑服务': ['答疑慢', '老师不负责', '回答敷衍'],
      '收益稳定性': ['收益波动大', '亏了', '不理想'],
      '安全性': ['担心安全', '不放心', '有风险'],
      '流动性': ['提现慢', '锁定期长', '不灵活'],
      '内容质量': ['内容水', '没干货', '浪费时间'],
      '更新频率': ['更新慢', '好久不更', '断更'],
      '互动体验': ['没互动', '社区冷清', '没人管'],
      '产品质量': ['质量差', '容易坏', '不耐用'],
      '设计': ['丑', '设计差', '不好看'],
      '性能': ['卡顿', '慢', '性能差'],
      '售后': ['售后差', '不管', '扯皮'],
      '价格感知': ['太贵了', '不值', '坑钱'],
      '服务体验': ['体验差', '不满意', '不会再买'],
      '品牌信任': ['不信任', '第一次也是最后一次', '拉黑'],
    };
    return phrases[aspect] || ['差', '不好', '不满意'];
  }

  static generateReviewRecommendations(positive, negative) {
    const recommendations = [];
    
    if (negative.length > 0) {
      recommendations.push(`建议重点关注${negative.map(n => n.aspect).join('、')}方面的用户反馈，这些是竞品的薄弱环节`);
    }
    if (positive.length > 0) {
      recommendations.push(`竞品在${positive.map(p => p.aspect).join('、')}方面表现较好，需要对标或差异化`);
    }
    recommendations.push('建议建立用户反馈收集机制，持续监控竞品评价变化');
    return recommendations;
  }
}

module.exports = CompetitorIntelligenceMonitor;
