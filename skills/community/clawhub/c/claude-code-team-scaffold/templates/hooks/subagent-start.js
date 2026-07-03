#!/usr/bin/env node
'use strict';
// SubagentStart handler — log subagent invocation to session audit log.

const { appendLog } = require('./session-log');

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch {}
  process.stdout.write('{}');
});

function run() {
  let data = {};
  try { data = JSON.parse(input); } catch {}

  const sessionId = data.session_id || '';
  const agentType = data.agent_type || 'unknown';
  const agentId = data.agent_id || '';
  const prompt = (data.tool_input && data.tool_input.prompt) || data.prompt || '';
  const promptPreview = String(prompt).slice(0, 200);

  appendLog(sessionId, 'subagent_start', {
    agent_type: agentType,
    agent_id: agentId,
    prompt_preview: promptPreview,
  });
}

process.stdin.resume();
