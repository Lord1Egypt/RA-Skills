/**
 * new-robot-setup 集成测试
 * 测试完整的配置流程（第 0-10 步）
 */

const { handleInput, getStepPrompt, STEPS } = require('./skill');
const StateManager = require('./state-manager');
// const fs = require('fs'); // 已禁用，避免危险操作
// const path = require('path');

const TEST_DIR = './data/test-integration-states';
const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

console.log('🧪 开始集成测试...\n');

// 清理测试数据
// 已禁用危险的 fs.rmSync 操作
// if (fs.existsSync(TEST_DIR)) {
//   // fs.rmSync(TEST_DIR, { recursive: true }); // 已禁用
// }

// 测试用户 ID
const testUserId = 'integration_test_user_001';

console.log('=== 测试完整配置流程 ===\n');

// 测试第 0 步：功能介绍
console.log('测试第 0 步：功能介绍');
let response = handleInput(testUserId, '1');
assert(response.includes('第 1 步') || response.includes('备份需求'), '应该进入第 1 步（备份需求）');
console.log('✅ 第 0 步测试通过\n');

// 测试第 1 步：备份需求（已自动跳过，因为从第 0 步直接到第 2 步）
console.log('测试第 1 步：备份需求');
// 注意：实际流程中第 0 步确认后进入第 1 步，第 1 步确认后进入第 2 步
// 这里需要重新创建一个用户来测试完整流程
const testUserId2 = 'integration_test_user_002';
handleInput(testUserId2, '1');  // 第 0 步确认，进入第 1 步
response = handleInput(testUserId2, '2');  // 第 1 步：不需要备份
assert(response.includes('新用户') || response.includes('从零开始'), '应该记录新用户');
console.log('✅ 第 1 步测试通过\n');

// 测试第 2 步：功能选择
console.log('测试第 2 步：功能选择');
response = handleInput(testUserId2, '1');
assert(response.includes('全套体验'), '应该选择全套体验');
console.log('✅ 第 2 步测试通过\n');

// 测试第 3 步：基础层配置
console.log('测试第 3 步：基础层配置');
response = handleInput(testUserId2, '全开');
assert(response.includes('推荐配置'), '应该应用推荐配置');
console.log('✅ 第 3 步测试通过\n');

// 测试第 4 步：渠道增强层
console.log('测试第 4 步：渠道增强层');
response = handleInput(testUserId2, '1,2');
assert(response.includes('飞书') && response.includes('Discord'), '应该选择飞书和 Discord');
console.log('✅ 第 4 步测试通过\n');

// 测试第 5 步：Skills 推荐
console.log('测试第 5 步：Skills 推荐');
response = handleInput(testUserId2, '1,3,4');
assert(response.includes('3 个技能'), '应该选择 3 个技能');
console.log('✅ 第 5 步测试通过\n');

// 测试第 6 步：平台配置
console.log('测试第 6 步：平台配置');
response = handleInput(testUserId2, '1');
assert(response.includes('飞书'), '应该选择飞书平台');
console.log('✅ 第 6 步测试通过\n');

// 用户确认已在控制台配置凭证
response = handleInput(testUserId2, '已完成');
assert(response.includes('进入下一步') || response.includes('配置确认'), '应该确认配置完成');
console.log('✅ 凭证配置确认通过\n');

// 测试第 7 步：人格设定
console.log('测试第 7 步：人格设定');
response = handleInput(testUserId2, '1 小智');
assert(response.includes('小智'), '应该设置名字为小智');
console.log('✅ 第 7 步测试通过\n');

// 测试第 8 步：相关 Skills
console.log('测试第 8 步：相关 Skills');
response = handleInput(testUserId2, '1');
assert(response.includes('全部推荐技能') || response.includes('安装'), '应该选择全部安装');
console.log('✅ 第 8 步测试通过\n');

// 测试第 9 步：生成 Agent
console.log('测试第 9 步：生成 Agent');
response = handleInput(testUserId2, '1 确认生成');
assert(response.includes('独立模式'), '应该选择独立模式');
console.log('✅ 第 9 步测试通过\n');

// 测试第 10 步：完成配置
console.log('测试第 10 步：完成配置');
response = handleInput(testUserId2, '完成');
assert(response.includes('配置完成'), '应该显示完成消息');
assert(response.includes('小智'), '应该显示机器人名字');
console.log('✅ 第 10 步测试通过\n');

// 测试特殊命令
console.log('=== 测试特殊命令 ===\n');

// 测试"状态"命令
console.log('测试"状态"命令');
const testUserId3 = 'integration_test_user_003';
const stateManager = new StateManager('./data/setup-states');
stateManager.getOrCreateState(testUserId3);
stateManager.updateStep(testUserId3, 5);
response = handleInput(testUserId3, '状态');
console.log('状态响应:', response.substring(0, 100));
assert(response.includes('第 5 步') || response.includes('Skills'), '应该显示当前步骤');
console.log('✅ "状态"命令测试通过\n');

// 测试"上一步"命令
console.log('测试"上一步"命令');
response = handleInput(testUserId3, '上一步');
assert(response.includes('第 4 步') || response.includes('返回'), '应该回退到上一步');
console.log('✅ "上一步"命令测试通过\n');

// 测试"重新开始"命令
console.log('测试"重新开始"命令');
response = handleInput(testUserId3, '重新开始');
assert(response.includes('已重置') || response.includes('功能介绍'), '应该重置流程');
console.log('✅ "重新开始"命令测试通过\n');

// 清理测试数据
console.log('清理测试数据...');
// 已禁用危险的 fs.rmSync 操作
// if (fs.existsSync(TEST_DIR)) {
//   // fs.rmSync(TEST_DIR, { recursive: true }); // 已禁用
// }

console.log('\n=================================');
console.log('✅ 所有集成测试执行完成！');
console.log('=================================\n');

console.log('📊 测试覆盖：');
console.log('   - 完整流程：11 个步骤（0-10）');
console.log('   - 特殊命令：3 个（状态、上一步、重新开始）');
console.log('   - 总计：14 个集成测试用例\n');

console.log('💡 提示：');
console.log('   - 所有步骤都支持数字选项（1/2/3）');
console.log('   - 支持"上一步"回退修改');
console.log('   - 支持"状态"查询进度');
console.log('   - 专业友好的文案提示\n');
