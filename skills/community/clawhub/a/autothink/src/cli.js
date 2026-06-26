#!/usr/bin/env node

/**
 * AutoThink CLI v2
 * 支持持久化模式设置
 */

const { AutoThinkEngine } = require('./index.js');

const engine = new AutoThinkEngine();

function runAgentWithThinking(message, thinkingLevel, sessionId = null) {
  const args = ['agent', '--thinking', thinkingLevel];
  if (sessionId) {
    args.push('--session-id', sessionId);
  }
  args.push('--message', message);

  console.log(`[AutoThink] 使用 thinking=${thinkingLevel} 处理消息...\n`);

  return new Promise((resolve, reject) => {
    const proc = require('child_process').spawn('openclaw', args, {
      stdio: 'inherit',
      shell: true,
      env: { ...process.env }
    });

    proc.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Agent exited with code ${code}`));
      }
    });

    proc.on('error', (err) => {
      reject(err);
    });
  });
}

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
AutoThink CLI v2 - 智能持久化 thinking 级别

用法:
  autothink [选项] "消息内容"

选项:
  -h, --high       强制使用 high 模式（并持久化）
  -l, --low        强制使用 low 模式（并持久化）
  -m, --medium     强制使用 medium 模式（并持久化）
  --auto           启用复杂度自动分析（v1 模式，不推荐）
  --reset          重置当前会话的模式状态
  --status         查看当前会话的 thinking 状态
  --session-id X   指定会话 ID
  -v, --verbose    详细输出

行为说明:
  - 使用 -h/-l/-m 会将该模式保存到当前会话，后续消息自动沿用
  - 如果不加任何前缀，则使用会话中已保存的模式或默认 high
  - 使用 --reset 可清除会话中的保存模式，恢复默认

示例:
  autothink -h "帮我设计一个复杂系统"   # 设置会话为 high 并发送
  autothink "继续刚才的话题"             # 沿用之前设置的 high
  autothink --status                    # 查看当前模式
  autothink --reset                     # 清除持久化设置

环境变量:
  OPENCLAW_SESSION_ID  当前会话 ID（可选）
  AUTOTHINK_DEBUG      开启调试日志
`);
    return;
  }

  // 解析参数
  let sessionId = process.env.OPENCLAW_SESSION_ID || null;
  let thinkingMode = null;
  let cleanedMessage = '';
  let isModeSwitch = false;
  let doReset = false;
  let doStatus = false;
  let autoAnalyze = false;

  const messageParts = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--high':
      case '-h':
        thinkingMode = 'high';
        isModeSwitch = true;
        break;
      case '--low':
      case '-l':
        thinkingMode = 'low';
        isModeSwitch = true;
        break;
      case '--medium':
      case '-m':
        thinkingMode = 'medium';
        isModeSwitch = true;
        break;
      case '--auto':
        autoAnalyze = true;
        break;
      case '--reset':
        doReset = true;
        break;
      case '--status':
        doStatus = true;
        break;
      case '--session-id':
        sessionId = args[++i];
        break;
      case '--verbose':
      case '-v':
        // 详细输出已默认开启
        break;
      default:
        if (!arg.startsWith('-')) {
          messageParts.push(arg);
        } else {
          console.warn(`[AutoThink] 未知参数: ${arg}`);
        }
    }
  }

  // 状态/重置操作
  if (doStatus) {
    const status = engine.getStatus(sessionId);
    console.log('[AutoThink] 状态:');
    console.log(`  会话 ID: ${status.sessionId}`);
    console.log(`  当前 thinking: ${status.currentThinking}`);
    console.log(`  默认 thinking: ${status.defaultThinking}`);
    console.log(`  自动分析: ${status.autoAnalyze ? '启用' : '禁用'}`);
    console.log(`  活跃会话数: ${status.activeSessions}`);
    return;
  }

  if (doReset) {
    engine.clearSessionState(sessionId);
    console.log(`[AutoThink] 会话状态已清除，恢复默认 (${engine.defaultThinking})`);
    return;
  }

  // 消息发送
  const rawMessage = messageParts.join(' ');
  if (!rawMessage) {
    console.error('错误: 必须提供消息内容');
    process.exit(1);
  }

  // 如果没有指定 thinking 模式，则自动检测
  if (!thinkingMode) {
    thinkingMode = engine.detectThinkingMode(rawMessage, sessionId, autoAnalyze);
    console.log(`[AutoThink] 自动选择 thinking: ${thinkingMode}`);
  } else {
    console.log(`[AutoThink] 手动指定 thinking: ${thinkingMode}`);
  }

  // 清理前缀
  cleanedMessage = engine.cleanPrefix(rawMessage);

  // 执行 agent
  runAgentWithThinking(cleanedMessage, thinkingMode, sessionId)
    .then(() => {
      console.log(`\n[AutoThink] 完成`);
    })
    .catch(err => {
      console.error(`[AutoThink] 错误:`, err.message);
      process.exit(1);
    });
}

main();
