#!/usr/bin/env node
/**
 * Code Review Cycle - A(编码) → B(Review) → 决策
 * 
 * 用法：
 *   node run.js "功能描述"
 *   node run.js --agent-a codex --agent-b claude-code --rounds 1 "功能描述"
 */

const { execSync } = require('child_process');
const path = require('path');

// 解析参数
const args = process.argv.slice(2);
const config = {
  agentA: 'codex',
  agentB: 'claude-code',
  rounds: 0,  // 0 = 手动决策
  cwd: process.cwd(),
  task: ''
};

let i = 0;
while (i < args.length) {
  if (args[i] === '--agent-a' && args[i + 1]) {
    config.agentA = args[++i];
  } else if (args[i] === '--agent-b' && args[i + 1]) {
    config.agentB = args[++i];
  } else if (args[i] === '--rounds' && args[i + 1]) {
    config.rounds = parseInt(args[++i], 10);
  } else if (args[i] === '--cwd' && args[i + 1]) {
    config.cwd = args[++i];
  } else if (!args[i].startsWith('--')) {
    config.task = args.slice(i).join(' ');
  }
  i++;
}

if (!config.task) {
  console.error('用法：node run.js [--agent-a codex] [--agent-b claude-code] [--rounds N] <功能描述>');
  process.exit(1);
}

console.log(`🦞 Code Review Cycle`);
console.log(`   A: ${config.agentA} | B: ${config.agentB} | Rounds: ${config.rounds}`);
console.log(`   任务：${config.task}\n`);

// 输出 OpenClaw sessions_spawn 调用说明
console.log(`📋 执行步骤：\n`);

console.log(`第 1 轮 - A 写代码:`);
console.log(`\`\`\`json
{
  "runtime": "acp",
  "agentId": "${config.agentA}",
  "task": "${config.task}\\n\\n请输出：\\n## [A-Code] 改动摘要\\n## [A-Code] 实现说明\\n## [A-Code] 待确认点",
  "mode": "run",
  "streamTo": "parent",
  "timeoutSeconds": 300
}
\`\`\`\n`);

console.log(`等 A 完成后，执行 B Review:`);
console.log(`\`\`\`json
{
  "runtime": "acp",
  "agentId": "${config.agentB}",
  "task": "Review 以下代码改动，输出：\\n## [B-Review] 严重问题\\n## [B-Review] 建议优化\\n## [B-Review] 结论（□需要修改 □可以直接合并）\\n\\n代码内容：[粘贴 A 的输出]",
  "mode": "run", 
  "streamTo": "parent",
  "timeoutSeconds": 300
}
\`\`\`\n`);

if (config.rounds > 0) {
  console.log(`如果 B 认为需要修改，自动循环（最多 ${config.rounds} 轮）\n`);
}

console.log(`💡 快捷方式：直接在主会话说 "/cr ${config.task}" 我会自动执行上述流程`);
