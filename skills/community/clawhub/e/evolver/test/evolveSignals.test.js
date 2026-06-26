'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

const signals = require('../src/evolve/pipeline/signals');

// ---------------------------------------------------------------------------
// shouldSkipHubCalls
// ---------------------------------------------------------------------------
describe('shouldSkipHubCalls', () => {
  it('returns false for empty signals array', () => {
    assert.equal(signals.shouldSkipHubCalls([]), false);
  });

  it('returns false for non-array input', () => {
    assert.equal(signals.shouldSkipHubCalls(null), false);
    assert.equal(signals.shouldSkipHubCalls(undefined), false);
  });

  it('returns false when no saturation signal present', () => {
    assert.equal(signals.shouldSkipHubCalls(['log_error', 'capability_gap']), false);
  });

  it('returns true when only saturation signals', () => {
    assert.equal(signals.shouldSkipHubCalls(['force_steady_state']), true);
    assert.equal(signals.shouldSkipHubCalls(['evolution_saturation']), true);
    assert.equal(signals.shouldSkipHubCalls(['empty_cycle_loop_detected']), true);
  });

  it('returns false when log_error coexists with saturation', () => {
    assert.equal(signals.shouldSkipHubCalls(['evolution_saturation', 'log_error']), false);
  });

  it('returns false when external_task coexists with saturation', () => {
    assert.equal(signals.shouldSkipHubCalls(['evolution_saturation', 'external_task']), false);
  });

  it('returns false when bounty_task coexists with saturation', () => {
    assert.equal(signals.shouldSkipHubCalls(['evolution_saturation', 'bounty_task']), false);
  });

  it('returns false when errsig: prefix present with saturation', () => {
    assert.equal(signals.shouldSkipHubCalls(['force_steady_state', 'errsig:ReferenceError']), false);
  });

  it('returns false when user_feature_request with content coexists with saturation', () => {
    assert.equal(signals.shouldSkipHubCalls(['evolution_saturation', 'user_feature_request:some request']), false);
  });

  it('returns true when user_feature_request is empty (no real content)', () => {
    // string length <= 21 → no real request
    assert.equal(signals.shouldSkipHubCalls(['evolution_saturation', 'user_feature_request:']), true);
  });
});

// ---------------------------------------------------------------------------
// extractSignalsStage
// ---------------------------------------------------------------------------
describe('extractSignalsStage', () => {
  const fs = require('node:fs');
  const os = require('node:os');
  const path = require('node:path');

  const baseCtx = {
    dormantHypothesis: null,
    recentMasterLog: '',
    todayLog: '',
    memorySnippet: '',
    userSnippet: '',
    lastHubFetchMs: 0,
  };

  // Isolate the asset store: the stage now calls consumePendingSignals(),
  // which read-once clears pending_signals.json. Without isolation, `npm test`
  // would wipe a real machine's queued explicit signals before any evolution
  // cycle sees them.
  let tmpDir;
  let prevAssetsDir;
  let prevSessionScope;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-extract-'));
    prevAssetsDir = process.env.GEP_ASSETS_DIR;
    process.env.GEP_ASSETS_DIR = tmpDir;
    // Clear session scope: otherwise getGepAssetsDir() resolves under
    // tmpDir/scopes/<scope> while these tests write pending_signals.json at
    // the tmp root, so the consume path would be missed on a scoped host.
    prevSessionScope = process.env.EVOLVER_SESSION_SCOPE;
    delete process.env.EVOLVER_SESSION_SCOPE;
  });

  afterEach(() => {
    if (prevAssetsDir === undefined) delete process.env.GEP_ASSETS_DIR;
    else process.env.GEP_ASSETS_DIR = prevAssetsDir;
    if (prevSessionScope === undefined) delete process.env.EVOLVER_SESSION_SCOPE;
    else process.env.EVOLVER_SESSION_SCOPE = prevSessionScope;
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  });

  it('returns ctx with genes, capsules, recentEvents, signals, skipHubCalls', async () => {
    const result = await signals.extractSignalsStage(baseCtx);
    assert.ok(Array.isArray(result.genes), 'genes should be an array');
    assert.ok(Array.isArray(result.capsules), 'capsules should be an array');
    assert.ok(Array.isArray(result.recentEvents), 'recentEvents should be an array');
    assert.ok(Array.isArray(result.signals), 'signals should be an array');
    assert.equal(typeof result.skipHubCalls, 'boolean');
  });

  it('preserves existing ctx fields', async () => {
    const ctx = { ...baseCtx, cycleNum: 42, someField: 'hello' };
    const result = await signals.extractSignalsStage(ctx);
    assert.equal(result.cycleNum, 42);
    assert.equal(result.someField, 'hello');
  });

  it('injects dormant hypothesis signals into output signals', async () => {
    const ctx = {
      ...baseCtx,
      dormantHypothesis: { signals: ['my_dormant_signal', 'another_dormant'] },
    };
    const result = await signals.extractSignalsStage(ctx);
    assert.ok(result.signals.includes('my_dormant_signal'), 'dormant signal should be injected');
    assert.ok(result.signals.includes('another_dormant'), 'dormant signal should be injected');
  });

  it('does not duplicate dormant signals already present', async () => {
    // extractSignals may or may not produce signals that overlap; the dedup logic
    // should ensure no duplicates from dormant injection.
    const ctx = {
      ...baseCtx,
      dormantHypothesis: { signals: ['dup_signal', 'dup_signal'] },
    };
    const result = await signals.extractSignalsStage(ctx);
    const count = result.signals.filter(s => s === 'dup_signal').length;
    assert.ok(count <= 1, 'dormant signal should not be added twice');
  });

  it('skipHubCalls is false when lastHubFetchMs is 0 (never fetched)', async () => {
    // Even if saturation signal is somehow present, lastHubFetchMs=0 means no gating
    const result = await signals.extractSignalsStage({ ...baseCtx, lastHubFetchMs: 0 });
    assert.equal(result.skipHubCalls, false);
  });
});

// ---------------------------------------------------------------------------
// Explicit signal injection (pending_signals.json)
// ---------------------------------------------------------------------------
describe('extractSignalsStage -- explicit signal injection', () => {
  const fs = require('node:fs');
  const os = require('node:os');
  const path = require('node:path');

  const baseCtx = {
    dormantHypothesis: null,
    recentMasterLog: '',
    todayLog: '',
    memorySnippet: '',
    userSnippet: '',
    lastHubFetchMs: 0,
  };

  let tmpDir;
  let prevAssetsDir;

  beforeEach(() => {
    // Isolate the asset store so we never touch the real pending_signals.json.
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-pending-'));
    prevAssetsDir = process.env.GEP_ASSETS_DIR;
    process.env.GEP_ASSETS_DIR = tmpDir;
  });

  afterEach(() => {
    if (prevAssetsDir === undefined) delete process.env.GEP_ASSETS_DIR;
    else process.env.GEP_ASSETS_DIR = prevAssetsDir;
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  });

  it('injects signals declared in pending_signals.json', async () => {
    fs.writeFileSync(
      path.join(tmpDir, 'pending_signals.json'),
      JSON.stringify({ signals: ['publish_markdown_to_feishu', 'create_feishu_doc'], note: 'test' }),
    );
    const result = await signals.extractSignalsStage(baseCtx);
    assert.ok(result.signals.includes('publish_markdown_to_feishu'), 'explicit signal should be injected');
    assert.ok(result.signals.includes('create_feishu_doc'), 'explicit signal should be injected');
  });

  it('consumes pending signals (read-once) so they do not re-fire', async () => {
    const p = path.join(tmpDir, 'pending_signals.json');
    fs.writeFileSync(p, JSON.stringify({ signals: ['one_shot_signal'] }));

    const first = await signals.extractSignalsStage(baseCtx);
    assert.ok(first.signals.includes('one_shot_signal'), 'first cycle injects the signal');

    const second = await signals.extractSignalsStage(baseCtx);
    assert.ok(!second.signals.includes('one_shot_signal'), 'second cycle must not re-inject (consumed)');

    const onDisk = JSON.parse(fs.readFileSync(p, 'utf8'));
    assert.deepEqual(onDisk.signals, [], 'file should be emptied after consumption');
  });

  it('is a no-op when pending_signals.json is absent', async () => {
    // No file written. Stage must not throw and must still return a signals array.
    const result = await signals.extractSignalsStage(baseCtx);
    assert.ok(Array.isArray(result.signals), 'signals array returned even with no pending file');
  });

  it('ignores empty / blank signal entries', async () => {
    fs.writeFileSync(
      path.join(tmpDir, 'pending_signals.json'),
      JSON.stringify({ signals: ['  ', '', 'real_signal'] }),
    );
    const result = await signals.extractSignalsStage(baseCtx);
    assert.ok(result.signals.includes('real_signal'), 'non-blank signal injected');
    assert.ok(!result.signals.includes(''), 'blank signal not injected');
    assert.ok(!result.signals.includes('  '), 'whitespace signal not injected');
  });

  it('consumes a file whose entries are all blank (read-once still completes)', async () => {
    // Regression: previously the file was only cleared when >=1 entry survived
    // filtering, so an all-blank file was re-read under lock every cycle.
    const p = path.join(tmpDir, 'pending_signals.json');
    fs.writeFileSync(p, JSON.stringify({ signals: ['  ', ''] }));

    await signals.extractSignalsStage(baseCtx);

    const onDisk = JSON.parse(fs.readFileSync(p, 'utf8'));
    assert.deepEqual(onDisk.signals, [], 'all-blank file should still be emptied after consumption');
  });
});
