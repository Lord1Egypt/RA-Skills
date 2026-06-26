'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const guards = require('../src/evolve/guards');

// ---------------------------------------------------------------------------
// detectCpuCount
// ---------------------------------------------------------------------------
describe('detectCpuCount', () => {
  it('returns a positive integer', () => {
    const count = guards.detectCpuCount();
    assert.ok(Number.isInteger(count) && count >= 1);
  });
});

// ---------------------------------------------------------------------------
// getSystemLoad
// ---------------------------------------------------------------------------
describe('getSystemLoad', () => {
  it('returns load1m, load5m, load15m as finite numbers', () => {
    const load = guards.getSystemLoad();
    assert.ok(Number.isFinite(load.load1m));
    assert.ok(Number.isFinite(load.load5m));
    assert.ok(Number.isFinite(load.load15m));
  });

  it('clamps values to at most 2x CPU count', () => {
    const load = guards.getSystemLoad();
    const cap = guards.detectCpuCount() * 2;
    assert.ok(load.load1m <= cap);
    assert.ok(load.load5m <= cap);
    assert.ok(load.load15m <= cap);
  });
});

// ---------------------------------------------------------------------------
// getDefaultLoadMax
// ---------------------------------------------------------------------------
describe('getDefaultLoadMax', () => {
  it('returns a positive finite number', () => {
    const max = guards.getDefaultLoadMax();
    assert.ok(Number.isFinite(max) && max > 0);
  });

  it('returns 0.9 for single-core equivalent', () => {
    const cpuCount = guards.detectCpuCount();
    const max = guards.getDefaultLoadMax();
    if (cpuCount <= 1) {
      assert.equal(max, 0.9);
    } else {
      assert.ok(max > 0.9);
    }
  });
});

// ---------------------------------------------------------------------------
// determineBridgeEnabled
// ---------------------------------------------------------------------------
describe('determineBridgeEnabled', () => {
  it('returns false when EVOLVE_BRIDGE=false', () => {
    const orig = process.env.EVOLVE_BRIDGE;
    process.env.EVOLVE_BRIDGE = 'false';
    assert.equal(guards.determineBridgeEnabled(), false);
    if (orig === undefined) delete process.env.EVOLVE_BRIDGE;
    else process.env.EVOLVE_BRIDGE = orig;
  });

  it('returns true when EVOLVE_BRIDGE=true', () => {
    const orig = process.env.EVOLVE_BRIDGE;
    process.env.EVOLVE_BRIDGE = 'true';
    assert.equal(guards.determineBridgeEnabled(), true);
    if (orig === undefined) delete process.env.EVOLVE_BRIDGE;
    else process.env.EVOLVE_BRIDGE = orig;
  });

  it('falls back to OPENCLAW_WORKSPACE presence', () => {
    const origBridge = process.env.EVOLVE_BRIDGE;
    const origOC = process.env.OPENCLAW_WORKSPACE;
    delete process.env.EVOLVE_BRIDGE;
    process.env.OPENCLAW_WORKSPACE = '/some/workspace';
    assert.equal(guards.determineBridgeEnabled(), true);
    delete process.env.OPENCLAW_WORKSPACE;
    assert.equal(guards.determineBridgeEnabled(), false);
    if (origBridge !== undefined) process.env.EVOLVE_BRIDGE = origBridge;
    if (origOC !== undefined) process.env.OPENCLAW_WORKSPACE = origOC;
  });
});

// ---------------------------------------------------------------------------
// dormant hypothesis: write / read / clear
// ---------------------------------------------------------------------------
describe('dormant hypothesis', () => {
  it('round-trips payload through write + read', () => {
    const payload = { backoff_reason: 'test', signals: ['foo', 'bar'] };
    guards.writeDormantHypothesis(payload);
    const result = guards.readDormantHypothesis();
    assert.ok(result !== null);
    assert.equal(result.backoff_reason, 'test');
    assert.deepEqual(result.signals, ['foo', 'bar']);
  });

  it('clear removes the hypothesis so read returns null', () => {
    guards.writeDormantHypothesis({ backoff_reason: 'to_be_cleared' });
    guards.clearDormantHypothesis();
    assert.equal(guards.readDormantHypothesis(), null);
  });
});

// ---------------------------------------------------------------------------
// checkRepairLoopCircuitBreaker
// ---------------------------------------------------------------------------
describe('checkRepairLoopCircuitBreaker', () => {
  it('runs without throwing even when asset store is empty', () => {
    const origForce = process.env.FORCE_INNOVATION;
    delete process.env.FORCE_INNOVATION;
    assert.doesNotThrow(() => guards.checkRepairLoopCircuitBreaker());
    if (origForce !== undefined) process.env.FORCE_INNOVATION = origForce;
    else delete process.env.FORCE_INNOVATION;
  });
});

// ---------------------------------------------------------------------------
// runPreflightChecks
// ---------------------------------------------------------------------------
describe('runPreflightChecks', () => {
  it('returns { abort: false } under normal conditions', async () => {
    // Force load max high so test machine never triggers load backoff
    const origLoad = process.env.EVOLVE_LOAD_MAX;
    const origQueue = process.env.EVOLVE_AGENT_QUEUE_MAX;
    const origReleaseWindow = process.env.EVOLVE_RELEASE_WINDOW_MS;
    process.env.EVOLVE_LOAD_MAX = '9999';
    process.env.EVOLVE_AGENT_QUEUE_MAX = '9999';
    // Disable the release-window guard. runPreflightChecks yields the cycle
    // when the HEAD commit subject matches /^chore\(release\)/ within
    // EVOLVE_RELEASE_WINDOW_MS (default 5min). On the post-release-bump CI run
    // the checked-out HEAD IS that commit (e.g. "chore(release): prepare
    // v1.89.3"), so without this the test reads its own repo's release commit
    // and returns abort:true. Setting the window to 0 disables the guard
    // (windowMs === 0 short-circuit), same neutralization style as LOAD_MAX
    // above. This is why the test passed on ordinary commits but failed the
    // required Ubuntu job on every release commit.
    process.env.EVOLVE_RELEASE_WINDOW_MS = '0';
    // PR #46 added a .evolver.lock cooperative-yield gate. If the developer
    // running tests has the lock present locally, this test would falsely
    // report abort=true. Ensure no lock is present for this assertion.
    const fs = require('fs');
    const path = require('path');
    const lockPath = path.join(process.cwd(), '.evolver.lock');
    let restoreLock = false;
    try {
      if (fs.existsSync(lockPath)) {
        fs.unlinkSync(lockPath);
        restoreLock = true;
      }
      const result = await guards.runPreflightChecks(false, false);
      assert.equal(result.abort, false);
    } finally {
      if (restoreLock) fs.writeFileSync(lockPath, '');
      if (origLoad === undefined) delete process.env.EVOLVE_LOAD_MAX;
      else process.env.EVOLVE_LOAD_MAX = origLoad;
      if (origQueue === undefined) delete process.env.EVOLVE_AGENT_QUEUE_MAX;
      else process.env.EVOLVE_AGENT_QUEUE_MAX = origQueue;
      if (origReleaseWindow === undefined) delete process.env.EVOLVE_RELEASE_WINDOW_MS;
      else process.env.EVOLVE_RELEASE_WINDOW_MS = origReleaseWindow;
    }
  });

  it('returns { abort: true } when system load exceeds EVOLVE_LOAD_MAX', async () => {
    const origLoad = process.env.EVOLVE_LOAD_MAX;
    const origBackoff = process.env.EVOLVE_AGENT_QUEUE_BACKOFF_MS;
    process.env.EVOLVE_LOAD_MAX = '-1';      // always exceeded (Windows loadavg returns 0)
    process.env.EVOLVE_AGENT_QUEUE_BACKOFF_MS = '0';  // skip sleep
    const result = await guards.runPreflightChecks(false, false);
    assert.equal(result.abort, true);
    if (origLoad === undefined) delete process.env.EVOLVE_LOAD_MAX;
    else process.env.EVOLVE_LOAD_MAX = origLoad;
    if (origBackoff === undefined) delete process.env.EVOLVE_AGENT_QUEUE_BACKOFF_MS;
    else process.env.EVOLVE_AGENT_QUEUE_BACKOFF_MS = origBackoff;
  });
});
