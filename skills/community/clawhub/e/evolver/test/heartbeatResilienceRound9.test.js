'use strict';

// Round-9 regression tests. Each test below FAILS against the pre-round-9
// code and PASSES after it -- the contract the round-8 maintainer note
// (and the round-9 review) demanded for any behavior change. They cover:
//
//   1. 401 vs 403 split: a benign 401 (hub has no secret for us yet) must
//      NOT arm the escalating reauth backoff; it schedules a short retry.
//   2. Secret divergence: node_secret_invalid / invalid_secret clears the
//      diverged local secret instead of being treated as a benign 401.
//   3. Reauth escape hatch: a node deep in reauth backoff (>=2 failures)
//      on a machine that never sleeps can still drive ONE re-hello probe
//      per probe interval and recover -- without a restart or a wall-clock
//      jump.
//   4. Probe throttle: within the probe interval, no re-hello is sent
//      (the 60/h hub protection the backoff exists for is preserved).
//   5. Tick-generation guard: an orphaned in-flight tick whose continuation
//      resolves after a watchdog/wake superseded it must NOT clear the gate
//      the new tick owns nor double-schedule.

const { test, describe, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

// Unconditionally pin the test secret inside test scope (a host-exported
// A2A_NODE_SECRET would otherwise win and make assertions host-dependent
// the moment global.fetch stops being stubbed). Save the original and
// restore it after the suite so we do not mutate ambient env for siblings.
const _origA2ASecret = process.env.A2A_NODE_SECRET;
process.env.A2A_NODE_SECRET = 'a'.repeat(64);
after(() => {
  if (_origA2ASecret === undefined) delete process.env.A2A_NODE_SECRET;
  else process.env.A2A_NODE_SECRET = _origA2ASecret;
});

const a2a = require('../src/gep/a2aProtocol');
const { sendHeartbeat } = a2a;
const {
  _resetHeartbeatStateForTesting,
  _setHeartbeatStateForTesting,
  _getHeartbeatInternalsForTesting,
  _driveHeartbeatTickForTesting,
  _bumpTickGenerationForTesting,
  _resetHubNodeSecretStateForTesting,
} = a2a._testing;

function nextTick() { return new Promise((r) => setImmediate(r)); }
async function settle() {
  for (let i = 0; i < 6; i++) await nextTick();
}

function res(status, body) {
  return {
    ok: status >= 200 && status < 300,
    status: status,
    json: async () => body || {},
    text: async () => JSON.stringify(body || {}),
  };
}

function installTempEvolverHome() {
  const previous = process.env.EVOLVER_HOME;
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-round9-'));
  process.env.EVOLVER_HOME = path.join(root, '.evomap');
  fs.mkdirSync(process.env.EVOLVER_HOME, { recursive: true });
  return function restore() {
    if (previous === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = previous;
    fs.rmSync(root, { recursive: true, force: true });
  };
}

describe('round-9: reauth 401-vs-403 split + shorter backoff', () => {
  let origFetch, origHubUrl, origAllow, restoreEvolverHome;
  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    _resetHubNodeSecretStateForTesting();
    origFetch = global.fetch;
    origHubUrl = process.env.A2A_HUB_URL;
    origAllow = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    restoreEvolverHome = installTempEvolverHome();
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    global.fetch = origFetch;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL; else process.env.A2A_HUB_URL = origHubUrl;
    if (origAllow === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE; else process.env.EVOMAP_HUB_ALLOW_INSECURE = origAllow;
    if (restoreEvolverHome) restoreEvolverHome();
    restoreEvolverHome = null;
    _resetHubNodeSecretStateForTesting();
    _resetHeartbeatStateForTesting();
  });

  test('benign 401 (node_secret_not_set) with a failed re-hello does NOT arm the reauth backoff', async () => {
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) return res(500, { ok: false, error: 'hub_down' });
      return res(401, { error: 'node_secret_not_set' });
    };
    _setHeartbeatStateForTesting({ running: true, intervalMs: 60_000 });
    await sendHeartbeat();
    await settle();
    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.reauthBackoffUntil, 0,
      'a benign 401 must NOT arm the 2min..4h reauth backoff (pre-round-9 it armed 30min)');
    assert.equal(s.consecutiveReauthFailures, 0,
      'a benign 401 must NOT bump the reauth failure counter');
    assert.ok(s.pendingRescheduleDelayMs >= 80_000 && s.pendingRescheduleDelayMs <= 100_000,
      'a benign 401 schedules a short (~90s) retry that stays under hub rate limits; got ' + s.pendingRescheduleDelayMs);
  });

  test('genuine 403 (node_secret_invalid) with a failed re-hello clears the diverged secret', async () => {
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) return res(500, { ok: false, error: 'hub_down' });
      return res(403, { error: 'node_secret_invalid' });
    };
    _setHeartbeatStateForTesting({ running: true, intervalMs: 60_000 });
    const result = await sendHeartbeat();
    await settle();
    const s = _getHeartbeatInternalsForTesting();
    assert.equal(result.ok, false);
    assert.equal(result.error, 'secret_diverged_cleared');
    assert.equal(s.consecutiveReauthFailures, 0, 'secret divergence clear must not arm the reauth counter');
    assert.equal(s.reauthBackoffUntil, 0, 'secret divergence clear must not arm reauth backoff');
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed')), true);
  });
});

describe('round-9: non-sleep reauth escape hatch', () => {
  let origFetch, origHubUrl, origAllow, restoreEvolverHome;
  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    _resetHubNodeSecretStateForTesting();
    origFetch = global.fetch;
    origHubUrl = process.env.A2A_HUB_URL;
    origAllow = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    restoreEvolverHome = installTempEvolverHome();
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    global.fetch = origFetch;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL; else process.env.A2A_HUB_URL = origHubUrl;
    if (origAllow === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE; else process.env.EVOMAP_HUB_ALLOW_INSECURE = origAllow;
    if (restoreEvolverHome) restoreEvolverHome();
    restoreEvolverHome = null;
    _resetHubNodeSecretStateForTesting();
    _resetHeartbeatStateForTesting();
  });

  test('deep reauth lockout + elapsed probe window: one re-hello probe recovers without restart/sleep', async () => {
    // Deep failure (>=2) with a 1h backoff still in the future, and no
    // probe sent yet (lastReauthProbeAt far in the past).
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 60_000,
      consecutiveReauthFailures: 3,
      reauthBackoffUntil: Date.now() + 60 * 60_000,
      lastReauthProbeAt: 0,
    });
    let hbCalls = 0;
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        // Hub recovered: hand back a fresh secret.
        return res(200, { ok: true, status: 'ok', payload: { node_secret: 'b'.repeat(64) } });
      }
      hbCalls++;
      // First (pre-rotate) heartbeat still 403; retried (post-rotate) ok.
      return hbCalls === 1 ? res(403, { error: 'node_secret_invalid' }) : res(200, { status: 'ok' });
    };
    await sendHeartbeat();
    await settle();
    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.reauthBackoffUntil, 0,
      'a successful probe re-hello during deep backoff must clear the backoff (escape hatch). ' +
      'Pre-round-9 the rotate short-circuited without ever contacting the hub, so this stayed non-zero.');
    assert.equal(s.consecutiveReauthFailures, 0, 'a successful probe resets the reauth failure counter');
  });

  test('deep reauth lockout within the probe throttle: no re-hello is sent (hub protection preserved)', async () => {
    const until = Date.now() + 60 * 60_000;
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 60_000,
      consecutiveReauthFailures: 3,
      reauthBackoffUntil: until,
      lastReauthProbeAt: Date.now(), // just probed -> within throttle
    });
    let helloCalls = 0;
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) { helloCalls++; return res(200, { ok: true, status: 'ok' }); }
      return res(403, { error: 'node_secret_invalid' });
    };
    await sendHeartbeat();
    await settle();
    const s = _getHeartbeatInternalsForTesting();
    assert.equal(helloCalls, 0, 'within the probe throttle no re-hello may be sent');
    assert.equal(s.reauthBackoffUntil, until, 'a throttled probe must not change the backoff window');
  });
});

describe('round-9: tick-generation guard', () => {
  let origFetch, origHubUrl, origAllow, restoreEvolverHome;
  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    _resetHubNodeSecretStateForTesting();
    origFetch = global.fetch;
    origHubUrl = process.env.A2A_HUB_URL;
    origAllow = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    restoreEvolverHome = installTempEvolverHome();
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    global.fetch = origFetch;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL; else process.env.A2A_HUB_URL = origHubUrl;
    if (origAllow === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE; else process.env.EVOMAP_HUB_ALLOW_INSECURE = origAllow;
    if (restoreEvolverHome) restoreEvolverHome();
    restoreEvolverHome = null;
    _resetHubNodeSecretStateForTesting();
    _resetHeartbeatStateForTesting();
  });

  test('an orphaned in-flight tick does not clear the gate a superseding tick now owns', async () => {
    // Deferred heartbeat response so tick A stays wedged in-flight.
    let resolveHb;
    const hbPromise = new Promise((r) => { resolveHb = r; });
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) return res(200, { ok: true, status: 'ok' });
      return hbPromise;
    };
    _setHeartbeatStateForTesting({ running: true, intervalMs: 1000 });
    _driveHeartbeatTickForTesting(1000); // tick A starts and wedges on hbPromise
    await settle();
    let s = _getHeartbeatInternalsForTesting();
    assert.equal(s.inFlight, true, 'tick A should be in flight (awaiting the deferred response)');
    const genA = s.tickGeneration;

    // Simulate the hung-tick watchdog / wake branch superseding tick A:
    // bump the generation, then a fresh tick B takes the single-flight gate.
    _bumpTickGenerationForTesting();
    _setHeartbeatStateForTesting({ inFlight: true }); // tick B now owns the gate

    // Now tick A's response finally arrives; its continuation must bail.
    resolveHb(res(200, { status: 'ok' }));
    await settle();
    s = _getHeartbeatInternalsForTesting();
    assert.ok(s.tickGeneration > genA, 'generation advanced past tick A');
    assert.equal(s.inFlight, true,
      'round-9: the orphaned tick A must NOT clear the gate owned by the superseding tick B ' +
      '(pre-fix its continuation set _heartbeatInFlight=false and double-scheduled)');
  });
});
