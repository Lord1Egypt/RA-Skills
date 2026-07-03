// SyncEngine loop-resilience coverage.
//
// Pre-fix shape (same root cause as the heartbeat #544 / PR #147 bug):
//   setTimeout(async () => {
//     try { await outbound.flush(); } catch { ... }
//     const nextDelay = store.countPending(...) > 0 ? 1_000 : DEFAULT;  // ← outside try
//     this._scheduleOutbound(nextDelay);                                  // ← outside try
//   })
//
// A throw from `store.countPending` (corrupt store file, FS hiccup, locked
// JSONL) escaped the setTimeout callback. Node logged the unhandled
// rejection and `_scheduleOutbound(nextDelay)` was never called. The
// outbound sync loop silently died — `engine._running` stayed true with no
// timer, no signal to the caller. These tests pin the post-fix contract:
// even an exploding `countPending` / `_isIdle` / `flush` must NOT park the
// loop.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

// Stub the lifecycle/manager AuthError before requiring the engine so the
// engine's `require('../lifecycle/manager')` resolves a minimal shim and we
// don't pull in the full manager (which expects hub creds, env, etc).
const lifecyclePath = require.resolve('../src/proxy/lifecycle/manager');
class AuthError extends Error { constructor(m) { super(m); this.name = 'AuthError'; } }
require.cache[lifecyclePath] = {
  id: lifecyclePath,
  filename: lifecyclePath,
  loaded: true,
  exports: { AuthError },
};

const { SyncEngine } = require('../src/proxy/sync/engine');
const { InboundSync, DEFAULT_POLL_INTERVAL_ACTIVE } = require('../src/proxy/sync/inbound');
const { OutboundSync } = require('../src/proxy/sync/outbound');
const hubFetchMod = require('../src/gep/hubFetch');

// Quiet logger so the deliberate error paths don't spam test output but the
// asserts on what got logged remain straightforward.
function makeQuietLogger() {
  return {
    _errors: [],
    _logs: [],
    log: (...a) => { /* noop */ },
    error: function (...a) { this._errors.push(a.join(' ')); },
    warn: () => {},
  };
}

// Minimal store stub — implementations may throw on demand to exercise the
// resilience paths. countPending defaults to a value > 0 so the loop picks
// the fast cadence and `setTimeout(_, 1_000)` arms quickly.
function makeStore(overrides = {}) {
  return Object.assign({
    countPending: () => 1,
  }, overrides);
}

function makeMailboxStore(overrides = {}) {
  const state = { node_id: 'node_aaaaaaaaaaaa' };
  return Object.assign({
    getState: (key) => (state[key] !== undefined ? state[key] : null),
    setState: (key, value) => { state[key] = value; },
    getCursor: () => null,
    setCursor: () => {},
    writeInboundBatch: () => {},
    writeInbound: () => {},
    list: () => [],
    pollOutbound: () => [],
    countPending: () => 0,
    incrementRetry: () => {},
    updateStatusBatch: () => {},
    _state: state,
  }, overrides);
}

function makeTextResponse(status, contentType, body) {
  return {
    status,
    ok: status >= 200 && status < 300,
    headers: new Headers({ 'content-type': contentType }),
    text: async () => body,
  };
}

function sensitiveHubBody() {
  return {
    raw: {
      nodeSecret: 'f'.repeat(64),
      bearer: 'Bearer ' + 'g'.repeat(64),
      token: 'tok_' + 'h'.repeat(40),
      envPath: '.env.local',
    },
    json() {
      return JSON.stringify({
        error: 'node_secret_invalid',
        node_secret: this.raw.nodeSecret,
        token: this.raw.token,
        detail: `${this.raw.bearer} from ${this.raw.envPath}`,
      });
    },
  };
}

function assertNoRawHubBodySecrets(text, raw) {
  assert.equal(text.includes(raw.nodeSecret), false, 'raw node_secret value must not be surfaced');
  assert.equal(text.includes(raw.bearer), false, 'raw Bearer token must not be surfaced');
  assert.equal(text.includes(raw.token), false, 'raw token field value must not be surfaced');
  assert.equal(text.includes(raw.envPath), false, 'raw .env path must not be surfaced');
}

async function runOneScheduledTick(schedule) {
  const realSetTimeout = global.setTimeout;
  const delays = [];
  let resolveDone;
  const done = new Promise((resolve) => { resolveDone = resolve; });
  global.setTimeout = (fn, delay) => {
    delays.push(delay);
    const timer = { unref: () => {} };
    if (delays.length === 1) {
      realSetTimeout(async () => {
        try {
          await fn();
        } finally {
          resolveDone();
        }
      }, 0);
    }
    return timer;
  };
  try {
    schedule();
    await done;
  } finally {
    global.setTimeout = realSetTimeout;
  }
  return delays;
}

async function waitFor(predicate, { timeoutMs = 2000, intervalMs = 25 } = {}) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (predicate()) return true;
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  return false;
}

describe('SyncEngine outbound loop resilience', () => {
  let engine;

  afterEach(() => {
    if (engine) try { engine.stop(); } catch (_) {}
    engine = null;
  });

  it('outbound flush throwing does NOT park the loop', async () => {
    let flushCalls = 0;
    const outbound = {
      flush: async () => {
        flushCalls++;
        throw new Error('simulated flush failure');
      },
    };
    const inbound = { pull: async () => ({ received: 0 }), ackDelivered: async () => {} };
    const logger = makeQuietLogger();

    engine = new SyncEngine({
      store: makeStore(),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger,
    });
    // Swap in our stubbed senders after construction so the real ones never
    // touch the network.
    engine.outbound = outbound;
    engine.inbound = inbound;

    engine.start();
    // After two flushes the loop must still be alive — i.e. _outTimer is
    // armed and flushCalls keeps incrementing.
    const sawMultipleFlushes = await waitFor(() => flushCalls >= 2, { timeoutMs: 3000 });
    assert.ok(sawMultipleFlushes,
      'flush must keep being called after a throw — loop must NOT silently die. flushCalls=' + flushCalls);
    assert.ok(engine._outTimer, 'outbound timer must remain armed after a flush throw');
  });

  it('outbound AuthError invokes lifecycle reAuthenticate callback', async () => {
    let reauthCalls = 0;
    const lifecycle = {
      reAuthenticate: async () => {
        reauthCalls++;
        return false;
      },
    };
    const logger = makeQuietLogger();

    engine = new SyncEngine({
      store: makeStore(),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger,
      onAuthError: () => lifecycle.reAuthenticate(),
    });
    engine.outbound = {
      flush: async () => {
        throw new AuthError('Hub 401: {"error":"node_secret_invalid"}');
      },
    };
    engine.inbound = { pull: async () => ({ received: 0 }), ackDelivered: async () => {} };
    engine._running = true;

    const delays = await runOneScheduledTick(() => engine._scheduleOutbound(0));

    assert.equal(reauthCalls, 1, 'sync AuthError must enter lifecycle reAuthenticate');
    assert.match(logger._errors.join('\n'), /auth error from outbound/);
    assert.equal(delays[0], 0);
    assert.equal(delays[1], 1_000, 'outbound loop should continue after auth handling');
  });

  it('store.countPending throwing does NOT park the loop (the #544 pattern in sync engine)', async () => {
    // After a successful flush the post-tick path calls store.countPending
    // to pick the next cadence (1s if pending > 0, else 5s). Pre-fix this
    // call was OUTSIDE the try/catch, so a throw here killed the loop.
    // Post-fix: the throw is caught and the loop falls back to the default
    // 5s cadence. Asserting the timer is re-armed after the first tick is
    // the property we actually need.
    let flushCalls = 0;
    let countPendingCalls = 0;
    const outbound = {
      flush: async () => {
        flushCalls++;
        return { sent: 0 };
      },
    };
    const inbound = { pull: async () => ({ received: 0 }), ackDelivered: async () => {} };
    const store = {
      countPending: () => {
        countPendingCalls++;
        throw new Error('simulated store corruption (countPending exploded)');
      },
    };
    const logger = makeQuietLogger();

    engine = new SyncEngine({
      store,
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger,
    });
    engine.outbound = outbound;
    engine.inbound = inbound;
    const initialOutTimer = engine._outTimer;

    engine.start();

    const sawFlushAndCount = await waitFor(
      () => flushCalls >= 1 && countPendingCalls >= 1,
      { timeoutMs: 3000 },
    );
    assert.ok(sawFlushAndCount,
      'flush + countPending must each fire at least once within 3s. flushCalls=' +
      flushCalls + ', countPendingCalls=' + countPendingCalls);
    // Let the finally block run one event-loop turn to re-arm the timer.
    await new Promise((r) => setTimeout(r, 50));
    assert.ok(engine._outTimer,
      'outbound timer must be RE-ARMED after countPending throws (the #544-class fix)');
    assert.notEqual(engine._outTimer, initialOutTimer,
      'a new timer must be installed (the rescheduled one), not the original');

    // Logger must have recorded the countPending failure (non-fatal).
    const sawCountPendingError = logger._errors.some((e) => e.includes('countPending'));
    assert.ok(sawCountPendingError,
      'countPending failure must be logged (non-fatal) — errors=' + JSON.stringify(logger._errors));
  });
});

describe('SyncEngine inbound loop resilience', () => {
  let engine;

  afterEach(() => {
    if (engine) try { engine.stop(); } catch (_) {}
    engine = null;
  });

  it('inbound pull throwing does NOT park the loop', async () => {
    // Inbound cadence is DEFAULT_POLL_INTERVAL_ACTIVE = 10s, so waiting for
    // a second call would make the test very slow. Instead: wait for the
    // first pull (1s after start()), wait one event-loop turn for the
    // setTimeout callback to fully resolve through `finally`, then assert
    // the next timer is armed. That's the property we actually care about
    // — the loop didn't die.
    let pullCalls = 0;
    const inbound = {
      pull: async () => {
        pullCalls++;
        throw new Error('simulated inbound pull failure');
      },
      ackDelivered: async () => {},
    };
    const outbound = { flush: async () => ({ sent: 0 }) };
    const logger = makeQuietLogger();

    engine = new SyncEngine({
      store: makeStore(),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger,
    });
    engine.outbound = outbound;
    engine.inbound = inbound;
    const initialInTimer = engine._inTimer;

    engine.start();

    const sawPull = await waitFor(() => pullCalls >= 1, { timeoutMs: 3000 });
    assert.ok(sawPull, 'first pull must fire within 3s of start(). pullCalls=' + pullCalls);
    // The throw resolves the setTimeout callback; let the finally block
    // run one event-loop turn so it can re-arm the timer.
    await new Promise((r) => setTimeout(r, 50));
    assert.ok(engine._inTimer, 'inbound timer must be RE-ARMED after a pull throw');
    assert.notEqual(engine._inTimer, initialInTimer,
      'a new timer must have been created (the rescheduled one), not the original');
  });

  it('inbound AuthError invokes lifecycle reAuthenticate callback', async () => {
    let reauthCalls = 0;
    const lifecycle = {
      reAuthenticate: async () => {
        reauthCalls++;
        return false;
      },
    };
    const logger = makeQuietLogger();

    engine = new SyncEngine({
      store: makeStore(),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger,
      onAuthError: () => lifecycle.reAuthenticate(),
    });
    engine.outbound = { flush: async () => ({ sent: 0 }) };
    engine.inbound = {
      pull: async () => {
        throw new AuthError('Hub 403: {"error":"node_secret_invalid"}');
      },
      ackDelivered: async () => {
        throw new Error('ack should not run after inbound auth failure');
      },
    };
    engine._running = true;

    const delays = await runOneScheduledTick(() => engine._scheduleInbound(0));

    assert.equal(reauthCalls, 1, 'inbound AuthError must enter lifecycle reAuthenticate');
    assert.match(logger._errors.join('\n'), /auth error from inbound/);
    assert.equal(delays[0], 0);
    assert.equal(delays[1], DEFAULT_POLL_INTERVAL_ACTIVE, 'inbound loop should continue after auth handling');
  });

  it('onInboundReceived callback throwing does NOT park the loop', async () => {
    // Same shape as above: assert the timer is re-armed after one tick
    // rather than waiting for a full 10s second cycle.
    let pullCalls = 0;
    let callbackCalls = 0;
    const inbound = {
      pull: async () => {
        pullCalls++;
        return { received: 1 };
      },
      ackDelivered: async () => {},
    };
    const outbound = { flush: async () => ({ sent: 0 }) };
    const logger = makeQuietLogger();

    engine = new SyncEngine({
      store: makeStore(),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger,
      onInboundReceived: () => {
        callbackCalls++;
        throw new Error('user callback exploded');
      },
    });
    engine.outbound = outbound;
    engine.inbound = inbound;

    engine.start();

    const sawPullAndCallback = await waitFor(() => pullCalls >= 1 && callbackCalls >= 1, { timeoutMs: 3000 });
    assert.ok(sawPullAndCallback,
      'first pull + callback must fire within 3s. pullCalls=' + pullCalls + ', callbackCalls=' + callbackCalls);
    await new Promise((r) => setTimeout(r, 50));
    assert.ok(engine._inTimer,
      'inbound timer must be re-armed even when the user callback throws');
  });
});

describe('SyncEngine stop() still wins over the resilience layer', () => {
  it('stop() prevents the reschedule even when called mid-await of the in-flight tick', async () => {
    // Bugbot PR #158: the previous shape of this test waited 30ms then
    // called stop() — but the first timer is armed at 500ms, so stop()
    // ran BEFORE the timer fired and `clearTimeout` cancelled it. The
    // setTimeout callback (which holds the `if (this._running)` guard we
    // actually want to validate) never ran. The test passed even if the
    // guard was removed.
    //
    // The contract the resilience layer must uphold: when stop() runs
    // WHILE a tick is mid-await, the in-flight flush still resolves
    // naturally, but `finally`'s `if (this._running)` gate prevents the
    // next timer from being armed. No further flushes happen.
    let flushStarted = 0;
    let flushFinished = 0;
    const outbound = {
      flush: async () => {
        flushStarted++;
        // Long enough that we can definitely call stop() between
        // flushStarted++ and the resolve below.
        await new Promise((r) => setTimeout(r, 300));
        flushFinished++;
        return { sent: 0 };
      },
    };
    const inbound = { pull: async () => ({ received: 0 }), ackDelivered: async () => {} };
    const logger = makeQuietLogger();

    const engine = new SyncEngine({
      store: makeStore(),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger,
    });
    engine.outbound = outbound;
    engine.inbound = inbound;

    engine.start();
    // Wait until the FIRST timer has fired and flush has started (~500ms).
    const flushIsRunning = await waitFor(() => flushStarted >= 1, { timeoutMs: 2000 });
    assert.ok(flushIsRunning, 'first flush must start within 2s of engine.start()');
    // Sanity check: we should be MID-AWAIT (started but not finished yet),
    // otherwise the test is racy and we'd be back to the pre-fix shape
    // where stop() just cancels a not-yet-fired timer.
    assert.equal(flushFinished, 0,
      'flush must still be mid-await when stop() runs — otherwise the test ' +
      'is not exercising the finally-guard path. flushStarted=' + flushStarted);

    engine.stop();
    // Let the in-flight flush resolve through `finally`. The guard is
    // what we are testing: stop() flipped _running=false, so finally
    // must NOT reschedule.
    await new Promise((r) => setTimeout(r, 600));
    assert.equal(flushFinished, 1,
      'in-flight flush must still resolve naturally after stop()');
    assert.equal(engine._outTimer, null,
      'outbound timer must NOT be re-armed by the finally block when stop() flipped _running=false');
    assert.equal(engine._inTimer, null,
      'inbound timer must be cleared by stop() too');

    // Wait beyond the default 5s cadence to prove no rogue timer is
    // hiding. If the finally guard were broken, a second flush would
    // fire here.
    const startedAfterStop = flushStarted;
    await new Promise((r) => setTimeout(r, 1000));
    assert.equal(flushStarted, startedAfterStop,
      'no further flushes after stop() — got ' + flushStarted + ' vs at-stop=' + startedAfterStop);
  });
});

describe('SyncEngine Hub non-API response backoff', () => {
  let engine;

  afterEach(() => {
    hubFetchMod._setFetchImplForTest(null);
    if (engine) {
      engine._running = false;
      engine._outTimer = null;
      engine._inTimer = null;
      try { engine.stop(); } catch (_) {}
    }
    engine = null;
  });

  it('InboundSync treats HTML 403 as hub unreachable without throwing AuthError', async () => {
    hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
      403,
      'text/html',
      '<!DOCTYPE html><title>Cloudflare</title><body>Forbidden</body>',
    ));
    const logger = makeQuietLogger();
    const inbound = new InboundSync({
      store: makeMailboxStore(),
      hubUrl: 'https://hub.example',
      getHeaders: () => ({}),
      logger,
    });

    const result = await inbound.pull();

    assert.equal(result.hubUnreachable, true);
    assert.equal(result.error, 'hub_unreachable');
    assert.ok(result.retryAfterMs >= 60_000);
    assert.deepEqual(logger._errors, []);
  });

  it('InboundSync skips oversized inbound rows and advances the cursor', async () => {
    const maxBytes = 512;
    const savedMax = process.env.EVOMAP_MAILBOX_MAX_LINE_BYTES;
    process.env.EVOMAP_MAILBOX_MAX_LINE_BYTES = String(maxBytes);
    hubFetchMod._setFetchImplForTest(async () => ({
      status: 200,
      ok: true,
      headers: new Headers({ 'content-type': 'application/json' }),
      text: async () => JSON.stringify({
        next_cursor: 'cursor-after-oversized',
        messages: [
          {
            id: 'in-ok-before',
            type: 'hub_event',
            payload: { text: 'before' },
            priority: 'normal',
          },
          {
            id: 'in-too-large',
            type: 'hub_event',
            payload: { text: 'x'.repeat(maxBytes * 2) },
            priority: 'normal',
          },
          {
            id: 'in-ok-after',
            type: 'hub_event',
            payload: { text: 'after' },
            priority: 'normal',
          },
        ],
      }),
    }));

    const { MailboxStore } = require('../src/proxy/mailbox/store');
    const fs = require('fs');
    const os = require('os');
    const path = require('path');
    const dataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'inbound-oversized-'));
    const store = new MailboxStore(dataDir);
    const logger = makeQuietLogger();
    const inbound = new InboundSync({
      store,
      hubUrl: 'https://hub.example',
      getHeaders: () => ({}),
      logger,
    });

    try {
      store.setState('node_id', 'node_aaaaaaaaaaaa');

      const result = await inbound.pull();

      assert.equal(result.received, 2);
      assert.equal(result.dropped, 1);
      assert.equal(result.cursor, 'cursor-after-oversized');
      assert.equal(store.getCursor('evomap-hub:inbound_cursor'), 'cursor-after-oversized');
      assert.ok(store.getById('in-ok-before'));
      assert.ok(store.getById('in-ok-after'));
      assert.equal(store.getById('in-too-large'), null);
      assert.equal(logger._errors.length, 0);
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch (_) {}
      if (savedMax === undefined) delete process.env.EVOMAP_MAILBOX_MAX_LINE_BYTES;
      else process.env.EVOMAP_MAILBOX_MAX_LINE_BYTES = savedMax;
    }
  });

  it('InboundSync redacts JSON auth response bodies before surfacing AuthError', async () => {
    const body = sensitiveHubBody();
    hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
      403,
      'application/json',
      body.json(),
    ));
    const inbound = new InboundSync({
      store: makeMailboxStore(),
      hubUrl: 'https://hub.example',
      getHeaders: () => ({}),
      logger: makeQuietLogger(),
    });

    await assert.rejects(
      () => inbound.pull(),
      (err) => {
        assert.equal(err.name, 'AuthError');
        assert.match(err.message, /"node_secret":"\[REDACTED\]"/);
        assertNoRawHubBodySecrets(err.message, body.raw);
        return true;
      },
    );
  });

  it('OutboundSync redacts JSON auth response bodies before surfacing AuthError', async () => {
    const body = sensitiveHubBody();
    hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
      401,
      'application/json',
      body.json(),
    ));
    const outbound = new OutboundSync({
      store: makeMailboxStore({
        pollOutbound: () => [{
          id: 'msg_1',
          type: 'asset_submit',
          payload: { ok: true },
          priority: 'normal',
          ref_id: null,
          created_at: new Date().toISOString(),
          retry_count: 0,
        }],
      }),
      hubUrl: 'https://hub.example',
      getHeaders: () => ({}),
      logger: makeQuietLogger(),
    });

    await assert.rejects(
      () => outbound.flush(),
      (err) => {
        assert.equal(err.name, 'AuthError');
        assert.match(err.message, /"node_secret":"\[REDACTED\]"/);
        assertNoRawHubBodySecrets(err.message, body.raw);
        return true;
      },
    );
  });

  it('OutboundSync does not increment retry counters for HTML 504 hub outages', async () => {
    hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
      504,
      'text/html',
      '<!DOCTYPE html><title>Gateway timeout</title>',
    ));
    let retryIncrements = 0;
    const outbound = new OutboundSync({
      store: makeMailboxStore({
        pollOutbound: () => [{
          id: 'msg_1',
          type: 'asset_submit',
          payload: { ok: true },
          priority: 'normal',
          ref_id: null,
          created_at: new Date().toISOString(),
          retry_count: 0,
        }],
        incrementRetry: () => { retryIncrements++; },
      }),
      hubUrl: 'https://hub.example',
      getHeaders: () => ({}),
      logger: makeQuietLogger(),
    });

    const result = await outbound.flush();

    assert.equal(result.hubUnreachable, true);
    assert.equal(result.error, 'hub_unreachable');
    assert.ok(result.retryAfterMs >= 60_000);
    assert.equal(retryIncrements, 0);
  });

  it('OutboundSync backs off on successful HTML non-API responses', async () => {
    hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
      200,
      'text/html; charset=utf-8',
      '<!DOCTYPE html><title>Captive portal</title>',
    ));
    let retryIncrements = 0;
    const outbound = new OutboundSync({
      store: makeMailboxStore({
        pollOutbound: () => [{
          id: 'msg_1',
          type: 'asset_submit',
          payload: { ok: true },
          priority: 'normal',
          ref_id: null,
          created_at: new Date().toISOString(),
          retry_count: 0,
        }],
        incrementRetry: () => { retryIncrements++; },
      }),
      hubUrl: 'https://hub.example',
      getHeaders: () => ({}),
      logger: makeQuietLogger(),
    });

    const result = await outbound.flush();

    assert.equal(result.hubUnreachable, true);
    assert.equal(result.error, 'hub_unreachable');
    assert.ok(result.retryAfterMs >= 60_000);
    assert.equal(retryIncrements, 0);
  });

  it('OutboundSync backs off on successful text/plain non-API responses', async () => {
    hubFetchMod._setFetchImplForTest(async () => makeTextResponse(
      200,
      'text/plain; charset=utf-8',
      'edge gateway maintenance page',
    ));
    let retryIncrements = 0;
    const outbound = new OutboundSync({
      store: makeMailboxStore({
        pollOutbound: () => [{
          id: 'msg_1',
          type: 'asset_submit',
          payload: { ok: true },
          priority: 'normal',
          ref_id: null,
          created_at: new Date().toISOString(),
          retry_count: 0,
        }],
        incrementRetry: () => { retryIncrements++; },
      }),
      hubUrl: 'https://hub.example',
      getHeaders: () => ({}),
      logger: makeQuietLogger(),
    });

    const result = await outbound.flush();

    assert.equal(result.hubUnreachable, true);
    assert.equal(result.error, 'hub_unreachable');
    assert.ok(result.retryAfterMs >= 60_000);
    assert.equal(retryIncrements, 0);
  });

  it('inbound loop schedules returned hub retryAfterMs and skips ack', async () => {
    let ackCalls = 0;
    engine = new SyncEngine({
      store: makeStore(),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger: makeQuietLogger(),
    });
    engine.outbound = { flush: async () => ({ sent: 0 }) };
    engine.inbound = {
      pull: async () => ({ received: 0, hubUnreachable: true, retryAfterMs: 61_000 }),
      ackDelivered: async () => {
        ackCalls++;
        return { acked: 0 };
      },
    };
    engine._running = true;

    const delays = await runOneScheduledTick(() => engine._scheduleInbound(0));

    assert.equal(delays[0], 0);
    assert.equal(delays[1], 61_000);
    assert.equal(ackCalls, 0);
  });

  it('outbound loop schedules returned hub retryAfterMs without polling countPending', async () => {
    let countPendingCalls = 0;
    engine = new SyncEngine({
      store: makeStore({
        countPending: () => {
          countPendingCalls++;
          return 1;
        },
      }),
      hubUrl: 'https://hub.example/test',
      getHeaders: () => ({}),
      logger: makeQuietLogger(),
    });
    engine.outbound = { flush: async () => ({ sent: 0, hubUnreachable: true, retryAfterMs: 62_000 }) };
    engine.inbound = { pull: async () => ({ received: 0 }), ackDelivered: async () => ({ acked: 0 }) };
    engine._running = true;

    const delays = await runOneScheduledTick(() => engine._scheduleOutbound(0));

    assert.equal(delays[0], 0);
    assert.equal(delays[1], 62_000);
    assert.equal(countPendingCalls, 0);
  });
});
