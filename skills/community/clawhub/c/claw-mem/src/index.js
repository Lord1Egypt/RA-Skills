/**
 * ClawMem - OpenClaw 轻量级记忆管理系统
 * 
 * 特性：
 * - 三层检索工作流 (L0/L1/L2)
 * - 无感知生命周期监听
 * - Token 优化 (节省 60-80%)
 * - 高级搜索功能 (关键词/时间/标签/会话)
 */

import { clawMem, ClawMemCore } from './core/retrieval.js';
import { lifecycleMonitor, LifecycleMonitor } from './core/lifecycle-monitor.js';
import { memorySearch, MemorySearch } from './core/search.js';
import db from './database/init.js';

// 导出核心模块
export { clawMem, ClawMemCore };
export { lifecycleMonitor, LifecycleMonitor };
export { memorySearch, MemorySearch };
export default clawMem;

// 初始化
console.log('🧠 ClawMem v0.0.1 已启动');
console.log('='.repeat(60));
console.log('特性:');
console.log('  ✅ 三层检索工作流 (L0/L1/L2)');
console.log('  ✅ 无感知生命周期监听');
console.log('  ✅ Token 优化 (节省 60-80%)');
console.log('='.repeat(60));

// 启动生命周期监听器
lifecycleMonitor.start();

// 示例用法
export async function demo() {
  console.log('\n📚 ClawMem 使用示例:\n');
  
  // 1. 存储记忆
  console.log('1️⃣  存储记忆...');
  const recordId = clawMem.storeL0({
    category: 'session',
    summary: '用户查询 TSLA 股价',
    timestamp: Math.floor(Date.now() / 1000)
  });
  
  clawMem.storeL1({
    record_id: recordId,
    session_id: 'session_001',
    event_type: 'query.stock',
    semantic_summary: '用户询问特斯拉股票价格，系统查询 Yahoo Finance API 并返回实时股价',
    tags: ['stock', 'TSLA', 'query']
  });
  
  clawMem.storeL2({
    record_id: recordId,
    full_content: JSON.stringify({
      query: 'TSLA 股价',
      result: { price: 248.50, change: '+2.3%' },
      timestamp: new Date().toISOString()
    }, null, 2)
  });
  
  // 2. 检索记忆
  console.log('\n2️⃣  检索记忆...');
  const result = await clawMem.retrieve({
    category: 'session',
    includeTimeline: true,
    includeDetails: true,
    limit: 10
  });
  
  console.log(`检索结果：${result.message}`);
  console.log(`Token 消耗：${result.tokenCost} tokens`);
  
  // 3. 查看统计
  console.log('\n3️⃣  系统统计:');
  const stats = clawMem.getStats();
  console.log(stats);
  
  // 4. 模拟生命周期事件
  console.log('\n4️⃣  模拟生命周期事件...');
  lifecycleMonitor.intercept('session.start', {
    session_id: 'session_002',
    user_id: 'user_leo'
  });
  
  lifecycleMonitor.intercept('tool.call', {
    tool_name: 'yahoo_finance',
    args: { symbol: 'AAPL' },
    session_id: 'session_002'
  });
  
  // 等待 Worker 处理
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // 查看监听统计
  const monitorStats = lifecycleMonitor.getStats();
  console.log('监听统计:', monitorStats);
  
  console.log('\n✅ 演示完成!\n');
}

// 如果直接运行此文件，执行演示
if (process.argv[1]?.includes('index.js')) {
  demo();
}
