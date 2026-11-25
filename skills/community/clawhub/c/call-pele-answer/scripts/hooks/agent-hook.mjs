#!/usr/bin/env node
// agent-hook.mjs — agent-level timing. Two ways in:
//  1. Claude Code hooks (plugin hooks/hooks.json): reads the hook JSON on stdin for UserPromptSubmit,
//     PreToolUse, PostToolUse, Stop and appends one line per event to ~/.call-pele-answer/logs/agent.jsonl.
//  2. Any other agent: `node agent-hook.mjs mark <step> [--session id]` at each step boundary
//     (e.g. research, write-answer, pe-answer, verify, deliver), and `mark end` when the answer is sent.
// It never blocks the agent: it exits 0 on any error and prints nothing on stdout.
// Scope: it times the turn, and names only pe's own calls. Any other tool call is kept as its tool name and
// timing alone, never its command, path, URL or pattern; a pe call is kept as `pe <subcommand>` only.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { LOG_DIR } from '../core/trace.mjs';
import { appendPrivate } from '../core/files.mjs';
const FILE = process.env.PE_AGENT_LOG || join(LOG_DIR, 'agent.jsonl');
const write = rec => { try { appendPrivate(FILE, JSON.stringify({ t: Date.now(), ...rec }) + '\n'); } catch {} };
const peCall = s => { const m = /(?:pe\.mjs|\bpe)\s+([a-z]+)/.exec(s); return /pe\.mjs|call-pele-answer|(^|[\s;&|])pe\s/.test(s) ? `pe ${m?.[1] || ''}`.trim() : null; };

const [, , cmd, step, ...rest] = process.argv;
if (cmd === 'mark') {
  const k = rest.indexOf('--session');
  write({ ev: 'Mark', step: step || 'unnamed', session: k >= 0 ? rest[k + 1] : process.env.PE_SESSION || 'manual' });
} else {
  let j = {}; try { j = JSON.parse(readFileSync(0, 'utf8') || '{}'); } catch {}
  const ev = j.hook_event_name || cmd || 'Unknown';
  const input = j.tool_input || {};
  const pe = peCall(String(input.command || ''));
  write({
    ev, session: j.session_id || '', tool: j.tool_name || undefined,
    id: j.tool_use_id || undefined, cmd: pe || undefined, pe: !!pe || undefined,
    chars: ev === 'UserPromptSubmit' ? String(j.prompt || '').length : undefined,
  });
}
process.exit(0);
