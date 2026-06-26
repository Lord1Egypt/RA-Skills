'use strict';

const test = require('node:test');
const assert = require('node:assert');

const { LifecycleManager } = require('../src/proxy/lifecycle/manager');

// LifecycleManager calls hubFetch internally; tests here stub global.fetch
// and pass a fake `https://example.test` hubUrl. In insecure mode hubFetch
// routes through global.fetch so the stubs apply. URL is already https,
// but this also disables URL validation in case the test resolves to a
// non-https form. node --test gives each file its own worker process, so
// this env var does not leak to sibling test files.
const _origLifecycleInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
test.after(() => {
  if (_origLifecycleInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  else process.env.EVOMAP_HUB_ALLOW_INSECURE = _origLifecycleInsecure;
});

function makeStore() {
  const state = {};
  return {
    getState: (k) => state[k] || null,
    setState: (k, v) => { state[k] = v; },
    countPending: () => 0,
    writeInbound: () => {},
    writeInboundBatch: () => {},
  };
}

function silentLogger() {
  return { log: () => {}, warn: () => {}, error: () => {} };
}

function mockFetch(responseFactory) {
  const calls = [];
  const fn = async (url, opts) => {
    calls.push({ url, opts });
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

test('lifecycle hello: sets _helloRateLimitUntil when hub returns 429', async () => {
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 429,
      json: { error: 'hello_rate_limit: max 60/hour per IP' },
      headers: { 'retry-after': '1800' },
    }));
    global.fetch = mf;
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: makeStore(), logger: silentLogger() });
    const result = await mgr.hello();
    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.error, 'hello_rate_limited');
    assert.strictEqual(result.retryAfter, 1800);
    assert.ok(mgr._helloRateLimitUntil > Date.now(), 'rate limit window should be set');
  } finally {
    global.fetch = originalFetch;
  }
});

test('lifecycle hello: suppresses call while rate-limit window is active', async () => {
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({ status: 200, json: {} }));
    global.fetch = mf;
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: makeStore(), logger: silentLogger() });
    mgr._helloRateLimitUntil = Date.now() + 60_000;
    const result = await mgr.hello();
    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.error, 'hello_rate_limit_active');
    assert.strictEqual(mf.calls.length, 0, 'no network call should be made while rate-limited');
  } finally {
    global.fetch = originalFetch;
  }
});

test('lifecycle reAuthenticate: breaks and sets backoff when hub rotates without returning secret', async () => {
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { payload: {} },
    }));
    global.fetch = mf;
    const store = makeStore();
    store.setState('node_id', 'node_test');
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.reAuthenticate();
    assert.strictEqual(result, false);
    assert.strictEqual(mf.calls.length, 1, 'should break after first missing-secret response, not retry');
    assert.ok(mgr._reauthBackoffUntil > Date.now(), '30-minute backoff should be set');
  } finally {
    global.fetch = originalFetch;
  }
});

test('lifecycle reAuthenticate: suppresses re-entry while backoff window is active', async () => {
  const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: makeStore(), logger: silentLogger() });
  mgr._reauthBackoffUntil = Date.now() + 30 * 60_000;
  const result = await mgr.reAuthenticate();
  assert.strictEqual(result, false);
});

test('lifecycle reAuthenticate: backoff escalates exponentially on consecutive failures', async () => {
  // Each consecutive failed re-auth doubles the backoff. Base was reduced
  // from 30min to 2min (proxy parity with the non-proxy path), capped near
  // 4 hours. Curve: 2, 4, 8, 16, 32, 64, 128, 240(cap)... minutes.
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { payload: {} },
    }));
    global.fetch = mf;
    const store = makeStore();
    store.setState('node_id', 'node_test');
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    // Failure #1 -> ~2 min (base)
    await mgr.reAuthenticate();
    const firstBackoff = mgr._reauthBackoffUntil - Date.now();
    assert.ok(firstBackoff > 60_000 && firstBackoff <= 2 * 60_000 + 1000, `first failure ~2min, got ${firstBackoff}ms`);

    // Pretend the window expired so we can drive a second failure.
    mgr._reauthBackoffUntil = 0;
    await mgr.reAuthenticate();
    const secondBackoff = mgr._reauthBackoffUntil - Date.now();
    assert.ok(secondBackoff > 3 * 60_000 && secondBackoff <= 4 * 60_000 + 1000, `second failure ~4min, got ${secondBackoff}ms`);

    // Drive enough more to saturate the 4h cap. Base 2min * 2^(n-1):
    // n=8 -> 256min -> capped at 240min. Run until we're well past the cap.
    for (let i = 0; i < 8; i++) {
      mgr._reauthBackoffUntil = 0;
      await mgr.reAuthenticate();
    }
    const cappedBackoff = mgr._reauthBackoffUntil - Date.now();
    assert.ok(cappedBackoff <= 4 * 60 * 60_000 + 1000, `backoff must cap at ~4h, got ${cappedBackoff}ms`);
    assert.ok(cappedBackoff >= 4 * 60 * 60_000 - 5000, `backoff should hit the cap, got ${cappedBackoff}ms`);
  } finally {
    global.fetch = originalFetch;
  }
});

test('lifecycle reAuthenticate: successful re-auth resets the consecutive-failures counter', async () => {
  const originalFetch = global.fetch;
  const VALID_HEX64_NEW = 'b'.repeat(64);
  try {
    const store = makeStore();
    store.setState('node_id', 'node_test');
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    mgr._consecutiveReauthFailures = 5; // pretend we have been failing a while

    const mf = mockFetch((nthCall) => {
      if (nthCall === 1) {
        return responseFromJson({
          status: 200,
          json: { payload: { status: 'acknowledged', node_secret: VALID_HEX64_NEW, your_node_id: 'node_test' } },
        });
      }
      return responseFromJson({ status: 200, json: { status: 'ok' } });
    });
    global.fetch = mf;

    const result = await mgr.reAuthenticate();
    assert.strictEqual(result, true);
    assert.strictEqual(mgr._consecutiveReauthFailures, 0, 'success must reset the failure counter');
  } finally {
    global.fetch = originalFetch;
  }
});

test('lifecycle reAuthenticate: breaks on hello_rate_limited without retrying', async () => {
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({
      status: 429,
      json: { error: 'hello_rate_limit: max 60/hour per IP' },
      headers: { 'retry-after': '60' },
    }));
    global.fetch = mf;
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: makeStore(), logger: silentLogger() });
    const result = await mgr.reAuthenticate();
    assert.strictEqual(result, false);
    assert.strictEqual(mf.calls.length, 1, 'should break on rate-limit, not retry second attempt');
    assert.ok(mgr._helloRateLimitUntil > Date.now());
  } finally {
    global.fetch = originalFetch;
  }
});

test('lifecycle _shouldUpgrade: handles prerelease minimum versions (community PR #516)', () => {
  // Previously used Number() for version parts, so "1-beta" -> NaN -> 0, which
  // silently broke prerelease comparisons. parseInt(..., 10) strips the
  // trailing tag and keeps the numeric prefix. Compare against the currently
  // shipped PROXY_PROTOCOL_VERSION rather than a hard-coded string so this
  // test keeps working across version bumps.
  const { PROXY_PROTOCOL_VERSION } = require('../src/proxy/mailbox/store');
  const [maj, min, pat] = PROXY_PROTOCOL_VERSION.split('.').map(p => parseInt(p, 10));

  const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: makeStore(), logger: silentLogger() });

  // A prerelease tag on the *same* version must not force an upgrade.
  assert.strictEqual(mgr._shouldUpgrade(`${maj}.${min}.${pat}-beta.1`), false,
    'same version with prerelease tag must not trigger upgrade');

  // A prerelease minimum one patch ahead must still trigger upgrade.
  assert.strictEqual(mgr._shouldUpgrade(`${maj}.${min}.${pat + 1}-beta.1`), true,
    'higher patch with prerelease tag must trigger upgrade');

  // A prerelease minimum one minor ahead must still trigger upgrade.
  assert.strictEqual(mgr._shouldUpgrade(`${maj}.${min + 1}.0-beta.1`), true,
    'higher minor with prerelease tag must trigger upgrade');
});
