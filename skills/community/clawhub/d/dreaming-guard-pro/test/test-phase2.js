/**
 * Dreaming Guard Pro Phase 2 - 快速测试
 * 测试 monitor, archiver, compressor 三个模块
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const os = require('os');

// 测试目录
const TEST_DIR = '/tmp/dreaming-guard-test-' + Date.now();
const DREAMING_DIR = path.join(TEST_DIR, 'dreaming');
const ARCHIVE_DIR = path.join(TEST_DIR, 'archive');

console.log('Test directory:', TEST_DIR);

// 模块路径
const Monitor = require('../src/monitor.js');
const Archiver = require('../src/archiver.js');
const Compressor = require('../src/compressor.js');

// 测试结果
let passed = 0;
let failed = 0;

async function test(name, fn) {
  try {
    await fn();
    console.log('  ✓', name);
    passed++;
  } catch (e) {
    console.log('  ✗', name);
    console.log('    Error:', e.message);
    failed++;
  }
}

// 主测试函数
async function runTests() {
  
  // ============ 准备测试环境 ============
  fs.mkdirSync(DREAMING_DIR, { recursive: true });
  fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  
  // 创建测试dream文件
  const testFiles = [
    { name: 'test-1.json', content: { id: 1, timestamp: Date.now(), type: 'thought', content: 'hello' } },
    { name: 'test-2.json', content: { id: 2, timestamp: Date.now(), type: 'decision', content: 'world' } },
    { name: 'test-3.json', content: { id: 3, timestamp: Date.now() - 86400000, type: 'memory', content: 'old' } }
  ];
  
  for (const f of testFiles) {
    fs.writeFileSync(path.join(DREAMING_DIR, f.name), JSON.stringify(f.content));
  }
  
  console.log('Setup complete\n');

  // ============ Monitor 测试 ============
  console.log('=== Monitor Tests ===');
  
  const monitor = new Monitor({
    watchPath: DREAMING_DIR,
    interval: 1000,
    historySize: 10,
    logger: { debug: () => {}, info: () => {}, warn: () => {}, error: () => {} }
  });
  
  await test('Monitor instantiation', async () => {
    assert(monitor instanceof Monitor);
    assert(monitor.config.watchPath === DREAMING_DIR);
  });
  
  await test('Monitor start and collect', async () => {
    await monitor.start();
    // 等待收集完成
    await new Promise(r => setTimeout(r, 50));
    const snapshot = monitor.getLatestSnapshot();
    assert(snapshot, 'should have snapshot');
    assert(typeof snapshot.totalFiles === 'number', 'should have totalFiles');
    assert(snapshot.totalFiles >= 3, `should have at least 3 files, got ${snapshot.totalFiles}`);
    await monitor.stop();
  });
  
  await test('Monitor getHistory', async () => {
    const history = monitor.getHistory(5);
    assert(Array.isArray(history), 'history should be array');
    assert(history.length >= 1, 'should have history');
  });

  // ============ Archiver 测试 ============
  console.log('\n=== Archiver Tests ===');
  
  const archiver = new Archiver({
    archivePath: ARCHIVE_DIR,
    logger: { debug: () => {}, info: () => {}, warn: () => {}, error: () => {} }
  });
  
  await test('Archiver instantiation', async () => {
    assert(archiver instanceof Archiver);
    assert(fs.existsSync(path.join(ARCHIVE_DIR, 'hot')));
    assert(fs.existsSync(path.join(ARCHIVE_DIR, 'warm')));
    assert(fs.existsSync(path.join(ARCHIVE_DIR, 'cold')));
  });
  
  await test('Archiver listArchives', async () => {
    const archives = await archiver.listArchives();
    assert(Array.isArray(archives), 'archives should be array');
  });
  
  await test('Archiver archive operation', async () => {
    const result = await archiver.archive({ sourcePath: DREAMING_DIR, level: 'hot' });
    assert(result, 'should have result');
    assert(typeof result.totalFiles === 'number', 'should have totalFiles');
    assert(archiver.index.archives !== undefined, 'should have index.archives');
  });

  // ============ Compressor 测试 ============
  console.log('\n=== Compressor Tests ===');
  
  const compressor = new Compressor({
    backup: false,
    dryRun: true,
    logger: { debug: () => {}, info: () => {}, warn: () => {}, error: () => {} }
  });
  
  await test('Compressor instantiation', async () => {
    assert(compressor instanceof Compressor);
  });
  
  await test('Compressor getStrategy', async () => {
    const strategy = compressor.getStrategy('lossless');
    assert(strategy, 'should have strategy');
    assert(typeof strategy.targetReduction === 'number', 'should have targetReduction');
    assert(Array.isArray(strategy.preserveFields), 'should have preserveFields');
  });
  
  await test('Compressor compress lossless', async () => {
    const content = JSON.stringify({
      entries: [
        { timestamp: Date.now(), type: 'thought', content: 'hello' },
        { timestamp: Date.now(), type: 'thought', content: 'world' }
      ]
    });
    const result = await compressor.compress(content, 'lossless');
    assert(result, 'should have result');
    assert(typeof result.reduction === 'number', 'should have reduction');
    assert(result.strategy === 'lossless', 'should have strategy');
  });
  
  await test('Compressor compress with deduplication', async () => {
    const content = JSON.stringify({
      entries: [
        { timestamp: Date.now(), type: 'log', content: 'same' },
        { timestamp: Date.now(), type: 'log', content: 'same' },
        { timestamp: Date.now(), type: 'log', content: 'same' }
      ]
    });
    const result = await compressor.compress(content, 'lossless');
    assert(result, 'should have result');
    assert(typeof result.reduction === 'number', 'should have reduction');
  });

  // ============ 清理 ============
  console.log('\n=== Cleanup ===');
  try {
    fs.rmSync(TEST_DIR, { recursive: true, force: true });
    console.log('Test directory cleaned up');
  } catch (e) {
    console.log('Cleanup warning:', e.message);
  }

  // ============ 总结 ============
  console.log('\n=== Results ===');
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total:  ${passed + failed}`);

  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(err => {
  console.error('Test runner failed:', err);
  process.exit(1);
});