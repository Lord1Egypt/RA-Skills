'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { extractTranscriptCwd } = require('../src/evolve/utils');

function writeJsonl(records) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'transcript-cwd-'));
  const file = path.join(dir, 'session.jsonl');
  fs.writeFileSync(file, records.map((r) => JSON.stringify(r)).join('\n') + '\n');
  return file;
}

describe('extractTranscriptCwd robustness (FIX-6)', () => {
  it('codex session_meta cwd', () => {
    const file = writeJsonl([{ type: 'session_meta', payload: { cwd: '/home/u/workspace/proj' } }]);
    assert.equal(extractTranscriptCwd(file), '/home/u/workspace/proj');
  });

  it('claude top-level cwd after envelope records', () => {
    const file = writeJsonl([
      { type: 'permission-mode', mode: 'default' },
      { type: 'queue-operation', op: 'enqueue' },
      { type: 'user', cwd: '/home/u/workspace/claude-proj', message: { role: 'user' } },
    ]);
    assert.equal(extractTranscriptCwd(file), '/home/u/workspace/claude-proj');
  });

  it('finds cwd past the old 4KB / 5-line window (would previously be dropped)', () => {
    // Prepend several large envelope records so the cwd record lands well beyond 4 KB and line index 5.
    const filler = 'x'.repeat(2000);
    const records = [];
    for (let i = 0; i < 8; i++) records.push({ type: 'envelope', i, filler });
    records.push({ type: 'user', cwd: '/home/u/workspace/deep', message: { role: 'user' } });
    const file = writeJsonl(records);
    assert.equal(extractTranscriptCwd(file), '/home/u/workspace/deep');
  });

  it('nested message.cwd is recognized', () => {
    const file = writeJsonl([
      { type: 'summary', summary: 'prior' },
      { type: 'assistant', message: { role: 'assistant', cwd: '/home/u/workspace/nested' } },
    ]);
    assert.equal(extractTranscriptCwd(file), '/home/u/workspace/nested');
  });

  it('returns null when no cwd exists', () => {
    const file = writeJsonl([{ type: 'user', message: { role: 'user' } }]);
    assert.equal(extractTranscriptCwd(file), null);
  });
});
