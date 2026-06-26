/**
 * AI-SEO-Optimizer 测试文件
 */

const seo = require('./index');

async function runTests() {
  console.log('🚀 开始测试 AI-SEO-Optimizer...\n');
  
  // 测试 1: 关键词研究
  console.log('📊 测试 1: 关键词研究');
  try {
    const keywordResult = await seo.keywordResearch('SEO 优化');
    console.log('✅ 关键词研究成功');
    console.log(`   发现机会：${keywordResult.totalOpportunities}`);
    console.log(`   高优先级：${keywordResult.highPriority}\n`);
  } catch (error) {
    console.log('❌ 关键词研究失败:', error.message);
  }
  
  // 测试 2: 内容优化
  console.log('📝 测试 2: 内容优化分析');
  try {
    const sampleContent = `
# SEO 优化完整指南

SEO 是搜索引擎优化的重要组成部分。

## 什么是 SEO

SEO 帮助网站获得更好的排名。

## 关键词研究

关键词研究是 SEO 的基础。
    `;
    
    const optimizeResult = await seo.optimizeContent(sampleContent, ['SEO', '搜索引擎优化']);
    console.log('✅ 内容分析成功');
    console.log(`   当前分数：${optimizeResult.currentScore}`);
    console.log(`   建议数量：${optimizeResult.totalSuggestions}\n`);
  } catch (error) {
    console.log('❌ 内容分析失败:', error.message);
  }
  
  // 测试 3: 内链建议
  console.log('🔗 测试 3: 内链建议');
  try {
    const linkResult = await seo.suggestInternalLinks(
      'https://example.com/seo-guide',
      'SEO 优化和关键词研究是数字营销的核心'
    );
    console.log('✅ 内链建议生成成功');
    console.log(`   建议数量：${linkResult.length}\n`);
  } catch (error) {
    console.log('❌ 内链建议失败:', error.message);
  }
  
  // 测试 4: 完整分析
  console.log('📈 测试 4: 完整 SEO 分析');
  try {
    const fullResult = await seo.analyze(
      'https://example.com/page',
      ['SEO 工具', '关键词研究']
    );
    console.log('✅ 完整分析成功');
    console.log(`   综合评分：${fullResult.scores.overall}`);
    console.log(`   建议数量：${fullResult.recommendations.length}\n`);
  } catch (error) {
    console.log('❌ 完整分析失败:', error.message);
  }
  
  console.log('✅ 所有测试完成!\n');
}

// 运行测试
runTests().catch(console.error);
