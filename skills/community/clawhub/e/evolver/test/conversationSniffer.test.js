'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

// The sniffer reads MODE from env at module-load time, so tests that need a
// specific mode load a fresh copy via a cache-busting require. Helper:
function loadSniffer(mode) {
  if (mode === undefined) delete process.env.EVOLVER_CONV_SNIFF_ENABLED;
  else process.env.EVOLVER_CONV_SNIFF_ENABLED = mode;
  // Bust both the sniffer and paths caches so EVOLVER_REPO_ROOT (set by the
  // test's beforeEach) takes effect — getEvolutionDir() resolves from repo root.
  delete require.cache[require.resolve('../src/gep/conversationSniffer')];
  return require('../src/gep/conversationSniffer');
}

describe('conversationSniffer.scanCorpus', () => {
  const s = require('../src/gep/conversationSniffer');

  it('surfaces a capability when success marker + reusable action co-occur', () => {
    const r = s.scanCorpus('Ran lark-cli docs +create; document published successfully.');
    assert.equal(r.length, 1);
    assert.equal(r[0].capability, 'publish-feishu-doc');
  });

  it('does NOT surface when the action failed (no success marker)', () => {
    const r = s.scanCorpus('Tried lark-cli docs +create but it errored and failed to publish.');
    // "failed" is not a success marker; no positive success token present
    const caps = r.map((c) => c.capability);
    assert.ok(!caps.includes('publish-feishu-doc') || r.length === 0,
      'a failed attempt should not surface (got: ' + JSON.stringify(caps) + ')');
  });

  it('does NOT surface a plain success with no reusable capability', () => {
    const r = s.scanCorpus('The build passed and all tests are working.');
    assert.equal(r.length, 0);
  });

  it('recognizes Chinese success markers', () => {
    const r = s.scanCorpus('用 lark-cli 发布飞书文档，验证通过，已发布。');
    assert.equal(r.length, 1);
    assert.equal(r[0].capability, 'publish-feishu-doc');
  });

  it('dedups multiple hits of the same capability', () => {
    const r = s.scanCorpus('lark-cli published OK. Later lark-cli published again successfully.');
    const caps = r.map((c) => c.capability);
    assert.equal(caps.filter((c) => c === 'publish-feishu-doc').length, 1);
  });

  it('returns empty for blank corpus', () => {
    assert.deepEqual(s.scanCorpus(''), []);
    assert.deepEqual(s.scanCorpus(null), []);
  });

  it('requires LOCAL co-occurrence: distant success does NOT pair with a failed capability mention', () => {
    // success marker far away (tests passed), capability mention is a FAILURE,
    // separated by >200 chars of filler -> must NOT surface (Bugbot #175 High)
    const filler = ' '.repeat(400);
    const corpus = 'All unit tests passed successfully.' + filler +
      'Then I tried lark-cli docs +create but it errored out and nothing was produced.';
    assert.deepEqual(s.scanCorpus(corpus), [],
      'distant success must not pair with an unrelated/failed capability mention');
  });

  it('accepts a later successful use even if an earlier mention had no success nearby', () => {
    const filler = ' '.repeat(400);
    const corpus = 'Attempted lark-cli docs +create (no result here).' + filler +
      'Re-ran lark-cli docs +create and it published successfully.';
    const r = s.scanCorpus(corpus);
    assert.equal(r.length, 1);
    assert.equal(r[0].capability, 'publish-feishu-doc');
  });

  it('negated success markers do NOT count (Bugbot #175 r2: "not verified")', () => {
    assert.deepEqual(s.scanCorpus('lark-cli docs +create ran but the doc was not verified'), [],
      '"not verified" must not qualify as success');
    assert.deepEqual(s.scanCorpus('lark-cli 发布飞书文档 未成功'), [],
      'Chinese negation 未成功 must not qualify');
  });

  it('array segments are scanned independently — no cross-boundary false proximity (Bugbot #175 r2)', () => {
    // segment A ends with a success (tests passed); segment B is a FAILED lark-cli.
    // Joined, the success tail would sit near B's head; as separate segments it must NOT.
    const segA = 'ran the suite, all tests passed successfully';
    const segB = 'then lark-cli docs +create errored and produced nothing';
    assert.deepEqual(s.scanCorpus([segA, segB]), [],
      'success in segment A must not pair with capability in segment B');
  });

  it('array form still surfaces a genuine in-segment success', () => {
    const r = s.scanCorpus(['idle chatter', 'lark-cli docs +create published successfully']);
    assert.equal(r.length, 1);
    assert.equal(r[0].capability, 'publish-feishu-doc');
  });
});

describe('conversationSniffer.convertToSignals', () => {
  const s = require('../src/gep/conversationSniffer');

  it('prepends the umbrella signal and emits per-capability signals', () => {
    const sigs = s.convertToSignals([{ capability: 'publish-feishu-doc' }, { capability: 'api-call' }]);
    assert.equal(sigs[0], 'conv_capability_candidate');
    assert.ok(sigs.includes('conv_capability:publish-feishu-doc'));
    assert.ok(sigs.includes('conv_capability:api-call'));
  });

  it('returns empty for no candidates', () => {
    assert.deepEqual(s.convertToSignals([]), []);
  });
});

describe('conversationSniffer.trySniff modes', () => {
  let tmpDir, prevRepoRoot, prevMode;

  function bustPaths() {
    try { delete require.cache[require.resolve('../src/gep/paths')]; } catch (_) {}
  }

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'conv-sniff-'));
    prevRepoRoot = process.env.EVOLVER_REPO_ROOT;
    prevMode = process.env.EVOLVER_CONV_SNIFF_ENABLED;
    // getEvolutionDir() resolves from repo root -> point it at the tmp dir so
    // state/log writes are fully isolated (no pollution of the real repo).
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    bustPaths();
  });

  afterEach(() => {
    if (prevRepoRoot === undefined) delete process.env.EVOLVER_REPO_ROOT; else process.env.EVOLVER_REPO_ROOT = prevRepoRoot;
    if (prevMode === undefined) delete process.env.EVOLVER_CONV_SNIFF_ENABLED; else process.env.EVOLVER_CONV_SNIFF_ENABLED = prevMode;
    bustPaths();
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  });

  it('off mode: no signals, no scan', () => {
    const s = loadSniffer('off');
    const r = s.trySniff('lark-cli published successfully', { seen: {}, last_sniff_ts: 0 });
    assert.equal(r.mode, 'off');
    assert.deepEqual(r.signals, []);
  });

  it('shadow mode: surfaces candidates but injects NO signals', () => {
    const s = loadSniffer('shadow');
    const r = s.trySniff('lark-cli docs +create published the doc successfully', { seen: {}, last_sniff_ts: 0 });
    assert.equal(r.mode, 'shadow');
    assert.ok(r.candidates.length >= 1, 'shadow still surfaces candidates');
    assert.deepEqual(r.signals, [], 'shadow injects no signals');
  });

  it('enforce mode: injects candidate signals', () => {
    const s = loadSniffer('enforce');
    const r = s.trySniff('lark-cli docs +create published the doc successfully', { seen: {}, last_sniff_ts: 0 });
    assert.equal(r.mode, 'enforce');
    assert.ok(r.signals.includes('conv_capability_candidate'));
    assert.ok(r.signals.includes('conv_capability:publish-feishu-doc'));
  });

  it('cooldown: a second immediate sniff is gated', () => {
    const s = loadSniffer('enforce');
    const state = { seen: {}, last_sniff_ts: 0 };
    const first = s.trySniff('lark-cli published successfully', state);
    assert.ok(first.signals.length > 0, 'first sniff fires');
    // state now has a fresh last_sniff_ts; re-read and try again immediately
    const st2 = s.readState();
    const second = s.trySniff('lark-cli published successfully again', st2);
    assert.deepEqual(second.signals, [], 'second sniff within cooldown is gated');
  });

  it('empty sniff does NOT arm the cooldown (Bugbot #175 Medium)', () => {
    const s = loadSniffer('enforce');
    const state = { seen: {}, last_sniff_ts: 0 };
    // first sniff finds nothing (no capability/success) -> must not set cooldown
    const empty = s.trySniff('just some idle chatter, nothing actionable here', state);
    assert.deepEqual(empty.signals, [], 'empty sniff yields no signals');
    const afterEmpty = s.readState();
    assert.ok(!afterEmpty.last_sniff_ts, 'empty sniff must NOT persist last_sniff_ts');
    // a subsequent sniff with real evidence should still fire (not gated)
    const real = s.trySniff('lark-cli docs +create published successfully', s.readState());
    assert.ok(real.signals.length > 0, 'real evidence after an empty sniff still fires');
  });
});
