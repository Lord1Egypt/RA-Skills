/**
 * Dreaming Guard Pro - Phase 1 Module Tests
 * 
 * 简单测试验证基础模块功能
 */

const path = require('path');
const fs = require('fs');
const os = require('os');

// 测试目录
const testDir = path.join(os.tmpdir(), 'dreaming-guard-test-' + Date.now());
fs.mkdirSync(testDir, { recursive: true });

// 测试结果
let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.log(`  ❌ ${message}`);
    failed++;
  }
}

async function runTests() {
  console.log('\n=== Dreaming Guard Pro Phase 1 Tests ===\n');
  console.log(`Test directory: ${testDir}\n`);

  // ========== Logger Tests ==========
  console.log('📦 Testing Logger...');
  const Logger = require('../src/logger');
  
  const logFile = path.join(testDir, 'test.log');
  const logger = new Logger({ 
    level: 'debug', 
    file: logFile,
    maxSize: 1024, // 小尺寸用于测试轮转
    console: false 
  });

  logger.info('Test info message');
  logger.warn('Test warn message', { key: 'value' });
  logger.error('Test error message');
  logger.debug('Test debug message');

  assert(fs.existsSync(logFile), 'Log file created');
  
  const logContent = fs.readFileSync(logFile, 'utf-8');
  assert(logContent.includes('[INFO]'), 'Info level logged');
  assert(logContent.includes('[WARN]'), 'Warn level logged');
  assert(logContent.includes('[ERROR]'), 'Error level logged');
  assert(logContent.includes('[DEBUG]'), 'Debug level logged');

  // Test log rotation
  for (let i = 0; i < 100; i++) {
    logger.info(`Rotation test message ${i} - `.repeat(10));
  }
  
  const logDir = path.dirname(logFile);
  const rotatedFiles = fs.readdirSync(logDir).filter(f => f.includes('.log'));
  assert(rotatedFiles.length > 1, 'Log rotation triggered');

  // Test child logger
  const childLogger = logger.child('test-module');
  assert(childLogger.module === 'test-module', 'Child logger created');

  // Test setLevel
  logger.setLevel('warn');
  logger.debug('Should not appear');
  const afterSetLevel = fs.readFileSync(logFile, 'utf-8');
  assert(!afterSetLevel.includes('Should not appear'), 'Level filtering works');

  // ========== Config Tests ==========
  console.log('\n📦 Testing Config...');
  const Config = require('../src/config');
  
  const configFile = path.join(testDir, 'config.json');
  const config = new Config(configFile);

  // Test default values
  config.loadSync();
  assert(config.get('version') === '1.0.0', 'Default version loaded');
  assert(config.get('monitor.interval') === 5000, 'Default monitor interval');
  assert(Array.isArray(config.get('workspaces')), 'Default workspaces loaded');

  // Test set/get
  config.set('monitor.interval', 3000);
  assert(config.get('monitor.interval') === 3000, 'Set/get works');

  // Test deep path
  config.set('archive.retention.maxAge', 14);
  assert(config.get('archive.retention.maxAge') === 14, 'Deep path access');

  // Test validation
  const validResult = config.validate();
  assert(validResult.valid === true, 'Default config is valid');

  config.set('monitor.interval', 100); // Invalid: too small
  const invalidResult = config.validate();
  assert(invalidResult.valid === false, 'Invalid config detected');
  assert(invalidResult.errors.length > 0, 'Validation errors reported');

  // Test save
  config.set('test.value', 'saved');
  await config.save();
  assert(fs.existsSync(configFile), 'Config file saved');

  // Test load saved config
  const config2 = new Config(configFile);
  config2.loadSync();
  assert(config2.get('test.value') === 'saved', 'Saved config loaded');

  // Test env override
  process.env.DREAMING_GUARD_MONITOR_INTERVAL = '2000';
  const configEnv = new Config(configFile);
  configEnv.loadSync();
  assert(configEnv.get('monitor.interval') === 2000, 'Env override works');

  // Test reset
  config.reset();
  assert(config.get('monitor.interval') === 5000, 'Reset to defaults');

  // ========== StateManager Tests ==========
  console.log('\n📦 Testing StateManager...');
  const StateManager = require('../src/state-manager');
  
  const stateFile = path.join(testDir, 'state.json');
  const state = new StateManager({ 
    statePath: stateFile,
    autoSave: false 
  });

  // Test load
  await state.load();
  assert(state.get('version') === '1.0.0', 'Default state loaded');

  // Test update/get
  state.update('monitors.test', { size: 1024, status: 'healthy' });
  assert(state.get('monitors.test.size') === 1024, 'State update/get works');

  // Test save
  await state.save();
  assert(fs.existsSync(stateFile), 'State file saved');

  // Test checkpoint
  const checkpoint = state.setCheckpoint({ 
    workspace: 'test', 
    size: 2048,
    files: 5 
  });
  assert(checkpoint.timestamp > 0, 'Checkpoint created');
  assert(state.getCheckpoint().data.size === 2048, 'Get checkpoint works');

  // Test recordAction
  state.recordAction({ type: 'archive', target: 'test', result: 'success' });
  const history = state.getActionHistory();
  assert(history.length === 1, 'Action recorded');
  assert(history[0].type === 'archive', 'Action has correct type');

  // Test monitor status
  state.updateMonitorStatus('/test/workspace', { 
    size: 4096, 
    status: 'warning' 
  });
  const monitorStatus = state.getMonitorStatus('/test/workspace');
  assert(monitorStatus.size === 4096, 'Monitor status updated');

  // Test crash/recovery tracking
  state.recordCrash();
  state.recordCrash();
  assert(state.get('recovery.crashes') === 2, 'Crash count tracked');

  state.recordSuccessfulRecovery();
  assert(state.get('recovery.successfulRecoveries') === 1, 'Recovery count tracked');

  // Save before testing persistence
  await state.save();

  // Test persistence
  const state2 = new StateManager({ statePath: stateFile, autoSave: false });
  await state2.load();
  assert(state2.get('monitors.test.size') === 1024, 'State persisted correctly');
  assert(state2.get('recovery.crashes') === 2, 'Crash count persisted');

  // Test checkpoint list
  state.setCheckpoint({ test: 2 });
  state.setCheckpoint({ test: 3 });
  const checkpoints = state.getCheckpoints();
  assert(checkpoints.length >= 3, 'Multiple checkpoints saved');

  // Test destroy
  state.update('test.cleanup', true);
  state.destroy();
  assert(!state.autoSaveTimer, 'AutoSave timer cleared');

  // Cleanup
  fs.rmSync(testDir, { recursive: true, force: true });

  // Results
  console.log('\n=== Test Results ===');
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📊 Total: ${passed + failed}\n`);

  if (failed > 0) {
    process.exit(1);
  }
}

runTests().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});