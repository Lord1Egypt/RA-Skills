'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const {
  estimateReuseTokensSaved,
  applyModeSaving,
  DERIVE_BASE_TOKENS,
  TOKENS_PER_CHANGED_LINE,
  DERIVE_CAP_TOKENS,
  TYPICAL_CHANGED_LINES,
  REFERENCE_SAVING_FRACTION,
} = require('../src/gep/tokenSavings');

describe('estimateReuseTokensSaved (grounded fallback estimate)', () => {
  it('scales with blast_radius.lines (basis estimated_blast_radius)', () => {
    const r = estimateReuseTokensSaved({ blast_radius: { files: 2, lines: 50 } }, 'direct');
    assert.equal(r.basis, 'estimated_blast_radius');
    assert.equal(r.tokens_saved, DERIVE_BASE_TOKENS + 50 * TOKENS_PER_CHANGED_LINE);
  });

  it('reads blast_radius from a nested payload', () => {
    const r = estimateReuseTokensSaved({ payload: { blast_radius: { lines: 10 } } }, 'direct');
    assert.equal(r.basis, 'estimated_blast_radius');
    assert.equal(r.tokens_saved, DERIVE_BASE_TOKENS + 10 * TOKENS_PER_CHANGED_LINE);
  });

  it('falls back to the typical default when no blast_radius (basis estimated_default)', () => {
    const r = estimateReuseTokensSaved({ id: 'asset1' }, 'direct');
    assert.equal(r.basis, 'estimated_default');
    assert.equal(r.tokens_saved, DERIVE_BASE_TOKENS + TYPICAL_CHANGED_LINES * TOKENS_PER_CHANGED_LINE);
  });

  it('default median reproduces the historical ~180k assumption', () => {
    assert.equal(estimateReuseTokensSaved(null, 'direct').tokens_saved, 180_000);
  });

  it('caps a pathological blast_radius', () => {
    const r = estimateReuseTokensSaved({ blast_radius: { lines: 100000 } }, 'direct');
    assert.equal(r.tokens_saved, DERIVE_CAP_TOKENS);
  });

  it('reference mode saves a fraction of a full re-derivation', () => {
    const direct = estimateReuseTokensSaved({ blast_radius: { lines: 50 } }, 'direct');
    const ref = estimateReuseTokensSaved({ blast_radius: { lines: 50 } }, 'reference');
    assert.equal(ref.tokens_saved, Math.round(direct.tokens_saved * REFERENCE_SAVING_FRACTION));
  });

  it('handles null / garbage asset without throwing', () => {
    assert.equal(estimateReuseTokensSaved(undefined).basis, 'estimated_default');
    assert.equal(estimateReuseTokensSaved(42).basis, 'estimated_default');
    assert.equal(estimateReuseTokensSaved({ blast_radius: 'nope' }).basis, 'estimated_default');
  });
});

describe('applyModeSaving (shared reference-mode discount)', () => {
  it('returns the full count for direct or unspecified mode', () => {
    assert.equal(applyModeSaving(100000, 'direct'), 100000);
    assert.equal(applyModeSaving(100000), 100000);
  });

  it('discounts reference mode by REFERENCE_SAVING_FRACTION and rounds', () => {
    assert.equal(applyModeSaving(123456, 'reference'), Math.round(123456 * REFERENCE_SAVING_FRACTION));
    assert.equal(applyModeSaving(123456, 'reference'), 49382);
  });

  it('coerces non-numbers to 0', () => {
    assert.equal(applyModeSaving(null, 'direct'), 0);
    assert.equal(applyModeSaving('x', 'reference'), 0);
  });
});
