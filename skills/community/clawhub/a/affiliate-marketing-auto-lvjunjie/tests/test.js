/**
 * Affiliate-Marketing-Auto 技能测试
 */

import affiliate from '../src/index.js';

async function runTests() {
  console.log('🧪 开始运行测试...\n');
  
  let passed = 0;
  let failed = 0;

  try {
    // 测试 1: 配置
    console.log('测试 1: 配置联盟平台...');
    const configResult = await affiliate.configure({
      platforms: {
        amazon: {
          apiKey: 'test-key',
          associateTag: 'test-tag'
        }
      }
    });
    
    if (configResult.success) {
      console.log('✅ 配置测试通过\n');
      passed++;
    } else {
      console.log('❌ 配置测试失败\n');
      failed++;
    }

    // 测试 2: 产品发现
    console.log('测试 2: 发现产品...');
    const products = await affiliate.findProducts({
      category: 'electronics',
      minCommissionRate: 0.05,
      minPrice: 50,
      maxResults: 5
    });
    
    if (products.length > 0) {
      console.log(`✅ 找到 ${products.length} 个产品`);
      console.log(`   示例产品：${products[0].name}`);
      console.log(`   佣金率：${(products[0].commissionRate * 100).toFixed(1)}%\n`);
      passed++;
    } else {
      console.log('❌ 产品发现测试失败\n');
      failed++;
    }

    // 测试 3: 内容生成
    console.log('测试 3: 生成内容...');
    if (products.length > 0) {
      const review = await affiliate.generateContent({
        type: 'review',
        product: products[0],
        tone: 'professional',
        length: 'medium'
      });
      
      if (review.title && review.content) {
        console.log(`✅ 生成评测文章：${review.title}`);
        console.log(`   字数：${review.wordCount}\n`);
        passed++;
      } else {
        console.log('❌ 内容生成测试失败\n');
        failed++;
      }
    }

    // 测试 4: 社交媒体帖子
    console.log('测试 4: 生成社交媒体帖子...');
    if (products.length > 0) {
      const posts = await affiliate.generateContent({
        type: 'social',
        product: products[0],
        platforms: ['twitter', 'xiaohongshu']
      });
      
      if (posts.length > 0) {
        console.log(`✅ 生成 ${posts.length} 个平台帖子`);
        console.log(`   Twitter: ${posts[0].content.substring(0, 50)}...\n`);
        passed++;
      } else {
        console.log('❌ 社交媒体测试失败\n');
        failed++;
      }
    }

    // 测试 5: 创建追踪链接
    console.log('测试 5: 创建追踪链接...');
    if (products.length > 0) {
      const link = await affiliate.createTrackingLink({
        productUrl: products[0].url,
        campaign: 'test-campaign',
        source: 'test'
      });
      
      if (link.id && link.shortUrl) {
        console.log(`✅ 创建追踪链接：${link.shortUrl}`);
        console.log(`   UTM 参数：campaign=${link.utmParams.utm_campaign}\n`);
        passed++;
      } else {
        console.log('❌ 链接追踪测试失败\n');
        failed++;
      }
    }

    // 测试 6: 链接统计
    console.log('测试 6: 获取链接统计...');
    if (products.length > 0) {
      const link = await affiliate.createTrackingLink({
        productUrl: products[0].url,
        campaign: 'stats-test'
      });
      
      // 模拟点击
      await affiliate.linkTracker.recordClick(link.id, {
        ip: '192.168.1.1',
        userAgent: 'Mozilla/5.0',
        referrer: 'twitter.com'
      });
      
      const stats = await affiliate.getLinkStats(link.id);
      
      if (stats.performance) {
        console.log(`✅ 获取链接统计`);
        console.log(`   点击数：${stats.performance.totalClicks}`);
        console.log(`   转化率：${stats.performance.conversionRate}%\n`);
        passed++;
      } else {
        console.log('❌ 链接统计测试失败\n');
        failed++;
      }
    }

    // 测试 7: 收入报告
    console.log('测试 7: 生成收入报告...');
    const report = await affiliate.getRevenueReport({
      startDate: '2024-01-01',
      endDate: '2024-03-31'
    });
    
    if (report.summary && report.revenue) {
      console.log(`✅ 生成收入报告`);
      console.log(`   总收入：$${report.summary.totalRevenue}`);
      console.log(`   转化率：${report.summary.conversionRate}%\n`);
      passed++;
    } else {
      console.log('❌ 收入报告测试失败\n');
      failed++;
    }

    // 测试 8: 收入预测
    console.log('测试 8: 收入预测...');
    const predictions = await affiliate.getPredictions(3);
    
    if (predictions.predictions && predictions.predictions.length > 0) {
      console.log(`✅ 生成${predictions.months}个月预测`);
      console.log(`   总预测收入：$${predictions.totalPredicted}`);
      console.log(`   月均收入：$${predictions.averageMonthly}\n`);
      passed++;
    } else {
      console.log('❌ 收入预测测试失败\n');
      failed++;
    }

    // 测试 9: 利基分析
    console.log('测试 9: 利基市场分析...');
    const nicheAnalysis = await affiliate.analyzeNiche({
      keywords: ['fitness', 'home workout'],
      competition: 'medium'
    });
    
    if (nicheAnalysis.topNiche && nicheAnalysis.estimatedRevenue) {
      console.log(`✅ 利基分析完成`);
      console.log(`   推荐利基：${nicheAnalysis.topNiche}`);
      console.log(`   预估月收入：$${nicheAnalysis.estimatedRevenue}\n`);
      passed++;
    } else {
      console.log('❌ 利基分析测试失败\n');
      failed++;
    }

    // 测试 10: 获取技能状态
    console.log('测试 10: 获取技能状态...');
    const status = affiliate.getStatus();
    
    if (status.configured && status.features) {
      console.log(`✅ 获取技能状态`);
      console.log(`   已配置：${status.configured}`);
      console.log(`   平台数：${status.platforms.length}`);
      console.log(`   版本：${status.version}\n`);
      passed++;
    } else {
      console.log('❌ 技能状态测试失败\n');
      failed++;
    }

  } catch (error) {
    console.log(`❌ 测试出错：${error.message}`);
    failed++;
  }

  // 输出测试结果
  console.log('═══════════════════════════════════════');
  console.log(`测试结果：${passed} 通过，${failed} 失败`);
  console.log(`成功率：${((passed / (passed + failed)) * 100).toFixed(1)}%`);
  console.log('═══════════════════════════════════════\n');

  if (failed === 0) {
    console.log('🎉 所有测试通过！\n');
    process.exit(0);
  } else {
    console.log('⚠️  部分测试失败，请检查代码\n');
    process.exit(1);
  }
}

// 运行测试
runTests();
