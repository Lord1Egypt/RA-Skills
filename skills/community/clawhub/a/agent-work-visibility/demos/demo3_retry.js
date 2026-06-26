/**
 * Demo 3: 超时重试流程
 * 
 * 演示场景：
 * 1. 网页请求超时
 * 2. 自动重试（第 1 次失败）
 * 3. 自动重试（第 2 次失败）
 * 4. 自动重试（第 3 次成功）
 * 5. 恢复执行
 */

const { TaskVisibilityManager, BLOCKER_TYPE } = require('../src/index');

// ==================== 初始化 ====================

console.log('\n════════════════════════════════════════');
console.log('  Demo 3: 超时重试流程');
console.log('════════════════════════════════════════\n');

const manager = new TaskVisibilityManager();

// 创建任务
manager.createTask('demo-003', '收集 AI 框架性能基准测试数据', 'research');
console.log('✅ 任务创建完成\n');

// ==================== 快速通过前两个阶段 ====================

manager.startPhase('demo-003', '理解任务');
manager.completePhase('demo-003', '理解任务', '已明确任务目标');

manager.startPhase('demo-003', '制定搜索计划');
manager.completePhase('demo-003', '制定搜索计划', '已确定数据源');

console.log('✅ 前两个阶段完成\n');

// ==================== 阶段 3: 收集信息 - 多次重试 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 3】收集信息 - 多次重试');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-003', '收集信息');
manager.event('demo-003', 'search_started');

const task = manager.getTask('demo-003');

// --- 第 1 次请求：超时 ---

console.log('🌐 请求数据源：https://benchmarks.ai-api.com/data');
console.log('⏱️  等待响应...\n');

manager.event('demo-003', 'page_fetch_started', { 
  url: 'https://benchmarks.ai-api.com/data', 
  pageNumber: 1 
});

// 超时
setTimeout(() => {
  console.log('❌ 第 1 次请求超时（5 秒无响应）\n');
  
  manager.block('demo-003', BLOCKER_TYPE.API_TIMEOUT, '外部 API 响应超时', 'low');
  manager.event('demo-003', 'page_fetch_timeout');
  
  console.log('📋 阻塞状态视图：');
  console.log(manager.getDefaultView('demo-003'));
  console.log();
  
  // --- 第 1 次重试 ---
  console.log('↻ 开始第 1 次重试...\n');
  
  task.retry_log.unshift({
    timestamp: new Date().toISOString(),
    operation: 'API 请求',
    attempt: 1,
    reason: '超时',
    success: false
  });
  manager.log('demo-003', '第 1 次重试失败，继续等待', 'retry');
  
  setTimeout(() => {
    console.log('❌ 第 1 次重试仍然超时\n');
    
    // --- 第 2 次重试 ---
    console.log('↻ 开始第 2 次重试...\n');
    
    task.retry_log.unshift({
      timestamp: new Date().toISOString(),
      operation: 'API 请求',
      attempt: 2,
      reason: '超时',
      success: false
    });
    manager.log('demo-003', '第 2 次重试失败', 'warning');
    
    // 升级阻塞级别
    manager.block('demo-003', BLOCKER_TYPE.API_TIMEOUT, '多次重试后仍然超时', 'medium');
    
    console.log('📋 阻塞升级视图：');
    console.log(manager.getDefaultView('demo-003'));
    console.log();
    
    setTimeout(() => {
      console.log('↻ 开始第 3 次重试...\n');
      
      // --- 第 3 次重试：成功 ---
      console.log('✅ 第 3 次重试成功！\n');
      
      task.retry_log.unshift({
        timestamp: new Date().toISOString(),
        operation: 'API 请求',
        attempt: 3,
        reason: '超时',
        success: true
      });
      
      manager.event('demo-003', 'retry_success', { operation: 'API 请求' });
      manager.unblock('demo-003');
      manager.log('demo-003', '重试成功，继续执行');
      
      // 继续执行
      manager.event('demo-003', 'page_fetch_completed', { pageNumber: 1 });
      manager.updatePhaseProgress('demo-003', '收集信息', 40, '正在读取第 1 个数据源');
      
      console.log('📋 恢复执行视图：');
      console.log(manager.getDefaultView('demo-003'));
      console.log();
      
      // 继续收集其他数据源
      manager.event('demo-003', 'page_fetch_started', { url: 'https://another-source.com', pageNumber: 2 });
      manager.event('demo-003', 'page_fetch_completed', { pageNumber: 2 });
      manager.event('demo-003', 'extraction_completed', { itemCount: 15 });
      manager.updatePhaseProgress('demo-003', '收集信息', 80, '正在整理 15 个基准测试数据');
      
      // 完成阶段 3
      manager.completePhase('demo-003', '收集信息', '已收集 15 个框架的性能数据');
      
      console.log('✅ 阶段 3 完成（经历 3 次重试）\n');
      
      // ==================== 阶段 4: 分析与比较 ====================
      
      console.log('─────────────────────────────────────────────');
      console.log('【阶段 4】分析与比较');
      console.log('─────────────────────────────────────────────\n');
      
      manager.startPhase('demo-003', '分析与比较');
      manager.event('demo-003', 'analysis_started');
      manager.log('demo-003', '正在比较 15 个框架的性能指标');
      
      manager.updatePhaseProgress('demo-003', '分析与比较', 50, '正在生成性能排名');
      manager.event('demo-003', 'pattern_found', { pattern: '发现 3 个性能领先的框架' });
      manager.updatePhaseProgress('demo-003', '分析与比较', 80, '正在整理对比结论');
      
      manager.completePhase('demo-003', '分析与比较', '已完成性能对比分析');
      
      console.log('✅ 阶段 4 完成\n');
      
      // ==================== 阶段 5: 形成输出 ====================
      
      console.log('─────────────────────────────────────────────');
      console.log('【阶段 5】形成输出');
      console.log('─────────────────────────────────────────────\n');
      
      manager.startPhase('demo-003', '形成输出');
      manager.event('demo-003', 'output_generating');
      manager.log('demo-003', '正在生成性能基准报告');
      
      manager.event('demo-003', 'report_created', { pages: 12 });
      manager.completePhase('demo-003', '形成输出', '已生成 12 页性能基准报告');
      manager.event('demo-003', 'task_completed');
      
      console.log('✅ 阶段 5 完成');
      console.log('✅ 任务完成！\n');
      
      // ==================== 最终视图 ====================
      
      console.log('════════════════════════════════════════');
      console.log('  最终状态');
      console.log('════════════════════════════════════════\n');
      
      console.log('📋 默认视图（完成状态）：');
      console.log(manager.getDefaultView('demo-003'));
      console.log();
      
      console.log('📋 展开视图（含重试记录）：');
      console.log(manager.getFullView('demo-003'));
      console.log();
      
      console.log('════════════════════════════════════════');
      console.log('  Demo 3 完成');
      console.log('════════════════════════════════════════\n');
      
      console.log('📝 本 Demo 演示了：');
      console.log('   1. 网页/API 请求超时检测');
      console.log('   2. 自动重试机制（3 次）');
      console.log('   3. 阻塞级别升级（low → medium）');
      console.log('   4. 重试成功后恢复执行');
      console.log('   5. 重试记录在展开视图中显示\n');
      
    }, 800);
    
  }, 800);
  
}, 500);

// 注意：这是一个异步 demo，需要等待 setTimeout 完成
console.log('⏳ 等待异步执行完成...\n');
