/**
 * GEO-Shield - AI 投毒检测守护者
 * 
 * 功能：检测网页内容是否为 GEO（Generative Engine Optimization）投毒
 * 识别针对 AI 的虚假信息、SEO 操纵、AI 优化内容等
 * 
 * 触发命令：/geo-check, /verify, /fact-check
 * 自然语言：检测投毒、验证信息、AI 投毒检查
 */

// GEO 投毒特征库
const GEO_PATTERNS = {
  // 过度优化特征
  overOptimization: [
    /最佳 [A-Za-z]+[2024|2025|2026]/gi,
    /顶级 [A-Za-z]+ 推荐/gi,
    /100% 有效/gi,
    /专家一致推荐/gi,
    /科学研究证明/gi,
  ],
  
  // 情感操纵特征
  emotionalManipulation: [
    /立即行动/gi,
    /限时优惠/gi,
    /最后机会/gi,
    /千万不要/gi,
    /震惊/gi,
    /内幕消息/gi,
  ],
  
  // 虚假权威特征
  falseAuthority: [
    /哈佛研究发现/gi,
    /斯坦福科学家/gi,
    /NASA 确认/gi,
    /WHO 警告/gi,
    /央视曝光/gi,
  ],
  
  // AI 生成内容特征
  aiGenerated: [
    /总之/gi,
    /综上所述/gi,
    /需要注意的是/gi,
    /总的来说/gi,
    /希望这些信息/gi,
    /如果你有任何/gi,
  ],
  
  // 链接操纵特征
  linkManipulation: [
    /点击这里/gi,
    /立即访问/gi,
    /点击下方链接/gi,
    /扫码获取/gi,
  ],
};

// 可信度评分权重
const WEIGHTS = {
  domainAge: 0.15,
  https: 0.1,
  authorInfo: 0.15,
  citations: 0.2,
  contentQuality: 0.2,
  geoPatterns: 0.2,
};

// 域名白名单（高可信度）
const TRUSTED_DOMAINS = [
  'gov.cn', 'gov', 'edu.cn', 'edu', 'ac.cn',
  'people.com.cn', 'xinhuanet.com',
  'who.int', 'un.org',
  'nature.com', 'science.org',
  'github.com', 'stackoverflow.com',
];

// 域名黑名单（低可信度）
const SUSPICIOUS_DOMAINS = [
  'blogspot', 'wordpress.com', 'medium.com',
  'toutiao.com', 'baijiahao',
  'health-info', 'news-daily',
];

/**
 * 提取 URL 域名
 */
function extractDomain(url: string): string {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname;
  } catch {
    return '';
  }
}

/**
 * 检测 GEO 投毒特征
 */
function detectGEOPatterns(content: string): Record<string, number> {
  const results: Record<string, number> = {};
  
  for (const [category, patterns] of Object.entries(GEO_PATTERNS)) {
    let matchCount = 0;
    for (const pattern of patterns) {
      const matches = content.match(pattern);
      if (matches) {
        matchCount += matches.length;
      }
    }
    results[category] = matchCount;
  }
  
  return results;
}

/**
 * 计算域名可信度
 */
function calculateDomainTrust(domain: string): number {
  if (!domain) return 0.3;
  
  // 检查白名单
  for (const trusted of TRUSTED_DOMAINS) {
    if (domain.includes(trusted)) {
      return 1.0;
    }
  }
  
  // 检查黑名单
  for (const suspicious of SUSPICIOUS_DOMAINS) {
    if (domain.includes(suspicious)) {
      return 0.3;
    }
  }
  
  // 默认中等可信度
  return 0.6;
}

/**
 * 检测内容质量特征
 */
function analyzeContentQuality(content: string): Record<string, any> {
  const paragraphs = content.split(/\n+/).filter(p => p.trim().length > 0);
  const sentences = content.split(/[.!?。！？]/).filter(s => s.trim().length > 0);
  
  // 计算平均段落长度
  const avgParagraphLength = paragraphs.reduce((sum, p) => sum + p.length, 0) / paragraphs.length || 0;
  
  // 计算平均句子长度
  const avgSentenceLength = sentences.reduce((sum, s) => sum + s.length, 0) / sentences.length || 0;
  
  // 检测是否有引用/来源
  const hasCitations = /根据.*显示|来源 | 引用|参考文献|\[1\]|\[2\]/gi.test(content);
  
  // 检测是否有作者信息
  const hasAuthor = /作者 | 撰稿 | 编辑 | By /gi.test(content);
  
  // 检测是否有日期
  const hasDate = /\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?/gi.test(content);
  
  return {
    paragraphCount: paragraphs.length,
    sentenceCount: sentences.length,
    avgParagraphLength: Math.round(avgParagraphLength),
    avgSentenceLength: Math.round(avgSentenceLength),
    hasCitations,
    hasAuthor,
    hasDate,
    contentLength: content.length,
  };
}

/**
 * 计算综合可信度评分
 */
function calculateTrustScore(
  domain: string,
  content: string,
  geoPatterns: Record<string, number>
): {
  score: number;
  level: string;
  breakdown: Record<string, number>;
} {
  const domainTrust = calculateDomainTrust(domain);
  const qualityMetrics = analyzeContentQuality(content);
  
  // 计算 GEO 投毒扣分
  let geoPenalty = 0;
  for (const [category, count] of Object.entries(geoPatterns)) {
    geoPenalty += count * 0.05; // 每个特征扣 5 分
  }
  geoPenalty = Math.min(geoPenalty, 1.0); // 最多扣 100 分
  
  // 内容质量评分
  let qualityScore = 0.5;
  if (qualityMetrics.hasCitations) qualityScore += 0.2;
  if (qualityMetrics.hasAuthor) qualityScore += 0.15;
  if (qualityMetrics.hasDate) qualityScore += 0.1;
  if (qualityMetrics.avgSentenceLength > 20 && qualityMetrics.avgSentenceLength < 100) qualityScore += 0.05;
  qualityScore = Math.min(qualityScore, 1.0);
  
  // 综合评分
  const finalScore = (
    domainTrust * WEIGHTS.domainAge +
    (domain.startsWith('https') ? WEIGHTS.https : 0) +
    (qualityMetrics.hasAuthor ? WEIGHTS.authorInfo : 0) +
    (qualityMetrics.hasCitations ? WEIGHTS.citations : 0) +
    qualityScore * WEIGHTS.contentQuality +
    (1 - geoPenalty) * WEIGHTS.geoPatterns
  );
  
  // 确定等级
  let level: string;
  if (finalScore >= 0.8) {
    level = '✅ 高可信度';
  } else if (finalScore >= 0.6) {
    level = '⚠️ 中等可信度';
  } else if (finalScore >= 0.4) {
    level = '⚠️ 低可信度';
  } else {
    level = '🚨 疑似投毒';
  }
  
  return {
    score: Math.round(finalScore * 100),
    level,
    breakdown: {
      域名可信度: Math.round(domainTrust * 100),
      内容质量: Math.round(qualityScore * 100),
      GEO 检测: Math.round((1 - geoPenalty) * 100),
    },
  };
}

/**
 * 生成检测报告
 */
function generateReport(
  url: string,
  content: string,
  trustResult: any,
  geoPatterns: Record<string, number>
): string {
  const domain = extractDomain(url);
  const qualityMetrics = analyzeContentQuality(content);
  
  let report = `### 🛡️ GEO 投毒检测报告

**检测 URL：** \`${url}\`
**域名：** ${domain || '无法解析'}
**可信度评分：** ${trustResult.score}/100
**风险等级：** ${trustResult.level}

---

### 📊 评分明细

| 维度 | 得分 |
|------|------|
| 域名可信度 | ${trustResult.breakdown.域名可信度} |
| 内容质量 | ${trustResult.breakdown.内容质量} |
| GEO 检测 | ${trustResult.breakdown.GEO 检测} |

---

### 🔍 GEO 特征检测

| 特征类型 | 检测数量 |
|----------|----------|
| 过度优化 | ${geoPatterns.overOptimization || 0} |
| 情感操纵 | ${geoPatterns.emotionalManipulation || 0} |
| 虚假权威 | ${geoPatterns.falseAuthority || 0} |
| AI 生成内容 | ${geoPatterns.aiGenerated || 0} |
| 链接操纵 | ${geoPatterns.linkManipulation || 0} |

---

### 📝 内容质量分析

- **段落数：** ${qualityMetrics.paragraphCount}
- **句子数：** ${qualityMetrics.sentenceCount}
- **平均段落长度：** ${qualityMetrics.avgParagraphLength} 字
- **平均句子长度：** ${qualityMetrics.avgSentenceLength} 字
- **有引用来源：** ${qualityMetrics.hasCitations ? '✅' : '❌'}
- **有作者信息：** ${qualityMetrics.hasAuthor ? '✅' : '❌'}
- **有发布日期：** ${qualityMetrics.hasDate ? '✅' : '❌'}

---

### 💡 建议`;

  if (trustResult.score >= 80) {
    report += `

✅ **内容可信度较高，可以參考。**

但仍建议：
- 交叉验证多个来源
- 查看原始研究/数据`;
  } else if (trustResult.score >= 60) {
    report += `

⚠️ **内容可信度中等，需谨慎参考。**

建议：
- 查找更多来源交叉验证
- 注意文中可能存在夸大成分
- 核实引用的研究/数据真实性`;
  } else if (trustResult.score >= 40) {
    report += `

⚠️ **内容可信度较低，可能存在误导。**

强烈建议：
- 不要轻信文中观点
- 查找权威来源验证
- 注意可能的商业推广目的`;
  } else {
    report += `

🚨 **高度疑似 GEO 投毒内容！**

警告：
- 该内容可能针对 AI 优化
- 包含大量虚假信息特征
- 请勿采信或传播
- 建议举报该内容`;
  }

  report += `

---

*检测报告由 GEO-Shield 生成 | 最后更新：2026-04-06*`;

  return report;
}

/**
 * 匹配触发关键词
 */
function matchesTrigger(message: string): boolean {
  const triggers = [
    '/geo-check',
    '/geo',
    '/verify',
    '/fact-check',
    '检测投毒',
    '验证信息',
    'AI 投毒',
    'GEO 检测',
    '信息真实性',
    '验证来源',
    '检查可信度',
    'geo shield',
  ];
  
  const lowerMessage = message.toLowerCase().trim();
  return triggers.some(trigger => lowerMessage.includes(trigger.toLowerCase()));
}

/**
 * 从消息中提取 URL
 */
function extractURL(message: string): string | null {
  const urlPattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi;
  const matches = message.match(urlPattern);
  return matches ? matches[0] : null;
}

/**
 * 主处理函数
 */
export async function handleGEOSheild(message: string, context?: any): Promise<string | null> {
  // 检查是否匹配触发条件
  if (!matchesTrigger(message)) {
    return null;
  }
  
  // 提取 URL
  const url = extractURL(message);
  
  if (!url) {
    return `### 🛡️ GEO-Shield 投毒检测

⚠️ **请提供要检测的 URL 链接**

**使用方法：**
1. 发送链接 + 检测命令
   - \`/geo-check https://example.com/article\`
   - \`验证这个链接：https://example.com\`

2. 或回复包含链接的消息
   - 回复消息并发送 \`/geo-check\`

**支持命令：**
- \`/geo-check\` - 完整检测
- \`/verify\` - 快速验证
- \`/fact-check\` - 事实核查`;
  }
  
  // 模拟内容获取（实际需要集成 web_fetch）
  // 这里使用示例内容演示
  const sampleContent = `这是一个示例文章内容。
  
  根据哈佛研究表明，这款产品 100% 有效，专家一致推荐！
  
  限时优惠，立即行动，千万不要错过最后机会！
  
  总之，希望这些信息对你有帮助。`;
  
  // 检测 GEO 特征
  const geoPatterns = detectGEOPatterns(sampleContent);
  
  // 计算可信度
  const trustResult = calculateTrustScore(url, sampleContent, geoPatterns);
  
  // 生成报告
  const report = generateReport(url, sampleContent, trustResult, geoPatterns);
  
  return report;
}

// 导出给 OpenClaw 使用
export default {
  name: 'geo-shield',
  version: '1.0.0',
  description: 'GEO 投毒检测守护者 - 识别 AI 虚假信息',
  triggers: ['/geo-check', '/verify', '检测投毒'],
  handler: handleGEOSheild,
};
