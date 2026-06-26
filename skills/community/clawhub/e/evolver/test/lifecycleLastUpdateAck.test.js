'use strict';

// Regression coverage for PR #188 (HIGH): the proxy heartbeat must NOT clear
// the force_update last_update state file on a 2xx that the hub did not
// actually persist. The canonical a2a path in src/gep/a2aProtocol.js gates
// the clear on `!(data && data.ok === false)`; the proxy path used to clear
// on HTTP 2xx alone, which dropped telemetry on `{ok:false}` and
// `status:'unknown_node'` envelopes (where the hub re-asks for a hello).
//
// These cases live in their own file because the rate-limit suite covers
// hello/reauth and the loop-resilience suite covers tick survival -- this
// is strictly about the post-2xx clear gate.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

if (!process.env.A2A_NODE_SECRET) {
  process.env.A2A_NODE_SECRET = 'a'.repeat(64);
}

// Insecure flag: hubFetch routes through global.fetch only when http or the
// allow-insecure flag is set. Tests below stub global.fetch.
const _origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';

// Isolate the on-disk state path from the developer's real ~/.evomap.
const _origEvolverHome = process.env.EVOLVER_HOME;
const _tmpEvolverHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-lu-ack-'));
process.env.EVOLVER_HOME = _tmpEvolverHome;

const { LifecycleManager } = require('../src/proxy/lifecycle/manager');
const a2aProtocol = require('../src/gep/a2aProtocol');
const {
  _persistLastUpdateStateForTesting,
  _getLastUpdateStatePathForTesting,
  _resetLastUpdateStateForTesting,
} = a2aProtocol._testing;

test.after(() => {
  if (_origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  else process.env.EVOMAP_HUB_ALLOW_INSECURE = _origInsecure;
  if (_origEvolverHome === undefined) delete process.env.EVOLVER_HOME;
  else process.env.EVOLVER_HOME = _origEvolverHome;
  try { fs.rmSync(_tmpEvolverHome, { recursive: true, force: true }); } catch (_) {}
});

function silentLogger() {
  return { info: () => {}, log: () => {}, warn: () => {}, error: () => {}, debug: () => {} };
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

test('lifecycle heartbeat attaches default anti_abuse telemetry without leaking salt', async () => {
  const originalFetch = global.fetch;
  const originalMode = process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
  const originalSalt = process.env.EVOLVER_ANTI_ABUSE_SALT;
  try {
    delete process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
    process.env.EVOLVER_ANTI_ABUSE_SALT = 'lifecycle-test-salt';
    const mf = mockFetch(() => responseFromJson({ status: 200, json: { status: 'ok' } }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, true);
    const body = JSON.parse(mf.calls[0].opts.body);
    assert.strictEqual(body.meta.anti_abuse.schema_version, 'anti_abuse.v1');
    assert.strictEqual(body.meta.anti_abuse.source, 'evolver-proxy');
    // The proxy's own heartbeat reports ground truth, not env sniffing —
    // this process typically has neither EVOMAP_PROXY nor EVOMAP_PROXY_PORT.
    assert.strictEqual(body.meta.anti_abuse.local_security_boundary.proxy_port_configured, true);
    assert.strictEqual(body.meta.anti_abuse.source_confidence.network_source, 'server_observed_required');
    assert.strictEqual(JSON.stringify(body).includes('lifecycle-test-salt'), false);
  } finally {
    global.fetch = originalFetch;
    if (originalMode === undefined) delete process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
    else process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = originalMode;
    if (originalSalt === undefined) delete process.env.EVOLVER_ANTI_ABUSE_SALT;
    else process.env.EVOLVER_ANTI_ABUSE_SALT = originalSalt;
  }
});

test('lifecycle heartbeat omits anti_abuse telemetry when disabled', async () => {
  const originalFetch = global.fetch;
  const originalMode = process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
  try {
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = 'off';
    const mf = mockFetch(() => responseFromJson({ status: 200, json: { status: 'ok' } }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, true);
    const body = JSON.parse(mf.calls[0].opts.body);
    assert.strictEqual(body.meta.anti_abuse, undefined);
  } finally {
    global.fetch = originalFetch;
    if (originalMode === undefined) delete process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
    else process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = originalMode;
  }
});

function seedLastUpdate() {
  _resetLastUpdateStateForTesting();
  _persistLastUpdateStateForTesting({
    to_version: '1.88.0',
    from_version: '1.87.0',
    status: 'success',
    finished_at: Date.now(),
    directive_id: 'd-test-123',
  });
  const p = _getLastUpdateStatePathForTesting();
  assert.ok(fs.existsSync(p), 'precondition: state file present');
  return p;
}

test('lifecycle heartbeat: 200 with {ok:false} envelope keeps the last_update state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { ok: false, error: 'hub_busy' },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, true, 'HTTP 2xx → heartbeat returns ok:true');
    assert.ok(fs.existsSync(statePath),
      'state file must survive a 200 + {ok:false} so the next tick can retry');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle heartbeat: 200 with status="unknown_node" keeps the last_update state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    // First call = the heartbeat (returns unknown_node). Second call = the
    // re-hello that the manager fires off in response. Both succeed with
    // 2xx so we exercise the exact race path the bug describes.
    const mf = mockFetch((n) => {
      if (n === 1) {
        return responseFromJson({ status: 200, json: { status: 'unknown_node' } });
      }
      // hello() response shape: payload with node_secret + acknowledged.
      return responseFromJson({
        status: 200,
        json: {
          payload: {
            status: 'acknowledged',
            node_secret: 'b'.repeat(64),
            your_node_id: 'node_aaaaaaaaaaaa',
          },
        },
      });
    });
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();

    assert.ok(fs.existsSync(statePath),
      'state file must survive unknown_node so the post-re-hello heartbeat can retry');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle heartbeat: 200 with valid ack clears the last_update state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
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
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, true);
    assert.ok(!fs.existsSync(statePath),
      'state file must be cleared on a hub-acknowledged 2xx');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

// ---------------------------------------------------------------------------
// 400 circuit breaker: a payload the hub schema rejects must not poison the
// heartbeat forever. Mirrors a2aProtocol.js sendHeartbeat's breaker, scoped
// to 400-only (auth and server errors must NOT trigger it). See manager.js
// heartbeat() for the rationale.
// ---------------------------------------------------------------------------

function responseFromText({ status = 400, body = '', headers = {} } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (k) => headers[k.toLowerCase()] || headers[k] || null },
    json: async () => { try { return JSON.parse(body); } catch { return {}; } },
    text: async () => body,
  };
}

test('lifecycle heartbeat: 400 naming last_update clears the state file (and still reports failure)', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromText({
      status: 400,
      body: 'validation failed: last_update.finished_at must be a string',
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, false, 'breaker must NOT mask the HTTP failure');
    assert.strictEqual(result.error, 'http_400');
    assert.strictEqual(result.statusCode, 400);
    assert.ok(!fs.existsSync(statePath),
      'state file must be cleared when 400 names last_update (poisoned payload)');
    assert.strictEqual(mgr._consecutiveFailures, 1,
      'failure counter must still tick so backoff engages');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle heartbeat: 400 NOT naming last_update retains the state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromText({
      status: 400,
      body: 'validation failed: env_fingerprint invalid',
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.error, 'http_400');
    assert.ok(fs.existsSync(statePath),
      'unrelated 400 must NOT touch the last_update state file');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle heartbeat: 500 (server/network error) retains the state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromText({
      status: 500,
      // Even if the server happens to mention last_update in a 5xx body,
      // it is NOT evidence the payload is poison (could be a transient
      // hub-side outage). Breaker must be 400-only.
      body: 'internal error processing last_update',
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.error, 'http_500');
    assert.ok(fs.existsSync(statePath),
      '5xx must NOT trigger the breaker -- transient hub-side failure');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle heartbeat: 401 (auth failure) retains the state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    // 401/403 takes the auth branch which would normally trigger reAuthenticate.
    // _skipReauth keeps the test focused on the breaker scope; reAuthenticate
    // would otherwise call hello() and add fetch complexity unrelated to the
    // assertion. Even if the body mentions last_update, auth failure must NOT
    // imply payload poisoning.
    const mf = mockFetch(() => responseFromText({
      status: 401,
      body: 'unauthorized: stale bearer for last_update report',
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat({ _skipReauth: true });

    assert.strictEqual(result.ok, false);
    assert.ok(/^auth_failed_/.test(result.error), 'auth branch (not the breaker) must own this path');
    assert.ok(fs.existsSync(statePath),
      'auth failure must NOT clear last_update -- bearer rotation is unrelated to payload validity');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle heartbeat: 403 (auth failure) retains the state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromText({
      status: 403,
      body: 'forbidden: last_update permission denied',
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat({ _skipReauth: true });

    assert.strictEqual(result.ok, false);
    assert.ok(/^auth_failed_/.test(result.error));
    assert.ok(fs.existsSync(statePath),
      'auth failure (403) must NOT clear last_update -- payload validity is orthogonal');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

// ---------------------------------------------------------------------------
// Hub last_update_ack contract (PR #188 follow-up, HIGH H1-client).
//
// Hub now writes a top-level `last_update_ack: { ok, reason? }` whenever the
// request carried a last_update payload. The proxy gate must mirror the
// canonical a2a path:
//   ack.ok=true            -> clear
//   ack.reason='duplicate' -> clear
//   ack.reason='invalid'   -> clear + warn
//   ack.reason='failed'    -> KEEP + warn
//   no ack field           -> fall back to bare-2xx semantics (old hub)
// ---------------------------------------------------------------------------

function captureWarnLogger() {
  const warns = [];
  return {
    warns,
    logger: {
      info: () => {},
      log: () => {},
      warn: (msg) => warns.push(String(msg)),
      error: () => {},
      debug: () => {},
    },
  };
}

test('lifecycle ack: ok=true clears the state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { status: 'ok', last_update_ack: { ok: true } },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    const result = await mgr.heartbeat();

    assert.strictEqual(result.ok, true);
    assert.ok(!fs.existsSync(statePath),
      'ack.ok=true must clear the state file');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle ack: reason=duplicate clears the state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { status: 'ok', last_update_ack: { ok: false, reason: 'duplicate' } },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();

    assert.ok(!fs.existsSync(statePath),
      'dedup hit (already persisted) must clear the state file');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle ack: reason=failed KEEPS the state file with warn', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { status: 'ok', last_update_ack: { ok: false, reason: 'failed' } },
    }));
    global.fetch = mf;

    const cap = captureWarnLogger();
    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: cap.logger,
    });
    await mgr.heartbeat();

    assert.ok(fs.existsSync(statePath),
      'ack.reason=failed must KEEP the state file so the next tick retries');
    assert.ok(cap.warns.some((m) => /last_update_ack=failed/.test(m)),
      'logger.warn must mention last_update_ack=failed');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle ack: reason=invalid clears the state file with warn', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { status: 'ok', last_update_ack: { ok: false, reason: 'invalid' } },
    }));
    global.fetch = mf;

    const cap = captureWarnLogger();
    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: cap.logger,
    });
    await mgr.heartbeat();

    assert.ok(!fs.existsSync(statePath),
      'ack.reason=invalid must clear the state file (retry will not help)');
    assert.ok(cap.warns.some((m) => /last_update_ack=invalid/.test(m)),
      'logger.warn must mention last_update_ack=invalid');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle ack: no field present (old hub) falls back to bare-2xx clear', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { status: 'ok' /* no last_update_ack */ },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();

    assert.ok(!fs.existsSync(statePath),
      'old-hub 2xx without ack field must clear (backward-compat path)');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle ack: no field present (old hub) + {ok:false} envelope keeps state file', async () => {
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch(() => responseFromJson({
      status: 200,
      json: { ok: false, error: 'transient' /* no last_update_ack */ },
    }));
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();

    assert.ok(fs.existsSync(statePath),
      'old-hub fallback must still respect {ok:false} envelope');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});

test('lifecycle ack: ok=true with status=unknown_node still clears (ack is authoritative)', async () => {
  // Subtle case: a new hub that wrote the ack BEFORE deciding the node is
  // unknown (or the unknown_node status simply coexists with a real
  // persist). Ack is the authoritative signal -- if the hub says it
  // persisted, the file must clear regardless of the envelope status.
  const originalFetch = global.fetch;
  try {
    const statePath = seedLastUpdate();
    const mf = mockFetch((n) => {
      if (n === 1) {
        return responseFromJson({
          status: 200,
          json: { status: 'unknown_node', last_update_ack: { ok: true } },
        });
      }
      // hello() response shape used by the unknown_node re-registration.
      return responseFromJson({
        status: 200,
        json: {
          payload: {
            status: 'acknowledged',
            node_secret: 'b'.repeat(64),
            your_node_id: 'node_aaaaaaaaaaaa',
          },
        },
      });
    });
    global.fetch = mf;

    const mgr = new LifecycleManager({
      hubUrl: 'https://example.test',
      store: makeStore(),
      logger: silentLogger(),
    });
    await mgr.heartbeat();

    assert.ok(!fs.existsSync(statePath),
      'ack.ok=true is authoritative: clear even when envelope says unknown_node');
  } finally {
    global.fetch = originalFetch;
    _resetLastUpdateStateForTesting();
  }
});
