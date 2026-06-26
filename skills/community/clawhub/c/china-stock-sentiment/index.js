/**
 * China Stock Sentiment - A 股舆情分析技能
 * 实时监控市场情绪、热点板块、个股舆情
 */

const fs = require('fs');
const path = require('path');

// 情感关键词库
const POSITIVE_WORDS = [
  '上涨', '利好', '突破', '创新高', '增长', '盈利', '超预期', '强势',
  '买入', '推荐', '看好', '机会', '反弹', '拉升', '涨停', '大涨',
  '业绩亮眼', '订单爆满', '产能扩张', '技术突破', '政策支持'
];

const NEGATIVE_WORDS = [
  '下跌', '利空', '暴跌', '跳水', '亏损', '下滑', '预警', '风险',
  '卖出', '谨慎', '看空', '调整', '跌停', '大跌', '崩盘', '暴雷',
  '业绩下滑', '订单减少', '产能过剩', '监管处罚', '负面新闻'
];

/**
 * 分析文本情感
 * @param {string} text - 要分析的文本
 * @returns {object} 情感分析结果 {score: number, sentiment: string}
 */
function analyzeSentiment(text) {
  let score = 0;
  
  POSITIVE_WORDS.forEach(word => {
    if (text.includes(word)) score += 5;
  });
  
  NEGATIVE_WORDS.forEach(word => {
    if (text.includes(word)) score -= 5;
  });
  
  // 归一化到 -100 到 100
  score = Math.max(-100, Math.min(100, score));
  
  let sentiment = '中性';
  if (score > 20) sentiment = '正面';
  if (score > 50) sentiment = '强烈正面';
  if (score < -20) sentiment = '负面';
  if (score < -50) sentiment = '强烈负面';
  
  return { score, sentiment };
}

/**
 * 获取百度热搜股票相关话题
 * @returns {Promise<Array>} 热搜话题列表
 */
async function getBaiduHotStocks() {
  // 调用 baidu-hot-cn 技能
  const { execSync } = require('child_process');
  try {
    const result = execSync('openclaw skill run baidu-hot-cn', { encoding: 'utf8' });
    return parseHotTopics(result);
  } catch (error) {
    console.error('获取百度热搜失败:', error.message);
    return [];
  }
}

/**
 * 解析热搜话题
 */
function parseHotTopics(rawData) {
  // 简化解析逻辑
  return rawData.split('\n')
    .filter(line => line.trim())
    .slice(0, 10)
    .map((line, index) => ({
      rank: index + 1,
      topic: line,
      isStockRelated: line.match(/股 | 票 | 金融 | 财经 | 投资 | 市场/) !== null
    }));
}

/**
 * 生成舆情报告
 * @param {string} stockName - 股票名称
 * @param {Array} newsList - 新闻列表
 * @returns {object} 舆情报告
 */
function generateReport(stockName, newsList) {
  const sentiments = newsList.map(news => analyzeSentiment(news.title + ' ' + (news.content || '')));
  
  const avgScore = sentiments.reduce((sum, s) => sum + s.score, 0) / sentiments.length;
  const positiveCount = sentiments.filter(s => s.score > 0).length;
  const negativeCount = sentiments.filter(s => s.score < 0).length;
  
  return {
    stock: stockName,
    generatedAt: new Date().toISOString(),
    totalNews: newsList.length,
    averageScore: Math.round(avgScore),
    sentiment: avgScore > 20 ? '正面' : avgScore < -20 ? '负面' : '中性',
    positiveCount,
    negativeCount,
    neutralCount: newsList.length - positiveCount - negativeCount,
    summary: generateSummary(avgScore, positiveCount, negativeCount),
    recommendations: generateRecommendations(avgScore)
  };
}

/**
 * 生成摘要
 */
function generateSummary(avgScore, positiveCount, negativeCount) {
  if (avgScore > 50) return '市场情绪强烈正面，利好消息占据主导，投资者信心充足';
  if (avgScore > 20) return '市场情绪偏正面，整体氛围较好，可适当关注';
  if (avgScore > -20) return '市场情绪中性，多空力量相当，建议观望';
  if (avgScore > -50) return '市场情绪偏负面，利空消息较多，需谨慎操作';
  return '市场情绪强烈负面，风险较高，建议规避';
}

/**
 * 生成投资建议
 */
function generateRecommendations(avgScore) {
  const recommendations = [];
  
  if (avgScore > 50) {
    recommendations.push('可考虑逢低买入');
    recommendations.push('关注成交量配合情况');
  } else if (avgScore > 20) {
    recommendations.push('可适度建仓');
    recommendations.push('设置好止损位');
  } else if (avgScore > -20) {
    recommendations.push('保持观望');
    recommendations.push('等待更明确信号');
  } else if (avgScore > -50) {
    recommendations.push('谨慎持仓');
    recommendations.push('考虑减仓避险');
  } else {
    recommendations.push('建议规避风险');
    recommendations.push('等待情绪企稳');
  }
  
  return recommendations;
}

/**
 * 保存报告到文件
 * @param {object} report - 报告对象
 * @param {string} outputPath - 输出路径
 */
function saveReport(report, outputPath) {
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  const markdown = `# ${report.stock} 舆情分析报告

**生成时间**: ${new Date(report.generatedAt).toLocaleString('zh-CN')}

## 📊 情感分析

- **平均情感分**: ${report.averageScore}
- **整体情绪**: ${report.sentiment}
- **新闻总数**: ${report.totalNews}

### 情绪分布
- 😊 正面：${report.positiveCount} 条
- 😐 中性：${report.neutralCount} 条
- 😟 负面：${report.negativeCount} 条

## 📝 摘要

${report.summary}

## 💡 投资建议

${report.recommendations.map(r => `- ${r}`).join('\n')}

---
*报告由 China Stock Sentiment 技能生成*
`;
  
  fs.writeFileSync(outputPath, markdown, 'utf8');
  console.log(`报告已保存至：${outputPath}`);
}

// 导出函数
module.exports = {
  analyzeSentiment,
  getBaiduHotStocks,
  generateReport,
  saveReport
};

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (command === 'analyze' && args[1]) {
    const text = args.slice(1).join(' ');
    const result = analyzeSentiment(text);
    console.log(`情感分析结果：${result.sentiment} (得分：${result.score})`);
  } else if (command === 'report' && args[1]) {
    const stockName = args[1];
    // 模拟新闻数据
    const mockNews = [
      { title: `${stockName}业绩超预期，净利润增长 50%`, content: '公司发布财报...' },
      { title: `${stockName}获得大额订单`, content: '与某知名企业签订合作协议...' },
      { title: `分析师看好${stockName}后市表现`, content: '多家券商给出买入评级...' }
    ];
    
    const report = generateReport(stockName, mockNews);
    const outputPath = path.join(process.cwd(), 'memory', 'stock-sentiment', 'reports', `${stockName}-${Date.now()}.md`);
    saveReport(report, outputPath);
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log('用法:');
    console.log('  node index.js analyze <文本>  - 分析文本情感');
    console.log('  node index.js report <股票名> - 生成股票舆情报告');
  }
}
