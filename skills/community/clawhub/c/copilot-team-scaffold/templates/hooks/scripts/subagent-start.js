#!/usr/bin/env node
'use strict';
// SubagentStart hook — 记录 subagent 启动事件到会话审计日志

const { appendLog } = require('./session-log');

let input = '';
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch {}
  process.stdout.write('{}');
});

function run() {
  let data;
  try { data = JSON.parse(input); } catch { return; }

  const sessionId = data.sessionId || '';
  const agentType = data.agent_type || 'unknown';
  const agentId = data.agent_id || '';

  appendLog(sessionId, 'SubagentStart', {
    Agent: agentType,
    AgentId: agentId.slice(0, 12),
  });
}
