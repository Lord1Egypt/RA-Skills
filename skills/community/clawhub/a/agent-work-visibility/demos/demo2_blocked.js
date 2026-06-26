/**
 * Demo 2: 阻塞 + 用户介入
 * 
 * 演示场景：
 * 1. 正常执行到收集信息阶段
 * 2. 遇到 API 超时阻塞
 * 3. 自动重试后恢复
 * 4. 发现多个方向需要用户决策
 * 5. 用户选择后继续推进
 */

const { TaskVisibilityManager, BLOCKER_TYPE, USER_INPUT_TYPE } = require('../src/index');

// ==================== 初始化 ====================

console.log('\n════════════════════════════════════════');
console.log('  Demo 2: 阻塞 + 用户介入');
console.log('════════════════════════════════════════\n');

const manager = new TaskVisibilityManager();

// 创建任务
manager.createTask('demo-002', '调研去中心化 AI 计算平台', 'research');
console.log('✅ 任务创建完成\n');

// ==================== 快速通过前两个阶段 ====================

console.log('─────────────────────────────────────────────');
console.log('【快速通过】理解任务 + 制定计划');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-002', '理解任务');
manager.completePhase('demo-002', '理解任务', '已明确任务目标');

manager.startPhase('demo-002', '制定搜索计划');
manager.completePhase('demo-002', '制定搜索计划', '已确定搜索策略');

console.log('✅ 前两个阶段完成\n');

// ==================== 阶段 3: 收集信息 - 遇到阻塞 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 3】收集信息 - 遇到 API 超时');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-002', '收集信息');
manager.event('demo-002', 'search_started');
manager.log('demo-002', '开始搜索去中心化 AI 计算平台');

console.log('📋 默认视图（正常搜索）：');
console.log(manager.getDefaultView('demo-002'));
console.log();

// 模拟网页读取
manager.event('demo-002', 'page_fetch_started', { url: 'https://api.example.com', pageNumber: 1 });
manager.updatePhaseProgress('demo-002', '收集信息', 30, '正在读取第 1 个网页');

// ⚠️ 遇到阻塞：API 超时
console.log('⚠️ 遇到 API 超时...\n');

manager.block('demo-002', BLOCKER_TYPE.API_TIMEOUT, '外部 API 响应超时');
manager.event('demo-002', 'page_fetch_timeout');

console.log('📋 默认视图（阻塞状态）：');
console.log(manager.getDefaultView('demo-002'));
console.log();

console.log('📋 展开视图（阻塞详情）：');
console.log(manager.getFullView('demo-002'));
console.log();

// ==================== 自动重试 ====================

console.log('─────────────────────────────────────────────');
console.log('【自动重试】第 1 次重试');
console.log('─────────────────────────────────────────────\n');

manager.log('demo-002', '正在重试 API 请求', 'retry');

// 模拟重试记录
const task = manager.getTask('demo-002');
task.retry_log.unshift({
  timestamp: new Date().toISOString(),
  operation: 'API 请求',
  attempt: 1,
  reason: '超时',
  success: false
});

// 重试成功
manager.event('demo-002', 'retry_success', { operation: 'API 请求' });
manager.unblock('demo-002');
manager.log('demo-002', '重试成功，继续执行');

console.log('📋 默认视图（恢复执行）：');
console.log(manager.getDefaultView('demo-002'));
console.log();

// 继续收集信息
manager.event('demo-002', 'page_fetch_completed', { pageNumber: 5 });
manager.event('demo-002', 'extraction_completed', { itemCount: 8 });
manager.updatePhaseProgress('demo-002', '收集信息', 80, '正在整理提取的数据');

// 完成阶段 3
manager.completePhase('demo-002', '收集信息', '已收集 8 个平台的信息');
console.log('✅ 阶段 3 完成（经历阻塞后恢复）\n');

// ==================== 阶段 4: 分析与比较 - 需要用户决策 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 4】分析与比较 - 需要用户决策');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-002', '分析与比较');
manager.log('demo-002', '开始分析 8 个平台');

// 发现多个方向，无法自动判断
console.log('⚠️ 发现多个可深入方向，需要用户决策...\n');

manager.ask('demo-002', USER_INPUT_TYPE.DIRECTION_CHOICE,
  '发现 3 个方向都可继续深入，你要优先看哪一个？',
  ['A: 技术架构（计算协议、共识机制）', 
   'B: 商业模式（定价策略、收入模型）', 
   'C: 生态发展（开发者数量、应用案例）']
);

console.log('📋 默认视图（等待用户输入）：');
console.log(manager.getDefaultView('demo-002'));
console.log();

console.log('📋 展开视图：');
console.log(manager.getFullView('demo-002'));
console.log();

// ==================== 用户响应 ====================

console.log('─────────────────────────────────────────────');
console.log('【用户响应】选择方向 A');
console.log('─────────────────────────────────────────────\n');

console.log('👤 用户选择：A - 技术架构\n');

manager.respond('demo-002');
manager.log('demo-002', '用户已选择优先分析技术架构');
manager.setNextAction('demo-002', '深入分析技术架构并输出结论');

console.log('📋 默认视图（继续执行）：');
console.log(manager.getDefaultView('demo-002'));
console.log();

// 继续分析
manager.updatePhaseProgress('demo-002', '分析与比较', 60, '正在分析技术架构');
manager.event('demo-002', 'pattern_found', { pattern: '多数平台采用类似架构' });
manager.updatePhaseProgress('demo-002', '分析与比较', 90, '正在整理分析结论');

// 完成阶段 4
manager.completePhase('demo-002', '分析与比较', '已完成技术架构对比分析');
console.log('✅ 阶段 4 完成\n');

// ==================== 阶段 5: 形成输出 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 5】形成输出');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-002', '形成输出');
manager.event('demo-002', 'output_generating');
manager.log('demo-002', '正在生成技术架构分析报告');

// 完成阶段 5
manager.event('demo-002', 'report_created', { pages: 8 });
manager.completePhase('demo-002', '形成输出', '已生成 8 页技术分析报告');
manager.event('demo-002', 'task_completed');

console.log('✅ 阶段 5 完成');
console.log('✅ 任务完成！\n');

// ==================== 最终视图 ====================

console.log('════════════════════════════════════════');
console.log('  最终状态');
console.log('════════════════════════════════════════\n');

console.log('📋 默认视图（完成状态）：');
console.log(manager.getDefaultView('demo-002'));
console.log();

console.log('📋 展开视图（含重试记录）：');
console.log(manager.getFullView('demo-002'));
console.log();

console.log('════════════════════════════════════════');
console.log('  Demo 2 完成');
console.log('════════════════════════════════════════\n');

console.log('📝 本 Demo 演示了：');
console.log('   1. 正常执行流程');
console.log('   2. API 超时阻塞的识别与显示');
console.log('   3. 阻塞状态下的推荐用户操作');
console.log('   4. 自动重试后恢复执行');
console.log('   5. Ask Human 用户介入机制');
console.log('   6. 用户响应后继续推进\n');
