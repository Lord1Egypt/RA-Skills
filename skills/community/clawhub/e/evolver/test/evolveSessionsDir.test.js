// Regression guard for #527: evolve.js must resolve the OpenClaw
// sessions directory via getAgentSessionsDir() so that
// process.env.AGENT_SESSIONS_DIR (commonly set in .env) is honored.
// Prior to 1.78.9 the directory was hard-coded to
// `os.homedir()/.openclaw/agents/<AGENT_NAME>/sessions`, which silently
// dropped user overrides and caused "[NO SESSION LOGS FOUND]" on
// Windows / non-standard OpenClaw layouts.
const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

function freshRequire(modulePath) {
  const resolved = require.resolve(modulePath);
  delete require.cache[resolved];
  return require(resolved);
}

function purgeModuleCache() {
  // evolve.js has many transitive deps; purging only evolve.js would
  // still pick up paths.js from cache. Wipe the entire src tree so
  // each test observes a clean module-load order and reads the
  // current process.env at require time.
  for (const k of Object.keys(require.cache)) {
    if (k.includes(path.sep + 'src' + path.sep)) {
      delete require.cache[k];
    }
  }
}

describe('evolve.js sessions-dir resolution (#527)', () => {
  let tmpDir;
  const savedEnv = {};
  const envKeys = [
    'AGENT_SESSIONS_DIR',
    'AGENT_NAME',
    'EVOLVER_SESSION_SCOPE',
    'EVOLVER_SESSION_SOURCE',
    'EVOLVER_REPO_ROOT',
    'MEMORY_DIR',
    'EVOLUTION_DIR',
    'EVOLVER_QUIET_PARENT_GIT',
    'HUB_OFFLINE',
    'A2A_NODE_SECRET',
  ];

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolve-sessions-'));
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
    // Quiet module-load chatter and avoid any accidental hub chatter.
    process.env.EVOLVER_QUIET_PARENT_GIT = '1';
    process.env.HUB_OFFLINE = '1';
    // Give the module a writable memory/evolution root so its module-level
    // ensureDir calls don't try to create dirs we don't own.
    process.env.MEMORY_DIR = path.join(tmpDir, 'memory');
    process.env.EVOLUTION_DIR = path.join(tmpDir, 'memory', 'evolution');
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    purgeModuleCache();
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    purgeModuleCache();
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('paths.getAgentSessionsDir honors AGENT_SESSIONS_DIR override', () => {
    const override = path.join(tmpDir, 'custom-sessions');
    process.env.AGENT_SESSIONS_DIR = override;
    const { getAgentSessionsDir } = freshRequire('../src/gep/paths');
    assert.equal(getAgentSessionsDir(), override);
  });

  it('paths.getAgentSessionsDir falls back to AGENT_NAME when no override', () => {
    process.env.AGENT_NAME = 'worker-7';
    const { getAgentSessionsDir } = freshRequire('../src/gep/paths');
    const home = process.env.HOME || process.env.USERPROFILE || '';
    assert.equal(getAgentSessionsDir(),
      path.join(home, '.openclaw', 'agents', 'worker-7', 'sessions'));
  });

  it('paths.getAgentSessionsDir derives agent from workspace-<name> scope', () => {
    process.env.EVOLVER_SESSION_SCOPE = 'workspace-proj-alpha';
    const { getAgentSessionsDir } = freshRequire('../src/gep/paths');
    const home = process.env.HOME || process.env.USERPROFILE || '';
    assert.equal(getAgentSessionsDir(),
      path.join(home, '.openclaw', 'agents', 'proj-alpha', 'sessions'));
  });

  it('paths.readSessionCwdFromHead reads cwd from session header', () => {
    const sessionsDir = path.join(tmpDir, 'sessions');
    fs.mkdirSync(sessionsDir, { recursive: true });
    const sessionPath = path.join(sessionsDir, 'session-abc.jsonl');
    const header = { type: 'session', cwd: '/home/alice/proj', sessionId: 'abc' };
    const body = { type: 'turn', role: 'user', content: 'hi' };
    fs.writeFileSync(sessionPath, JSON.stringify(header) + '\n' + JSON.stringify(body) + '\n');
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    assert.equal(readSessionCwdFromHead(sessionPath), '/home/alice/proj');
  });

  it('paths.readSessionCwdFromHead returns null on missing file', () => {
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    assert.equal(readSessionCwdFromHead(path.join(tmpDir, 'nope.jsonl')), null);
  });

  it('paths.readSessionCwdFromHead returns null on malformed header', () => {
    const sessionsDir = path.join(tmpDir, 'sessions');
    fs.mkdirSync(sessionsDir, { recursive: true });
    const sessionPath = path.join(sessionsDir, 'bad.jsonl');
    fs.writeFileSync(sessionPath, 'not-json-at-all\n');
    const { readSessionCwdFromHead } = freshRequire('../src/gep/paths');
    assert.equal(readSessionCwdFromHead(sessionPath), null);
  });

  it('evolve.js reads sessions from AGENT_SESSIONS_DIR override (the #527 regression)', () => {
    const customSessionsDir = path.join(tmpDir, 'win-style', 'data', '.openclaw', 'agents', 'main', 'sessions');
    fs.mkdirSync(customSessionsDir, { recursive: true });

    // Write a recent .jsonl file so readOpenClawSessions would pick it up.
    const sessionPath = path.join(customSessionsDir, 'session-1.jsonl');
    const header = { type: 'session', cwd: tmpDir, sessionId: 'test-1' };
    const turn = { type: 'turn', role: 'user', content: 'integration test for 527' };
    fs.writeFileSync(sessionPath, JSON.stringify(header) + '\n' + JSON.stringify(turn) + '\n');

    process.env.AGENT_SESSIONS_DIR = customSessionsDir;

    // Purge cache so evolve.js reads the env var we just set.
    purgeModuleCache();
    // evolve.js has many deps; grabbing its module side-effects at load time
    // is enough for this regression -- we only need to confirm that the
    // module-level AGENT_SESSIONS_DIR now points at the override. evolve.js
    // does not export AGENT_SESSIONS_DIR directly, but it DOES export
    // diagnoseSessionSourceEmpty() which surfaces the resolved path.
    const evolve = require('../src/evolve');
    const diag = typeof evolve.diagnoseSessionSourceEmpty === 'function'
      ? evolve.diagnoseSessionSourceEmpty()
      : null;

    assert.ok(diag, 'diagnoseSessionSourceEmpty should be exported');
    // Normalize for cross-platform equality (resolve any trailing sep).
    const actual = path.resolve(diag.agentSessionsDir || '');
    const expected = path.resolve(customSessionsDir);
    assert.equal(actual, expected,
      `evolve.js must honor AGENT_SESSIONS_DIR override (got "${actual}", expected "${expected}")`);
    assert.equal(diag.agentSessionsDirExists, true);
  });

  it('evolve.js falls back to default path when AGENT_SESSIONS_DIR is unset', () => {
    delete process.env.AGENT_SESSIONS_DIR;
    process.env.AGENT_NAME = 'test-agent';

    purgeModuleCache();
    const evolve = require('../src/evolve');
    const diag = typeof evolve.diagnoseSessionSourceEmpty === 'function'
      ? evolve.diagnoseSessionSourceEmpty()
      : null;

    assert.ok(diag);
    const home = process.env.HOME || process.env.USERPROFILE || '';
    const expected = path.join(home, '.openclaw', 'agents', 'test-agent', 'sessions');
    assert.equal(path.resolve(diag.agentSessionsDir || ''), path.resolve(expected));
  });
});
