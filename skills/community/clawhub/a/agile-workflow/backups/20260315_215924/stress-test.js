#!/usr/bin/env node
/**
 * 多 Agent 架构压力测试 v1.0
 * 
 * 测试场景：
 * 1. 缓存性能测试
 * 2. 并发消息测试
 * 3. 记忆持久化测试
 * 4. 综合集成测试
 */

const { getContextRouter } = require('./context-router');
const { getPromptCache } = require('./prompt-cache');
const { getMessageBus } = require('./message-bus');
const { getMemoryManager } = require('./memory-manager');
const { getLLMGateway } = require('./llm-gateway');
const { getIntegrationAdapter } = require('./integration-adapter');
const { SmartCacheBackend } = require('./cache-backend');

console.log('========================================');
console.log('  多 Agent 架构压力测试');
console.log('========================================\n');

// ============ 测试配置 ============

const CONFIG = {
  cacheTestCount: 1000,      // 缓存测试次数
  messageTestCount: 500,     // 消息测试次数
  memoryTestCount: 100,      // 记忆测试次数
  concurrentTestCount: 50    // 并发测试次数
};

// ============ 测试 1：缓存性能 ============

async function testCachePerformance() {
  console.log('📦 测试 1：缓存性能测试');
  console.log(`   测试次数: ${CONFIG.cacheTestCount}`);
  
  const cache = getPromptCache();
  const startTime = Date.now();
  
  // 写入测试
  console.log('\n   1.1 写入测试...');
  for (let i = 0; i < CONFIG.cacheTestCount; i++) {
    cache.set(`test-prompt-${i}`, { result: `result-${i}`, index: i });
  }
  const writeTime = Date.now() - startTime;
  console.log(`   写入 ${CONFIG.cacheTestCount} 条，耗时: ${writeTime}ms (${(CONFIG.cacheTestCount / writeTime * 1000).toFixed(0)} ops/s)`);
  
  // 读取测试（50% 命中）
  console.log('\n   1.2 读取测试（50% 命中）...');
  const readStart = Date.now();
  let hits = 0;
  for (let i = 0; i < CONFIG.cacheTestCount; i++) {
    const key = i % 2 === 0 ? `test-prompt-${i}` : `test-prompt-new-${i}`;
    const result = cache.get(key);
    if (result) hits++;
  }
  const readTime = Date.now() - readStart;
  console.log(`   读取 ${CONFIG.cacheTestCount} 条，命中: ${hits}，耗时: ${readTime}ms (${(CONFIG.cacheTestCount / readTime * 1000).toFixed(0)} ops/s)`);
  
  // 统计
  const stats = cache.getStats();
  console.log(`\n   📊 缓存统计:`);
  console.log(`      命中率: ${stats.hitRate}`);
  console.log(`      内存缓存: ${stats.memoryCacheSize}`);
  console.log(`      磁盘缓存: ${stats.diskCacheCount}`);
  
  return { writeTime, readTime, hitRate: stats.hitRate };
}

// ============ 测试 2：并发消息 ============

async function testMessagePerformance() {
  console.log('\n📨 测试 2：并发消息测试');
  console.log(`   测试次数: ${CONFIG.messageTestCount}`);
  
  const bus = getMessageBus();
  let receivedCount = 0;
  
  // 订阅
  bus.subscribe('stress-test', (msg) => {
    receivedCount++;
  });
  
  const startTime = Date.now();
  
  // 发布测试
  console.log('\n   2.1 发布测试...');
  for (let i = 0; i < CONFIG.messageTestCount; i++) {
    bus.publish('stress-test', { index: i, data: `message-${i}` });
  }
  const publishTime = Date.now() - startTime;
  console.log(`   发布 ${CONFIG.messageTestCount} 条，耗时: ${publishTime}ms (${(CONFIG.messageTestCount / publishTime * 1000).toFixed(0)} ops/s)`);
  
  // 请求-响应测试
  console.log('\n   2.2 请求-响应测试...');
  const requestStart = Date.now();
  
  // 订阅响应
  bus.subscribe('stress-response', (msg) => {
    bus.reply(msg.payload._replyTo, { processed: true });
  });
  
  // 发送请求（同步测试）
  let responseCount = 0;
  for (let i = 0; i < Math.min(10, CONFIG.messageTestCount); i++) {
    try {
      await Promise.race([
        bus.request('stress-response', { index: i }),
        new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 5000))
      ]);
      responseCount++;
    } catch (e) {
      // 超时
    }
  }
  const requestTime = Date.now() - requestStart;
  console.log(`   请求-响应 ${responseCount} 次，耗时: ${requestTime}ms`);
  
  const stats = bus.getStats();
  console.log(`\n   📊 消息统计:`);
  console.log(`      发布: ${stats.published}`);
  console.log(`      送达: ${stats.delivered}`);
  console.log(`      订阅: ${stats.subscriptions}`);
  
  return { publishTime, requestTime, published: stats.published };
}

// ============ 测试 3：记忆持久化 ============

async function testMemoryPerformance() {
  console.log('\n🧠 测试 3：记忆持久化测试');
  console.log(`   测试次数: ${CONFIG.memoryTestCount}`);
  
  const memory = getMemoryManager();
  const sessionId = `stress-test-${Date.now()}`;
  
  const startTime = Date.now();
  
  // 写入测试
  console.log('\n   3.1 短期记忆写入...');
  for (let i = 0; i < CONFIG.memoryTestCount; i++) {
    memory.setShort(sessionId, `decision:${i}`, `决策内容 ${i}`);
    memory.setShort(sessionId, `result:${i}`, `结果内容 ${i}`);
  }
  const writeTime = Date.now() - startTime;
  console.log(`   写入 ${CONFIG.memoryTestCount * 2} 条，耗时: ${writeTime}ms`);
  
  // 读取测试
  console.log('\n   3.2 短期记忆读取...');
  const readStart = Date.now();
  for (let i = 0; i < CONFIG.memoryTestCount; i++) {
    memory.getShort(sessionId, `decision:${i}`);
  }
  const readTime = Date.now() - readStart;
  console.log(`   读取 ${CONFIG.memoryTestCount} 条，耗时: ${readTime}ms`);
  
  // 持久化测试
  console.log('\n   3.3 持久化测试...');
  const persistStart = Date.now();
  memory.persistSession(sessionId, '压力测试会话完成');
  const persistTime = Date.now() - persistStart;
  console.log(`   持久化耗时: ${persistTime}ms`);
  
  const stats = memory.getStats();
  console.log(`\n   📊 记忆统计:`);
  console.log(`      短期命中率: ${stats.shortMemoryHitRate}`);
  console.log(`      长期会话数: ${stats.longMemorySessions}`);
  console.log(`      决策数: ${stats.longMemoryDecisions}`);
  
  return { writeTime, readTime, persistTime };
}

// ============ 测试 4：上下文路由 ============

async function testContextRouterPerformance() {
  console.log('\n🔍 测试 4：上下文路由测试');
  console.log(`   测试次数: ${CONFIG.concurrentTestCount}`);
  
  const router = getContextRouter();
  const startTime = Date.now();
  
  // 创建测试任务
  const tasks = [];
  for (let i = 0; i < CONFIG.concurrentTestCount; i++) {
    const task = {
      id: `task-${i}`,
      goal: `目标 ${i}`,
      input: { data: `输入数据 ${i}`.repeat(100) }, // 模拟大数据
      dependencies: [{ id: `dep-${i}`, status: 'completed' }],
      result: `结果 ${i}`
    };
    router.cache.set(`task-${i}`, task);
  }
  
  // 路由测试
  console.log('\n   4.1 上下文路由测试...');
  let totalSize = 0;
  for (let i = 0; i < CONFIG.concurrentTestCount; i++) {
    const ctx = router.getContext(`task-${i}`, 'executor');
    totalSize += JSON.stringify(ctx).length;
  }
  const routeTime = Date.now() - startTime;
  console.log(`   路由 ${CONFIG.concurrentTestCount} 次，耗时: ${routeTime}ms`);
  console.log(`   平均上下文大小: ${(totalSize / CONFIG.concurrentTestCount).toFixed(0)} bytes`);
  
  const stats = router.getStats();
  console.log(`\n   📊 路由统计:`);
  console.log(`      缓存大小: ${stats.cacheSize}`);
  console.log(`      模板数: ${stats.templates.length}`);
  
  return { routeTime, avgContextSize: (totalSize / CONFIG.concurrentTestCount).toFixed(0) };
}

// ============ 测试 5：综合集成 ============

async function testIntegrationPerformance() {
  console.log('\n🔌 测试 5：综合集成测试');
  
  const adapter = getIntegrationAdapter();
  const startTime = Date.now();
  
  // 模拟完整工作流
  console.log('\n   5.1 模拟工作流...');
  
  const task = {
    id: 'integration-test-001',
    goal: '完成压力测试',
    dependencies: []
  };
  
  // 1. 准备上下文
  const context = adapter.prepareContext(task, 'executor');
  console.log('   ✅ 上下文准备完成');
  
  // 2. 发布事件
  adapter.publishEvent('task.started', { taskId: task.id, agent: 'test-agent' });
  console.log('   ✅ 事件发布完成');
  
  // 3. 记录决策
  adapter.recordDecision('architecture', '三层架构');
  console.log('   ✅ 决策记录完成');
  
  // 4. 结束会话
  adapter.endSession('集成测试完成');
  console.log('   ✅ 会话结束完成');
  
  const totalTime = Date.now() - startTime;
  console.log(`\n   综合测试耗时: ${totalTime}ms`);
  
  // 健康检查
  const health = adapter.healthCheck();
  console.log(`\n   📊 健康检查:`);
  console.log(`      状态: ${health.healthy ? '健康' : '异常'}`);
  if (health.issues.length > 0) {
    console.log(`      问题: ${health.issues.join(', ')}`);
  }
  
  return { totalTime, healthy: health.healthy };
}

// ============ 运行所有测试 ============

async function runAllTests() {
  const results = {};
  
  try {
    results.cache = await testCachePerformance();
    results.message = await testMessagePerformance();
    results.memory = await testMemoryPerformance();
    results.router = await testContextRouterPerformance();
    results.integration = await testIntegrationPerformance();
    
    // 汇总
    console.log('\n========================================');
    console.log('  测试结果汇总');
    console.log('========================================\n');
    
    console.log('缓存性能:');
    console.log(`  写入: ${results.cache.writeTime}ms`);
    console.log(`  读取: ${results.cache.readTime}ms`);
    console.log(`  命中率: ${results.cache.hitRate}`);
    
    console.log('\n消息性能:');
    console.log(`  发布: ${results.message.publishTime}ms`);
    console.log(`  消息数: ${results.message.published}`);
    
    console.log('\n记忆性能:');
    console.log(`  写入: ${results.memory.writeTime}ms`);
    console.log(`  读取: ${results.memory.readTime}ms`);
    console.log(`  持久化: ${results.memory.persistTime}ms`);
    
    console.log('\n路由性能:');
    console.log(`  路由时间: ${results.router.routeTime}ms`);
    console.log(`  平均上下文: ${results.router.avgContextSize} bytes`);
    
    console.log('\n集成测试:');
    console.log(`  总耗时: ${results.integration.totalTime}ms`);
    console.log(`  状态: ${results.integration.healthy ? '健康' : '异常'}`);
    
    console.log('\n========================================');
    console.log('  ✅ 所有测试完成');
    console.log('========================================');
    
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error(error.stack);
  }
}

runAllTests();