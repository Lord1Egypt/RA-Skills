'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { readTrajectoryInputsDetailed, collectRuntimeSessionInputs } = require('../src/gep/trajectoryExport');

// FIX-3: Gemini CLI runtime adapter. Reads ~/.gemini/tmp/<project>/chats/session-*.{json,jsonl}.
// Builds a session subtree so GEMINI_CLI_FILE_RE matches (it requires the .gemini/tmp/<x>/chats/ path).

function geminiSessionDir() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'gemini-cli-'));
  const dir = path.join(base, '.gemini', 'tmp', 'demo-project', 'chats');
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

const JSONL_LINES = [
  { sessionId: 'sess-1', projectHash: 'abc', startTime: '2026-05-16T04:30:00.000Z', kind: 'main' },
  { id: 'u1', timestamp: '2026-05-16T04:30:10.000Z', type: 'user', content: [{ text: 'Run the unit tests please' }] },
  { $set: { lastUpdated: '2026-05-16T04:30:10.000Z' } },
  {
    id: 'g1',
    timestamp: '2026-05-16T04:30:20.000Z',
    type: 'gemini',
    content: 'Running them now.',
    thoughts: [{ subject: 'Plan', description: 'I should invoke the test runner.' }],
    toolCalls: [{
      id: 'tool-1',
      name: 'run_shell_command',
      args: { command: 'npm test' },
      result: [{ functionResponse: { id: 'tool-1', name: 'run_shell_command', response: { output: 'All tests passed' } } }],
      status: 'success',
    }],
    tokens: { input: 100, output: 20, total: 120 },
    model: 'gemini-3-pro',
  },
  { id: 'info-1', timestamp: '2026-05-16T04:30:25.000Z', type: 'info', content: 'Gemini CLI update available!' },
];

describe('Gemini CLI runtime adapter (FIX-3)', () => {
  it('jsonl: extracts user/assistant/thinking/tool_call/tool_result/model/usage', () => {
    const dir = geminiSessionDir();
    const file = path.join(dir, 'session-2026-05-16T04-30-aaaa.jsonl');
    fs.writeFileSync(file, JSONL_LINES.map((l) => JSON.stringify(l)).join('\n') + '\n');

    const res = readTrajectoryInputsDetailed(file);
    assert.equal(res.sessionTrajectories.length, 1);
    const t = res.sessionTrajectories[0];
    assert.equal(t.source_agent, 'gemini-cli');
    assert.equal(t.client_source, 'gemini-cli');
    assert.equal(t.session_model, 'gemini-3-pro');
    assert.equal(t.task, 'Run the unit tests please');
    assert.equal(t.stats.has_tool_calls, true);
    assert.equal(t.stats.tool_types.run_shell_command, 1);

    const reasoning = t.turns.filter((turn) => turn.reasoning);
    assert.ok(reasoning.length >= 1, 'thoughts must surface as reasoning turns');
    assert.match(JSON.stringify(reasoning), /invoke the test runner/);

    // The functionResponse surfaces as a dedicated tool turn (runtime-session shape: role 'tool' -> a turn
    // whose response_body carries the result text), matching the claude/codex adapters.
    assert.match(JSON.stringify(t.turns), /All tests passed/, 'functionResponse output must be captured');
    // usage aggregates from tokens
    assert.equal(t.stats.input_tokens, 100);
    assert.equal(t.stats.output_tokens, 20);
    // info-type records are dropped
    assert.ok(!JSON.stringify(t.turns).includes('Gemini CLI update available'));
  });

  it('json variant: single pretty-printed session object with messages[]', () => {
    const dir = geminiSessionDir();
    const file = path.join(dir, 'session-2026-04-28T05-44-bbbb.json');
    const session = {
      sessionId: 'sess-json',
      projectHash: 'def',
      messages: JSONL_LINES.filter((l) => l.type),
    };
    fs.writeFileSync(file, JSON.stringify(session, null, 2));

    const res = readTrajectoryInputsDetailed(file);
    assert.equal(res.sessionTrajectories.length, 1);
    const t = res.sessionTrajectories[0];
    assert.equal(t.source_agent, 'gemini-cli');
    assert.equal(t.stats.has_tool_calls, true);
    assert.equal(t.task, 'Run the unit tests please');
  });

  it('gemini adapter never claims logs.json by path (detect scoped to chats/session-*)', () => {
    // The gemini-cli adapter's detect regex must NOT match logs.json, so it can never be parsed as a Gemini
    // session, and auto-discovery only walks chats/ session files. (Mirror of GEMINI_CLI_FILE_RE.)
    const re = /(^|[/\\])\.gemini[/\\]tmp[/\\][^/\\]+[/\\]chats[/\\]session-[^/\\]*\.jsonl?$/i;
    assert.equal(re.test('/home/u/.gemini/tmp/proj/logs.json'), false);
    assert.equal(re.test('/home/u/.gemini/tmp/proj/chats/logs.json'), false);
    assert.equal(re.test('/home/u/.gemini/tmp/proj/chats/session-x.jsonl'), true);
    assert.equal(re.test('/home/u/.gemini/tmp/proj/chats/session-x.json'), true);
  });

  // Regression for the end-to-end discovery gap: Gemini chat records carry no cwd, and the older sessions are
  // .json, so both the workspace gate and the .jsonl-only walker silently dropped every real Gemini session.
  it('auto-discovery surfaces Gemini .json AND .jsonl despite a non-matching workspace + no cwd', () => {
    const tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'gemini-home-'));
    const chats = path.join(tmpHome, '.gemini', 'tmp', 'demo-project', 'chats');
    fs.mkdirSync(chats, { recursive: true });
    const records = JSONL_LINES.filter((l) => l.type);
    // .jsonl variant (header + messages)
    fs.writeFileSync(
      path.join(chats, 'session-2026-05-16T04-30-aaaa.jsonl'),
      JSONL_LINES.map((l) => JSON.stringify(l)).join('\n') + '\n',
    );
    // .json variant (single pretty-printed object) — the one the .jsonl walker can't see.
    fs.writeFileSync(
      path.join(chats, 'session-2026-04-28T05-44-bbbb.json'),
      JSON.stringify({ sessionId: 's-json', messages: records }, null, 2),
    );

    const geminiTmp = path.join(tmpHome, '.gemini', 'tmp');
    // Deliberately non-matching workspace + a fresh homedir so codex/claude defaults don't exist.
    // Gemini CLI runs no evolver session-start hook, so its sessions are never in the marked-sessions
    // registry; under the strict-by-default marking gate they would be excluded. This regression test is
    // specifically about cwd/.json discovery, so opt the marking gate open with includeUnmarked. (A
    // separate test, trajectoryMarkedSessionGate.test.js, covers strict-mode exclusion of unmarked
    // sessions.) Also pin the marked-sessions + trace files into the tmp home so the gate read is hermetic.
    const opts = {
      runtimeSessions: 1,
      homedir: tmpHome,
      runtimeSessionDirs: [geminiTmp],
      workspaceRoot: path.join(tmpHome, 'no-such-workspace'),
      includeUnmarked: 1,
      markedSessionsFile: path.join(tmpHome, 'marked-sessions.jsonl'),
    };

    const discovered = collectRuntimeSessionInputs(opts);
    const geminiFiles = discovered.files.filter((f) => /\.gemini[/\\]tmp[/\\]/.test(f.path));
    assert.equal(geminiFiles.length, 2, 'both .json and .jsonl Gemini sessions must be discovered');
    assert.ok(geminiFiles.some((f) => f.path.endsWith('.json')), '.json variant must be surfaced');
    assert.ok(geminiFiles.some((f) => f.path.endsWith('.jsonl')), '.jsonl variant must be surfaced');

    // Point the default trace file at an empty path inside the tmp home so the read is hermetic and does not
    // pull in (or fail on) the host's real ~/.evomap proxy-traces.jsonl.
    const prevTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    process.env.EVOMAP_PROXY_TRACE_FILE = path.join(tmpHome, 'proxy-traces.jsonl');
    let res;
    try {
      res = readTrajectoryInputsDetailed(null, opts);
    } finally {
      if (prevTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
      else process.env.EVOMAP_PROXY_TRACE_FILE = prevTraceFile;
    }
    const built = res.sessionTrajectories.filter((t) => t.source_agent === 'gemini-cli');
    assert.equal(built.length, 2, 'both Gemini sessions must build trajectories end-to-end');
    assert.ok(built.every((t) => t.stats.turns > 0));
  });
});
