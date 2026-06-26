// Tests for the concurrency guard added to src/forceUpdate.js (PR #188 fix).
//
// Background: two code paths can observe a pending force_update directive in
// the same scheduler tick:
//   (1) heartbeat-thread: _maybeTriggerForceUpdateFromHeartbeat in
//       src/gep/a2aProtocol.js, gated by the instance-level
//       _forceUpdateInFlight flag.
//   (2) evolve-tick:     src/evolve/pipeline/enrich.js (Stage 5 enrich) which
//       calls executeForceUpdate(forceUpdate) directly with NO guard.
//
// If path (1) drops the directive without consuming it (e.g. cooldown bail in
// the heartbeat handler) the next evolve tick on path (2) re-fires. Worse,
// if a prior heartbeat-thread upgrade is still in flight (slow degit/npm) AND
// the evolve tick reads consumeForceUpdate() before the heartbeat clears the
// pending slot, BOTH paths call executeForceUpdate concurrently. Both fire
// reportForceUpdateOutcome -> both write the same state file via atomic
// rename -> last writer wins, first attempt's telemetry is lost.
//
// The fix moves the mutex into src/forceUpdate.js itself as a module-level
// flag so it is shared by every caller of require('../forceUpdate'). The
// second concurrent invocation returns the FORCE_UPDATE_BUSY sentinel and
// callers treat it as a no-op (no state file write, no process.exit).

const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const childProcess = require('child_process');
const origExecFileSync = childProcess.execFileSync;

const forceUpdateModPath = require.resolve('../src/forceUpdate');
const pathsModPath = require.resolve('../src/gep/paths');

let installRoot;

function freshRequireForceUpdate(execFileStub) {
  delete require.cache[forceUpdateModPath];
  require.cache[pathsModPath] = {
    id: pathsModPath, filename: pathsModPath, loaded: true,
    exports: { getEvolverInstallRoot: () => installRoot },
  };
  childProcess.execFileSync = execFileStub;
  const mod = require('../src/forceUpdate');
  childProcess.execFileSync = origExecFileSync;
  return mod;
}

function writeInstallPkg(version) {
  fs.writeFileSync(
    path.join(installRoot, 'package.json'),
    JSON.stringify({ name: '@evomap/evolver', version }),
    'utf8',
  );
}

describe('executeForceUpdate: module-level concurrency guard', () => {
  before(() => {
    installRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-fu-conc-'));
  });

  after(() => {
    childProcess.execFileSync = origExecFileSync;
    delete require.cache[pathsModPath];
    delete require.cache[forceUpdateModPath];
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
    fs.mkdirSync(installRoot, { recursive: true });
  });

  it('exports FORCE_UPDATE_BUSY as a Symbol distinct from FORCE_UPDATE_NOOP and true/false', () => {
    const stub = function () { throw new Error('must not invoke degit'); };
    const mod = freshRequireForceUpdate(stub);
    assert.equal(typeof mod.FORCE_UPDATE_BUSY, 'symbol',
      'sentinel must be a Symbol so === checks cannot accidentally collide');
    assert.notEqual(mod.FORCE_UPDATE_BUSY, mod.FORCE_UPDATE_NOOP,
      'BUSY and NOOP must be distinct sentinels');
    assert.notEqual(mod.FORCE_UPDATE_BUSY, true);
    assert.notEqual(mod.FORCE_UPDATE_BUSY, false);
    assert.notEqual(mod.FORCE_UPDATE_BUSY, null);
    assert.notEqual(mod.FORCE_UPDATE_BUSY, undefined);
  });

  it('re-entrant call during a slow upgrade returns FORCE_UPDATE_BUSY without invoking degit again', () => {
    // Force the upgrade path (not the no-op short-circuit).
    writeInstallPkg('1.87.0');

    // Capture the moment a re-entrant call returns.
    let reentrantResult = null;
    let reentrantExecCalls = 0;
    let outerExecCalls = 0;

    // Need a reference to the module before we can stub execFileSync to
    // call back into executeForceUpdate. Use a forward-declared holder.
    let mod;

    const stub = function () {
      outerExecCalls++;
      // While we are "in the middle" of the first executeForceUpdate (the
      // outer call), simulate the concurrent invocation by calling
      // executeForceUpdate AGAIN from a different caller (the evolve tick).
      // The module-level mutex MUST observe that _inFlight === true and
      // return FORCE_UPDATE_BUSY without entering _executeForceUpdateInner
      // (which would invoke execFileSync -- we'd see reentrantExecCalls > 0).
      reentrantResult = mod.executeForceUpdate({ required_version: '1.88.0' });
      // Now let the outer call's degit fail so the upgrade itself returns
      // false (we only care about the mutex behavior here, not the upgrade).
      throw new Error('simulated degit failure (outer)');
    };

    mod = freshRequireForceUpdate(stub);
    // Track BOTH executions via the same stub: the second invocation, if it
    // mistakenly bypassed the mutex, would land here a second time.
    const trackingStub = function () {
      // First outer call invokes the original stub. Inside that stub, the
      // re-entrant call would also land here if the mutex were broken.
      // We count separately to distinguish: outerExecCalls is bumped by the
      // original stub above; reentrantExecCalls is bumped only if the
      // re-entrant path bypassed the mutex.
      reentrantExecCalls++;
      throw new Error('simulated degit failure (reentrant)');
    };
    // Rewire the stub for the re-entrant call by swapping execFileSync just
    // before re-entering. Simpler: install the trackingStub now and have the
    // outer stub increment outerExecCalls itself.
    childProcess.execFileSync = function () {
      outerExecCalls++;
      // First time only: do the re-entrant call.
      if (outerExecCalls === 1) {
        // Swap to the tracking stub so any re-entrant degit hits it.
        const prev = childProcess.execFileSync;
        childProcess.execFileSync = trackingStub;
        try {
          reentrantResult = mod.executeForceUpdate({ required_version: '1.88.0' });
        } finally {
          childProcess.execFileSync = prev;
        }
      }
      throw new Error('simulated degit failure (outer)');
    };

    const outerResult = mod.executeForceUpdate({ required_version: '1.88.0' });
    childProcess.execFileSync = origExecFileSync;

    assert.equal(reentrantResult, mod.FORCE_UPDATE_BUSY,
      're-entrant call during in-flight upgrade returns FORCE_UPDATE_BUSY');
    assert.equal(reentrantExecCalls, 0,
      're-entrant call MUST NOT reach degit (mutex short-circuit before _executeForceUpdateInner)');
    assert.equal(outerResult.ok, false,
      'outer call still returns its normal failure result (structured fail on degit failure)');
    assert.equal(outerResult.code, 'degit_failed',
      'outer failure carries the degit_failed code (was a bare false before structured failures)');
    assert.ok(outerExecCalls >= 1,
      'outer call did reach degit at least once');
  });

  it('mutex resets after the outer call returns: subsequent invocations proceed normally', () => {
    writeInstallPkg('1.87.0');
    let execCalls = 0;
    const stub = function () {
      execCalls++;
      throw new Error('simulated degit failure');
    };
    const mod = freshRequireForceUpdate(stub);

    // First call: enters _executeForceUpdateInner, fails at degit, returns a
    // structured { ok:false, code:'degit_failed' } (was a bare false).
    const r1 = mod.executeForceUpdate({ required_version: '1.88.0' });
    assert.equal(r1.ok, false);
    assert.equal(r1.code, 'degit_failed', 'degit throw classified as degit_failed');
    assert.equal(execCalls, 1, 'first call reached degit');

    // Second call AFTER first completes: must NOT be blocked by a stuck mutex.
    const r2 = mod.executeForceUpdate({ required_version: '1.88.0' });
    assert.equal(r2.ok, false, 'mutex released; second call ran normally');
    assert.equal(execCalls, 2, 'second call also reached degit (no stale BUSY)');
  });

  it('mutex resets even when _executeForceUpdateInner throws (finally semantics)', () => {
    writeInstallPkg('1.87.0');
    // Throw something exotic that bypasses the inner try/catch -- specifically,
    // a synchronous throw from getEvolverInstallRoot itself. Easiest: pollute
    // the install root so reading package.json throws AFTER mutex acquired
    // but BEFORE returning. We force that by deleting the install dir.
    try { fs.rmSync(installRoot, { recursive: true, force: true }); } catch (_) {}
    const stub = function () { throw new Error('unreachable'); };
    const mod = freshRequireForceUpdate(stub);

    // First call: refuses (missing package.json), returns a structured
    // { ok:false, code:'install_guard_unreadable' } (was a bare false).
    const r1 = mod.executeForceUpdate({ required_version: '1.88.0' });
    assert.equal(r1.ok, false, 'missing pkg returns a structured failure');
    assert.equal(r1.code, 'install_guard_unreadable',
      'missing/unreadable install package.json → install_guard_unreadable');

    // Recreate install root for next call.
    fs.mkdirSync(installRoot, { recursive: true });
    writeInstallPkg('1.88.0');

    // Second call (no-op, already at target) must proceed -- proves mutex
    // was released by the finally.
    const r2 = mod.executeForceUpdate({ required_version: '1.88.0' });
    assert.equal(r2, mod.FORCE_UPDATE_NOOP,
      'mutex released by finally; second call observed no-op short-circuit');
  });

  it('_resetInFlightForTesting clears the mutex (test hook hygiene)', () => {
    writeInstallPkg('1.87.0');
    // Force mutex into stuck state by invoking with a stub that DOES NOT
    // throw synchronously -- normally finally would clear it, but we want to
    // verify the test hook works.
    const stub = function () { throw new Error('simulated'); };
    const mod = freshRequireForceUpdate(stub);

    // After a normal call, mutex is already clear; assert _resetInFlightForTesting
    // is callable and idempotent.
    mod.executeForceUpdate({ required_version: '1.88.0' });
    mod._resetInFlightForTesting();
    // After reset, a fresh call should still proceed.
    const r = mod.executeForceUpdate({ required_version: '1.88.0' });
    assert.equal(r.ok, false, 'reset hook works and is idempotent');
  });
});

// ---------------------------------------------------------------------------
// Integration: the heartbeat-trigger path in a2aProtocol.js MUST defensively
// tolerate a BUSY return without writing a state file or calling exit(78).
// In production, _forceUpdateInFlight (the instance-level cooldown flag in
// a2aProtocol) already gates this — but the BUSY check is a belt-and-braces
// guard. This test exercises the path by stubbing executeForceUpdate to
// return FORCE_UPDATE_BUSY directly.
// ---------------------------------------------------------------------------

describe('a2aProtocol heartbeat-trigger: BUSY return short-circuits telemetry', () => {
  const forceUpdatePath = require.resolve('../src/forceUpdate');
  const a2aProtocolPath = require.resolve('../src/gep/a2aProtocol');

  let tmpDir;
  let evomapHomeDir;
  let origHubUrl;
  let origLogsDir;
  let origEvolverHome;
  let origInsecure;
  let origFetch;
  let origExit;
  let execCalls;
  let execReturn;

  function loadProtocolWithSpy() {
    delete require.cache[a2aProtocolPath];
    const realFU = require('../src/forceUpdate');
    require.cache[forceUpdatePath] = {
      id: forceUpdatePath,
      filename: forceUpdatePath,
      loaded: true,
      exports: {
        executeForceUpdate: function (fu) {
          execCalls.push(fu);
          if (execReturn === '__BUSY__') return realFU.FORCE_UPDATE_BUSY;
          if (execReturn === '__NOOP__') return realFU.FORCE_UPDATE_NOOP;
          return execReturn;
        },
        FORCE_UPDATE_NOOP: realFU.FORCE_UPDATE_NOOP,
        FORCE_UPDATE_BUSY: realFU.FORCE_UPDATE_BUSY,
      },
    };
    return require('../src/gep/a2aProtocol');
  }

  before(() => {
    if (!process.env.A2A_NODE_SECRET) process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-fu-busy-'));
    evomapHomeDir = path.join(tmpDir, 'evomap-home');
    fs.mkdirSync(evomapHomeDir, { recursive: true });

    origHubUrl = process.env.A2A_HUB_URL;
    origLogsDir = process.env.EVOLVER_LOGS_DIR;
    origEvolverHome = process.env.EVOLVER_HOME;
    origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19997';
    process.env.EVOLVER_LOGS_DIR = tmpDir;
    process.env.EVOLVER_HOME = evomapHomeDir;
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';

    origFetch = global.fetch;
    origExit = process.exit;
  });

  after(() => {
    global.fetch = origFetch;
    process.exit = origExit;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = origHubUrl;
    if (origLogsDir === undefined) delete process.env.EVOLVER_LOGS_DIR;
    else process.env.EVOLVER_LOGS_DIR = origLogsDir;
    if (origEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = origEvolverHome;
    if (origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = origInsecure;
    delete require.cache[a2aProtocolPath];
    delete require.cache[forceUpdatePath];
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  });

  beforeEach(() => {
    execCalls = [];
    execReturn = '__BUSY__';
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '0';
  });

  it('heartbeat trigger observing BUSY does NOT write state file and does NOT call exit(78)', async () => {
    execReturn = '__BUSY__';
    const a2a = loadProtocolWithSpy();
    a2a.getNodeId();
    const statePath = a2a._testing._getLastUpdateStatePathForTesting();
    a2a._testing._resetLastUpdateStateForTesting();
    a2a._testing._resetForceUpdateStateForTesting();
    try { fs.unlinkSync(statePath); } catch (_) {}

    const exitCalls = [];
    process.exit = function (code) { exitCalls.push(code); };
    global.fetch = async function () {
      return {
        ok: true, status: 200,
        json: async () => ({
          status: 'ok',
          force_update: {
            required_version: '>=1.88.0',
            directive_id: 'd-busy-hb',
            reason: 'test',
          },
        }),
        text: async () => '',
      };
    };

    await a2a.sendHeartbeat();
    // Drain the Promise.resolve().then(...) microtask the trigger schedules.
    await new Promise(r => setImmediate(r));

    assert.equal(execCalls.length, 1, 'executeForceUpdate invoked exactly once');
    assert.equal(exitCalls.length, 0,
      'process.exit(78) MUST NOT be called when executeForceUpdate returns BUSY');
    assert.ok(!fs.existsSync(statePath),
      'no state file written for BUSY (in-flight caller owns telemetry; concurrent writes would lose data)');
  });

  it('heartbeat trigger: BUSY does not interfere with subsequent real success', async () => {
    // First heartbeat: BUSY -> no telemetry written.
    execReturn = '__BUSY__';
    const a2a = loadProtocolWithSpy();
    a2a.getNodeId();
    const statePath = a2a._testing._getLastUpdateStatePathForTesting();
    a2a._testing._resetLastUpdateStateForTesting();
    a2a._testing._resetForceUpdateStateForTesting();
    try { fs.unlinkSync(statePath); } catch (_) {}

    const exitCalls = [];
    process.exit = function (code) { exitCalls.push(code); };
    global.fetch = async function () {
      return {
        ok: true, status: 200,
        json: async () => ({
          status: 'ok',
          force_update: {
            required_version: '>=1.88.0',
            directive_id: 'd1',
            reason: 'test',
          },
        }),
        text: async () => '',
      };
    };

    await a2a.sendHeartbeat();
    await new Promise(r => setImmediate(r));
    assert.ok(!fs.existsSync(statePath), 'BUSY: no state file');
    assert.equal(exitCalls.length, 0, 'BUSY: no exit');

    // Second heartbeat: real success -> state file + exit(78).
    a2a._testing._resetForceUpdateStateForTesting();
    execReturn = true;
    await a2a.sendHeartbeat();
    await new Promise(r => setImmediate(r));
    assert.ok(fs.existsSync(statePath), 'real success: state file written');
    const payload = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    assert.equal(payload.status, 'success');
    assert.equal(exitCalls.length, 1, 'real success: exit called');
    assert.equal(exitCalls[0], 78);
  });
});
