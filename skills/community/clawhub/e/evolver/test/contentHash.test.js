const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { canonicalize, computeAssetId, verifyAssetId, SCHEMA_VERSION } = require('../src/gep/contentHash');

describe('canonicalize', () => {
  it('serializes null and undefined as "null"', () => {
    assert.equal(canonicalize(null), 'null');
    assert.equal(canonicalize(undefined), 'null');
  });

  it('serializes primitives', () => {
    assert.equal(canonicalize(true), 'true');
    assert.equal(canonicalize(false), 'false');
    assert.equal(canonicalize(42), '42');
    assert.equal(canonicalize('hello'), '"hello"');
  });

  it('serializes non-finite numbers as null', () => {
    assert.equal(canonicalize(Infinity), 'null');
    assert.equal(canonicalize(-Infinity), 'null');
    assert.equal(canonicalize(NaN), 'null');
  });

  it('serializes arrays preserving order', () => {
    assert.equal(canonicalize([1, 2, 3]), '[1,2,3]');
    assert.equal(canonicalize([]), '[]');
  });

  it('serializes objects with sorted keys', () => {
    assert.equal(canonicalize({ b: 2, a: 1 }), '{"a":1,"b":2}');
    assert.equal(canonicalize({ z: 'last', a: 'first' }), '{"a":"first","z":"last"}');
  });

  it('produces deterministic output regardless of key insertion order', () => {
    const obj1 = { c: 3, a: 1, b: 2 };
    const obj2 = { a: 1, b: 2, c: 3 };
    assert.equal(canonicalize(obj1), canonicalize(obj2));
  });

  it('handles nested objects and arrays', () => {
    const nested = { arr: [{ b: 2, a: 1 }], val: null };
    const result = canonicalize(nested);
    assert.equal(result, '{"arr":[{"a":1,"b":2}],"val":null}');
  });
});

describe('computeAssetId', () => {
  it('returns a sha256-prefixed hash string', () => {
    const id = computeAssetId({ type: 'Gene', id: 'test_gene' });
    assert.ok(id.startsWith('sha256:'));
    assert.equal(id.length, 7 + 64); // "sha256:" + 64 hex chars
  });

  it('excludes asset_id field from hash by default', () => {
    const obj = { type: 'Gene', id: 'g1', data: 'x' };
    const withoutField = computeAssetId(obj);
    const withField = computeAssetId({ ...obj, asset_id: 'sha256:something' });
    assert.equal(withoutField, withField);
  });

  it('produces identical hashes for identical content', () => {
    const a = computeAssetId({ type: 'Capsule', id: 'c1', value: 42 });
    const b = computeAssetId({ type: 'Capsule', id: 'c1', value: 42 });
    assert.equal(a, b);
  });

  it('produces different hashes for different content', () => {
    const a = computeAssetId({ type: 'Gene', id: 'g1' });
    const b = computeAssetId({ type: 'Gene', id: 'g2' });
    assert.notEqual(a, b);
  });

  it('returns null for non-object input', () => {
    assert.equal(computeAssetId(null), null);
    assert.equal(computeAssetId('string'), null);
  });
});

describe('verifyAssetId', () => {
  it('returns true for correct asset_id', () => {
    const obj = { type: 'Gene', id: 'g1', data: 'test' };
    obj.asset_id = computeAssetId(obj);
    assert.ok(verifyAssetId(obj));
  });

  it('returns false for tampered content', () => {
    const obj = { type: 'Gene', id: 'g1', data: 'test' };
    obj.asset_id = computeAssetId(obj);
    obj.data = 'tampered';
    assert.ok(!verifyAssetId(obj));
  });

  it('returns false for missing asset_id', () => {
    assert.ok(!verifyAssetId({ type: 'Gene', id: 'g1' }));
  });

  it('returns false for null input', () => {
    assert.ok(!verifyAssetId(null));
  });
});

describe('SCHEMA_VERSION', () => {
  it('is a semver string', () => {
    assert.match(SCHEMA_VERSION, /^\d+\.\d+\.\d+$/);
  });
});

describe('@evomap/gep-sdk facade', () => {
  it('re-exports SDK references identically (no inlined copies)', () => {
    const sdk = require('@evomap/gep-sdk');
    const facade = require('../src/gep/contentHash');
    assert.equal(facade.SCHEMA_VERSION, sdk.SCHEMA_VERSION);
    assert.equal(facade.canonicalize, sdk.canonicalize);
    assert.equal(facade.computeAssetId, sdk.computeAssetId);
    assert.equal(facade.verifyAssetId, sdk.verifyAssetId);
  });

  it('produces the same asset_id as v1.83.0 for a known fixed gene', () => {
    // Frozen fixture: a Gene whose asset_id was computed by the inlined
    // pre-1.84.0 implementation. If the SDK ever ships a behaviour-breaking
    // change to canonicalize() / computeAssetId(), this test fails before
    // we accidentally bump and break Hub-side asset_id verification.
    const gene = {
      type: 'Gene',
      schema_version: '1.6.0',
      id: 'gene_repair_from_errors',
      category: 'repair',
      signals_match: ['log_error'],
      strategy: ['Inspect logs', 'Apply fix', 'Re-run validation'],
      constraints: { max_files: 20, forbidden_paths: ['.git', 'node_modules'] },
      validation: ['npm test'],
    };
    const id = computeAssetId(gene);
    assert.equal(id, 'sha256:327aa3452cde16a9aa2416431bbb2c75339cca05306e4933498cef63fc8a3d08');
  });
});
