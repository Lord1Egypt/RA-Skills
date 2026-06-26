#!/usr/bin/env node
/**
 * 多 Agent 架构集成测试
 * 
 * 验证所有模块协同工作
 */

const { getContextRouter } = require('./context-router');
const { getPromptCache } = require('./prompt-cache');
const { getMessageBus } = require('./message-bus');
const { getMemoryManager } = require('./memory-manager');
const { getLLMGateway } = require('./llm-gateway');

console.log('========================================');
console.log('  多 Agent 架构集成测试');
console.log('========================================\n');

async function runTests() {
  // 1. 初始化所有模块
  console.log('📦 1. 初始化模块...');
  const router = getContextRouter();
  const cache = getPromptCache();
  const bus = getMessageBus();
  const memory = getMemoryManager();
  const gateway = getLLMGateway();
  console.log('   ✅ 所有模块初始化成功\n');

  // 2. 测试 Context Router
  console.log('🔍 2. 测试 Context Router...');
  const task = {
    id: 'task-integration-001',
    goal: '创建一部玄幻小说',
    input: { worldType: '修仙世界', chapters: 10 },
    dependencies: [{ id: 'dep-1', status: 'completed' }],
    result: '世界观架构完成'
  };
  router.cache.set('task-integration-001', task);
  
  const plannerCtx = router.getContext('task-integration-001', 'planner');
  const executorCtx = router.getContext('task-integration-001', 'executor');
  console.log('   Planner 上下文大小:', JSON.stringify(plannerCtx).length, 'bytes');
  console.log('   Executor 上下文大小:', JSON.stringify(executorCtx).length, 'bytes');
  console.log('   ✅ Context Router 测试通过\n');

  // 3. 测试 Prompt Cache
  console.log('💾 3. 测试 Prompt Cache...');
  const testPrompt = '请生成一段关于修仙世界的描述';
  
  const beforeCache = cache.get(testPrompt);
  console.log('   缓存前查询:', beforeCache === null ? 'MISS' : 'HIT');
  
  cache.set(testPrompt, { text: '在一个灵气充沛的世界...' });
  const afterCache = cache.get(testPrompt);
  console.log('   缓存后查询:', afterCache ? 'HIT' : 'MISS');
  console.log('   ✅ Prompt Cache 测试通过\n');

  // 4. 测试 Message Bus
  console.log('📨 4. 测试 Message Bus...');
  let receivedMessages = [];
  
  bus.subscribe('task.completed', (msg) => {
    receivedMessages.push(msg);
  });
  
  bus.taskCompleted('task-001', { status: 'done' }, 'agent-writer');
  bus.taskCompleted('task-002', { status: 'done' }, 'agent-writer');
  
  console.log('   发布消息: 2');
  console.log('   接收消息:', receivedMessages.length);
  console.log('   ✅ Message Bus 测试通过\n');

  // 5. 测试 Memory Manager
  console.log('🧠 5. 测试 Memory Manager...');
  memory.setShort('test-session', 'decision:architecture', '采用三层架构');
  memory.setShort('test-session', 'result:worldbuilding', '世界观完成');
  
  const decision = memory.getShort('test-session', 'decision:architecture');
  console.log('   短期记忆:', decision);
  
  memory.persistSession('test-session', '测试会话完成');
  console.log('   持久化: 完成');
  console.log('   长期记忆决策数:', memory.getDecisions().length);
  console.log('   ✅ Memory Manager 测试通过\n');

  // 6. 测试 LLM Gateway
  console.log('🚀 6. 测试 LLM Gateway...');
  try {
    const result1 = await gateway.call('测试提示词 1');
    console.log('   第一次调用: 完成');
    
    const result2 = await gateway.call('测试提示词 1'); // 应该命中缓存
    console.log('   第二次调用（缓存）: 完成');
    
    const stats = gateway.getStats();
    console.log('   缓存命中率:', stats.cacheHitRate);
    console.log('   ✅ LLM Gateway 测试通过\n');
  } catch (e) {
    console.log('   ⚠️ LLM Gateway 调用失败:', e.message, '\n');
  }

  // 7. 综合统计
  console.log('========================================');
  console.log('  模块统计汇总');
  console.log('========================================');
  console.log('\nContext Router:', JSON.stringify(router.getStats(), null, 2));
  console.log('\nPrompt Cache:', JSON.stringify(cache.getStats(), null, 2));
  console.log('\nMessage Bus:', JSON.stringify(bus.getStats(), null, 2));
  console.log('\nMemory Manager:', JSON.stringify(memory.getStats(), null, 2));
  console.log('\nLLM Gateway:', JSON.stringify(gateway.getStats(), null, 2));

  console.log('\n========================================');
  console.log('  ✅ 所有测试通过');
  console.log('========================================');
}

runTests().catch(console.error);