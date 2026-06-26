'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const Module = require('module');

const CORE_PATH = path.resolve(__dirname, '..', 'src', 'gep', 'recallInject.js');
const HUBSEARCH_PATH = require.resolve('../src/gep/hubSearch');
const ASSETSTORE_PATH = require.resolve('../src/gep/assetStore');
const A2A_PATH = require.resolve('../src/gep/a2aProtocol');
const ASSETLOG_PATH = require.resolve('../src/gep/assetCallLog');

// Load a FRESH copy of recallInject with selected sibling modules stubbed, so
// each test controls the Hub rows / local genes / logging without a network.
function loadCoreWithStubs({ hubRows, localGenes, hubUrl = 'https://hub.test', a2aResolvesEnv = false, onLog } = {}) {
  for (const p of [CORE_PATH, HUBSEARCH_PATH, ASSETSTORE_PATH, A2A_PATH, ASSETLOG_PATH]) {
    delete require.cache[p];
  }
  const origLoad = Module._load;
  const logged = [];
  const stats = { hubCalls: 0 };
  Module._load = function (request, parent, isMain) {
    const resolved = (() => {
      try { return Module._resolveFilename(request, parent, isMain); } catch (_) { return null; }
    })();
    if (resolved === HUBSEARCH_PATH) {
      return {
        getHubUrl: () => hubUrl,
        isSemanticEnabled: () => {
          const v = process.env.HUBSEARCH_SEMANTIC;
          return !(v === 'false' || v === '0');
        },
        fetchSemanticResults: async () => {
          stats.hubCalls++;
          return (Array.isArray(hubRows) ? hubRows : []);
        },
      };
    }
    if (resolved === A2A_PATH) {
      const a2a = { buildHubHeaders: () => ({}), getNodeId: () => 'node_selftest0001' };
      // When a2aResolvesEnv is set, mimic the REAL a2aProtocol.getHubUrl which
      // honors A2A_HUB_URL || EVOMAP_HUB_URL — so we can assert recall resolves
      // the legacy var (Bugbot #183 medium).
      if (a2aResolvesEnv) {
        a2a.getHubUrl = () => process.env.A2A_HUB_URL || process.env.EVOMAP_HUB_URL || '';
      }
      return a2a;
    }
    if (resolved === ASSETSTORE_PATH) {
      return { loadGenes: () => (Array.isArray(localGenes) ? localGenes : []) };
    }
    if (resolved === ASSETLOG_PATH) {
      return { logAssetCall: (e) => { logged.push(e); if (onLog) onLog(e); } };
    }
    return origLoad.apply(this, arguments);
  };
  try {
    const core = require(CORE_PATH);
    return { core, logged, stats, restore: () => { Module._load = origLoad; } };
  } catch (e) {
    Module._load = origLoad;
    throw e;
  }
}

describe('recallInject — mode gating', () => {
  let saved;
  beforeEach(() => { saved = process.env.EVOLVER_RECALL_MODE; });
  afterEach(() => {
    if (saved === undefined) delete process.env.EVOLVER_RECALL_MODE;
    else process.env.EVOLVER_RECALL_MODE = saved;
  });

  it('getMode defaults to off and only accepts shadow/enforce', () => {
    const { core, restore } = loadCoreWithStubs({});
    try {
      delete process.env.EVOLVER_RECALL_MODE;
      assert.equal(core.getMode(), 'off');
      process.env.EVOLVER_RECALL_MODE = 'SHADOW';
      assert.equal(core.getMode(), 'shadow');
      process.env.EVOLVER_RECALL_MODE = 'enforce';
      assert.equal(core.getMode(), 'enforce');
      process.env.EVOLVER_RECALL_MODE = 'garbage';
      assert.equal(core.getMode(), 'off');
    } finally { restore(); }
  });

  it('off mode returns inject:false without searching', async () => {
    const { core, restore } = loadCoreWithStubs({
      hubRows: [{ asset_id: 'a1', _semantic_similarity: 0.99, nl_summary: 'x' }],
    });
    try {
      const r = await core.recallForTask({ prompt: 'add retry with backoff', mode: 'off' });
      assert.equal(r.inject, false);
      assert.equal(r.text, null);
    } finally { restore(); }
  });
});

describe('recallInject — confidence-band gate', () => {
  it('drops Hub rows below the similarity floor (0.75), keeps high band', async () => {
    const { core, restore } = loadCoreWithStubs({
      hubRows: [
        { asset_id: 'low', _semantic_similarity: 0.60, nl_summary: 'low band trap' },
        { asset_id: 'high', _semantic_similarity: 0.88, nl_summary: 'high band hit', short_title: 'Retry backoff' },
      ],
    });
    try {
      const r = await core.recallForTask({ prompt: 'add retry with backoff to http client', mode: 'enforce', timeoutMs: 1000 });
      const ids = r.decided.map(d => d.asset_id);
      assert.ok(ids.includes('high'), 'high-band row must be injected');
      assert.ok(!ids.includes('low'), 'low-band row must be dropped');
    } finally { restore(); }
  });
});

describe('recallInject — shadow vs enforce', () => {
  it('shadow computes + logs but injects nothing (inject:false)', async () => {
    const { core, logged, restore } = loadCoreWithStubs({
      hubRows: [{ asset_id: 'a1', _semantic_similarity: 0.91, nl_summary: 'retry strategy', short_title: 'Retry' }],
    });
    try {
      const r = await core.recallForTask({ prompt: 'add retry with backoff to http client', mode: 'shadow', timeoutMs: 1000 });
      assert.equal(r.inject, false, 'shadow must never inject');
      assert.ok(r.text && r.text.length > 0, 'shadow still computes the would-be text for inspection');
      assert.ok(logged.length >= 1, 'shadow must log the would-be injection');
      assert.equal(logged[0].action, 'asset_inject_shadow', 'shadow logs the shadow action');
    } finally { restore(); }
  });

  it('enforce injects and logs asset_inject', async () => {
    const { core, logged, restore } = loadCoreWithStubs({
      hubRows: [{ asset_id: 'a1', _semantic_similarity: 0.91, nl_summary: 'retry strategy', short_title: 'Retry' }],
    });
    try {
      const r = await core.recallForTask({ prompt: 'add retry with backoff to http client', mode: 'enforce', timeoutMs: 1000 });
      assert.equal(r.inject, true);
      assert.match(r.text, /Evolver — relevant prior capability/);
      assert.match(r.text, /a1/);
      assert.equal(logged[0].action, 'asset_inject');
    } finally { restore(); }
  });
});

describe('recallInject — honors HUBSEARCH_SEMANTIC kill-switch', () => {
  it('skips the Hub call when HUBSEARCH_SEMANTIC=false (local genes still apply)', async () => {
    const saved = process.env.HUBSEARCH_SEMANTIC;
    const { core, stats, restore } = loadCoreWithStubs({
      hubRows: [{ asset_id: 'h', _semantic_similarity: 0.99, nl_summary: 'should not be fetched' }],
      localGenes: [{ type: 'Gene', id: 'g_local', asset_id: 'L1', signals_match: ['retry'], summary: 'local retry' }],
    });
    try {
      process.env.HUBSEARCH_SEMANTIC = 'false';
      const r = await core.recallForTask({ prompt: 'add retry with backoff', mode: 'enforce', timeoutMs: 800 });
      assert.equal(stats.hubCalls, 0, 'no semantic GET when the kill-switch is off');
      // local gene still injected
      assert.ok(r.decided.every(d => d.origin === 'local'), 'only local genes when Hub semantic is disabled');
    } finally {
      if (saved === undefined) delete process.env.HUBSEARCH_SEMANTIC; else process.env.HUBSEARCH_SEMANTIC = saved;
      restore();
    }
  });
});

describe('recallInject — Hub budget bounded by deadline', () => {
  it('skips the Hub call when the absolute deadline leaves too little time', async () => {
    const { core, stats, restore } = loadCoreWithStubs({
      hubRows: [{ asset_id: 'h', _semantic_similarity: 0.99, nl_summary: 'x' }],
      localGenes: [{ type: 'Gene', id: 'g', asset_id: 'L1', signals_match: ['retry'], summary: 'local retry' }],
    });
    try {
      // deadline already (nearly) elapsed -> remaining < 300 -> Hub skipped,
      // but local gene work (done before the await) still produces a result.
      const r = await core.recallForTask({
        prompt: 'add retry with backoff', mode: 'enforce', timeoutMs: 2000, deadlineMs: Date.now() + 50,
      });
      assert.equal(stats.hubCalls, 0, 'Hub call skipped when no budget remains to the deadline');
      assert.equal(r.decided[0].origin, 'local', 'local-gene result still returned');
    } finally { restore(); }
  });
});

describe('recallInject — air-gapped (no hub url) uses local genes only', () => {
  it('returns local gene hit with no Hub url', async () => {
    const { core, restore } = loadCoreWithStubs({
      hubUrl: '', // air-gapped
      localGenes: [
        {
          type: 'Gene',
          id: 'gene_retry_backoff',
          asset_id: 'localasset1',
          signals_match: ['retry', 'backoff'],
          summary: 'exponential backoff retry',
        },
      ],
    });
    try {
      const r = await core.recallForTask({ prompt: 'add retry with backoff to the client', mode: 'enforce', timeoutMs: 500 });
      assert.equal(r.inject, true);
      assert.equal(r.decided[0].origin, 'local');
      assert.equal(r.decided[0].asset_id, 'localasset1');
    } finally { restore(); }
  });
});

describe('recallInject — hub url resolution honors legacy EVOMAP_HUB_URL', () => {
  it('resolves the Hub via a2aProtocol.getHubUrl (A2A_HUB_URL || EVOMAP_HUB_URL)', async () => {
    const savedA = process.env.A2A_HUB_URL;
    const savedE = process.env.EVOMAP_HUB_URL;
    const { core, restore } = loadCoreWithStubs({
      a2aResolvesEnv: true,
      hubRows: [{ asset_id: 'h1', _semantic_similarity: 0.92, nl_summary: 'legacy-var hit', short_title: 'Legacy' }],
    });
    try {
      // Only the LEGACY var set -> recall must still search the Hub.
      delete process.env.A2A_HUB_URL;
      process.env.EVOMAP_HUB_URL = 'https://legacy-hub.test';
      const r = await core.recallForTask({ prompt: 'add retry with backoff to http client', mode: 'enforce', timeoutMs: 800 });
      assert.equal(r.inject, true, 'EVOMAP_HUB_URL alone must still enable Hub recall');
      assert.ok(r.decided.some(d => d.asset_id === 'h1'));
    } finally {
      if (savedA === undefined) delete process.env.A2A_HUB_URL; else process.env.A2A_HUB_URL = savedA;
      if (savedE === undefined) delete process.env.EVOMAP_HUB_URL; else process.env.EVOMAP_HUB_URL = savedE;
      restore();
    }
  });
});

describe('recallInject — dedup local vs hub by asset_id', () => {
  it('does not inject the same asset_id twice', async () => {
    const { core, restore } = loadCoreWithStubs({
      hubRows: [{ asset_id: 'dup', _semantic_similarity: 0.95, nl_summary: 'from hub', short_title: 'Dup' }],
      localGenes: [{ type: 'Gene', id: 'g', asset_id: 'dup', signals_match: ['retry'], summary: 'from local' }],
    });
    try {
      // allow up to 5 so the cap doesn't mask a dedup failure
      process.env.EVOLVER_RECALL_MAX = '5';
      const r = await core.recallForTask({ prompt: 'retry retry retry backoff', mode: 'enforce', timeoutMs: 500 });
      const ids = r.decided.map(d => d.asset_id);
      const dupCount = ids.filter(x => x === 'dup').length;
      assert.equal(dupCount, 1, 'asset_id dup must appear at most once');
    } finally { delete process.env.EVOLVER_RECALL_MAX; restore(); }
  });
});

describe('recallInject — LLM-free invariant (no child_process / no curl)', () => {
  it('extractSignalsPure never spawns a child process', () => {
    // Trip a tripwire if child_process.execFileSync/spawnSync is invoked during
    // signal extraction (would mean the forbidden _extractLLM path ran).
    const cp = require('child_process');
    const origExec = cp.execFileSync;
    const origSpawn = cp.spawnSync;
    let spawned = false;
    cp.execFileSync = () => { spawned = true; return ''; };
    cp.spawnSync = () => { spawned = true; return { status: 0, stdout: '' }; };
    const { core, restore } = loadCoreWithStubs({});
    try {
      const sigs = core.extractSignalsPure('the build keeps failing with a timeout error, please add retry');
      assert.ok(Array.isArray(sigs));
      assert.equal(spawned, false, 'signal extraction must not spawn curl/child_process');
    } finally {
      cp.execFileSync = origExec;
      cp.spawnSync = origSpawn;
      restore();
    }
  });
});

describe('recallInject — fail-open on Hub error', () => {
  it('returns inject:false when fetchSemanticResults throws (no crash)', async () => {
    for (const p of [CORE_PATH, HUBSEARCH_PATH, A2A_PATH, ASSETSTORE_PATH, ASSETLOG_PATH]) delete require.cache[p];
    const origLoad = Module._load;
    Module._load = function (request, parent, isMain) {
      let resolved = null;
      try { resolved = Module._resolveFilename(request, parent, isMain); } catch (_) {}
      if (resolved === HUBSEARCH_PATH) {
        return { getHubUrl: () => 'https://hub.test', fetchSemanticResults: async () => { throw new Error('network down'); } };
      }
      if (resolved === A2A_PATH) return { buildHubHeaders: () => ({}), getNodeId: () => '' };
      if (resolved === ASSETSTORE_PATH) return { loadGenes: () => [] };
      if (resolved === ASSETLOG_PATH) return { logAssetCall: () => {} };
      return origLoad.apply(this, arguments);
    };
    try {
      const core = require(CORE_PATH);
      const r = await core.recallForTask({ prompt: 'add retry with backoff', mode: 'enforce', timeoutMs: 300 });
      assert.equal(r.inject, false);
    } finally { Module._load = origLoad; }
  });
});

describe('recallInject — hollow candidate handling', () => {
  it('injects nothing when the only match has no title and no summary', async () => {
    const { core, restore } = loadCoreWithStubs({
      // a hub row with no title/summary fields at all
      hubRows: [{ asset_id: '', _semantic_similarity: 0.95 }],
    });
    try {
      const r = await core.recallForTask({ prompt: 'add retry with backoff to http client', mode: 'enforce', timeoutMs: 500 });
      assert.equal(r.inject, false, 'a content-less candidate must not be injected');
      assert.equal(r.text, null);
    } finally { restore(); }
  });

  it('log records ONLY rendered assets, never skipped hollow ones (max>1)', async () => {
    // One renderable hub row + one hollow hub row, both above the band, with
    // MAX=5 so both reach `decided`. The hollow one must be excluded from BOTH
    // the injected text and the attribution log (Bugbot #183 low).
    const { core, logged, restore } = loadCoreWithStubs({
      hubRows: [
        { asset_id: 'real', _semantic_similarity: 0.95, nl_summary: 'real strategy', short_title: 'Real' },
        { asset_id: 'hollow', _semantic_similarity: 0.93 }, // no title, no summary
      ],
    });
    try {
      process.env.EVOLVER_RECALL_MAX = '5';
      const r = await core.recallForTask({ prompt: 'add retry with backoff to http client', mode: 'enforce', timeoutMs: 1000 });
      assert.equal(r.inject, true);
      assert.ok(/real/.test(r.text), 'renderable asset must be injected');
      assert.ok(!/hollow/.test(r.text), 'hollow asset must not be injected');
      const loggedIds = logged.map(e => e.asset_id);
      assert.deepEqual(loggedIds, ['real'], 'log must contain ONLY the rendered asset, not the hollow one');
      const decidedIds = r.decided.map(d => d.asset_id);
      assert.deepEqual(decidedIds, ['real'], 'decided must equal the rendered set');
    } finally { delete process.env.EVOLVER_RECALL_MAX; restore(); }
  });

  it('local gene with no summary falls back to signals_match (no dangling colon)', async () => {
    const { core, restore } = loadCoreWithStubs({
      hubUrl: '',
      localGenes: [{ type: 'Gene', id: 'gene_repair', asset_id: '', signals_match: ['log_error', 'test_failure'] }],
    });
    try {
      const r = await core.recallForTask({ prompt: 'the build keeps failing with a log_error', mode: 'enforce', timeoutMs: 500 });
      assert.equal(r.inject, true);
      assert.match(r.text, /matches: log_error/);
      assert.ok(!/: \n/.test(r.text) && !/\): $/m.test(r.text), 'no dangling colon for empty summary');
      assert.ok(!/gep_reuse/.test(r.text), 'unpublished local gene must not advertise gep_reuse');
    } finally { restore(); }
  });
});

describe('recallInject — char ceiling', () => {
  it('clips injected text to the hard ceiling', async () => {
    const big = 'x'.repeat(5000);
    const { core, restore } = loadCoreWithStubs({
      hubRows: [{ asset_id: 'a1', _semantic_similarity: 0.91, nl_summary: big, short_title: 'Big' }],
    });
    try {
      const r = await core.recallForTask({ prompt: 'add retry with backoff to http client', mode: 'enforce', timeoutMs: 500 });
      assert.ok(r.text.length <= 800, 'injected text must respect the 800-char ceiling');
    } finally { restore(); }
  });
});
