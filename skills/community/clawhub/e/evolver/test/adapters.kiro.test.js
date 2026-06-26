const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const fs = require('fs');
const os = require('os');

const hookAdapter = require('../src/adapters/hookAdapter');
const kiroAdapter = require('../src/adapters/kiro');

function makeTmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-kiro-test-'));
}

function cleanup(dir) {
  try { fs.rmSync(dir, { recursive: true, force: true }); } catch {}
}

describe('kiro: registration in hookAdapter', () => {
  it('PLATFORMS contains kiro entry', () => {
    assert.ok(hookAdapter.PLATFORMS.kiro, 'PLATFORMS.kiro must be defined');
    assert.equal(hookAdapter.PLATFORMS.kiro.configDir, '.kiro');
    assert.equal(hookAdapter.PLATFORMS.kiro.detector, '.kiro');
    assert.equal(hookAdapter.PLATFORMS.kiro.name, 'Kiro');
  });

  it('loadAdapter("kiro") returns kiro module', () => {
    const mod = hookAdapter.loadAdapter('kiro');
    assert.ok(mod);
    assert.equal(typeof mod.install, 'function');
    assert.equal(typeof mod.uninstall, 'function');
  });

  it('detectPlatform finds kiro from .kiro directory', () => {
    const tmp = makeTmpDir();
    try {
      fs.mkdirSync(path.join(tmp, '.kiro'), { recursive: true });
      assert.equal(hookAdapter.detectPlatform(tmp), 'kiro');
    } finally { cleanup(tmp); }
  });
});

describe('kiro adapter: buildHookConfig', () => {
  it('produces three hook kinds with required schema fields', () => {
    for (const kind of ['sessionStart', 'signalDetect', 'sessionEnd']) {
      const cfg = kiroAdapter.buildHookConfig(kind, '.kiro/hooks');
      assert.equal(typeof cfg.name, 'string', `${kind} missing name`);
      assert.equal(cfg.version, '1', `${kind} version must be "1"`);
      assert.equal(typeof cfg.description, 'string', `${kind} missing description`);
      assert.ok(cfg.when && typeof cfg.when.type === 'string', `${kind} missing when.type`);
      assert.equal(cfg.then.type, 'runCommand', `${kind} must use runCommand`);
      assert.equal(typeof cfg.then.command, 'string', `${kind} missing command`);
      assert.ok(cfg.then.timeout > 0, `${kind} must have positive timeout`);
      assert.equal(cfg._evolver_managed, true, `${kind} must mark managed`);
    }
  });

  it('maps sessionStart -> promptSubmit and sets dedup env flag', () => {
    const cfg = kiroAdapter.buildHookConfig('sessionStart', '.kiro/hooks');
    assert.equal(cfg.when.type, 'promptSubmit');
    assert.match(cfg.then.command, /EVOLVER_SESSION_START_DEDUP=1/);
    assert.match(cfg.then.command, /evolver-session-start\.js/);
  });

  it('maps signalDetect -> postToolUse with write filter', () => {
    const cfg = kiroAdapter.buildHookConfig('signalDetect', '.kiro/hooks');
    assert.equal(cfg.when.type, 'postToolUse');
    assert.deepEqual(cfg.when.toolTypes, ['write']);
    assert.match(cfg.then.command, /evolver-signal-detect\.js/);
  });

  it('maps sessionEnd -> agentStop', () => {
    const cfg = kiroAdapter.buildHookConfig('sessionEnd', '.kiro/hooks');
    assert.equal(cfg.when.type, 'agentStop');
    assert.match(cfg.then.command, /evolver-session-end\.js/);
    assert.equal(cfg.then.timeout, 8);
  });
});

describe('kiro adapter: install', () => {
  it('writes three .kiro.hook files, copies scripts, injects AGENTS.md section', () => {
    const tmp = makeTmpDir();
    try {
      fs.mkdirSync(path.join(tmp, '.kiro'), { recursive: true });
      const evolverRoot = path.resolve(__dirname, '..');
      const result = kiroAdapter.install({ configRoot: tmp, evolverRoot, force: true });
      assert.equal(result.ok, true);
      assert.equal(result.platform, 'kiro');

      const hooksDir = path.join(tmp, '.kiro', 'hooks');
      for (const file of Object.values(kiroAdapter.HOOK_FILES)) {
        const full = path.join(hooksDir, file);
        assert.ok(fs.existsSync(full), `hook file missing: ${file}`);
        const parsed = JSON.parse(fs.readFileSync(full, 'utf8'));
        assert.equal(parsed._evolver_managed, true);
      }

      for (const script of ['evolver-session-start.js', 'evolver-signal-detect.js', 'evolver-session-end.js']) {
        assert.ok(fs.existsSync(path.join(hooksDir, script)), `script missing: ${script}`);
      }

      const agentsMd = fs.readFileSync(path.join(tmp, 'AGENTS.md'), 'utf8');
      assert.ok(agentsMd.includes('Evolution Memory'));
      assert.ok(agentsMd.includes('evolver-evolution-memory'));
    } finally { cleanup(tmp); }
  });

  it('skips when already installed without force', () => {
    const tmp = makeTmpDir();
    try {
      fs.mkdirSync(path.join(tmp, '.kiro'), { recursive: true });
      const evolverRoot = path.resolve(__dirname, '..');
      kiroAdapter.install({ configRoot: tmp, evolverRoot, force: true });
      const result = kiroAdapter.install({ configRoot: tmp, evolverRoot, force: false });
      assert.equal(result.ok, true);
      assert.equal(result.skipped, true);
    } finally { cleanup(tmp); }
  });

  it('produces hook files whose JSON matches buildHookConfig output', () => {
    const tmp = makeTmpDir();
    try {
      fs.mkdirSync(path.join(tmp, '.kiro'), { recursive: true });
      const evolverRoot = path.resolve(__dirname, '..');
      kiroAdapter.install({ configRoot: tmp, evolverRoot, force: true });
      const hooksDir = path.join(tmp, '.kiro', 'hooks');

      const sessionStartFile = JSON.parse(
        fs.readFileSync(path.join(hooksDir, kiroAdapter.HOOK_FILES.sessionStart), 'utf8')
      );
      const expected = kiroAdapter.buildHookConfig('sessionStart', '.kiro/hooks');
      assert.equal(sessionStartFile.name, expected.name);
      assert.equal(sessionStartFile.when.type, expected.when.type);
      assert.equal(sessionStartFile.then.command, expected.then.command);
    } finally { cleanup(tmp); }
  });
});

describe('kiro adapter: uninstall', () => {
  it('removes hook files and scripts, strips AGENTS.md section', () => {
    const tmp = makeTmpDir();
    try {
      fs.mkdirSync(path.join(tmp, '.kiro'), { recursive: true });
      const evolverRoot = path.resolve(__dirname, '..');
      kiroAdapter.install({ configRoot: tmp, evolverRoot, force: true });

      const result = kiroAdapter.uninstall({ configRoot: tmp });
      assert.equal(result.ok, true);
      assert.equal(result.removed, true);

      const hooksDir = path.join(tmp, '.kiro', 'hooks');
      for (const file of Object.values(kiroAdapter.HOOK_FILES)) {
        assert.ok(!fs.existsSync(path.join(hooksDir, file)), `hook file not removed: ${file}`);
      }
      for (const script of ['evolver-session-start.js', 'evolver-signal-detect.js', 'evolver-session-end.js']) {
        assert.ok(!fs.existsSync(path.join(hooksDir, script)), `script not removed: ${script}`);
      }

      const agentsMd = fs.readFileSync(path.join(tmp, 'AGENTS.md'), 'utf8');
      assert.ok(!agentsMd.includes('evolver-evolution-memory'));
    } finally { cleanup(tmp); }
  });

  it('does not remove user-authored non-evolver .kiro.hook files', () => {
    const tmp = makeTmpDir();
    try {
      const hooksDir = path.join(tmp, '.kiro', 'hooks');
      fs.mkdirSync(hooksDir, { recursive: true });
      const userHookPath = path.join(hooksDir, 'user-custom.kiro.hook');
      fs.writeFileSync(userHookPath, JSON.stringify({
        name: 'User Custom Hook',
        version: '1',
        when: { type: 'promptSubmit' },
        then: { type: 'runCommand', command: 'echo hello', timeout: 1 },
      }));

      const evolverRoot = path.resolve(__dirname, '..');
      kiroAdapter.install({ configRoot: tmp, evolverRoot, force: true });
      kiroAdapter.uninstall({ configRoot: tmp });

      assert.ok(fs.existsSync(userHookPath), 'user-authored hook must be preserved');
      const content = JSON.parse(fs.readFileSync(userHookPath, 'utf8'));
      assert.equal(content.name, 'User Custom Hook');
    } finally { cleanup(tmp); }
  });

  it('returns ok with removed=false when nothing to remove', () => {
    const tmp = makeTmpDir();
    try {
      fs.mkdirSync(path.join(tmp, '.kiro'), { recursive: true });
      const result = kiroAdapter.uninstall({ configRoot: tmp });
      assert.equal(result.ok, true);
      assert.equal(result.removed, false);
    } finally { cleanup(tmp); }
  });
});

describe('kiro adapter: isEvolverManagedHookFile', () => {
  it('detects files with _evolver_managed flag', () => {
    const tmp = makeTmpDir();
    try {
      const p = path.join(tmp, 'a.kiro.hook');
      fs.writeFileSync(p, JSON.stringify({ _evolver_managed: true, name: 'x' }));
      assert.equal(kiroAdapter.isEvolverManagedHookFile(p), true);
    } finally { cleanup(tmp); }
  });

  it('detects files whose name starts with Evolver', () => {
    const tmp = makeTmpDir();
    try {
      const p = path.join(tmp, 'a.kiro.hook');
      fs.writeFileSync(p, JSON.stringify({ name: 'Evolver Foo', when: {}, then: {} }));
      assert.equal(kiroAdapter.isEvolverManagedHookFile(p), true);
    } finally { cleanup(tmp); }
  });

  it('rejects non-evolver files', () => {
    const tmp = makeTmpDir();
    try {
      const p = path.join(tmp, 'a.kiro.hook');
      fs.writeFileSync(p, JSON.stringify({ name: 'My Hook', when: {}, then: { command: 'ls' } }));
      assert.equal(kiroAdapter.isEvolverManagedHookFile(p), false);
    } finally { cleanup(tmp); }
  });

  it('handles malformed JSON gracefully', () => {
    const tmp = makeTmpDir();
    try {
      const p = path.join(tmp, 'a.kiro.hook');
      fs.writeFileSync(p, '{not json');
      assert.equal(kiroAdapter.isEvolverManagedHookFile(p), false);
    } finally { cleanup(tmp); }
  });
});

describe('session-start dedup guard', () => {
  const scriptPath = path.resolve(__dirname, '..', 'src', 'adapters', 'scripts', 'evolver-session-start.js');
  const { execFileSync } = require('child_process');

  it('emits context on first run and empty on second run within TTL', () => {
    const tmp = makeTmpDir();
    try {
      const stateDir = path.join(tmp, 'state');
      const env = {
        ...process.env,
        EVOLVER_SESSION_START_DEDUP: '1',
        EVOLVER_SESSION_STATE_DIR: stateDir,
      };

      const first = execFileSync('node', [scriptPath], { cwd: tmp, env, input: '', encoding: 'utf8' });
      const second = execFileSync('node', [scriptPath], { cwd: tmp, env, input: '', encoding: 'utf8' });

      let secondParsed = {};
      try { secondParsed = JSON.parse(second); } catch { /* blank */ }
      assert.deepEqual(secondParsed, {}, 'second invocation must be suppressed');

      assert.ok(fs.existsSync(path.join(stateDir, 'session-start-state.json')), 'state file must be created');
    } finally { cleanup(tmp); }
  });

  it('does not dedup when EVOLVER_SESSION_START_DEDUP is not set', () => {
    const tmp = makeTmpDir();
    try {
      const stateDir = path.join(tmp, 'state');
      const env = { ...process.env, EVOLVER_SESSION_STATE_DIR: stateDir };
      delete env.EVOLVER_SESSION_START_DEDUP;

      execFileSync('node', [scriptPath], { cwd: tmp, env, input: '', encoding: 'utf8' });
      assert.ok(!fs.existsSync(path.join(stateDir, 'session-start-state.json')),
        'state file must NOT be created when dedup disabled');
    } finally { cleanup(tmp); }
  });
});
