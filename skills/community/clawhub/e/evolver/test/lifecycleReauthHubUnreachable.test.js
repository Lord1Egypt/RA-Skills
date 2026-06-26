'use strict';

const test = require('node:test');
const assert = require('node:assert');

const { LifecycleManager } = require('../src/proxy/lifecycle/manager');

// LifecycleManager calls hubFetch internally; in insecure mode hubFetch
// routes through global.fetch so the stubs below apply. node --test gives
// each file its own worker process, so this env var does not leak to
// sibling test files.
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
    return responseFactory(calls.length, url);
  };
  fn.calls = calls;
  return fn;
}

// A non-JSON Hub response (WAF challenge page, captive portal, gateway error)
// has no `json()` body the API path can parse. readHubResponseText falls back
// to `res.text()` here since there is no streaming body.getReader.
function responseFromHtml({ status = 403, html = '<html><body>403 Forbidden (WAF)</body></html>' } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (k) => (k.toLowerCase() === 'content-type' ? 'text/html; charset=utf-8' : null) },
    text: async () => html,
  };
}

function responseFromJson({ status = 200, json = {}, headers = {} } = {}) {
  const merged = { 'content-type': 'application/json', ...headers };
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (k) => merged[k.toLowerCase()] || merged[k] || null },
    json: async () => json,
    text: async () => JSON.stringify(json),
  };
}

// Regression for the re-auth × hub-unreachable interaction (PR #262 review):
// a genuine JSON 401/403 enters reAuthenticate, but the rotate hello then hits
// a non-API Hub response (WAF HTML). The loop must NOT exhaust its attempts and
// arm the long re-auth backoff (REAUTH_BACKOFF_BASE_MS..MAX_MS) -- that would
// suppress legitimate auth recovery for up to hours once the hub is reachable.
test('reAuthenticate: hub-unreachable during rotate does NOT arm re-auth backoff', async () => {
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromHtml({ status: 403 }));
    global.fetch = mf;
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: makeStore(), logger: silentLogger() });

    const recovered = await mgr.reAuthenticate();

    assert.strictEqual(recovered, false, 're-auth cannot succeed while hub is unreachable');
    assert.strictEqual(
      mgr._reauthBackoffUntil,
      0,
      're-auth backoff must NOT be armed by a transient hub outage'
    );
    assert.strictEqual(
      mgr._consecutiveReauthFailures,
      0,
      'a hub outage is not a re-auth failure and must not increment the counter'
    );
    // The hub-unreachable window (set by hello) is what gates the next attempt.
    assert.ok(mgr._hubUnreachableUntil > Date.now(), 'hub-unreachable window should gate re-entry');
  } finally {
    global.fetch = originalFetch;
  }
});

// Positive control: a reachable hub returning a real JSON API error (500) is a
// genuine auth-recovery failure and MUST still arm the re-auth backoff after
// exhausting attempts. Guards against the fix over-suppressing the normal path.
test('reAuthenticate: genuine JSON API failure still arms re-auth backoff', async () => {
  const originalFetch = global.fetch;
  try {
    const mf = mockFetch(() => responseFromJson({ status: 500, json: { error: 'rotate_failed' } }));
    global.fetch = mf;
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: makeStore(), logger: silentLogger() });

    const recovered = await mgr.reAuthenticate();

    assert.strictEqual(recovered, false);
    assert.strictEqual(mgr._consecutiveReauthFailures, 1, 'genuine failure increments the counter');
    assert.ok(mgr._reauthBackoffUntil > Date.now(), 're-auth backoff should be armed on a real API failure');
    assert.strictEqual(mgr._hubUnreachableUntil, 0, 'a JSON 500 is reachable, not a hub outage');
  } finally {
    global.fetch = originalFetch;
  }
});
