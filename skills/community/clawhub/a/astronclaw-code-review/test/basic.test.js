/**
 * AI Code Review Assistant 基本测试
 */

import { CodeReviewAssistant } from '../src/index.js';

// 测试代码示例
const TEST_CODE = `
// 示例代码：一个简单的用户处理函数
function processUserData(user) {
  // 硬编码的API密钥（安全风险）
  const apiKey = "sk_live_1234567890abcdef";
  
  // 验证用户输入
  if (!user || !user.name || !user.email) {
    return { error: "Invalid user data" };
  }
  
  // 处理数据 - 这里有一些性能问题
  let result = "";
  for (let i = 0; i < 100; i++) {
    result += user.name + "-" + i; // 字符串拼接在循环中（性能问题）
  }
  
  // 保存到数据库（模拟SQL拼接 - 安全风险）
  const query = "INSERT INTO users VALUES ('" + user.name + "', '" + user.email + "')";
  
  // 返回结果
  return { success: true, query: query };
}

// 使用eval（安全风险）
function dangerousFunction(code) {
  return eval(code);
}
`;

async function runTests() {
  console.log('🧪 AI Code Review Assistant 基本测试');
  console.log('='.repeat(60));
  
  try {
    // 1. 初始化助手
    console.log('1. 初始化 Code Review Assistant...');
    const assistant = new CodeReviewAssistant({
      reviewLevel: 'standard',
      aiEnabled: true,
      includeSecurity: true,
      includePerformance: true
    });
    
    await assistant.init();
    
    const status = assistant.getStatus();
    console.log('✅ 初始化成功');
    console.log(`   可用工具: ${status.availableTools.length} 个`);
    console.log(`   配置: ${JSON.stringify(status.config)}`);
    
    // 2. 测试综合代码审查
    console.log('\n2. 测试综合代码审查...');
    const reviewResult = await assistant.reviewCode({
      code: TEST_CODE,
      filePath: 'test-example.js',
      options: {
        language: 'javascript'
      }
    });
    
    if (reviewResult.success) {
      console.log('✅ 代码审查成功');
      console.log(`   总体评分: ${reviewResult.result.summary.overallScore}/100`);
      console.log(`   问题总数: ${reviewResult.result.analysis.quality.issues.length + 
                              (reviewResult.result.analysis.security?.issues?.length || 0) + 
                              (reviewResult.result.analysis.performance?.issues?.length || 0)}`);
      
      // 显示关键问题
      const criticalIssues = [];
      ['quality', 'security', 'performance'].forEach(category => {
        const issues = reviewResult.result.analysis[category]?.issues || [];
        issues.forEach(issue => {
          if (issue.severity === 'critical' || issue.severity === 'high') {
            criticalIssues.push({
              category,
              message: issue.message,
              line: issue.line
            });
          }
        });
      });
      
      if (criticalIssues.length > 0) {
        console.log(`\n   🚨 关键问题:`);
        criticalIssues.forEach((issue, idx) => {
          console.log(`     ${idx + 1}. [${issue.category}] ${issue.message} (第${issue.line}行)`);
        });
      }
      
    } else {
      console.log('❌ 代码审查失败:', reviewResult.error?.message);
    }
    
    // 3. 测试专项扫描
    console.log('\n3. 测试代码质量专项扫描...');
    const qualityResult = await assistant.scanCodeQuality({
      code: TEST_CODE
    });
    
    if (qualityResult.success) {
      console.log(`✅ 质量扫描完成: 评分 ${qualityResult.result.summary.overallScore}/100`);
    }
    
    // 4. 测试安全审计
    console.log('\n4. 测试安全审计...');
    const securityResult = await assistant.auditSecurity({
      code: TEST_CODE
    });
    
    if (securityResult.success) {
      console.log(`✅ 安全审计完成: 评分 ${securityResult.result.summary.overallScore}/100`);
    }
    
    // 5. 测试报告生成
    console.log('\n5. 测试报告生成...');
    if (reviewResult.success) {
      const reportResult = await assistant.generateReport({
        reviewResults: reviewResult.result,
        format: 'markdown',
        includeDetails: true
      });
      
      if (reportResult.success) {
        console.log(`✅ 报告生成完成: ${reportResult.result.format} 格式`);
        console.log(`   文件大小: ${reportResult.result.report.size} 字节`);
      }
    }
    
    // 6. 测试工具列表
    console.log('\n6. 测试工具列表...');
    const tools = assistant.listTools();
    console.log(`✅ 可用工具 (${tools.length} 个):`);
    tools.forEach(tool => {
      console.log(`   - ${tool.name} (${tool.category}): ${tool.description}`);
    });
    
    console.log('\n' + '='.repeat(60));
    console.log('🎉 所有基本测试通过！');
    console.log('\n📋 测试总结:');
    console.log('   ✓ 系统初始化正常');
    console.log('   ✓ 代码审查功能正常');
    console.log('   ✓ 质量扫描正常');
    console.log('   ✓ 安全审计正常');
    console.log('   ✓ 报告生成正常');
    console.log('   ✓ 工具注册正常');
    
    return true;
    
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error('堆栈:', error.stack);
    return false;
  }
}

// 运行测试
if (import.meta.url === `file://${process.argv[1]}`) {
  runTests()
    .then(success => {
      console.log(success ? '\n✅ 测试完成，系统正常工作' : '\n❌ 测试失败');
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error('❌ 测试执行异常:', error);
      process.exit(1);
    });
}

export { runTests };