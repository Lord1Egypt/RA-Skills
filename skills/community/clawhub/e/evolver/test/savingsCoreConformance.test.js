'use strict';

// savings-core CONFORMANCE test.
//
// Two locks, same pattern as every other savings-core consumer (evomap-hub
// conformance/savings-core, evomap-private internal/gep/savingscore, ...):
//  1. impl == local copy -- src/gep/savingsCore.js must replay every vendored
//     golden vector bit-for-bit, and its constants must equal the vendored
//     conformance/savings-core/constants.json.
//  2. local copy == upstream -- EvoMap/savings-core's daily drift-check
//     compares the vendored files against the source of truth.
//
// Additionally replays the E3 vectors through the REAL production path
// (tokenSavings.estimateReuseTokensSaved) so the wrapper can never drift from
// the spec formula it claims to implement.

const { describe, it } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

const core = require('../src/gep/savingsCore');
const { estimateReuseTokensSaved } = require('../src/gep/tokenSavings');

const VENDOR_DIR = path.join(__dirname, '..', 'conformance', 'savings-core');
const constants = JSON.parse(fs.readFileSync(path.join(VENDOR_DIR, 'constants.json'), 'utf8'));
const golden = JSON.parse(fs.readFileSync(path.join(VENDOR_DIR, 'golden-vectors.json'), 'utf8'));

const RUN = {
  measured_savings: (i) => core.measuredSavings(i.raw_tokens, i.optimized_tokens),
  rollout_fold: (i) => ({ rollout_fold_pct: core.rolloutFoldPct(i.n_avg_rollouts) }),
  entropy_total: (i) => core.entropyTotal(i.events),
  fetch_usage_estimate: (i) => ({ estimated_token_saved: core.fetchUsageEstimate(i.byType) }),
  reuse_estimate: (i) => core.reuseEstimate(i.blast_radius_lines, i.mode),
  hit_rate: (i) => ({ hit_rate_pct: core.hitRatePct(i.hits, i.misses) }),
  usd_saved: (i) => ({ usd_saved: core.usdSaved(i.tokens) }),
  cache_saved_usd: (i) => ({ cache_saved_usd: core.cacheSavedUsd(i.provider, i.cache_read_tokens) }),
};

describe('savings-core conformance', () => {
  it('declares the same spec version everywhere', () => {
    assert.equal(constants.spec_version, core.SAVINGS_SPEC_VERSION);
    assert.equal(golden.spec_version, core.SAVINGS_SPEC_VERSION);
  });

  it('impl constants are the vendored constants.json (same object, no copy to drift)', () => {
    assert.deepEqual(core.CONSTANTS, constants);
  });

  it('ships the full vector set with unique ids', () => {
    assert.ok(golden.cases.length >= 25);
    const ids = golden.cases.map((c) => c.id);
    assert.equal(new Set(ids).size, ids.length);
  });

  for (const c of golden.cases) {
    it(`vector: ${c.id}`, () => {
      const fn = RUN[c.formula];
      assert.equal(typeof fn, 'function', `unknown formula ${c.formula} -- spec drifted ahead of impl`);
      assert.deepEqual(fn(c.input), c.expected);
    });
  }

  // E3 through the production wrapper: the same vectors must reproduce via
  // tokenSavings.estimateReuseTokensSaved given an equivalent asset shape.
  for (const c of golden.cases.filter((c) => c.formula === 'reuse_estimate')) {
    it(`production path: ${c.id}`, () => {
      const lines = c.input.blast_radius_lines;
      const asset = lines == null ? null : { blast_radius: { lines } };
      assert.deepEqual(estimateReuseTokensSaved(asset, c.input.mode), c.expected);
    });
  }
});
