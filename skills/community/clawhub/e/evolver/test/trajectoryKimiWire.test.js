'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { readTrajectoryInputsDetailed, collectRuntimeSessionInputs } = require('../src/gep/trajectoryExport');

// FIX-5: Kimi CLI wire.jsonl adapter. Build a ~/.kimi/sessions/<hash>/<id>/wire.jsonl subtree so
// KIMI_WIRE_FILE_RE matches.

function kimiWireFile(lines) {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'kimi-wire-'));
  const dir = path.join(base, '.kimi', 'sessions', 'workspacehash', 'sess-id');
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, 'wire.jsonl');
  fs.writeFileSync(file, lines.map((l) => JSON.stringify(l)).join('\n') + '\n');
  return file;
}

describe('Kimi CLI wire.jsonl adapter (FIX-5)', () => {
  it('parses user/thinking/text/tool_call/tool_result with plaintext thinking', () => {
    const file = kimiWireFile([
      { type: 'metadata', protocol_version: '1.10' },
      { timestamp: 1779370805.04, message: { type: 'TurnBegin', payload: { user_input: [{ type: 'text', text: 'Read the README' }] } } },
      { timestamp: 1779370806.0, message: { type: 'ContentPart', payload: { type: 'think', think: 'I should read the file first.' } } },
      { timestamp: 1779370806.5, message: { type: 'ContentPart', payload: { type: 'text', text: 'Sure, reading it.' } } },
      { timestamp: 1779370807.0, message: { type: 'ToolCall', payload: { type: 'function', id: 'tool_1', function: { name: 'ReadFile', arguments: '{"path":"README.md"}' } } } },
      { timestamp: 1779370808.0, message: { type: 'ToolResult', payload: { tool_call_id: 'tool_1', return_value: { is_error: false, output: '# Title\nbody' } } } },
      { timestamp: 1779370809.0, message: { type: 'TurnEnd', payload: {} } },
    ]);

    const res = readTrajectoryInputsDetailed(file);
    assert.equal(res.sessionTrajectories.length, 1);
    const t = res.sessionTrajectories[0];
    assert.equal(t.source_agent, 'kimi');
    assert.equal(t.client_source, 'kimi-cli');
    assert.equal(t.task, 'Read the README');
    assert.equal(t.stats.has_tool_calls, true);
    assert.equal(t.stats.tool_types.ReadFile, 1);

    const reasoning = t.turns.filter((x) => x.reasoning);
    assert.ok(reasoning.length >= 1, 'plaintext thinking must surface as reasoning');
    assert.match(JSON.stringify(reasoning), /read the file first/);
    assert.match(JSON.stringify(t.turns), /# Title/, 'tool result output must be captured');
  });

  it('error tool result is flagged', () => {
    const file = kimiWireFile([
      { type: 'metadata', protocol_version: '1.10' },
      { timestamp: 1, message: { type: 'TurnBegin', payload: { user_input: [{ type: 'text', text: 'run it' }] } } },
      { timestamp: 2, message: { type: 'ToolCall', payload: { id: 'c1', function: { name: 'Shell', arguments: '{"cmd":"false"}' } } } },
      { timestamp: 3, message: { type: 'ToolResult', payload: { tool_call_id: 'c1', return_value: { is_error: true, output: 'exit 1' } } } },
    ]);
    const res = readTrajectoryInputsDetailed(file);
    const t = res.sessionTrajectories[0];
    assert.ok(t);
    assert.match(JSON.stringify(t.turns), /"error":"exit 1"/);
  });

  // Regression for the discovery gap: Kimi wire.jsonl carries no cwd (only a hashed workspace dir), so the
  // workspace gate (transcriptBelongsToWorkspace) silently dropped every Kimi session under auto-discovery.
  // The Kimi adapter must be workspaceScoped:false (like Gemini CLI) so a wire.jsonl in the default discovery
  // dir surfaces even from an UNRELATED workspace. (The earlier FIX-3 residual commit only patched Gemini.)
  it('auto-discovery surfaces a Kimi wire.jsonl from an unrelated workspace (no cwd, hashed workspace dir)', () => {
    const tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'kimi-home-'));
    const dir = path.join(tmpHome, '.kimi', 'sessions', 'a1b2c3workspacehash', 'sess-discover-1');
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(
      path.join(dir, 'wire.jsonl'),
      [
        { type: 'metadata', protocol_version: '1.10' },
        { timestamp: 1779370805.04, message: { type: 'TurnBegin', payload: { user_input: [{ type: 'text', text: 'List the files' }] } } },
        { timestamp: 1779370806.0, message: { type: 'ContentPart', payload: { type: 'think', think: 'I will list them.' } } },
        { timestamp: 1779370807.0, message: { type: 'ToolCall', payload: { id: 'tool_1', function: { name: 'ListDir', arguments: '{"path":"."}' } } } },
        { timestamp: 1779370808.0, message: { type: 'ToolResult', payload: { tool_call_id: 'tool_1', return_value: { is_error: false, output: 'a.txt\nb.txt' } } } },
      ].map((l) => JSON.stringify(l)).join('\n') + '\n',
    );

    const kimiSessions = path.join(tmpHome, '.kimi', 'sessions');
    // Deliberately non-matching workspace + a fresh homedir so codex/claude defaults don't exist. If the Kimi
    // adapter were still workspaceScoped, the gate would drop this file because its cwd can never be resolved.
    // Kimi CLI runs no evolver session-start hook (and its wire.jsonl basename carries no session id), so it
    // can never be in the marked-sessions registry; under the strict marking gate it would be excluded. This
    // discovery test predates that gate, so opt it open with includeUnmarked and pin a hermetic registry path.
    const opts = {
      runtimeSessions: 1,
      homedir: tmpHome,
      runtimeSessionDirs: [kimiSessions],
      workspaceRoot: path.join(tmpHome, 'no-such-unrelated-workspace'),
      includeUnmarked: 1,
      markedSessionsFile: path.join(tmpHome, 'marked-sessions.jsonl'),
    };

    const discovered = collectRuntimeSessionInputs(opts);
    const kimiFiles = discovered.files.filter((f) => /\.kimi[/\\]sessions[/\\]/.test(f.path));
    assert.equal(kimiFiles.length, 1, 'Kimi wire.jsonl must be discovered despite an unrelated workspace + no cwd');

    // And it must build a real trajectory end-to-end through the discovery chain.
    const prevTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    process.env.EVOMAP_PROXY_TRACE_FILE = path.join(tmpHome, 'proxy-traces.jsonl');
    let res;
    try {
      res = readTrajectoryInputsDetailed(null, opts);
    } finally {
      if (prevTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
      else process.env.EVOMAP_PROXY_TRACE_FILE = prevTraceFile;
    }
    const built = res.sessionTrajectories.filter((x) => x.source_agent === 'kimi');
    assert.equal(built.length, 1, 'the discovered Kimi session must build a trajectory end-to-end');
    assert.equal(built[0].task, 'List the files');
    assert.ok(built[0].stats.turns > 0);
    assert.equal(built[0].stats.tool_types.ListDir, 1);
  });
});
