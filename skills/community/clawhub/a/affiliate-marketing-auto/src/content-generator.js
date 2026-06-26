/**
 * 内容生成模块
 * 
 * 功能：
 * - SEO 产品评测文章
 * - 社交媒体文案
 * - 邮件营销模板
 * - 视频脚本
 */

class ContentGenerator {
  constructor() {
    this.templates = {
      review: this._getReviewTemplate(),
      social: this._getSocialTemplate(),
      email: this._getEmailTemplate(),
      video: this._getVideoTemplate()
    };
  }

  /**
   * 生成内容
   * @param {Object} options - 内容选项
   * @returns {Promise<Object>} 生成的内容
   */
  async generate(options) {
    const { type, product, tone, length, language, platforms } = options;

    console.log(`✍️  生成${type}内容，产品：${product.name}`);

    switch (type) {
      case 'review':
        return await this.generateReview(product, { tone, length, language });
      case 'social':
        return await this.generateSocialPosts(product, platforms);
      case 'email':
        return await this.generateEmail(product, { tone, language });
      case 'video':
        return await this.generateVideoScript(product, { length, language });
      default:
        throw new Error(`不支持的内容类型：${type}`);
    }
  }

  /**
   * 生成产品评测文章
   * @param {Object} product - 产品信息
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 评测文章
   */
  async generateReview(product, options = {}) {
    const { tone = 'professional', length = 'medium', language = 'zh-CN' } = options;

    const wordCounts = { short: 500, medium: 1000, long: 2000 };
    const targetWords = wordCounts[length];

    const review = {
      title: this._generateTitle(product),
      content: this._generateReviewContent(product, tone, targetWords),
      seoKeywords: this._generateSEOKeywords(product),
      metaDescription: this._generateMetaDescription(product),
      headings: this._generateHeadings(product),
      callToAction: this._generateCTA(product),
      wordCount: targetWords,
      language,
      generatedAt: new Date().toISOString()
    };

    console.log(`✅ 生成评测文章：${review.title}`);
    return review;
  }

  /**
   * 生成社交媒体帖子
   * @param {Object} product - 产品信息
   * @param {Array} platforms - 平台列表
   * @returns {Promise<Array>} 社交媒体帖子
   */
  async generateSocialPosts(product, platforms = ['twitter']) {
    const posts = [];

    for (const platform of platforms) {
      const post = this._generatePlatformPost(product, platform);
      posts.push(post);
    }

    console.log(`✅ 生成 ${posts.length} 个社交媒体帖子`);
    return posts;
  }

  /**
   * 生成邮件营销内容
   * @param {Object} product - 产品信息
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 邮件内容
   */
  async generateEmail(product, options = {}) {
    const { tone = 'friendly', language = 'zh-CN' } = options;

    const email = {
      subject: this._generateEmailSubject(product),
      preview: this._generateEmailPreview(product),
      body: this._generateEmailBody(product, tone),
      cta: this._generateCTA(product),
      unsubscribe: this._generateUnsubscribe(),
      language
    };

    console.log(`✅ 生成邮件营销内容`);
    return email;
  }

  /**
   * 生成视频脚本
   * @param {Object} product - 产品信息
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 视频脚本
   */
  async generateVideoScript(product, options = {}) {
    const { length = 'medium', language = 'zh-CN' } = options;

    const durations = { short: 60, medium: 180, long: 300 };
    const duration = durations[length];

    const script = {
      title: this._generateVideoTitle(product),
      hook: this._generateHook(product),
      intro: this._generateVideoIntro(product),
      mainContent: this._generateVideoMain(product),
      conclusion: this._generateVideoConclusion(product),
      cta: this._generateCTA(product),
      duration: duration,
      language
    };

    console.log(`✅ 生成视频脚本（${duration}秒）`);
    return script;
  }

  // 内容生成辅助方法
  _generateTitle(product) {
    const templates = [
      `${product.name} 深度评测：值得购买吗？`,
      `2024 年最佳${product.category}：${product.name} 全面分析`,
      `${product.name} 使用体验：${product.rating}星是否名副其实？`,
      `为什么${product.name}是这个价位的首选`
    ];
    return templates[Math.floor(Math.random() * templates.length)];
  }

  _generateReviewContent(product, tone, wordCount) {
    const sections = [
      `## 产品概述\n\n${product.name}是一款${product.description}。在本文中，我们将深入分析这款产品的优缺点，帮助您做出明智的购买决定。`,
      `## 主要特点\n\n- 高质量材料制造\n- 用户友好设计\n- 出色的性价比\n- ${product.rating}星用户评价`,
      `## 使用体验\n\n经过实际测试，${product.name}在各方面表现优异。特别是在耐用性和功能性方面，超出同价位产品平均水平。`,
      `## 优缺点分析\n\n**优点：**\n- 价格实惠（$${product.price}）\n- 佣金优惠（${(product.commissionRate * 100).toFixed(0)}%返利）\n- 用户评价优秀\n\n**缺点：**\n- 库存可能有限\n- 部分颜色缺货`,
      `## 购买建议\n\n如果您正在寻找一款性价比高的${product.category}，${product.name}绝对值得考虑。特别是现在有${(product.commissionRate * 100).toFixed(0)}%的返利优惠。`,
      `## 总结\n\n综合评分：${product.rating}/5\n推荐指数：⭐⭐⭐⭐⭐\n\n[立即购买](${product.url})`
    ];

    return sections.join('\n\n');
  }

  _generateSEOKeywords(product) {
    return [
      product.name,
      `${product.name} 评测`,
      `${product.category} 推荐`,
      `最佳${product.category}`,
      `${product.name} 价格`,
      `${product.name} 购买`
    ];
  }

  _generateMetaDescription(product) {
    return `${product.name}深度评测，${product.rating}星用户推荐。了解产品特点、价格和购买建议，现在购买享${(product.commissionRate * 100).toFixed(0)}%返利！`;
  }

  _generateHeadings(product) {
    return [
      '产品概述',
      '主要特点',
      '使用体验',
      '优缺点分析',
      '购买建议',
      '总结'
    ];
  }

  _generateCTA(product) {
    return {
      text: `立即查看 ${product.name}`,
      url: product.url,
      urgency: '限时优惠',
      incentive: `购买即享${(product.commissionRate * 100).toFixed(0)}%返利`
    };
  }

  _generatePlatformPost(product, platform) {
    const posts = {
      twitter: {
        platform: 'Twitter',
        content: `🔥 发现好物！${product.name}\n\n⭐ ${product.rating}星好评 | 💰 $${product.price}\n\n${product.description.substring(0, 100)}...\n\n#好物推荐 #${product.category} #购物`,
        hashtags: ['#好物推荐', `#${product.category}`, '#购物', '#优惠'],
        charCount: 280
      },
      xiaohongshu: {
        platform: '小红书',
        title: `💖 ${product.name}真实评测！`,
        content: `姐妹们！今天给大家安利一个超好用的${product.category}！\n\n✨ ${product.name}\n💰 价格：$${product.price}\n⭐ 评分：${product.rating}\n\n使用感受：${product.description}\n\n真心推荐！性价比超高～\n\n#好物分享 #${product.category} #种草 #购物推荐`,
        tags: ['好物分享', product.category, '种草', '购物推荐'],
        imageCount: 3
      },
      weibo: {
        platform: '微博',
        content: `【好物推荐】${product.name} 🌟\n\n价格：$${product.price}\n评分：${product.rating}⭐\n\n${product.description}\n\n点击链接了解更多 👉 ${product.url}\n\n#好物推荐# #${product.category}# #购物#`,
        hashtags: ['#好物推荐#', `#${product.category}#`, '#购物#']
      },
      facebook: {
        platform: 'Facebook',
        content: `🎉 Great Deal Alert! 🎉\n\n${product.name}\n⭐ ${product.rating}/5 stars from ${product.reviews}+ reviews\n💰 Only $${product.price}\n\n${product.description}\n\nShop now: ${product.url}\n\n#Shopping #Deals #${product.category}`,
        hashtags: ['#Shopping', '#Deals', `#${product.category}`]
      },
      instagram: {
        platform: 'Instagram',
        caption: `✨ ${product.name} ✨\n\n💰 $${product.price}\n⭐ ${product.rating}/5\n\n${product.description.substring(0, 150)}...\n\nLink in bio! 🔗\n\n#shopping #deals #${product.category} #musthave`,
        hashtags: ['#shopping', '#deals', `#${product.category}`, '#musthave']
      }
    };

    return posts[platform] || posts.twitter;
  }

  _generateEmailSubject(product) {
    const subjects = [
      `🔥 限时优惠：${product.name} 仅需$${product.price}！`,
      `您不能错过的${product.category}：${product.name}`,
      `${product.name} - ${product.rating}星好评的${product.category}`,
      `特别推荐：${product.name}（内含独家优惠）`
    ];
    return subjects[Math.floor(Math.random() * subjects.length)];
  }

  _generateEmailPreview(product) {
    return `发现${product.name}的超值优惠...`;
  }

  _generateEmailBody(product, tone) {
    return `
亲爱的用户，

我们为您精选了一款优质${product.category}：

🌟 ${product.name}

产品特点：
• ${product.description}
• 用户评分：${product.rating}/5 ⭐
• 价格：$${product.price}

现在购买还可享受额外优惠！

[立即查看](${product.url})

祝您购物愉快！

此致
敬礼
    `.trim();
  }

  _generateUnsubscribe() {
    return '如不想接收此类邮件，请点击退订';
  }

  _generateVideoTitle(product) {
    return `${product.name} 完整评测 - 真的值得买吗？`;
  }

  _generateHook(product) {
    return `你知道吗？${product.category}市场水很深！今天我来帮你避坑，看看这款${product.name}到底值不值得买！`;
  }

  _generateVideoIntro(product) {
    return `大家好，欢迎回到我的频道。今天要评测的是${product.name}，这款产品在${product.category}类别中非常受欢迎。让我们一起来看看它到底怎么样！`;
  }

  _generateVideoMain(product) {
    return `
1. 开箱展示（30 秒）
   - 包装质量
   - 配件清单
   - 第一印象

2. 外观评测（30 秒）
   - 设计美感
   - 做工质量
   - 手感体验

3. 功能测试（60 秒）
   - 核心功能演示
   - 性能测试
   - 对比竞品

4. 优缺点总结（30 秒）
   - 优点列举
   - 缺点说明
   - 适用人群
    `.trim();
  }

  _generateVideoConclusion(product) {
    return `总的来说，${product.name}在$${product.price}这个价位段表现优秀。如果你正在寻找${product.category}，这款产品值得考虑。`;
  }

  // 模板方法（保留扩展性）
  _getReviewTemplate() { return {}; }
  _getSocialTemplate() { return {}; }
  _getEmailTemplate() { return {}; }
  _getVideoTemplate() { return {}; }
}

export default ContentGenerator;
