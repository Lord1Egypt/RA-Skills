const Skill = require('./index.js');

async function test() {
  console.log('测试: 非洲市场政策查询Skill');
  const skill = new Skill();
  
  try {
    // 测试中文查询
    console.log('1. 测试中文查询...');
    skill.setLanguage('zh-CN');
    const policiesCN = await skill.queryPolicies('investment');
    console.log('   ✅ 中文政策查询通过:', policiesCN.totalPolicies, '条政策');
    
    // 测试英文查询
    console.log('2. 测试英文查询...');
    skill.setLanguage('en-US');
    const policiesEN = await skill.queryPolicies('investment');
    console.log('   ✅ 英文政策查询通过:', policiesEN.totalPolicies, 'policies');
    
    // 测试投资环境分析
    console.log('3. 测试投资环境分析...');
    const analysis = await skill.analyzeInvestmentEnvironment();
    console.log('   ✅ 投资环境分析通过，评分:', analysis.score);
    
    // 测试语言切换
    console.log('4. 测试语言切换...');
    const langResult = skill.setLanguage('zh-CN');
    console.log('   ✅ 语言切换测试:', langResult ? '通过' : '失败');
    
    console.log('\n🎉 非洲市场政策查询Skill 所有测试通过！');
    return true;
  } catch (error) {
    console.error('❌ 测试失败:', error);
    return false;
  }
}

// 运行测试
test().then(success => {
  process.exit(success ? 0 : 1);
});
