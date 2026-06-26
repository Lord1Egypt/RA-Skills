/**
 * Dreaming Guard Pro - Phase 4 Tests
 * 
 * 测试 Protector 和 Healer 模块
 * 运行时间 < 10秒，不实际重启gateway
 */

const assert = require('assert');
const path = require('path');
const fs = require('fs');
const os = require('os');

// 设置测试模式
process.env.HEALER_TEST_MODE = 'true';

// 导入模块
const Protector = require('../src/protector');
const Healer = require('../src/healer');
const { INTERVENTION_LEVELS, MEMORY_THRESHOLDS } = require('../src/protector');
const { RECOVERY_STATUS } = require('../src/healer');

// 测试工具
const testDir = path.join(os.homedir(), '.openclaw', 'test-dreaming-guard');
const dreamingPath = path.join(testDir, 'memory', '.dreams');

// 创建测试环境
function setupTestEnv() {
  // 清理旧测试目录
  if (fs.existsSync(testDir)) {
    fs.rmSync(testDir, { recursive: true, force: true });
  }
  
  // 创建测试目录
  fs.mkdirSync(dreamingPath, { recursive: true });
  
  // 创建测试文件
  const testFile1 = path.join(dreamingPath, 'test-1.json');
  fs.writeFileSync(testFile1, JSON.stringify([
    { timestamp: Date.now(), type: 'test', data: 'entry1' },
    { timestamp: Date.now(), type: 'test', data: 'entry2' }
  ]));
  
  const testFile2 = path.join(dreamingPath, 'test-2.jsonl');
  fs.writeFileSync(testFile2, 
    JSON.stringify({ timestamp: Date.now(), type: 'log' }) + '\n' +
    JSON.stringify({ timestamp: Date.now(), type: 'log' }) + '\n'
  );
}

// 清理测试环境
function cleanupTestEnv() {
  if (fs.existsSync(testDir)) {
    fs.rmSync(testDir, { recursive: true, force: true });
  }
}

// 测试计数
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (err) {
    console.log(`✗ ${name}: ${err.message}`);
    failed++;
  }
}

// ========== Protector Tests ==========

console.log('\n=== Protector Tests ===\n');

test('Protector should initialize correctly', () => {
  const protector = new Protector({ maxMemoryMB: 256 });
  assert.ok(protector);
  assert.strictEqual(protector.config.maxMemoryMB, 256);
  assert.strictEqual(protector.running, false);
});

test('Protector should have correct thresholds', () => {
  assert.strictEqual(MEMORY_THRESHOLDS.warning, 0.70);
  assert.strictEqual(MEMORY_THRESHOLDS.critical, 0.85);
  assert.strictEqual(MEMORY_THRESHOLDS.emergency, 0.95);
});

test('Protector.getIntervention should return correct levels', () => {
  const protector = new Protector();
  
  // Normal
  let result = protector.getIntervention(0.5);
  assert.strictEqual(result.level, INTERVENTION_LEVELS.NORMAL);
  
  // Warning
  result = protector.getIntervention(0.75);
  assert.strictEqual(result.level, INTERVENTION_LEVELS.WARNING);
  assert.ok(result.actions.includes('compress'));
  
  // Critical
  result = protector.getIntervention(0.90);
  assert.strictEqual(result.level, INTERVENTION_LEVELS.CRITICAL);
  assert.ok(result.actions.includes('compress'));
  assert.ok(result.actions.includes('archive'));
  
  // Emergency
  result = protector.getIntervention(0.98);
  assert.strictEqual(result.level, INTERVENTION_LEVELS.EMERGENCY);
  assert.ok(result.actions.includes('restart'));
});

test('Protector.check should return memory stats', async () => {
  const protector = new Protector({ checkInterval: 1000 });
  
  const result = await protector.check();
  
  assert.ok(result.timestamp);
  assert.ok(result.memory);
  assert.ok(result.memory.rssMB >= 0);
  assert.ok(result.memory.usagePercent >= 0);
  assert.ok(result.intervention);
  assert.strictEqual(result.stats.checks, 1);
});

test('Protector should track stats correctly', async () => {
  const protector = new Protector();
  
  // 多次检查
  await protector.check();
  await protector.check();
  await protector.check();
  
  assert.strictEqual(protector.stats.checks, 3);
});

test('Protector.executeIntervention should return results', async () => {
  const protector = new Protector({
    maxMemoryMB: 10, // 很小的内存限制，触发干预
    cooldown: 0      // 无冷却
  });
  
  // 强制执行warning级别干预
  const result = await protector.executeIntervention(INTERVENTION_LEVELS.WARNING);
  
  assert.ok(result);
  assert.ok(result.actions);
  assert.strictEqual(result.level, INTERVENTION_LEVELS.WARNING);
});

// ========== Healer Tests ==========

console.log('\n=== Healer Tests ===\n');

test('Healer should initialize correctly', () => {
  const healer = new Healer();
  assert.ok(healer);
  assert.strictEqual(healer.running, false);
  assert.strictEqual(healer.status, RECOVERY_STATUS.IDLE);
});

test('Healer should have correct recovery status constants', () => {
  assert.strictEqual(RECOVERY_STATUS.IDLE, 'idle');
  assert.strictEqual(RECOVERY_STATUS.DETECTING, 'detecting');
  assert.strictEqual(RECOVERY_STATUS.RECOVERING, 'recovering');
  assert.strictEqual(RECOVERY_STATUS.RECOVERED, 'recovered');
  assert.strictEqual(RECOVERY_STATUS.FAILED, 'failed');
});

test('Healer.saveHealthCheckpoint should create checkpoint', async () => {
  setupTestEnv();
  
  const healer = new Healer({
    statePath: path.join(testDir, 'healer-state.json')
  });
  await healer.stateManager.load();
  
  const checkpoint = await healer.saveHealthCheckpoint();
  
  assert.ok(checkpoint);
  assert.ok(checkpoint.timestamp);
  assert.ok(checkpoint.snapshot);
  assert.ok(Array.isArray(checkpoint.files));
  assert.strictEqual(healer.stats.checkpointsSaved, 1);
  
  cleanupTestEnv();
});

test('Healer.detectCrash should return false when gateway running', async () => {
  process.env.HEALER_TEST_MODE = 'true';
  
  const healer = new Healer();
  healer.status = RECOVERY_STATUS.IDLE;
  
  const crashed = await healer.detectCrash();
  
  // 测试模式下模拟gateway运行
  assert.strictEqual(crashed, false);
});

test('Healer.getStatus should return correct info', async () => {
  const healer = new Healer();
  
  const status = healer.getStatus();
  
  assert.ok(status);
  assert.strictEqual(status.running, false);
  assert.strictEqual(status.status, RECOVERY_STATUS.IDLE);
  assert.ok(status.stats);
});

test('Healer.getCheckpoints should return array', async () => {
  setupTestEnv();
  
  const healer = new Healer({
    statePath: path.join(testDir, 'healer-state.json')
  });
  await healer.stateManager.load();
  
  // 保存一个检查点
  await healer.saveHealthCheckpoint();
  
  const checkpoints = healer.getCheckpoints();
  
  assert.ok(Array.isArray(checkpoints));
  assert.ok(checkpoints.length >= 1);
  
  cleanupTestEnv();
});

test('Healer.recover should handle no checkpoint case', async () => {
  const healer = new Healer({
    statePath: path.join(testDir, 'healer-state-empty.json')
  });
  await healer.stateManager.load();
  healer.stateManager.state.recovery.checkpoints = [];
  
  const result = await healer.recover();
  
  assert.strictEqual(result.success, false);
  assert.ok(result.error.includes('No checkpoint'));
});

test('Healer.restartGateway should return simulated result', async () => {
  process.env.HEALER_TEST_MODE = 'true';
  
  const healer = new Healer();
  
  const result = await healer.restartGateway();
  
  assert.strictEqual(result.success, true);
  assert.strictEqual(result.simulated, true);
});

// ========== Integration Tests ==========

console.log('\n=== Integration Tests ===\n');

test('Both modules can be created together', () => {
  const protector = new Protector();
  const healer = new Healer();
  
  assert.ok(protector);
  assert.ok(healer);
  
  // 检查状态
  const pStatus = protector.getStatus();
  const hStatus = healer.getStatus();
  
  assert.strictEqual(pStatus.running, false);
  assert.strictEqual(hStatus.running, false);
});

test('Events are emitted correctly', async () => {
  setupTestEnv();
  
  const protector = new Protector({ maxMemoryMB: 512, checkInterval: 500 });
  const healer = new Healer({
    statePath: path.join(testDir, 'integration-state.json'),
    checkpointInterval: 1000
  });
  
  let checkEvent = false;
  let checkpointEvent = false;
  
  protector.on('check', () => { checkEvent = true; });
  healer.on('checkpoint-saved', () => { checkpointEvent = true; });
  
  await healer.stateManager.load();
  await protector.check();
  await healer.saveHealthCheckpoint();
  
  assert.strictEqual(checkEvent, true);
  assert.strictEqual(checkpointEvent, true);
  
  cleanupTestEnv();
});

test('Stats reset works correctly', async () => {
  const protector = new Protector();
  const healer = new Healer();
  
  // 做一些操作
  await protector.check();
  await healer.stateManager.load();
  await healer.saveHealthCheckpoint();
  
  // 重置统计
  protector.resetStats();
  healer.resetStats();
  
  assert.strictEqual(protector.stats.checks, 0);
  assert.strictEqual(healer.stats.checkpointsSaved, 0);
});

// ========== Summary ==========

console.log('\n=== Test Summary ===\n');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total: ${passed + failed}`);

// 最终清理
cleanupTestEnv();

// 退出
if (failed > 0) {
  process.exit(1);
} else {
  console.log('\n✓ All tests passed!\n');
  process.exit(0);
}