'use strict';

// v1 marking gate (strict-by-default): the runtime-session discovery link only
// collects transcripts whose session_id evolver actively marked via the
// session-start hook (recorded in marked-sessions.jsonl), minus those the proxy
// gateway already captured (proxy-traces.jsonl, joined on session_id_sha256).
//
// Covers:
//   1. The session-start hook writes the tool's stdin session_id into the
//      marked-sessions registry, end-to-end (real child process).
//   2. A marked runtime session is collected; an unmarked one is excluded under
//      strict mode and re-admitted with includeUnmarked.
//   3. A session whose id is already gateway-captured (hash match) is skipped;
//      re-admitted with includeGatewayCaptured.

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('node:child_process');

const repoRoot = path.resolve(__dirname, '..');
const sessionStartScript = path.join(repoRoot, 'src', 'adapters', 'scripts', 'evolver-session-start.js');
const { collectRuntimeSessionInputs } = require('../src/gep/trajectoryExport');
const { hashTraceValue } = require('../src/proxy/trace/extractor');

function tmpHome() {
  return fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'mark-gate-')));
}

function writeClaudeSession(home, sessionId) {
  const dir = path.join(home, '.claude', 'projects', 'proj');
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, `${sessionId}.jsonl`);
  fs.writeFileSync(file, [
    { type: 'user', cwd: home, message: { role: 'user', content: [{ type: 'text', text: 'Please do a real task, not a meta marker.' }] } },
    { type: 'assistant', cwd: home, message: { role: 'assistant', content: [{ type: 'text', text: 'Done, here is the real assistant content.' }] } },
  ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');
  return file;
}

function discoveredSessionIds(opts) {
  return collectRuntimeSessionInputs(opts).files
    .map((f) => path.basename(f.path).replace(/\.jsonl$/i, ''))
    .sort();
}

describe('v1 marking gate', () => {
  it('session-start hook writes the stdin session_id into the marked-sessions registry', () => {
    const home = tmpHome();
    try {
      const markedFile = path.join(home, '.evolver', 'marked-sessions.jsonl');
      const res = spawnSync(process.execPath, [sessionStartScript], {
        input: JSON.stringify({ session_id: 'hook-session-xyz', cwd: home, source: 'claude-code' }),
        env: {
          ...process.env,
          HOME: home,
          EVOLVER_MARKED_SESSIONS_FILE: markedFile,
          EVOLVER_SESSION_AUTO_RESTART: '0',
          EVOLVER_SESSION_SOURCE: '',
        },
        encoding: 'utf8',
        timeout: 8000,
      });

      assert.equal(res.status, 0, `hook should exit 0; stderr: ${res.stderr}`);
      // stdout is still valid JSON (context injection contract is preserved).
      assert.doesNotThrow(() => JSON.parse(res.stdout || '{}'));

      const lines = fs.readFileSync(markedFile, 'utf8').trim().split('\n').filter(Boolean);
      assert.equal(lines.length, 1, 'exactly one mark record should be written');
      const record = JSON.parse(lines[0]);
      assert.equal(record.session_id, 'hook-session-xyz');
      assert.ok(typeof record.marked_at === 'string' && record.marked_at, 'marked_at timestamp present');
    } finally {
      fs.rmSync(home, { recursive: true, force: true });
    }
  });

  it('hook with no session_id on stdin writes nothing but still emits context JSON', () => {
    const home = tmpHome();
    try {
      const markedFile = path.join(home, '.evolver', 'marked-sessions.jsonl');
      const res = spawnSync(process.execPath, [sessionStartScript], {
        input: JSON.stringify({ cwd: home }), // no session_id
        env: {
          ...process.env,
          HOME: home,
          EVOLVER_MARKED_SESSIONS_FILE: markedFile,
          EVOLVER_SESSION_AUTO_RESTART: '0',
        },
        encoding: 'utf8',
        timeout: 8000,
      });
      assert.equal(res.status, 0);
      assert.doesNotThrow(() => JSON.parse(res.stdout || '{}'));
      assert.equal(fs.existsSync(markedFile), false, 'no registry file when there is no session_id to mark');
    } finally {
      fs.rmSync(home, { recursive: true, force: true });
    }
  });

  it('strict mode collects a marked session and excludes an unmarked one; includeUnmarked re-admits it', () => {
    const home = tmpHome();
    const prevTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    try {
      writeClaudeSession(home, 'marked-session');
      writeClaudeSession(home, 'unmarked-session');
      const markedFile = path.join(home, 'marked-sessions.jsonl');
      fs.writeFileSync(markedFile, JSON.stringify({ session_id: 'marked-session', marked_at: 'x' }) + '\n');
      // Hermetic empty trace file so the gateway gate has nothing to exclude.
      process.env.EVOMAP_PROXY_TRACE_FILE = path.join(home, 'no-traces.jsonl');

      const baseOpts = {
        runtimeSessions: 1,
        homedir: home,
        runtimeSessionDirs: [path.join(home, '.claude', 'projects')],
        workspaceRoot: home,
        markedSessionsFile: markedFile,
      };

      assert.deepEqual(discoveredSessionIds(baseOpts), ['marked-session'],
        'strict mode keeps only the marked session');

      const withUnmarked = collectRuntimeSessionInputs({ ...baseOpts, includeUnmarked: 1 });
      assert.deepEqual(
        withUnmarked.files.map((f) => path.basename(f.path).replace(/\.jsonl$/i, '')).sort(),
        ['marked-session', 'unmarked-session'],
        'includeUnmarked re-admits the unmarked session',
      );

      // Discovery summary reports the gate decision.
      const strict = collectRuntimeSessionInputs(baseOpts);
      assert.equal(strict.discovery.markGate.enforceMarked, true);
      assert.equal(strict.discovery.markGate.excludedByMark, 1);
    } finally {
      if (prevTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
      else process.env.EVOMAP_PROXY_TRACE_FILE = prevTraceFile;
      fs.rmSync(home, { recursive: true, force: true });
    }
  });

  it('skips a session the gateway already captured (hash join); includeGatewayCaptured re-admits it', () => {
    const home = tmpHome();
    const prevTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    try {
      writeClaudeSession(home, 'fresh-session');
      writeClaudeSession(home, 'already-captured');
      const markedFile = path.join(home, 'marked-sessions.jsonl');
      // Both are marked; the gateway gate is what differentiates them.
      fs.writeFileSync(markedFile, [
        { session_id: 'fresh-session', marked_at: 'x' },
        { session_id: 'already-captured', marked_at: 'x' },
      ].map((r) => JSON.stringify(r)).join('\n') + '\n');

      // proxy-traces.jsonl stores the hashed session id exactly as the proxy does.
      const traceFile = path.join(home, 'proxy-traces.jsonl');
      fs.writeFileSync(traceFile, JSON.stringify({
        event: 'llm_turn',
        sessionId: hashTraceValue('already-captured', 'session_id_sha256'),
      }) + '\n');
      process.env.EVOMAP_PROXY_TRACE_FILE = traceFile;

      const baseOpts = {
        runtimeSessions: 1,
        homedir: home,
        runtimeSessionDirs: [path.join(home, '.claude', 'projects')],
        workspaceRoot: home,
        markedSessionsFile: markedFile,
      };

      assert.deepEqual(discoveredSessionIds(baseOpts), ['fresh-session'],
        'strict mode skips the gateway-captured session');

      const withGateway = collectRuntimeSessionInputs({ ...baseOpts, includeGatewayCaptured: 1 });
      assert.deepEqual(
        withGateway.files.map((f) => path.basename(f.path).replace(/\.jsonl$/i, '')).sort(),
        ['already-captured', 'fresh-session'],
        'includeGatewayCaptured re-admits the gateway-captured session',
      );

      const strict = collectRuntimeSessionInputs(baseOpts);
      assert.equal(strict.discovery.markGate.excludedByGateway, 1);
      assert.equal(strict.discovery.markGate.gatewayCapturedCount, 1);
    } finally {
      if (prevTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
      else process.env.EVOMAP_PROXY_TRACE_FILE = prevTraceFile;
      fs.rmSync(home, { recursive: true, force: true });
    }
  });

  it('CLI: --runtime-sessions is strict by default and --include-unmarked opens the gate', () => {
    const home = tmpHome();
    try {
      writeClaudeSession(home, 'cli-marked');
      writeClaudeSession(home, 'cli-unmarked');
      const markedFile = path.join(home, 'marked-sessions.jsonl');
      fs.writeFileSync(markedFile, JSON.stringify({ session_id: 'cli-marked', marked_at: 'x' }) + '\n');
      const claudeProjects = path.join(home, '.claude', 'projects');
      const indexJs = path.join(repoRoot, 'index.js');
      const env = {
        ...process.env,
        HOME: home,
        EVOMAP_PROXY_TRACE_FILE: path.join(home, 'no-traces.jsonl'),
        A2A_NODE_SECRET: '',
        EVOMAP_NODE_SECRET: '',
      };

      const runExport = (extraArgs) => {
        const output = path.join(home, `out-${Math.random().toString(36).slice(2)}.jsonl`);
        const res = spawnSync(process.execPath, [
          indexJs, 'trajectory-export',
          '--runtime-sessions',
          '--runtime-session-dir', claudeProjects,
          '--marked-sessions-file', markedFile,
          '--output', output,
          ...extraArgs,
        ], { cwd: home, env, encoding: 'utf8', timeout: 20000 });
        assert.equal(res.status, 0, `export should exit 0; stderr: ${res.stderr}`);
        const sids = fs.existsSync(output)
          ? fs.readFileSync(output, 'utf8').trim().split('\n').filter(Boolean)
            .map((l) => JSON.parse(l).session_id).sort()
          : [];
        return sids;
      };

      // Strict by default: only the marked session is exported. (Workspace cwd
      // gating still applies; the sessions carry cwd=home and the CLI runs with
      // cwd=home, so both pass the cwd gate and the marking gate is what filters.)
      const strict = runExport([]);
      assert.ok(strict.includes('cli-marked'), 'strict export includes the marked session');
      assert.ok(!strict.includes('cli-unmarked'), 'strict export excludes the unmarked session');

      const open = runExport(['--include-unmarked']);
      assert.ok(open.includes('cli-marked') && open.includes('cli-unmarked'),
        '--include-unmarked exports both sessions');
    } finally {
      fs.rmSync(home, { recursive: true, force: true });
    }
  });

  it('strict mode with an empty/missing registry excludes everything (fail-closed)', () => {
    const home = tmpHome();
    const prevTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    try {
      writeClaudeSession(home, 'orphan-session');
      process.env.EVOMAP_PROXY_TRACE_FILE = path.join(home, 'no-traces.jsonl');
      const opts = {
        runtimeSessions: 1,
        homedir: home,
        runtimeSessionDirs: [path.join(home, '.claude', 'projects')],
        workspaceRoot: home,
        markedSessionsFile: path.join(home, 'does-not-exist.jsonl'),
      };
      assert.deepEqual(discoveredSessionIds(opts), [], 'no marked sessions -> nothing collected');
    } finally {
      if (prevTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
      else process.env.EVOMAP_PROXY_TRACE_FILE = prevTraceFile;
      fs.rmSync(home, { recursive: true, force: true });
    }
  });
});
