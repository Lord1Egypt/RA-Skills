const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  rejectPendingRun,
  isPendingSolidify,
  readJsonSafe,
  CycleTimeoutError,
  handleCycleTimeout,
  waitForTimedOutEvolvePromise,
} = require('../index.js');

const savedEnv = {};
const envKeys = [
  'EVOLVER_REPO_ROOT', 'OPENCLAW_WORKSPACE', 'EVOLUTION_DIR',
  'MEMORY_DIR', 'A2A_HUB_URL', 'HEARTBEAT_INTERVAL_MS', 'WORKER_ENABLED',
  'EVOLVER_LOCK_DIR', 'EVOLVER_SETTINGS_DIR', 'EVOMAP_PROXY',
  'EVOMAP_PROXY_AUTO_INJECT', 'CLAUDE_SETTINGS_FILE', 'EVOLVER_SUICIDE',
  'EVOLVER_CYCLE_TIMEOUT_ENABLED', 'EVOLVER_CYCLE_TIMEOUT_MS',
];
let tmpDir;

function removeTmpDir(dir) {
  if (!dir) return;
  try {
    fs.rmSync(dir, {
      recursive: true,
      force: true,
      maxRetries: process.platform === 'win32' ? 20 : 3,
      retryDelay: 100,
    });
  } catch (err) {
    // Best-effort teardown. This runs in afterEach, AFTER the test's
    // assertions have already passed. On Windows a daemon spawned with
    // cwd=tmpDir (or a grandchild that outlives the synchronous spawnSync)
    // can hold a handle on the directory past the retry window, so rmSync
    // still throws EBUSY — which surfaced as a `hookFailed` red on
    // `loop-mode EVOLVE_BRIDGE default (#96)`. CI runners are ephemeral and a
    // leftover temp dir is harmless, so a cleanup race must never fail an
    // otherwise-passing test.
    console.warn(`[loopMode.test] best-effort tmp cleanup failed: ${err && (err.code || err.message)}`);
  }
}

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-loop-test-'));
  for (const k of envKeys) { savedEnv[k] = process.env[k]; }
  process.env.EVOLVER_REPO_ROOT = tmpDir;
  process.env.OPENCLAW_WORKSPACE = tmpDir;
  process.env.EVOLUTION_DIR = path.join(tmpDir, 'memory', 'evolution');
  process.env.MEMORY_DIR = path.join(tmpDir, 'memory');
  process.env.A2A_HUB_URL = '';
  process.env.HEARTBEAT_INTERVAL_MS = '3600000';
  process.env.EVOLVER_LOCK_DIR = tmpDir;
  process.env.EVOLVER_SETTINGS_DIR = path.join(tmpDir, '.evolver-settings');
  process.env.EVOMAP_PROXY = '0';
  process.env.EVOMAP_PROXY_AUTO_INJECT = 'off';
  process.env.CLAUDE_SETTINGS_FILE = path.join(tmpDir, '.claude', 'settings.json');
  process.env.EVOLVER_SUICIDE = 'false';
  process.env.EVOLVER_CYCLE_TIMEOUT_ENABLED = 'false';
  process.env.EVOLVER_CYCLE_TIMEOUT_MS = '2700000';
  delete process.env.WORKER_ENABLED;
});

afterEach(() => {
  for (const k of envKeys) {
    if (savedEnv[k] === undefined) delete process.env[k];
    else process.env[k] = savedEnv[k];
  }
  removeTmpDir(tmpDir);
});

describe('loop-mode auto reject', () => {
  it('marks pending runs rejected without deleting untracked files', () => {
    const stateDir = path.join(tmpDir, 'memory', 'evolution');
    fs.mkdirSync(stateDir, { recursive: true });
    fs.writeFileSync(path.join(stateDir, 'evolution_solidify_state.json'), JSON.stringify({
      last_run: { run_id: 'run_123' }
    }, null, 2));
    fs.writeFileSync(path.join(tmpDir, 'PR_BODY.md'), 'keep me\n');
    const changed = rejectPendingRun(path.join(stateDir, 'evolution_solidify_state.json'));

    const state = JSON.parse(fs.readFileSync(path.join(stateDir, 'evolution_solidify_state.json'), 'utf8'));
    assert.equal(changed, true);
    assert.equal(state.last_solidify.run_id, 'run_123');
    assert.equal(state.last_solidify.rejected, true);
    assert.equal(state.last_solidify.reason, 'loop_bridge_disabled_autoreject_no_rollback');
    assert.equal(fs.readFileSync(path.join(tmpDir, 'PR_BODY.md'), 'utf8'), 'keep me\n');
  });
});

describe('isPendingSolidify', () => {
  it('returns false when state is null', () => {
    assert.equal(isPendingSolidify(null), false);
  });

  it('returns false when state has no last_run', () => {
    assert.equal(isPendingSolidify({}), false);
  });

  it('returns false when last_run has no run_id', () => {
    assert.equal(isPendingSolidify({ last_run: {} }), false);
  });

  it('returns true when last_run has run_id but no last_solidify', () => {
    assert.equal(isPendingSolidify({ last_run: { run_id: 'run_1' } }), true);
  });

  it('returns true when last_solidify run_id differs from last_run', () => {
    assert.equal(isPendingSolidify({
      last_run: { run_id: 'run_2' },
      last_solidify: { run_id: 'run_1' },
    }), true);
  });

  it('returns false when last_solidify run_id matches last_run', () => {
    assert.equal(isPendingSolidify({
      last_run: { run_id: 'run_1' },
      last_solidify: { run_id: 'run_1' },
    }), false);
  });

  it('handles numeric run_ids via string coercion', () => {
    assert.equal(isPendingSolidify({
      last_run: { run_id: 123 },
      last_solidify: { run_id: '123' },
    }), false);
  });
});

describe('readJsonSafe', () => {
  it('returns null for non-existent file', () => {
    assert.equal(readJsonSafe(path.join(tmpDir, 'nonexistent.json')), null);
  });

  it('returns null for empty file', () => {
    const p = path.join(tmpDir, 'empty.json');
    fs.writeFileSync(p, '');
    assert.equal(readJsonSafe(p), null);
  });

  it('returns null for whitespace-only file', () => {
    const p = path.join(tmpDir, 'whitespace.json');
    fs.writeFileSync(p, '   \n  ');
    assert.equal(readJsonSafe(p), null);
  });

  it('returns null for invalid JSON', () => {
    const p = path.join(tmpDir, 'bad.json');
    fs.writeFileSync(p, '{ not valid json }');
    assert.equal(readJsonSafe(p), null);
  });

  it('parses valid JSON', () => {
    const p = path.join(tmpDir, 'good.json');
    fs.writeFileSync(p, JSON.stringify({ key: 'value' }));
    const result = readJsonSafe(p);
    assert.deepEqual(result, { key: 'value' });
  });
});

describe('loop-mode non-fatal error handling', () => {
  // line 298 in index.js: empty catch block swallowing errors during cycle execution
  // This test verifies the error handling contract: errors in the cycle loop are caught
  // and do not propagate, allowing the loop to continue executing subsequent cycles.

  const { execFileSync } = require('child_process');
  const repoRoot = path.resolve(__dirname, '..');

  function loopChildEnv(extra = {}) {
    return {
      ...process.env,
      EVOLVE_LOOP: 'true',
      EVOLVE_BRIDGE: 'false',
      A2A_HUB_URL: '',
      EVOLVER_REPO_ROOT: repoRoot,
      EVOLVER_LOCK_DIR: tmpDir,
      EVOLVER_SETTINGS_DIR: path.join(tmpDir, '.evolver-settings'),
      EVOMAP_PROXY: '0',
      EVOMAP_PROXY_AUTO_INJECT: 'off',
      CLAUDE_SETTINGS_FILE: path.join(tmpDir, '.claude', 'settings.json'),
      EVOLVER_CAFFEINATE: '0',
      EVOLVER_SUICIDE: 'false',
      EVOLVER_CYCLE_TIMEOUT_ENABLED: 'false',
      EVOLVER_CYCLE_TIMEOUT_MS: '2700000',
      EVOLVER_MIN_SLEEP_MS: '1',
      EVOLVER_MAX_SLEEP_MS: '1',
      EVOLVE_PENDING_SLEEP_MS: '1',
      // Force immediate exit after first cycle for test predictability.
      EVOLVER_MAX_CYCLES_PER_PROCESS: '1',
      ...extra,
    };
  }

  it('loop child env disables cycle timeout by default', () => {
    process.env.EVOLVER_CYCLE_TIMEOUT_ENABLED = 'true';
    process.env.EVOLVER_CYCLE_TIMEOUT_MS = '1';
    const env = loopChildEnv();
    assert.equal(env.EVOLVER_CYCLE_TIMEOUT_ENABLED, 'false');
    assert.equal(env.EVOLVER_CYCLE_TIMEOUT_MS, '2700000');
  });

  it('loop-mode continues after evolve.run() throws', () => {
    // When EVOLVE_LOOP=true, the cycle loop catches all errors (line 297's catch(e){})
    // This ensures a throwing evolve.run() does not terminate the daemon.
    // We verify by checking the process exits cleanly rather than crashing.
    let exitCode = null;
    let stdout = '';
    try {
      const out = execFileSync(process.execPath, ['index.js'], {
        cwd: repoRoot,
        encoding: 'utf8',
        timeout: 30000,
        env: loopChildEnv(),
      });
      stdout = out;
    } catch (err) {
      exitCode = err.status;
      stdout = (err.stdout || '') + (err.stderr || '');
    }
    // Loop-mode should exit cleanly with code 0 or 1 (bridge mode exit),
    // not with a thrown error that would give code > 1 or ENOENT
    assert.ok(
      exitCode === null || exitCode === 0 || exitCode === 1,
      'loop-mode should exit cleanly, got code: ' + exitCode + ', stdout: ' + stdout.slice(0, 200)
    );
    assert.ok(
      !stdout.includes('SyntaxError') && !stdout.includes('ReferenceError'),
      'loop-mode should not leak uncaught errors: ' + stdout.slice(0, 200)
    );
  });

  it('should_explore branch does not leak errors to cycle loop', async () => {
    // lines 281-291: should_explore branch wraps tryExplore in try/catch
    // This test verifies explore errors are swallowed and logged verbosely only
    const { execFileSync } = require('child_process');
    const repoRoot = path.resolve(__dirname, '..');
    let stdout = '';
    try {
      stdout = execFileSync(process.execPath, ['index.js'], {
        cwd: repoRoot,
        encoding: 'utf8',
        timeout: 30000,
        env: loopChildEnv({ OMLS_ENABLED: 'true' }),
      });
    } catch (err) {
      stdout = (err.stdout || '') + (err.stderr || '');
    }
    // Should not have unhandled errors from tryExplore
    assert.ok(
      !stdout.includes('TypeError: Cannot') && !stdout.includes('Error: ENOENT'),
      'explore branch should not leak filesystem errors: ' + stdout.slice(0, 300)
    );
  });
});

describe('loop-mode EVOLVE_BRIDGE default (issue #96)', () => {
  // From v1.85.0 the daemon defaults EVOLVE_BRIDGE=true so cycles actually
  // evolve the working tree. The previous default 'false' produced no
  // EvolutionEvents on Aurora over 33 days because every cycle hit
  // rejectPendingRun(reason=loop_bridge_disabled_autoreject_no_rollback).
  // These tests verify the default flip and the safety banner.
  const { execFileSync, spawnSync } = require('child_process');
  const repoRoot = path.resolve(__dirname, '..');

  // Use the test-scoped tmpDir as REPO_ROOT so a leftover `.evolver.lock`
  // in the dev repo (e.g. during a release prep) does not preflight-yield
  // the spawned daemon and short-circuit the test. Init it as a git repo
  // since the daemon refuses to run outside of one.
  function ensureGitRepo(dir) {
    try {
      execFileSync('git', ['init', '-q'], { cwd: dir, stdio: 'ignore' });
      execFileSync('git', ['config', 'user.email', 'test@example.com'], { cwd: dir, stdio: 'ignore' });
      execFileSync('git', ['config', 'user.name', 'test'], { cwd: dir, stdio: 'ignore' });
      execFileSync('git', ['commit', '--allow-empty', '-m', 'init', '-q'], { cwd: dir, stdio: 'ignore' });
    } catch (_) { /* best-effort */ }
  }

  function daemonChildEnv(extraEnv = {}) {
    return {
      ...process.env,
      EVOLVE_LOOP: 'true',
      A2A_HUB_URL: '',
      EVOLVER_REPO_ROOT: tmpDir,
      EVOLVER_CAFFEINATE: '0',
      // Isolate the singleton pid-file in tmpDir so concurrent tests (and
      // a real daemon at the dev repo) do not block this spawn.
      EVOLVER_LOCK_DIR: tmpDir,
      EVOLVER_SETTINGS_DIR: path.join(tmpDir, '.evolver-settings'),
      EVOMAP_PROXY: '0',
      EVOMAP_PROXY_AUTO_INJECT: 'off',
      CLAUDE_SETTINGS_FILE: path.join(tmpDir, '.claude', 'settings.json'),
      EVOLVER_SUICIDE: 'false',
      EVOLVER_CYCLE_TIMEOUT_ENABLED: 'false',
      EVOLVER_CYCLE_TIMEOUT_MS: '2700000',
      EVOLVER_MIN_SLEEP_MS: '1',
      EVOLVER_MAX_SLEEP_MS: '1',
      EVOLVE_PENDING_SLEEP_MS: '1',
      EVOLVER_MAX_CYCLES_PER_PROCESS: '1',
      ...extraEnv,
    };
  }

  function runDaemonOnce(extraEnv = {}) {
    ensureGitRepo(tmpDir);
    const result = spawnSync(process.execPath, [path.join(repoRoot, 'index.js'), '--loop'], {
      cwd: tmpDir,
      encoding: 'utf8',
      timeout: 3000,
      env: daemonChildEnv(extraEnv),
    });
    return (result.stdout || '') + (result.stderr || '');
  }

  it('--loop with EVOLVE_BRIDGE unset defaults to bridge=true', () => {
    const combined = runDaemonOnce({ EVOLVE_BRIDGE: '' });
    assert.ok(
      /bridge=true/.test(combined),
      'combined output should announce bridge=true: ' + combined.slice(0, 500)
    );
  });

  it('--loop with EVOLVE_BRIDGE=true keeps bridge=true', () => {
    const combined = runDaemonOnce({ EVOLVE_BRIDGE: 'true' });
    assert.ok(
      /bridge=true/.test(combined),
      'explicit true should be honored: ' + combined.slice(0, 500)
    );
  });

  it('--loop with EVOLVE_BRIDGE=false still respected (opt-out)', () => {
    const combined = runDaemonOnce({ EVOLVE_BRIDGE: 'false' });
    assert.ok(
      /bridge=false/.test(combined),
      'explicit false must be honored as opt-out: ' + combined.slice(0, 500)
    );
    assert.ok(
      /observe-only/.test(combined),
      'opt-out banner should mention observe-only: ' + combined.slice(0, 500)
    );
  });

  it('bridge=true banner mentions stash recovery', () => {
    // The safety banner is the one mitigation that compensates for the
    // riskier default. If the message is missing or rewritten, users lose
    // the recovery breadcrumb -- they must see "git stash" in the warning.
    const combined = runDaemonOnce({ EVOLVE_BRIDGE: '' });
    assert.ok(
      /git stash/.test(combined),
      'safety banner must reference git stash recovery: ' + combined.slice(0, 800)
    );
  });

  it('test loop child env disables suicide respawn, cycle timeout, and isolates proxy settings', () => {
    process.env.EVOLVER_CYCLE_TIMEOUT_ENABLED = 'true';
    process.env.EVOLVER_CYCLE_TIMEOUT_MS = '1';
    const env = daemonChildEnv({ EVOLVE_BRIDGE: '' });
    assert.equal(env.EVOLVER_CYCLE_TIMEOUT_ENABLED, 'false');
    assert.equal(env.EVOLVER_CYCLE_TIMEOUT_MS, '2700000');

    const combined = runDaemonOnce({ EVOLVE_BRIDGE: '' });
    assert.ok(!/Restarting self/.test(combined),
      'loop-mode child tests must not spawn detached replacement processes');
    assert.ok(!/Cycle hard-timeout/.test(combined),
      'loop-mode child tests must not inherit cycle timeout from parent env');
    assert.ok(!combined.includes(path.join(os.homedir(), '.evolver')),
      'loop-mode child tests must not use the operator settings file');
  });
});

describe('cycle timeout suicide control', () => {
  it('non-fatal timeout wait does not settle until the timed-out run resolves', async () => {
    let release;
    let waitSettled = false;
    const pendingRun = new Promise((resolve) => {
      release = resolve;
    });

    const waitPromise = waitForTimedOutEvolvePromise(pendingRun, () => {}).then((result) => {
      waitSettled = true;
      return result;
    });

    await new Promise((resolve) => setImmediate(resolve));
    assert.equal(waitSettled, false, 'wait must remain pending while evolve.run() is pending');

    release();
    assert.deepEqual(await waitPromise, { status: 'resolved' });
    assert.equal(waitSettled, true);
  });

  it('non-fatal timeout wait consumes and logs late rejection from timed-out run', async () => {
    const lateError = new Error('late run failure');
    const logs = [];
    const result = await waitForTimedOutEvolvePromise(Promise.reject(lateError), (message) => {
      logs.push(message);
    });

    assert.deepEqual(result, { status: 'rejected' });
    assert.equal(logs.length, 1);
    assert.match(logs[0], /Timed-out evolve\.run\(\) eventually rejected: late run failure/);
  });

  it('does not request replacement respawn when EVOLVER_SUICIDE=false', () => {
    const progressPath = path.join(tmpDir, 'cycle_progress.json');
    const spawnCalls = [];
    const logs = [];
    const originalError = console.error;
    const originalWarn = console.warn;
    console.error = (...args) => { logs.push(args.join(' ')); };
    console.warn = (...args) => { logs.push(args.join(' ')); };
    try {
      const result = handleCycleTimeout({
        error: new CycleTimeoutError(1, 'evolve.run', 7),
        cycleProgressPath: progressPath,
        progressFields: {
          pid: 123,
          outer_cycle: 7,
          inner_cycle: 7,
          started_at: 456,
        },
        suicideEnabled: false,
        args: ['--loop'],
        logPath: path.join(tmpDir, 'evolver.log'),
        spawnReplacementFn: (opts) => { spawnCalls.push(opts); },
      });

      assert.deepEqual(result, { action: 'continue' });
      assert.equal(spawnCalls.length, 0);
      const progress = JSON.parse(fs.readFileSync(progressPath, 'utf8'));
      assert.equal(progress.phase, 'cycle_timeout_nonfatal');
      const combined = logs.join('\n');
      assert.match(combined, /Cycle hard-timeout exceeded/);
      assert.doesNotMatch(combined, /cycle_timeout_respawn|Spawn-replacement|Restarting self/);
    } finally {
      console.error = originalError;
      console.warn = originalWarn;
    }
  });

  it('requests replacement respawn when suicide is enabled', () => {
    const progressPath = path.join(tmpDir, 'cycle_progress.json');
    const spawnCalls = [];
    const logs = [];
    const originalError = console.error;
    console.error = (...args) => { logs.push(args.join(' ')); };
    try {
      const result = handleCycleTimeout({
        error: new CycleTimeoutError(1, 'evolve.run', 8),
        cycleProgressPath: progressPath,
        progressFields: {
          pid: 123,
          outer_cycle: 8,
          inner_cycle: 8,
          started_at: 456,
        },
        suicideEnabled: true,
        args: ['--loop'],
        logPath: path.join(tmpDir, 'evolver.log'),
        spawnReplacementFn: (opts) => { spawnCalls.push(opts); },
      });

      assert.deepEqual(result, { action: 'respawn' });
      assert.deepEqual(spawnCalls, [{
        reason: 'cycle_hard_timeout',
        args: ['--loop'],
        logPath: path.join(tmpDir, 'evolver.log'),
      }]);
      const progress = JSON.parse(fs.readFileSync(progressPath, 'utf8'));
      assert.equal(progress.phase, 'cycle_timeout_respawn');
      assert.match(logs.join('\n'), /Cycle hard-timeout exceeded/);
    } finally {
      console.error = originalError;
    }
  });
});

describe('bare invocation routing -- black-box', () => {
  const { execFileSync } = require('child_process');
  const repoRoot = path.resolve(__dirname, '..');

  it('node index.js (no args) starts evolution, not help', () => {
    let out;
    try {
      out = execFileSync(process.execPath, ['index.js'], {
        cwd: repoRoot,
        encoding: 'utf8',
        timeout: 60000,
        env: {
          ...process.env,
          EVOLVE_BRIDGE: 'false',
          A2A_HUB_URL: '',
          EVOLVER_REPO_ROOT: repoRoot,
          EVOMAP_PROXY: '0',
          EVOMAP_PROXY_AUTO_INJECT: 'off',
          EVOLVER_SETTINGS_DIR: path.join(tmpDir, '.evolver-settings'),
          CLAUDE_SETTINGS_FILE: path.join(tmpDir, '.claude', 'settings.json'),
          EVOLVER_SUICIDE: 'false',
          EVOLVER_CYCLE_TIMEOUT_ENABLED: 'false',
          EVOLVER_CYCLE_TIMEOUT_MS: '2700000',
        },
      });
    } catch (err) {
      // evolve.run() will block/timeout -- that is expected for a bare invocation.
      // Extract whatever stdout was captured before the timeout.
      out = (err.stdout || '') + '';
    }
    assert.ok(out.includes('Starting evolver') || out.includes('GEP'),
      'bare invocation should start evolution, not show usage. Got: ' + out.slice(0, 200));
    assert.ok(!out.includes('Usage:'), 'should not show usage for bare invocation');
  });

  it('unknown command shows usage help', () => {
    const out = execFileSync(process.execPath, ['index.js', 'nonexistent-cmd'], {
      cwd: repoRoot,
      encoding: 'utf8',
      timeout: 60000,
      env: {
        ...process.env,
        A2A_HUB_URL: '',
        EVOMAP_PROXY: '0',
        EVOMAP_PROXY_AUTO_INJECT: 'off',
        EVOLVER_SETTINGS_DIR: path.join(tmpDir, '.evolver-settings'),
        CLAUDE_SETTINGS_FILE: path.join(tmpDir, '.claude', 'settings.json'),
        EVOLVER_CYCLE_TIMEOUT_ENABLED: 'false',
        EVOLVER_CYCLE_TIMEOUT_MS: '2700000',
      },
    });
    assert.ok(out.includes('Usage:'), 'unknown command should show usage');
  });
});
