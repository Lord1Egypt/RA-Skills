/**
 * Manager-Worker Agent 单元测试
 * 
 * 运行方式：node tests/manager-worker-agent.test.js
 */

const { ManagerAgent, WorkerAgent } = require('../src/agents/manager-worker-agent');

// ============================================
// Mock LLM
// ============================================

class MockLLM {
  constructor(responses) {
    this.responses = responses || [];
    this.callCount = 0;
  }

  async generate(prompt) {
    this.callCount++;
    const response = this.responses[this.callCount - 1];
    
    if (response === undefined) {
      throw new Error(`No mock response for call ${this.callCount}`);
    }
    
    return response;
  }

  reset() {
    this.callCount = 0;
  }
}

// ============================================
// Test Utilities
// ============================================

let passedTests = 0;
let failedTests = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✅ ${message}`);
    passedTests++;
  } else {
    console.error(`  ❌ ${message}`);
    failedTests++;
  }
}

function assertEqual(actual, expected, message) {
  if (actual === expected) {
    console.log(`  ✅ ${message}`);
    passedTests++;
  } else {
    console.error(`  ❌ ${message}`);
    console.error(`     Expected: ${expected}`);
    console.error(`     Actual:   ${actual}`);
    failedTests++;
  }
}

function assertArrayEqual(actual, expected, message) {
  const equal = Array.isArray(actual) && Array.isArray(expected) &&
                actual.length === expected.length &&
                actual.every((v, i) => v === expected[i]);
  
  if (equal) {
    console.log(`  ✅ ${message}`);
    passedTests++;
  } else {
    console.error(`  ❌ ${message}`);
    console.error(`     Expected: ${JSON.stringify(expected)}`);
    console.error(`     Actual:   ${JSON.stringify(actual)}`);
    failedTests++;
  }
}

// ============================================
// Tests
// ============================================

async function testWorkerAgent() {
  console.log('\n=== Worker Agent 测试 ===\n');
  
  // Test 1: Worker 创建测试
  console.log('Test 1: Worker 创建测试');
  {
    const worker = new WorkerAgent('worker-1', ['javascript', 'python'], {});
    
    assertEqual(worker.id, 'worker-1', 'Worker ID 正确');
    assertArrayEqual(worker.skills, ['javascript', 'python'], '技能列表正确');
  }
  
  // Test 2: Worker 技能匹配测试
  console.log('\nTest 2: Worker 技能匹配测试');
  {
    const worker = new WorkerAgent('worker-1', ['javascript', 'react'], {});
    
    const llm = new MockLLM(['task result']);
    worker.llm = llm;
    
    const subtask = {
      description: '测试任务',
      requiredSkills: ['javascript']
    };
    
    try {
      const result = await worker.execute(subtask);
      assertEqual(result, 'task result', 'Worker 正确执行任务');
    } catch (error) {
      assert(false, `执行失败：${error.message}`);
    }
  }
}

async function testManagerAgent() {
  console.log('\n=== Manager Agent 测试 ===\n');
  
  // Test 1: Manager 创建测试
  console.log('Test 1: Manager 创建测试');
  {
    const workers = [
      new WorkerAgent('worker-1', ['javascript'], {}),
      new WorkerAgent('worker-2', ['python'], {})
    ];
    
    const manager = new ManagerAgent(workers, {
      maxRetries: 3,
      timeout: 30000,
      verbose: false
    });
    
    assertEqual(manager.workers.length, 2, 'Worker 数量正确');
    assertEqual(manager.maxRetries, 3, '最大重试次数正确');
  }
  
  // Test 2: 任务分解测试
  console.log('\nTest 2: 任务分解测试');
  {
    const workers = [
      new WorkerAgent('worker-1', ['javascript'], {})
    ];
    
    const llm = new MockLLM([
      JSON.stringify([
        { id: 'task-1', description: '子任务 1', requiredSkills: [] },
        { id: 'task-2', description: '子任务 2', requiredSkills: [] }
      ])
    ]);
    
    const manager = new ManagerAgent(workers, { llm, verbose: false });
    
    try {
      const subtasks = await manager.decompose('测试任务');
      assertEqual(subtasks.length, 2, '分解为 2 个子任务');
      assertEqual(subtasks[0].id, 'task-1', '子任务 ID 正确');
    } catch (error) {
      assert(false, `分解失败：${error.message}`);
    }
  }
  
  // Test 3: Worker 选择测试（技能匹配）
  console.log('\nTest 3: Worker 选择测试（技能匹配）');
  {
    const workers = [
      new WorkerAgent('worker-1', ['javascript', 'react'], {}),
      new WorkerAgent('worker-2', ['python', 'django'], {}),
      new WorkerAgent('worker-3', ['javascript', 'nodejs'], {})
    ];
    
    const manager = new ManagerAgent(workers, { verbose: false });
    
    const subtask = {
      description: 'React 开发',
      requiredSkills: ['react', 'javascript']
    };
    
    const selectedWorker = manager.selectWorker(subtask);
    
    // 应该选择 worker-1（技能完全匹配）
    assertEqual(
      selectedWorker.id,
      'worker-1',
      '选择技能最匹配的 Worker'
    );
    
    // 验证匹配分数计算
    const score1 = manager.calculateMatchScore(workers[0], ['react', 'javascript']);
    const score2 = manager.calculateMatchScore(workers[1], ['react', 'javascript']);
    const score3 = manager.calculateMatchScore(workers[2], ['react', 'javascript']);
    
    assert(score1 === 1.0, 'worker-1 匹配分数 1.0（完全匹配）');
    assert(score2 === 0.0, 'worker-2 匹配分数 0.0（不匹配）');
    assert(score3 === 0.5, 'worker-3 匹配分数 0.5（部分匹配）');
  }
  
  // Test 4: 任务分配测试
  console.log('\nTest 4: 任务分配测试');
  {
    const workers = [
      new WorkerAgent('worker-1', ['javascript'], {}),
      new WorkerAgent('worker-2', ['python'], {})
    ];
    
    const manager = new ManagerAgent(workers, { verbose: false });
    
    const subtasks = [
      { id: 'task-1', description: 'JS 任务', requiredSkills: ['javascript'] },
      { id: 'task-2', description: 'Python 任务', requiredSkills: ['python'] },
      { id: 'task-3', description: 'JS 任务 2', requiredSkills: ['javascript'] }
    ];
    
    const assignments = manager.assign(subtasks);
    
    // worker-1 应该分配到 2 个 JS 任务
    const worker1Tasks = assignments.get('worker-1') || [];
    assertEqual(worker1Tasks.length, 2, 'worker-1 分配到 2 个任务');
    
    // worker-2 应该分配到 1 个 Python 任务
    const worker2Tasks = assignments.get('worker-2') || [];
    assertEqual(worker2Tasks.length, 1, 'worker-2 分配到 1 个任务');
  }
  
  // Test 5: 超时处理测试
  console.log('\nTest 5: 超时处理测试');
  {
    const workers = [
      new WorkerAgent('worker-1', [], {})
    ];
    
    // Mock worker 执行很慢
    workers[0].execute = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      return 'result';
    };
    
    const manager = new ManagerAgent(workers, {
      timeout: 100, // 100ms 超时
      verbose: false
    });
    
    const subtask = { description: '慢任务' };
    
    try {
      const result = await manager.executeWithRetry(workers[0], subtask);
      assert(!result.success, '超时任务应该失败');
      assert(
        result.error.includes('Timeout'),
        '错误信息包含 Timeout'
      );
    } catch (error) {
      assert(false, `测试失败：${error.message}`);
    }
  }
  
  // Test 6: 重试机制测试
  console.log('\nTest 6: 重试机制测试');
  {
    const workers = [
      new WorkerAgent('worker-1', [], {})
    ];
    
    let callCount = 0;
    workers[0].execute = async () => {
      callCount++;
      if (callCount < 3) {
        throw new Error('临时错误');
      }
      return 'success';
    };
    
    const manager = new ManagerAgent(workers, {
      maxRetries: 3,
      verbose: false
    });
    
    const subtask = { description: '测试任务' };
    
    try {
      const result = await manager.executeWithRetry(workers[0], subtask);
      assert(result.success, '重试后成功');
      assertEqual(callCount, 3, '重试了 3 次');
    } catch (error) {
      assert(false, `测试失败：${error.message}`);
    }
  }
  
  // Test 7: 结果整合测试
  console.log('\nTest 7: 结果整合测试');
  {
    const workers = [
      new WorkerAgent('worker-1', [], {})
    ];
    
    const llm = new MockLLM(['整合后的最终结果']);
    
    const manager = new ManagerAgent(workers, { llm, verbose: false });
    
    const results = [
      { taskId: 'task-1', success: true, result: '结果 1', worker: 'worker-1' },
      { taskId: 'task-2', success: true, result: '结果 2', worker: 'worker-1' },
      { taskId: 'task-3', success: false, error: '失败', worker: 'worker-1' }
    ];
    
    try {
      const finalResult = await manager.integrate('测试任务', results);
      assertEqual(finalResult, '整合后的最终结果', '整合结果正确');
    } catch (error) {
      assert(false, `整合失败：${error.message}`);
    }
  }
  
  // Test 8: 并行执行测试
  console.log('\nTest 8: 并行执行测试');
  {
    const workers = [
      new WorkerAgent('worker-1', [], {}),
      new WorkerAgent('worker-2', [], {})
    ];
    
    const executionTimes = [];
    
    workers[0].execute = async () => {
      executionTimes.push({ worker: 'worker-1', time: Date.now() });
      return 'result-1';
    };
    
    workers[1].execute = async () => {
      executionTimes.push({ worker: 'worker-2', time: Date.now() });
      return 'result-2';
    };
    
    const manager = new ManagerAgent(workers, { verbose: false });
    
    const assignments = new Map([
      ['worker-1', [{ id: 'task-1', description: '任务 1' }]],
      ['worker-2', [{ id: 'task-2', description: '任务 2' }]]
    ]);
    
    try {
      const results = await manager.executeParallel(assignments);
      assertEqual(results.length, 2, '收到 2 个结果');
      
      // 验证并行执行（时间差应该很小）
      if (executionTimes.length === 2) {
        const timeDiff = Math.abs(executionTimes[0].time - executionTimes[1].time);
        assert(timeDiff < 100, '任务是并行执行的');
      }
    } catch (error) {
      assert(false, `并行执行失败：${error.message}`);
    }
  }
}

async function testIntegration() {
  console.log('\n=== 集成测试 ===\n');
  
  // Test: 完整流程测试
  console.log('Test: 完整流程测试（简化版）');
  {
    const workers = [
      new WorkerAgent('worker-1', ['javascript'], {}),
      new WorkerAgent('worker-2', ['python'], {})
    ];
    
    const llm = new MockLLM([
      // 分解
      JSON.stringify([
        { id: 'task-1', description: 'JS 任务', requiredSkills: ['javascript'] },
        { id: 'task-2', description: 'Python 任务', requiredSkills: ['python'] }
      ]),
      // 整合
      '最终结果'
    ]);
    
    // Mock worker 执行
    workers[0].execute = async () => 'JS 结果';
    workers[1].execute = async () => 'Python 结果';
    
    const manager = new ManagerAgent(workers, { llm, verbose: false });
    
    try {
      const result = await manager.coordinate('完整测试任务');
      assertEqual(result, '最终结果', '完整流程返回正确结果');
    } catch (error) {
      assert(false, `完整流程失败：${error.message}`);
    }
  }
}

// ============================================
// Run Tests
// ============================================

async function runAllTests() {
  console.log('🧪 开始运行 Manager-Worker Agent 单元测试...\n');
  
  const startTime = Date.now();
  
  await testWorkerAgent();
  await testManagerAgent();
  await testIntegration();
  
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  console.log('\n=== 测试结果 ===');
  console.log(`总测试数：${passedTests + failedTests}`);
  console.log(`✅ 通过：${passedTests}`);
  console.log(`❌ 失败：${failedTests}`);
  console.log(`⏱️  耗时：${duration}ms`);
  
  if (failedTests === 0) {
    console.log('\n🎉 所有测试通过！');
  } else {
    console.error(`\n⚠️  有 ${failedTests} 个测试失败`);
    process.exit(1);
  }
}

// ============================================
// Main
// ============================================

runAllTests().catch(error => {
  console.error('测试运行失败:', error);
  process.exit(1);
});
