/**
 * new-robot-setup 技能测试用例
 * 测试状态管理和日志脱敏功能
 */

const StateManager = require('./state-manager');
const { sanitizeLog, sanitizeObject } = require('./skill'); // ✅ 修复：从 skill.js 导入
const assert = require('assert');

console.log('🧪 开始运行测试用例...\n');

// ========== 测试状态管理器 ==========
console.log('=== 测试状态管理器 ===\n');

// 测试 1: 创建状态管理器
console.log('测试 1: 创建状态管理器');
try {
  const stateManager = new StateManager();
  console.log('✅ 状态管理器创建成功\n');
} catch (error) {
  console.log('❌ 状态管理器创建失败:', error.message, '\n');
}

// 测试 2: 创建新状态
console.log('测试 2: 创建新状态');
try {
  const stateManager = new StateManager();
  const testUserId = 'test_user_001';
  const state = stateManager.createState(testUserId);
  
  assert(state.session_id, '应该有 session_id');
  assert(state.user_id === testUserId, 'user_id 应该匹配');
  assert(state.current_step === 0, '初始步骤应该是 0');
  assert(state.step_data, '应该有 step_data');
  
  console.log('✅ 状态创建成功');
  console.log('   Session ID:', state.session_id);
  console.log('   初始步骤:', state.current_step, '\n');
} catch (error) {
  console.log('❌ 状态创建失败:', error.message, '\n');
}

// 测试 3: 保存和加载状态
console.log('测试 3: 保存和加载状态');
try {
  const stateManager = new StateManager();
  const testUserId = 'test_user_002';
  
  const initialState = stateManager.createState(testUserId);
  stateManager.saveState(testUserId, initialState);
  
  const loadedState = stateManager.loadState(testUserId);
  
  assert(loadedState, '应该能加载状态');
  assert(loadedState.session_id === initialState.session_id, 'session_id 应该匹配');
  
  console.log('✅ 保存和加载状态成功\n');
} catch (error) {
  console.log('❌ 保存和加载状态失败:', error.message, '\n');
}

// 测试 4: 回退功能
console.log('测试 4: 回退功能 (goBack)');
try {
  const stateManager = new StateManager();
  const testUserId = 'test_user_003';
  
  const state = stateManager.createState(testUserId);
  state.current_step = 5;
  stateManager.saveState(testUserId, state);
  
  const result1 = stateManager.goBack(testUserId);
  assert(result1.success === true, '回退应该成功');
  assert(result1.step === 4, '应该回退到第 4 步');
  assert(result1.message, '应该有消息');
  
  const result2 = stateManager.goBack(testUserId);
  assert(result2.success === true, '再次回退应该成功');
  assert(result2.step === 3, '应该回退到第 3 步');
  
  stateManager.updateStep(testUserId, 0);
  const result3 = stateManager.goBack(testUserId);
  assert(result3.success === false, '第 0 步回退应该失败');
  assert(result3.message, '应该有错误消息');
  
  console.log('✅ 回退功能测试成功\n');
} catch (error) {
  console.log('❌ 回退功能测试失败:', error.message, '\n');
}

// 测试 5: 前进功能
console.log('测试 5: 前进功能 (goNext)');
try {
  const stateManager = new StateManager();
  const testUserId = 'test_user_004';
  
  stateManager.createState(testUserId);
  
  const result1 = stateManager.goNext(testUserId);
  assert(result1.success === true, '前进应该成功');
  assert(result1.step === 1, '应该前进到第 1 步');
  
  for (let i = 0; i < 9; i++) {
    stateManager.goNext(testUserId);
  }
  
  const result2 = stateManager.goNext(testUserId);
  assert(result2.success === false, '第 10 步前进应该失败');
  
  console.log('✅ 前进功能测试成功\n');
} catch (error) {
  console.log('❌ 前进功能测试失败:', error.message, '\n');
}

// 测试 6: 步骤数据保存
console.log('测试 6: 步骤数据保存');
try {
  const stateManager = new StateManager();
  const testUserId = 'test_user_005';
  
  stateManager.getOrCreateState(testUserId);
  
  const stepData = { streaming: true, memory: 'enhanced' };
  stateManager.saveStepData(testUserId, 1, stepData);
  
  const loadedData = stateManager.getStepData(testUserId, 1);
  assert(loadedData, '应该能加载步骤数据');
  assert(loadedData.streaming === true, 'streaming 应该匹配');
  
  console.log('✅ 步骤数据保存成功\n');
} catch (error) {
  console.log('❌ 步骤数据保存失败:', error.message, '\n');
}

// 测试 7: 清除状态
console.log('测试 7: 清除状态');
try {
  const stateManager = new StateManager();
  const testUserId = 'test_user_006';
  
  stateManager.getOrCreateState(testUserId);
  const result = stateManager.clearState(testUserId);
  
  assert(result === true, '清除应该成功');
  assert(stateManager.loadState(testUserId) === null, '清除后应该返回 null');
  
  console.log('✅ 清除状态成功\n');
} catch (error) {
  console.log('❌ 清除状态失败:', error.message, '\n');
}

// 测试 8: 获取所有会话
console.log('测试 8: 获取所有会话');
try {
  const stateManager = new StateManager();
  
  for (let i = 10; i < 13; i++) {
    stateManager.getOrCreateState(`test_user_0${i}`);
  }
  
  const sessions = stateManager.getAllSessions();
  assert(sessions.length >= 3, '应该至少有 3 个会话');
  
  console.log(`✅ 获取所有会话成功，共 ${sessions.length} 个会话\n`);
} catch (error) {
  console.log('❌ 获取所有会话失败:', error.message, '\n');
}

// ========== 测试日志脱敏 ==========
console.log('=== 测试日志脱敏 ===\n');

// 测试 9: API Key 脱敏
console.log('测试 9: API Key 脱敏');
try {
  const result = sanitizeLog('api_key=abcdef1234567890abcdef1234567890');
  assert(result.includes('***REDACTED***'), '应该脱敏 API Key');
  console.log('✅ API Key 脱敏测试通过\n');
} catch (error) {
  console.log('❌ API Key 脱敏测试失败:', error.message, '\n');
}

// 测试 10: 密码脱敏
console.log('测试 10: 密码脱敏');
try {
  const testCases = [
    'password: secret123456789012345',
    "password = 'mysecret12345678901234'",
    'Secret: topsecret12345678901234',
    'Token: abc123xyz123456789012345'
  ];
  
  for (const testCase of testCases) {
    const result = sanitizeLog(testCase);
    assert(result.includes('***REDACTED***'), `应该脱敏：${testCase}`);
  }
  
  console.log('✅ 密码脱敏测试通过\n');
} catch (error) {
  console.log('❌ 密码脱敏测试失败:', error.message, '\n');
}

// 测试 11: 对象脱敏
console.log('测试 11: 对象脱敏');
try {
  const testObj = {
    username: '张三',
    password: 'secret123',
    config: { api_key: 'abcdef1234567890', enabled: true }
  };
  
  const sanitized = sanitizeObject(testObj);
  
  assert(sanitized.password === '***REDACTED***', '密码应该被脱敏');
  assert(sanitized.config.api_key === '***REDACTED***', 'API Key 应该被脱敏');
  assert(sanitized.username === '张三', '普通字段不应该被脱敏');
  
  console.log('✅ 对象脱敏测试通过\n');
} catch (error) {
  console.log('❌ 对象脱敏测试失败:', error.message, '\n');
}

// ========== 测试总结 ==========
console.log('=================================');
console.log('✅ 所有测试用例执行完成！');
console.log('=================================\n');
console.log('📊 测试覆盖：');
console.log('   - 状态管理器：8 个测试');
console.log('   - 日志脱敏：3 个测试');
console.log('   - 总计：11 个测试用例\n');
