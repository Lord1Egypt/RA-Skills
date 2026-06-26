const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { expandSignals, geneTags, scoreTagOverlap } = require('../src/gep/learningSignals');

describe('expandSignals', () => {
  it('returns an empty array for non-array / empty input', () => {
    assert.deepEqual(expandSignals(null), []);
    assert.deepEqual(expandSignals(undefined), []);
    assert.deepEqual(expandSignals([]), []);
    assert.deepEqual(expandSignals('not-an-array'), []);
  });

  it('preserves raw signal values in tags', () => {
    const tags = expandSignals(['foo_bar']);
    assert.ok(tags.includes('foo_bar'));
  });

  it('emits the namespace prefix of a namespaced signal', () => {
    const tags = expandSignals(['problem:reliability']);
    assert.ok(tags.includes('problem:reliability'));
    assert.ok(tags.includes('problem'));
  });

  it('does not emit a standalone prefix when signal has no colon', () => {
    const tags = expandSignals(['plain_signal']);
    assert.deepEqual(
      tags.filter((t) => t === 'plain_signal' || t === 'plain_signal:'),
      ['plain_signal']
    );
  });

  it('deduplicates identical tags', () => {
    const tags = expandSignals(['log_error', 'log_error', 'log_error']);
    const count = tags.filter((t) => t === 'log_error').length;
    assert.equal(count, 1);
  });

  it('filters out falsy and whitespace-only entries', () => {
    const tags = expandSignals(['', '   ', null, undefined, 0, 'real_one']);
    assert.ok(tags.includes('real_one'));
    assert.ok(!tags.includes(''));
    assert.ok(!tags.includes('   '));
  });

  it('classifies reliability signals', () => {
    const tags = expandSignals(['log_error']);
    assert.ok(tags.includes('problem:reliability'));
    assert.ok(tags.includes('action:repair'));
  });

  it('classifies protocol signals', () => {
    const tags = expandSignals(['schema_drift']);
    assert.ok(tags.includes('problem:protocol'));
    assert.ok(tags.includes('action:optimize'));
    assert.ok(tags.includes('area:prompt'));
  });

  it('classifies performance signals', () => {
    const tags = expandSignals(['perf_bottleneck']);
    assert.ok(tags.includes('problem:performance'));
    assert.ok(tags.includes('action:optimize'));
  });

  it('classifies capability signals', () => {
    const tags = expandSignals(['capability_gap']);
    assert.ok(tags.includes('problem:capability'));
    assert.ok(tags.includes('action:innovate'));
  });

  it('classifies stagnation signals', () => {
    const tags = expandSignals(['loop_detected']);
    assert.ok(tags.includes('problem:stagnation'));
    assert.ok(tags.includes('action:innovate'));
  });

  it('classifies orchestration signals', () => {
    const tags = expandSignals(['worker_heartbeat_missed']);
    assert.ok(tags.includes('area:orchestration'));
  });

  it('classifies memory signals', () => {
    const tags = expandSignals(['narrative_drift']);
    assert.ok(tags.includes('area:memory'));
  });

  it('classifies skill signals', () => {
    const tags = expandSignals(['skill_install_failed']);
    assert.ok(tags.includes('area:skills'));
  });

  it('classifies validation / risk signals', () => {
    const tags = expandSignals(['canary_rollback']);
    assert.ok(tags.includes('risk:validation'));
  });

  it('uses extraText to influence classification', () => {
    const tags = expandSignals(['generic_event'], 'the latency was terrible');
    assert.ok(tags.includes('problem:performance'));
  });

  it('combines multiple classifications for multi-signal input', () => {
    const tags = expandSignals(['log_error', 'perf_bottleneck', 'capability_gap']);
    assert.ok(tags.includes('problem:reliability'));
    assert.ok(tags.includes('problem:performance'));
    assert.ok(tags.includes('problem:capability'));
    assert.ok(tags.includes('action:repair'));
    assert.ok(tags.includes('action:optimize'));
    assert.ok(tags.includes('action:innovate'));
  });

  it('is case-insensitive when classifying via extraText', () => {
    const lower = expandSignals([], 'perf issue');
    const upper = expandSignals([], 'PERF ISSUE');
    assert.ok(lower.includes('problem:performance'));
    assert.ok(upper.includes('problem:performance'));
  });

  it('does not misclassify unrelated signals', () => {
    const tags = expandSignals(['unrelated_tag']);
    assert.ok(!tags.includes('problem:reliability'));
    assert.ok(!tags.includes('problem:performance'));
    assert.ok(!tags.includes('problem:protocol'));
  });
});

describe('geneTags', () => {
  it('returns empty array for invalid input', () => {
    assert.deepEqual(geneTags(null), []);
    assert.deepEqual(geneTags(undefined), []);
    assert.deepEqual(geneTags('not-an-object'), []);
    assert.deepEqual(geneTags(42), []);
  });

  it('returns empty array for an empty object', () => {
    assert.deepEqual(geneTags({}), []);
  });

  it('includes category as action:<lowercase-category>', () => {
    const tags = geneTags({ category: 'REPAIR' });
    assert.ok(tags.includes('action:repair'));
  });

  it('includes signals_match entries', () => {
    const tags = geneTags({ signals_match: ['log_error', 'perf_bottleneck'] });
    assert.ok(tags.includes('log_error'));
    assert.ok(tags.includes('perf_bottleneck'));
  });

  it('includes gene id and summary as raw inputs', () => {
    const tags = geneTags({ id: 'gene_fix_timeouts', summary: 'handle perf issues' });
    assert.ok(tags.includes('gene_fix_timeouts'));
    assert.ok(tags.includes('problem:performance'));
  });

  it('combines all fields', () => {
    const tags = geneTags({
      category: 'innovate',
      signals_match: ['capability_gap'],
      id: 'gene_new_capability',
      summary: 'introduce a missing capability',
    });
    assert.ok(tags.includes('action:innovate'));
    assert.ok(tags.includes('capability_gap'));
    assert.ok(tags.includes('problem:capability'));
  });
});

describe('scoreTagOverlap', () => {
  it('returns 0 when gene is empty', () => {
    assert.equal(scoreTagOverlap({}, ['log_error']), 0);
    assert.equal(scoreTagOverlap(null, ['log_error']), 0);
  });

  it('returns 0 when signals are empty', () => {
    assert.equal(scoreTagOverlap({ category: 'repair' }, []), 0);
    assert.equal(scoreTagOverlap({ category: 'repair' }, null), 0);
  });

  it('counts tag intersections', () => {
    const gene = { category: 'repair', signals_match: ['log_error'] };
    const score = scoreTagOverlap(gene, ['log_error']);
    assert.ok(score > 0);
  });

  it('ranks better-matched genes higher', () => {
    const specificGene = {
      category: 'repair',
      signals_match: ['log_error'],
      id: 'gene_repair_timeouts',
    };
    const unrelatedGene = {
      category: 'innovate',
      signals_match: ['capability_gap'],
      id: 'gene_new_feature',
    };
    const signals = ['log_error'];
    assert.ok(
      scoreTagOverlap(specificGene, signals) > scoreTagOverlap(unrelatedGene, signals)
    );
  });

  it('is symmetric to the number of distinct overlapping tags', () => {
    const gene = {
      category: 'repair',
      signals_match: ['log_error', 'perf_bottleneck'],
    };
    const fewSignals = scoreTagOverlap(gene, ['log_error']);
    const manySignals = scoreTagOverlap(gene, ['log_error', 'perf_bottleneck']);
    assert.ok(manySignals >= fewSignals);
  });
});
