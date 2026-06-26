'use strict';

// openPRRegistry tests.
//
// Background: 2026-05-16 — daemon was observed re-implementing work already
// in flight on open PRs (#38, #43), dirtying the working tree and triggering
// downstream rollback risk. This module gives the daemon a way to detect
// "my changed files overlap with an open PR" so solidify can rollback.
//
// Tests use Node's built-in mock library to stub child_process.execSync;
// no real `gh` is invoked.

const { describe, it, beforeEach, afterEach, mock } = require('node:test');
const assert = require('node:assert/strict');

// Helper: clear require cache so each test gets a fresh module-level cache.
function loadFresh() {
  delete require.cache[require.resolve('../src/gep/openPRRegistry')];
  return require('../src/gep/openPRRegistry');
}

// Helper: stub child_process.execSync globally for one test.
function withExecMock(impl, fn) {
  const cp = require('child_process');
  const original = cp.execSync;
  cp.execSync = impl;
  try {
    return fn();
  } finally {
    cp.execSync = original;
  }
}

const SAMPLE_PRS_JSON = JSON.stringify([
  {
    number: 38,
    title: 'fix(gep): inbound asset_id integrity check + solidify integration tests',
    headRefName: 'fix/phase4-integrity-tests',
    files: [
      { path: 'src/gep/a2aProtocol.js' },
      { path: 'src/gep/portable.js' },
      { path: 'test/solidifyIntegration.test.js' },
    ],
  },
  {
    number: 43,
    title: 'fix(gep): harden rollback against cross-repo data loss',
    headRefName: 'fix/rollback-safety-defaults',
    files: [
      { path: 'src/gep/solidify.js' },
      { path: 'src/gep/gitOps.js' },
    ],
  },
]);

describe('openPRRegistry — getOpenPRs', () => {
  let savedFlag;
  beforeEach(() => {
    savedFlag = process.env.EVOLVE_OPEN_PR_DEDUP;
    delete process.env.EVOLVE_OPEN_PR_DEDUP;
  });
  afterEach(() => {
    if (savedFlag === undefined) delete process.env.EVOLVE_OPEN_PR_DEDUP;
    else process.env.EVOLVE_OPEN_PR_DEDUP = savedFlag;
  });

  it('parses gh pr list JSON output into normalized PR objects', () => {
    const reg = loadFresh();
    reg._resetForTesting();
    withExecMock(
      function () { return SAMPLE_PRS_JSON; },
      function () {
        const prs = reg.getOpenPRs({ ttlMs: 0 });
        assert.equal(prs.length, 2);
        assert.equal(prs[0].number, 38);
        assert.deepEqual(prs[0].files, [
          'src/gep/a2aProtocol.js',
          'src/gep/portable.js',
          'test/solidifyIntegration.test.js',
        ]);
      }
    );
  });

  it('returns [] when gh is not installed (ENOENT)', () => {
    const reg = loadFresh();
    reg._resetForTesting();
    withExecMock(
      function () { const e = new Error('command not found: gh'); throw e; },
      function () {
        const prs = reg.getOpenPRs({ ttlMs: 0 });
        assert.deepEqual(prs, []);
      }
    );
  });

  it('returns [] on gh non-zero exit', () => {
    const reg = loadFresh();
    reg._resetForTesting();
    withExecMock(
      function () { const e = new Error('gh: API rate limit exceeded'); throw e; },
      function () {
        const prs = reg.getOpenPRs({ ttlMs: 0 });
        assert.deepEqual(prs, []);
      }
    );
  });

  it('caches results within TTL — second call does not re-invoke gh', () => {
    const reg = loadFresh();
    reg._resetForTesting();
    let calls = 0;
    withExecMock(
      function () { calls++; return SAMPLE_PRS_JSON; },
      function () {
        reg.getOpenPRs({ ttlMs: 60000 });
        reg.getOpenPRs({ ttlMs: 60000 });
        reg.getOpenPRs({ ttlMs: 60000 });
        assert.equal(calls, 1);
      }
    );
  });

  it('refetches after TTL expiry', () => {
    const reg = loadFresh();
    reg._resetForTesting();
    let calls = 0;
    withExecMock(
      function () { calls++; return SAMPLE_PRS_JSON; },
      function () {
        // ttlMs=0 means every call sees age >= ttlMs and triggers re-fetch
        reg.getOpenPRs({ ttlMs: 0 });
        reg.getOpenPRs({ ttlMs: 0 });
        assert.equal(calls, 2);
      }
    );
  });

  it('respects EVOLVE_OPEN_PR_DEDUP=0 by short-circuiting to []', () => {
    process.env.EVOLVE_OPEN_PR_DEDUP = '0';
    const reg = loadFresh();
    reg._resetForTesting();
    let calls = 0;
    withExecMock(
      function () { calls++; return SAMPLE_PRS_JSON; },
      function () {
        const prs = reg.getOpenPRs({ ttlMs: 0 });
        assert.deepEqual(prs, []);
        assert.equal(calls, 0); // never invoked gh at all
      }
    );
  });

  it('handles malformed JSON gracefully', () => {
    const reg = loadFresh();
    reg._resetForTesting();
    withExecMock(
      function () { return 'not valid json {'; },
      function () {
        const prs = reg.getOpenPRs({ ttlMs: 0 });
        assert.deepEqual(prs, []);
      }
    );
  });
});

describe('openPRRegistry — findOverlap', () => {
  it('returns no overlap when changedFiles is empty', () => {
    const reg = loadFresh();
    const r = reg.findOverlap({ changedFiles: [], prs: [] });
    assert.equal(r.overlap, false);
    assert.equal(r.reason, 'no_changed_files');
  });

  it('returns no overlap when no open PRs', () => {
    const reg = loadFresh();
    const r = reg.findOverlap({ changedFiles: ['src/x.js'], prs: [] });
    assert.equal(r.overlap, false);
    assert.equal(r.reason, 'no_open_prs');
  });

  it('returns no overlap when no files match', () => {
    const reg = loadFresh();
    const r = reg.findOverlap({
      changedFiles: ['src/never.js', 'docs/elsewhere.md'],
      prs: [{ number: 38, title: 'x', files: ['src/gep/a2aProtocol.js'] }],
    });
    assert.equal(r.overlap, false);
    assert.equal(r.reason, 'no_intersection');
  });

  it('returns overlap details when most changed files match a PR', () => {
    // Daemon-POV: I changed 4 files. 3 of them are in PR #38. That's 0.75
    // overlap from MY perspective — re-doing 75% of work the PR is doing.
    const reg = loadFresh();
    const r = reg.findOverlap({
      changedFiles: [
        'src/gep/a2aProtocol.js',
        'src/gep/portable.js',
        'test/solidifyIntegration.test.js',
        'src/gep/something_else.js',
      ],
      prs: [{
        number: 38,
        title: 'fix(gep): integrity',
        headRefName: 'fix/phase4',
        files: [
          'src/gep/a2aProtocol.js',
          'src/gep/portable.js',
          'test/solidifyIntegration.test.js',
          'src/gep/skill2gep.js',
        ],
      }],
    });
    assert.equal(r.overlap, true);
    assert.equal(r.prNumber, 38);
    assert.ok(Math.abs(r.overlapRatio - 0.75) < 0.001, 'overlap ratio should be 3/4');
    assert.deepEqual(r.sharedFiles.sort(), [
      'src/gep/a2aProtocol.js',
      'src/gep/portable.js',
      'test/solidifyIntegration.test.js',
    ].sort());
  });

  it('picks the strongest overlap when multiple PRs share files', () => {
    const reg = loadFresh();
    const r = reg.findOverlap({
      changedFiles: ['src/a.js', 'src/b.js', 'src/c.js', 'src/d.js'],
      prs: [
        // PR #1 shares 1/4 = 0.25
        { number: 1, title: 'low overlap', files: ['src/a.js', 'src/x.js'] },
        // PR #2 shares 3/4 = 0.75 — should be picked
        { number: 2, title: 'high overlap', files: ['src/a.js', 'src/b.js', 'src/c.js'] },
        // PR #3 shares 2/4 = 0.50
        { number: 3, title: 'mid overlap', files: ['src/a.js', 'src/b.js'] },
      ],
    });
    assert.equal(r.overlap, true);
    assert.equal(r.prNumber, 2);
    assert.ok(Math.abs(r.overlapRatio - 0.75) < 0.001);
  });

  it('respects EVOLVE_OPEN_PR_DEDUP=0 even with overlap', () => {
    const saved = process.env.EVOLVE_OPEN_PR_DEDUP;
    process.env.EVOLVE_OPEN_PR_DEDUP = '0';
    try {
      const reg = loadFresh();
      const r = reg.findOverlap({
        changedFiles: ['src/x.js'],
        prs: [{ number: 1, title: 't', files: ['src/x.js'] }],
      });
      assert.equal(r.overlap, false);
      assert.equal(r.reason, 'feature_disabled');
    } finally {
      if (saved === undefined) delete process.env.EVOLVE_OPEN_PR_DEDUP;
      else process.env.EVOLVE_OPEN_PR_DEDUP = saved;
    }
  });
});

describe('openPRRegistry — findSignalHints', () => {
  it('returns [] for empty signals', () => {
    const reg = loadFresh();
    assert.deepEqual(reg.findSignalHints({ signals: [], prs: [] }), []);
  });

  it('matches when signal tokens overlap with PR title tokens at >= threshold', () => {
    const reg = loadFresh();
    const hits = reg.findSignalHints({
      signals: ['integrity_check', 'asset_id_validation', 'inbound_asset'],
      prs: [
        {
          number: 38,
          title: 'fix(gep): inbound asset_id integrity check',
          headRefName: 'fix/phase4-integrity-tests',
          files: ['src/gep/a2aProtocol.js'],
        },
      ],
      threshold: 0.5,
    });
    assert.equal(hits.length, 1);
    assert.equal(hits[0].number, 38);
    assert.ok(hits[0].tokenOverlap >= 0.5);
  });

  it('does not match when token overlap is below threshold', () => {
    const reg = loadFresh();
    const hits = reg.findSignalHints({
      signals: ['typescript_strict_mode', 'compile_warning'],
      prs: [
        {
          number: 1,
          title: 'fix(rust): borrow checker',
          headRefName: 'fix/rust',
          files: [],
        },
      ],
      threshold: 0.5,
    });
    assert.equal(hits.length, 0);
  });

  // Bugbot review on PR #50: pr.files may be missing for partial PR objects
  // (tests, external callers, future schema changes). findSignalHints must
  // not throw — it must return hits for the OTHER valid PRs and fall back
  // to [] for the malformed one.
  it('handles PRs with missing files gracefully (no throw, files=[])', () => {
    const reg = loadFresh();
    const hits = reg.findSignalHints({
      signals: ['integrity_check', 'asset_id'],
      prs: [
        // No files property
        { number: 38, title: 'integrity check asset_id fix', headRefName: 'fix/x' },
        // files=null
        { number: 43, title: 'rollback safety', headRefName: 'fix/y', files: null },
        // valid PR — should still be returned
        { number: 50, title: 'integrity check asset', headRefName: 'fix/z', files: ['a.js'] },
      ],
      threshold: 0.5,
    });
    // Must not throw; must include all 3 PRs that match by tokens
    const numbers = hits.map(h => h.number).sort();
    assert.ok(numbers.includes(38), 'PR with missing files should still match');
    // PR #38: missing files → fileSample=[]
    const pr38 = hits.find(h => h.number === 38);
    assert.deepEqual(pr38.files, []);
  });

  it('sorts results by tokenOverlap descending and caps at 3', () => {
    const reg = loadFresh();
    const hits = reg.findSignalHints({
      signals: ['alpha', 'beta', 'gamma'],
      prs: [
        { number: 1, title: 'alpha beta gamma', headRefName: 'a', files: [] }, // 1.0
        { number: 2, title: 'alpha beta', headRefName: 'b', files: [] },        // 0.66
        { number: 3, title: 'alpha', headRefName: 'c', files: [] },              // 0.33 (below 0.5 threshold)
        { number: 4, title: 'alpha gamma', headRefName: 'd', files: [] },       // 0.66
        { number: 5, title: 'beta gamma', headRefName: 'e', files: [] },        // 0.66
      ],
      threshold: 0.5,
    });
    assert.equal(hits.length, 3);
    assert.equal(hits[0].number, 1); // highest
    // PR #3 is below threshold, must NOT be present
    assert.ok(!hits.some(function (h) { return h.number === 3; }));
  });
});
