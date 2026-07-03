'use strict';

// Regression coverage for EvoMap/evolver#529
//   "Proxy: MailboxStore stale node_secret causes infinite auth failure loop"
//
// Three fixes are exercised here:
//   1. nodeSecret getter reconciles A2A_NODE_SECRET env var with the
//      MailboxStore: env wins on conflict and the store is rewritten so the
//      stale value cannot bite again on the next call.
//   2. reAuthenticate, when faced with node_id_already_claimed, drops the
//      cached secret on the way to the second attempt instead of looping.
//   3. After hello rotates the secret, _suppressEnvSecret flips so the next
//      _resolveNodeSecret call (e.g. inside the verification heartbeat) does
//      NOT undo the rotation by syncing the store back to the now-stale env
//      value (Bugbot review on PR #22).

const test = require('node:test');
const assert = require('node:assert');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { LifecycleManager } = require('../src/proxy/lifecycle/manager');
const { MailboxStore } = require('../src/proxy/mailbox/store');

// LifecycleManager calls hubFetch internally; tests here stub global.fetch
// and pass a fake `https://example.test` hubUrl. In insecure mode hubFetch
// routes through global.fetch so the stubs apply. node --test gives each
// file its own worker process, so this env var does not leak.
const _origLifecycleSecretInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
test.after(() => {
  if (_origLifecycleSecretInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  else process.env.EVOMAP_HUB_ALLOW_INSECURE = _origLifecycleSecretInsecure;
});

const VALID_HEX64_A = 'a'.repeat(64);
const VALID_HEX64_B = 'b'.repeat(64);
const VALID_HEX64_C = 'c'.repeat(64);

function suppressionMarker(secret) {
  return 'sha256:' + crypto.createHash('sha256').update(secret.toLowerCase()).digest('hex');
}

function makeStore(initial = {}) {
  const state = { ...initial };
  const inbound = [];
  const sets = [];
  return {
    getState: (k) => (state[k] !== undefined ? state[k] : null),
    setState: (k, v) => { state[k] = v; sets.push([k, v]); },
    countPending: () => 0,
    writeInbound: (event) => { inbound.push(event); },
    writeInboundBatch: () => {},
    _state: state,
    _inbound: inbound,
    _sets: sets,
  };
}

function silentLogger() {
  const calls = { log: [], warn: [], error: [] };
  return {
    log: (...args) => calls.log.push(args.join(' ')),
    warn: (...args) => calls.warn.push(args.join(' ')),
    error: (...args) => calls.error.push(args.join(' ')),
    _calls: calls,
  };
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

function responseFromJson({ status = 200, json = {}, headers = {} } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (k) => headers[k.toLowerCase()] || headers[k] || null },
    json: async () => json,
    text: async () => JSON.stringify(json),
  };
}

function assertNoRawHubResponseSecrets(logText, raw) {
  assert.strictEqual(logText.includes(raw.nodeSecret), false, 'raw node_secret value must not be logged');
  assert.strictEqual(logText.includes(raw.bearer), false, 'raw Bearer token must not be logged');
  assert.strictEqual(logText.includes(raw.token), false, 'raw token field value must not be logged');
  assert.strictEqual(logText.includes(raw.envPath), false, 'raw .env path must not be logged');
  assert.strictEqual(logText.includes(raw.body), false, 'raw Hub response body must not be logged verbatim');
}

test('nodeSecret getter: env var wins over store with no source tag (legacy / first boot)', () => {
  // Mirrors #529: store carries a legacy or env_seed value that has gone
  // stale in the meantime, while the operator just exported a fresh secret
  // in A2A_NODE_SECRET. With no source tag, env still wins and we re-sync.
  const original = process.env.A2A_NODE_SECRET;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    const store = makeStore({ node_secret: VALID_HEX64_B });
    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger });

    const resolved = mgr.nodeSecret;

    assert.strictEqual(resolved, VALID_HEX64_A, 'env value should win on conflict');
    assert.strictEqual(store.getState('node_secret'), VALID_HEX64_A, 'store should be re-synced');
    assert.strictEqual(
      store.getState('node_secret_source'),
      'env_seed',
      'env-resync must mark the new store value as env_seed'
    );
    assert.strictEqual(store.getState('node_secret_env_suppressed'), '', 'env refresh must clear stale suppression marker');
    assert.ok(
      logger._calls.warn.some((m) => m.includes('A2A_NODE_SECRET env var differs')),
      'should warn the operator exactly once'
    );

    // Second access must NOT log again -- prevents log flooding on every header build.
    mgr.nodeSecret;
    const warnCount = logger._calls.warn.filter((m) => m.includes('A2A_NODE_SECRET env var differs')).length;
    assert.strictEqual(warnCount, 1, 'override warning should be one-shot');
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
  }
});

test('nodeSecret getter: store wins when its value was last written by hub_rotate', () => {
  // Symmetric failure to #529. A previous daemon run rotated the secret via
  // /a2a/hello (store now holds the hub-recognised value, tagged
  // node_secret_source='hub_rotate'). After a daemon restart the parent
  // shell still exports the *old* value of A2A_NODE_SECRET. Without
  // source-tracking, env-wins would silently overwrite the rotated secret
  // and trigger an irrecoverable 30-min auth backoff.
  const original = process.env.A2A_NODE_SECRET;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    const store = makeStore({
      node_secret: VALID_HEX64_B,
      node_secret_source: 'hub_rotate',
    });
    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger });

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B, 'hub-rotated store value must win');
    assert.strictEqual(store.getState('node_secret'), VALID_HEX64_B, 'store must NOT be rewritten with stale env');
    assert.strictEqual(
      store.getState('node_secret_source'),
      'hub_rotate',
      'source tag must persist'
    );
    assert.ok(
      logger._calls.warn.some((m) => m.includes('treating env as stale')),
      'should warn that env was disregarded'
    );

    // Repeated reads do NOT re-log.
    mgr.nodeSecret;
    mgr.nodeSecret;
    const warnCount = logger._calls.warn.filter((m) => m.includes('treating env as stale')).length;
    assert.strictEqual(warnCount, 1, 'stale-env warning should be one-shot');
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
  }
});

test('nodeSecret getter: stale in-memory env_seed cannot overwrite newer disk hub_rotate', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'lifecycle-secret-race-'));
  const dir = path.join(root, 'mailbox');
  const oldStore = new MailboxStore(dir);
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    process.env.A2A_NODE_SECRET_VERSION = '1';
    oldStore.setNodeSecretState({
      secret: VALID_HEX64_C,
      version: '2',
      source: 'env_seed',
      envSuppressed: '',
    });

    const freshStore = new MailboxStore(dir);
    freshStore.setNodeSecretState({
      secret: VALID_HEX64_B,
      version: '11',
      source: 'hub_rotate',
      envSuppressed: '',
    });
    freshStore.close();

    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: oldStore, logger });
    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B, 'newer disk hub_rotate secret must win');
    assert.strictEqual(mgr.nodeSecretVersion, 11);

    const finalState = JSON.parse(fs.readFileSync(path.join(dir, 'state.json'), 'utf8'));
    assert.strictEqual(finalState.node_secret, VALID_HEX64_B);
    assert.strictEqual(finalState.node_secret_version, '11');
    assert.strictEqual(finalState.node_secret_source, 'hub_rotate');
    assert.ok(
      logger._calls.warn.some((m) => m.includes('MailboxStore memory differs from disk hub-rotated node_secret')),
      'should warn that stale in-memory state was ignored'
    );
  } finally {
    oldStore.close();
    fs.rmSync(root, { recursive: true, force: true });
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
  }
});

test('_dropLocalSecret: stale in-memory store syncs newer disk hub_rotate before building headers', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalEvoSecret = process.env.EVOMAP_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'lifecycle-secret-drop-race-'));
  const dir = path.join(root, 'mailbox');
  const oldStore = new MailboxStore(dir);
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    delete process.env.EVOMAP_NODE_SECRET;
    process.env.A2A_NODE_SECRET_VERSION = '2';
    delete process.env.EVOMAP_NODE_SECRET_VERSION;

    oldStore.setNodeSecretState({
      secret: VALID_HEX64_A,
      version: '2',
      source: 'hub_rotate',
      envSuppressed: 'existing-marker',
    });

    const freshStore = new MailboxStore(dir);
    freshStore.setNodeSecretState({
      secret: VALID_HEX64_B,
      version: '11',
      source: 'hub_rotate',
      envSuppressed: '',
    });
    freshStore.close();

    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store: oldStore, logger });
    const staleHeaders = mgr._buildHeaders();
    assert.strictEqual(staleHeaders.Authorization, `Bearer ${VALID_HEX64_A}`);
    assert.strictEqual(staleHeaders['X-EvoMap-Node-Secret-Version'], '2');

    mgr._dropLocalSecret('node_secret_invalid');
    const headers = mgr._buildHeaders();

    assert.strictEqual(headers.Authorization, `Bearer ${VALID_HEX64_B}`);
    assert.strictEqual(headers['X-EvoMap-Node-Secret-Version'], '11');
    assert.strictEqual(oldStore.getState('node_secret'), VALID_HEX64_B);
    assert.strictEqual(oldStore.getState('node_secret_version'), '11');
    assert.strictEqual(oldStore.getState('node_secret_source'), 'hub_rotate');
    assert.strictEqual(oldStore.getState('node_secret_env_suppressed'), 'existing-marker');
    assert.ok(
      logger._calls.warn.some((m) => m.includes('local in-memory node_secret is stale')),
      'should warn without logging the secret value'
    );
    const logText = logger._calls.warn.concat(logger._calls.error, logger._calls.log).join('\n');
    assert.strictEqual(logText.includes(VALID_HEX64_A), false, 'old raw secret must not be logged');
    assert.strictEqual(logText.includes(VALID_HEX64_B), false, 'new raw secret must not be logged');
  } finally {
    oldStore.close();
    fs.rmSync(root, { recursive: true, force: true });
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalEvoSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
    else process.env.EVOMAP_NODE_SECRET = originalEvoSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
  }
});

test('nodeSecret getter: persistent env suppression survives manager restart', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    process.env.A2A_NODE_SECRET_VERSION = '1';
    const store = makeStore({ node_secret_env_suppressed: 'true' });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    assert.strictEqual(mgr.nodeSecret, null, 'suppressed env secret must not be restored after restart');
    assert.strictEqual(mgr.nodeSecretVersion, null, 'suppressed env version must not be emitted');
    assert.strictEqual(mgr._buildHeaders().Authorization, undefined, 'headers must stay unauthenticated');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
  }
});

test('nodeSecret getter: fingerprinted suppression keeps unchanged env suppressed', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    process.env.A2A_NODE_SECRET_VERSION = '1';
    const store = makeStore({ node_secret_env_suppressed: suppressionMarker(VALID_HEX64_A) });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    assert.strictEqual(mgr.nodeSecret, null, 'same env secret must stay suppressed after restart');
    assert.strictEqual(mgr.nodeSecretVersion, null, 'same env version must stay suppressed after restart');
    assert.strictEqual(mgr._buildHeaders().Authorization, undefined, 'headers must stay unauthenticated');
    assert.strictEqual(
      store.getState('node_secret_env_suppressed'),
      suppressionMarker(VALID_HEX64_A),
      'same-env suppression marker must remain'
    );
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
  }
});

test('nodeSecret getter: changed env clears fingerprinted suppression and syncs store', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_B;
    process.env.A2A_NODE_SECRET_VERSION = '8';
    const store = makeStore({
      node_secret: VALID_HEX64_A,
      node_secret_version: '5',
      node_secret_source: 'hub_rotate',
      node_secret_env_suppressed: suppressionMarker(VALID_HEX64_A),
    });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const headers = mgr._buildHeaders();

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B, 'changed env secret must become active');
    assert.strictEqual(store.getState('node_secret'), VALID_HEX64_B, 'store must sync changed env secret');
    assert.strictEqual(store.getState('node_secret_version'), '8', 'store must sync changed env version');
    assert.strictEqual(store.getState('node_secret_source'), 'env_seed', 'store source must become env_seed');
    assert.strictEqual(store.getState('node_secret_env_suppressed'), '', 'changed env must clear suppression marker');
    assert.strictEqual(headers.Authorization, `Bearer ${VALID_HEX64_B}`);
    assert.strictEqual(headers['X-EvoMap-Node-Secret-Version'], '8');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
  }
});

test('nodeSecret getter: changed env matching hub-rotated store keeps hub source', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_B;
    process.env.A2A_NODE_SECRET_VERSION = '8';
    const store = makeStore({
      node_secret: VALID_HEX64_B,
      node_secret_version: '5',
      node_secret_source: 'hub_rotate',
      node_secret_env_suppressed: suppressionMarker(VALID_HEX64_A),
    });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const headers = mgr._buildHeaders();

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B, 'matching env secret can be used');
    assert.strictEqual(store.getState('node_secret'), VALID_HEX64_B, 'store secret must stay unchanged');
    assert.strictEqual(store.getState('node_secret_version'), '5', 'hub-rotated store version must stay authoritative');
    assert.strictEqual(store.getState('node_secret_source'), 'hub_rotate', 'store source must remain hub_rotate');
    assert.strictEqual(store.getState('node_secret_env_suppressed'), '', 'changed env must still clear suppression marker');
    assert.strictEqual(headers.Authorization, `Bearer ${VALID_HEX64_B}`);
    assert.strictEqual(headers['X-EvoMap-Node-Secret-Version'], '5');

    process.env.A2A_NODE_SECRET = VALID_HEX64_C;
    process.env.A2A_NODE_SECRET_VERSION = '9';

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B, 'hub-rotated store must still win over later stale env');
    assert.strictEqual(mgr.nodeSecretVersion, 5);
    assert.strictEqual(store.getState('node_secret_source'), 'hub_rotate', 'source tag must persist after stale env read');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
  }
});

test('nodeSecretVersion getter: env secret without env version does not reuse stale store version', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    delete process.env.A2A_NODE_SECRET_VERSION;
    delete process.env.EVOMAP_NODE_SECRET_VERSION;
    const store = makeStore({
      node_secret: VALID_HEX64_B,
      node_secret_version: '8',
      node_secret_source: 'env_seed',
    });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_A, 'env secret should still win for auth');
    assert.strictEqual(mgr.nodeSecretVersion, null, 'stale store version must not follow a different env secret');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
  }
});

test('nodeSecretVersion getter: hub-rotated store without version does not reuse stale env version', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalEvoSecret = process.env.EVOMAP_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    delete process.env.EVOMAP_NODE_SECRET;
    process.env.A2A_NODE_SECRET_VERSION = '1';
    delete process.env.EVOMAP_NODE_SECRET_VERSION;
    const store = makeStore({
      node_secret: VALID_HEX64_B,
      node_secret_source: 'hub_rotate',
    });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B, 'hub-rotated store secret should win');
    assert.strictEqual(mgr.nodeSecretVersion, null, 'stale env version must not follow hub-rotated store secret');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalEvoSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
    else process.env.EVOMAP_NODE_SECRET = originalEvoSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
  }
});

test('nodeSecretVersion getter: orphan env version does not attach to store secret', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalEvoSecret = process.env.EVOMAP_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
  try {
    delete process.env.A2A_NODE_SECRET;
    delete process.env.EVOMAP_NODE_SECRET;
    process.env.A2A_NODE_SECRET_VERSION = '1';
    delete process.env.EVOMAP_NODE_SECRET_VERSION;
    const store = makeStore({
      node_secret: VALID_HEX64_B,
      node_secret_source: 'hub_rotate',
    });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B, 'store secret should still be usable');
    assert.strictEqual(mgr.nodeSecretVersion, null, 'orphan env version must not describe store secret');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalEvoSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
    else process.env.EVOMAP_NODE_SECRET = originalEvoSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
  }
});

test('nodeSecretVersion getter: EVOMAP_NODE_SECRET pair is source-bound', () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalEvoSecret = process.env.EVOMAP_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
  try {
    delete process.env.A2A_NODE_SECRET;
    delete process.env.A2A_NODE_SECRET_VERSION;
    process.env.EVOMAP_NODE_SECRET = VALID_HEX64_A;
    process.env.EVOMAP_NODE_SECRET_VERSION = '9';
    const store = makeStore({
      node_secret: VALID_HEX64_B,
      node_secret_version: '8',
      node_secret_source: 'env_seed',
    });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_A, 'EVOMAP env secret should win like A2A env secret');
    assert.strictEqual(mgr.nodeSecretVersion, 9, 'EVOMAP env version must stay paired with EVOMAP env secret');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalEvoSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
    else process.env.EVOMAP_NODE_SECRET = originalEvoSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
  }
});

test('hello: successful response without node_secret_version clears stale store version', async () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
  const originalFetch = global.fetch;
  try {
    delete process.env.A2A_NODE_SECRET;
    delete process.env.A2A_NODE_SECRET_VERSION;
    delete process.env.EVOMAP_NODE_SECRET_VERSION;
    const store = makeStore({
      node_id: 'node_test',
      node_secret: VALID_HEX64_A,
      node_secret_version: '7',
      node_secret_source: 'hub_rotate',
    });
    global.fetch = mockFetch(() => responseFromJson({
      status: 200,
      json: { payload: { status: 'acknowledged', your_node_id: 'node_test' } },
    }));

    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.hello();

    assert.strictEqual(result.ok, true);
    assert.strictEqual(store.getState('node_secret_version'), '', 'missing version from hub must clear stale store version');
    assert.strictEqual(mgr.nodeSecretVersion, null, 'cleared store must not keep emitting version metadata');
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
    global.fetch = originalFetch;
  }
});

test('hello: successful response with node_secret_version refreshes store version without rotating secret', async () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
  const originalFetch = global.fetch;
  try {
    delete process.env.A2A_NODE_SECRET;
    delete process.env.A2A_NODE_SECRET_VERSION;
    delete process.env.EVOMAP_NODE_SECRET_VERSION;
    const store = makeStore({
      node_id: 'node_test',
      node_secret: VALID_HEX64_A,
      node_secret_version: '7',
      node_secret_source: 'hub_rotate',
    });
    global.fetch = mockFetch(() => responseFromJson({
      status: 200,
      json: { payload: { status: 'acknowledged', node_secret_version: 9, your_node_id: 'node_test' } },
    }));

    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.hello();

    assert.strictEqual(result.ok, true);
    assert.strictEqual(store.getState('node_secret_version'), '9', 'hub-returned version must be stored');
    assert.strictEqual(mgr.nodeSecretVersion, 9);
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
    global.fetch = originalFetch;
  }
});

test('heartbeat auth failure logs sanitized Hub response body', async () => {
  const original = process.env.A2A_NODE_SECRET;
  const originalFetch = global.fetch;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    const raw = {
      nodeSecret: 'f'.repeat(64),
      bearer: 'Bearer ' + 'g'.repeat(64),
      token: 'tok_' + 'h'.repeat(40),
      envPath: '.env.local',
    };
    const body = {
      error: 'node_secret_invalid',
      node_secret: raw.nodeSecret,
      token: raw.token,
      detail: `${raw.bearer} from ${raw.envPath}`,
    };
    raw.body = JSON.stringify(body);
    global.fetch = mockFetch(() => responseFromJson({ status: 403, json: body }));

    const store = makeStore({
      node_id: 'node_test',
      node_secret: VALID_HEX64_A,
      node_secret_source: 'env_seed',
    });
    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger });
    const result = await mgr.heartbeat({ _skipReauth: true });

    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.error, 'auth_failed_403');
    const logText = logger._calls.error.join('\n');
    assert.match(logText, /\[lifecycle\] heartbeat auth failed \(403\):/);
    assert.match(logText, /"node_secret":"\[REDACTED\]"/);
    assertNoRawHubResponseSecrets(logText, raw);
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
    global.fetch = originalFetch;
  }
});

test('heartbeat HTTP 426 logs sanitized text while parsing raw body', async () => {
  const original = process.env.A2A_NODE_SECRET;
  const originalFetch = global.fetch;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    const raw = {
      nodeSecret: 'f'.repeat(64),
      bearer: 'Bearer ' + 'g'.repeat(64),
      token: 'tok_' + 'h'.repeat(40),
      envPath: '.env.local',
    };
    const body = {
      error: 'evolver_min_version_required',
      node_secret: raw.nodeSecret,
      token: raw.token,
      detail: `${raw.bearer} from ${raw.envPath}`,
    };
    raw.body = JSON.stringify(body);
    global.fetch = mockFetch(() => responseFromJson({ status: 426, json: body }));

    const store = makeStore({
      node_id: 'node_test',
      node_secret: VALID_HEX64_A,
      node_secret_source: 'env_seed',
    });
    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger });
    const result = await mgr.heartbeat({ _skipReauth: true });

    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.error, 'http_426');
    const logText = logger._calls.warn.concat(logger._calls.error).join('\n');
    assert.match(logText, /\[lifecycle\] heartbeat HTTP 426 without parseable force_update payload:/);
    assert.match(logText, /"node_secret":"\[REDACTED\]"/);
    assertNoRawHubResponseSecrets(logText, raw);
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
    global.fetch = originalFetch;
  }
});

test('nodeSecret getter: malformed env var falls back to store', () => {
  const original = process.env.A2A_NODE_SECRET;
  try {
    process.env.A2A_NODE_SECRET = 'not-a-real-hex64-secret';
    const store = makeStore({ node_secret: VALID_HEX64_B });
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_B);
    assert.strictEqual(store.getState('node_secret'), VALID_HEX64_B, 'store untouched on malformed env');
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
  }
});

test('nodeSecret getter: identical env and store values do not log', () => {
  const original = process.env.A2A_NODE_SECRET;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    const store = makeStore({ node_secret: VALID_HEX64_A });
    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger });

    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_A);
    assert.strictEqual(logger._calls.warn.length, 0, 'no warning when values agree');
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
  }
});

test('reAuthenticate: drops cached secret and retries unauthenticated when hub returns node_id_already_claimed', async () => {
  const original = process.env.A2A_NODE_SECRET;
  const originalFetch = global.fetch;
  try {
    delete process.env.A2A_NODE_SECRET;
    const store = makeStore({ node_id: 'node_test', node_secret: VALID_HEX64_A });
    let secondHelloAuthHeader;

    const mf = mockFetch((nthCall, opts) => {
      if (nthCall === 1) {
        // attempt 1: rotate hello with current bearer -> rejected
        return responseFromJson({
          status: 200,
          json: { payload: { status: 'rejected', reason: 'node_id_already_claimed: belongs to another user' } },
        });
      }
      if (nthCall === 2) {
        secondHelloAuthHeader = opts?.headers ? opts.headers.Authorization : 'NO_HEADERS';
        // attempt 2: bearer was dropped, hub still rejects (truly disowned)
        return responseFromJson({
          status: 200,
          json: { payload: { status: 'rejected', reason: 'node_id_already_claimed: belongs to another user' } },
        });
      }
      return responseFromJson({ status: 500, json: { error: 'unexpected_extra_call' } });
    });
    global.fetch = mf;

    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.reAuthenticate();

    assert.strictEqual(result, false);
    assert.strictEqual(mf.calls.length, 2, 'should attempt twice (once with bearer, once without)');
    assert.ok(
      secondHelloAuthHeader === undefined,
      `second hello must NOT carry an Authorization header (got: ${JSON.stringify(secondHelloAuthHeader)})`
    );
    assert.strictEqual(store.getState('node_secret'), '', 'cached secret must be cleared');
    assert.strictEqual(store.getState('node_secret_env_suppressed'), '', 'no env means no persistent suppression marker');
    assert.strictEqual(
      store.getState('node_secret_source'),
      '',
      'source tag must be cleared too -- nothing in store, nothing to attribute'
    );
    assert.ok(mgr._reauthBackoffUntil > Date.now(), '30-min backoff still set after manual reset path');
    assert.ok(
      store._inbound.some((e) => e?.payload?.action === 'manual_secret_reset_required'),
      'should emit manual_secret_reset_required system event'
    );
    assert.match(
      store._inbound.find((e) => e?.payload?.action === 'manual_secret_reset_required').payload.message,
      /evolver reset-local-secret/,
      'manual reset event should recommend reset-local-secret'
    );
    assert.match(
      store._inbound.find((e) => e?.payload?.action === 'manual_secret_reset_required').payload.message,
      /suppression state/,
      'manual reset event should mention suppression state'
    );
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
    global.fetch = originalFetch;
  }
});

test('hello: maps stale-secret HTTP auth reasons to stable divergence error without leaking body', async () => {
  const original = process.env.A2A_NODE_SECRET;
  const originalFetch = global.fetch;
  const cases = [
    {
      status: 401,
      reason: 'node_secret_invalid',
      body: (raw) => ({
        error: 'node_secret_invalid',
        node_secret: raw.nodeSecret,
        token: raw.token,
        detail: `${raw.bearer} from ${raw.envPath}`,
      }),
    },
    {
      status: 403,
      reason: 'invalid_secret',
      body: (raw) => ({
        reason: 'invalid_secret',
        node_secret: raw.nodeSecret,
        token: raw.token,
        detail: `${raw.bearer} from ${raw.envPath}`,
      }),
    },
    {
      status: 403,
      reason: 'rotation_requires_current_secret',
      body: (raw) => ({
        payload: {
          reason: 'rotation_requires_current_secret',
        },
        node_secret: raw.nodeSecret,
        token: raw.token,
        detail: `${raw.bearer} from ${raw.envPath}`,
      }),
    },
  ];
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    for (const c of cases) {
      const raw = {
        nodeSecret: 'f'.repeat(64),
        bearer: 'Bearer ' + 'g'.repeat(64),
        token: 'tok_' + 'h'.repeat(40),
        envPath: '.env.local',
      };
      const body = c.body(raw);
      raw.body = JSON.stringify(body);
      const mf = mockFetch(() => responseFromJson({ status: c.status, json: body }));
      global.fetch = mf;
      const store = makeStore({ node_id: 'node_test', node_secret: VALID_HEX64_A });
      const logger = silentLogger();
      const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger });

      const result = await mgr.hello({ rotateSecret: true });

      assert.strictEqual(result.ok, false);
      assert.strictEqual(result.error, 'secret_diverged_cleared');
      assert.strictEqual(result.reason, c.reason);
      assert.strictEqual(result.statusCode, c.status);
      assert.strictEqual(mf.calls.length, 1);
      assert.strictEqual(
        mf.calls[0].opts.headers.Authorization,
        `Bearer ${VALID_HEX64_A}`,
        'first rotate hello should still present the current local secret'
      );
      const logText = logger._calls.warn.concat(logger._calls.error).join('\n');
      assert.match(logText, new RegExp(`reason=${c.reason}`));
      assertNoRawHubResponseSecrets(logText, raw);
    }
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
    global.fetch = originalFetch;
  }
});

test('reAuthenticate: hello secret divergence drops local secret before unauthenticated retry', async () => {
  const originalSecret = process.env.A2A_NODE_SECRET;
  const originalVersion = process.env.A2A_NODE_SECRET_VERSION;
  const originalFetch = global.fetch;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_A;
    process.env.A2A_NODE_SECRET_VERSION = '2';
    const store = makeStore({
      node_id: 'node_test',
      node_secret: VALID_HEX64_A,
      node_secret_version: '2',
      node_secret_source: 'env_seed',
    });
    const raw = {
      nodeSecret: 'f'.repeat(64),
      bearer: 'Bearer ' + 'g'.repeat(64),
      token: 'tok_' + 'h'.repeat(40),
      envPath: '.env.local',
    };
    const divergenceBody = {
      error: 'node_secret_invalid',
      node_secret: raw.nodeSecret,
      token: raw.token,
      detail: `${raw.bearer} from ${raw.envPath}`,
    };
    raw.body = JSON.stringify(divergenceBody);

    const mf = mockFetch((nthCall) => {
      if (nthCall === 1) {
        return responseFromJson({ status: 401, json: divergenceBody });
      }
      if (nthCall === 2) {
        return responseFromJson({
          status: 200,
          json: {
            payload: {
              status: 'acknowledged',
              node_secret: VALID_HEX64_B,
              node_secret_version: 5,
              your_node_id: 'node_test',
            },
          },
        });
      }
      return responseFromJson({ status: 200, json: { status: 'ok' } });
    });
    global.fetch = mf;

    const logger = silentLogger();
    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger });
    const result = await mgr.reAuthenticate();

    assert.strictEqual(result, true, 'second unauthenticated rotate should recover auth');
    assert.strictEqual(mf.calls.length, 3, 'expect failed hello + unauth hello + verification heartbeat');
    assert.match(mf.calls[0].url, /\/a2a\/hello$/);
    assert.strictEqual(mf.calls[0].opts.headers.Authorization, `Bearer ${VALID_HEX64_A}`);
    assert.strictEqual(mf.calls[0].opts.headers['X-EvoMap-Node-Secret-Version'], '2');
    assert.match(mf.calls[1].url, /\/a2a\/hello$/);
    assert.strictEqual(
      mf.calls[1].opts.headers.Authorization,
      undefined,
      'second rotate hello must not carry the stale Authorization header'
    );
    assert.strictEqual(
      mf.calls[1].opts.headers['X-EvoMap-Node-Secret-Version'],
      undefined,
      'second rotate hello must not carry the stale secret version header'
    );
    assert.strictEqual(JSON.parse(mf.calls[1].opts.body).payload.rotate_secret, true);
    assert.match(mf.calls[2].url, /\/a2a\/heartbeat$/);
    assert.strictEqual(mf.calls[2].opts.headers.Authorization, `Bearer ${VALID_HEX64_B}`);
    assert.strictEqual(mf.calls[2].opts.headers['X-EvoMap-Node-Secret-Version'], '5');
    assert.ok(
      store._sets.some(([key, value]) => key === 'node_secret' && value === ''),
      'dropLocalSecret must clear the cached node_secret before retry'
    );
    assert.ok(
      store._sets.some(([key, value]) => key === 'node_secret_source' && value === ''),
      'dropLocalSecret must clear the cached source before retry'
    );
    assert.strictEqual(store.getState('node_secret'), VALID_HEX64_B);
    assert.strictEqual(store.getState('node_secret_version'), '5');
    assert.strictEqual(store.getState('node_secret_source'), 'hub_rotate');
    assert.strictEqual(
      store.getState('node_secret_env_suppressed'),
      suppressionMarker(VALID_HEX64_A),
      'diverged env secret must stay suppressed after successful retry'
    );
    assert.strictEqual(mgr._reauthBackoffUntil, 0, 'successful divergence recovery must not arm reauth backoff');
    assert.strictEqual(
      store._inbound.filter((e) => e?.payload?.action === 'manual_secret_reset_required').length,
      0,
      'secret divergence recovery must not emit a manual reset event'
    );
    const logText = logger._calls.warn.concat(logger._calls.error, logger._calls.log).join('\n');
    assertNoRawHubResponseSecrets(logText, raw);
  } finally {
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    global.fetch = originalFetch;
  }
});

test('reAuthenticate: env var does NOT undo a successful rotation during verification heartbeat (Bugbot #22)', async () => {
  // Repro:
  //   env A2A_NODE_SECRET = Y (valid, but stale per hub view)
  //   store node_secret   = X (also stale; rewritten to Y by the env-wins path on first read)
  //   hello rotate -> hub returns fresh Z and stores it
  //   verification heartbeat MUST send Bearer Z, not Bearer Y. Without the
  //   _suppressEnvSecret flip in hello, _resolveNodeSecret would see Z (store)
  //   vs Y (env), env-wins, rewrite store back to Y, and sign the heartbeat
  //   with the stale Y -> 403 -> infinite re-auth loop.
  const VALID_HEX64_Y = 'c'.repeat(64);
  const VALID_HEX64_X = 'd'.repeat(64);
  const VALID_HEX64_Z = 'e'.repeat(64);
  const original = process.env.A2A_NODE_SECRET;
  const originalFetch = global.fetch;
  try {
    process.env.A2A_NODE_SECRET = VALID_HEX64_Y;
    const store = makeStore({ node_id: 'node_test', node_secret: VALID_HEX64_X });

    const seenAuthHeaders = [];
    const seenVersionHeaders = [];
    const seenBodies = [];
    const mf = mockFetch((nthCall, opts) => {
      seenAuthHeaders.push(opts?.headers ? opts.headers.Authorization : null);
      seenVersionHeaders.push(opts?.headers ? opts.headers['X-EvoMap-Node-Secret-Version'] : null);
      try { seenBodies.push(opts?.body ? JSON.parse(opts.body) : null); } catch { seenBodies.push(null); }
      if (nthCall === 1) {
        return responseFromJson({
          status: 200,
          json: { payload: { status: 'acknowledged', node_secret: VALID_HEX64_Z, node_secret_version: 4, your_node_id: 'node_test' } },
        });
      }
      return responseFromJson({ status: 200, json: { status: 'ok' } });
    });
    global.fetch = mf;

    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.reAuthenticate();

    assert.strictEqual(result, true, 're-auth must succeed');
    assert.strictEqual(mf.calls.length, 2, 'expect hello + verification heartbeat');
    assert.strictEqual(
      store.getState('node_secret'),
      VALID_HEX64_Z,
      'rotated secret must remain in store after verification heartbeat'
    );
    assert.strictEqual(
      store.getState('node_secret_source'),
      'hub_rotate',
      'rotated secret must be tagged so the next daemon boot can ignore stale shell env'
    );
    assert.strictEqual(
      store.getState('node_secret_env_suppressed'),
      suppressionMarker(VALID_HEX64_Y),
      'successful rotation must suppress only the stale env secret fingerprint'
    );
    assert.strictEqual(store.getState('node_secret_version'), '4', 'rotated secret version must be stored');
    assert.strictEqual(
      seenAuthHeaders[1],
      `Bearer ${VALID_HEX64_Z}`,
      `verification heartbeat must use the freshly rotated secret, not the stale env var (got ${seenAuthHeaders[1]})`
    );
    assert.strictEqual(seenVersionHeaders[1], '4', 'verification heartbeat must carry node secret version header');
    assert.strictEqual(seenBodies[1].node_secret_version, 4, 'verification heartbeat must carry node secret version body');
    assert.strictEqual(seenBodies[1].meta.node_secret_version, 4, 'verification heartbeat must carry node secret version meta');
    assert.strictEqual(mgr._suppressEnvSecret, true, 'env var must be suppressed after a successful rotation');
    // And subsequent reads should keep returning the rotated secret, not the env value.
    assert.strictEqual(mgr.nodeSecret, VALID_HEX64_Z, 'subsequent nodeSecret reads must keep returning Z');
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
    global.fetch = originalFetch;
  }
});

test('reAuthenticate: no manual_reset event when rotate eventually succeeds', async () => {
  const original = process.env.A2A_NODE_SECRET;
  const originalFetch = global.fetch;
  try {
    delete process.env.A2A_NODE_SECRET;
    const store = makeStore({ node_id: 'node_test', node_secret: VALID_HEX64_A });

    const mf = mockFetch((nthCall) => {
      if (nthCall === 1) {
        // hello rotate succeeds with fresh secret
        return responseFromJson({
          status: 200,
          json: { payload: { status: 'acknowledged', node_secret: VALID_HEX64_B, your_node_id: 'node_test' } },
        });
      }
      // heartbeat OK
      return responseFromJson({ status: 200, json: { status: 'ok' } });
    });
    global.fetch = mf;

    const mgr = new LifecycleManager({ hubUrl: 'https://example.test', store, logger: silentLogger() });
    const result = await mgr.reAuthenticate();

    assert.strictEqual(result, true);
    assert.strictEqual(store.getState('node_secret'), VALID_HEX64_B, 'fresh secret persisted');
    assert.strictEqual(
      store.getState('node_secret_source'),
      'hub_rotate',
      'fresh secret must be tagged hub_rotate'
    );
    assert.strictEqual(
      store._inbound.filter((e) => e?.payload?.action === 'manual_secret_reset_required').length,
      0,
      'no manual-reset event on happy recovery'
    );
  } finally {
    if (original === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = original;
    global.fetch = originalFetch;
  }
});
