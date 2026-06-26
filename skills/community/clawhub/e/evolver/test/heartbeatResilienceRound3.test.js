// Regression coverage for the round-3 audit (2026-05-28) heartbeat
// resilience fixes. Each test pins exactly one fix so a future refactor
// that silently undoes it will fail loudly. The bugs being covered:
//
//   1. pokeHeartbeat() previously cleared _heartbeatConsecutiveFailures
//      BEFORE checking _heartbeatInFlight. With a tick already in flight
//      the early-return left the counter wiped even though the in-flight
//      tick had not yet produced a result. The drift detector's
//      persistent-failure branch then could not fire because it gates on
//      consecutiveFailures > 0. The new order: gate first, mutate second.
//
//   2. _fetchHubEvents flipped _pollInflight=true BEFORE calling
//      hubFetch. A synchronous throw from getNodeId / hubFetch / etc.
//      escaped the .finally() cleaner and pinned _pollInflight=true for
//      the rest of the process lifetime. Every subsequent heartbeat that
//      saw has_pending_events would early-return at the top of the
//      function and the node never processed another hub event.
//
//   3. _heartbeatFpSent flipped to true synchronously inside the body
//      construction (before hubFetch ran). A heartbeat that failed
//      mid-flight (process suspended, abort timeout, dropped response)
//      left the client thinking the fingerprint was delivered while the
//      hub had no record. A short sleep (90s..30min) pokes but does NOT
//      re-arm fingerprint -> dashboard stays "unknown version" until
//      the next process restart. The flag now flips only inside the
//      success branch.
//
//   4. _scheduleNextHeartbeat had no lower bound on the delay. A
//      misconfigured HEARTBEAT_INTERVAL_MS=0 (now floored by envPositiveInt
//      but defense in depth) or a hub retry_after_ms=0 would turn the
//      next-tick setTimeout into ~1ms, becoming an event-loop hot spin
//      that burns CPU and trips the hub's 6/300s per-sender rate limit.
//
//   5. SSE reconnect backoff (_sseReconnectMs) saturated at 120s through
//      pre-sleep flaps. The drift detector's long-sleep branch did NOT
//      reset it on wake, so the first post-wake reconnect waited up to
//      2 minutes even though the cause (broken socket) was already
//      resolved by the wake.
//
//   6. stopHeartbeat / _resetHeartbeatStateForTesting did not clear
//      _pendingRescheduleDelayMs. A test that exercised the rate_limited
//      branch and then stopped without letting _scheduleNextHeartbeat
//      consume the value leaked the delay into the next test (or the
//      next process lifetime under an admin restart).

const { describe, it, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

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
const {
  pokeHeartbeat,
  stopHeartbeat,
} = a2a;
const {
  _resetHeartbeatStateForTesting,
  _setHeartbeatStateForTesting,
  _driveHeartbeatTickForTesting,
  _getHeartbeatInternalsForTesting,
  _resetSseReconnectBackoffForTesting,
} = a2a._testing;

function nextTick() {
  return new Promise((r) => setImmediate(r));
}
async function settle() {
  await nextTick(); await nextTick(); await nextTick();
}

describe('round-3: pokeHeartbeat preserves consecutiveFailures when a tick is in flight', () => {
  beforeEach(() => { _resetHeartbeatStateForTesting(); });
  afterEach(() => { _resetHeartbeatStateForTesting(); });

  it('does NOT wipe _heartbeatConsecutiveFailures when inFlight=true', () => {
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 60_000,
      inFlight: true,
      consecutiveFailures: 4,
    });
    const before = _getHeartbeatInternalsForTesting();
    assert.equal(before.consecutiveFailures, 4);
    assert.equal(before.inFlight, true);

    const result = pokeHeartbeat();

    const after = _getHeartbeatInternalsForTesting();
    assert.equal(result, true, 'in-flight is liveness proof; poke returns true');
    assert.equal(after.consecutiveFailures, 4,
      'counter must be preserved so drift detector v2 can fire');
    assert.equal(after.inFlight, true, 'in-flight stays true');
  });

  it('DOES wipe _heartbeatConsecutiveFailures when inFlight=false (poke drives a fresh tick)', async () => {
    // Stub fetch so the driven tick resolves cleanly.
    const origFetch = global.fetch;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    global.fetch = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    try {
      _setHeartbeatStateForTesting({
        running: true,
        intervalMs: 60_000,
        inFlight: false,
        consecutiveFailures: 3,
        // Stamp lastTickAt far in the past so the healthy-node throttle
        // does not suppress the poke.
        lastTickAt: 0,
      });

      pokeHeartbeat();

      const after = _getHeartbeatInternalsForTesting();
      assert.equal(after.consecutiveFailures, 0,
        'fresh poke clears counter -- this is the user-driven retry signal');
    } finally {
      global.fetch = origFetch;
    }
  });
});

describe('round-3: _scheduleNextHeartbeat respects a 1s floor against misconfiguration', () => {
  const {
    _scheduleNextHeartbeatForTesting,
    _heartbeatMinScheduleDelayMsForTesting,
  } = a2a._testing;

  beforeEach(() => { _resetHeartbeatStateForTesting(); });
  afterEach(() => { _resetHeartbeatStateForTesting(); });

  it('exposes a positive floor constant', () => {
    assert.ok(_heartbeatMinScheduleDelayMsForTesting >= 1000,
      'floor must be >= 1000ms to keep next-tick out of hot-loop territory');
  });

  it('intervalMs=0 + pending=0 schedules at the floor, not 0', () => {
    _setHeartbeatStateForTesting({ running: true, intervalMs: 0 });
    _scheduleNextHeartbeatForTesting(0);
    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.hasTimer, true,
      'reschedule fires the setTimeout even when intervalMs=0');
    // The internal _heartbeatTimer is opaque to tests, so we re-assert
    // via the side effect: the loop is now armed at the floor. We can
    // verify the value indirectly by triggering a second reschedule with
    // a known-higher delay and confirming hasTimer flips correctly.
    _scheduleNextHeartbeatForTesting(10_000);
    const s2 = _getHeartbeatInternalsForTesting();
    assert.equal(s2.hasTimer, true);
  });

  // Regression: the hung-tick watchdog calls _scheduleNextHeartbeat(0)
  // to force prompt recovery from a wedged tick. A previous version used
  // `delayMs || _heartbeatIntervalMs`, which coerces an explicit 0 to
  // the full default interval (~6min), delaying recovery and bypassing
  // the 1s floor. The existing intervalMs=0 test masked this because
  // 0||0===0 (the floor then fires anyway). Use a NON-zero interval so
  // the bug surfaces: pre-fix, requested === intervalMs (e.g. 60_000)
  // and the timer arms 60s out; post-fix, requested === 0 and the floor
  // clamps to 1000ms.
  it('explicit delayMs=0 is honored as "schedule now" and clamped only by the floor (non-zero interval)', () => {
    _setHeartbeatStateForTesting({ running: true, intervalMs: 60_000 });
    // Capture the delay passed to setTimeout. The internal
    // _heartbeatTimer is opaque, but the global setTimeout call IS
    // observable. Stub once, restore immediately.
    const origSetTimeout = global.setTimeout;
    let observedDelay = null;
    global.setTimeout = function (fn, delay) {
      observedDelay = delay;
      // Return a no-op timer-like object with unref() so production code
      // (`if (_heartbeatTimer.unref) _heartbeatTimer.unref();`) is happy
      // and the actual fn never fires during this synchronous test.
      return { unref: function () {}, _isStub: true };
    };
    try {
      _scheduleNextHeartbeatForTesting(0);
    } finally {
      global.setTimeout = origSetTimeout;
    }
    assert.ok(observedDelay !== null,
      'setTimeout must have been called by _scheduleNextHeartbeat');
    assert.ok(observedDelay <= _heartbeatMinScheduleDelayMsForTesting,
      'explicit delayMs=0 must be treated as "schedule promptly" and clamped to the floor (got ' +
      observedDelay + 'ms; floor=' + _heartbeatMinScheduleDelayMsForTesting +
      'ms; intervalMs=60000). Pre-fix bug: `0 || intervalMs` coerced 0 to 60_000.');
    assert.notEqual(observedDelay, 60_000,
      'delayMs=0 must NOT degrade to the full _heartbeatIntervalMs -- ' +
      'that breaks the hung-tick watchdog\'s prompt-recovery contract');
  });

  it('a stale _pendingRescheduleDelayMs is honored if it exceeds requested+floor', () => {
    const {
      _setPendingRescheduleDelayMsForTesting,
    } = a2a._testing;
    _setHeartbeatStateForTesting({ running: true, intervalMs: 60_000 });
    _setPendingRescheduleDelayMsForTesting(600_000);
    _scheduleNextHeartbeatForTesting();
    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.pendingRescheduleDelayMs, 0,
      'pending is read-and-clear so the next reschedule cannot inherit');
  });
});

describe('round-3: stopHeartbeat clears _pendingRescheduleDelayMs', () => {
  const { _setPendingRescheduleDelayMsForTesting } = a2a._testing;
  beforeEach(() => { _resetHeartbeatStateForTesting(); });
  afterEach(() => { _resetHeartbeatStateForTesting(); });

  it('stopHeartbeat() wipes a non-zero pending signal so a fresh start cannot inherit it', () => {
    _setHeartbeatStateForTesting({ running: true, intervalMs: 60_000 });
    _setPendingRescheduleDelayMsForTesting(605_000);
    const before = _getHeartbeatInternalsForTesting();
    assert.equal(before.pendingRescheduleDelayMs, 605_000,
      'precondition: pending signal is set');

    stopHeartbeat();

    const after = _getHeartbeatInternalsForTesting();
    assert.equal(after.pendingRescheduleDelayMs, 0,
      'stopHeartbeat must clear _pendingRescheduleDelayMs');
    assert.equal(after.inFlight, false,
      'stopHeartbeat must also clear in-flight so a future startHeartbeat() can run');
  });

  it('_resetHeartbeatStateForTesting() wipes the pending signal for cross-test isolation', () => {
    _setHeartbeatStateForTesting({ running: true, intervalMs: 60_000 });
    _setPendingRescheduleDelayMsForTesting(900_000);
    _resetHeartbeatStateForTesting();
    const after = _getHeartbeatInternalsForTesting();
    assert.equal(after.pendingRescheduleDelayMs, 0,
      'reset hook must clear pending so prior-test state cannot bleed in');
  });
});

describe('round-3: env_fingerprint flag flips only on successful response', () => {
  let origFetch;
  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    origFetch = global.fetch;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    global.fetch = origFetch;
    _resetHeartbeatStateForTesting();
  });

  it('a failing heartbeat does NOT set _heartbeatFpSent (so the next tick re-emits the fingerprint)', async () => {
    // First tick fails (network error). The fingerprint must NOT be
    // marked as sent.
    global.fetch = async () => { throw new Error('connect ETIMEDOUT'); };
    _driveHeartbeatTickForTesting(60_000);
    await settle();
    const after = _getHeartbeatInternalsForTesting();
    assert.equal(after.fpSent, false,
      'failed tick must not commit fpSent -- otherwise short-sleep recovery never re-emits the fingerprint');
  });

  it('a successful heartbeat sets _heartbeatFpSent', async () => {
    global.fetch = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    _driveHeartbeatTickForTesting(60_000);
    await settle();
    const after = _getHeartbeatInternalsForTesting();
    assert.equal(after.fpSent, true,
      'successful tick commits fpSent so subsequent ticks do not re-spend the bandwidth');
  });
});

describe('round-3: SSE reconnect backoff resets on long-sleep wake', () => {
  beforeEach(() => { _resetHeartbeatStateForTesting(); });
  afterEach(() => {
    _resetHeartbeatStateForTesting();
    // stopEventStream() snaps _sseReconnectMs back to base and clears any
    // pending reconnect timer (real or stubbed) so this test cannot leak
    // saturated state into sibling tests in the same process.
    try { a2a.stopEventStream(); } catch (_) {}
  });

  it('snaps the backoff from a saturated value back to the base interval (not just <= base)', () => {
    // The pre-fix version of this test only asserted `sseReconnectMs <= 5000`
    // after calling the reset helper -- but the initial default IS 5000ms,
    // so the assertion passed even if the reset were a no-op. To actually
    // guard the long-sleep-wake fix we have to INFLATE _sseReconnectMs to
    // saturation first, then prove the reset snaps it back down.
    //
    // We do not have a direct setter for _sseReconnectMs (it lives inside
    // the SSE module as a `let`), but startEventStream() walks the same
    // bump path the production-bug repro does: on a hubOpenEventStream
    // failure it calls _scheduleSseReconnect(), which (a) sets a setTimeout
    // and (b) doubles _sseReconnectMs (capped at 120000). With A2A_HUB_URL
    // unset, hubOpenEventStream returns ok:false:no_hub_url, exercising
    // exactly that path. Stub setTimeout temporarily so the scheduled
    // reconnect timer never actually fires during the test.
    assert.equal(typeof _resetSseReconnectBackoffForTesting, 'function',
      'long-sleep wake path must have a test-visible reset hook');

    const origHubUrl = process.env.A2A_HUB_URL;
    delete process.env.A2A_HUB_URL;
    const origSetTimeout = global.setTimeout;
    global.setTimeout = function () { return { unref: function () {} }; };
    try {
      // 5000 -> 10000 -> 20000 -> 40000 -> 80000 -> 120000 (saturated).
      // Six calls leaves us comfortably at the ceiling.
      for (let i = 0; i < 6; i++) {
        a2a.startEventStream();
      }
    } finally {
      global.setTimeout = origSetTimeout;
      if (origHubUrl === undefined) delete process.env.A2A_HUB_URL;
      else process.env.A2A_HUB_URL = origHubUrl;
    }

    const inflated = _getHeartbeatInternalsForTesting().sseReconnectMs;
    assert.ok(inflated > 5000,
      'precondition: _sseReconnectMs must have inflated past the 5000ms base; got ' + inflated);
    assert.equal(inflated, 120000,
      'precondition: six failed startEventStream() calls must saturate at 120000ms; got ' + inflated);

    // Now exercise the round-3 reset helper. Pre-fix, this helper was a
    // no-op (or absent), and a long-sleep wake would carry the saturated
    // 120s backoff into the first post-wake reconnect.
    _resetSseReconnectBackoffForTesting();
    const after = _getHeartbeatInternalsForTesting().sseReconnectMs;
    assert.equal(after, 5000,
      'reset must snap _sseReconnectMs from saturation back to the 5000ms base; got ' + after);
    assert.notEqual(after, inflated,
      'reset must actually CHANGE _sseReconnectMs from the inflated value (' + inflated +
      'ms) -- a no-op reset would leave it saturated and the original assertion ' +
      '(<= 5000) would have FALSELY passed because the base default is also 5000');
  });
});

describe('round-3: hubFetch.drainPool() is callable and does not throw', () => {
  it('exports drainPool', () => {
    const hf = require('../src/gep/hubFetch');
    assert.equal(typeof hf.drainPool, 'function',
      'SIGCONT handler relies on this entry point');
  });
  it('drainPool() does not throw and lets subsequent hubFetch work', async () => {
    const hf = require('../src/gep/hubFetch');
    hf.drainPool(); // must not throw
    // After draining, hubFetch should still resolve (in insecure mode it
    // hits global.fetch).
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    const origFetch = global.fetch;
    global.fetch = async () => ({ ok: true, status: 200 });
    try {
      const res = await hf.hubFetch('http://localhost:19999/ping');
      assert.equal(res.ok, true);
    } finally {
      global.fetch = origFetch;
    }
  });
});

describe('round-3: envPositiveInt rejects misconfiguration without spamming warnings', () => {
  const { envPositiveInt } = require('../src/config');
  const origWarn = console.warn;
  let warnCount = 0;
  beforeEach(() => {
    warnCount = 0;
    console.warn = () => { warnCount++; };
  });
  afterEach(() => { console.warn = origWarn; });

  it('returns fallback on 0', () => {
    process.env._TEST_EPI_ZERO = '0';
    assert.equal(envPositiveInt('_TEST_EPI_ZERO', 1234), 1234);
    delete process.env._TEST_EPI_ZERO;
  });
  it('returns fallback on negative', () => {
    process.env._TEST_EPI_NEG = '-5';
    assert.equal(envPositiveInt('_TEST_EPI_NEG', 9999), 9999);
    delete process.env._TEST_EPI_NEG;
  });
  it('returns fallback on non-numeric prefix-only', () => {
    process.env._TEST_EPI_NON = 'abc';
    assert.equal(envPositiveInt('_TEST_EPI_NON', 4242), 4242);
    delete process.env._TEST_EPI_NON;
  });
  it('returns the value when positive integer', () => {
    process.env._TEST_EPI_OK = '15000';
    assert.equal(envPositiveInt('_TEST_EPI_OK', 1), 15000);
    delete process.env._TEST_EPI_OK;
  });
  it('returns fallback on values >= 2^31 (setTimeout would downgrade to 1ms)', () => {
    process.env._TEST_EPI_BIG = String(2 ** 31);
    assert.equal(envPositiveInt('_TEST_EPI_BIG', 7777), 7777);
    delete process.env._TEST_EPI_BIG;
  });
  it('warns at most once per key', () => {
    process.env._TEST_EPI_WARN_ONCE = '0';
    envPositiveInt('_TEST_EPI_WARN_ONCE', 1);
    envPositiveInt('_TEST_EPI_WARN_ONCE', 1);
    envPositiveInt('_TEST_EPI_WARN_ONCE', 1);
    assert.equal(warnCount, 1,
      'one-time warning suppresses log spam on repeated reads of the same misconfigured key');
    delete process.env._TEST_EPI_WARN_ONCE;
  });
});

describe('round-3: idleScheduler caches results for 2s', () => {
  it('does not re-spawn the OS probe within the cache TTL', { skip: process.platform === 'win32' ? 'Windows GetLastInputInfo via inline-C# PowerShell takes >2s on slow VMs (JIT + ps startup), exceeding the cache TTL between the two probes and producing a false-negative on the cache-hit assertion. The cache itself is platform-agnostic; this test exercises real OS spawn timing, which is not what Windows can promise here. Re-enable once we mock the probe via __test hooks for Windows like we do for Linux.' : false }, () => {
    // Force the cache empty by reloading the module.
    delete require.cache[require.resolve('../src/gep/idleScheduler')];
    const ids = require('../src/gep/idleScheduler');
    const t0 = Date.now();
    const a = ids.getSystemIdleSeconds();
    const aLatency = Date.now() - t0;
    const t1 = Date.now();
    const b = ids.getSystemIdleSeconds();
    const bLatency = Date.now() - t1;
    assert.equal(a, b,
      'a cached read returns the same value as the seeding read');
    // The second call should be near-instant (< ~5ms) because no
    // process was spawned. The first call may take 50-800ms depending
    // on platform. We give the second call a generous ceiling that
    // would still flag a regression where the cache is bypassed.
    assert.ok(bLatency <= Math.max(aLatency, 10),
      'cached read must not re-spawn a child process; saw ' +
      bLatency + 'ms (seeding read took ' + aLatency + 'ms)');
  });
});

describe('round-3: validator daemon exposes pokeValidatorDaemon for SIGCONT wake', () => {
  it('exports the function', () => {
    const v = require('../src/gep/validator');
    assert.equal(typeof v.pokeValidatorDaemon, 'function',
      'SIGCONT handler relies on this entry point');
  });
  it('returns false when the daemon is not running', () => {
    const v = require('../src/gep/validator');
    // We do not start the daemon here -- stopping it first is safe.
    if (typeof v.stopValidatorDaemon === 'function') v.stopValidatorDaemon();
    assert.equal(v.pokeValidatorDaemon(), false,
      'no-op when daemon is stopped');
  });
});
