/**
 * AutoThink Hook for OpenClaw
 * 注册为 message_preprocessor 钩子
 *
 * 使用方法：
 * 1. 将此文件放到 ~/.openclaw/plugins/
 * 2. 在 OpenClaw 配置中启用：
 *    "plugins": {
 *      "autothink-hook": {
 *        "enabled": true,
 *        "autoMode": true,
 *        "defaultThinking": "low"
 *      }
 *    }
 */

const { AutoThinkEngine } = require('./src/index.js');
const engine = new AutoThinkEngine();

// 钩子实现
async function preProcess(message, context) {
  const analysis = engine.analyzeComplexity(message);

  // 设置上下文的 thinking 级别
  if (context && typeof context.setThinking === 'function') {
    context.setThinking(analysis.level);
  } else if (context) {
    context.thinking = analysis.level;
  }

  // 可选的日志
  if (process.env.AUTOTHINK_DEBUG) {
    console.log(`[AutoThink] message="${message.substring(0, 50)}..." -> thinking=${analysis.level} (score=${analysis.score})`);
  }

  // 返回原始消息（不修改内容）
  return message;
}

// 导出钩子
module.exports = {
  name: 'autothink-hook',
  hook: 'message_preprocessor',
  priority: 100,
  process: preProcess,
  engine
};
