/**
 * Pre-Tool-Call Hook - 工具调用前检查
 */

const fs = require('fs');
const path = require('path');
const logger = require('./logger');

const dangerousTools = ['exec', 'write', 'edit', 'delete', 'remove'];

async function preToolCallHook(ctx, plugin) {
  const toolName = ctx.toolName || '';

  // 对话计数 +1 (每次工具调用，代表一次对话)
  const chatsFile = path.join(process.env.HOME || '/root', '.openclaw/workspace/chats.txt');
  try {
    let chats = 0;
    if (fs.existsSync(chatsFile)) {
      chats = parseInt(fs.readFileSync(chatsFile, 'utf8')) || 0;
    }
    chats += 1;
    fs.writeFileSync(chatsFile, chats.toString(), 'utf8');
  } catch (e) {
    // ignore
  }

  // 记录工具调用
  plugin.state.lastToolCall = {
    name: toolName,
    args: ctx.toolArgs ? JSON.stringify(ctx.toolArgs).substring(0, 100) : '',
    time: new Date().toISOString()
  };

  // 检查危险工具
  if (dangerousTools.includes(toolName.toLowerCase())) {
    logger.hook(logger.t('hooks.preToolCall.toolDetected', { tool: toolName }), 'preToolCall');
  }

  return ctx;
}

module.exports = { preToolCallHook };
