const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const qc = require('../src/atp/questionComposer');

describe('questionComposer.compose', () => {
  it('returns a non-empty string even with no inputs', () => {
    const q = qc.compose({});
    assert.equal(typeof q, 'string');
    assert.ok(q.length > 0, 'expected non-empty fallback question');
  });

  it('returns a capability-specific template when capability is known', () => {
    const q = qc.compose({ capabilities: ['performance'], signals: [] });
    assert.ok(/performance|bottleneck|optim/i.test(q), 'expected performance-related wording, got: ' + q);
  });

  it('is deterministic for the same inputs', () => {
    const a = qc.compose({ capabilities: ['debugging'], signals: ['log_error', 'stack_trace'] });
    const b = qc.compose({ capabilities: ['debugging'], signals: ['log_error', 'stack_trace'] });
    assert.equal(a, b);
  });

  it('never exceeds the default length cap', () => {
    const longCaps = Array.from({ length: 20 }, function (_, i) { return 'cap_' + i; });
    const q = qc.compose({ capabilities: longCaps, signals: ['sig_x'.repeat(200)] });
    assert.ok(q.length <= 240, 'question too long: ' + q.length);
  });

  it('does not leak internal signal wording', () => {
    const q = qc.compose({ capabilities: ['code_evolution'], signals: ['evolver_cycle', 'mutation_id_x'] });
    assert.ok(!/evolver_cycle/.test(q), 'leaked evolver_cycle into question');
    assert.ok(!/mutation_id_x/.test(q), 'leaked mutation id into question');
  });

  it('falls back to generic phrasing for unknown capabilities', () => {
    const q = qc.compose({ capabilities: ['this_is_not_a_known_template'] });
    assert.equal(typeof q, 'string');
    assert.ok(q.length > 0);
  });

  it('respects custom maxLen', () => {
    const q = qc.compose({ capabilities: ['general'], maxLen: 60 });
    assert.ok(q.length <= 60, 'expected <=60, got ' + q.length);
  });
});

describe('questionComposer._normalize', () => {
  it('lowercases and strips non-alphanumerics', () => {
    assert.equal(qc._normalize('Code-Evolution!'), 'code_evolution');
    assert.equal(qc._normalize('  Perf Tuning  '), 'perf_tuning');
    assert.equal(qc._normalize('X'), 'x');
    assert.equal(qc._normalize(''), '');
  });
});

describe('questionComposer._hashFor', () => {
  it('is stable across calls', () => {
    const a = qc._hashFor(['a', 'b']);
    const b = qc._hashFor(['a', 'b']);
    assert.equal(a, b);
  });
  it('changes when inputs change', () => {
    const a = qc._hashFor(['a', 'b']);
    const b = qc._hashFor(['a', 'c']);
    assert.notEqual(a, b);
  });
});
