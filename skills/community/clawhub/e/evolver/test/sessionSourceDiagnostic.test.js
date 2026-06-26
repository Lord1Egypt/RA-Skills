const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Isolate env so module-level constants in evolve.js resolve to a tmp HOME.
const originalHome = os.homedir();
const tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-sessiondiag-'));
const originalEnv = {
  HOME: process.env.HOME,
  USERPROFILE: process.env.USERPROFILE,
  AGENT_NAME: process.env.AGENT_NAME,
  AGENT_SESSIONS_DIR: process.env.AGENT_SESSIONS_DIR,
  EVOLVER_SESSION_SOURCE: process.env.EVOLVER_SESSION_SOURCE,
  EVOLVER_CURSOR_TRANSCRIPTS_DIR: process.env.EVOLVER_CURSOR_TRANSCRIPTS_DIR,
  CURSOR_TRACE_DIR: process.env.CURSOR_TRACE_DIR,
};

function ensureAgentsRoot() {
  fs.mkdirSync(path.join(tmpHome, '.openclaw', 'agents'), { recursive: true });
}

function clearAgentsRoot() {
  try {
    fs.rmSync(path.join(tmpHome, '.openclaw'), { recursive: true, force: true });
  } catch { /* ignore */ }
}

describe('diagnoseSessionSourceEmpty (session source diagnostics)', () => {
  let diagnoseSessionSourceEmpty;
  let resetSessionSourceWarning;

  before(() => {
    process.env.HOME = tmpHome;
    process.env.USERPROFILE = tmpHome;
    delete process.env.AGENT_NAME;
    delete process.env.AGENT_SESSIONS_DIR;
    delete process.env.EVOLVER_SESSION_SOURCE;
    delete process.env.EVOLVER_CURSOR_TRANSCRIPTS_DIR;
    delete process.env.CURSOR_TRACE_DIR;
    // Require AFTER env is staged so module-level constants resolve to tmpHome.
    // Clear cache first in case another test loaded evolve.js earlier.
    delete require.cache[require.resolve('../src/evolve')];
    ({ diagnoseSessionSourceEmpty, resetSessionSourceWarning } = require('../src/evolve'));
  });

  after(() => {
    for (const [k, v] of Object.entries(originalEnv)) {
      if (v === undefined) delete process.env[k];
      else process.env[k] = v;
    }
    process.env.HOME = originalHome;
    try { fs.rmSync(tmpHome, { recursive: true, force: true }); } catch { /* ignore */ }
  });

  beforeEach(() => {
    clearAgentsRoot();
    if (typeof resetSessionSourceWarning === 'function') resetSessionSourceWarning();
  });

  it('lists candidate OpenClaw agents when AGENT_NAME points to a missing directory', () => {
    ensureAgentsRoot();
    fs.mkdirSync(path.join(tmpHome, '.openclaw', 'agents', 'coder', 'sessions'), { recursive: true });
    fs.mkdirSync(path.join(tmpHome, '.openclaw', 'agents', 'worker-01', 'sessions'), { recursive: true });

    const diag = diagnoseSessionSourceEmpty({
      homedir: tmpHome,
      agentName: 'main',
      sessionSource: 'auto',
      cursorTranscriptsDir: '',
    });

    assert.equal(diag.agentSessionsDirExists, false);
    assert.deepEqual(diag.availableOpenClawAgents.sort(), ['coder', 'worker-01']);
    const hintText = diag.hints.join('\n');
    assert.match(hintText, /AGENT_NAME="main"/);
    assert.match(hintText, /coder/);
    assert.match(hintText, /worker-01/);
  });

  it('emits a "no session sources detected" hint when every source is absent', () => {
    clearAgentsRoot();
    const diag = diagnoseSessionSourceEmpty({
      homedir: tmpHome,
      agentName: 'main',
      sessionSource: 'auto',
      cursorTranscriptsDir: '',
    });
    assert.equal(diag.agentSessionsDirExists, false);
    assert.equal(diag.availableOpenClawAgents.length, 0);
    const hintText = diag.hints.join('\n');
    assert.match(hintText, /No session sources detected/);
  });

  it('warns specifically when SESSION_SOURCE=openclaw but AGENT_SESSIONS_DIR is missing', () => {
    const diag = diagnoseSessionSourceEmpty({
      homedir: tmpHome,
      agentName: 'main',
      sessionSource: 'openclaw',
      cursorTranscriptsDir: '',
    });
    const hintText = diag.hints.join('\n');
    assert.match(hintText, /EVOLVER_SESSION_SOURCE=openclaw/);
    assert.match(hintText, /does not exist/);
  });

  it('warns when SESSION_SOURCE=cursor but no IDE transcript dir exists', () => {
    const diag = diagnoseSessionSourceEmpty({
      homedir: tmpHome,
      agentName: 'main',
      sessionSource: 'cursor',
      cursorTranscriptsDir: '',
    });
    const hintText = diag.hints.join('\n');
    assert.match(hintText, /EVOLVER_SESSION_SOURCE=cursor/);
    assert.match(hintText, /none of ~\/\.cursor, ~\/\.claude, ~\/\.codex/);
  });

  it('produces no hints when the configured OpenClaw agent dir exists', () => {
    const agentDir = path.join(tmpHome, '.openclaw', 'agents', 'main', 'sessions');
    fs.mkdirSync(agentDir, { recursive: true });
    const diag = diagnoseSessionSourceEmpty({
      homedir: tmpHome,
      agentName: 'main',
      agentSessionsDir: agentDir,
      sessionSource: 'auto',
      cursorTranscriptsDir: '',
    });
    assert.equal(diag.agentSessionsDirExists, true);
    assert.equal(diag.hints.length, 0);
  });

  it('treats EVOLVER_CURSOR_TRANSCRIPTS_DIR as a valid source for cursor mode', () => {
    const override = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-cursor-override-'));
    try {
      const diag = diagnoseSessionSourceEmpty({
        homedir: tmpHome,
        agentName: 'main',
        sessionSource: 'cursor',
        cursorTranscriptsDir: override,
      });
      const hintText = diag.hints.join('\n');
      assert.doesNotMatch(hintText, /EVOLVER_SESSION_SOURCE=cursor/);
    } finally {
      try { fs.rmSync(override, { recursive: true, force: true }); } catch { /* ignore */ }
    }
  });
});
