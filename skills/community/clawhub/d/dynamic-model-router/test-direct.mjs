/**
 * 直接测试DecisionEngine - 不使用Jest
 */

import { DecisionEngine } from './dist/routing/decision-engine.js';

async function test() {
  console.log('🚀 直接测试DecisionEngine...\n');
  
  try {
    console.log('1. 创建DecisionEngine实例...');
    const start = Date.now();
    const engine = new DecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
    });
    console.log(`   创建完成 (${Date.now() - start}ms)`);
    
    console.log('2. 获取引擎状态...');
    const status = engine.getEngineStatus();
    console.log('   状态:', {
      isInitialized: status.isInitialized,
      learningEnabled: status.config.learningEnabled,
    });
    
    console.log('3. 测试简单路由...');
    const request = {
      task: {
        id: 'test_direct_001',
        content: '直接测试任务',
        language: 'zh',
        complexity: 'simple',
        category: ['test'],
        estimatedTokens: 50,
        createdAt: new Date(),
      },
      constraints: {},
    };
    
    const routeStart = Date.now();
    const response = await engine.route(request);
    console.log(`   路由完成 (${Date.now() - routeStart}ms):`, {
      decisionId: response.decision.decisionId,
      selectedModel: response.decision.selectedModel?.id || response.decision.selectedModel?.modelId,
      executionInstructions: response.executionInstructions.modelId,
    });
    
    console.log('\n✅ 所有测试通过！');
    console.log(`总时间: ${Date.now() - start}ms`);
    
    return 0;
    
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error('堆栈:', error.stack);
    return 1;
  }
}

// 处理未捕获的Promise拒绝
process.on('unhandledRejection', (reason, promise) => {
  console.error('未处理的Promise拒绝:', reason);
  process.exit(1);
});

// 执行测试
test().then(code => {
  process.exit(code);
});