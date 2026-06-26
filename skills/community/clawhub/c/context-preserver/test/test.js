#!/usr/bin/env node

/**
 * Context Preserver 测试套件
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const os = require('os');

const { 
  init, 
  createSnapshot, 
  listSnapshots, 
  restoreSnapshot, 
  deleteSnapshot,
  exportSnapshot,
  importSnapshot,
  getConfig,
  CONFIG
} = require('../src/index.js');

// 测试计数
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (e) {
    console.error(`❌ ${name}`);
    console.error(`   ${e.message}`);
    failed++;
  }
}

function assertEqual(actual, expected, msg) {
  if (actual !== expected) {
    throw new Error(`${msg || 'Assertion failed'}: expected ${expected}, got ${actual}`);
  }
}

function assertTrue(value, msg) {
  if (!value) {
    throw new Error(msg || 'Expected true, got false');
  }
}

console.log('🧪 Context Preserver 测试开始\n');

// 测试1: 初始化
test('初始化数据目录', () => {
  init();
  assertTrue(fs.existsSync(CONFIG.dataDir), '数据目录应该存在');
  assertTrue(fs.existsSync(CONFIG.snapshotsDir), '快照目录应该存在');
});

// 测试2: 创建快照
test('创建快照', () => {
  const snapshotId = createSnapshot('测试快照', ['test']);
  assertTrue(snapshotId.startsWith('snapshot_'), '快照ID应该以snapshot_开头');
  
  const snapshotPath = path.join(CONFIG.snapshotsDir, `${snapshotId}.json`);
  assertTrue(fs.existsSync(snapshotPath), '快照文件应该存在');
  
  const data = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  assertEqual(data.name, '测试快照', '快照名称应该匹配');
  assertTrue(data.tags.includes('test'), '快照应该包含test标签');
});

// 测试3: 列出快照
test('列出快照', () => {
  const snapshots = listSnapshots();
  assertTrue(Array.isArray(snapshots), '应该返回数组');
  assertTrue(snapshots.length > 0, '应该至少有一个快照');
});

// 测试4: 恢复快照
test('恢复快照', () => {
  const snapshots = fs.readdirSync(CONFIG.snapshotsDir).filter(f => f.endsWith('.json'));
  assertTrue(snapshots.length > 0, '应该存在快照文件');
  
  const snapshotId = snapshots[0].replace('.json', '');
  const result = restoreSnapshot(snapshotId);
  assertTrue(result !== false, '恢复应该成功');
  assertTrue(result.id === snapshotId, '恢复的ID应该匹配');
});

// 测试5: 配置管理
test('配置管理', () => {
  const config = getConfig();
  assertTrue(typeof config === 'object', '配置应该是对象');
  assertTrue(typeof config.autoSnapshot === 'boolean', 'autoSnapshot应该是布尔值');
  assertTrue(typeof config.maxSnapshots === 'number', 'maxSnapshots应该是数字');
});

// 测试6: 导出快照
test('导出快照', () => {
  const snapshots = fs.readdirSync(CONFIG.snapshotsDir).filter(f => f.endsWith('.json'));
  if (snapshots.length > 0) {
    const snapshotId = snapshots[0].replace('.json', '');
    const exportPath = path.join(os.tmpdir(), `test-export-${Date.now()}.json`);
    const result = exportSnapshot(snapshotId, exportPath);
    assertTrue(result !== false, '导出应该成功');
    assertTrue(fs.existsSync(result), '导出文件应该存在');
    
    // 清理
    fs.unlinkSync(result);
  }
});

// 测试7: 导出所有快照
test('导出所有快照', () => {
  const exportDir = path.join(os.tmpdir(), `test-export-all-${Date.now()}`);
  const result = exportSnapshot('all', exportDir);
  assertTrue(result !== false, '导出所有应该成功');
  assertTrue(fs.existsSync(result), '导出目录应该存在');
  
  // 清理
  fs.rmSync(result, { recursive: true, force: true });
});

// 测试8: 导入快照
test('导入快照', () => {
  // 先创建一个临时快照文件
  const tempSnapshot = {
    id: 'test-import-snapshot',
    name: '导入测试快照',
    timestamp: new Date().toISOString(),
    tags: ['import-test']
  };
  
  const tempPath = path.join(os.tmpdir(), 'test-import.json');
  fs.writeFileSync(tempPath, JSON.stringify(tempSnapshot, null, 2));
  
  // 导入
  const result = importSnapshot(tempPath);
  assertTrue(result === true, '导入应该成功');
  
  // 验证
  const importedPath = path.join(CONFIG.snapshotsDir, 'test-import-snapshot.json');
  assertTrue(fs.existsSync(importedPath), '导入的文件应该存在');
  
  // 清理
  fs.unlinkSync(tempPath);
  fs.unlinkSync(importedPath);
});

// 测试9: 删除快照
test('删除快照', () => {
  // 先创建一个测试快照
  const snapshotId = createSnapshot('待删除快照', ['delete-test']);
  const snapshotPath = path.join(CONFIG.snapshotsDir, `${snapshotId}.json`);
  
  assertTrue(fs.existsSync(snapshotPath), '快照文件应该存在');
  
  const result = deleteSnapshot(snapshotId);
  assertTrue(result === true, '删除应该成功');
  assertTrue(!fs.existsSync(snapshotPath), '快照文件应该已被删除');
});

// 总结
console.log('\n' + '='.repeat(50));
console.log(`测试结果: ${passed} 通过, ${failed} 失败`);
console.log('='.repeat(50));

process.exit(failed > 0 ? 1 : 0);
