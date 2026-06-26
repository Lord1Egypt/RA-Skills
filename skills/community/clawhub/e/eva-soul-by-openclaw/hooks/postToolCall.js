/**
 * Post-Tool-Call Hook - 工具调用后记录
 */

const fs = require('fs');
const path = require('path');
const logger = require('./logger');

async function postToolCallHook(ctx, plugin) {
  const toolName = ctx.toolName || '';
  const toolResult = ctx.toolResult;

  // 记录工具使用历史
  plugin.state.toolHistory = plugin.state.toolHistory || [];
  plugin.state.toolHistory.push({
    name: toolName,
    time: new Date().toISOString(),
    success: !ctx.toolError
  });

  // 保留最近50条
  plugin.state.toolHistory = plugin.state.toolHistory.slice(-50);

  // 特殊处理：文件操作后自动记忆
  if (['write', 'edit'].includes(toolName.toLowerCase())) {
    const resultStr = typeof toolResult === 'string' ? toolResult : JSON.stringify(toolResult);
    if (resultStr && resultStr.length > 10 && resultStr !== '{}') {
      logger.hook(`File operation detected, checking for memory...`, 'postToolCall');
    }
  }

  return ctx;
}

module.exports = { postToolCallHook };
