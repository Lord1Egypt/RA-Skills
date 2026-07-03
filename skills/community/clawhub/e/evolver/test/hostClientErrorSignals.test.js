'use strict';

// #571: an unrecoverable host/LLM client error (4xx: malformed request / auth /
// quota) must NOT be attributed to a Gene. It must not feed the consecutive-
// failure streak or ban_gene / failure_loop_detected, and must surface the
// actionable `host_llm_client_error` signal instead.

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { isHostClientError, HOST_PROVIDER_ERR_RE } = require('../src/gep/hostErrorClassifier');
const { extractSignals } = require('../src/gep/signals');

// Five consecutive failed, non-empty (blast radius > 0) cycles on the same
// gene. On its own this trips failure_loop_detected + ban_gene:gene_x.
function failedStreak(geneId) {
  const evts = [];
  for (let i = 0; i < 5; i++) {
    evts.push({
      intent: 'innovate',
      signals: [],
      genes_used: [geneId],
      blast_radius: { files: 1, lines: 5 },
      outcome: { status: 'failed', score: 0.2 },
    });
  }
  return evts;
}

describe('hostErrorClassifier.isHostClientError', () => {
  it('matches host/LLM 4xx-class provider errors', () => {
    assert.equal(isHostClientError('[LLM ERROR] field MaxTokens invalid, should be in [1, 65536]'), true);
    assert.equal(isHostClientError('provider returned invalid_api_key'), true);
    assert.equal(isHostClientError('insufficient_quota for this request'), true);
    assert.equal(isHostClientError('Request failed with HTTP 400'), true);
    assert.equal(isHostClientError('status code: 401'), true);
    assert.equal(isHostClientError('got 403 Forbidden from the gateway'), true);
    assert.equal(isHostClientError('rate limit exceeded, retry later'), true);
  });

  it('does NOT match ordinary gene/test failures or bare numbers', () => {
    assert.equal(isHostClientError('AssertionError: expected 2 to equal 3'), false);
    assert.equal(isHostClientError('refactor touched 400 lines across 12 files'), false);
    assert.equal(isHostClientError('TypeError: cannot read property foo of undefined'), false);
    assert.equal(isHostClientError(''), false);
    assert.equal(isHostClientError(null), false);
  });

  it('exposes a stateless (non-global) regex', () => {
    assert.equal(HOST_PROVIDER_ERR_RE.global, false);
    // Two calls in a row must agree (no lastIndex carry-over).
    assert.equal(isHostClientError('HTTP 400'), true);
    assert.equal(isHostClientError('HTTP 400'), true);
  });
});

describe('extractSignals — host client error vs gene failure', () => {
  it('host 4xx streak surfaces host_llm_client_error and suppresses ban/loop', () => {
    const signals = extractSignals({
      recentSessionTranscript:
        '**ASSISTANT**: [LLM ERROR] field MaxTokens invalid, should be in [1, 65536]',
      todayLog: '',
      memorySnippet: '',
      userSnippet: '',
      recentEvents: failedStreak('gene_x'),
    });
    assert.ok(signals.includes('host_llm_client_error'), 'expected host_llm_client_error');
    assert.ok(!signals.includes('failure_loop_detected'), 'must not trip failure_loop_detected');
    assert.ok(!signals.some((s) => s.startsWith('ban_gene:')), 'must not ban any gene');
    assert.ok(!signals.some((s) => s.startsWith('consecutive_failure_streak_')), 'must not emit streak');
    assert.ok(!signals.includes('force_innovation_after_repair_loop'), 'must not force innovation');
  });

  it('a genuine gene failure streak still bans the gene (regression guard)', () => {
    const signals = extractSignals({
      recentSessionTranscript: '**ASSISTANT**: AssertionError: expected solidify to write 1 file',
      todayLog: '',
      memorySnippet: '',
      userSnippet: '',
      recentEvents: failedStreak('gene_x'),
    });
    assert.ok(signals.includes('failure_loop_detected'), 'expected failure_loop_detected');
    assert.ok(signals.includes('ban_gene:gene_x'), 'expected ban_gene:gene_x');
    assert.ok(!signals.includes('host_llm_client_error'), 'must not misclassify as host error');
  });
});
