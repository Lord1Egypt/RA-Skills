#!/usr/bin/env node

/**
 * Harness Engineering Demo - 示例项目
 * 
 * 演示如何使用 Harness Engineering 完成真实任务
 * 
 * 运行:
 * node examples/harness-demo.js
 */

import { HarnessOrchestrator } from '../harness/orchestrator.js';
import { CodeReviewWorkflow } from '../workflows/code-review.js';
import { WALProtocol } from '../memory/wal.js';
import { WorkingBuffer } from '../memory/working-buffer.js';

// ============================================================================
// 示例 1: 多 Agent 并行任务
// ============================================================================

async function demo1_ParallelExecution() {
  console.log('\n' + '='.repeat(60));
  console.log('示例 1: 多 Agent 并行执行');
  console.log('='.repeat(60) + '\n');

  const orchestrator = new HarnessOrchestrator({
    maxParallel: 5,
    timeoutSeconds: 60,
    enableLogging: true,
  });

  // 监听事件
  orchestrator.on('start', ({ task }) => {
    console.log(`🚀 开始执行：${task}`);
  });

  orchestrator.on('task-start', (task) => {
    console.log(`  ▶️  任务开始：${task.id}`);
  });

  orchestrator.on('task-complete', (task) => {
    console.log(`  ✅ 任务完成：${task.id} (${task.duration}ms)`);
  });

  orchestrator.on('complete', (result) => {
    console.log(`\n📊 执行结果:`);
    console.log(`   成功：${result.completed}/${result.total}`);
    console.log(`   总耗时：${result.totalDuration}ms`);
    console.log(`   平均耗时：${result.metadata.avgTime.toFixed(2)}ms`);
  });

  // 执行并行任务
  const result = await orchestrator.execute({
    task: '分析项目代码质量',
    pattern: 'parallel',
    subTasks: [
      { task: '检查代码风格', agent: 'linter', priority: 1 },
      { task: '检查安全漏洞', agent: 'security', priority: 2 },
      { task: '检查性能问题', agent: 'performance', priority: 3 },
      { task: '检查测试覆盖率', agent: 'tester', priority: 4 },
      { task: '检查文档完整性', agent: 'reviewer', priority: 5 },
    ]
  });

  console.log('\n📋 详细结果:');
  console.log(JSON.stringify(result, null, 2));

  return result;
}

// ============================================================================
// 示例 2: 流水线处理
// ============================================================================

async function demo2_PipelineExecution() {
  console.log('\n' + '='.repeat(60));
  console.log('示例 2: 流水线处理 (CI/CD)');
  console.log('='.repeat(60) + '\n');

  const orchestrator = new HarnessOrchestrator({
    maxParallel: 3,
    enableLogging: true,
  });

  const result = await orchestrator.execute({
    task: '发布新版本 v1.0.0',
    pattern: 'pipeline',
    subTasks: [
      // 阶段 1: 构建
      { task: '安装依赖 npm install', stage: 'build', priority: 3 },
      { task: '编译 TypeScript', stage: 'build', priority: 2 },
      { task: '打包资源文件', stage: 'build', priority: 1 },
      
      // 阶段 2: 测试
      { task: '运行单元测试', stage: 'test', priority: 2 },
      { task: '运行集成测试', stage: 'test', priority: 1 },
      
      // 阶段 3: 部署
      { task: '部署到 Staging', stage: 'deploy', priority: 2 },
      { task: '冒烟测试', stage: 'deploy', priority: 1 },
      { task: '部署到 Production', stage: 'deploy', priority: 0 },
    ]
  });

  console.log('\n📊 流水线结果:');
  console.log(`   状态：${result.success ? '✅ 成功' : '❌ 失败'}`);
  console.log(`   完成：${result.completed} 任务`);
  console.log(`   失败：${result.failed} 任务`);
  console.log(`   总耗时：${result.totalDuration}ms`);

  return result;
}

// ============================================================================
// 示例 3: 代码审查工作流
// ============================================================================

async function demo3_CodeReview() {
  console.log('\n' + '='.repeat(60));
  console.log('示例 3: 代码审查工作流');
  console.log('='.repeat(60) + '\n');

  const workflow = new CodeReviewWorkflow({
    enableLint: true,
    enableSecurity: true,
    enablePerformance: true,
    enableTests: true,
    minApprovalScore: 0.8,
  });

  const result = await workflow.execute({
    prNumber: 123,
    files: ['src/auth.js', 'src/user.js', 'src/api.js'],
    repo: 'my-org/my-project',
    autoComment: false,
  });

  console.log('\n📊 审查报告:');
  console.log(`   PR: #${result.report.prNumber}`);
  console.log(`   评分：${(result.report.score * 100).toFixed(0)}/100`);
  console.log(`   结果：${result.report.approval ? '✅ 通过' : '❌ 需要修复'}`);
  console.log(`   文件数：${result.report.filesReviewed}`);
  console.log(`\n   问题统计:`);
  console.log(`     🔴 严重：${result.report.summary.critical}`);
  console.log(`     🟠 主要：${result.report.summary.major}`);
  console.log(`     🟡 次要：${result.report.summary.minor}`);
  console.log(`     💡 建议：${result.report.summary.suggestion}`);

  if (result.report.recommendations.length > 0) {
    console.log(`\n   建议:`);
    for (const rec of result.report.recommendations) {
      console.log(`     - [${rec.priority}] ${rec.action}`);
    }
  }

  return result;
}

// ============================================================================
// 示例 4: WAL 持久化
// ============================================================================

async function demo4_WAL() {
  console.log('\n' + '='.repeat(60));
  console.log('示例 4: WAL 预写日志协议');
  console.log('='.repeat(60) + '\n');

  const wal = new WALProtocol({
    walDir: './examples/fixtures/wal-demo',
    enableCompaction: false,
  });

  console.log('📝 记录任务执行过程...\n');

  // 开始事务
  await wal.begin('task-demo-001', {
    type: 'code-review',
    prNumber: 456,
  });
  console.log('  ✅ 事务开始：task-demo-001');

  // 记录进度
  await wal.log('task-demo-001', 'start', {
    files: ['a.js', 'b.js', 'c.js'],
  });
  console.log('  ✅ 记录：开始审查');

  await wal.log('task-demo-001', 'progress', {
    completed: 1,
    total: 3,
    currentFile: 'b.js',
  });
  console.log('  ✅ 记录：进度 1/3');

  await wal.log('task-demo-001', 'progress', {
    completed: 2,
    total: 3,
    currentFile: 'c.js',
  });
  console.log('  ✅ 记录：进度 2/3');

  await wal.log('task-demo-001', 'complete', {
    result: 'success',
    score: 0.85,
    issues: 3,
  });
  console.log('  ✅ 记录：审查完成');

  // 提交事务
  const commitResult = await wal.commit('task-demo-001');
  console.log(`  ✅ 事务提交：耗时 ${commitResult.duration}ms`);

  // 获取统计
  const stats = wal.getStats();
  console.log(`\n📊 WAL 统计:`);
  console.log(`   序列号：${stats.sequence}`);
  console.log(`   活跃事务：${stats.activeTransactions}`);
  console.log(`   当前段：${stats.currentSegment}`);

  // 恢复演示
  console.log(`\n🔄 模拟崩溃恢复...`);
  const recovery = await wal.recover();
  console.log(`   恢复完成：${recovery.incomplete.length} 个未完成事务`);

  return { commitResult, stats, recovery };
}

// ============================================================================
// 示例 5: Working Buffer
// ============================================================================

async function demo5_WorkingBuffer() {
  console.log('\n' + '='.repeat(60));
  console.log('示例 5: Working Buffer 工作缓冲区');
  console.log('='.repeat(60) + '\n');

  const buffer = new WorkingBuffer({
    bufferDir: './examples/fixtures/buffer-demo',
    autoSave: true,
    autoSaveInterval: 5000,
    maxAge: 3600000,  // 1 小时
  });

  console.log('💾 保存任务状态...\n');

  // 保存状态
  await buffer.set('task-001', {
    status: 'running',
    progress: 25,
    currentStep: 'analyzing',
  });
  console.log('  ✅ 保存：task-001 (25%)');

  await buffer.set('task-002', {
    status: 'running',
    progress: 50,
    currentStep: 'processing',
  });
  console.log('  ✅ 保存：task-002 (50%)');

  await buffer.set('task-003', {
    status: 'running',
    progress: 75,
    currentStep: 'validating',
  });
  console.log('  ✅ 保存：task-003 (75%)');

  // 获取状态
  console.log('\n📖 读取任务状态...\n');
  
  const { found, value } = await buffer.get('task-002');
  if (found) {
    console.log(`  ✅ task-002: ${value.progress}% - ${value.currentStep}`);
  }

  // 更新状态
  await buffer.set('task-002', {
    ...value,
    progress: 100,
    currentStep: 'completed',
  });
  console.log('  ✅ 更新：task-002 (100%)');

  // 获取统计
  const stats = buffer.getStats();
  console.log(`\n📊 Buffer 统计:`);
  console.log(`   条目数：${stats.count}`);
  console.log(`   总访问：${stats.totalAccessCount}`);
  console.log(`   自动保存：${stats.autoSaveEnabled ? '✅' : '❌'}`);
  console.log(`   最大年龄：${stats.maxAge}`);

  // 持久化演示
  console.log(`\n💾 保存到磁盘...`);
  await buffer.save();
  console.log('  ✅ 保存完成');

  return stats;
}

// ============================================================================
// 主函数
// ============================================================================

async function main() {
  console.log('\n╔══════════════════════════════════════════════════════════╗');
  console.log('║       Harness Engineering 演示项目                       ║');
  console.log('║       多 Agent 编排 · 生产工作流 · 自进化系统            ║');
  console.log('╚══════════════════════════════════════════════════════════╝');

  try {
    // 运行所有演示
    await demo1_ParallelExecution();
    await demo2_PipelineExecution();
    await demo3_CodeReview();
    await demo4_WAL();
    await demo5_WorkingBuffer();

    console.log('\n' + '='.repeat(60));
    console.log('✅ 所有演示完成！');
    console.log('='.repeat(60) + '\n');

  } catch (error) {
    console.error('\n❌ 演示执行失败:', error);
    process.exit(1);
  }
}

// 运行演示
main();
