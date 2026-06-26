// Regression for EvoMap/evolver#562 — "Gene selection stagnation: auto-generated
// gene selected ~99.7% of the time in --loop mode".
//
// Root mechanism (reproduced against the published 1.88.2 binary):
//   1. `stable_no_error` outcomes (no error before/after, no parseable
//      EvolutionEvent) were tallied as Bayesian "successes" (score 0.6), so a
//      gene that only ever did nothing climbed p -> ~1.0 and was preferred.
//   2. A sole-matching gene is re-selected every cycle (selector drift only
//      diversifies when >1 gene scores > 0) and never banned (the failure-streak
//      ban never trips on "successes") -> it dominated --loop mode forever while
//      producing zero artifacts.
//
// The fix tallies these zero-work outcomes as `inert` (not `success`) so they
// build no confidence, and bans a gene after GENE_INERT_BAN_STREAK consecutive
// inert outcomes on a signal with no real success — letting the selector fall
// through to mutation (null -> fresh gene), restoring diversity.
const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert');
const path = require('path');
const fs = require('fs');
const os = require('os');

const mg = require('../src/gep/memoryGraph');
const { selectGene } = require('../src/gep/selector');
const cfg = require('../src/config');

function setupTmpEnv() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'mg562-'));
  const origEnv = {};
  for (const k of ['EVOLVER_REPO_ROOT', 'MEMORY_GRAPH_PATH', 'EVOLUTION_DIR', 'OPENCLAW_WORKSPACE', 'EVOLVER_SESSION_SCOPE']) {
    origEnv[k] = process.env[k];
  }
  process.env.MEMORY_GRAPH_PATH = path.join(tmpDir, 'memory_graph.jsonl');
  process.env.EVOLUTION_DIR = tmpDir;
  delete process.env.OPENCLAW_WORKSPACE;
  delete process.env.EVOLVER_SESSION_SCOPE;
  return { tmpDir, origEnv };
}

function teardownTmpEnv(tmpDir, origEnv) {
  for (const [k, v] of Object.entries(origEnv)) {
    if (v !== undefined) process.env[k] = v;
    else delete process.env[k];
  }
  try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
}

// Write a chronological sequence of outcome events. `seq` is an array of
// { status, note } in time order (earliest first) so consecutive-trailing
// semantics can be exercised deterministically.
function writeOutcomeSeq(tmpDir, geneId, signals, seq) {
  const graphPath = path.join(tmpDir, 'memory_graph.jsonl');
  const signalKey = mg.computeSignalKey(signals);
  const now = Date.now();
  const lines = seq.map((o, i) => JSON.stringify({
    type: 'MemoryGraphEvent',
    kind: 'outcome',
    id: `mge562_${i}`,
    ts: new Date(now - (seq.length - i) * 1000).toISOString(),
    signal: { key: signalKey, signals },
    gene: { id: geneId, category: 'repair' },
    action: { id: `act562_${i}` },
    outcome: { status: o.status, score: o.score != null ? o.score : (o.status === 'failed' ? 0.15 : 0.6), note: o.note },
  }));
  fs.writeFileSync(graphPath, lines.join('\n') + '\n');
}

const inert = (n) => Array.from({ length: n }, () => ({ status: 'success', note: 'stable_no_error|heuristic_delta|predictive' }));
const real = (n) => Array.from({ length: n }, () => ({ status: 'success', note: 'error_cleared' }));

const SIGNALS = ['memory_missing'];
const GENE = { id: 'gene_auto_6279e076', type: 'Gene', signals_match: ['memory_missing', 'memory.md missing'] };

describe('memoryGraph#562 - inert (stable_no_error) outcomes do not build confidence', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  it('does NOT prefer a gene whose entire history is inert', () => {
    writeOutcomeSeq(tmpDir, GENE.id, SIGNALS, inert(20));
    const advice = mg.getMemoryAdvice({ signals: SIGNALS, genes: [GENE], driftEnabled: false });
    assert.strictEqual(advice.preferredGeneId, null,
      'zero-work successes must not count as positive evidence (was: preferred at p~0.998)');
  });

  it('DOES prefer the same gene when its successes are real (control)', () => {
    writeOutcomeSeq(tmpDir, GENE.id, SIGNALS, real(20));
    const advice = mg.getMemoryAdvice({ signals: SIGNALS, genes: [GENE], driftEnabled: false });
    assert.strictEqual(advice.preferredGeneId, GENE.id,
      'real successes must still build confidence and be preferred');
  });
});

describe('memoryGraph#562 - inert-streak ban breaks the dominance loop', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  it('bans a gene after GENE_INERT_BAN_STREAK consecutive inert outcomes (drift on or off)', () => {
    writeOutcomeSeq(tmpDir, GENE.id, SIGNALS, inert(cfg.GENE_INERT_BAN_STREAK));
    for (const drift of [false, true]) {
      const advice = mg.getMemoryAdvice({ signals: SIGNALS, genes: [GENE], driftEnabled: drift });
      assert.ok(advice.bannedGeneIds.has(GENE.id),
        `stuck-inert gene must be banned so selection explores (driftEnabled=${drift})`);
    }
  });

  it('does NOT ban below the streak threshold', () => {
    writeOutcomeSeq(tmpDir, GENE.id, SIGNALS, inert(cfg.GENE_INERT_BAN_STREAK - 1));
    const advice = mg.getMemoryAdvice({ signals: SIGNALS, genes: [GENE], driftEnabled: false });
    assert.ok(!advice.bannedGeneIds.has(GENE.id), 'must not ban before the inert streak is reached');
  });

  it('a single real success resets the streak (consecutive, not cumulative)', () => {
    // 7 inert, 1 real success, 7 inert => 14 inert total but only 7 trailing.
    const seq = [...inert(7), ...real(1), ...inert(7)];
    writeOutcomeSeq(tmpDir, GENE.id, SIGNALS, seq);
    const advice = mg.getMemoryAdvice({ signals: SIGNALS, genes: [GENE], driftEnabled: false });
    assert.ok(!advice.bannedGeneIds.has(GENE.id),
      'a gene that ever does real work must not be punished for old idle cycles');
  });
});

describe('selector#562 - banned sole-match gene yields null so the caller mutates', () => {
  it('selectGene returns selected:null when the only matching gene is banned (escape hatch)', () => {
    // Baseline: with drift fully forced, a sole match is still selected 100% --
    // drift cannot diversify a single candidate. This is the dominance trap.
    const baseline = selectGene([GENE], SIGNALS, {
      driftEnabled: true, effectivePopulationSize: 1,
      plateauOverride: { active: true, severity: 'required' },
    });
    assert.strictEqual(baseline.selected && baseline.selected.id, GENE.id,
      'sanity: sole match is selected even at max drift (the trap #562 describes)');

    // With the inert ban applied, the sole match is filtered out -> null, which
    // upstream turns into "mutate a fresh gene".
    const banned = selectGene([GENE], SIGNALS, {
      driftEnabled: true, effectivePopulationSize: 1,
      plateauOverride: { active: true, severity: 'required' },
      bannedGeneIds: new Set([GENE.id]),
    });
    assert.strictEqual(banned.selected, null,
      'a banned sole-match gene must yield null so the pipeline forces mutation');
  });
});
