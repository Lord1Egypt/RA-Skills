'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { readTrajectoryInputsDetailed } = require('../src/gep/trajectoryExport');

function writeClaude(records) {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-rt-'));
  const dir = path.join(base, '.claude', 'projects', 'proj');
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, 'claude-session.jsonl');
  fs.writeFileSync(file, records.map((r) => JSON.stringify(r)).join('\n') + '\n');
  return file;
}

function writeCodex(records) {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'codex-rt-'));
  const dir = path.join(base, '.codex', 'sessions');
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, 'rollout-2026-06-26.jsonl');
  fs.writeFileSync(file, records.map((r) => JSON.stringify(r)).join('\n') + '\n');
  return file;
}

describe('FIX-7 empty thinking is preserved with thinking_empty marker', () => {
  it('Claude empty/redacted thinking block keeps the reasoning turn', () => {
    const file = writeClaude([
      { type: 'user', message: { role: 'user', content: 'Solve it' } },
      {
        type: 'assistant',
        message: {
          role: 'assistant',
          content: [
            { type: 'thinking', thinking: '' },
            { type: 'redacted_thinking', data: 'encrypted-blob' },
            { type: 'text', text: 'Done.' },
          ],
        },
      },
    ]);
    const res = readTrajectoryInputsDetailed(file);
    const t = res.sessionTrajectories[0];
    assert.ok(t);
    const emptyThinking = t.turns.filter((turn) => turn.thinking_empty === true);
    assert.ok(emptyThinking.length >= 1, 'empty thinking blocks must be preserved, not dropped');
    assert.ok(emptyThinking.every((turn) => turn.reasoning !== undefined));
  });
});

describe('FIX-8 session-level system_prompt extraction', () => {
  it('Codex base_instructions string surfaces as system_prompt', () => {
    const file = writeCodex([
      { type: 'session_meta', payload: { id: 'sess-codex', base_instructions: 'You are a careful coding agent.' } },
      { type: 'response_item', payload: { type: 'message', role: 'user', content: [{ type: 'input_text', text: 'hi' }] } },
      { type: 'response_item', payload: { type: 'message', role: 'assistant', content: [{ type: 'output_text', text: 'hello' }] } },
    ]);
    const res = readTrajectoryInputsDetailed(file);
    const t = res.sessionTrajectories[0];
    assert.ok(t);
    assert.equal(t.system_prompt, 'You are a careful coding agent.');
  });

  it('Claude system-role message surfaces as system_prompt', () => {
    const file = writeClaude([
      { type: 'system', message: { role: 'system', content: 'Follow the repo conventions.' } },
      { type: 'user', message: { role: 'user', content: 'do x' } },
      { type: 'assistant', message: { role: 'assistant', content: [{ type: 'text', text: 'ok' }] } },
    ]);
    const res = readTrajectoryInputsDetailed(file);
    const t = res.sessionTrajectories[0];
    assert.ok(t);
    assert.equal(t.system_prompt, 'Follow the repo conventions.');
  });
});
