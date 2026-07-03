'use strict';

// P4-a Slice A — evolver reuse-attribution report (default off, shadow-only).
// Verifies: the flag parsing, the attribution block built from the dispatch
// run-state, the money/identity-safety invariants (no client source_node_id,
// absent when generated, absent when off), and the local-only reuse rollup.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ENV = [
  'EVOLUTION_DIR',
  'MEMORY_DIR',
  'EVOLVER_REPO_ROOT',
  'EVOLVER_HOME',
  'EVOLVER_REUSE_ATTRIBUTION',
  'MEMORY_GRAPH_SYNC_HUB',
  'A2A_HUB_URL',
  'EVOLVER_OUTCOME_REPORT',
  'EVOMAP_HUB_ALLOW_INSECURE',
  'A2A_NODE_SECRET',
  'EVOMAP_NODE_SECRET',
  'A2A_NODE_SECRET_VERSION',
  'EVOMAP_NODE_SECRET_VERSION',
];

function fresh(p) { const r = require.resolve(p); delete require.cache[r]; return require(r); }
function reloadAll() {
  // config + paths are read by memoryGraph; reload so env changes take effect.
  for (const m of ['../src/config', '../src/gep/paths', '../src/gep/a2aProtocol', '../src/gep/assetCallLog', '../src/gep/assetStore', '../src/gep/memoryGraph']) {
    try { delete require.cache[require.resolve(m)]; } catch (_) {}
  }
}

describe('P4-a Slice A — reuse attribution', () => {
  let tmp, saved;
  beforeEach(() => {
    tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-attr-test-'));
    saved = {};
    for (const k of ENV) { saved[k] = process.env[k]; delete process.env[k]; }
    process.env.EVOLUTION_DIR = tmp;
    process.env.EVOLVER_HOME = path.join(tmp, '.evomap');
    reloadAll();
  });
  afterEach(() => {
    for (const k of ENV) { if (saved[k] === undefined) delete process.env[k]; else process.env[k] = saved[k]; }
    fs.rmSync(tmp, { recursive: true, force: true });
    reloadAll();
  });

  // Pipeline order: recordAttempt (last_action) -> dispatch (last_run) ->
  // recordOutcome. So a CURRENT-cycle last_run.created_at is >= last_action's.
  const ACT_AT = '2026-06-03T10:00:00.000Z';
  const RUN_AT_FRESH = '2026-06-03T10:00:05.000Z'; // after the attempt (same cycle)
  const RUN_AT_STALE = '2026-06-03T09:59:00.000Z'; // before the attempt (prior cycle)

  // write evolution_solidify_state.json the way dispatch.js does (state.last_run.*)
  // Defaults created_at to a fresh (same-cycle) timestamp unless the caller sets one.
  function writeRunState(lastRun) {
    const lr = Object.assign({ created_at: RUN_AT_FRESH }, lastRun);
    fs.writeFileSync(path.join(tmp, 'evolution_solidify_state.json'), JSON.stringify({ last_run: lr }));
  }
  // write memory_graph_state.json so recordOutcomeFromState has a last_action
  function writeLastAction() {
    fs.writeFileSync(path.join(tmp, 'memory_graph_state.json'), JSON.stringify({
      last_action: { action_id: 'act_test', signal_key: 'k', signals: ['log_error'], had_error: true, outcome_recorded: false, created_at: ACT_AT },
    }));
  }

  describe('config flag', () => {
    it('defaults to off; only shadow is accepted', () => {
      const cfg = fresh('../src/config');
      assert.equal(cfg.reuseAttributionMode(), 'off');
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'SHADOW';
      assert.equal(cfg.reuseAttributionMode(), 'shadow');
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'enforce'; // no client enforce -> off
      assert.equal(cfg.reuseAttributionMode(), 'off');
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'garbage';
      assert.equal(cfg.reuseAttributionMode(), 'off');
    });
  });

  describe('outcome event gets reuse_attribution only in shadow + on real reuse', () => {
    it('off mode: no reuse_attribution even when a reuse happened', () => {
      // default off
      writeRunState({ source_type: 'reused', reused_asset_id: 'sha256:abc', reused_chain_id: 'chain1', reused_source_node: 'node_pub' });
      writeLastAction();
      const mg = fresh('../src/gep/memoryGraph');
      const ev = mg.recordOutcomeFromState({ signals: [], observations: null });
      assert.ok(ev, 'outcome event produced');
      assert.equal(ev.reuse_attribution, undefined, 'no attribution when off');
    });

    it('shadow + reused: attaches block with runtime asset_id, NO client source_node_id', () => {
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'shadow';
      writeRunState({ source_type: 'reused', reused_asset_id: 'sha256:abc', reused_chain_id: 'chain1', reused_source_node: 'node_pub_DO_NOT_TRUST' });
      writeLastAction();
      const mg = fresh('../src/gep/memoryGraph');
      const ev = mg.recordOutcomeFromState({ signals: [], observations: null });
      assert.ok(ev.reuse_attribution, 'attribution attached in shadow');
      assert.equal(ev.reuse_attribution.reused_asset_id, 'sha256:abc');
      assert.equal(ev.reuse_attribution.reused_chain_id, 'chain1');
      assert.equal(ev.reuse_attribution.source_type, 'reused');
      assert.equal(ev.reuse_attribution.schema, 'reuse_attr/1.0');
      // CRITICAL anti-sybil: never carry the client's claim of who to pay
      assert.ok(!('source_node_id' in ev.reuse_attribution), 'must NOT carry client source_node_id');
      assert.ok(!JSON.stringify(ev.reuse_attribution).includes('node_pub_DO_NOT_TRUST'), 'reuser must not name the payee');
    });

    it('shadow + generated (nothing reused): no block', () => {
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'shadow';
      writeRunState({ source_type: 'generated', reused_asset_id: null });
      writeLastAction();
      const mg = fresh('../src/gep/memoryGraph');
      const ev = mg.recordOutcomeFromState({ signals: [], observations: null });
      assert.equal(ev.reuse_attribution, undefined, 'generated => no attribution');
    });

    it('shadow + reference: attaches block', () => {
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'shadow';
      writeRunState({ source_type: 'reference', reused_asset_id: 'sha256:ref1', reused_chain_id: null });
      writeLastAction();
      const mg = fresh('../src/gep/memoryGraph');
      const ev = mg.recordOutcomeFromState({ signals: [], observations: null });
      assert.ok(ev.reuse_attribution);
      assert.equal(ev.reuse_attribution.source_type, 'reference');
      assert.equal(ev.reuse_attribution.reused_chain_id, null);
    });

    it('shadow + STALE last_run (prior cycle, created_at < last_action): no block (Bugbot #186)', () => {
      // dispatch never ran this cycle -> last_run is from an earlier cycle and
      // must NOT mislink another cycle's reuse to this outcome.
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'shadow';
      writeRunState({ source_type: 'reused', reused_asset_id: 'sha256:STALE', created_at: RUN_AT_STALE });
      writeLastAction();
      const mg = fresh('../src/gep/memoryGraph');
      const ev = mg.recordOutcomeFromState({ signals: [], observations: null });
      assert.equal(ev.reuse_attribution, undefined, 'stale last_run must not attach');
      assert.ok(!JSON.stringify(ev).includes('STALE'), 'no stale asset id leaks into the outcome');
    });

    it('shadow + last_run with no created_at: no block (cannot correlate cycle)', () => {
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'shadow';
      // bypass the helper default to simulate a legacy state w/o created_at
      fs.writeFileSync(path.join(tmp, 'evolution_solidify_state.json'),
        JSON.stringify({ last_run: { source_type: 'reused', reused_asset_id: 'sha256:nocreat' } }));
      writeLastAction();
      const mg = fresh('../src/gep/memoryGraph');
      const ev = mg.recordOutcomeFromState({ signals: [], observations: null });
      assert.equal(ev.reuse_attribution, undefined, 'uncorrelatable last_run must not attach');
    });

    it('shadow but no run-state file: no block, no crash', () => {
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'shadow';
      writeLastAction(); // no evolution_solidify_state.json
      const mg = fresh('../src/gep/memoryGraph');
      const ev = mg.recordOutcomeFromState({ signals: [], observations: null });
      assert.ok(ev, 'still produces the outcome event');
      assert.equal(ev.reuse_attribution, undefined);
    });
  });

  describe('reuseAttributionSummary (local-only rollup)', () => {
    it('aggregates reuse/reference per asset from the local log', () => {
      const acl = fresh('../src/gep/assetCallLog');
      acl.logAssetCall({ run_id: 'r1', action: 'asset_reuse', asset_id: 'A', source_node_id: 'nodeA', chain_id: 'c1' });
      acl.logAssetCall({ run_id: 'r2', action: 'asset_reuse', asset_id: 'A' });
      acl.logAssetCall({ run_id: 'r3', action: 'asset_reference', asset_id: 'B', source_node_id: 'nodeB' });
      acl.logAssetCall({ run_id: 'r4', action: 'hub_search_hit', asset_id: 'C' }); // ignored
      const s = acl.reuseAttributionSummary();
      assert.equal(s.total_reuse, 2);
      assert.equal(s.total_reference, 1);
      const a = s.by_asset.find(x => x.asset_id === 'A');
      assert.equal(a.reuse, 2); assert.equal(a.reference, 0); assert.equal(a.source_node_id, 'nodeA');
      const b = s.by_asset.find(x => x.asset_id === 'B');
      assert.equal(b.reference, 1);
      assert.ok(!s.by_asset.find(x => x.asset_id === 'C'), 'non-reuse actions excluded');
      // sorted by total desc -> A first
      assert.equal(s.by_asset[0].asset_id, 'A');
    });
    it('empty log -> zeroes, no throw', () => {
      const acl = fresh('../src/gep/assetCallLog');
      const s = acl.reuseAttributionSummary();
      assert.equal(s.total_reuse, 0); assert.equal(s.total_reference, 0); assert.deepEqual(s.by_asset, []);
      assert.equal(s.total_tokens_saved, 0);
    });
    it('sums tokens_saved across reuse/reference rows (total + per-asset)', () => {
      const acl = fresh('../src/gep/assetCallLog');
      acl.logAssetCall({ run_id: 'r1', action: 'asset_reuse', asset_id: 'A', tokens_saved: 1000 });
      acl.logAssetCall({ run_id: 'r2', action: 'asset_reuse', asset_id: 'A', tokens_saved: 500 });
      acl.logAssetCall({ run_id: 'r3', action: 'asset_reference', asset_id: 'B', tokens_saved: 200 });
      acl.logAssetCall({ run_id: 'r4', action: 'asset_publish', asset_id: 'A', tokens_spent: 9999 }); // not a reuse
      const s = acl.reuseAttributionSummary();
      assert.equal(s.total_tokens_saved, 1700);
      assert.equal(s.by_asset.find(x => x.asset_id === 'A').tokens_saved, 1500);
      assert.equal(s.by_asset.find(x => x.asset_id === 'B').tokens_saved, 200);
    });
  });

  describe('assetCostIndex (asset_id -> measured tokens_spent)', () => {
    it('maps published assets to their derivation cost; latest wins, untokened skipped', () => {
      const acl = fresh('../src/gep/assetCallLog');
      acl.logAssetCall({ run_id: 'r1', action: 'asset_publish', asset_id: 'A', tokens_spent: 1000 });
      acl.logAssetCall({ run_id: 'r2', action: 'asset_publish', asset_id: 'A', tokens_spent: 1200 });
      acl.logAssetCall({ run_id: 'r3', action: 'asset_publish', asset_id: 'B' }); // no tokens -> skipped
      acl.logAssetCall({ run_id: 'r4', action: 'asset_reuse', asset_id: 'C', tokens_saved: 5 }); // not a publish
      const idx = acl.assetCostIndex();
      assert.equal(idx['A'], 1200);
      assert.ok(!('B' in idx));
      assert.ok(!('C' in idx));
    });
  });

  // P4-a Slice B (client side): opt-in Hub outcome report. Drives the REAL wiring
  // through recordOutcomeFromState and asserts the best-effort POST (stubbed
  // global.fetch via the insecure path, mirroring test/hubEvents.test.js).
  describe('P4-a Slice B — Hub outcome report (EVOLVER_OUTCOME_REPORT, opt-in)', () => {
    let savedFetch, calls;
    beforeEach(() => {
      savedFetch = global.fetch;
      calls = [];
      global.fetch = async (url, opts) => {
        calls.push({ url: String(url), opts });
        return { ok: true, status: 200, json: async () => ({ recorded: true }), text: async () => '' };
      };
      process.env.A2A_HUB_URL = 'http://localhost:19997';
      process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
      process.env.A2A_NODE_SECRET = 'test_secret';
      process.env.EVOLVER_REUSE_ATTRIBUTION = 'shadow'; // builds the attribution this consumes
    });
    afterEach(() => { global.fetch = savedFetch; });
    const flush = () => new Promise((r) => setImmediate(r));
    const records = () => calls.filter((c) => c.url.includes('/a2a/memory/record'));

    it('flag default off: shadow + direct reuse does NOT POST to the Hub', async () => {
      writeRunState({ source_type: 'reused', reused_asset_id: 'sha256:abc' });
      writeLastAction();
      fresh('../src/gep/memoryGraph').recordOutcomeFromState({ signals: [], observations: null });
      await flush();
      assert.equal(records().length, 0, 'no POST when EVOLVER_OUTCOME_REPORT is off');
    });

    it('flag on + shadow + direct reuse: POSTs flat {signals,status,used_asset_ids} to /a2a/memory/record', async () => {
      process.env.EVOLVER_OUTCOME_REPORT = 'on';
      writeRunState({ source_type: 'reused', reused_asset_id: 'sha256:abc' });
      writeLastAction(); // last_action.had_error:true, signals:['log_error']
      // current signals empty => error cleared => status 'success' (not stable_no_error)
      fresh('../src/gep/memoryGraph').recordOutcomeFromState({ signals: [], observations: null });
      await flush();
      const rec = records()[0];
      assert.ok(rec, 'POST to /a2a/memory/record fired');
      const body = JSON.parse(rec.opts.body);
      assert.deepEqual(body.used_asset_ids, ['sha256:abc']);
      assert.equal(body.status, 'success');
      assert.ok(Array.isArray(body.signals) && body.signals.length > 0, 'non-empty signals');
      // The hub resolves the recording node from body.sender_id (the node_secret
      // only authenticates that id, never derives it). Without sender_id the
      // record 400s with "sender_id_required" and this best-effort reporter
      // silently drops it — so this is the regression guard for that bug.
      assert.ok(typeof body.sender_id === 'string' && body.sender_id.length > 0,
        'flat body MUST carry sender_id so the hub can resolve the recording node');
      assert.ok(!('event' in body), 'still flat — not the {sender_id, event} memory-event envelope');
      assert.equal(rec.opts.headers.Authorization, 'Bearer test_secret');
    });

    it('flag on + reference (not direct reuse): no POST (reference is the weaker signal)', async () => {
      process.env.EVOLVER_OUTCOME_REPORT = 'on';
      writeRunState({ source_type: 'reference', reused_asset_id: 'sha256:ref1' });
      writeLastAction();
      fresh('../src/gep/memoryGraph').recordOutcomeFromState({ signals: [], observations: null });
      await flush();
      assert.equal(records().length, 0, 'reference reuse must not claim used_asset_ids');
    });

    it('flag on but no run-state (no reuse this cycle): no POST', async () => {
      process.env.EVOLVER_OUTCOME_REPORT = 'on';
      writeLastAction(); // no evolution_solidify_state.json
      fresh('../src/gep/memoryGraph').recordOutcomeFromState({ signals: [], observations: null });
      await flush();
      assert.equal(records().length, 0, 'no reuse => nothing to report');
    });
  });
});
