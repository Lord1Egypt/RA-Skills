/**
 * 企业级智能客服知识库构建器 v1.0
 * 
 * 功能：
 * - 多意图识别与分类
 * - 话术优化（按行业/语气）
 * - 多轮对话流程设计
 * - 敏感词过滤
 * - 知识覆盖度分析
 * 
 * 定价：¥129/月 | $49.99/月
 * 企业主体：上海冰月网络科技有限公司
 */

class KnowledgeBaseBuilder {

  // ============================================================
  // 行业话术模板
  // ============================================================
  static industryToneGuide = {
    '电商': {
      professional: '亲，感谢您的咨询~ 关于您的问题...',
      friendly: '哈喽！很高兴为您解答哦~',
      formal: '尊敬的客户，您好。关于您的咨询...',
      lively: '哇！这个问题问得太好了！让我来帮你~',
    },
    'SaaS': {
      professional: '您好，关于此功能的使用说明如下...',
      friendly: '你好呀！这个功能很好用的~',
      formal: '尊敬的用户，该功能的技术规范如下...',
      lively: '太棒了！这个功能超实用的！',
    },
    '教育': {
      professional: '同学你好，关于这个问题...',
      friendly: '同学你好呀！这个问题很有意思~',
      formal: '同学您好，根据教学大纲要求...',
      lively: '同学！这个问题问得非常好！',
    },
    '金融': {
      professional: '您好，关于此业务的具体流程...',
      friendly: '您好！很高兴为您介绍~',
      formal: '尊敬的客户，根据相关业务规定...',
      lively: '您好！这个产品很适合您呢~',
    },
    '医疗': {
      professional: '您好，关于此症状的建议如下...',
      friendly: '您好！别担心，我来帮您看看~',
      formal: '尊敬的患者，根据临床指南...',
      lively: '您好！这个问题很常见，不用担心~',
    },
    '通用': {
      professional: '您好，关于您的问题...',
      friendly: '你好呀！很高兴为你解答~',
      formal: '尊敬的客户，您好...',
      lively: '你好！这个问题很好！',
    },
  };

  // ============================================================
  // 意图分类体系
  // ============================================================
  static intentTaxonomy = {
    '产品咨询': {
      sub: ['功能介绍', '规格参数', '价格询问', '版本对比', '兼容性'],
      keywords: ['什么功能', '怎么用', '多少钱', '有什么区别', '支持', '兼容', '规格', '参数'],
    },
    '售后服务': {
      sub: ['退换货', '维修', '保修期', '发票', '物流查询'],
      keywords: ['退货', '换货', '维修', '保修', '发票', '物流', '快递', '多久到'],
    },
    '技术支持': {
      sub: ['安装指导', '故障排查', '升级更新', '配置问题', '兼容性'],
      keywords: ['安装', '故障', '报错', '升级', '配置', '连接不上', '打不开'],
    },
    '账户管理': {
      sub: ['注册登录', '密码找回', '账户安全', '信息修改', '注销'],
      keywords: ['注册', '登录', '密码', '账号', '修改信息', '注销', '安全'],
    },
    '投诉建议': {
      sub: ['服务投诉', '产品质量', '改进建议', '表扬'],
      keywords: ['投诉', '不满意', '差评', '建议', '太差', '态度', '举报'],
    },
    '订单相关': {
      sub: ['下单咨询', '订单修改', '取消订单', '订单查询', '支付问题'],
      keywords: ['下单', '修改订单', '取消', '查订单', '支付', '付款', '没收到'],
    },
    '政策法规': {
      sub: ['隐私政策', '用户协议', '退款政策', '使用条款'],
      keywords: ['隐私', '协议', '政策', '条款', '规定', '法律'],
    },
  };

  // ============================================================
  // 敏感词库
  // ============================================================
  static sensitiveWords = {
    '绝对化用语': ['最好', '第一', '最强', '100%', '绝对', '唯一', '包治', '根治'],
    '承诺风险': ['保证赚钱', '稳赚', '无风险', '必过', '一定', '承诺'],
    '竞品攻击': ['比 XX 好', 'XX 不行', '垃圾', '骗子', '黑心'],
    '违规内容': ['返现', '刷单', '好评返现', '虚假', '伪造'],
    '隐私风险': ['身份证号', '银行卡号', '密码', '验证码'],
  };

  // ============================================================
  // FAQ 模板库（按行业）
  // ============================================================
  static faqTemplates = {
    '电商': [
      { q: '发货后多久能收到？', a: '一般发货后 2-5 个工作日送达，偏远地区可能需要 5-7 天。您可以在"我的订单"中查看物流信息。' },
      { q: '支持哪些支付方式？', a: '我们支持支付宝、微信支付、银行卡、花呗等多种支付方式。' },
      { q: '退换货政策是什么？', a: '我们支持 7 天无理由退换货。商品签收后 7 天内，如不影响二次销售，可申请退换货。退货运费由买家承担。' },
      { q: '如何开具发票？', a: '订单完成后，可在"我的订单"中申请开具发票。支持增值税普通发票和专用发票。' },
    ],
    'SaaS': [
      { q: '免费版和付费版有什么区别？', a: '免费版包含基础功能，适合个人使用。付费版解锁高级功能、团队协作和优先客服支持。具体对比请查看定价页面。' },
      { q: '数据安全如何保障？', a: '我们采用银行级加密技术，数据存储在通过 ISO 27001 认证的数据中心。同时提供数据备份和导出功能。' },
      { q: '如何升级到高级版本？', a: '在账户设置中点击"升级"，选择适合的套餐并完成支付即可即时升级。' },
      { q: '支持哪些第三方集成？', a: '目前已支持 Slack、飞书、企业微信、钉钉、Jira、GitHub 等 50+ 主流工具的集成。' },
    ],
    '教育': [
      { q: '课程有效期是多久？', a: '课程购买后有效期为 1 年，有效期内可无限次观看。部分课程提供永久有效选项。' },
      { q: '可以退款吗？', a: '购买后 7 天内如观看进度不超过 10%，可申请全额退款。超过 7 天或观看进度超过 10% 则不支持退款。' },
      { q: '有老师答疑吗？', a: '是的！我们提供社群答疑和专属助教服务。工作日 9:00-18:00 有老师在线答疑。' },
    ],
    '金融': [
      { q: '资金安全如何保障？', a: '您的资金由银行存管，我们采用银行级加密技术保障交易安全。所有操作均有记录可查。' },
      { q: '提现需要多久？', a: '一般 1-3 个工作日到账，具体取决于银行处理速度。工作日 15:00 前提现当天到账。' },
      { q: '利率是如何计算的？', a: '利率根据产品类型和市场情况确定，具体请查看产品详情页。所有收益均为年化收益率。' },
    ],
    '通用': [
      { q: '如何联系客服？', a: '您可以通过在线客服、电话（400-XXX-XXXX）、邮件（support@example.com）联系我们。工作日 9:00-18:00 提供人工服务。' },
      { q: '你们的营业时间是什么？', a: '在线客服服务时间为每天 9:00-22:00，电话服务为工作日 9:00-18:00。非工作时间可通过邮件联系。' },
      { q: '如何投诉或提建议？', a: '感谢您的反馈！请在"我的"-"意见反馈"中提交，或发送邮件至 feedback@example.com。我们会在 24 小时内回复。' },
    ],
  };

  // ============================================================
  // 主构建函数
  // ============================================================
  static build(params) {
    const {
      raw_content: rawContent = '',
      industry = '通用',
      tone = '专业',
      output_format: outputFormat = 'JSON'
    } = params;

    // 1. 解析原始内容
    const parsed = this.parseContent(rawContent);
    
    // 2. 意图分类
    const intentMap = this.classifyIntents(parsed.entries);
    
    // 3. 话术优化
    const optimizedEntries = this.optimizeTone(parsed.entries, industry, tone);
    
    // 4. 多轮对话设计
    const dialogueFlows = this.designDialogueFlows(optimizedEntries, industry);
    
    // 5. 敏感词检查
    const sensitiveFindings = this.checkSensitiveWords(rawContent, optimizedEntries);
    
    // 6. 覆盖度分析
    const coverage = this.analyzeCoverage(intentMap, industry);

    // 7. 生成输出
    const knowledgeEntries = optimizedEntries.map((entry, i) => ({
      id: i + 1,
      intent: entry.intent,
      subIntent: entry.subIntent,
      question: entry.question,
      answer: entry.answer,
      keywords: entry.keywords,
      scenario: entry.scenario,
      confidence: entry.confidence,
      relatedIntents: entry.relatedIntents || [],
    }));

    return {
      industry,
      tone,
      outputFormat,
      totalEntries: knowledgeEntries.length,
      intentMap,
      knowledgeEntries,
      dialogueFlows,
      coverageAnalysis: coverage,
      sensitiveWords: sensitiveFindings,
      recommendations: this.generateRecommendations(coverage, sensitiveFindings),
      builtAt: new Date().toISOString(),
    };
  }

  // ============================================================
  // 内容解析
  // ============================================================
  static parseContent(rawContent) {
    const entries = [];

    if (!rawContent) {
      // 无输入时，使用行业模板
      const templates = this.faqTemplates['通用'] || [];
      for (const faq of templates) {
        entries.push({
          question: faq.q,
          answer: faq.a,
          intent: '通用',
          subIntent: '通用',
          keywords: this.extractKeywords(faq.q),
          scenario: '通用咨询',
          confidence: 0.8,
        });
      }
      return { entries, source: 'template' };
    }

    // 尝试解析 FAQ 格式（问：... 答：...）
    const faqPattern = /(?:问|Q|问题)[:：]\s*(.+?)(?:答|A|回答)[:：]\s*(.+?)(?=(?:问|Q|问题)|$)/gs;
    let match;
    while ((match = faqPattern.exec(rawContent)) !== null) {
      entries.push({
        question: match[1].trim(),
        answer: match[2].trim(),
        intent: '',
        subIntent: '',
        keywords: this.extractKeywords(match[1]),
        scenario: '',
        confidence: 0.9,
      });
    }

    // 如果没有 FAQ 格式，按行分割
    if (entries.length === 0) {
      const lines = rawContent.split('\n').filter(l => l.trim());
      for (let i = 0; i < lines.length - 1; i += 2) {
        if (lines[i] && lines[i + 1]) {
          entries.push({
            question: lines[i].trim().replace(/^[-•*\d.]+\s*/, ''),
            answer: lines[i + 1].trim().replace(/^[-•*\d.]+\s*/, ''),
            intent: '',
            subIntent: '',
            keywords: this.extractKeywords(lines[i]),
            scenario: '',
            confidence: 0.7,
          });
        }
      }
    }

    // 如果仍然没有，创建单一条目
    if (entries.length === 0 && rawContent.length > 20) {
      entries.push({
        question: '关于产品/服务的常见问题',
        answer: rawContent.substring(0, 1000),
        intent: '通用',
        subIntent: '通用',
        keywords: this.extractKeywords(rawContent),
        scenario: '通用咨询',
        confidence: 0.5,
      });
    }

    return { entries, source: entries.length > 0 ? 'parsed' : 'template' };
  }

  // ============================================================
  // 意图分类
  // ============================================================
  static classifyIntents(entries) {
    const intentMap = {};

    for (const entry of entries) {
      let matchedIntent = '通用';
      let matchedSub = '通用';
      let maxScore = 0;

      for (const [intent, config] of Object.entries(this.intentTaxonomy)) {
        let score = 0;
        for (const kw of config.keywords) {
          if (entry.question.includes(kw) || entry.answer.includes(kw)) {
            score += 1;
          }
        }
        if (score > maxScore) {
          maxScore = score;
          matchedIntent = intent;
          matchedSub = config.sub[0] || '通用';
        }
      }

      entry.intent = matchedIntent;
      entry.subIntent = matchedSub;

      if (!intentMap[matchedIntent]) {
        intentMap[matchedIntent] = {
          count: 0,
          subIntents: {},
          keywords: new Set(),
        };
      }
      intentMap[matchedIntent].count++;
      intentMap[matchedIntent].subIntents[matchedSub] = 
        (intentMap[matchedIntent].subIntents[matchedSub] || 0) + 1;
      
      for (const kw of entry.keywords) {
        intentMap[matchedIntent].keywords.add(kw);
      }
    }

    // Convert Sets to Arrays for serialization
    for (const intent of Object.keys(intentMap)) {
      intentMap[intent].keywords = [...intentMap[intent].keywords];
    }

    return intentMap;
  }

  // ============================================================
  // 话术优化
  // ============================================================
  static optimizeTone(entries, industry, tone) {
    const toneGuide = this.industryToneGuide[industry] || this.industryToneGuide['通用'];
    const opening = toneGuide[tone] || toneGuide['professional'];

    return entries.map(entry => {
      // 优化回答开头
      let optimizedAnswer = entry.answer;
      if (!optimizedAnswer.startsWith(opening.substring(0, 5))) {
        optimizedAnswer = `${opening} ${optimizedAnswer}`;
      }
      
      entry.answer = optimizedAnswer;
      entry.scenario = entry.subIntent;
      entry.relatedIntents = this.findRelatedIntents(entry.intent, entry.question);
      
      return entry;
    });
  }

  // ============================================================
  // 多轮对话设计
  // ============================================================
  static designDialogueFlows(entries, industry) {
    const flows = [];

    // 按意图分组，设计多轮对话
    const intentGroups = {};
    for (const entry of entries) {
      if (!intentGroups[entry.intent]) {
        intentGroups[entry.intent] = [];
      }
      intentGroups[entry.intent].push(entry);
    }

    for (const [intent, groupEntries] of Object.entries(intentGroups)) {
      if (groupEntries.length >= 2) {
        flows.push({
          intent,
          flowName: `${intent}咨询流程`,
          steps: [
            {
              step: 1,
              userSays: groupEntries[0].question,
              botReplies: groupEntries[0].answer,
              nextOptions: groupEntries.slice(1).map(e => e.question.substring(0, 30) + '...'),
            },
          ],
          fallback: '抱歉，我不太理解您的问题。请尝试换个方式描述，或输入"转人工"联系人工客服。',
        });
      }
    }

    return flows;
  }

  // ============================================================
  // 敏感词检查
  // ============================================================
  static checkSensitiveWords(rawContent, entries) {
    const findings = [];
    const allText = rawContent + ' ' + entries.map(e => e.answer).join(' ');

    for (const [category, words] of Object.entries(this.sensitiveWords)) {
      for (const word of words) {
        if (allText.includes(word)) {
          findings.push({
            category,
            word,
            severity: 'HIGH',
            suggestion: `建议在客服话术中避免使用"${word}"，可能引发合规风险`,
          });
        }
      }
    }

    return findings;
  }

  // ============================================================
  // 覆盖度分析
  // ============================================================
  static analyzeCoverage(intentMap, industry) {
    const totalIntents = Object.keys(this.intentTaxonomy).length;
    const coveredIntents = Object.keys(intentMap).filter(k => k !== '通用').length;
    const coveragePercent = Math.round((coveredIntents / totalIntents) * 100);

    const missingIntents = Object.keys(this.intentTaxonomy).filter(
      intent => !intentMap[intent]
    );

    return {
      totalIntents,
      coveredIntents,
      coveragePercent,
      missingIntents,
      suggestion: coveragePercent < 50 
        ? '知识库覆盖度较低，建议补充缺失意图的问答内容'
        : '知识库覆盖度良好，可继续优化已有意图的话术质量',
    };
  }

  // ============================================================
  // 建议生成
  // ============================================================
  static generateRecommendations(coverage, sensitiveFindings) {
    const recommendations = [];

    if (coverage.coveragePercent < 50) {
      recommendations.push({
        type: 'coverage',
        priority: 'HIGH',
        content: `当前仅覆盖 ${coverage.coveragePercent}% 的常见意图，建议补充：${coverage.missingIntents.join('、')}`,
      });
    }

    if (sensitiveFindings.length > 0) {
      recommendations.push({
        type: 'compliance',
        priority: 'HIGH',
        content: `发现 ${sensitiveFindings.length} 个敏感词，建议修改话术以避免合规风险`,
      });
    }

    recommendations.push({
      type: 'optimization',
      priority: 'MEDIUM',
      content: '建议为高频意图设计多轮对话流程，提升用户体验',
    });

    recommendations.push({
      type: 'maintenance',
      priority: 'LOW',
      content: '建议每月更新知识库，根据用户反馈优化话术',
    });

    return recommendations;
  }

  // ============================================================
  // 辅助函数
  // ============================================================
  static extractKeywords(text) {
    const commonWords = ['如何', '怎么', '什么', '为什么', '是否', '能不能', '可以吗', '请问', '请问一下'];
    const keywords = [];
    const segments = text.split(/[\s，。、！？,\.!\?\n]+/);
    
    for (const seg of segments) {
      if (seg.length > 1 && !commonWords.includes(seg)) {
        keywords.push(seg);
      }
    }
    
    return keywords.slice(0, 10);
  }

  static findRelatedIntents(currentIntent, question) {
    const relatedMap = {
      '产品咨询': ['技术支持', '订单相关'],
      '售后服务': ['订单相关', '投诉建议'],
      '技术支持': ['产品咨询', '账户管理'],
      '账户管理': ['技术支持'],
      '投诉建议': ['售后服务'],
      '订单相关': ['售后服务', '产品咨询'],
    };
    return relatedMap[currentIntent] || [];
  }
}

module.exports = KnowledgeBaseBuilder;
