const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert');
const path = require('path');
const fs = require('fs');
const os = require('os');

const mg = require('../src/gep/memoryGraph');

describe('memoryGraph - computeSignalKey', () => {
  it('returns deterministic key for same signals regardless of order', () => {
    const k1 = mg.computeSignalKey(['error_a', 'error_b']);
    const k2 = mg.computeSignalKey(['error_b', 'error_a']);
    assert.strictEqual(k1, k2);
  });

  it('returns different keys for different signals', () => {
    const k1 = mg.computeSignalKey(['error_a']);
    const k2 = mg.computeSignalKey(['error_b']);
    assert.notStrictEqual(k1, k2);
  });

  it('handles empty signal list gracefully', () => {
    const k = mg.computeSignalKey([]);
    assert.strictEqual(typeof k, 'string');
    assert.ok(k.length > 0);
  });

  it('handles non-array input gracefully', () => {
    const k = mg.computeSignalKey(null);
    assert.strictEqual(typeof k, 'string');
  });

  it('trims whitespace before hashing', () => {
    const k1 = mg.computeSignalKey(['  error_a  ']);
    const k2 = mg.computeSignalKey(['error_a']);
    assert.strictEqual(k1, k2);
  });

  it('deduplicates identical signals', () => {
    const k1 = mg.computeSignalKey(['error_a', 'error_a']);
    const k2 = mg.computeSignalKey(['error_a']);
    assert.strictEqual(k1, k2);
  });
});

function setupTmpEnv() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'mg-test-'));
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

describe('memoryGraph - getMemoryAdvice', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  it('returns advice object with expected fields', () => {
    const advice = mg.getMemoryAdvice({
      signals: ['recurring_error'],
      genes: [{ id: 'gene_test', type: 'Gene' }],
      driftEnabled: false,
    });
    assert.strictEqual(typeof advice, 'object');
    assert.ok('currentSignalKey' in advice);
    assert.ok('preferredGeneId' in advice);
    assert.ok('bannedGeneIds' in advice);
    assert.ok('explanation' in advice);
  });

  it('handles empty signals and genes', () => {
    const advice = mg.getMemoryAdvice({ signals: [], genes: [], driftEnabled: false });
    assert.strictEqual(advice.preferredGeneId, null);
  });

  it('handles null input gracefully', () => {
    const advice = mg.getMemoryAdvice({ signals: null, genes: null, driftEnabled: false });
    assert.strictEqual(typeof advice, 'object');
  });
});

// Helper: write outcome events directly so we can assert ban behavior without
// running the full attempt -> outcome state-machine flow.
function writeOutcomeEvents(tmpDir, geneId, signals, count, status) {
  const graphPath = path.join(tmpDir, 'memory_graph.jsonl');
  const signalKey = mg.computeSignalKey(signals);
  const lines = [];
  const now = Date.now();
  for (let i = 0; i < count; i++) {
    const ts = new Date(now - (count - i) * 1000).toISOString();
    const ev = {
      type: 'MemoryGraphEvent',
      kind: 'outcome',
      id: `mge_test_${i}`,
      ts,
      signal: { key: signalKey, signals },
      gene: { id: geneId, category: 'repair' },
      action: { id: `act_test_${i}` },
      outcome: { status, score: status === 'failed' ? 0 : 1 },
    };
    lines.push(JSON.stringify(ev));
  }
  fs.writeFileSync(graphPath, lines.join('\n') + '\n');
}

describe('memoryGraph - getMemoryAdvice ban respects drift mode (regression)', () => {
  // Regression for the plateau-drift-bypass-ban feedback loop (rule: drift's
  // purpose is to explore new combinations, not to resurrect proven failures).
  // Before the fix, both ban conditions were gated on `!driftEnabled`, so a
  // gene that triggered plateau detection (which forces drift on) would
  // bypass its own ban and stay in the candidate pool indefinitely.
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  const SIGNALS = ['log_error', 'recurring_error', 'repair_loop_detected'];
  const FAILED_GENE = { id: 'gene_repair_failing', type: 'Gene' };

  it('bans a saturated gene when drift is OFF', () => {
    writeOutcomeEvents(tmpDir, FAILED_GENE.id, SIGNALS, 5, 'failed');
    const advice = mg.getMemoryAdvice({
      signals: SIGNALS,
      genes: [FAILED_GENE],
      driftEnabled: false,
    });
    assert.ok(advice.bannedGeneIds instanceof Set);
    assert.ok(advice.bannedGeneIds.has(FAILED_GENE.id),
      'baseline: 5 failures on same key with drift OFF should ban the gene');
  });

  it('ALSO bans a saturated gene when drift is ON (the fix)', () => {
    writeOutcomeEvents(tmpDir, FAILED_GENE.id, SIGNALS, 5, 'failed');
    const advice = mg.getMemoryAdvice({
      signals: SIGNALS,
      genes: [FAILED_GENE],
      driftEnabled: true,
    });
    assert.ok(advice.bannedGeneIds instanceof Set);
    assert.ok(advice.bannedGeneIds.has(FAILED_GENE.id),
      'fix: drift mode must not bypass ban for repeatedly failing genes');
  });

  it('does not ban a gene with healthy success rate, drift on or off', () => {
    writeOutcomeEvents(tmpDir, 'gene_healthy', SIGNALS, 5, 'success');
    for (const drift of [false, true]) {
      const advice = mg.getMemoryAdvice({
        signals: SIGNALS,
        genes: [{ id: 'gene_healthy', type: 'Gene' }],
        driftEnabled: drift,
      });
      assert.ok(!advice.bannedGeneIds.has('gene_healthy'),
        `successful gene should not be banned (driftEnabled=${drift})`);
    }
  });
});

describe('memoryGraph - recordSignalSnapshot', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  it('writes a signal event to the memory graph', () => {
    const result = mg.recordSignalSnapshot({
      signals: ['error_crash', 'high_failure_ratio'],
      observations: { test_mode: true },
    });

    assert.ok(result);
    assert.strictEqual(result.kind, 'signal');

    const graphPath = path.join(tmpDir, 'memory_graph.jsonl');
    assert.ok(fs.existsSync(graphPath));
    const lines = fs.readFileSync(graphPath, 'utf8').trim().split('\n');
    const ev = JSON.parse(lines[0]);
    assert.strictEqual(ev.type, 'MemoryGraphEvent');
    assert.strictEqual(ev.kind, 'signal');
    assert.ok(Array.isArray(ev.signal.signals));
    assert.ok(ev.signal.signals.includes('error_crash'));
  });
});

describe('memoryGraph - recordHypothesis', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  it('writes a hypothesis event and returns hypothesisId + signalKey', () => {
    const result = mg.recordHypothesis({
      signals: ['error_crash'],
      selectedGene: { id: 'gene_test_123', category: 'repair' },
      driftEnabled: false,
    });

    assert.ok(result);
    assert.strictEqual(typeof result.hypothesisId, 'string');
    assert.strictEqual(typeof result.signalKey, 'string');

    const graphPath = path.join(tmpDir, 'memory_graph.jsonl');
    const lines = fs.readFileSync(graphPath, 'utf8').trim().split('\n');
    const ev = JSON.parse(lines[lines.length - 1]);
    assert.strictEqual(ev.kind, 'hypothesis');
    assert.strictEqual(ev.gene.id, 'gene_test_123');
  });
});

describe('memoryGraph - recordAttempt', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  it('records attempt event and returns actionId + signalKey', () => {
    const result = mg.recordAttempt({
      signals: ['recurring_error'],
      selectedGene: { id: 'gene_repair_test', category: 'repair' },
      driftEnabled: false,
    });

    assert.ok(result);
    assert.strictEqual(typeof result.actionId, 'string');
    assert.strictEqual(typeof result.signalKey, 'string');

    const graphPath = path.join(tmpDir, 'memory_graph.jsonl');
    const lines = fs.readFileSync(graphPath, 'utf8').trim().split('\n');
    const events = lines.map(l => JSON.parse(l));
    const attemptEvent = events.find(e => e.kind === 'attempt');
    assert.ok(attemptEvent);
    assert.strictEqual(attemptEvent.gene.id, 'gene_repair_test');
  });

  it('writes state file with last_action metadata', () => {
    mg.recordAttempt({
      signals: ['error_crash'],
      selectedGene: { id: 'gene_bad', category: 'repair' },
      driftEnabled: false,
    });

    const statePath = path.join(tmpDir, 'memory_graph_state.json');
    assert.ok(fs.existsSync(statePath));
    const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    assert.ok(state.last_action);
    assert.strictEqual(state.last_action.gene_id, 'gene_bad');
    assert.strictEqual(state.last_action.outcome_recorded, false);
  });
});

describe('memoryGraph - recordExternalCandidate', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  it('returns null when asset is missing type or id', () => {
    assert.strictEqual(mg.recordExternalCandidate({ asset: null }), null);
    assert.strictEqual(mg.recordExternalCandidate({ asset: { id: 'x' } }), null);
    assert.strictEqual(mg.recordExternalCandidate({ asset: { type: 'Capsule' } }), null);
  });

  // The candidate.{trigger,gene,confidence} hints are Capsule-only by design:
  // a Gene candidate must NOT acquire synthetic trigger/gene/confidence even if
  // the incoming asset carries those keys. This guards the a2a ingestion path
  // against a refactor that drops the `type === 'Capsule'` condition.
  it('populates trigger/gene/confidence for a Capsule', () => {
    const ev = mg.recordExternalCandidate({
      asset: { type: 'Capsule', id: 'cap1', trigger: ['log_error'], gene: 'gene_x', confidence: 0.8 },
      source: 'peer_node',
      signals: ['log_error'],
    });
    assert.strictEqual(ev.kind, 'external_candidate');
    assert.deepStrictEqual(ev.candidate.trigger, ['log_error']);
    assert.strictEqual(ev.candidate.gene, 'gene_x');
    assert.strictEqual(ev.candidate.confidence, 0.8);
    assert.strictEqual(ev.external.source, 'peer_node');
    assert.deepStrictEqual(ev.asset, { type: 'Capsule', id: 'cap1' });
  });

  it('does NOT synthesize Capsule-only fields for a Gene candidate', () => {
    const ev = mg.recordExternalCandidate({
      // a Gene carrying these keys must still yield the empty/null defaults
      asset: { type: 'Gene', id: 'gene1', trigger: ['x'], gene: 'g', confidence: 0.9 },
      source: 'peer_node',
      signals: [],
    });
    assert.strictEqual(ev.kind, 'external_candidate');
    assert.deepStrictEqual(ev.candidate.trigger, []);
    assert.strictEqual(ev.candidate.gene, null);
    assert.strictEqual(ev.candidate.confidence, null);
  });

  it('defaults source to "external" and persists the event', () => {
    const ev = mg.recordExternalCandidate({ asset: { type: 'Capsule', id: 'cap2' } });
    assert.strictEqual(ev.external.source, 'external');
    // confidence falls back to null when the Capsule omits it
    assert.strictEqual(ev.candidate.confidence, null);
    const events = mg.tryReadMemoryGraphEvents();
    assert.ok(events.some(e => e.id === ev.id && e.kind === 'external_candidate'));
  });
});
