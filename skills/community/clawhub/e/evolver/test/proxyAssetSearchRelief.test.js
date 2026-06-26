'use strict';

// Unit tests for the proxy's client-side asset-search relief: fresh-cache
// short-circuit, concurrent dedup, node_id attribution, and Retry-After-aware
// cooldown. We exercise the methods on a bare prototype instance with a stubbed
// _proxyHttp so there is no hub/network/disk dependency.

const { test } = require('node:test');
const assert = require('node:assert');
const { EvoMapProxy, parseRetryAfterMs } = require('../src/proxy/index.js');

function makeProxy(proxyHttpImpl, { nodeId = 'node_test' } = {}) {
  const p = Object.create(EvoMapProxy.prototype);
  p._searchCache = new Map();
  p._searchInflight = new Map();
  p._searchCooldownUntil = 0;
  p.store = { getState: (k) => (k === 'node_id' ? nodeId : undefined) };
  p.logger = { warn() {} };
  let calls = 0;
  p._proxyHttp = async (...args) => { calls += 1; return proxyHttpImpl(...args); };
  Object.defineProperty(p, '_calls', { get: () => calls });
  return p;
}

test('injects this node_id into the search query for hub attribution', async () => {
  let seenQuery = null;
  const p = makeProxy(async (_path, _body, opts) => { seenQuery = opts.query; return { assets: [] }; });
  await p._assetSearch({ signals: ['perf'] });
  assert.equal(seenQuery.node_id, 'node_test');
  assert.equal(seenQuery.signals, 'perf');
});

test('always attributes to the proxy own node_id (anti-impersonation)', async () => {
  let seenQuery = null;
  const p = makeProxy(async (_path, _body, opts) => { seenQuery = opts.query; return { assets: [] }; });
  // A caller cannot attribute its search to another node through the proxy.
  await p._assetSearch({ signals: ['perf'], node_id: 'node_explicit' });
  assert.equal(seenQuery.node_id, 'node_test');
});

test('fresh cache hit serves from cache without a second request', async () => {
  const p = makeProxy(async () => ({ assets: [{ asset_id: 'a1' }] }));
  const first = await p._assetSearch({ signals: ['perf'] });
  const second = await p._assetSearch({ signals: ['perf'] });
  assert.equal(p._calls, 1);
  assert.deepEqual(second, first);
});

test('different signals are cached independently', async () => {
  const p = makeProxy(async (_path, _body, opts) => ({ assets: [], echo: opts.query.signals }));
  await p._assetSearch({ signals: ['a'] });
  await p._assetSearch({ signals: ['b'] });
  assert.equal(p._calls, 2);
});

test('concurrent identical searches collapse into one request', async () => {
  let resolveHub;
  const p = makeProxy(() => new Promise((r) => { resolveHub = r; }));
  const a = p._assetSearch({ signals: ['perf'] });
  const b = p._assetSearch({ signals: ['perf'] });
  resolveHub({ assets: [{ asset_id: 'x' }] });
  const [ra, rb] = await Promise.all([a, b]);
  assert.equal(p._calls, 1);
  assert.deepEqual(ra, rb);
});

test('429 sets a cooldown that short-circuits the next search without a request', async () => {
  const p = makeProxy(async () => {
    throw Object.assign(new Error('Hub 429'), { statusCode: 429, retryAfterMs: 60_000 });
  });
  await assert.rejects(p._assetSearch({ signals: ['perf'] }), (e) => e.statusCode === 429);
  assert.equal(p._calls, 1);

  // Second call (different signals) must NOT hit the network while cooling down.
  await assert.rejects(
    p._assetSearch({ signals: ['other'] }),
    (e) => e.statusCode === 429 && e.fromCooldown === true && e.retryAfterMs > 0,
  );
  assert.equal(p._calls, 1);
});

test('during cooldown a previously-cached query is served stale instead of failing', async () => {
  let mode = 'ok';
  const p = makeProxy(async (_path, _body, opts) => {
    if (mode === '429') throw Object.assign(new Error('Hub 429'), { statusCode: 429, retryAfterMs: 60_000 });
    return { assets: [{ asset_id: 'cached' }], echo: opts.query.signals };
  });
  // Warm the cache for signals=['warm'].
  const warm = await p._assetSearch({ signals: ['warm'] });
  // Force expiry so it is no longer a "fresh" hit, then enter cooldown.
  p._searchCache.get(p._assetSearchCacheKey({ path: '/a2a/assets/search', query: { node_id: 'node_test', signals: 'warm' } })).expiresAt = Date.now() - 1;
  mode = '429';
  await assert.rejects(p._assetSearch({ signals: ['trigger'] }), (e) => e.statusCode === 429);
  // Now cooling down; the warm query should return its stale cached value.
  const stale = await p._assetSearch({ signals: ['warm'] });
  assert.deepEqual(stale, warm);
});

test('parseRetryAfterMs prefers JSON retry_after_ms, falls back to Retry-After header', () => {
  const noHdr = { headers: { get: () => null } };
  assert.equal(parseRetryAfterMs(noHdr, JSON.stringify({ retry_after_ms: 4200 })), 4200);
  const hdr = { headers: { get: (n) => (n === 'retry-after' ? '7' : null) } };
  assert.equal(parseRetryAfterMs(hdr, 'not json'), 7000);
  assert.equal(parseRetryAfterMs(noHdr, ''), 0);
});
