/**
 * Test Suite - 测试套件索引
 * 
 * 运行所有测试：
 * node tests/test-suite.js
 * 
 * 运行单个测试：
 * node tests/test-suite.js --test=orchestrator
 */

import { HarnessOrchestrator } from '../harness/orchestrator.js';
import { CodeReviewWorkflow } from '../workflows/code-review.js';
import { WALProtocol } from '../memory/wal.js';
import { WorkingBuffer } from '../memory/working-buffer.js';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';

// ============================================================================
// 测试工具
// ============================================================================

const TestStatus = {
  PASS: '✅ PASS',
  FAIL: '❌ FAIL',
  SKIP: '⏭️  SKIP',
};

class TestRunner {
  constructor() {
    this.results = [];
    this.startTime = Date.now();
  }

  async run(name, fn) {
    try {
      await fn();
      this.results.push({ name, status: TestStatus.PASS, error: null });
      console.log(`${TestStatus.PASS} ${name}`);
    } catch (error) {
      this.results.push({ name, status: TestStatus.FAIL, error: error.message });
      console.error(`${TestStatus.FAIL} ${name}`);
      console.error(`  Error: ${error.message}`);
    }
  }

  summary() {
    const total = this.results.length;
    const passed = this.results.filter(r => r.status === TestStatus.PASS).length;
    const failed = this.results.filter(r => r.status === TestStatus.FAIL).length;
    const duration = Date.now() - this.startTime;

    console.log('\n' + '='.repeat(60));
    console.log(`测试完成：${total} 个测试，${passed} 通过，${failed} 失败，耗时 ${duration}ms`);
    console.log('='.repeat(60));

    if (failed > 0) {
      console.log('\n失败的测试:');
      for (const result of this.results.filter(r => r.status === TestStatus.FAIL)) {
        console.log(`  - ${result.name}: ${result.error}`);
      }
    }

    return { total, passed, failed, duration };
  }
}

// ============================================================================
// 测试：Harness Orchestrator
// ============================================================================

async function testOrchestrator(runner) {
  console.log('\n📦 Testing Harness Orchestrator...\n');

  await runner.run('Orchestrator: 创建实例', async () => {
    const orchestrator = new HarnessOrchestrator({
      maxParallel: 3,
      timeoutSeconds: 30,
      enableLogging: false,
    });
    if (!orchestrator) throw new Error('Failed to create orchestrator');
  });

  await runner.run('Orchestrator: 并行执行任务', async () => {
    const orchestrator = new HarnessOrchestrator({ enableLogging: false });
    
    const result = await orchestrator.execute({
      task: '测试并行执行',
      pattern: 'parallel',
      subTasks: [
        { task: '任务 1', priority: 1 },
        { task: '任务 2', priority: 2 },
        { task: '任务 3', priority: 3 },
      ]
    });

    if (!result.success) throw new Error('Parallel execution failed');
    if (result.completed !== 3) throw new Error(`Expected 3 completed, got ${result.completed}`);
  });

  await runner.run('Orchestrator: 顺序执行任务', async () => {
    const orchestrator = new HarnessOrchestrator({ enableLogging: false });
    
    const result = await orchestrator.execute({
      task: '测试顺序执行',
      pattern: 'sequential',
      subTasks: [
        { task: '步骤 1' },
        { task: '步骤 2', dependencies: ['task-1'] },
        { task: '步骤 3', dependencies: ['task-2'] },
      ]
    });

    if (!result.success) throw new Error('Sequential execution failed');
  });

  await runner.run('Orchestrator: 获取状态', async () => {
    const orchestrator = new HarnessOrchestrator({ enableLogging: false });
    const status = orchestrator.getStatus();
    
    if (!status.isRunning === undefined) throw new Error('Invalid status');
    if (!Array.isArray(status.tasks)) throw new Error('Invalid tasks');
  });

  await runner.run('Orchestrator: 事件监听', async () => {
    const orchestrator = new HarnessOrchestrator({ enableLogging: false });
    let eventFired = false;

    orchestrator.on('start', () => { eventFired = true; });

    await orchestrator.execute({
      task: '测试事件',
      pattern: 'parallel',
      subTasks: [{ task: '子任务' }]
    });

    if (!eventFired) throw new Error('Start event not fired');
  });
}

// ============================================================================
// 测试：Workflows
// ============================================================================

async function testWorkflows(runner) {
  console.log('\n📦 Testing Workflows...\n');

  await runner.run('Workflow: 创建 CodeReviewWorkflow', async () => {
    const workflow = new CodeReviewWorkflow({ enableLogging: false });
    if (!workflow) throw new Error('Failed to create workflow');
  });

  await runner.run('Workflow: CodeReview 执行', async () => {
    const workflow = new CodeReviewWorkflow({
      enableLogging: false,
      enableLint: false,  // 跳过实际检查
      enableSecurity: false,
      enablePerformance: false,
      enableTests: false,
    });

    const result = await workflow.execute({
      prNumber: 999,
      files: ['test.js'],
      autoComment: false,
    });

    if (!result.success) throw new Error('CodeReview workflow failed');
    if (!result.report) throw new Error('No report generated');
  });

  await runner.run('Workflow: 生成审查报告', async () => {
    const workflow = new CodeReviewWorkflow({ enableLogging: false });
    
    const mockResult = {
      outputs: [
        { issues: [{ severity: 'major', description: 'Test issue' }], summary: 'OK' }
      ],
      errors: [],
    };

    const report = workflow.generateReport(mockResult, {
      prNumber: 123,
      files: ['test.js'],
    });

    if (!report.score) throw new Error('No score in report');
    if (!report.summary) throw new Error('No summary in report');
  });
}

// ============================================================================
// 测试：WAL Protocol
// ============================================================================

async function testWAL(runner) {
  console.log('\n📦 Testing WAL Protocol...\n');

  const walDir = './tests/fixtures/wal-test';
  if (!existsSync(walDir)) {
    mkdirSync(walDir, { recursive: true });
  }

  await runner.run('WAL: 创建实例', async () => {
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    if (!wal) throw new Error('Failed to create WAL');
  });

  await runner.run('WAL: 开始事务', async () => {
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    const result = await wal.begin('tx-1', { type: 'test' });
    
    if (!result.transactionId) throw new Error('No transaction ID');
    if (!result.sequence) throw new Error('No sequence number');
  });

  await runner.run('WAL: 记录日志', async () => {
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    
    await wal.begin('tx-2', { type: 'test' });
    const result = await wal.log('tx-2', 'progress', { step: 1 });
    
    if (!result.sequence) throw new Error('No sequence number');
  });

  await runner.run('WAL: 提交事务', async () => {
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    
    await wal.begin('tx-3', { type: 'test' });
    await wal.log('tx-3', 'data', { value: 'test' });
    const result = await wal.commit('tx-3');
    
    if (!result.committed) throw new Error('Commit failed');
    if (!result.sequence) throw new Error('No sequence number');
  });

  await runner.run('WAL: 回滚事务', async () => {
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    
    await wal.begin('tx-4', { type: 'test' });
    const result = await wal.abort('tx-4');
    
    if (!result.aborted) throw new Error('Abort failed');
  });

  await runner.run('WAL: 获取统计', async () => {
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    const stats = wal.getStats();
    
    if (stats.sequence === undefined) throw new Error('No sequence in stats');
    if (stats.activeTransactions === undefined) throw new Error('No activeTransactions in stats');
  });

  await runner.run('WAL: 恢复', async () => {
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    const recovery = await wal.recover();
    
    if (recovery.incomplete === undefined) throw new Error('No incomplete in recovery');
    if (recovery.totalEntries === undefined) throw new Error('No totalEntries in recovery');
  });
}

// ============================================================================
// 测试：Working Buffer
// ============================================================================

async function testWorkingBuffer(runner) {
  console.log('\n📦 Testing Working Buffer...\n');

  const bufferDir = './tests/fixtures/buffer-test';
  if (!existsSync(bufferDir)) {
    mkdirSync(bufferDir, { recursive: true });
  }

  await runner.run('Buffer: 创建实例', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    if (!buffer) throw new Error('Failed to create buffer');
  });

  await runner.run('Buffer: 设置值', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    const result = await buffer.set('key-1', { value: 'test' });
    
    if (!result.key) throw new Error('No key in result');
  });

  await runner.run('Buffer: 获取值', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    
    await buffer.set('key-2', { value: 'test-2' });
    const result = await buffer.get('key-2');
    
    if (!result.found) throw new Error('Key not found');
    if (result.value.value !== 'test-2') throw new Error('Invalid value');
  });

  await runner.run('Buffer: 获取不存在的值', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    const result = await buffer.get('non-existent-key');
    
    if (result.found) throw new Error('Should not find non-existent key');
  });

  await runner.run('Buffer: 删除值', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    
    await buffer.set('key-3', { value: 'test-3' });
    const deleted = await buffer.delete('key-3');
    
    if (!deleted) throw new Error('Delete failed');
    
    const result = await buffer.get('key-3');
    if (result.found) throw new Error('Key should be deleted');
  });

  await runner.run('Buffer: 获取大小', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    
    await buffer.set('key-4', {});
    await buffer.set('key-5', {});
    
    const size = buffer.size();
    if (size < 2) throw new Error(`Expected size >= 2, got ${size}`);
  });

  await runner.run('Buffer: 获取统计', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    const stats = buffer.getStats();
    
    if (stats.count === undefined) throw new Error('No count in stats');
    if (stats.autoSaveEnabled === undefined) throw new Error('No autoSaveEnabled in stats');
  });

  await runner.run('Buffer: 保存和加载', async () => {
    const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
    
    await buffer.set('persist-key', { data: 'test-data' });
    await buffer.save();
    
    // 创建新实例加载
    const buffer2 = new WorkingBuffer({ bufferDir, autoSave: false });
    const result = await buffer2.get('persist-key');
    
    if (!result.found) throw new Error('Failed to load persisted data');
    if (result.value.data !== 'test-data') throw new Error('Invalid persisted data');
  });
}

// ============================================================================
// 性能基准测试
// ============================================================================

async function runBenchmarks() {
  console.log('\n⏱️  Running Benchmarks...\n');

  const benchmarks = {
    orchestrator: { iterations: 0, avgDuration: 0 },
    wal: { iterations: 0, avgDuration: 0 },
    buffer: { iterations: 0, avgDuration: 0 },
  };

  // 基准测试：Orchestrator
  console.log('Benchmark: Orchestrator (10 次并行执行)');
  const orchestratorDurations = [];
  for (let i = 0; i < 10; i++) {
    const start = Date.now();
    const orchestrator = new HarnessOrchestrator({ enableLogging: false });
    await orchestrator.execute({
      task: '基准测试',
      pattern: 'parallel',
      subTasks: Array.from({ length: 5 }, (_, j) => ({ task: `子任务${j}` }))
    });
    orchestratorDurations.push(Date.now() - start);
  }
  benchmarks.orchestrator.iterations = 10;
  benchmarks.orchestrator.avgDuration = 
    orchestratorDurations.reduce((a, b) => a + b, 0) / orchestratorDurations.length;
  console.log(`  平均耗时：${benchmarks.orchestrator.avgDuration}ms\n`);

  // 基准测试：WAL
  console.log('Benchmark: WAL (100 次事务)');
  const walDir = './tests/fixtures/wal-benchmark';
  if (!existsSync(walDir)) mkdirSync(walDir, { recursive: true });
  
  const walDurations = [];
  for (let i = 0; i < 100; i++) {
    const start = Date.now();
    const wal = new WALProtocol({ walDir, enableCompaction: false });
    await wal.begin(`tx-${i}`, { type: 'benchmark' });
    await wal.log(`tx-${i}`, 'data', { i });
    await wal.commit(`tx-${i}`);
    walDurations.push(Date.now() - start);
  }
  benchmarks.wal.iterations = 100;
  benchmarks.wal.avgDuration = 
    walDurations.reduce((a, b) => a + b, 0) / walDurations.length;
  console.log(`  平均耗时：${benchmarks.wal.avgDuration}ms\n`);

  // 基准测试：Buffer
  console.log('Benchmark: Buffer (100 次读写)');
  const bufferDir = './tests/fixtures/buffer-benchmark';
  if (!existsSync(bufferDir)) mkdirSync(bufferDir, { recursive: true });
  
  const bufferDurations = [];
  const buffer = new WorkingBuffer({ bufferDir, autoSave: false });
  for (let i = 0; i < 100; i++) {
    const start = Date.now();
    await buffer.set(`key-${i}`, { i });
    await buffer.get(`key-${i}`);
    bufferDurations.push(Date.now() - start);
  }
  benchmarks.buffer.iterations = 100;
  benchmarks.buffer.avgDuration = 
    bufferDurations.reduce((a, b) => a + b, 0) / bufferDurations.length;
  console.log(`  平均耗时：${benchmarks.buffer.avgDuration}ms\n`);

  return benchmarks;
}

// ============================================================================
// 主函数
// ============================================================================

async function main() {
  console.log('='.repeat(60));
  console.log('Harness Engineering 测试套件');
  console.log('='.repeat(60));

  const runner = new TestRunner();

  // 运行单元测试
  await testOrchestrator(runner);
  await testWorkflows(runner);
  await testWAL(runner);
  await testWorkingBuffer(runner);

  // 运行基准测试
  const benchmarks = await runBenchmarks();

  // 生成报告
  const summary = runner.summary();

  // 保存报告
  const report = {
    timestamp: new Date().toISOString(),
    summary,
    benchmarks,
    details: runner.results,
  };

  const reportPath = './tests/BENCHMARKS.md';
  const reportContent = `# 性能基准测试报告

**生成时间**: ${report.timestamp}

## 测试摘要

| 指标 | 值 |
|------|-----|
| 总测试数 | ${summary.total} |
| 通过 | ${summary.passed} |
| 失败 | ${summary.failed} |
| 通过率 | ${(summary.passed / summary.total * 100).toFixed(1)}% |
| 总耗时 | ${summary.duration}ms |

## 性能基准

| 组件 | 迭代次数 | 平均耗时 |
|------|---------|---------|
| Orchestrator | ${benchmarks.orchestrator.iterations} | ${benchmarks.orchestrator.avgDuration.toFixed(2)}ms |
| WAL | ${benchmarks.wal.iterations} | ${benchmarks.wal.avgDuration.toFixed(2)}ms |
| Buffer | ${benchmarks.buffer.iterations} | ${benchmarks.buffer.avgDuration.toFixed(2)}ms |

## 详细结果

${runner.results.map(r => `- ${r.status} ${r.name}${r.error ? ': ' + r.error : ''}`).join('\n')}

---

*报告生成于 ${new Date().toLocaleString('zh-CN')}*
`;

  writeFileSync(reportPath, reportContent);
  console.log(`\n📊 报告已保存到 ${reportPath}`);

  // 返回退出码
  process.exit(summary.failed > 0 ? 1 : 0);
}

// 运行测试
main().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});
