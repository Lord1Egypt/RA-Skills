#!/usr/bin/env node

/**
 * AI-Social-Media-Manager 演示脚本
 * 展示所有核心功能
 */

const { SocialMediaManager } = require('./src/index');

async function main() {
  console.log('🤖 AI-Social-Media-Manager 功能演示\n');
  console.log('='.repeat(60));

  const smm = new SocialMediaManager();

  // 演示 1: 生成内容日历
  console.log('\n📅 演示 1: 生成内容日历\n');
  const calendar = smm.generateContentCalendar(
    'xiaohongshu',
    new Date(2026, 2, 1),
    '春季科技新品评测',
    10
  );

  console.log(`月份：${calendar.month}`);
  console.log(`平台：${calendar.platform}`);
  console.log(`帖子数量：${calendar.totalPosts}`);
  console.log(`\n前 3 条内容:`);
  calendar.calendar.slice(0, 3).forEach((item, i) => {
    console.log(`  ${i + 1}. ${item.date} ${item.time} - ${item.contentType}`);
    console.log(`     标签：${item.hashtags.join(' ')}`);
    console.log(`     预估互动：${item.estimatedEngagement}`);
  });
  console.log(`\n每周发布：${calendar.summary.postsPerWeek} 条`);
  console.log(`预估总互动：${calendar.summary.estimatedTotalEngagement}`);

  // 演示 2: 最佳发布时间
  console.log('\n' + '='.repeat(60));
  console.log('\n⏰ 演示 2: 最佳发布时间推荐\n');

  const platforms = ['xiaohongshu', 'weibo', 'twitter', 'linkedin'];
  const platformNames = {
    xiaohongshu: '小红书',
    weibo: '微博',
    twitter: 'Twitter',
    linkedin: 'LinkedIn'
  };

  platforms.forEach(platform => {
    const time = smm.getBestPostingTime(platform, new Date());
    console.log(`  ${platformNames[platform]}: ${time}`);
  });

  // 演示 3: 自动回复
  console.log('\n' + '='.repeat(60));
  console.log('\n💬 演示 3: 自动回复和互动\n');

  const comments = [
    { text: '这个产品怎么样？价格多少？', tone: '友好专业' },
    { text: '哈哈，太有趣了！', tone: '幽默风趣' },
    { text: '质量太差了，要退款！', tone: '简洁直接' }
  ];

  for (const comment of comments) {
    const reply = await smm.autoReply(comment.text, comment.tone);
    console.log(`评论：${reply.originalComment}`);
    console.log(`情感：${reply.sentiment}`);
    console.log(`回复：${reply.reply}`);
    console.log('---');
  }

  // 演示 4: 表现分析
  console.log('\n📊 演示 4: 表现分析和优化建议\n');

  const mockPosts = [
    { likes: 500, comments: 80, shares: 120, views: 8000, contentType: '评测' },
    { likes: 300, comments: 50, shares: 80, views: 5000, contentType: '教程' },
    { likes: 800, comments: 150, shares: 200, views: 12000, contentType: '种草' },
    { likes: 450, comments: 70, shares: 100, views: 7500, contentType: '对比' },
    { likes: 600, comments: 90, shares: 140, views: 9000, contentType: '评测' }
  ];

  const analysis = smm.analyzePerformance('xiaohongshu', 'last_30_days', mockPosts);

  console.log(`平台：${analysis.platform}`);
  console.log(`时间段：${analysis.period}`);
  console.log(`总帖子数：${analysis.metrics.totalPosts}`);
  console.log(`\n核心指标:`);
  console.log(`  总点赞：${analysis.metrics.totalLikes}`);
  console.log(`  总评论：${analysis.metrics.totalComments}`);
  console.log(`  总分享：${analysis.metrics.totalShares}`);
  console.log(`  总浏览：${analysis.metrics.totalViews}`);
  console.log(`  平均互动率：${analysis.metrics.avgEngagementRate}`);
  console.log(`\n最佳表现帖子:`);
  console.log(`  类型：${analysis.metrics.bestPerformingPost.contentType}`);
  console.log(`  互动数：${analysis.metrics.bestPerformingPost.likes + analysis.metrics.bestPerformingPost.comments + analysis.metrics.bestPerformingPost.shares}`);
  console.log(`\n优化建议:`);
  analysis.metrics.recommendations.forEach((rec, i) => {
    console.log(`  ${i + 1}. ${rec}`);
  });

  // 总结
  console.log('\n' + '='.repeat(60));
  console.log('\n✅ 演示完成！\n');
  console.log('AI-Social-Media-Manager 提供:');
  console.log('  ✓ 自动化内容日历生成');
  console.log('  ✓ 智能发布时间推荐');
  console.log('  ✓ 自动回复和互动');
  console.log('  ✓ 深度数据分析和优化建议');
  console.log('  ✓ 支持 6+ 主流社交媒体平台');
  console.log('\n立即安装：clawhub install ai-social-media-manager');
  console.log('定价：$99/月\n');
}

main().catch(console.error);
