'use strict';

// Unit tests for the asset-search endpoint planner. planAssetSearch() decides
// whether POST /asset/search forwards to the hub's signal-search (keyword) or
// semantic-search (free-text) endpoint. These are pure-function tests: no hub,
// no network, fully deterministic.

const { test } = require('node:test');
const assert = require('node:assert');
const {
  planAssetSearch,
  buildSemanticSearchQuery,
  buildAssetSearchQuery,
} = require('../src/proxy/index.js');

test('signals-only body keeps the signal-search endpoint (no regression)', () => {
  const plan = planAssetSearch({ signals: ['log_error', 'perf_bottleneck'], limit: 5 });
  assert.equal(plan.path, '/a2a/assets/search');
  assert.equal(plan.query.signals, 'log_error,perf_bottleneck');
  assert.equal(plan.query.limit, 5);
  assert.equal('q' in plan.query, false);
});

test('free-text query routes to semantic-search carried in q', () => {
  const plan = planAssetSearch({ query: 'recover quoted feishu reply text', limit: 3 });
  assert.equal(plan.path, '/a2a/assets/semantic-search');
  assert.equal(plan.query.q, 'recover quoted feishu reply text');
  assert.equal(plan.query.limit, 3);
  assert.equal('signals' in plan.query, false);
});

test('query wins when both query and signals are present', () => {
  const plan = planAssetSearch({ query: 'fix flaky async test', signals: ['test_failure'] });
  assert.equal(plan.path, '/a2a/assets/semantic-search');
  assert.equal(plan.query.q, 'fix flaky async test');
});

test('whitespace-only query falls back to the signal path', () => {
  const plan = planAssetSearch({ query: '   ', signals: ['capability_gap'] });
  assert.equal(plan.path, '/a2a/assets/search');
  assert.equal(plan.query.signals, 'capability_gap');
});

test('non-string query (defensive) falls back to the signal path', () => {
  const plan = planAssetSearch({ query: 123, signals: ['log_error'] });
  assert.equal(plan.path, '/a2a/assets/search');
});

test('empty body produces a signal-search plan with no params', () => {
  const plan = planAssetSearch();
  assert.equal(plan.path, '/a2a/assets/search');
  assert.deepEqual(plan.query, {});
});

test('semantic query forwards type and fields', () => {
  const plan = planAssetSearch({
    query: 'add retry with backoff',
    type: 'Gene',
    fields: ['strategy', 'preconditions'],
  });
  assert.equal(plan.path, '/a2a/assets/semantic-search');
  assert.equal(plan.query.type, 'Gene');
  assert.equal(plan.query.fields, 'strategy,preconditions');
});

test('buildSemanticSearchQuery omits absent optionals', () => {
  const q = buildSemanticSearchQuery({ query: 'hello world' });
  assert.equal(q.q, 'hello world');
  assert.equal('type' in q, false);
  assert.equal('limit' in q, false);
  assert.equal('fields' in q, false);
});

test('buildAssetSearchQuery is unchanged for the signal path', () => {
  const q = buildAssetSearchQuery({ signals: ['log_error'], domain: 'web', status: 'promoted' });
  assert.equal(q.signals, 'log_error');
  assert.equal(q.domain, 'web');
  assert.equal(q.status, 'promoted');
  assert.equal('q' in q, false);
});
