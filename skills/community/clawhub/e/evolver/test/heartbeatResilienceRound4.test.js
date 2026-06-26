// Regression coverage for the round-4 audit (2026-05-28) heartbeat
// resilience fixes. Each test pins exactly one fix. The bugs being
// covered:
//
//   1. Hub-side response-cache poisoning loop. When the hub caches an
//      unknown_node payload for 7 minutes, the client previously
//      re-helloed on every tick, racked up ~14 hellos in the cache TTL,
//      and tripped the hub's per-IP hello rate limit -- locking the node
//      out for hours. The round-4 guard counts consecutive unknown_node
//      responses where re-hello succeeded and installs a > cache-TTL
//      backoff once the threshold is hit, breaking the loop instead of
//      hammering the hub.
//
//   2. The resend_hello branch inside sendHeartbeat()'s response chain
//      previously did `sendHelloToHub().then(...).catch(...)` with no
//      sync-throw guard. If sendHelloToHub() threw SYNCHRONOUSLY
//      (post-wake module cache poisoning, crypto.randomUUID failing on a
//      still-asleep entropy pool, a bad require), the exception escaped
//      the .catch() and bubbled up the heartbeat promise chain, dropping
//      available_work / overdue tasks / shared knowledge updates from the
//      same payload. Wrap in try/catch so a sync throw never breaks the
//      rest of the tick.
//
//   3. evolver_loop.log was only utimesSync()'d on each successful tick,
//      so it stayed 0 bytes for the entire process lifetime. Rounds 1-3
//      had to do source-code audits to RCA the user-reported "evolver
//      dead after idle" symptom because there was no log evidence on
//      disk. Round-4 appends a one-line JSON record per tick.
//
//   4. getHeartbeatStats() did not expose reauthBackoffUntil /
//      consecutiveReauthFailures / consecutiveUnknownNodeAfterHello, so
//      ops tooling that polled stats saw `running: true, lastTickAt:
//      <recent>` even when the loop was silent for 30 min waiting on a
//      reauth backoff. Round-4 surfaces all penalty-state fields.

const { describe, it, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const os = require('os');

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
  sendHeartbeat,
  getHeartbeatStats,
} = a2a;
const {
  _resetHeartbeatStateForTesting,
  _setHeartbeatStateForTesting,
  _getHeartbeatInternalsForTesting,
} = a2a._testing;

function nextTick() {
  return new Promise((r) => setImmediate(r));
}
async function settle() {
  await nextTick(); await nextTick(); await nextTick(); await nextTick();
}

function makeMultiFetch(responses) {
  // Returns a fetch stub that returns responses[i] for the i-th call,
  // staying on the last one once exhausted.
  let i = 0;
  return async function (_url) {
    const r = responses[Math.min(i, responses.length - 1)];
    i++;
    return {
      ok: r.ok !== false,
      status: r.status || 200,
      json: async () => r.body || {},
      text: async () => JSON.stringify(r.body || {}),
    };
  };
}

describe('round-4: unknown_node cache-poisoning loop installs backoff after threshold', () => {
  let origFetch;
  let origHubUrl;
  let origAllow;
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

  it('counter increments on unknown_node + hello-ok and arms backoff at threshold', async () => {
    // Each heartbeat returns unknown_node; each hello succeeds. Repeat
    // until the counter crosses the threshold and the backoff arms.
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };

    // Tick 1: first unknown_node -> hello ok -> counter=1. Round-5 adds
    // a small hello-recovery delay so the next tick gives DB replication
    // time to catch up (avoiding the same cached unknown_node ~30s later).
    // The full 8-min cache backoff still does NOT arm until the threshold.
    await sendHeartbeat();
    await settle();
    const after1 = _getHeartbeatInternalsForTesting();
    assert.equal(after1.consecutiveUnknownNodeAfterHello, 1,
      'first unknown_node after a successful re-hello must increment the counter');
    assert.ok(after1.pendingRescheduleDelayMs < 7 * 60_000,
      'cache-poisoning backoff must NOT arm before threshold; got ' +
      after1.pendingRescheduleDelayMs);

    // Tick 2: same response -> counter=2 (the threshold) -> backoff arms.
    await sendHeartbeat();
    await settle();
    const after2 = _getHeartbeatInternalsForTesting();
    assert.equal(after2.consecutiveUnknownNodeAfterHello, 2,
      'second unknown_node after re-hello brings the counter to threshold');
    assert.ok(after2.pendingRescheduleDelayMs >= 7 * 60_000,
      'backoff must be at least the hub cache TTL (420s) -- got ' +
      after2.pendingRescheduleDelayMs + 'ms');
  });

  it('counter resets on the first ok heartbeat', async () => {
    // First tick: unknown_node + hello ok (counter -> 1).
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };
    await sendHeartbeat();
    await settle();
    assert.equal(_getHeartbeatInternalsForTesting().consecutiveUnknownNodeAfterHello, 1);

    // Second tick: hub cache cleared, returns ok. Counter must reset.
    global.fetch = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });
    await sendHeartbeat();
    await settle();
    assert.equal(_getHeartbeatInternalsForTesting().consecutiveUnknownNodeAfterHello, 0,
      'a single ok heartbeat must drop the loop counter back to zero');
  });

  it('a failed re-hello installs the 5-min backoff and increments the failure counter (round-8 §21.1)', async () => {
    // Round-8 corrected the round-4 contract this test originally asserted.
    // Pre-round-7 the unknown_node hello-fail branch reset
    // _consecutiveUnknownNodeAfterHello = 0 with the rationale "rate_limited /
    // reauth-backoff paths take over." That handoff never happened in
    // practice: the round-7 audit found the soft-error allow-list
    // (which would have kept _heartbeatConsecutiveFailures climbing
    // so the drift detector could drive recovery) is unreachable from
    // this code path -- the unknown_node branch returns early from the
    // outer .then(data) callback. Round-7's attempted fix returned
    // {ok:false, error:'hello_failed_after_unknown_node'} and added
    // that key to the allow-list, but the allow-list still sat AFTER
    // the early return so the increment never happened. Round-8
    // increments inline AND preserves _consecutiveUnknownNodeAfterHello
    // (so the next unknown_node response can re-arm the full 8-min
    // cache backoff immediately rather than restart from 0), AND sets
    // _unknownNodeBackoffUntil = now+5min so pokeHeartbeat's round-6
    // gate protects the wait window.
    _setHeartbeatStateForTesting({ running: true, intervalMs: 60_000 });
    // First cycle: hello ok -> counter=1.
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };
    await sendHeartbeat();
    await settle();
    assert.equal(_getHeartbeatInternalsForTesting().consecutiveUnknownNodeAfterHello, 1);
    const failuresBefore = _getHeartbeatInternalsForTesting().consecutiveFailures;

    // Second cycle: hello fails. Round-8 expectations: counter preserved,
    // failure counter climbs, 5-min backoff armed.
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: false, status: 500, json: async () => ({ ok: false, error: 'hub_down' }), text: async () => 'down' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };
    const t0 = Date.now();
    await sendHeartbeat();
    await settle();
    const after = _getHeartbeatInternalsForTesting();
    assert.ok(
      after.consecutiveUnknownNodeAfterHello >= 1,
      'round-8: counter must be preserved (or incremented) on hello failure, not reset to 0'
    );
    assert.ok(
      after.consecutiveFailures > failuresBefore,
      'round-8: _heartbeatConsecutiveFailures must climb so the drift detector can drive recovery'
    );
    assert.ok(
      after.unknownNodeBackoffUntil >= t0 + 4 * 60_000,
      'round-8: 5-min backoff must be installed (got ' + (after.unknownNodeBackoffUntil - t0) + 'ms ahead)'
    );
  });

  it('_resetHeartbeatStateForTesting() clears the loop counter', async () => {
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'unknown_node' }), text: async () => '' };
    };
    await sendHeartbeat();
    await settle();
    assert.equal(_getHeartbeatInternalsForTesting().consecutiveUnknownNodeAfterHello, 1,
      'precondition: counter is non-zero');
    _resetHeartbeatStateForTesting();
    assert.equal(_getHeartbeatInternalsForTesting().consecutiveUnknownNodeAfterHello, 0,
      'reset hook must clear the round-4 counter for cross-test isolation');
  });
});

describe('round-4: resend_hello sync-throw guard', () => {
  let origFetch;
  let origHubUrl;
  let origAllow;
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

  it('a synchronous throw from sendHelloToHub() is caught and does not break the rest of the tick', async () => {
    // The fix this test pins: the try/catch around sendHelloToHub() inside
    // the resend_hello branch (see a2aProtocol.js around L1859-1869). The
    // earlier version of this test stubbed global.fetch to a happy 200 and
    // only asserted result.ok -- the try/catch arm was NEVER exercised, so
    // the test passed whether or not the guard existed.
    //
    // To force the sync-throw arm we make crypto.randomUUID() throw on its
    // SECOND call: the first call is consumed by sendHeartbeat() ->
    // buildHubHeaders() before the response is processed; the second
    // happens inside sendHelloToHub() -> buildHubHeaders() AFTER the
    // resend_hello branch is entered. This mirrors the production-bug
    // class the round-4 guard was added for ("post-wake entropy pool not
    // ready" / "crypto.randomUUID failing on a still-asleep host"), and
    // crucially the throw inside buildHubHeaders escapes out of
    // sendHelloToHub SYNCHRONOUSLY (it happens during argument evaluation
    // for hubFetch(), before any .then() chain is set up).
    let helloFetchCalls = 0;
    let heartbeatFetchCalls = 0;
    global.fetch = async (url) => {
      const u = String(url || '');
      if (u.indexOf('/a2a/hello') !== -1) {
        helloFetchCalls++;
        return { ok: true, status: 200, json: async () => ({ ok: true, status: 'ok' }), text: async () => '' };
      }
      heartbeatFetchCalls++;
      return {
        ok: true, status: 200,
        json: async () => ({
          status: 'ok',
          resend_hello: true,
          resend_reason: 'test_sync_throw',
          // Include available_work so the assertion below can prove the
          // rest of the .then(data) body kept processing after the sync
          // throw: pre-fix, the throw escapes the resend_hello block and
          // the whole .then(data) callback is interrupted -- available_work
          // is never recorded and the heartbeat is counted as a failure.
          available_work: [{ id: 'w_round4_sync_throw', kind: 'probe' }],
        }),
        text: async () => '',
      };
    };

    const crypto = require('crypto');
    const origRandomUUID = crypto.randomUUID.bind(crypto);
    let randomUUIDCalls = 0;
    crypto.randomUUID = function () {
      randomUUIDCalls++;
      if (randomUUIDCalls >= 2) {
        throw new Error('simulated post-wake entropy_pool_not_ready');
      }
      return origRandomUUID();
    };

    const beforeFailed = _getHeartbeatInternalsForTesting().totalFailed;
    let result;
    let threw = null;
    try {
      try {
        result = await sendHeartbeat();
      } catch (e) {
        threw = e;
      }
      await settle();
    } finally {
      crypto.randomUUID = origRandomUUID;
    }

    assert.equal(threw, null,
      'sendHeartbeat must not reject/throw when sendHelloToHub() throws synchronously; ' +
      'the round-4 try/catch (a2aProtocol.js ~L1859-1869) is what catches it. ' +
      'threw=' + (threw && threw.message));
    assert.ok(result && result.ok === true,
      'resend_hello sync throw must NOT degrade the tick into a failure: with the ' +
      'round-4 guard the outer .then(data) keeps processing the rest of the payload. ' +
      'Pre-fix, the sync throw escapes the resend_hello block, the outer .catch(err) ' +
      'counts the tick as a failure, and available_work / overdue_tasks are dropped. ' +
      'result=' + JSON.stringify(result));
    assert.equal(_getHeartbeatInternalsForTesting().totalFailed, beforeFailed,
      'sync throw inside resend_hello must NOT bump totalFailed -- pre-fix it did');
    assert.ok(randomUUIDCalls >= 2,
      'precondition: the SECOND randomUUID call (inside sendHelloToHub->buildHubHeaders) ' +
      'must have fired to actually exercise the sync-throw arm; calls=' + randomUUIDCalls);
    assert.equal(helloFetchCalls, 0,
      'precondition: sendHelloToHub must have thrown BEFORE issuing hubFetch ' +
      '(headers are built sync as part of the hubFetch argument list)');
    assert.ok(heartbeatFetchCalls >= 1,
      'precondition: the initial heartbeat hubFetch must have fired so the ' +
      'resend_hello response could be processed');
  });
});

describe('round-4: evolver_loop.log gets appended content per successful tick', () => {
  // Reuse the same path-injection pattern as the existing
  // a2aProtocol.test.js heartbeat-log tests: EVOLVER_LOGS_DIR drives
  // getEvolverLogPath().
  let tmpDir;
  let origFetch;
  let origHubUrl;
  let origAllow;
  let origLogsDir;

  beforeEach(() => {
    _resetHeartbeatStateForTesting();
    origFetch = global.fetch;
    origHubUrl = process.env.A2A_HUB_URL;
    origAllow = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    origLogsDir = process.env.EVOLVER_LOGS_DIR;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-round4-log-'));
    process.env.EVOLVER_LOGS_DIR = tmpDir;
  });
  afterEach(() => {
    global.fetch = origFetch;
    if (origHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = origHubUrl;
    if (origAllow === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = origAllow;
    if (origLogsDir === undefined) delete process.env.EVOLVER_LOGS_DIR;
    else process.env.EVOLVER_LOGS_DIR = origLogsDir;
    fs.rmSync(tmpDir, { recursive: true, force: true });
    _resetHeartbeatStateForTesting();
  });

  it('writes a non-empty JSON line on each successful heartbeat', async () => {
    global.fetch = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });

    await sendHeartbeat();
    await settle();

    const logPath = path.join(tmpDir, 'evolver_loop.log');
    assert.ok(fs.existsSync(logPath), 'log file should be created');
    const content = fs.readFileSync(logPath, 'utf8');
    assert.ok(content.length > 0,
      'round-4 fix: log file must have CONTENT, not just an updated mtime');
    const lines = content.split('\n').filter(Boolean);
    assert.ok(lines.length >= 1, 'at least one tick line should be appended');
    const parsed = JSON.parse(lines[0]);
    assert.equal(parsed.type, 'heartbeat_ok');
    assert.equal(typeof parsed.ts, 'string');
    assert.equal(typeof parsed.tick, 'number');
  });

  it('appends additional lines per subsequent tick (file is not truncated)', async () => {
    global.fetch = async () => ({
      ok: true, status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });

    await sendHeartbeat();
    await settle();
    await sendHeartbeat();
    await settle();

    const logPath = path.join(tmpDir, 'evolver_loop.log');
    const content = fs.readFileSync(logPath, 'utf8');
    const lines = content.split('\n').filter(Boolean);
    assert.ok(lines.length >= 2,
      'two successful ticks must produce at least two appended lines (got ' +
      lines.length + ')');
  });
});

describe('round-4: getHeartbeatStats() exposes penalty-state fields', () => {
  beforeEach(() => { _resetHeartbeatStateForTesting(); });
  afterEach(() => { _resetHeartbeatStateForTesting(); });

  it('includes reauthBackoffUntil, consecutiveReauthFailures, consecutiveUnknownNodeAfterHello, lastTickAt', () => {
    const stats = getHeartbeatStats();
    assert.ok(Object.prototype.hasOwnProperty.call(stats, 'reauthBackoffUntil'),
      'reauthBackoffUntil must be in stats so ops can see "alive but in 30min backoff"');
    assert.ok(Object.prototype.hasOwnProperty.call(stats, 'consecutiveReauthFailures'),
      'consecutiveReauthFailures must be in stats for the same reason');
    assert.ok(Object.prototype.hasOwnProperty.call(stats, 'consecutiveUnknownNodeAfterHello'),
      'consecutiveUnknownNodeAfterHello must be in stats so ops can detect cache-poisoning');
    assert.ok(Object.prototype.hasOwnProperty.call(stats, 'lastTickAt'),
      'lastTickAt must be in stats for liveness checks');
  });
});
