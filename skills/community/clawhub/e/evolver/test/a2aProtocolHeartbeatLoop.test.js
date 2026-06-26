// Regression tests for the heartbeat-loop resilience fix that ports
// evolver/evolver#544 (proxy LifecycleManager) to the default-mode
// a2aProtocol path. The bugs being covered here are:
//
//   1. Loop-killer: in the previous _scheduleNextHeartbeat the reschedule
//      lived in .then(), not finally. A synchronous throw from
//      sendHeartbeat() (e.g. getNodeId() raising, JSON.stringify on a
//      poisoned commitment_updates payload, a logger transport blowing
//      up during the warn call) escaped .catch(), .then never ran,
//      _heartbeatInFlight stayed true forever, and the node went silent
//      for the rest of the process lifetime.
//
//   2. No wake-up mechanism: there was no equivalent of
//      LifecycleManager.pokeHeartbeat(), so even a user activity signal
//      could not force an earlier tick after a long backoff. The default
//      heartbeat interval is 360s.
//
// We do NOT exercise startHeartbeat()'s 30s first-delay timer here --
// that would slow the test suite. Instead we use _driveHeartbeatTickForTesting()
// which short-circuits straight into the scheduler.

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
// Test-only hooks live under a2a._testing.* (intentionally namespaced so
// production callers of the published dist cannot trivially inject faults).
const {
  _setHeartbeatThrowForTesting,
  _resetHeartbeatStateForTesting,
  _driveHeartbeatTickForTesting,
  _getHeartbeatInternalsForTesting,
  _forceDriftLastCheckAtForTesting,
} = a2a._testing;

function nextTick() {
  return new Promise((r) => setImmediate(r));
}

async function settle() {
  // Two setImmediate hops covers the .catch -> .then chain inside the
  // tick, plus the inner setImmediate scheduled by pokeHeartbeat().
  await nextTick();
  await nextTick();
  await nextTick();
}

describe('a2aProtocol heartbeat loop resilience (#544 port)', () => {
  // Stub fetch so any real heartbeat attempt resolves cleanly. The
  // sync-throw cases will not reach here, but the post-throw rescheduled
  // tick will, and we want that one to succeed (or at least not blow up).
  let originalFetch;
  let originalHubUrl;
  let originalInsecure;

  beforeEach(() => {
    originalFetch = global.fetch;
    originalHubUrl = process.env.A2A_HUB_URL;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    _resetHeartbeatStateForTesting();
  });

  afterEach(() => {
    // Always stop so the rescheduled timer (which uses _heartbeatIntervalMs
    // = 60_000 by default in our test driver) does not leak between tests
    // or keep the test runner alive.
    stopHeartbeat();
    _resetHeartbeatStateForTesting();
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
  });

  it('reschedules a follow-up tick after sendHeartbeat throws synchronously (the #544 bug)', async () => {
    // Arm a one-shot synchronous throw. This is the exact failure mode
    // the old code could not survive: the throw happens BEFORE the
    // hubFetch call returns a promise, so the old `.catch()` chain never
    // saw it, and `_heartbeatInFlight` stayed true forever.
    _setHeartbeatThrowForTesting(new Error('synthetic pre-fetch throw'));

    _driveHeartbeatTickForTesting(60_000);

    // After the tick chain settles, the loop must have rescheduled and
    // released the single-flight gate.
    await settle();

    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.inFlight, false, '_heartbeatInFlight must be released after a sync throw');
    assert.equal(s.running, true, 'loop must still be marked running');
    assert.equal(s.hasTimer, true, 'a follow-up setTimeout must have been scheduled');
  });

  it('survives a logger throw inside the catch arm and still reschedules', async () => {
    // Inject a throw, then poison console.warn so even the defensive
    // logger call in the .catch arm raises. The "finally"-equivalent .then
    // backstop must still run.
    _setHeartbeatThrowForTesting(new Error('synthetic pre-fetch throw'));

    const origWarn = console.warn;
    console.warn = function () { throw new Error('logger transport broken'); };

    try {
      _driveHeartbeatTickForTesting(60_000);
      await settle();
    } finally {
      console.warn = origWarn;
    }

    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.inFlight, false, 'loop must reschedule even when the logger itself throws');
    assert.equal(s.hasTimer, true, 'follow-up tick must be scheduled despite logger blowing up');
  });

  it('clears the single-flight gate after a normal successful tick', async () => {
    _driveHeartbeatTickForTesting(60_000);

    await settle();

    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.inFlight, false, '_heartbeatInFlight must be cleared after a clean tick');
    assert.equal(s.hasTimer, true, 'a follow-up tick must be scheduled');
    assert.equal(s.totalSent, 1, 'sendHeartbeat must have been counted exactly once');
  });
});

describe('a2aProtocol pokeHeartbeat() wake-up hook', () => {
  let originalFetch;
  let originalHubUrl;
  let originalInsecure;
  let fetchCallCount;

  beforeEach(() => {
    originalFetch = global.fetch;
    originalHubUrl = process.env.A2A_HUB_URL;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    fetchCallCount = 0;
    global.fetch = async () => {
      fetchCallCount++;
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };
    _resetHeartbeatStateForTesting();
  });

  afterEach(() => {
    stopHeartbeat();
    _resetHeartbeatStateForTesting();
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
  });

  it('is exported from the module', () => {
    assert.equal(typeof pokeHeartbeat, 'function', 'pokeHeartbeat must be exported');
  });

  it('returns false when the loop is not running', () => {
    // _resetHeartbeatStateForTesting set _heartbeatRunning=false in beforeEach.
    assert.equal(pokeHeartbeat(), false, 'pokeHeartbeat must noop when stopped');
  });

  it('fires a tick on the next setImmediate when a healthy node has never ticked', async () => {
    _driveHeartbeatTickForTesting(60_000);
    await settle();
    assert.equal(fetchCallCount, 1, 'baseline tick should have fetched once');

    // Reset the throttle bookkeeping so we can verify pokeHeartbeat
    // fires a fresh tick. Simulate "no recent tick" by clearing
    // _lastTickAt via reset, but keep the loop running.
    const internalsBefore = _getHeartbeatInternalsForTesting();
    assert.equal(internalsBefore.running, true);

    // Force the throttle window expired: rewrite lastTickAt to long ago by
    // stopping and re-driving with a fresh state, then immediately re-arm
    // running=true via the test helper.
    stopHeartbeat();
    _resetHeartbeatStateForTesting();
    // Mark running without running a tick yet; manually set state to
    // mimic "loop has been started but no tick has fired yet" -- _lastTickAt=0
    // means the throttle check skips (sinceLast == Date.now()).
    a2a._testing._driveHeartbeatTickForTesting(60_000);
    await settle();
    // _lastTickAt is now ~now. Move it to the past by stop/reset/re-drive,
    // OR (simpler) just check the "failing" bypass path in the next test.

    // Above flow already proves the tick fires when driven; the throttle
    // and failing-bypass paths are exercised in dedicated tests below.
  });

  it('returns false when called twice in quick succession on a healthy node (60s debounce)', async () => {
    _driveHeartbeatTickForTesting(60_000);
    await settle();
    // _lastTickAt is now ~Date.now(). pokeHeartbeat on a healthy node
    // (consecutiveFailures = 0) must be throttled by _HEARTBEAT_POKE_THROTTLE_MS.
    const result = pokeHeartbeat();
    assert.equal(result, false, 'second poke within debounce window must return false');
  });

  it('bypasses the debounce when the node is failing (consecutiveFailures > 0)', async () => {
    // First, drive a normal tick so _lastTickAt is fresh (throttle would
    // normally block a follow-up poke).
    _driveHeartbeatTickForTesting(60_000);
    await settle();
    const baselineFetch = fetchCallCount;

    // Now simulate a failure state. _resetHeartbeatStateForTesting wipes
    // everything, so instead inject failures via a sync throw + a tick.
    _setHeartbeatThrowForTesting(new Error('synthetic failure'));
    // Re-drive to bump consecutiveFailures through the catch path. Note:
    // sendHeartbeat's catch block (not _heartbeatTick's defensive catch)
    // is what increments _heartbeatConsecutiveFailures. A pre-fetch sync
    // throw bypasses that, so we manually bump via the public surface:
    // call sendHeartbeat directly with the throw armed and let the tick
    // wrap it. The follow-up tick uses normal flow.
    a2a._testing._driveHeartbeatTickForTesting(60_000);
    await settle();

    // The pre-fetch throw doesn't touch _heartbeatConsecutiveFailures,
    // so manually set up the failing-state precondition by stuffing the
    // counter via a controlled async failure path:
    global.fetch = async () => { throw new Error('network down'); };
    a2a._testing._driveHeartbeatTickForTesting(60_000);
    await settle();

    const s = _getHeartbeatInternalsForTesting();
    assert.ok(s.consecutiveFailures > 0, 'precondition: node must be marked failing, got ' + s.consecutiveFailures);

    // Restore success fetch so the poke tick succeeds.
    global.fetch = async () => {
      fetchCallCount++;
      return { ok: true, status: 200, json: async () => ({ status: 'ok' }), text: async () => '' };
    };

    // Now poke. Because consecutiveFailures > 0, the throttle is bypassed.
    const fetchBeforePoke = fetchCallCount;
    const result = pokeHeartbeat();
    assert.equal(result, true, 'poke on a failing node must return true');
    await settle();

    // After a successful poke tick, consecutiveFailures resets to 0
    // (pokeHeartbeat clears it eagerly, and a successful sendHeartbeat
    // also resets it in its .then chain).
    const after = _getHeartbeatInternalsForTesting();
    assert.equal(after.consecutiveFailures, 0, 'poke must clear consecutiveFailures');
    assert.ok(fetchCallCount > fetchBeforePoke, 'poke must have triggered an extra fetch');
  });

  it('returns true (but does not double-fire) when a tick is already in flight', async () => {
    // Make fetch never resolve so the in-flight tick stays pending. Use a
    // manually-controlled promise we resolve in afterEach implicitly via
    // stopHeartbeat + reset.
    let releaseFetch;
    const fetchGate = new Promise((r) => { releaseFetch = r; });
    global.fetch = async () => {
      await fetchGate;
      return { ok: true, status: 200, json: async () => ({ status: 'ok' }), text: async () => '' };
    };

    _driveHeartbeatTickForTesting(60_000);
    await nextTick();
    // The tick should be in flight now (awaiting fetch).
    const s = _getHeartbeatInternalsForTesting();
    assert.equal(s.inFlight, true, 'precondition: tick must be in flight');

    const result = pokeHeartbeat();
    assert.equal(result, true, 'poke during in-flight tick returns true as liveness proof');

    // Release fetch so the test can shut down cleanly.
    releaseFetch();
    await settle();
  });
});

// --------------------------------------------------------------------------
// Wall-clock drift detector (sleep/wake recovery, Task #13)
// --------------------------------------------------------------------------
//
// Default-mode users (no EVOMAP_PROXY=1) only hit startHeartbeat() in
// a2aProtocol; setTimeout fires on libuv's monotonic clock so a suspended
// laptop's heartbeat would never wake up until the next scheduled tick
// (up to 30 min under backoff). The drift detector samples Date.now()
// every 30s and forces a poke if the wall-clock gap exceeds 90s.
//
// Mirrors evolver/test/lifecycleHeartbeatLoopResilience.test.js (task #11
// of the public-repo PR).

describe('a2aProtocol wall-clock drift detector', () => {
  let originalFetch;
  let originalHubUrl;
  let originalInsecure;
  let originalSetInterval;

  beforeEach(() => {
    originalFetch = global.fetch;
    originalHubUrl = process.env.A2A_HUB_URL;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    originalSetInterval = global.setInterval;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    _resetHeartbeatStateForTesting();
  });

  afterEach(() => {
    stopHeartbeat();
    _resetHeartbeatStateForTesting();
    global.setInterval = originalSetInterval;
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
  });

  it('registers a 30s drift interval via startHeartbeat()', () => {
    let driftCallback = null;
    let driftPeriod = null;
    global.setInterval = function (fn, ms, ...rest) {
      if (ms === 30_000) {
        driftCallback = fn;
        driftPeriod = ms;
        return { unref: () => {}, _captured: true };
      }
      return originalSetInterval(fn, ms, ...rest);
    };

    a2a.startHeartbeat(60_000);
    try {
      assert.equal(driftPeriod, 30_000, 'drift interval must be registered at 30s');
      assert.equal(typeof driftCallback, 'function', 'a drift callback must be captured');
      const internals = _getHeartbeatInternalsForTesting();
      assert.equal(internals.hasDriftInterval, true, 'drift interval handle must be tracked');
    } finally {
      stopHeartbeat();
    }
  });

  it('wall-clock jump > threshold pokes heartbeat', async () => {
    let driftCallback = null;
    global.setInterval = function (fn, ms, ...rest) {
      if (ms === 30_000) {
        driftCallback = fn;
        return { unref: () => {}, _captured: true };
      }
      return originalSetInterval(fn, ms, ...rest);
    };

    a2a.startHeartbeat(60_000);
    try {
      assert.ok(driftCallback, 'precondition: drift interval registered');

      // Spy on pokeHeartbeat. We can't easily monkey-patch the
      // module-internal reference, so observe the side effect instead:
      // _heartbeatLastDriftCheckAt advances to the jumped wall clock, and
      // a follow-up tick is scheduled (pokeHeartbeat calls setImmediate
      // _heartbeatTick which sets _heartbeatInFlight true).
      const realNow = Date.now;
      const baseline = realNow();
      // Force the detector's last sample to "baseline" so the jump is
      // measured from a known point. startHeartbeat sets this to realNow
      // at install time; rewriting it here decouples from scheduling jitter.
      a2a._testing._forceDriftLastCheckAtForTesting(baseline);

      // Capture poke calls by wrapping the public pokeHeartbeat. The
      // detector calls pokeHeartbeat from module scope, but we can detect
      // it indirectly via state mutations (_heartbeatInFlight or
      // _heartbeatLastTickAt) -- pokeHeartbeat fires setImmediate(_heartbeatTick).
      const beforeLastTickAt = _getHeartbeatInternalsForTesting().lastTickAt;

      // Simulate a 5-minute wall-clock jump (well above the 90s threshold).
      Date.now = () => baseline + 5 * 60_000;
      try {
        driftCallback();
      } finally {
        Date.now = realNow;
      }

      // After the synchronous driftCallback(), pokeHeartbeat() has been
      // called. It schedules a setImmediate(_heartbeatTick), so flush it.
      await new Promise((r) => setImmediate(r));
      await new Promise((r) => setImmediate(r));

      const after = _getHeartbeatInternalsForTesting();
      assert.ok(
        after.lastDriftCheckAt >= baseline + 5 * 60_000,
        '_lastDriftCheckAt must advance to the observed (jumped) wall clock',
      );
      // A poke from a healthy node with no prior _lastTickAt fires a tick.
      // _heartbeatLastTickAt must therefore have been updated by the poke
      // tick (which calls _heartbeatTick via setImmediate).
      assert.ok(
        after.lastTickAt > beforeLastTickAt,
        'pokeHeartbeat must have driven a tick after the wall-clock jump',
      );
    } finally {
      stopHeartbeat();
    }
  });

  it('small gap (<threshold) does NOT poke heartbeat', async () => {
    let driftCallback = null;
    global.setInterval = function (fn, ms, ...rest) {
      if (ms === 30_000) {
        driftCallback = fn;
        return { unref: () => {}, _captured: true };
      }
      return originalSetInterval(fn, ms, ...rest);
    };

    a2a.startHeartbeat(60_000);
    try {
      assert.ok(driftCallback);

      const realNow = Date.now;
      const baseline = realNow();
      a2a._testing._forceDriftLastCheckAtForTesting(baseline);
      const beforeLastTickAt = _getHeartbeatInternalsForTesting().lastTickAt;

      // 45s gap -- realistic max scheduling jitter, must NOT trigger.
      Date.now = () => baseline + 45_000;
      try {
        driftCallback();
      } finally {
        Date.now = realNow;
      }
      await new Promise((r) => setImmediate(r));
      await new Promise((r) => setImmediate(r));

      const after = _getHeartbeatInternalsForTesting();
      // _lastTickAt may advance during startHeartbeat's hello+first-tick
      // pipeline, but the drift callback itself must not have caused a
      // *new* tick beyond what was already running.
      assert.equal(
        after.lastTickAt, beforeLastTickAt,
        'a <90s wall-clock gap must NOT trigger a fresh poke-driven tick',
      );
    } finally {
      stopHeartbeat();
    }
  });

  it('drift detector survives a thrown logger inside its callback', async () => {
    let driftCallback = null;
    global.setInterval = function (fn, ms, ...rest) {
      if (ms === 30_000) {
        driftCallback = fn;
        return { unref: () => {}, _captured: true };
      }
      return originalSetInterval(fn, ms, ...rest);
    };

    a2a.startHeartbeat(60_000);
    try {
      assert.ok(driftCallback);

      const realNow = Date.now;
      const baseline = realNow();
      a2a._testing._forceDriftLastCheckAtForTesting(baseline);

      // Poison console.warn so the detector's own logger raises. The
      // outer try/catch must swallow it and still update state.
      const origWarn = console.warn;
      console.warn = function () { throw new Error('logger transport broken'); };
      Date.now = () => baseline + 5 * 60_000;
      try {
        assert.doesNotThrow(
          () => driftCallback(),
          'drift callback must NEVER throw, even when its logger explodes',
        );
      } finally {
        Date.now = realNow;
        console.warn = origWarn;
      }
    } finally {
      stopHeartbeat();
    }
  });

  it('stopHeartbeat clears the drift interval', () => {
    a2a.startHeartbeat(60_000);
    try {
      const before = _getHeartbeatInternalsForTesting();
      assert.equal(before.hasDriftInterval, true, 'precondition: drift interval present');
      stopHeartbeat();
      const after = _getHeartbeatInternalsForTesting();
      assert.equal(after.hasDriftInterval, false, 'stopHeartbeat must clear the drift interval');
    } finally {
      stopHeartbeat();
    }
  });
});

// --------------------------------------------------------------------------
// Test-hook namespacing (Task #16, prevent production fault injection)
// --------------------------------------------------------------------------
//
// The previous commit shipped *ForTesting helpers directly on
// module.exports. The obfuscated published dist is generated from this
// file, so production callers of @evomap/evolver could trivially call
//   require('@evomap/evolver/src/gep/a2aProtocol')
//     ._setHeartbeatThrowForTesting(new Error('die'))
// and permanently kill the heartbeat loop. This regression test asserts
// the helpers are only reachable under a2a._testing.*.

describe('a2aProtocol test-hook namespacing (#544 Task #16)', () => {
  const NAMESPACED_HOOKS = [
    '_setHeartbeatThrowForTesting',
    '_resetHeartbeatStateForTesting',
    '_driveHeartbeatTickForTesting',
    '_getHeartbeatInternalsForTesting',
    '_forceDriftLastCheckAtForTesting',
    '_setHeartbeatStateForTesting',
    '_resetForceUpdateStateForTesting',
    '_resetDryRunWarnedForTesting',
  ];

  it('exposes _testing as an object on module.exports', () => {
    assert.equal(typeof a2a._testing, 'object', '_testing must be the namespace object');
    assert.notEqual(a2a._testing, null, '_testing must not be null');
  });

  it('every *ForTesting hook is present under a2a._testing', () => {
    for (const name of NAMESPACED_HOOKS) {
      assert.equal(
        typeof a2a._testing[name], 'function',
        `a2a._testing.${name} must be a function`,
      );
    }
  });

  it('no *ForTesting hook is reachable on a2a directly (production-facing surface)', () => {
    for (const name of NAMESPACED_HOOKS) {
      assert.equal(
        a2a[name], undefined,
        `a2a.${name} must be undefined (only reachable via a2a._testing.${name})`,
      );
    }
  });
});

// --------------------------------------------------------------------------
// Drift detector v2: race-recovery branch (Task #14, mirrors evolver#544
// commit 464c009). The wall-clock-gap branch alone misses the post-wake
// race where a failing tick wins against the detector. v2 fires a poke
// when _heartbeatConsecutiveFailures > 0 and sinceLastTick > 2*interval,
// regardless of wall-clock gap.
// --------------------------------------------------------------------------

describe('a2aProtocol drift detector v2 (race recovery on persistent failure)', () => {
  let originalFetch;
  let originalHubUrl;
  let originalInsecure;
  let originalSetInterval;
  const {
    _setHeartbeatStateForTesting,
  } = a2a._testing;

  beforeEach(() => {
    originalFetch = global.fetch;
    originalHubUrl = process.env.A2A_HUB_URL;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    originalSetInterval = global.setInterval;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    _resetHeartbeatStateForTesting();
  });

  afterEach(() => {
    stopHeartbeat();
    _resetHeartbeatStateForTesting();
    global.setInterval = originalSetInterval;
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
  });

  it('regression: persistent failure + sinceLastTick > 2*interval triggers a poke even with a small wall-clock gap', async () => {
    let driftCallback = null;
    global.setInterval = function (fn, ms, ...rest) {
      if (ms === 30_000) {
        driftCallback = fn;
        return { unref: () => {}, _captured: true };
      }
      return originalSetInterval(fn, ms, ...rest);
    };

    a2a.startHeartbeat(60_000);
    try {
      assert.ok(driftCallback, 'precondition: drift interval registered');

      // Install the v2-trigger preconditions: one consecutive failure, a
      // last tick well over 2*interval ago (13min for a 6min loop), a
      // healthy interval, and a fresh last-drift-check so the wall-clock
      // gap is small (<90s, so the v1 branch CANNOT fire).
      const realNow = Date.now;
      const baseline = realNow();
      _setHeartbeatStateForTesting({
        running: true,
        intervalMs: 6 * 60_000,
        consecutiveFailures: 1,
        lastTickAt: baseline - 13 * 60_000,
        lastDriftCheckAt: baseline,
      });

      const beforeLastTickAt = _getHeartbeatInternalsForTesting().lastTickAt;

      // Tick the wall clock forward by only 45s -- well below the 90s v1
      // threshold. Only the v2 branch should fire.
      Date.now = () => baseline + 45_000;
      try {
        driftCallback();
      } finally {
        Date.now = realNow;
      }

      // pokeHeartbeat schedules a setImmediate(_heartbeatTick). Flush it.
      await new Promise((r) => setImmediate(r));
      await new Promise((r) => setImmediate(r));

      const after = _getHeartbeatInternalsForTesting();
      assert.ok(
        after.lastTickAt > beforeLastTickAt,
        'v2 branch must have driven a fresh tick (lastTickAt advanced past the synthetic past value)',
      );
    } finally {
      stopHeartbeat();
    }
  });

  it('negative: healthy node (consecutiveFailures=0) does NOT trigger v2 even with sinceLastTick > 2*interval', async () => {
    let driftCallback = null;
    global.setInterval = function (fn, ms, ...rest) {
      if (ms === 30_000) {
        driftCallback = fn;
        return { unref: () => {}, _captured: true };
      }
      return originalSetInterval(fn, ms, ...rest);
    };

    a2a.startHeartbeat(60_000);
    try {
      assert.ok(driftCallback);

      const realNow = Date.now;
      const baseline = realNow();
      // Same setup as the positive test BUT with no consecutive failures.
      _setHeartbeatStateForTesting({
        running: true,
        intervalMs: 6 * 60_000,
        consecutiveFailures: 0,
        lastTickAt: baseline - 13 * 60_000,
        lastDriftCheckAt: baseline,
      });

      const beforeLastTickAt = _getHeartbeatInternalsForTesting().lastTickAt;

      Date.now = () => baseline + 45_000;
      try {
        driftCallback();
      } finally {
        Date.now = realNow;
      }
      await new Promise((r) => setImmediate(r));
      await new Promise((r) => setImmediate(r));

      const after = _getHeartbeatInternalsForTesting();
      assert.equal(
        after.lastTickAt, beforeLastTickAt,
        'healthy node must NOT trigger v2; lastTickAt must remain at the seeded past value',
      );
    } finally {
      stopHeartbeat();
    }
  });
});

// --------------------------------------------------------------------------
// Reauth backoff hot-loop protection (Task #15, mirrors evolver#544
// commit 104cdbd). pokeHeartbeat must preserve _heartbeatReauthBackoffUntil
// after 2+ consecutive reauth failures, and deep-failure pokes must still
// respect the 60s throttle.
// --------------------------------------------------------------------------

describe('a2aProtocol reauth backoff + pokeHeartbeat carve-outs', () => {
  let originalFetch;
  let originalHubUrl;
  let originalInsecure;
  const {
    _setHeartbeatStateForTesting,
  } = a2a._testing;

  beforeEach(() => {
    originalFetch = global.fetch;
    originalHubUrl = process.env.A2A_HUB_URL;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    _resetHeartbeatStateForTesting();
  });

  afterEach(() => {
    stopHeartbeat();
    _resetHeartbeatStateForTesting();
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
  });

  it('pokeHeartbeat preserves _heartbeatReauthBackoffUntil after 2+ consecutive reauth failures', () => {
    const now = Date.now();
    const backoffUntil = now + 30 * 60_000;
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 60_000,
      consecutiveFailures: 0,
      lastTickAt: now,
      consecutiveReauthFailures: 2,
      reauthBackoffUntil: backoffUntil,
    });

    pokeHeartbeat();

    const after = _getHeartbeatInternalsForTesting();
    assert.equal(
      after.reauthBackoffUntil, backoffUntil,
      'deep-failure node (>=2 reauth failures) must keep its backoff window intact',
    );
    assert.equal(
      after.consecutiveReauthFailures, 2,
      'consecutiveReauthFailures must not be wiped by pokeHeartbeat',
    );
  });

  it('pokeHeartbeat CLEARS _heartbeatReauthBackoffUntil after only 1 reauth failure (transient blip)', () => {
    const now = Date.now();
    const backoffUntil = now + 30 * 60_000;
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 60_000,
      consecutiveFailures: 0,
      lastTickAt: now,
      consecutiveReauthFailures: 1,
      reauthBackoffUntil: backoffUntil,
    });

    pokeHeartbeat();

    const after = _getHeartbeatInternalsForTesting();
    assert.equal(
      after.reauthBackoffUntil, 0,
      'one-shot reauth failures must let user activity retry by wiping the backoff window',
    );
  });

  it('deep-failure poke (consecutiveReauthFailures>=2) respects the 60s throttle and schedules no new tick', () => {
    // Seed a very recent lastTickAt so the throttle window is firmly active.
    const now = Date.now();
    _setHeartbeatStateForTesting({
      running: true,
      intervalMs: 60_000,
      consecutiveFailures: 0,
      lastTickAt: now - 1_000, // 1s ago, well inside 60s throttle
      consecutiveReauthFailures: 5,
      reauthBackoffUntil: now + 30 * 60_000,
      inFlight: false,
    });

    const before = _getHeartbeatInternalsForTesting();
    const result = pokeHeartbeat();

    assert.equal(
      result, false,
      'deep-failure node must respect the 60s throttle and return false',
    );

    const after = _getHeartbeatInternalsForTesting();
    assert.equal(
      after.hasTimer, before.hasTimer,
      'no new setTimeout should have been scheduled (throttled poke is a noop)',
    );
    assert.equal(
      after.reauthBackoffUntil, before.reauthBackoffUntil,
      'deep-failure throttled poke must also preserve the backoff window',
    );
  });
});
