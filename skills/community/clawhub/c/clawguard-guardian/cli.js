#!/usr/bin/env node
/**
 * ClawGuard v3 - Guardian CLI
 * 运行时守护者：行为监控、拦截、回放、冻结
 */

const { Guardian } = require('./src/guardian.js');
const fs = require('fs');

const args = process.argv.slice(2);
const commands = {
  start: args.includes('start') || args.includes('monitor'),
  replay: args.includes('replay'),
  freeze: args.includes('freeze'),
  unfreeze: args.includes('unfreeze'),
  status: args.includes('status'),
  logs: args.includes('logs')
};

async function main() {
  const guardian = new Guardian();

  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║         🛡️ ClawGuard v3 - Guardian (运行时守护者)      ║
╠═══════════════════════════════════════════════════════════════╣
║  命令:                                                     ║
║    start / monitor    启动监控                            ║
║    replay [id]         回放指定会话                        ║
║    freeze [id]        冻结指定会话                        ║
║    unfreeze [id]      解冻指定会话                        ║
║    status             查看当前状态                        ║
║    logs [lines]       查看最近日志                        ║
╚═══════════════════════════════════════════════════════════════╝
  `);

  if (commands.start) {
    await guardian.start();
  } else if (commands.replay) {
    const sessionId = args.find(a => a.startsWith('session-')) || 'latest';
    await guardian.replaySession(sessionId);
  } else if (commands.freeze) {
    const sessionId = args.find(a => a.startsWith('session-')) || 'all';
    await guardian.freezeSession(sessionId);
  } else if (commands.unfreeze) {
    const sessionId = args.find(a => a.startsWith('session-')) || 'all';
    await guardian.unfreezeSession(sessionId);
  } else if (commands.status) {
    await guardian.showStatus();
  } else if (commands.logs) {
    const lines = parseInt(args.find(a => /^\d+$/.test(a)) || '50');
    await guardian.showLogs(lines);
  } else {
    // 默认启动监控
    await guardian.start();
  }
}

main().catch(err => {
  console.error('❌ Guardian 错误:', err.message);
  process.exit(1);
});

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n🛡️ Guardian 退出...');
  process.exit(0);
});
