const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { selectGene, selectCapsule, selectGeneAndCapsule, isEpigeneticallySuppressed } = require('../src/gep/selector');
const { captureEnvFingerprint } = require('../src/gep/envFingerprint');

const GENES = [
  {
    type: 'Gene',
    id: 'gene_repair',
    category: 'repair',
    signals_match: ['error', 'exception', 'failed'],
    strategy: ['fix it'],
    validation: ['node -e "true"'],
  },
  {
    type: 'Gene',
    id: 'gene_optimize',
    category: 'optimize',
    signals_match: ['protocol', 'prompt', 'audit'],
    strategy: ['optimize it'],
    validation: ['node -e "true"'],
  },
  {
    type: 'Gene',
    id: 'gene_innovate',
    category: 'innovate',
    signals_match: ['user_feature_request', 'user_improvement_suggestion', 'capability_gap', 'stable_success_plateau'],
    strategy: ['build it'],
    validation: ['node -e "true"'],
  },
  {
    type: 'Gene',
    id: 'gene_perf_optimize',
    category: 'optimize',
    signals_match: ['latency', 'throughput'],
    summary: 'Reduce latency and improve throughput on slow paths',
    strategy: ['speed it up'],
    validation: ['node -e "true"'],
  },
];

const CAPSULES = [
  {
    type: 'Capsule',
    id: 'capsule_1',
    trigger: ['log_error', 'exception'],
    gene: 'gene_repair',
    summary: 'Fixed an error',
    confidence: 0.9,
  },
  {
    type: 'Capsule',
    id: 'capsule_2',
    trigger: ['protocol', 'gep'],
    gene: 'gene_optimize',
    summary: 'Optimized prompt',
    confidence: 0.85,
  },
];

describe('selectGene', () => {
  it('selects the gene with highest signal match', () => {
    const result = selectGene(GENES, ['error', 'exception', 'failed'], {});
    assert.equal(result.selected.id, 'gene_repair');
  });

  it('returns null when no signals match', () => {
    const result = selectGene(GENES, ['completely_unrelated_signal'], {});
    assert.equal(result.selected, null);
  });

  it('returns alternatives when multiple genes match', () => {
    const result = selectGene(GENES, ['error', 'protocol'], {});
    assert.ok(result.selected);
    assert.ok(Array.isArray(result.alternatives));
  });

  it('includes drift intensity in result', () => {
    // Drift intensity is population-size-dependent; verify it is returned.
    const result = selectGene(GENES, ['error', 'exception'], {});
    assert.ok('driftIntensity' in result);
    assert.equal(typeof result.driftIntensity, 'number');
    assert.ok(result.driftIntensity >= 0 && result.driftIntensity <= 1);
  });

  it('applies score multiplier for preferred gene from memory graph', () => {
    const orig = Math.random;
    Math.random = () => 0.99;
    try {
      const result = selectGene(GENES, ['error', 'protocol'], {
        preferredGeneId: 'gene_optimize',
      });
      assert.equal(result.selected.id, 'gene_optimize');
    } finally { Math.random = orig; }
  });

  it('does not let multiplier override a much-higher-scoring gene', () => {
    const orig = Math.random;
    Math.random = () => 0.99;
    try {
      const result = selectGene(GENES, ['error', 'exception', 'failed'], {
        preferredGeneId: 'gene_optimize',
      });
      assert.equal(result.selected.id, 'gene_repair');
    } finally { Math.random = orig; }
  });

  it('matches gene via baseName:snippet signal (user_feature_request:snippet)', () => {
    const result = selectGene(GENES, ['user_feature_request:add a dark mode toggle to the settings'], {});
    assert.ok(result.selected);
    assert.equal(result.selected.id, 'gene_innovate', 'innovate gene has signals_match user_feature_request');
  });

  it('matches gene via baseName:snippet signal (user_improvement_suggestion:snippet)', () => {
    const result = selectGene(GENES, ['user_improvement_suggestion:refactor the payment module and simplify the API'], {});
    assert.ok(result.selected);
    assert.equal(result.selected.id, 'gene_innovate', 'innovate gene has signals_match user_improvement_suggestion');
  });

  it('uses derived learning tags to match related performance genes', () => {
    const originalRandom = Math.random;
    Math.random = () => 0.99;
    try {
      const result = selectGene(GENES, ['perf_bottleneck'], { effectivePopulationSize: 100 });
      assert.ok(result.selected);
      assert.equal(result.selected.id, 'gene_perf_optimize');
    } finally {
      Math.random = originalRandom;
    }
  });

  it('downweights genes with repeated hard-fail anti-patterns', () => {
    const originalRandom = Math.random;
    Math.random = () => 0.99;
    try {
      const riskyGenes = [
        {
          type: 'Gene',
          id: 'gene_perf_risky',
          category: 'optimize',
          signals_match: ['perf_bottleneck'],
          anti_patterns: [
            { mode: 'hard', learning_signals: ['problem:performance'] },
            { mode: 'hard', learning_signals: ['problem:performance'] },
          ],
          validation: ['node -e "true"'],
        },
        {
          type: 'Gene',
          id: 'gene_perf_safe',
          category: 'optimize',
          signals_match: ['perf_bottleneck'],
          learning_history: [
            { outcome: 'success', mode: 'none' },
          ],
          validation: ['node -e "true"'],
        },
      ];
      const result = selectGene(riskyGenes, ['perf_bottleneck'], { effectivePopulationSize: 100 });
      assert.ok(result.selected);
      assert.equal(result.selected.id, 'gene_perf_safe');
    } finally {
      Math.random = originalRandom;
    }
  });
});

describe('selectCapsule', () => {
  it('selects capsule matching signals', () => {
    const result = selectCapsule(CAPSULES, ['log_error', 'exception']);
    assert.equal(result.id, 'capsule_1');
  });

  it('returns null when no triggers match', () => {
    const result = selectCapsule(CAPSULES, ['unrelated']);
    assert.equal(result, null);
  });
});

describe('selectGeneAndCapsule', () => {
  it('returns selected gene, capsule candidates, and selector decision', () => {
    const result = selectGeneAndCapsule({
      genes: GENES,
      capsules: CAPSULES,
      signals: ['error', 'log_error'],
      memoryAdvice: null,
      driftEnabled: false,
    });
    assert.ok(result.selectedGene);
    assert.ok(result.selector);
    assert.ok(result.selector.selected);
    assert.ok(Array.isArray(result.selector.reason));
  });

  it('includes selectionPath and memoryUsed telemetry', () => {
    const result = selectGeneAndCapsule({
      genes: GENES,
      capsules: CAPSULES,
      signals: ['error', 'log_error'],
      memoryAdvice: { bannedGeneIds: new Set(), preferredGeneId: null, totalAttempts: 0 },
      driftEnabled: false,
    });
    assert.ok(result.selectionPath);
    assert.equal(typeof result.memoryUsed, 'boolean');
    assert.equal(typeof result.memoryEvidence, 'number');
    assert.ok(result.selector.selectionPath);
  });
});

describe('computeDriftIntensity adaptive decay', () => {
  const { computeDriftIntensity } = require('../src/gep/selector');

  it('returns base drift with max offset when no memory evidence', () => {
    const d = computeDriftIntensity({ driftEnabled: true, genePoolSize: 10, memoryEvidence: 0 });
    const expected = Math.min(1, 1 / Math.sqrt(10) + 0.3);
    assert.ok(Math.abs(d - expected) < 0.001, `expected ~${expected.toFixed(3)}, got ${d.toFixed(3)}`);
  });

  it('decays offset as memory evidence grows', () => {
    const dLow = computeDriftIntensity({ driftEnabled: true, genePoolSize: 10, memoryEvidence: 0 });
    const dMid = computeDriftIntensity({ driftEnabled: true, genePoolSize: 10, memoryEvidence: 50 });
    const dHigh = computeDriftIntensity({ driftEnabled: true, genePoolSize: 10, memoryEvidence: 200 });
    assert.ok(dLow > dMid, `low evidence drift ${dLow} should exceed mid ${dMid}`);
    assert.ok(dMid > dHigh, `mid evidence drift ${dMid} should exceed high ${dHigh}`);
  });

  it('reaches floor offset at full maturity', () => {
    const ne = 10;
    const fullMature = ne * 10;
    const d = computeDriftIntensity({ driftEnabled: true, genePoolSize: ne, memoryEvidence: fullMature * 2 });
    const expectedFloor = Math.min(1, 1 / Math.sqrt(ne) + 0.02);
    assert.ok(Math.abs(d - expectedFloor) < 0.001, `expected floor ~${expectedFloor.toFixed(3)}, got ${d.toFixed(3)}`);
  });

  it('returns population-dependent drift when not explicitly enabled', () => {
    const d = computeDriftIntensity({ driftEnabled: false, genePoolSize: 10, memoryEvidence: 50 });
    const expected = Math.min(1, 1 / Math.sqrt(10));
    assert.ok(Math.abs(d - expected) < 0.001, `expected ~${expected.toFixed(3)}, got ${d.toFixed(3)}`);
  });
});

describe('selectGene drift respects bannedGeneIds (regression)', () => {
  // Regression for the plateau-drift-bypass-ban feedback loop:
  // a Gene that fails repeatedly on the same signal key triggers plateau
  // detection in evolve.js, plateau forces drift on, drift was previously
  // bypassing bannedGeneIds, and the same failed Gene kept being re-selected.
  // After the fix, bans must apply in drift mode too.
  const FAILING = {
    type: 'Gene',
    id: 'gene_repair_failed',
    category: 'repair',
    signals_match: ['recurring_error', 'repair_loop_detected'],
    strategy: ['retry'],
    validation: ['node -e "true"'],
  };
  const ALT = {
    type: 'Gene',
    id: 'gene_repair_alt',
    category: 'repair',
    signals_match: ['recurring_error'],
    strategy: ['try a different approach'],
    validation: ['node -e "true"'],
  };

  it('skips a banned gene even when drift is enabled', () => {
    const banned = new Set(['gene_repair_failed']);
    const orig = Math.random;
    Math.random = () => 0;
    try {
      for (let i = 0; i < 20; i++) {
        const result = selectGene([FAILING, ALT], ['recurring_error', 'repair_loop_detected'], {
          driftEnabled: true,
          bannedGeneIds: banned,
          effectivePopulationSize: 2,
        });
        assert.ok(result.selected, 'should still select a non-banned gene');
        assert.notEqual(result.selected.id, 'gene_repair_failed',
          'banned gene must never be selected, even under drift');
      }
    } finally { Math.random = orig; }
  });

  it('returns null when every candidate is banned, regardless of drift', () => {
    const banned = new Set(['gene_repair_failed', 'gene_repair_alt']);
    const result = selectGene([FAILING, ALT], ['recurring_error'], {
      driftEnabled: true,
      bannedGeneIds: banned,
    });
    assert.equal(result.selected, null);
  });
});

describe('isEpigeneticallySuppressed', () => {
  // Hard-stop layer that catches genes whose epigenetic boost has decayed
  // past the configured threshold (default -0.3, ~3 failures in same env).
  // Independent from memoryGraph's per-signal-key ban so it survives even
  // if signal keys keep shifting and per-key counts never accumulate.
  const ENV = captureEnvFingerprint();
  const envContext = [ENV.platform || '', ENV.arch || '', ENV.node_version || '']
    .filter(Boolean).join('/') || 'unknown';

  it('returns false for a gene with no epigenetic marks', () => {
    const gene = { type: 'Gene', id: 'gene_clean' };
    assert.equal(isEpigeneticallySuppressed(gene, ENV), false);
  });

  it('returns false for a mild negative boost above the hard threshold', () => {
    const gene = {
      type: 'Gene',
      id: 'gene_mild',
      epigenetic_marks: [{ context: envContext, boost: -0.1, reason: 'failure_in_environment', created_at: new Date().toISOString() }],
    };
    assert.equal(isEpigeneticallySuppressed(gene, ENV), false);
  });

  it('returns true once boost reaches the hard threshold (-0.3)', () => {
    const gene = {
      type: 'Gene',
      id: 'gene_severe',
      epigenetic_marks: [{ context: envContext, boost: -0.3, reason: 'suppressed_by_failure', created_at: new Date().toISOString() }],
    };
    assert.equal(isEpigeneticallySuppressed(gene, ENV), true);
  });

  it('returns true for boost well past the threshold', () => {
    const gene = {
      type: 'Gene',
      id: 'gene_dead',
      epigenetic_marks: [{ context: envContext, boost: -0.5, reason: 'suppressed_by_failure', created_at: new Date().toISOString() }],
    };
    assert.equal(isEpigeneticallySuppressed(gene, ENV), true);
  });

  it('does not suppress when the negative mark belongs to a different env', () => {
    const gene = {
      type: 'Gene',
      id: 'gene_other_env',
      epigenetic_marks: [{ context: 'aix/sparc/v0.0.0', boost: -0.5, reason: 'suppressed_by_failure', created_at: new Date().toISOString() }],
    };
    assert.equal(isEpigeneticallySuppressed(gene, ENV), false);
  });
});

describe('selectGene distilled-gene fallback when no signal matches (issue #97)', () => {
  // Regression for the daemon-mode no-evolution loop: when a node's live
  // signals don't overlap any seed signals_match, scoreGene returned 0 for
  // every gene, scored.length===0, and selector returned selected:null. With
  // EVOLVE_BRIDGE=false (loop default) the cycle is auto-rejected and no
  // EvolutionEvent is recorded. After 33 days on Aurora the asset store had
  // 27 no_outcome candidates and 0 daemon-driven events. After this fix, when
  // a distilled gene is available it is returned as a low-confidence fallback
  // so the cycle has *something* to do. The driftMode marker
  // 'distilled_fallback' lets telemetry distinguish real matches from this
  // path.
  const NORMAL_GENE = {
    type: 'Gene',
    id: 'gene_repair',
    category: 'repair',
    signals_match: ['error', 'exception'],
    validation: ['node -e "true"'],
  };
  const DISTILLED = {
    type: 'Gene',
    id: 'gene_distilled_s2g_env_vars',
    category: 'optimize',
    signals_match: ['env_files', 'vercel_env_commands'],
    summary: 'Vercel env-var skill',
    validation: ['node --version'],
  };

  it('falls back to a distilled gene when no signal matches', () => {
    const result = selectGene([NORMAL_GENE, DISTILLED], ['totally_unrelated_signal'], {});
    assert.ok(result.selected, 'fallback should produce a selected gene');
    assert.equal(result.selected.id, 'gene_distilled_s2g_env_vars');
    assert.equal(result.driftMode, 'distilled_fallback');
  });

  it('returns null when no distilled gene exists in the pool', () => {
    // Preserves upstream contract: "null -> mutation creates a new gene".
    const result = selectGene([NORMAL_GENE], ['totally_unrelated_signal'], {});
    assert.equal(result.selected, null);
    assert.equal(result.driftMode, 'none');
  });

  it('does not fall back to a banned distilled gene', () => {
    const banned = new Set(['gene_distilled_s2g_env_vars']);
    const result = selectGene([NORMAL_GENE, DISTILLED], ['totally_unrelated_signal'], {
      bannedGeneIds: banned,
    });
    assert.equal(result.selected, null,
      'banned distilled gene should NOT be picked as fallback');
  });

  it('does not fall back to an epigenetically suppressed distilled gene', () => {
    const ENV = captureEnvFingerprint();
    const envContext = [ENV.platform || '', ENV.arch || '', ENV.node_version || '']
      .filter(Boolean).join('/') || 'unknown';
    const suppressedDistilled = {
      ...DISTILLED,
      epigenetic_marks: [{ context: envContext, boost: -0.5, reason: 'suppressed_by_failure', created_at: new Date().toISOString() }],
    };
    const result = selectGene([NORMAL_GENE, suppressedDistilled], ['totally_unrelated_signal'], {});
    assert.equal(result.selected, null,
      'suppressed distilled gene should NOT be picked as fallback');
  });

  it('still prefers a real signal-matched gene over the distilled fallback', () => {
    // Sanity check: fallback is only triggered when scored.length===0.
    // If the normal gene actually matches, we get score-ranked selection.
    const result = selectGene([NORMAL_GENE, DISTILLED], ['error'], {});
    assert.ok(result.selected);
    assert.equal(result.selected.id, 'gene_repair');
    assert.notEqual(result.driftMode, 'distilled_fallback');
  });
});

describe('tokenize is unicode-aware (issue #98)', () => {
  // Regression: tokenize used to use [^a-z0-9_\-]+ which silently dropped
  // every CJK / Cyrillic / Arabic character, causing CN/JA/KO users to
  // score 0 against every gene and selector to return null on every cycle.
  const { tokenize } = require('../src/gep/selector');

  it('preserves Chinese characters', () => {
    const tokens = tokenize('[错误] connection refused');
    assert.ok(tokens.includes('错误'), 'Chinese token should be preserved');
    assert.ok(tokens.includes('connection'));
    assert.ok(tokens.includes('refused'));
  });

  it('preserves Japanese characters', () => {
    const tokens = tokenize('タスク失敗 timeout');
    assert.ok(tokens.includes('タスク失敗'), 'Japanese token should be preserved');
    assert.ok(tokens.includes('timeout'));
  });

  it('preserves Korean characters', () => {
    const tokens = tokenize('실패 connection');
    assert.ok(tokens.includes('실패'));
    assert.ok(tokens.includes('connection'));
  });

  it('still strips ASCII punctuation', () => {
    const tokens = tokenize('error: failed; not.ok');
    assert.deepEqual(tokens.sort(), ['error', 'failed', 'ok'].sort());
  });

  it('lowercases ASCII while leaving non-ASCII untouched', () => {
    const tokens = tokenize('ERROR 错误 Failed');
    assert.ok(tokens.includes('error'));
    assert.ok(tokens.includes('错误'));
    assert.ok(tokens.includes('failed'));
  });
});

describe('selectGene matches multilingual signals_match (issue #98)', () => {
  // The seed gene store ships signals_match patterns of the form
  // 'error|错误|エラー|오류'. matchPatternToSignals already supports the
  // pipe-alias syntax via substring branch matching -- verify it actually
  // works end-to-end so non-English signals route to the right gene.
  const MULTI_GENE = {
    type: 'Gene',
    id: 'gene_repair_multi',
    category: 'repair',
    signals_match: [
      'error|错误|异常|エラー|오류',
      'failed|失败|失敗|실패',
    ],
    validation: ['node -e "true"'],
  };
  const OTHER_GENE = {
    type: 'Gene',
    id: 'gene_other',
    category: 'optimize',
    signals_match: ['gep', 'protocol'],
    validation: ['node -e "true"'],
  };

  it('matches a Chinese signal against the | alias', () => {
    const result = selectGene([MULTI_GENE, OTHER_GENE], ['错误'], {});
    assert.ok(result.selected, 'should select a gene for CN signal');
    assert.equal(result.selected.id, 'gene_repair_multi');
  });

  it('matches a Japanese signal against the | alias', () => {
    const result = selectGene([MULTI_GENE, OTHER_GENE], ['エラー'], {});
    assert.ok(result.selected);
    assert.equal(result.selected.id, 'gene_repair_multi');
  });

  it('matches a Korean signal against the | alias', () => {
    const result = selectGene([MULTI_GENE, OTHER_GENE], ['실패'], {});
    assert.ok(result.selected);
    assert.equal(result.selected.id, 'gene_repair_multi');
  });

  it('English signal still matches (no regression)', () => {
    const result = selectGene([MULTI_GENE, OTHER_GENE], ['error'], {});
    assert.ok(result.selected);
    assert.equal(result.selected.id, 'gene_repair_multi');
  });
});

describe('selectGene filters epigenetically suppressed genes (regression)', () => {
  const ENV = captureEnvFingerprint();
  const envContext = [ENV.platform || '', ENV.arch || '', ENV.node_version || '']
    .filter(Boolean).join('/') || 'unknown';

  it('skips a gene with boost <= -0.3 even when its signal score would win', () => {
    const suppressed = {
      type: 'Gene',
      id: 'gene_repair_suppressed',
      category: 'repair',
      signals_match: ['error', 'exception', 'failed', 'crash'],
      epigenetic_marks: [{ context: envContext, boost: -0.4, reason: 'suppressed_by_failure', created_at: new Date().toISOString() }],
      validation: ['node -e "true"'],
    };
    const fallback = {
      type: 'Gene',
      id: 'gene_repair_fallback',
      category: 'repair',
      signals_match: ['error'],
      validation: ['node -e "true"'],
    };
    const result = selectGene([suppressed, fallback], ['error', 'exception', 'failed', 'crash'], {});
    assert.ok(result.selected);
    assert.equal(result.selected.id, 'gene_repair_fallback');
  });

  it('still selects a suppressed gene when no other candidates exist', () => {
    // Edge case: if every gene is suppressed and selection returns null,
    // the upstream loop will create a new gene via mutation. Document that
    // behavior here so future refactors do not silently change it.
    const onlyOne = {
      type: 'Gene',
      id: 'gene_only',
      category: 'repair',
      signals_match: ['error'],
      epigenetic_marks: [{ context: envContext, boost: -0.5, reason: 'suppressed_by_failure', created_at: new Date().toISOString() }],
      validation: ['node -e "true"'],
    };
    const result = selectGene([onlyOne], ['error'], {});
    assert.equal(result.selected, null,
      'all suppressed -> selector returns null so the caller can mutate a new gene');
  });
});
