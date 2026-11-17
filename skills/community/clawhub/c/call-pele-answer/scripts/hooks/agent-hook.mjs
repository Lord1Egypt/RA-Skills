#!/usr/bin/env node
// agent-hook.mjs — agent-level timing. Two ways in:
//  1. Claude Code hooks (plugin hooks/hooks.json): reads the hook JSON on stdin for UserPromptSubmit,
//     PreToolUse, PostToolUse, Stop and appends one line per event to ~/.call-pele-answer/logs/agent.jsonl.
//  2. Any other agent: `node agent-hook.mjs mark <step> [--session id]` at each step boundary
//     (e.g. research, write-answer, pe-answer, verify, deliver), and `mark end` when the answer is sent.
// It never blocks the agent: it exits 0 on any error and prints nothing on stdout.
import { appendFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { LOG_DIR } from '../core/trace.mjs';
const FILE = process.env.PE_AGENT_LOG || join(LOG_DIR, 'agent.jsonl');
const write = rec => { try { mkdirSync(dirname(FILE), { recursive: true }); appendFileSync(FILE, JSON.stringify({ t: Date.now(), ...rec }) + '\n'); } catch {} };

const [, , cmd, step, ...rest] = process.argv;
if (cmd === 'mark') {
  const k = rest.indexOf('--session');
  write({ ev: 'Mark', step: step || 'unnamed', session: k >= 0 ? rest[k + 1] : process.env.PE_SESSION || 'manual' });
} else {
  let j = {}; try { j = JSON.parse(readFileSync(0, 'utf8') || '{}'); } catch {}
  const ev = j.hook_event_name || cmd || 'Unknown';
  const input = j.tool_input || {};
  const command = String(input.command || input.file_path || input.url || input.pattern || '').slice(0, 160);
  write({
    ev, session: j.session_id || '', tool: j.tool_name || undefined,
    id: j.tool_use_id || undefined, cmd: command || undefined,
    pe: /pe\.mjs|call-pele-answer/.test(command) || undefined,
    chars: ev === 'UserPromptSubmit' ? String(j.prompt || '').length : undefined,
  });
}
process.exit(0);
