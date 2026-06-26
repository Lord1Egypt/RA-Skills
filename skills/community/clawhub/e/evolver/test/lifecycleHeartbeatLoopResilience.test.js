'use strict';

// Regression coverage for evolver/issue#544: the heartbeat loop must
// survive (a) a synchronous throw from any pre-fetch helper
// (`countPending`, `getTaskMeta`, `_getEnvFingerprint`, `hello`) and
// (b) cap its backoff at 5min so a single transient failure cannot
// leave the daemon perceived-dead at the previous 30min ceiling.
//
// Why this lives in lifecycleHeartbeatLoopResilience.test.js and not
// in lifecycleRateLimit.test.js: the rate-limit suite covers the
// hello() reauth backoff (REAUTH_BACKOFF_BASE_MS), which is a
// distinct loop. Splitting keeps each suite's stub graph small.

const test = require('node:test');
const assert = require('node:assert');

const { LifecycleManager, HEARTBEAT_BACKOFF_CAP_MS, DEFAULT_HEARTBEAT_INTERVAL } = require('../src/proxy/lifecycle/manager');
const hubFetchMod = require('../src/gep/hubFetch');

const _origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
test.afterEach(() => {
  hubFetchMod._setFetchImplForTest(null);
});
test.after(() => {
  if (_origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  else process.env.EVOMAP_HUB_ALLOW_INSECURE = _origInsecure;
});

function silentLogger() {
  return { info: () => {}, warn: () => {}, error: () => {}, debug: () => {} };
}

function makeStore({ nodeId = null, throwOnCountPending = false } = {}) {
  const state = { node_id: nodeId };
  const inbound = [];
  return {
    getState: (k) => (state[k] !== undefined ? state[k] : null),
    setState: (k, v) => { state[k] = v; },
    countPending: () => {
      if (throwOnCountPending) throw new Error('store_corrupt');
      return 0;
    },
    writeInbound: (e) => inbound.push(e),
    writeInboundBatch: (es) => inbound.push(...es),
    _inbound: inbound,
    _state: state,
  };
}

function makeTextResponse(status, contentType, body) {
  return {
    status,
    ok: status >= 200 && status < 300,
    headers: new Headers({ 'content-type': contentType }),
    text: async () => body,
  };
}

test('heartbeat() returns rejection result instead of throwing when pre-fetch helper throws', async () => {
  // Bug 1 root cause: `countPending` called BEFORE the original try
  // block. A throw here used to escape and reject `tick()`'s awaited
  // promise, killing the loop. After the fix, the whole body sits
  // inside try/catch and returns a structured `{ ok: false, error }`.
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    store: makeStore({ nodeId: 'node_aaaaaaaaaaaa', throwOnCountPending: true }),
    logger: silentLogger(),
  });
  let result;
  await assert.doesNotReject(async () => {
    result = await mgr.heartbeat();
  });
  assert.strictEqual(result.ok, false);
  assert.match(result.error, /store_corrupt/);
  assert.strictEqual(mgr._consecutiveFailures, 1);
});

test('heartbeat tick survives an unforeseen synchronous throw and schedules next tick', async () => {
  // Defence-in-depth: even if a defective subclass overrides
  // heartbeat() to throw synchronously, the loop must keep going.
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    nodeId: 'node_bbbbbbbbbbbb',
    store: makeStore(),
    logger: silentLogger(),
  });
  mgr.heartbeat = () => { throw new Error('synchronous_boom'); };
  // Drive a single tick manually; the loop body increments
  // `_consecutiveFailures` and the timer is armed for the next call.
  mgr._running = true;
  mgr._heartbeatInterval = 360_000;
  await mgr._heartbeatTick();
  assert.strictEqual(mgr._consecutiveFailures, 1);
  assert.ok(mgr._heartbeatTimer, 'next tick must be scheduled');
  // Cleanup before exit so node:test doesn't hang on the unrefed timer.
  clearTimeout(mgr._heartbeatTimer);
  mgr._running = false;
});

test('heartbeat backoff caps at 15min and stays above DEFAULT_HEARTBEAT_INTERVAL', async () => {
  // Issue #544: with the old 30min ceiling, a single hiccup parked the
  // loop for half an hour and the user had to restart the process.
  // Bugbot review caught the inverse mistake: a 5min cap was *below*
  // the 6min default interval, making the exponential branch retry
  // FASTER than success ticks. Cap is now 15min (2.5× default).
  // The cap is exported so this test reads the same constant the loop
  // does — drift detection without coupling to the literal.
  assert.strictEqual(HEARTBEAT_BACKOFF_CAP_MS, 15 * 60_000);
  assert.ok(
    HEARTBEAT_BACKOFF_CAP_MS > DEFAULT_HEARTBEAT_INTERVAL,
    `cap ${HEARTBEAT_BACKOFF_CAP_MS} must exceed default interval ${DEFAULT_HEARTBEAT_INTERVAL} or backoff inverts`
  );

  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    nodeId: 'node_cccccccccccc',
    store: makeStore(),
    logger: silentLogger(),
  });
  mgr.heartbeat = async () => {
    mgr._consecutiveFailures++;
    return { ok: false, error: 'simulated' };
  };
  // 50 prior failures: pow(2, 50) * 360s would land in years if
  // uncapped. We measure that setTimeout was called with the cap.
  mgr._consecutiveFailures = 50;
  const realSetTimeout = global.setTimeout;
  let observedDelay = null;
  global.setTimeout = (fn, delay) => {
    observedDelay = delay;
    return realSetTimeout(() => {}, 0); // park; we'll clearTimeout below
  };
  try {
    mgr._running = true;
    mgr._heartbeatInterval = 360_000;
    await mgr._heartbeatTick();
  } finally {
    global.setTimeout = realSetTimeout;
    mgr._running = false;
    if (mgr._heartbeatTimer) clearTimeout(mgr._heartbeatTimer);
  }
  assert.strictEqual(observedDelay, HEARTBEAT_BACKOFF_CAP_MS);
});

test('heartbeat treats HTML 403 as hub unreachable and does not re-authenticate', async () => {
  hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
    403,
    'text/html',
    '<!DOCTYPE html><title>Cloudflare</title><body>Forbidden</body>',
  ));
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    store: makeStore({ nodeId: 'node_111111111111' }),
    logger: silentLogger(),
  });
  let reauthCalls = 0;
  mgr.reAuthenticate = async () => {
    reauthCalls++;
    return true;
  };

  const result = await mgr.heartbeat();

  assert.strictEqual(result.ok, false);
  assert.strictEqual(result.error, 'hub_unreachable');
  assert.ok(result.retryAfterMs >= 60_000);
  assert.strictEqual(reauthCalls, 0);
  assert.strictEqual(mgr._consecutiveFailures, 1);
});

test('heartbeat still re-authenticates on JSON 403 from the Hub API', async () => {
  hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
    403,
    'application/json',
    '{"error":"invalid_secret"}',
  ));
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    store: makeStore({ nodeId: 'node_222222222222' }),
    logger: silentLogger(),
  });
  let reauthCalls = 0;
  mgr.reAuthenticate = async () => {
    reauthCalls++;
    return false;
  };

  const result = await mgr.heartbeat();

  assert.strictEqual(result.ok, false);
  assert.strictEqual(result.error, 'auth_failed_403');
  assert.strictEqual(reauthCalls, 1);
  assert.strictEqual(mgr._consecutiveFailures, 1);
});

test('heartbeat treats 200 application/json with empty body as a failed heartbeat', async () => {
  hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
    200,
    'application/json',
    '',
  ));
  const store = makeStore({ nodeId: 'node_444444444444' });
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    store,
    logger: silentLogger(),
  });

  const result = await mgr.heartbeat();

  assert.strictEqual(result.ok, false);
  assert.match(result.error, /hub_unreachable|invalid_json|unexpected end|json/i);
  assert.strictEqual(store.getState('last_heartbeat_at'), null);
  assert.strictEqual(mgr._consecutiveFailures, 1);
});

test('heartbeat tick honors hub-unreachable retryAfter before generic failure backoff', async () => {
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    store: makeStore({ nodeId: 'node_333333333333' }),
    logger: silentLogger(),
  });
  mgr.heartbeat = async () => ({ ok: false, error: 'hub_unreachable_backoff', retryAfterMs: 61_000 });
  mgr._hubUnreachableUntil = Date.now() + 61_000;
  mgr._consecutiveFailures = 50;

  const realSetTimeout = global.setTimeout;
  let observedDelay = null;
  global.setTimeout = (fn, delay) => {
    observedDelay = delay;
    return realSetTimeout(() => {}, 0);
  };
  try {
    mgr._running = true;
    mgr._heartbeatInterval = 360_000;
    await mgr._heartbeatTick();
  } finally {
    global.setTimeout = realSetTimeout;
    mgr._running = false;
    if (mgr._heartbeatTimer) clearTimeout(mgr._heartbeatTimer);
  }

  assert.ok(observedDelay >= 60_000 && observedDelay <= 61_000,
    `expected hub retryAfter-sized delay, got ${observedDelay}`);
});

test('heartbeat tick schedules the remaining hub window, not a 30s floor, when <30s left', async () => {
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    store: makeStore({ nodeId: 'node_444444444444' }),
    logger: silentLogger(),
  });
  mgr.heartbeat = async () => ({ ok: false, error: 'hub_unreachable_backoff', retryAfterMs: 5_000 });
  // Only 5s left on the hub-unreachable window. The next tick must fire when
  // the window elapses (~5s), not be padded out to a 30s floor.
  mgr._hubUnreachableUntil = Date.now() + 5_000;
  mgr._consecutiveFailures = 50; // generic branch would otherwise give the 15min cap

  const realSetTimeout = global.setTimeout;
  let observedDelay = null;
  global.setTimeout = (fn, delay) => {
    observedDelay = delay;
    return realSetTimeout(() => {}, 0);
  };
  try {
    mgr._running = true;
    mgr._heartbeatInterval = 360_000;
    await mgr._heartbeatTick();
  } finally {
    global.setTimeout = realSetTimeout;
    mgr._running = false;
    if (mgr._heartbeatTimer) clearTimeout(mgr._heartbeatTimer);
  }

  assert.ok(observedDelay >= 1_000 && observedDelay <= 6_000,
    `expected ~5s remaining-window delay (1s floor, no 30s pad), got ${observedDelay}`);
});

test('pokeHeartbeatLoop is a no-op when loop is not running', () => {
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    nodeId: 'node_dddddddddddd',
    store: makeStore(),
    logger: silentLogger(),
  });
  // Should not throw, should not arm a timer.
  mgr.pokeHeartbeatLoop();
  assert.strictEqual(mgr._heartbeatTimer, null);
});

test('pokeHeartbeatLoop while a tick is mid-await does not fork the loop', async () => {
  // Bugbot #147 finding (2026-05-28): the original implementation
  // stored only one `_heartbeatTimer` reference but had two paths
  // arming timers — the in-flight tick (when its `await heartbeat()`
  // resumes) and the poke handler. If both armed timers, only one was
  // tracked; the other ran orphaned and forked the loop into two
  // concurrent ticks. The fix: a generation counter; the in-flight
  // tick captures gen at entry and refuses to schedule on resume if
  // gen changed.
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    store: makeStore({ nodeId: 'node_ffffffffffff' }),
    logger: silentLogger(),
  });
  // heartbeat() resolves on demand so we can hold a tick mid-await.
  let resolveHeartbeat;
  let calls = 0;
  mgr.heartbeat = () => new Promise((resolve) => {
    calls++;
    resolveHeartbeat = () => resolve({ ok: true });
  });
  mgr._running = true;
  mgr._heartbeatInterval = 360_000;
  mgr._heartbeatGen = 1;
  // Kick off tick 1; it parks awaiting heartbeat().
  const tick1 = mgr._heartbeatTick(1);
  await new Promise((r) => setImmediate(r));
  // Poke while tick 1 is parked. Must clear the (null) timer, bump
  // gen, and arm a new 0ms tick under the new gen.
  mgr.pokeHeartbeatLoop();
  const genAfterPoke = mgr._heartbeatGen;
  assert.strictEqual(genAfterPoke, 2, 'poke must bump generation');

  // Resolve tick 1's heartbeat. Tick 1 should see gen mismatch and
  // refuse to schedule a follow-up timer.
  const timerBefore = mgr._heartbeatTimer;
  resolveHeartbeat();
  await tick1;
  // After tick 1 finishes, the only timer must be the poke's; tick 1
  // must not have overwritten it.
  assert.strictEqual(
    mgr._heartbeatTimer,
    timerBefore,
    'in-flight tick after poke must not arm its own timer'
  );

  mgr._running = false;
  if (mgr._heartbeatTimer) clearTimeout(mgr._heartbeatTimer);
});

test('pokeHeartbeatLoop clears the pending timer and resets consecutive failures', async () => {
  // External wake-on-event scenario: machine resumes from sleep and a
  // Hub event handler calls pokeHeartbeatLoop() so the user does not
  // wait out the prior backoff.
  const mgr = new LifecycleManager({
    hubUrl: 'http://hub.invalid',
    nodeId: 'node_eeeeeeeeeeee',
    store: makeStore(),
    logger: silentLogger(),
  });
  let heartbeatCalls = 0;
  mgr.heartbeat = async () => {
    heartbeatCalls++;
    return { ok: true };
  };
  mgr._running = true;
  mgr._heartbeatInterval = 360_000;
  mgr._consecutiveFailures = 5;
  // Seed a pending timer to simulate "currently waiting on backoff".
  mgr._heartbeatTimer = setTimeout(() => { throw new Error('should_have_been_cleared'); }, 60_000);
  if (mgr._heartbeatTimer.unref) mgr._heartbeatTimer.unref();

  mgr.pokeHeartbeatLoop();
  assert.strictEqual(mgr._consecutiveFailures, 0);
  assert.ok(mgr._heartbeatTimer, 'poke must arm a fresh 0ms timer');

  // The poke schedules with setTimeout(fn, 0). setImmediate vs setTimeout(0)
  // ordering is non-deterministic in Node, so wait briefly on real wall clock
  // for the timer queue to drain rather than racing with setImmediate.
  await new Promise((resolve) => setTimeout(resolve, 20));

  assert.ok(heartbeatCalls >= 1, `heartbeat must run promptly on poke (saw ${heartbeatCalls})`);

  mgr._running = false;
  if (mgr._heartbeatTimer) clearTimeout(mgr._heartbeatTimer);
});
