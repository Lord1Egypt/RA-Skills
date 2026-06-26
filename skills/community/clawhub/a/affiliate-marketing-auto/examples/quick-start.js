/**
 * Affiliate-Marketing-Auto 快速开始示例
 * 
 * 这个示例展示如何使用技能完成完整的联盟营销流程
 */

import affiliate from '../src/index.js';

async function quickStart() {
  console.log('🚀 Affiliate-Marketing-Auto 快速开始\n');
  console.log('═══════════════════════════════════════\n');

  // 步骤 1: 配置
  console.log('📋 步骤 1: 配置联盟平台\n');
  await affiliate.configure({
    platforms: {
      amazon: {
        apiKey: 'your-amazon-api-key',
        associateTag: 'your-tag-20'
      }
    }
  });
  console.log('✅ 配置完成\n');

  // 步骤 2: 发现高佣金产品
  console.log('🔍 步骤 2: 发现高佣金产品\n');
  const products = await affiliate.findProducts({
    category: 'electronics',
    minCommissionRate: 0.10,
    minPrice: 100,
    maxResults: 5
  });

  console.log(`找到 ${products.length} 个高佣金产品:\n`);
  products.forEach((product, index) => {
    console.log(`${index + 1}. ${product.name}`);
    console.log(`   价格：$${product.price}`);
    console.log(`   佣金：${(product.commissionRate * 100).toFixed(1)}% ($${product.commission})`);
    console.log(`   评分：${product.rating}⭐\n`);
  });

  // 步骤 3: 生成推广内容
  console.log('✍️  步骤 3: 生成推广内容\n');
  const topProduct = products[0];

  // 生成评测文章
  const review = await affiliate.generateContent({
    type: 'review',
    product: topProduct,
    tone: 'professional',
    length: 'medium'
  });

  console.log(`📝 评测文章标题：${review.title}\n`);
  console.log(`SEO 关键词：${review.seoKeywords.join(', ')}\n`);

  // 生成社交媒体帖子
  const socialPosts = await affiliate.generateContent({
    type: 'social',
    product: topProduct,
    platforms: ['twitter', 'xiaohongshu', 'weibo']
  });

  console.log('📱 社交媒体帖子:\n');
  socialPosts.forEach(post => {
    console.log(`【${post.platform}】`);
    console.log(`${post.content.substring(0, 100)}...\n`);
  });

  // 步骤 4: 创建追踪链接
  console.log('🔗 步骤 4: 创建追踪链接\n');
  const trackingLink = await affiliate.createTrackingLink({
    productUrl: topProduct.url,
    campaign: 'spring-promotion',
    source: 'social-media',
    medium: 'organic'
  });

  console.log(`原始链接：${trackingLink.originalUrl}`);
  console.log(`追踪链接：${trackingLink.trackingUrl}`);
  console.log(`短链接：${trackingLink.shortUrl}\n`);

  // 步骤 5: 模拟点击和转化
  console.log('📊 步骤 5: 模拟数据追踪\n');
  
  // 记录一些点击
  for (let i = 0; i < 10; i++) {
    await affiliate.linkTracker.recordClick(trackingLink.id, {
      ip: `192.168.1.${i}`,
      userAgent: 'Mozilla/5.0',
      referrer: ['twitter.com', 'xiaohongshu.com', 'direct'][Math.floor(Math.random() * 3)]
    });
  }

  // 记录一些转化
  for (let i = 0; i < 2; i++) {
    await affiliate.linkTracker.recordConversion(trackingLink.id, {
      revenue: topProduct.price,
      orderId: `order_${Date.now()}_${i}`
    });
  }

  // 步骤 6: 查看统计
  console.log('📈 步骤 6: 查看链接统计\n');
  const stats = await affiliate.getLinkStats(trackingLink.id);

  console.log(`点击数：${stats.performance.totalClicks}`);
  console.log(`转化数：${stats.performance.totalConversions}`);
  console.log(`转化率：${stats.performance.conversionRate}%`);
  console.log(`总收入：$${stats.performance.totalRevenue}\n`);

  // 步骤 7: 生成收入报告
  console.log('💰 步骤 7: 生成收入报告\n');
  const report = await affiliate.getRevenueReport({
    startDate: '2024-01-01',
    endDate: '2024-03-31'
  });

  console.log('收入摘要:');
  console.log(`  总收入：$${report.summary.totalRevenue}`);
  console.log(`  总点击：${report.summary.totalClicks}`);
  console.log(`  总转化：${report.summary.totalConversions}`);
  console.log(`  转化率：${report.summary.conversionRate}%`);
  console.log(`  客单价：$${report.summary.averageOrderValue}\n`);

  // 步骤 8: 收入预测
  console.log('🔮 步骤 8: 收入预测\n');
  const predictions = await affiliate.getPredictions(3);

  console.log('未来 3 个月预测:');
  predictions.predictions.forEach(pred => {
    console.log(`  第${pred.month}个月：$${pred.predictedRevenue} (置信度：${(pred.confidence * 100).toFixed(0)}%)`);
  });
  console.log(`\n总预测收入：$${predictions.totalPredicted}`);
  console.log(`月均收入：$${predictions.averageMonthly}\n`);

  // 步骤 9: 导出报告
  console.log('💾 步骤 9: 导出报告\n');
  const exportResult = await affiliate.exportReport(report, {
    format: 'csv',
    path: './exports'
  });

  console.log(`报告已导出：${exportResult.path}`);
  console.log(`文件格式：${exportResult.format}`);
  console.log(`文件大小：${exportResult.size} bytes\n`);

  console.log('═══════════════════════════════════════');
  console.log('✅ 快速开始完成！\n');
  console.log('💡 提示：');
  console.log('   - 使用 analyzeNiche() 发现新的盈利机会');
  console.log('   - 使用 setupAutomation() 设置自动化流程');
  console.log('   - 定期查看 getRevenueReport() 监控收入');
  console.log('   - 使用 exportReport() 导出详细报告\n');
}

// 运行示例
quickStart().catch(console.error);
