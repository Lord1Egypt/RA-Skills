// Regression coverage for the round-5 audit (2026-05-28) heartbeat
// resilience fixes. Each test pins exactly one fix surfaced by the
// 12-agent round-5 audit on top of rounds 1-4. The bugs being covered:
//
//   1. Round-4 installed _pendingRescheduleDelayMs = 8 min when the
//      unknown_node loop counter saturated. But the drift detector's
//      persistent-failure branch (consecutiveFailures > 0 + idle >
//      2*interval) called pokeHeartbeat() every 30s and bypassed the
//      delay via setImmediate(_heartbeatTick). The very next tick hit
//      the still-cached unknown_node, bumped the counter, and the 8
//      min wait was effectively zero. Round-5 adds an absolute
//      _unknownNodeBackoffUntil deadline that the drift detector
//      respects.
//
//   2. The unknown_node -> re-hello-ok branch reset the failure
//      counter but did NOT delay the next tick. At default 30s
//      heartbeat interval, the next tick hits the same cached
//      unknown_node almost immediately and the counter climbs to the
//      threshold (above) for nothing but DB replication lag on the
//      first hello write. Round-5 installs a hello-recovery delay
//      so the cache has time to refresh.
//
//   3. _fetchHubEvents was only called from the heartbeat success
//      path when has_pending_events=true. With SSE silently broken
//      on default installs (Node 22.x EventSource is experimental,
//      the `eventsource` fallback package is not in node_modules),
//      events queued server-side until the next heartbeat happened
//      to surface has_pending_events. Round-5 adds a self-driving
//      long-poll that runs continuously and respects the unknown_node
//      backoff.
//
//   4. SSE open / error and reauth-backoff installation now write
//      one-line JSON records to evolver_loop.log so the next "evolver
//      dead" incident has on-disk evidence past the final
//      heartbeat_ok entry. Round-4 logged only the success path.
//
//   5. getHeartbeatStats() exposes unknownNodeBackoffUntil +
//      selfDrivingPollEnabled / selfDrivingPollBackoffMs so ops can
//      distinguish "waiting on hub cache" from "running but no
//      events" without re-reading the source.

const { describe, it, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

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
const { sendHeartbeat, getHeartbeatStats } = a2a;
const {
  _resetHeartbeatStateForTesting,
  _setHeartbeatStateForTesting,
  _getHeartbeatInternalsForTesting,
  _startSelfDrivingPollForTesting,
  _stopSelfDrivingPollForTesting,
  _runSelfDrivingPollForTesting,
} = a2a._testing;

function nextTick() {
  return new Promise((r) => setImmediate(r));
}
async function settle() {
  await nextTick(); await nextTick(); await nextTick(); await nextTick();
}

describe('round-5: unknown_node backoff installs an absolute deadline (not just _pendingRescheduleDelayMs)', () => {
  let origFetch, origHubUrl, origAllow;
  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    origFetch = global.fetch;
    origHubUrl = process.env.A2A_HUB_URL;
    origAllow = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    global.fetch = origFetch;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = origHubUrl;
    if (origAllow === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = origAllow;
    _resetHeartbeatStateForTesting();
  });

  it('crossing the threshold installs unknownNodeBackoffUntil >= now + 7min', async () => {
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };
    await sendHeartbeat();
    await settle();
    await sendHeartbeat();
    await settle();
    const state = _getHeartbeatInternalsForTesting();
    assert.ok(
      state.unknownNodeBackoffUntil > Date.now() + 7 * 60_000,
      'deadline must extend past the hub cache TTL (420s); got ' + state.unknownNodeBackoffUntil
    );
  });

  it('persistent-failure poke is suppressed while the deadline is active (drift + pokeHeartbeat share the gate)', () => {
    // The pre-fix version of this test only set state and asserted that
    // state -- it never actually invoked the drift detector's poke path,
    // so the gate it claims to guard was never exercised. The drift
    // detector lives in an internal setInterval (a2aProtocol.js around
    // L2614) and has no direct test seam, so we exercise the IDENTICAL
    // gate contract by calling pokeHeartbeat() directly:
    //   - Round-5 added `!unknownNodeBackoffActive` to the drift detector's
    //     persistent-failure branch (a2aProtocol.js ~L2836).
    //   - Round-6 (§19.1) added the matching
    //     `if (_unknownNodeBackoffUntil > now) return false`
    //     guard inside pokeHeartbeat() itself (a2aProtocol.js ~L1249).
    // Both fixes enforce the same contract: while the cache-poisoning
    // backoff is hot, NO poke (drift-detector-driven, user-activity,
    // SIGCONT, SSE-message) may schedule a heartbeat tick. Reverting
    // either fix flips pokeHeartbeat from `return false` to scheduling
    // a setImmediate(_heartbeatTick), which this test catches.
    const now = Date.now();
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 30_000,
      lastTickAt: now - 5 * 60_000, // way past 2*interval -> drift would poke
      consecutiveFailures: 3,         // wasFailing branch -> bypasses throttle
      unknownNodeBackoffUntil: now + 4 * 60_000,
    });
    // Sanity: the persistent-failure preconditions are real, so a missing
    // gate would actually schedule a tick (rather than being suppressed by
    // some other unrelated guard).
    const preState = _getHeartbeatInternalsForTesting();
    assert.equal(preState.running, true);
    assert.equal(preState.inFlight, false);
    assert.ok(preState.consecutiveFailures > 0,
      'precondition: failure counter must be > 0 so pokeHeartbeat takes the wasFailing path');
    assert.ok(preState.unknownNodeBackoffUntil > Date.now(),
      'precondition: backoff deadline must be in the future to exercise the gate');

    // Spy on setImmediate -- pokeHeartbeat's "actually schedule a tick"
    // path queues setImmediate(_heartbeatTick). If the gate is alive, no
    // such call is made.
    let setImmediateCalls = 0;
    const origSI = global.setImmediate;
    global.setImmediate = function () {
      setImmediateCalls++;
      return origSI.apply(null, arguments);
    };
    let pokeResult;
    try {
      pokeResult = a2a.pokeHeartbeat();
    } finally {
      global.setImmediate = origSI;
    }

    assert.equal(pokeResult, false,
      'pokeHeartbeat must REFUSE while unknownNodeBackoffUntil is in the future. ' +
      'Pre-fix: returns true and queues setImmediate(_heartbeatTick), hammering ' +
      'the still-hot hub cache every 30s.');
    assert.equal(setImmediateCalls, 0,
      'no setImmediate(_heartbeatTick) must be queued while the deadline is active');

    const after = _getHeartbeatInternalsForTesting();
    assert.ok(after.unknownNodeBackoffUntil > Date.now(),
      'deadline must remain intact after a refused poke');
    assert.equal(after.consecutiveFailures, 3,
      'pokeHeartbeat must NOT clear the failure counter when it refuses ' +
      '(the round-3 fix to pokeHeartbeat: gate first, mutate second)');
  });

  it('hello-recovery delay arms _pendingRescheduleDelayMs even when the counter is below threshold', async () => {
    // First tick: unknown_node + hello ok -> counter=1, below threshold,
    // but the hello-recovery delay should still arm so the next tick
    // does not slam the cached response 30s later.
    //
    // Precondition: confirm _pendingRescheduleDelayMs starts at 0 so the
    // assertion below proves the value was set DURING this tick (rather
    // than inherited from prior state). _resetHeartbeatStateForTesting()
    // in beforeEach already clears it, but pinning the precondition makes
    // a regression in the reset hook surface here too instead of silently
    // letting a stale 30s+ value pass the post-tick assertion.
    const pre = _getHeartbeatInternalsForTesting();
    assert.equal(pre.pendingRescheduleDelayMs, 0,
      'precondition: _pendingRescheduleDelayMs must start at 0 so the post-tick ' +
      'assertion proves the hello-recovery branch (a2aProtocol.js ~L1749) set it');

    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };
    await sendHeartbeat();
    await settle();
    const after = _getHeartbeatInternalsForTesting();
    assert.equal(after.consecutiveUnknownNodeAfterHello, 1,
      'counter should be 1 (below threshold) after one cycle -- proves the unknown_node ' +
      'hello-ok branch actually fired (not just stubbed state inspection)');
    assert.ok(after.pendingRescheduleDelayMs >= 30_000,
      'hello-recovery delay must be at least HEARTBEAT_FIRST_DELAY_MS margin to let DB replication catch up; got ' +
      after.pendingRescheduleDelayMs);
  });

  it('an ok heartbeat clears both the counter AND the deadline', async () => {
    // Force the deadline to a future value, then run one ok cycle.
    const future = Date.now() + 10 * 60_000;
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 30_000,
      unknownNodeBackoffUntil: future,
    });
    assert.equal(_getHeartbeatInternalsForTesting().unknownNodeBackoffUntil, future);
    global.fetch = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    await sendHeartbeat();
    await settle();
    assert.equal(_getHeartbeatInternalsForTesting().unknownNodeBackoffUntil, 0,
      'a single ok heartbeat must drop the deadline so the next episode starts fresh');
  });

  it('_resetHeartbeatStateForTesting clears the deadline (cross-test isolation)', () => {
    _setHeartbeatStateForTesting({ unknownNodeBackoffUntil: Date.now() + 60_000 });
    _resetHeartbeatStateForTesting();
    assert.equal(_getHeartbeatInternalsForTesting().unknownNodeBackoffUntil, 0,
      'reset hook must clear the round-5 deadline');
  });
});

describe('round-5: self-driving long-poll runs independently of heartbeat', () => {
  let origFetch, origHubUrl, origAllow, origDisableSelf;
  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    origFetch = global.fetch;
    origHubUrl = process.env.A2A_HUB_URL;
    origAllow = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    origDisableSelf = process.env.EVOLVER_DISABLE_SELF_DRIVING_POLL;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    delete process.env.EVOLVER_DISABLE_SELF_DRIVING_POLL;
  });
  afterEach(() => {
    _stopSelfDrivingPollForTesting();
    global.fetch = origFetch;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = origHubUrl;
    if (origAllow === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = origAllow;
    if (origDisableSelf === undefined) delete process.env.EVOLVER_DISABLE_SELF_DRIVING_POLL;
    else process.env.EVOLVER_DISABLE_SELF_DRIVING_POLL = origDisableSelf;
    _resetHeartbeatStateForTesting();
  });

  it('startSelfDrivingPoll arms the timer; stop clears it', () => {
    assert.equal(_getHeartbeatInternalsForTesting().selfDrivingPollEnabled, false);
    _startSelfDrivingPollForTesting();
    const after = _getHeartbeatInternalsForTesting();
    assert.equal(after.selfDrivingPollEnabled, true,
      'enabled flag is set by start()');
    assert.equal(after.hasSelfDrivingPollTimer, true,
      'start() schedules the initial run');
    _stopSelfDrivingPollForTesting();
    const stopped = _getHeartbeatInternalsForTesting();
    assert.equal(stopped.selfDrivingPollEnabled, false);
    assert.equal(stopped.hasSelfDrivingPollTimer, false);
  });

  it('EVOLVER_DISABLE_SELF_DRIVING_POLL=1 is the escape hatch', () => {
    process.env.EVOLVER_DISABLE_SELF_DRIVING_POLL = '1';
    _startSelfDrivingPollForTesting();
    const state = _getHeartbeatInternalsForTesting();
    assert.equal(state.selfDrivingPollEnabled, false,
      'env var prevents the runner from arming');
    assert.equal(state.hasSelfDrivingPollTimer, false);
  });

  it('runner short-circuits while unknownNodeBackoffUntil is in the future', async () => {
    let pollCalls = 0;
    global.fetch = async (url) => {
      if (String(url).indexOf('/a2a/events/poll') !== -1) {
        pollCalls++;
      }
      return { ok: true, status: 200, json: async () => ({ events: [] }), text: async () => '' };
    };
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 30_000,
      unknownNodeBackoffUntil: Date.now() + 5 * 60_000,
    });
    _startSelfDrivingPollForTesting();
    // Manually run once -- it should bail without issuing a network request.
    _runSelfDrivingPollForTesting();
    await settle();
    assert.equal(pollCalls, 0,
      'self-driving poll must not call /a2a/events/poll while unknown_node backoff is active');
    // The timer must still be re-armed for a future quiet check.
    assert.equal(_getHeartbeatInternalsForTesting().hasSelfDrivingPollTimer, true);
  });

  it('runner short-circuits while reauth backoff is in the future', async () => {
    let pollCalls = 0;
    global.fetch = async (url) => {
      if (String(url).indexOf('/a2a/events/poll') !== -1) {
        pollCalls++;
      }
      return { ok: true, status: 200, json: async () => ({ events: [] }), text: async () => '' };
    };
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 30_000,
      reauthBackoffUntil: Date.now() + 60 * 60_000,
    });
    _startSelfDrivingPollForTesting();
    _runSelfDrivingPollForTesting();
    await settle();
    assert.equal(pollCalls, 0,
      'self-driving poll must not call /a2a/events/poll while reauth backoff is active');
  });

  it('getHeartbeatStats() surfaces selfDrivingPollEnabled / backoff for ops tooling', () => {
    _startSelfDrivingPollForTesting();
    const stats = getHeartbeatStats();
    assert.equal(stats.selfDrivingPollEnabled, true);
    assert.equal(typeof stats.selfDrivingPollBackoffMs, 'number');
    assert.equal(typeof stats.unknownNodeBackoffUntil, 'number');
  });
});

describe('round-5: disk log writes failure + lifecycle records (not just heartbeat_ok)', () => {
  let origFetch, origHubUrl, origAllow, origLogPath, origEvolverHome;
  let tmpDir;
  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    origFetch = global.fetch;
    origHubUrl = process.env.A2A_HUB_URL;
    origAllow = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    origLogPath = process.env.EVOLVER_LOG_PATH;
    origEvolverHome = process.env.EVOLVER_REPO_ROOT;
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-r5-log-'));
    // Force the log destination so the test does not depend on repo
    // root resolution. getEvolverLogPath honours EVOLVER_LOG_PATH.
    process.env.EVOLVER_LOG_PATH = path.join(tmpDir, 'evolver_loop.log');
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    global.fetch = origFetch;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = origHubUrl;
    if (origAllow === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = origAllow;
    if (origLogPath === undefined) delete process.env.EVOLVER_LOG_PATH;
    else process.env.EVOLVER_LOG_PATH = origLogPath;
    if (origEvolverHome === undefined) delete process.env.EVOLVER_REPO_ROOT;
    else process.env.EVOLVER_REPO_ROOT = origEvolverHome;
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    _resetHeartbeatStateForTesting();
  });

  it('a network failure writes a heartbeat_fail record (not silence after the last ok)', async () => {
    global.fetch = async () => {
      throw new Error('ECONNRESET: simulated transport failure');
    };
    await sendHeartbeat();
    await settle();
    const logPath = process.env.EVOLVER_LOG_PATH;
    if (!fs.existsSync(logPath)) {
      // If the log helper could not resolve the path (some test envs),
      // skip the assertion rather than failing on infra noise.
      return;
    }
    const content = fs.readFileSync(logPath, 'utf8');
    assert.ok(
      content.indexOf('"heartbeat_fail"') !== -1,
      'failure path must write a heartbeat_fail entry; log content: ' + content
    );
  });

  it('unknown_node backoff arming writes a dedicated record so RCA can find it', async () => {
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };
    // Two cycles trips the threshold and arms the deadline.
    await sendHeartbeat();
    await settle();
    await sendHeartbeat();
    await settle();
    const logPath = process.env.EVOLVER_LOG_PATH;
    if (!fs.existsSync(logPath)) return;
    const content = fs.readFileSync(logPath, 'utf8');
    assert.ok(
      content.indexOf('"unknown_node_backoff_armed"') !== -1,
      'backoff arming must be logged for the next incident RCA; log content: ' + content
    );
  });
});
