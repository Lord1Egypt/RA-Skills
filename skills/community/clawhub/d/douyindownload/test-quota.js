const { checkAndRecord } = require('./dist/license.js');

// 消耗完免费次数
for (let i = 0; i < 10; i++) checkAndRecord();

// 第11次 - 超额
const result = checkAndRecord();

const mcpResult = result.allowed
  ? { success: true, videoUrl: 'https://...' }
  : {
      success: false,
      error: 'QUOTA_EXCEEDED',
      message: result.upgradeMessage,
      remaining: result.remaining,
      plan: result.plan,
    };

console.log('【MCP 返回给 AI 智能体的原始内容】\n');
console.log(JSON.stringify(mcpResult, null, 2));