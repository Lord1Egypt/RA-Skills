'use strict';

// Regression coverage: lifecycle hello() must reuse the node_id persisted by
// the legacy GEP path (~/.evomap/node_id, written by src/gep/a2aProtocol.js)
// when MailboxStore has none. Without this, a fresh state.json paired with
// an existing legacy file silently mints a new node identity at
// `crypto.randomBytes(6)` and the hub registers a duplicate A2ANode under
// the same owner — the original (with stake, reputation, aliases) is then
// abandoned. Discovered on Aurora 2026-05-22 after a bad daemon restart on
// 2026-05-21 created node_17daa803cca6 alongside the real
// node_973fad206a3846f7 and the lifecycle path drove the dup for a week.
//
// Override EVOLVER_HOME (not $HOME): #114 unified all ~/.evomap callsites
// onto `paths.getEvomapDir()`, which honours EVOLVER_HOME first and only
// falls through to os.homedir() when unset. Both _readLegacyNodeId here
// and _persistNodeId in a2aProtocol.js now route through that helper, so
// pinning EVOLVER_HOME is enough to redirect both reader and writer.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { LifecycleManager } = require('../src/proxy/lifecycle/manager');
const { _resetCachedNodeIdForTesting } = require('../src/gep/a2aProtocol')._testing;

const _origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
test.after(() => {
  if (_origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  else process.env.EVOMAP_HUB_ALLOW_INSECURE = _origInsecure;
});

const VALID_NODE_ID = 'node_973fad206a3846f7';
// A second valid id to prove the fallback ordering: when the store has its
// own legitimate value AND the legacy file has a *different* legitimate
// value, the store must win on the wire.
const VALID_LEGACY_OTHER = 'node_abcdef0123456789';

// Build a fake EVOLVER_HOME directory and call setupFn against it so
// callers can drop a node_id file inside. Note that EVOLVER_HOME points
// at the .evomap dir directly (not at a parent containing one) — that's
// the contract `paths.getEvomapDir()` exposes.
function makeFakeEvomapDir(setupFn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-legacy-nodeid-'));
  if (setupFn) setupFn(dir);
  return dir;
}

function makeStore(initial = {}) {
  const state = { ...initial };
  return {
    getState: (k) => (state[k] !== undefined ? state[k] : null),
    setState: (k, v) => { state[k] = v; },
    countPending: () => 0,
    writeInbound: () => {},
    writeInboundBatch: () => {},
    _state: state,
  };
}

function silentLogger() {
  return { log: () => {}, warn: () => {}, error: () => {} };
}

function mockFetch(responseFactory) {
  const calls = [];
  const fn = async (url, opts) => {
    calls.push({ url, opts });
    return responseFactory(calls.length, opts);
  };
  fn.calls = calls;
  return fn;
}

function responseFromJson({ status = 200, json = {} } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: () => null },
    json: async () => json,
    text: async () => JSON.stringify(json),
  };
}

// Run `body` with EVOLVER_HOME pointed at the given fake .evomap dir.
// The reader routes through `paths.getEvomapDir()`, which honours
// EVOLVER_HOME first, so this redirects both reader and writer in lockstep.
async function withFakeEvomapDir(dir, body) {
  const _origHome = process.env.EVOLVER_HOME;
  const _origFetch = global.fetch;
  process.env.EVOLVER_HOME = dir;
  _resetCachedNodeIdForTesting();
  try {
    return await body();
  } finally {
    if (_origHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = _origHome;
    global.fetch = _origFetch;
    _resetCachedNodeIdForTesting();
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

test('hello reuses legacy ~/.evomap/node_id when store has none', async () => {
  const dir = makeFakeEvomapDir((evomap) => {
    fs.writeFileSync(path.join(evomap, 'node_id'), VALID_NODE_ID, { mode: 0o600 });
  });
  await withFakeEvomapDir(dir, async () => {
    let observedSenderId = null;
    global.fetch = mockFetch((_n, opts) => {
      try { observedSenderId = JSON.parse(opts.body).sender_id; } catch { /* ignore */ }
      return responseFromJson({ status: 200, json: { payload: { status: 'acknowledged' } } });
    });

    const store = makeStore(); // store has no node_id yet
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.hello();

    assert.strictEqual(result.ok, true, 'hello must succeed');
    assert.strictEqual(result.nodeId, VALID_NODE_ID, 'hello must reuse the legacy node_id');
    assert.strictEqual(observedSenderId, VALID_NODE_ID, 'sender_id on the wire must be the legacy id');
    assert.strictEqual(store.getState('node_id'), VALID_NODE_ID, 'store must be primed with the recovered id');
  });
});

test('hello prefers store node_id over a *different valid* legacy id', async () => {
  // Both are valid node ids per NODE_ID_RE; only the store-precedes-legacy
  // ordering decides the winner. If the regex were the only thing rejecting
  // the legacy file, this test would fail. (Bugbot #117 round-2 catch.)
  const dir = makeFakeEvomapDir((evomap) => {
    fs.writeFileSync(path.join(evomap, 'node_id'), VALID_LEGACY_OTHER, { mode: 0o600 });
  });
  await withFakeEvomapDir(dir, async () => {
    let observedSenderId = null;
    global.fetch = mockFetch((_n, opts) => {
      try { observedSenderId = JSON.parse(opts.body).sender_id; } catch { /* ignore */ }
      return responseFromJson({ status: 200, json: { payload: { status: 'acknowledged' } } });
    });

    const store = makeStore({ node_id: VALID_NODE_ID });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.hello();

    assert.strictEqual(result.nodeId, VALID_NODE_ID, 'store wins when both have valid ids');
    assert.strictEqual(observedSenderId, VALID_NODE_ID, 'sender_id on the wire must be the store id');
    assert.notStrictEqual(observedSenderId, VALID_LEGACY_OTHER, 'legacy id must NOT be used when store has its own');
  });
});

test('hello falls back to randomBytes when neither store nor legacy file has a valid id', async () => {
  const dir = makeFakeEvomapDir((evomap) => {
    // Malformed legacy file must be rejected by NODE_ID_RE, not silently
    // fed into the hello payload.
    fs.writeFileSync(path.join(evomap, 'node_id'), 'totally-not-a-node-id\n', { mode: 0o600 });
  });
  await withFakeEvomapDir(dir, async () => {
    let observedSenderId = null;
    global.fetch = mockFetch((_n, opts) => {
      try { observedSenderId = JSON.parse(opts.body).sender_id; } catch { /* ignore */ }
      return responseFromJson({ status: 200, json: { payload: { status: 'acknowledged' } } });
    });

    const store = makeStore();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.hello();

    assert.strictEqual(result.ok, true);
    assert.match(observedSenderId, /^node_[a-f0-9]{12}$/, 'malformed legacy id must be ignored, falling back to random');
    assert.notStrictEqual(observedSenderId, 'totally-not-a-node-id', 'must not echo the malformed file');
  });
});

test('hello tolerates missing legacy file (falls through to random)', async () => {
  const dir = makeFakeEvomapDir(); // no node_id file at all
  await withFakeEvomapDir(dir, async () => {
    let observedSenderId = null;
    global.fetch = mockFetch((_n, opts) => {
      try { observedSenderId = JSON.parse(opts.body).sender_id; } catch { /* ignore */ }
      return responseFromJson({ status: 200, json: { payload: { status: 'acknowledged' } } });
    });

    const store = makeStore();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.hello();

    assert.strictEqual(result.ok, true);
    assert.match(observedSenderId, /^node_[a-f0-9]{12}$/, 'no legacy file -> random');
  });
});

// Project-local fallback path. The legacy writer in src/gep/a2aProtocol.js
// falls back to `<install>/.evomap_node_id` whenever ~/.evomap/ isn't
// writable (read-only $HOME in containers / restricted CI). The reader has
// to look there too — Bugbot #117 round-3 catch. Resolve the file the same
// way the production code does: from the lifecycle module's __dirname,
// which is `<install>/src/proxy/lifecycle`. From this test file
// (`<install>/test/...`) that's the repo root + `.evomap_node_id`.
const INSTALL_ROOT_LOCAL_FILE = path.resolve(__dirname, '..', '.evomap_node_id');

test('hello recovers a node_id persisted at <install>/.evomap_node_id when home file is absent', async () => {
  // The home directory is empty (no ~/.evomap/node_id) but the install
  // root holds a valid id from an earlier run with a read-only $HOME.
  const dir = makeFakeEvomapDir();
  // Refuse to clobber a real local file — if one exists on this checkout
  // (unusual but possible) the test would corrupt it.
  if (fs.existsSync(INSTALL_ROOT_LOCAL_FILE)) {
    throw new Error(`refusing to clobber existing ${INSTALL_ROOT_LOCAL_FILE}; remove it before re-running`);
  }
  fs.writeFileSync(INSTALL_ROOT_LOCAL_FILE, VALID_NODE_ID, { mode: 0o600 });
  try {
    await withFakeEvomapDir(dir, async () => {
      let observedSenderId = null;
      global.fetch = mockFetch((_n, opts) => {
        try { observedSenderId = JSON.parse(opts.body).sender_id; } catch { /* ignore */ }
        return responseFromJson({ status: 200, json: { payload: { status: 'acknowledged' } } });
      });

      const store = makeStore();
      const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
      const result = await mgr.hello();

      assert.strictEqual(result.ok, true);
      assert.strictEqual(result.nodeId, VALID_NODE_ID, 'hello must reuse the install-root legacy id');
      assert.strictEqual(observedSenderId, VALID_NODE_ID, 'sender_id must be the install-root id');
    });
  } finally {
    fs.rmSync(INSTALL_ROOT_LOCAL_FILE, { force: true });
  }
});
