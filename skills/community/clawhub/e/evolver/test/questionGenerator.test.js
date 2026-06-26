const { describe, it, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

// Stub getEvolutionDir to use a temp directory
const tmpDir = path.join(__dirname, '.tmp_qgen_test_' + process.pid);
const stateFile = path.join(tmpDir, 'question_generator_state.json');

function cleanup() {
  try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
}

// Patch paths before requiring questionGenerator
const pathsMod = require('../src/gep/paths');
const origGetEvolutionDir = pathsMod.getEvolutionDir;
pathsMod.getEvolutionDir = function () { return tmpDir; };

const { generateQuestions, generateUrgentQuestions } = require('../src/gep/questionGenerator');

describe('questionGenerator', () => {
  beforeEach(() => {
    cleanup();
    fs.mkdirSync(tmpDir, { recursive: true });
  });

  describe('generateQuestions (standard path)', () => {
    it('returns empty when no triggering signals and no work to anchor on', () => {
      const qs = generateQuestions({ signals: ['stable_success_plateau'], recentEvents: [] });
      assert.ok(Array.isArray(qs));
      assert.strictEqual(qs.length, 0);
    });

    it('generates an exploration question for a healthy agent with recent work', () => {
      const qs = generateQuestions({
        signals: ['stable_success_plateau'],
        recentEvents: [{ genes_used: ['gene_pdf_extract'] }],
        sessionTranscript: 'invoice pdf extraction pipeline. invoice table parser. invoice pipeline throughput.',
        memorySnippet: 'agent specializes in invoice pdf pipeline',
      });
      assert.strictEqual(qs.length, 1, 'healthy agent with work should ask one exploration question');
      assert.ok(qs[0].signals.includes('exploration'), 'should be tagged exploration');
      assert.ok(/invoice|pipeline|pdf/.test(qs[0].question), 'should anchor on real recent work');
    });

    it('problem questions outrank exploration and exploration does not crowd them out', () => {
      const qs = generateQuestions({
        signals: ['recurring_error', 'recurring_errsig(3x): TypeError cannot read property'],
        recentEvents: [{ genes_used: ['gene_x'] }],
        sessionTranscript: 'parser parser parser handling something parser',
      });
      assert.ok(qs.length >= 1);
      assert.ok(qs[0].question.includes('Recurring error'), 'highest-priority problem question wins the top slot');
    });

    it('honors EVOLVER_EXPLORATION_QUESTIONS=0 kill switch', () => {
      const prev = process.env.EVOLVER_EXPLORATION_QUESTIONS;
      process.env.EVOLVER_EXPLORATION_QUESTIONS = '0';
      try {
        const qs = generateQuestions({
          signals: ['stable_success_plateau'],
          recentEvents: [{ genes_used: ['gene_x'] }],
          sessionTranscript: 'invoice pdf pipeline invoice pipeline',
        });
        assert.strictEqual(qs.length, 0, 'exploration disabled → no question for a healthy agent');
      } finally {
        if (prev === undefined) delete process.env.EVOLVER_EXPLORATION_QUESTIONS;
        else process.env.EVOLVER_EXPLORATION_QUESTIONS = prev;
      }
    });

    it('generates question on recurring_error signal', () => {
      const qs = generateQuestions({
        signals: ['recurring_error', 'recurring_errsig(3x): TypeError cannot read property'],
        recentEvents: [],
        sessionTranscript: '',
      });
      assert.ok(qs.length >= 1, 'expected at least 1 question');
      assert.ok(qs[0].question.includes('Recurring error'), 'question should mention recurring error');
      assert.ok(Array.isArray(qs[0].signals), 'should have signals array');
    });

    it('generates question on consecutive_failure_streak_3', () => {
      const qs = generateQuestions({
        signals: ['consecutive_failure_streak_3'],
        recentEvents: [],
      });
      assert.ok(qs.length >= 1, 'expected question for streak >= 3');
      assert.ok(qs[0].question.includes('failed 3'), 'should mention streak count');
    });

    it('generates question on hub_search_miss_with_problem', () => {
      const qs = generateQuestions({
        signals: ['hub_search_miss_with_problem', 'log_error', 'errsig:timeout'],
        recentEvents: [],
        sessionTranscript: 'Error: connection timeout after 5000ms',
      });
      assert.ok(qs.length >= 1, 'expected question for hub search miss');
      assert.ok(qs[0].question.includes('No matching solution'), 'should mention no ecosystem solution');
    });

    it('generates question on repair_loop_detected', () => {
      const events = Array.from({ length: 6 }, (_, i) => ({
        genes_used: ['gene_retry_' + (i % 2)],
        outcome: { status: 'failed' },
      }));
      const qs = generateQuestions({
        signals: ['repair_loop_detected', 'force_innovation_after_repair_loop'],
        recentEvents: events,
      });
      assert.ok(qs.length >= 1, 'expected question for repair loop');
      assert.ok(qs[0].question.includes('repair loop'), 'should mention repair loop');
    });

    it('generates question on plateau_pivot_required', () => {
      const qs = generateQuestions({
        signals: ['plateau_pivot_required'],
        recentEvents: [],
      });
      assert.ok(qs.length >= 1, 'expected question for plateau');
      assert.ok(qs[0].question.includes('plateaued'), 'should mention plateau');
    });

    it('respects rate limit', () => {
      generateQuestions({ signals: ['recurring_error', 'recurring_errsig(3x): test'], recentEvents: [] });
      const qs2 = generateQuestions({ signals: ['recurring_error', 'recurring_errsig(3x): test2'], recentEvents: [] });
      assert.strictEqual(qs2.length, 0, 'second call within rate limit should return empty');
    });

    it('returns max 3 questions', () => {
      const qs = generateQuestions({
        signals: [
          'recurring_error', 'recurring_errsig(3x): err1',
          'capability_gap',
          'evolution_saturation',
          'consecutive_failure_streak_5', 'ban_gene:gene_x',
          'hub_search_miss_with_problem', 'log_error',
          'repair_loop_detected',
          'plateau_pivot_required',
        ],
        recentEvents: [{ genes_used: ['gene_a'] }, { genes_used: ['gene_b'] }],
        sessionTranscript: 'Error: not supported feature\nTimeout detected',
      });
      assert.ok(qs.length <= 3, 'should return at most 3 questions, got ' + qs.length);
      assert.ok(qs.length >= 1, 'should return at least 1 question');
    });

    it('deduplicates against recent questions', () => {
      const qs1 = generateQuestions({
        signals: ['recurring_error', 'recurring_errsig(3x): TypeError cannot read property xyz'],
        recentEvents: [],
      });
      assert.ok(qs1.length >= 1);

      // Reset timer by manipulating state
      const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
      state.lastAskedAt = new Date(Date.now() - 35 * 60 * 1000).toISOString();
      fs.writeFileSync(stateFile, JSON.stringify(state));

      const qs2 = generateQuestions({
        signals: ['recurring_error', 'recurring_errsig(3x): TypeError cannot read property xyz'],
        recentEvents: [],
      });
      assert.strictEqual(qs2.length, 0, 'duplicate question should be filtered');
    });

    it('skips infrastructure 401 errors from recurring_errsig', () => {
      const qs = generateQuestions({
        signals: [
          'recurring_error',
          'recurring_errsig(3208x): LLM ERROR] 401 {"type":"error","error":{"type":"authentication_error","message":"invalid api key"',
        ],
        recentEvents: [],
      });
      assert.strictEqual(qs.length, 0, 'invalid api key storms must not become community bounties');
    });

    it('skips rate-limit / overloaded errors from recurring_errsig', () => {
      const qs = generateQuestions({
        signals: [
          'recurring_error',
          'recurring_errsig(120x): LLM ERROR] 529 {"type":"overloaded_error","message":"service overloaded"',
        ],
        recentEvents: [],
      });
      assert.strictEqual(qs.length, 0, '5xx overload errors must not become community bounties');
    });

    it('skips infrastructure errors from capability_gap transcript', () => {
      const qs = generateQuestions({
        signals: ['capability_gap'],
        recentEvents: [],
        sessionTranscript: 'Error: fetch failed ECONNRESET while calling api.anthropic.com',
      });
      assert.strictEqual(qs.length, 0, 'network errors must not turn into capability_gap bounties');
    });
  });

  describe('generateUrgentQuestions (post-solidify)', () => {
    it('generates question on validation failure', () => {
      const qs = generateUrgentQuestions({
        validationFailed: true,
        validationErrors: 'npm test: 3 tests failed',
        geneId: 'gene_retry_timeout',
      });
      assert.ok(qs.length >= 1, 'expected urgent question');
      assert.ok(qs[0].question.includes('failed validation'), 'should mention validation failure');
      assert.ok(qs[0].question.includes('gene_retry_timeout'), 'should mention gene id');
    });

    it('generates question on low confidence', () => {
      const qs = generateUrgentQuestions({
        lowConfidence: true,
        confidenceScore: 0.15,
        intent: 'repair',
      });
      assert.ok(qs.length >= 1, 'expected urgent question for low confidence');
      assert.ok(qs[0].question.includes('low confidence'), 'should mention low confidence');
      assert.ok(qs[0].question.includes('0.15'), 'should include score');
    });

    it('generates question on LLM review rejection', () => {
      const qs = generateUrgentQuestions({
        llmReviewRejected: true,
        llmReviewReason: 'Potential race condition in async handler',
      });
      assert.ok(qs.length >= 1, 'expected urgent question');
      assert.ok(qs[0].question.includes('rejected by LLM review'), 'should mention LLM rejection');
    });

    it('generates question on zero blast radius', () => {
      const qs = generateUrgentQuestions({
        zeroBlastRadius: true,
        hadSignals: true,
        signals: ['log_error', 'errsig:connection_refused'],
      });
      assert.ok(qs.length >= 1, 'expected urgent question');
      assert.ok(qs[0].question.includes('zero blast radius'), 'should mention zero blast radius');
    });

    it('generates question on task completion failure', () => {
      const qs = generateUrgentQuestions({
        taskCompletionFailed: true,
        taskTitle: 'Fix memory leak in worker pool',
        taskSignals: 'memory_leak,worker_pool',
      });
      assert.ok(qs.length >= 1, 'expected urgent question');
      assert.ok(qs[0].question.includes('Fix memory leak'), 'should include task title');
    });

    it('respects urgent rate limit (5 min)', () => {
      generateUrgentQuestions({ validationFailed: true, validationErrors: 'test error' });
      const qs2 = generateUrgentQuestions({ validationFailed: true, validationErrors: 'test error 2' });
      assert.strictEqual(qs2.length, 0, 'second urgent call within 5 min should return empty');
    });

    it('returns empty when no failure indicators', () => {
      const qs = generateUrgentQuestions({});
      assert.strictEqual(qs.length, 0);
    });

    it('skips validation failures caused by infrastructure errors', () => {
      const qs = generateUrgentQuestions({
        validationFailed: true,
        validationErrors: 'LLM ERROR] 401 authentication_error invalid api key',
        geneId: 'gene_any',
      });
      assert.strictEqual(qs.length, 0, '401 during validation is a user-local issue, not a community question');
    });

    it('skips LLM review rejections caused by rate limits', () => {
      const qs = generateUrgentQuestions({
        llmReviewRejected: true,
        llmReviewReason: 'HTTP 429 rate limit exceeded from upstream provider',
      });
      assert.strictEqual(qs.length, 0, '429 rate limit review rejection must not leak into bounties');
    });

    it('skips task completion failures caused by network errors', () => {
      const qs = generateUrgentQuestions({
        taskCompletionFailed: true,
        taskTitle: 'Fetch remote recipe and solidify patch',
        taskSignals: 'log_error,ECONNRESET,fetch failed',
      });
      assert.strictEqual(qs.length, 0, 'ECONNRESET during task execution is infra, not capability gap');
    });

    it('returns max 2 urgent questions', () => {
      const qs = generateUrgentQuestions({
        validationFailed: true,
        validationErrors: 'test failed',
        geneId: 'gene_x',
        lowConfidence: true,
        confidenceScore: 0.1,
        intent: 'repair',
        llmReviewRejected: true,
        llmReviewReason: 'bad code',
        zeroBlastRadius: true,
        hadSignals: true,
        signals: ['log_error'],
        taskCompletionFailed: true,
        taskTitle: 'Task X',
        taskSignals: 'sig_a',
      });
      assert.ok(qs.length <= 2, 'should return at most 2 urgent questions, got ' + qs.length);
      assert.ok(qs.length >= 1, 'should return at least 1');
    });
  });

  // Cleanup after all tests
  describe('cleanup', () => {
    it('removes temp dir', () => {
      cleanup();
      pathsMod.getEvolutionDir = origGetEvolutionDir;
    });
  });
});
