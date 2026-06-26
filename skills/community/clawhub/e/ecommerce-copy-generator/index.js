/**
 * Content Generator - 种草内容生成器
 */

class ContentGenerator {
  constructor() {
    this.templates = this.loadTemplates();
  }

  loadTemplates() {
    return {
      'xiaohongshu': {
        name: '小红书',
        style: '种草风',
        templates: [
          {
            name: '测评型',
            structure: ['痛点引入', '产品介绍', '使用体验', '优缺点', '购买建议'],
            tone: '真诚分享'
          },
          {
            name: '清单型',
            structure: ['场景引入', '产品列表', '推荐理由', '总结'],
            tone: '实用干货'
          },
          {
            name: '对比型',
            structure: ['问题提出', '产品对比', '选择建议'],
            tone: '理性分析'
          }
        ]
      },
      'douyin': {
        name: '抖音',
        style: '短视频文案',
        templates: [
          {
            name: '开场钩子',
            pattern: '你们有没有遇到过.../我发现了一个.../绝了！这个...'
          },
          {
            name: '种草话术',
            pattern: '姐妹们冲/真的好用/按头安利/闭眼入'
          }
        ]
      },
      'moments': {
        name: '朋友圈',
        style: '生活分享',
        templates: [
          {
            name: '日常型',
            pattern: '简短真实+表情'
          },
          {
            name: '晒单型',
            pattern: '价格+体验+推荐'
          }
        ]
      }
    };
  }

  /**
   * 生成种草文案
   */
  generate(product, options = {}) {
    const { platform = 'xiaohongshu', style = '测评型', length = 'medium' } = options;
    
    const generator = {
      'xiaohongshu': () => this.generateXiaohongshu(product, style, length),
      'douyin': () => this.generateDouyin(product, length),
      'moments': () => this.generateMoments(product, length),
      'zhihu': () => this.generateZhihu(product, length)
    };
    
    return generator[platform]?.() || generator.xiaohongshu();
  }

  generateXiaohongshu(product, style, length) {
    const { name, category, price, highlights, usage, pros, cons } = product;
    
    const titles = [
      `${price}元的${name}真的值得买吗？真实测评`,
      `被问爆的${category}好物！${name}使用分享`,
      `挖到宝了！${name}真的绝绝子`,
      `${name}使用一个月真实反馈`
    ];
    
    const title = titles[Math.floor(Math.random() * titles.length)];
    
    const content = `${this.generateEmoji()} ${title}

${this.generateHook(product)}

✨ 产品信息
• 名称：${name}
• 价格：¥${price}
• 适合人群：${product.targetAudience || '所有人'}

📝 使用体验
${usage || highlights?.map(h => `• ${h}`).join('\n') || '待补充使用体验'}

✅ 优点
${pros?.map(p => `• ${p}`).join('\n') || '• 性价比高\n• 使用感好'}

❌ 缺点
${cons?.map(c => `• ${c}`).join('\n') || '• 暂时没发现明显缺点'}

💡 购买建议
${this.generateAdvice(product)}

${this.generateHashtags(category)}
`;
    
    return { title, content, platform: '小红书' };
  }

  generateDouyin(product, length) {
    const { name, price, highlights } = product;
    
    const hooks = [
      `姐妹们，我发现了一个${price}块的宝藏${product.category}！`,
      `绝了！这个${name}真的太好用了`,
      `被问爆的${product.category}，今天终于安排上了`
    ];
    
    const scripts = {
      short: `${hooks[0]} ${highlights?.[0] || '真的好用'}，${highlights?.[1] || '强烈推荐'}！`,
      medium: `${hooks[0]}

第一，${highlights?.[0] || '颜值超高'}
第二，${highlights?.[1] || '性价比绝了'}
第三，${highlights?.[2] || '真的好用'}

姐妹们冲就完事了！`,
      long: `【完整脚本待补充】`
    };
    
    return {
      hook: hooks[0],
      script: scripts[length] || scripts.medium,
      platform: '抖音'
    };
  }

  generateMoments(product, length) {
    const { name, price, rating } = product;
    
    const templates = {
      short: `新入的${name}，¥${price}，真香${'👍'.repeat(rating || 3)}`,
      medium: `终于入手了${name}！
用了几天感觉${rating >= 4 ? '真不错' : '还行'}
¥${price}的价格，这个品质${rating >= 4 ? '很值' : '还可以'}
推荐给大家～`,
      long: `【详细朋友圈文案】`
    };
    
    return {
      content: templates[length] || templates.short,
      platform: '朋友圈'
    };
  }

  generateZhihu(product, length) {
    const { name, category, price, highlights, pros, cons } = product;
    const recommend = product.rating >= 4 ? '值得入手' : '建议观望';
    const highlightText = (highlights && highlights.length)
      ? highlights.map(h => `- ${h}`).join('\n')
      : '- 核心卖点需要结合真实使用场景进一步确认';
    const prosText = (pros && pros.length)
      ? pros.map(p => `- ${p}`).join('\n')
      : '- 性价比尚可\n- 使用门槛不高';
    const consText = (cons && cons.length)
      ? cons.map(c => `- ${c}`).join('\n')
      : '- 暂无长期使用数据\n- 是否适合所有人群仍需看个人需求';

    return {
      title: `如何评价${price}元的${name}？值得买吗？`,
      content: `谢邀。\n\n先上结论：${recommend}。\n\n## 一、产品背景\n${name}属于${category}类产品，当前讨论重点通常集中在价格、实际体验和是否值得买。\n\n## 二、核心亮点\n${highlightText}\n\n## 三、优缺点分析\n### 优点\n${prosText}\n\n### 缺点\n${consText}\n\n## 四、适合什么人\n${product.targetAudience || '适合对这类产品有明确需求、且预算在可接受范围内的人群。'}\n\n## 五、购买建议\n如果你更看重${(highlights && highlights[0]) || '核心体验'}，那它是可以考虑的；如果你更在意极致性价比，建议等活动价或先对比同类产品再决定。`,
      platform: '知乎'
    };
  }

  generateHook(product) {
    const hooks = [
      `最近被种草了${product.name}，用了两周来分享一下真实感受。`,
      `作为一个${product.category}重度用户，这个${product.name}真的让我惊喜。`,
      `买之前犹豫了很久，用了之后真香！`
    ];
    return hooks[Math.floor(Math.random() * hooks.length)];
  }

  generateAdvice(product) {
    if (product.rating >= 4.5) {
      return '性价比很高，推荐入手！建议等活动价更划算。';
    } else if (product.rating >= 3.5) {
      return `整体不错，适合${product.targetAudience || '预算有限的朋友'}。`;
    } else {
      return '建议先试用或观望，看看后续口碑。';
    }
  }

  generateHashtags(category) {
    const tags = {
      '美妆': '#好物分享 #美妆测评 #平价好物 #学生党必备',
      '数码': '#数码测评 #好物推荐 #科技数码 #开箱',
      '家居': '#家居好物 #生活好物 #提升幸福感 #居家必备',
      '服装': '#穿搭分享 #ootd #好物推荐 #平价穿搭'
    };
    return tags[category] || '#好物分享 #测评 #推荐';
  }

  generateEmoji() {
    const emojis = ['✨', '🌟', '💫', '🔥', '💯', '🉑'];
    return emojis[Math.floor(Math.random() * emojis.length)];
  }

  /**
   * 批量生成多平台内容
   */
  generateAll(product) {
    return {
      xiaohongshu: this.generate(product, { platform: 'xiaohongshu' }),
      douyin: this.generate(product, { platform: 'douyin', length: 'short' }),
      moments: this.generate(product, { platform: 'moments', length: 'short' }),
      zhihu: this.generate(product, { platform: 'zhihu' })
    };
  }
}

module.exports = { ContentGenerator };
