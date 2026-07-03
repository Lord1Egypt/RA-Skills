'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { DatabaseSync } = require('node:sqlite');

const { readTrajectoryInputsDetailed } = require('../src/gep/trajectoryExport');

// FIX-4: Cursor adapter reads conversations from state.vscdb (sqlite, cursorDiskKV table).
// Builds a minimal synthetic DB covering both storage layouts:
//   1) bubbles inlined under composerData.conversationMap
//   2) bubbles stored as separate bubbleId:<composerId>:<bubbleId> rows

function makeVscdb(rows) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cursor-vscdb-'));
  const dbPath = path.join(dir, 'state.vscdb');
  const db = new DatabaseSync(dbPath);
  db.exec('CREATE TABLE cursorDiskKV (key TEXT PRIMARY KEY, value TEXT)');
  const insert = db.prepare('INSERT INTO cursorDiskKV (key, value) VALUES (?, ?)');
  for (const [key, value] of rows) insert.run(key, typeof value === 'string' ? value : JSON.stringify(value));
  db.close();
  return dbPath;
}

describe('Cursor state.vscdb adapter (FIX-4)', () => {
  it('inline conversationMap: user/assistant/thinking/tool turns', () => {
    const composerId = 'comp-inline-1';
    const composer = {
      composerId,
      modelConfig: { modelName: 'claude-sonnet' },
      fullConversationHeadersOnly: [{ bubbleId: 'b1' }, { bubbleId: 'b2' }],
      conversationMap: {
        b1: { bubbleId: 'b1', type: 1, text: 'Refactor the auth module' },
        b2: {
          bubbleId: 'b2',
          type: 2,
          thinking: { text: 'I will read the file first.' },
          text: 'On it.',
          toolFormerData: { name: 'read_file', toolCallId: 'call-1', rawArgs: { path: 'auth.ts' }, result: 'file contents here' },
        },
      },
    };
    const dbPath = makeVscdb([[`composerData:${composerId}`, composer]]);

    const res = readTrajectoryInputsDetailed(dbPath);
    assert.equal(res.sessionTrajectories.length, 1);
    const t = res.sessionTrajectories[0];
    assert.equal(t.source_agent, 'cursor');
    assert.equal(t.client_source, 'cursor');
    assert.equal(t.session_id, composerId);
    assert.equal(t.session_model, 'claude-sonnet');
    assert.equal(t.task, 'Refactor the auth module');
    assert.equal(t.stats.has_tool_calls, true);
    assert.equal(t.stats.tool_types.read_file, 1);
    assert.match(JSON.stringify(t.turns.filter((x) => x.reasoning)), /read the file first/);
    assert.match(JSON.stringify(t.turns), /file contents here/);
  });

  it('separate bubbleId rows (newer Cursor layout)', () => {
    const composerId = 'comp-bubbles-2';
    const composer = {
      composerId,
      fullConversationHeadersOnly: [{ bubbleId: 'x1' }, { bubbleId: 'x2' }],
      conversationMap: {},
    };
    const rows = [
      [`composerData:${composerId}`, composer],
      [`bubbleId:${composerId}:x1`, { bubbleId: 'x1', type: 1, text: 'Run the build' }],
      [`bubbleId:${composerId}:x2`, { bubbleId: 'x2', type: 2, text: 'Building now', toolFormerData: { name: 'run_terminal_cmd', params: { command: 'npm run build' }, result: 'build ok' } }],
    ];
    const dbPath = makeVscdb(rows);

    const res = readTrajectoryInputsDetailed(dbPath);
    assert.equal(res.sessionTrajectories.length, 1);
    const t = res.sessionTrajectories[0];
    assert.equal(t.task, 'Run the build');
    assert.equal(t.stats.has_tool_calls, true);
    assert.equal(t.stats.tool_types.run_terminal_cmd, 1);
  });

  it('opens the db and skips composers with no recoverable content', () => {
    const dbPath = makeVscdb([
      ['composerData:empty', { composerId: 'empty', conversationMap: {} }],
    ]);
    const res = readTrajectoryInputsDetailed(dbPath);
    assert.equal(res.sessionTrajectories.length, 0); // no crash, no phantom session
  });
});
