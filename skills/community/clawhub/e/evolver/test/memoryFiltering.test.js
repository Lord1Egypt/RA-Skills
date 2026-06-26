// test/memoryFiltering.test.js
// Unit tests for memory filtering module

const test = require('node:test');
const assert = require('node:assert');
const { filterRelevantOutcomes, DEFAULT_MIN_SCORE, DEFAULT_MAX_AGE_MS, DEFAULT_MAX_OUTCOMES } = require('../src/adapters/scripts/_memoryFiltering');

test('filterRelevantOutcomes: basic filtering', (t) => {
  const now = Date.now();
  const entries = [
    { outcome: { status: 'success', score: 0.8 }, timestamp: new Date(now - 2*24*60*60*1000).toISOString() },
    { outcome: { status: 'failed', score: 0.3 }, timestamp: new Date(now - 1*24*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.4 }, timestamp: new Date(now - 5*24*60*60*1000).toISOString() },
  ];

  const filtered = filterRelevantOutcomes(entries);
  assert.strictEqual(filtered.length, 1, 'Should filter to 1 outcome (high score + recent)');
  assert.strictEqual(filtered[0].outcome.score, 0.8, 'Should keep highest score');
});

test('filterRelevantOutcomes: multiple valid outcomes', (t) => {
  const now = Date.now();
  const entries = [
    { outcome: { status: 'success', score: 0.9 }, timestamp: new Date(now - 1*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.8 }, timestamp: new Date(now - 2*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.7 }, timestamp: new Date(now - 3*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.6 }, timestamp: new Date(now - 4*60*60*1000).toISOString() },
  ];

  const filtered = filterRelevantOutcomes(entries);
  assert.strictEqual(filtered.length, 3, 'Should keep up to 3 outcomes');
  assert.deepStrictEqual(
    filtered.map(e => e.outcome.score),
    [0.8, 0.7, 0.6], // Note: slice(-3) keeps last 3 in original order
    'Should keep last 3 after filtering'
  );
});

test('filterRelevantOutcomes: filters failed outcomes', (t) => {
  const now = Date.now();
  const entries = [
    { outcome: { status: 'failed', score: 0.9 }, timestamp: new Date(now - 1*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.8 }, timestamp: new Date(now - 2*60*60*1000).toISOString() },
  ];

  const filtered = filterRelevantOutcomes(entries);
  assert.strictEqual(filtered.length, 1, 'Should filter out failed outcomes');
  assert.strictEqual(filtered[0].outcome.status, 'success', 'Should only keep success');
});

test('filterRelevantOutcomes: filters low scores', (t) => {
  const now = Date.now();
  const entries = [
    { outcome: { status: 'success', score: 0.4 }, timestamp: new Date(now - 1*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.5 }, timestamp: new Date(now - 2*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.6 }, timestamp: new Date(now - 3*60*60*1000).toISOString() },
  ];

  const filtered = filterRelevantOutcomes(entries);
  assert.strictEqual(filtered.length, 2, 'Should filter score < 0.5');
  assert(filtered.every(e => e.outcome.score >= DEFAULT_MIN_SCORE), 'All scores >= minScore');
});

test('filterRelevantOutcomes: filters old outcomes', (t) => {
  const now = Date.now();
  const entries = [
    { outcome: { status: 'success', score: 0.9 }, timestamp: new Date(now - 10*24*60*60*1000).toISOString() }, // 10 days old
    { outcome: { status: 'success', score: 0.8 }, timestamp: new Date(now - 3*24*60*60*1000).toISOString() },  // 3 days old
  ];

  const filtered = filterRelevantOutcomes(entries);
  assert.strictEqual(filtered.length, 1, 'Should filter outcomes older than 7 days');
  assert.strictEqual(filtered[0].outcome.score, 0.8, 'Should keep recent outcome');
});

test('filterRelevantOutcomes: empty input', (t) => {
  const filtered = filterRelevantOutcomes([]);
  assert.strictEqual(filtered.length, 0, 'Should handle empty input');
});

test('filterRelevantOutcomes: null timestamps', (t) => {
  const now = Date.now();
  const entries = [
    { outcome: { status: 'success', score: 0.8 }, timestamp: null },
    { outcome: { status: 'success', score: 0.7 }, timestamp: undefined },
    { outcome: { status: 'success', score: 0.6 }, timestamp: new Date(now - 1*24*60*60*1000).toISOString() },
  ];

  const filtered = filterRelevantOutcomes(entries);
  // Null/undefined timestamps are treated as very old (ts = 0)
  assert.strictEqual(filtered.length, 1, 'Should filter out entries with null/undefined timestamps');
  assert.strictEqual(filtered[0].outcome.score, 0.6, 'Should keep valid timestamp');
});

test('filterRelevantOutcomes: custom options', (t) => {
  const now = Date.now();
  const entries = [
    { outcome: { status: 'success', score: 0.3 }, timestamp: new Date(now - 1*60*60*1000).toISOString() },
    { outcome: { status: 'success', score: 0.5 }, timestamp: new Date(now - 2*60*60*1000).toISOString() },
  ];

  // Lower min score threshold
  const filtered = filterRelevantOutcomes(entries, { minScore: 0.2 });
  assert.strictEqual(filtered.length, 2, 'Should respect custom minScore option');
});

test('filterRelevantOutcomes: constants exported', (t) => {
  assert.strictEqual(typeof DEFAULT_MIN_SCORE, 'number', 'DEFAULT_MIN_SCORE should be exported');
  assert.strictEqual(typeof DEFAULT_MAX_AGE_MS, 'number', 'DEFAULT_MAX_AGE_MS should be exported');
  assert.strictEqual(typeof DEFAULT_MAX_OUTCOMES, 'number', 'DEFAULT_MAX_OUTCOMES should be exported');
  assert.strictEqual(DEFAULT_MIN_SCORE, 0.5, 'DEFAULT_MIN_SCORE should be 0.5');
  assert.strictEqual(DEFAULT_MAX_AGE_MS, 7 * 24 * 60 * 60 * 1000, 'DEFAULT_MAX_AGE_MS should be 7 days');
  assert.strictEqual(DEFAULT_MAX_OUTCOMES, 3, 'DEFAULT_MAX_OUTCOMES should be 3');
});
