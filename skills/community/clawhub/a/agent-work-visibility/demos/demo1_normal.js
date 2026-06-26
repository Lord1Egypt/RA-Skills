/**
 * Demo 1: 正常 Research 流程
 * 
 * 演示场景：
 * 1. 理解任务
 * 2. 制定搜索计划
 * 3. 收集信息
 * 4. 分析与比较
 * 5. 形成输出
 */

const { TaskVisibilityManager } = require('../src/index');

// ==================== 初始化 ====================

console.log('\n════════════════════════════════════════');
console.log('  Demo 1: 正常 Research 流程');
console.log('════════════════════════════════════════\n');

const manager = new TaskVisibilityManager();

// 创建任务
const task = manager.createTask('demo-001', '调研 AI Agent 专用区块链', 'research');
console.log('✅ 任务创建完成');
console.log('   任务 ID:', task.task_id);
console.log('   任务标题:', task.task_title);
console.log();

// ==================== 阶段 1: 理解任务 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 1】理解任务 (10%)');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-001', '理解任务');
manager.log('demo-001', '正在解析用户需求');
manager.setNextAction('demo-001', '明确搜索关键词和数据源');

console.log('📋 默认视图：');
console.log(manager.getDefaultView('demo-001'));
console.log();

// 完成阶段 1
manager.completePhase('demo-001', '理解任务', '已明确任务目标：调研 AI Agent 专用区块链项目');
console.log('✅ 阶段 1 完成\n');

// ==================== 阶段 2: 制定搜索计划 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 2】制定搜索计划 (15%)');
console.log('─────────────────────────────────────────────\n');

manager.event('demo-001', 'planning_started');
manager.log('demo-001', '正在设计搜索策略');
manager.setNextAction('demo-001', '确定关键词和优先级');

// 模拟搜索计划制定过程
manager.event('demo-001', 'search_query_defined', { 
  query: 'AI Agent blockchain infrastructure' 
});
manager.log('demo-001', '已明确搜索范围：AI + 区块链 + Agent 基础设施');

console.log('📋 默认视图：');
console.log(manager.getDefaultView('demo-001'));
console.log();

// 完成阶段 2
manager.completePhase('demo-001', '制定搜索计划', '已确定 5 个关键词和 3 个主要数据源');
console.log('✅ 阶段 2 完成\n');

// ==================== 阶段 3: 收集信息 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 3】收集信息 (30%)');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-001', '收集信息');
manager.event('demo-001', 'search_started');

console.log('📋 默认视图（开始搜索）：');
console.log(manager.getDefaultView('demo-001'));
console.log();

// 模拟收集信息过程
console.log('   正在抓取网页...\n');

manager.event('demo-001', 'page_fetch_started', { url: 'https://example1.com', pageNumber: 1 });
manager.updatePhaseProgress('demo-001', '收集信息', 20, '正在读取第 1 个网页');
console.log('📋 进度 20%：');
console.log(manager.getDefaultView('demo-001'));
console.log();

manager.event('demo-001', 'page_fetch_completed', { pageNumber: 3 });
manager.updatePhaseProgress('demo-001', '收集信息', 50, '正在读取第 3 个网页');
console.log('📋 进度 50%：');
console.log(manager.getDefaultView('demo-001'));
console.log();

manager.event('demo-001', 'extraction_completed', { itemCount: 12 });
manager.log('demo-001', '已提取 12 个候选项目');
manager.updatePhaseProgress('demo-001', '收集信息', 80, '正在整理提取的数据');

console.log('📋 进度 80%：');
console.log(manager.getDefaultView('demo-001'));
console.log();

// 完成阶段 3
manager.completePhase('demo-001', '收集信息', '已收集 12 个项目的详细信息');
console.log('✅ 阶段 3 完成\n');

// ==================== 阶段 4: 分析与比较 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 4】分析与比较 (30%)');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-001', '分析与比较');
manager.event('demo-001', 'analysis_started');
manager.log('demo-001', '正在比较 3 个重点项目的定位与差异');
manager.setNextAction('demo-001', '完成交叉验证并输出结论');

console.log('📋 默认视图：');
console.log(manager.getDefaultView('demo-001'));
console.log();

// 模拟分析过程
manager.event('demo-001', 'comparison_started', { itemCount: 3 });
manager.updatePhaseProgress('demo-001', '分析与比较', 40, '正在对比技术架构');

manager.event('demo-001', 'cross_validation_started');
manager.log('demo-001', '发现信息不一致，正在交叉验证');
manager.updatePhaseProgress('demo-001', '分析与比较', 70, '正在验证数据来源');

console.log('📋 进度 70%（交叉验证中）：');
console.log(manager.getDefaultView('demo-001'));
console.log();

// 完成阶段 4
manager.completePhase('demo-001', '分析与比较', '已完成 3 个项目的对比分析');
console.log('✅ 阶段 4 完成\n');

// ==================== 阶段 5: 形成输出 ====================

console.log('─────────────────────────────────────────────');
console.log('【阶段 5】形成输出 (15%)');
console.log('─────────────────────────────────────────────\n');

manager.startPhase('demo-001', '形成输出');
manager.event('demo-001', 'output_generating');
manager.log('demo-001', '正在生成结论摘要');
manager.setNextAction('demo-001', '完成最终报告');

console.log('📋 默认视图：');
console.log(manager.getDefaultView('demo-001'));
console.log();

// 完成阶段 5
manager.event('demo-001', 'report_created', { pages: 5 });
manager.completePhase('demo-001', '形成输出', '已生成 5 页研究报告');

// 任务完成
manager.event('demo-001', 'task_completed');

console.log('✅ 阶段 5 完成');
console.log('✅ 任务完成！\n');

// ==================== 最终视图 ====================

console.log('════════════════════════════════════════');
console.log('  最终状态');
console.log('════════════════════════════════════════\n');

console.log('📋 默认视图（完成状态）：');
console.log(manager.getDefaultView('demo-001'));
console.log();

console.log('📋 展开视图：');
console.log(manager.getFullView('demo-001'));
console.log();

console.log('📋 JSON 输出：');
console.log(JSON.stringify(manager.getStatusJSON('demo-001', true), null, 2));
console.log();

console.log('════════════════════════════════════════');
console.log('  Demo 1 完成');
console.log('════════════════════════════════════════\n');
