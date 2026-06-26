'use strict';

// Regression coverage for PR #188 H1 bug: the proxy LifecycleManager
// heartbeat MUST drive executeForceUpdate when:
//   (a) hub returns 200 with `data.force_update`, OR
//   (b) hub returns 426 with body `{ error: 'evolver_min_version_required',
//        force_update: {...} }` (see hub src/routes/a2a/_middleware.js).
//
// Before the fix:
//   - The 200+force_update path was simply not inspected at all by the
//     proxy heartbeat, so pure proxy-mode nodes (EVOMAP_PROXY=1) never
//     attempted any forced upgrade and never produced an
//     EvolverUpgradeAttempt row.
//   - The 426 path funnelled into a generic `http_426` error and returned
//     without parsing the body, so the upgrade directive carried by the
//     error envelope was silently dropped.
//
// The fix mirrors `_maybeTriggerForceUpdateFromHeartbeat` from
// src/gep/a2aProtocol.js: in-flight lock + cooldown gate, microtask
// kick-off, persists outcome via reportForceUpdateOutcome so the next
// heartbeat carries it as body.last_update.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

// hubFetch refuses to route through global.fetch for https://example.test
// unless EVOMAP_HUB_ALLOW_INSECURE=1. Stub global.fetch from each test.
const _origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';

// A2A_NODE_SECRET is required by _buildHeaders.
if (!process.env.A2A_NODE_SECRET) {
  process.env.A2A_NODE_SECRET = 'a'.repeat(64);
}

// Cooldown env: pin to 0 so back-to-back assertions inside one process do
// not get blocked by the 15-min default. Each test resets the in-flight
// state explicitly through the _testing hook.
const _origCooldown = process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS;
process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '0';

// Isolate the on-disk state path from the developer's real ~/.evomap.
const _origEvolverHome = process.env.EVOLVER_HOME;
const _tmpEvolverHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-lu-fu-'));
process.env.EVOLVER_HOME = _tmpEvolverHome;

// Cache-swap the forceUpdate module BEFORE requiring manager.js so the
// in-test executeForceUpdate spy is what manager.js's
// _maybeTriggerForceUpdateFromHeartbeat picks up. Matches the pattern in
// test/forceUpdateHeartbeat.test.js. process.exit is also stubbed below so
// a "success" path does not actually kill the test runner.
const forceUpdatePath = require.resolve('../src/forceUpdate');
let executeForceUpdateCalls = [];
let executeForceUpdateReturn = false;
let executeForceUpdateReturns = [];
let executeForceUpdateThrow = null;
// FORCE_UPDATE_NOOP / FORCE_UPDATE_BUSY must be stable identities that
// the manager picks up via `mod.FORCE_UPDATE_NOOP === result` /
// `mod.FORCE_UPDATE_BUSY === result`. We expose the same Symbol values
// so a test can opt the spy into the no-op or busy sentinel path.
const SPY_NOOP = Symbol('SPY_FORCE_UPDATE_NOOP');
const SPY_BUSY = Symbol('SPY_FORCE_UPDATE_BUSY');
require.cache[forceUpdatePath] = {
  id: forceUpdatePath,
  filename: forceUpdatePath,
  loaded: true,
  exports: {
    executeForceUpdate: function (fu) {
      executeForceUpdateCalls.push(fu);
      if (executeForceUpdateThrow) throw executeForceUpdateThrow;
      if (executeForceUpdateReturns.length > 0) return executeForceUpdateReturns.shift();
      return executeForceUpdateReturn;
    },
    FORCE_UPDATE_NOOP: SPY_NOOP,
    FORCE_UPDATE_BUSY: SPY_BUSY,
  },
};

const { LifecycleManager, _testing } = require('../src/proxy/lifecycle/manager');
const a2aProtocol = require('../src/gep/a2aProtocol');
const {
  _getLastUpdateStatePathForTesting,
  _resetLastUpdateStateForTesting,
  _readPendingLastUpdateForTesting,
} = a2aProtocol._testing;
const { _resetProxyForceUpdateStateForTesting } = _testing;

// Stub process.exit so a true-return executeForceUpdate path can be
// exercised without tearing down the test runner. exitCalls is reset
// per-test in the harness below.
let exitCalls = [];
const _origProcessExit = process.exit;
process.exit = function (code) { exitCalls.push(code); };

test.after(() => {
  process.exit = _origProcessExit;
  if (_origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  else process.env.EVOMAP_HUB_ALLOW_INSECURE = _origInsecure;
  if (_origCooldown === undefined) delete process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS;
  else process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = _origCooldown;
  if (_origEvolverHome === undefined) delete process.env.EVOLVER_HOME;
  else process.env.EVOLVER_HOME = _origEvolverHome;
  try { fs.rmSync(_tmpEvolverHome, { recursive: true, force: true }); } catch (_) {}
});

function silentLogger() {
  return {
    info: () => {}, log: () => {}, warn: () => {}, error: () => {}, debug: () => {},
  };
}

function captureLogger() {
  const warns = [];
  const logs = [];
  return {
    warns,
    logs,
    logger: {
      info: () => {},
      log: (m) => logs.push(String(m)),
      warn: (m) => warns.push(String(m)),
      error: () => {},
      debug: () => {},
    },
  };
}

function makeStore({ nodeId = 'node_aaaaaaaaaaaa' } = {}) {
  const state = { node_id: nodeId };
  return {
    getState: (k) => (state[k] !== undefined ? state[k] : null),
    setState: (k, v) => { state[k] = v; },
    countPending: () => 0,
    writeInbound: () => {},
    writeInboundBatch: () => {},
  };
}

function mockFetch(responseFactory) {
  const calls = [];
  const fn = async (url, opts) => {
    calls.push({ url: String(url), opts });
    return responseFactory(calls.length);
  };
  fn.calls = calls;
  return fn;
}

function responseFromJson({ status = 200, json = {}, headers = {} } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (k) => headers[k.toLowerCase()] || headers[k] || null },
    json: async () => json,
    text: async () => JSON.stringify(json),
  };
}

function responseFromText({ status = 426, body = '', headers = {} } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (k) => headers[k.toLowerCase()] || headers[k] || null },
    json: async () => { try { return JSON.parse(body); } catch { return {}; } },
    text: async () => body,
  };
}

// Wait for the microtask spawned by _maybeTriggerForceUpdateFromHeartbeat
// (the Promise.resolve().then(...) block) to settle, AND for any chained
// microtasks (reportForceUpdateOutcome -> persist -> fs.writeSync). One
// setImmediate is enough in practice but we double up for safety against
// chained microtask scheduling differences across Node patch versions.
async function settleMicrotasks() {
  await new Promise((r) => setImmediate(r));
  await new Promise((r) => setImmediate(r));
}

// Per-test reset hook. Wrap each test body so cooldown / state-file /
// fetch / spy state are deterministic.
function resetAll() {
  executeForceUpdateCalls = [];
  executeForceUpdateReturn = false;
  executeForceUpdateReturns = [];
  executeForceUpdateThrow = null;
  exitCalls = [];
  _resetProxyForceUpdateStateForTesting();
  _resetLastUpdateStateForTesting();
}

// ----------------------------------------------------------------------
// 200 + force_update: the path that did not exist before the fix.
// ----------------------------------------------------------------------

test('200 heartbeat with force_update calls executeForceUpdate exactly once', async () => {
  resetAll();
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'atp_auto_deliver' },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();
    assert.strictEqual(result.ok, true, 'heartbeat itself returns ok');
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 1,
      'executeForceUpdate must run exactly once per 200+force_update tick');
    assert.strictEqual(executeForceUpdateCalls[0].required_version, '>=1.74.1');
  } finally {
    global.fetch = originalFetch;
  }
});

test('200 heartbeat with force_update persists last_update state file (failure path)', async () => {
  resetAll();
  const originalFetch = global.fetch;
  try {
    // Default executeForceUpdateReturn=false (failure) — should still
    // persist a status="failed" payload to the state file. The hub-side
    // EvolverUpgradeAttempt row depends on this; the empty-table bug
    // happens precisely when nothing reaches this state file.
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'atp_auto_deliver' },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();
    await settleMicrotasks();

    const statePath = _getLastUpdateStatePathForTesting();
    assert.ok(fs.existsSync(statePath),
      'state file must be persisted after a failure outcome — next heartbeat ferries it');
    const pending = _readPendingLastUpdateForTesting();
    assert.ok(pending, 'pending last_update must be parseable');
    assert.strictEqual(pending.status, 'failed',
      'spy returned false → status="failed"');
    assert.strictEqual(pending.to_version, '1.74.1',
      'to_version must be the stripped concrete semver');
  } finally {
    global.fetch = originalFetch;
  }
});

test('200 heartbeat without force_update: executeForceUpdate is NOT called', async () => {
  resetAll();
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { status: 'ok' },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 0,
      'no force_update payload → no upgrade attempt');
  } finally {
    global.fetch = originalFetch;
  }
});

// ----------------------------------------------------------------------
// 426 + force_update: the path that funnelled into http_426 before.
// ----------------------------------------------------------------------

test('426 heartbeat with force_update body triggers executeForceUpdate', async () => {
  resetAll();
  const originalFetch = global.fetch;
  try {
    const body = JSON.stringify({
      error: 'evolver_min_version_required',
      force_update: { required_version: '>=1.74.1', reason: 'min_version_required' },
    });
    const mf = mockFetch(() => responseFromText({ status: 426, body }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();
    // 426 is still a non-2xx; the heartbeat itself reports failure so the
    // backoff engages, but executeForceUpdate must have been kicked off.
    assert.strictEqual(result.ok, false, '426 must surface as a heartbeat failure');
    assert.strictEqual(result.statusCode, 426);
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 1,
      'executeForceUpdate must fire from the 426+force_update body');
    assert.strictEqual(executeForceUpdateCalls[0].required_version, '>=1.74.1');
  } finally {
    global.fetch = originalFetch;
  }
});

test('426 heartbeat without parseable force_update body does NOT throw, does NOT trigger', async () => {
  resetAll();
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromText({ status: 426, body: 'plain text not json' }));
    global.fetch = mf;

    const cap = captureLogger();
    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: cap.logger,
    });
    const result = await mgr.heartbeat();
    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.statusCode, 426);
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 0,
      'unparseable 426 body must not trigger an upgrade');
    assert.ok(cap.warns.some((m) => /426/.test(m) && /without parseable/.test(m)),
      'logger must warn that the 426 body was unparseable');
  } finally {
    global.fetch = originalFetch;
  }
});

test('426 heartbeat with JSON body but no force_update field does NOT trigger', async () => {
  resetAll();
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromText({
      status: 426,
      body: JSON.stringify({ error: 'something_else' }),
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 0,
      '426 without force_update must not call into the upgrader');
  } finally {
    global.fetch = originalFetch;
  }
});

// ----------------------------------------------------------------------
// In-flight + cooldown semantics. Mirror a2aProtocol.js's contract.
// ----------------------------------------------------------------------

test('cooldown blocks back-to-back triggers within EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS', async () => {
  resetAll();
  // Override the global pin to a large value so the second heartbeat is
  // gated by the cooldown branch (not the in-flight branch, which has
  // already cleared by then).
  const prev = process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS;
  process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '3600000';
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'atp' },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();
    await settleMicrotasks();
    await mgr.heartbeat();
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 1,
      'second tick within cooldown must NOT re-trigger');
  } finally {
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = prev;
    global.fetch = originalFetch;
  }
});

// ----------------------------------------------------------------------
// NOOP sentinel: executeForceUpdate returning FORCE_UPDATE_NOOP must
// emit status="skipped" telemetry and MUST NOT trigger process.exit(78).
// ----------------------------------------------------------------------

test('FORCE_UPDATE_NOOP sentinel results in status="skipped" and no exit', async () => {
  resetAll();
  executeForceUpdateReturn = SPY_NOOP;
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'atp' },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();
    await settleMicrotasks();

    assert.deepStrictEqual(exitCalls, [],
      'no-op must not call process.exit(78)');
    const pending = _readPendingLastUpdateForTesting();
    assert.ok(pending, 'no-op must still persist a last_update row for telemetry');
    assert.strictEqual(pending.status, 'skipped',
      'NOOP sentinel must report status="skipped"');
  } finally {
    global.fetch = originalFetch;
  }
});

test('FORCE_UPDATE_NOOP does not consume cooldown for a later higher version', async () => {
  resetAll();
  executeForceUpdateReturns = [SPY_NOOP, false];
  const prev = process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS;
  process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '3600000';
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch((callNo) => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: {
          required_version: callNo === 1 ? '>=1.88.3' : '>=1.89.1',
          reason: 'atp',
        },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();
    await settleMicrotasks();
    await mgr.heartbeat();
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 2,
      'a proxy no-op stale floor must not delay a newer force_update directive');
    assert.strictEqual(executeForceUpdateCalls[0].required_version, '>=1.88.3');
    assert.strictEqual(executeForceUpdateCalls[1].required_version, '>=1.89.1');
  } finally {
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = prev;
    global.fetch = originalFetch;
  }
});

// ----------------------------------------------------------------------
// BUSY sentinel: executeForceUpdate returning FORCE_UPDATE_BUSY means a
// concurrent caller (a2aProtocol heartbeat trigger or evolve tick) is
// already running the upgrade and owns the telemetry. The proxy trigger
// MUST NOT write a state file or call exit(78) — doing either would
// clobber the in-flight caller's outcome with a phantom failed row.
// Mirrors src/gep/a2aProtocol.js (search FORCE_UPDATE_BUSY).
// ----------------------------------------------------------------------

test('FORCE_UPDATE_BUSY sentinel skips telemetry and does not exit', async () => {
  resetAll();
  executeForceUpdateReturn = SPY_BUSY;
  const originalFetch = global.fetch;
  const cap = captureLogger();
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'atp' },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: cap.logger,
    });
    await mgr.heartbeat();
    await settleMicrotasks();

    assert.strictEqual(executeForceUpdateCalls.length, 1,
      'spy must still have been invoked exactly once');
    assert.deepStrictEqual(exitCalls, [],
      'BUSY must not trigger exit(78) — the in-flight caller owns restart');
    const statePath = _getLastUpdateStatePathForTesting();
    assert.strictEqual(fs.existsSync(statePath), false,
      'BUSY must NOT write a state file — would clobber in-flight caller telemetry');
    const pending = _readPendingLastUpdateForTesting();
    assert.strictEqual(pending, null,
      'no pending payload should be readable after a BUSY short-circuit');
    assert.ok(
      cap.logs.some((m) => /BUSY \(concurrent invocation\)/.test(m)),
      'BUSY short-circuit must emit a logger.log line for observability');
  } finally {
    global.fetch = originalFetch;
  }
});

// ----------------------------------------------------------------------
// Truthy success: executeForceUpdate returning true MUST call exit(78).
// ----------------------------------------------------------------------

test('executeForceUpdate=true triggers process.exit(78) and status="success"', async () => {
  resetAll();
  executeForceUpdateReturn = true;
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'atp' },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();
    await settleMicrotasks();

    assert.deepStrictEqual(exitCalls, [78],
      'successful upgrade must request restart via exit(78)');
    const pending = _readPendingLastUpdateForTesting();
    assert.ok(pending, 'success path must still persist a last_update row');
    assert.strictEqual(pending.status, 'success');
    assert.strictEqual(pending.to_version, '1.74.1');
  } finally {
    global.fetch = originalFetch;
  }
});

// ----------------------------------------------------------------------
// executeForceUpdate throwing must NOT escape the microtask boundary,
// MUST still persist status="failed" with the error string.
// ----------------------------------------------------------------------

test('executeForceUpdate throwing is non-fatal and persists status="failed" with error', async () => {
  resetAll();
  executeForceUpdateThrow = new Error('npm registry unreachable');
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: {
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'atp' },
      },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    // Heartbeat itself must complete successfully — the upgrade throw
    // lives in a detached microtask.
    const result = await mgr.heartbeat();
    assert.strictEqual(result.ok, true);
    await settleMicrotasks();

    const pending = _readPendingLastUpdateForTesting();
    assert.ok(pending, 'thrown error path must still persist a last_update row');
    assert.strictEqual(pending.status, 'failed');
    assert.match(pending.error || '', /npm registry unreachable/);
  } finally {
    global.fetch = originalFetch;
  }
});
