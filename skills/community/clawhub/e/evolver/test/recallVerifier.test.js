'use strict';

// recallVerifier tests — drive the worker synchronously via _runWorkerOnce
// with stubbed global.fetch. tmpDir-isolated memoryGraph so each case
// starts fresh.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

function loadFresh() {
  delete require.cache[require.resolve('../src/gep/recallVerifier')];
  delete require.cache[require.resolve('../src/gep/hubSearch')];
  delete require.cache[require.resolve('../src/gep/memoryGraph')];
  delete require.cache[require.resolve('../src/gep/a2aProtocol')];
  return require('../src/gep/recallVerifier');
}

async function withFetchMock(impl, fn) {
  const original = global.fetch;
  global.fetch = impl;
  try {
    return await fn();
  } finally {
    global.fetch = original;
  }
}

function setupTmpGraph() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'recall-verify-test-'));
  const memDir = path.join(tmpDir, 'memory');
  const evoDir = path.join(tmpDir, 'evolution');
  const gepDir = path.join(evoDir, 'gep');
  fs.mkdirSync(memDir, { recursive: true });
  fs.mkdirSync(gepDir, { recursive: true });
  process.env.MEMORY_DIR = memDir;
  process.env.EVOLUTION_DIR = evoDir;
  process.env.EVOLVER_REPO_ROOT = tmpDir;
  return { tmpDir, memDir, evoDir, gepDir };
}

function readEvents(evoDir) {
  const file = path.join(evoDir, 'memory_graph.jsonl');
  if (!fs.existsSync(file)) return [];
  return fs.readFileSync(file, 'utf8').trim().split('\n').filter(Boolean).map(function (l) {
    try { return JSON.parse(l); } catch (_) { return null; }
  }).filter(Boolean);
}

const ENV_KEYS = [
  'EVOLVE_RECALL_VERIFY',
  'EVOLVE_RECALL_VERIFY_SAMPLE_RATE',
  'EVOLVE_RECALL_VERIFY_QUEUE_MAX',
  'EVOLVE_RECALL_VERIFY_INITIAL_WAIT_MS',
  'EVOLVE_RECALL_VERIFY_ATTEMPTS',
  'EVOLVE_RECALL_VERIFY_FETCH_TIMEOUT_MS',
  'A2A_HUB_URL',
  'A2A_NODE_SECRET',
  'EVOMAP_HUB_ALLOW_INSECURE',
  'MEMORY_DIR',
  'EVOLUTION_DIR',
  'EVOLVER_REPO_ROOT',
];

describe('recallVerifier.enqueuePublishedAsset', () => {
  let savedEnv = {};
  let ctx;

  beforeEach(() => {
    savedEnv = {};
    for (const k of ENV_KEYS) savedEnv[k] = process.env[k];
    ctx = setupTmpGraph();
    process.env.EVOLVE_RECALL_VERIFY = '1';
    process.env.EVOLVE_RECALL_VERIFY_INITIAL_WAIT_MS = '0';
    process.env.EVOLVE_RECALL_VERIFY_ATTEMPTS = '3';
    process.env.A2A_HUB_URL = 'http://localhost:9999';
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });

  afterEach(() => {
    try { fs.rmSync(ctx.tmpDir, { recursive: true, force: true }); } catch (_) {}
    for (const k of ENV_KEYS) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
  });

  it('emits feature_disabled when EVOLVE_RECALL_VERIFY=0', () => {
    process.env.EVOLVE_RECALL_VERIFY = '0';
    const rv = loadFresh();
    rv._resetForTesting();
    const r = rv.enqueuePublishedAsset({ asset_id: 'a1', type: 'Capsule', signals: [], publishedAt: Date.now() });
    assert.equal(r.enqueued, false);
    assert.equal(r.reason, 'feature_disabled');
    const events = readEvents(ctx.evoDir);
    const verify = events.filter(function (e) { return e.kind === 'recall_verify'; });
    assert.equal(verify.length, 1);
    assert.equal(verify[0].verification.outcome, 'verification_skipped');
    assert.equal(verify[0].verification.reason, 'feature_disabled');
  });

  // #136: verifier flipped from default-on (client-side fallback) to opt-in
  // observability after Hub /a2a/fetch contract was confirmed strict (see
  // EvoMap/evomap-hub#669). When EVOLVE_RECALL_VERIFY is unset, enqueue must
  // skip with feature_disabled — not silently run.
  it('is OFF by default when EVOLVE_RECALL_VERIFY is unset', () => {
    delete process.env.EVOLVE_RECALL_VERIFY;
    const rv = loadFresh();
    rv._resetForTesting();
    const r = rv.enqueuePublishedAsset({ asset_id: 'a1', type: 'Capsule', signals: [], publishedAt: Date.now() });
    assert.equal(r.enqueued, false);
    assert.equal(r.reason, 'feature_disabled');
  });

  it('emits sample_rate when sample roll fails', () => {
    process.env.EVOLVE_RECALL_VERIFY_SAMPLE_RATE = '0';
    const rv = loadFresh();
    rv._resetForTesting();
    const r = rv.enqueuePublishedAsset({ asset_id: 'a1', type: 'Capsule', signals: [], publishedAt: Date.now() });
    assert.equal(r.enqueued, false);
    assert.equal(r.reason, 'sample_rate');
    const events = readEvents(ctx.evoDir);
    const verify = events.filter(function (e) { return e.kind === 'recall_verify'; });
    assert.equal(verify.length, 1);
    assert.equal(verify[0].verification.reason, 'sample_rate');
  });

  // Bugbot review on PR #53 round 3 caught this: a negative sample rate
  // would silently disable verification (Math.random() >= -0.5 is always
  // true → every asset skipped) while the startup banner still showed 1.0
  // because index.js does its own range clamp. Now both the banner and
  // _getSampleRate() agree: out-of-range → 1.0.
  it('treats out-of-range sample rate (negative) as 1.0', () => {
    process.env.EVOLVE_RECALL_VERIFY_SAMPLE_RATE = '-0.5';
    const rv = loadFresh();
    rv._resetForTesting();
    const r = rv.enqueuePublishedAsset({ asset_id: 'a1', type: 'Capsule', signals: [], publishedAt: Date.now() });
    // With sample_rate clamped to 1.0, the asset MUST be enqueued
    // (Math.random() < 1.0 is always true).
    assert.equal(r.enqueued, true);
  });

  it('treats out-of-range sample rate (>1) as 1.0', () => {
    process.env.EVOLVE_RECALL_VERIFY_SAMPLE_RATE = '5';
    const rv = loadFresh();
    rv._resetForTesting();
    const r = rv.enqueuePublishedAsset({ asset_id: 'a2', type: 'Capsule', signals: [], publishedAt: Date.now() });
    assert.equal(r.enqueued, true);
  });

  it('treats non-numeric sample rate as 1.0', () => {
    process.env.EVOLVE_RECALL_VERIFY_SAMPLE_RATE = 'banana';
    const rv = loadFresh();
    rv._resetForTesting();
    const r = rv.enqueuePublishedAsset({ asset_id: 'a3', type: 'Capsule', signals: [], publishedAt: Date.now() });
    assert.equal(r.enqueued, true);
  });

  it('emits missing_asset_id when asset_id is null', () => {
    const rv = loadFresh();
    rv._resetForTesting();
    const r = rv.enqueuePublishedAsset({ asset_id: null, type: 'Capsule', signals: [], publishedAt: Date.now() });
    assert.equal(r.enqueued, false);
    assert.equal(r.reason, 'missing_asset_id');
    const events = readEvents(ctx.evoDir);
    const verify = events.filter(function (e) { return e.kind === 'recall_verify'; });
    assert.equal(verify.length, 1);
    assert.equal(verify[0].verification.reason, 'missing_asset_id');
  });

  it('drops oldest with queue_full reason when queue at max', () => {
    process.env.EVOLVE_RECALL_VERIFY_QUEUE_MAX = '2';
    const rv = loadFresh();
    rv._resetForTesting();
    rv.enqueuePublishedAsset({ asset_id: 'a1', type: 'Capsule', signals: [], publishedAt: 1000 });
    rv.enqueuePublishedAsset({ asset_id: 'a2', type: 'Capsule', signals: [], publishedAt: 2000 });
    rv.enqueuePublishedAsset({ asset_id: 'a3', type: 'Capsule', signals: [], publishedAt: 3000 });
    const events = readEvents(ctx.evoDir);
    const dropped = events.filter(function (e) { return e.kind === 'recall_verify' && e.verification.reason === 'queue_full'; });
    assert.equal(dropped.length, 1);
    assert.equal(dropped[0].asset.id, 'a1');
    assert.equal(rv._getQueueLengthForTesting(), 2);
  });
});

describe('recallVerifier.verifyOnce', () => {
  let savedEnv = {};
  let ctx;
  beforeEach(() => {
    savedEnv = {};
    for (const k of ENV_KEYS) savedEnv[k] = process.env[k];
    ctx = setupTmpGraph();
    process.env.EVOLVE_RECALL_VERIFY = '1';
    process.env.A2A_HUB_URL = 'http://localhost:9999';
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    try { fs.rmSync(ctx.tmpDir, { recursive: true, force: true }); } catch (_) {}
    for (const k of ENV_KEYS) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
  });

  it('returns roundtrip_ok when fetched asset hash matches recompute', async () => {
    const { computeAssetId } = require('../src/gep/contentHash');
    const asset = { type: 'Capsule', id: 'cap1', payload: { x: 1 } };
    asset.asset_id = computeAssetId(asset);
    const rv = loadFresh();
    rv._resetForTesting();
    let result;
    await withFetchMock(async function () {
      return {
        ok: true,
        json: async function () { return { payload: { results: [asset] } }; },
      };
    }, async function () {
      result = await rv.verifyOnce(asset.asset_id, 'Capsule');
    });
    assert.equal(result.outcome, 'roundtrip_ok');
    assert.equal(result.recalled_hash, asset.asset_id);
  });

  it('returns roundtrip_missing on empty results', async () => {
    const rv = loadFresh();
    rv._resetForTesting();
    let result;
    await withFetchMock(async function () {
      return {
        ok: true,
        json: async function () { return { payload: { results: [] } }; },
      };
    }, async function () {
      result = await rv.verifyOnce('nonexistent', 'Capsule');
    });
    assert.equal(result.outcome, 'roundtrip_missing');
  });

  it('returns roundtrip_mismatch when recomputed hash differs', async () => {
    // Hub returns an asset whose claimed asset_id differs from its real content hash.
    const asset = { type: 'Capsule', id: 'cap1', payload: { x: 1 }, asset_id: 'forged_hash_value' };
    const rv = loadFresh();
    rv._resetForTesting();
    let result;
    await withFetchMock(async function () {
      return {
        ok: true,
        json: async function () { return { payload: { results: [asset] } }; },
      };
    }, async function () {
      result = await rv.verifyOnce('forged_hash_value', 'Capsule');
    });
    assert.equal(result.outcome, 'roundtrip_mismatch');
    assert.equal(result.reason, 'hash_drift');
  });

  it('returns verification_skipped when fetch throws', async () => {
    const rv = loadFresh();
    rv._resetForTesting();
    let result;
    await withFetchMock(async function () {
      throw new Error('ECONNREFUSED');
    }, async function () {
      result = await rv.verifyOnce('a1', 'Capsule');
    });
    assert.equal(result.outcome, 'verification_skipped');
    assert.equal(result.reason, 'hub_unreachable');
  });
});

describe('recallVerifier._runWorkerOnce', () => {
  let savedEnv = {};
  let ctx;
  beforeEach(() => {
    savedEnv = {};
    for (const k of ENV_KEYS) savedEnv[k] = process.env[k];
    ctx = setupTmpGraph();
    process.env.EVOLVE_RECALL_VERIFY = '1';
    process.env.EVOLVE_RECALL_VERIFY_INITIAL_WAIT_MS = '0';
    process.env.EVOLVE_RECALL_VERIFY_ATTEMPTS = '3';
    process.env.A2A_HUB_URL = 'http://localhost:9999';
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });
  afterEach(() => {
    try { fs.rmSync(ctx.tmpDir, { recursive: true, force: true }); } catch (_) {}
    for (const k of ENV_KEYS) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
  });

  it('exhausts retries on persistent missing, emits roundtrip_missing terminal', async () => {
    process.env.EVOLVE_RECALL_VERIFY_ATTEMPTS = '1';
    const rv = loadFresh();
    rv._resetForTesting();
    rv.enqueuePublishedAsset({ asset_id: 'gone', type: 'Capsule', signals: [], publishedAt: Date.now() });
    await withFetchMock(async function () {
      return { ok: true, json: async function () { return { payload: { results: [] } }; } };
    }, async function () {
      await rv._runWorkerOnce();
    });
    const events = readEvents(ctx.evoDir);
    const verify = events.filter(function (e) { return e.kind === 'recall_verify'; });
    assert.equal(verify.length, 1);
    assert.equal(verify[0].verification.outcome, 'roundtrip_missing');
    assert.equal(verify[0].verification.attempts, 1);
    assert.equal(rv._getQueueLengthForTesting(), 0);
  });

  it('processes multiple eligible entries in one tick', async () => {
    const { computeAssetId } = require('../src/gep/contentHash');
    process.env.EVOLVE_RECALL_VERIFY_ATTEMPTS = '1';
    const a = { type: 'Capsule', id: 'a', payload: { x: 1 } }; a.asset_id = computeAssetId(a);
    const b = { type: 'Capsule', id: 'b', payload: { x: 2 } }; b.asset_id = computeAssetId(b);
    const rv = loadFresh();
    rv._resetForTesting();
    // publishedAt in the past so entries are immediately eligible regardless of INITIAL_WAIT_MS.
    rv.enqueuePublishedAsset({ asset_id: a.asset_id, type: 'Capsule', signals: [], publishedAt: Date.now() - 60000 });
    rv.enqueuePublishedAsset({ asset_id: b.asset_id, type: 'Capsule', signals: [], publishedAt: Date.now() - 60000 });
    await withFetchMock(async function (url, opts) {
      const body = JSON.parse(opts.body);
      const ids = body && body.payload && body.payload.asset_ids;
      const id = ids && ids[0];
      if (id === a.asset_id) return { ok: true, json: async function () { return { payload: { results: [a] } }; } };
      if (id === b.asset_id) return { ok: true, json: async function () { return { payload: { results: [b] } }; } };
      return { ok: true, json: async function () { return { payload: { results: [] } }; } };
    }, async function () {
      await rv._runWorkerOnce();
    });
    const events = readEvents(ctx.evoDir);
    const verify = events.filter(function (e) { return e.kind === 'recall_verify' && e.verification.outcome === 'roundtrip_ok'; });
    assert.equal(verify.length, 2);
    assert.equal(rv._getQueueLengthForTesting(), 0);
  });

  it('keeps entry queued for retry on missing when attempts left', async () => {
    process.env.EVOLVE_RECALL_VERIFY_ATTEMPTS = '3';
    const rv = loadFresh();
    rv._resetForTesting();
    rv.enqueuePublishedAsset({ asset_id: 'tryagain', type: 'Capsule', signals: [], publishedAt: Date.now() });
    await withFetchMock(async function () {
      return { ok: true, json: async function () { return { payload: { results: [] } }; } };
    }, async function () {
      await rv._runWorkerOnce();
    });
    // After tick 1: missing, but attempts < max. Entry stays queued, no terminal event.
    const events = readEvents(ctx.evoDir);
    const verify = events.filter(function (e) { return e.kind === 'recall_verify'; });
    assert.equal(verify.length, 0, 'no terminal event after first miss');
    assert.equal(rv._getQueueLengthForTesting(), 1, 'entry remains queued for retry');
  });
});
