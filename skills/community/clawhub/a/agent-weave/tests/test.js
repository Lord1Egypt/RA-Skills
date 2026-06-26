/**
 * Agent-Weave 基础测试
 */

const { Loom } = require('../lib/index.js');

console.log('🧪 Agent-Weave 基础测试\n');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (err) {
    console.log(`❌ ${name}: ${err.message}`);
    failed++;
  }
}

// 测试1: 导入
test('导入 Loom', () => {
  if (typeof Loom !== 'function') {
    throw new Error('Loom 不是函数');
  }
});

// 测试2: 创建实例
test('创建 Loom 实例', () => {
  const loom = new Loom();
  if (!loom) {
    throw new Error('创建失败');
  }
});

// 测试3: 创建 Master
test('创建 Master', () => {
  const loom = new Loom();
  const master = loom.createMaster('test');
  if (!master) {
    throw new Error('Master 创建失败');
  }
});

// 测试4: 创建 Workers
test('创建 Workers', () => {
  const loom = new Loom();
  const master = loom.createMaster('test');
  master.spawn(3, (x) => x * 2);
  if (master.workers.size !== 3) {
    throw new Error(`Worker 数量错误: ${master.workers.size}`);
  }
});

// 测试5: 任务分发（异步）
async function testDispatch() {
  try {
    const loom = new Loom();
    const master = loom.createMaster('test');
    master.spawn(3, (x) => x * 2);
    
    const result = await master.dispatch([1, 2, 3, 4, 5]);
    
    if (result.summary.success !== 5) {
      throw new Error(`任务成功数错误: ${result.summary.success}`);
    }
    
    console.log('✅ 任务分发和执行');
    passed++;
    
    master.destroy();
  } catch (err) {
    console.log(`❌ 任务分发和执行: ${err.message}`);
    failed++;
  }
}

// 运行异步测试
(async () => {
  await testDispatch();
  
  // 最终报告
  console.log('\n' + '='.repeat(40));
  console.log('              测试报告');
  console.log('='.repeat(40));
  console.log(`总测试: ${passed + failed}`);
  console.log(`✅ 通过: ${passed}`);
  console.log(`❌ 失败: ${failed}`);
  console.log(`成功率: ${(((passed / (passed + failed)) * 100) || 0).toFixed(2)}%`);
  console.log('='.repeat(40) + '\n');
  
  process.exit(failed > 0 ? 1 : 0);
})();
