'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const select = require('../src/evolve/pipeline/select');

// IMPORTANT: selectAndMutate writes hypothesis/attempt entries to the memory
// graph via src/gep/memoryGraph. Without redirecting EVOLUTION_DIR /
// MEMORY_GRAPH_PATH to a tmp dir, every test run pollutes the developer's
// real memory/evolution/memory_graph.jsonl with `agent: "test"` events that
// never get an outcome (selector finds no gene), creating phantom "running"
// pipelines in the WebUI forever. Mirrors the pattern in
// test/memoryGraph.test.js and test/tttInspired.test.js.
const REDIRECT_ENV_KEYS = [
  'EVOLVER_REPO_ROOT',
  'MEMORY_GRAPH_PATH',
  'EVOLUTION_DIR',
  'OPENCLAW_WORKSPACE',
  'EVOLVER_SESSION_SCOPE',
];

function setupTmpEnv() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'select-test-'));
  const origEnv = {};
  for (const k of REDIRECT_ENV_KEYS) origEnv[k] = process.env[k];
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
  try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) { /* best-effort */ }
}

function readMemoryGraphEvents(graphPath) {
  return fs.readFileSync(graphPath, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

// ---------------------------------------------------------------------------
// computeAdaptiveStrategyPolicy
// ---------------------------------------------------------------------------
describe('computeAdaptiveStrategyPolicy', () => {
  it('returns an object with expected shape', () => {
    const policy = select.computeAdaptiveStrategyPolicy({ recentEvents: [], selectedGene: null, signals: [] });
    assert.ok(typeof policy.name === 'string');
    assert.ok(typeof policy.forceInnovate === 'boolean');
    assert.ok(typeof policy.cautiousExecution === 'boolean');
    assert.ok(typeof policy.blastRadiusMaxFiles === 'number');
    assert.ok(Array.isArray(policy.directives));
  });

  it('forces innovation after 3+ consecutive repair events', () => {
    const tail = Array.from({ length: 3 }, () => ({ intent: 'repair', outcome: { status: 'failed' } }));
    const policy = select.computeAdaptiveStrategyPolicy({
      recentEvents: tail,
      selectedGene: null,
      signals: [],
    });
    assert.equal(policy.forceInnovate, true);
  });

  it('does not force innovation when log_error present even with repair streak', () => {
    const tail = Array.from({ length: 3 }, () => ({ intent: 'repair', outcome: { status: 'failed' } }));
    const policy = select.computeAdaptiveStrategyPolicy({
      recentEvents: tail,
      selectedGene: null,
      signals: ['log_error'],
    });
    assert.equal(policy.forceInnovate, false);
  });

  it('sets cautiousExecution true after 2+ consecutive failures', () => {
    const tail = [
      { intent: 'optimize', outcome: { status: 'failed' } },
      { intent: 'optimize', outcome: { status: 'failed' } },
    ];
    const policy = select.computeAdaptiveStrategyPolicy({
      recentEvents: tail,
      selectedGene: null,
      signals: [],
    });
    assert.equal(policy.cautiousExecution, true);
  });

  it('caps blastRadiusMaxFiles at 6 when cautiousExecution', () => {
    const tail = Array.from({ length: 3 }, () => ({ intent: 'optimize', outcome: { status: 'failed' } }));
    const policy = select.computeAdaptiveStrategyPolicy({
      recentEvents: tail,
      selectedGene: { constraints: { max_files: 20 } },
      signals: ['log_error'],
    });
    assert.ok(policy.blastRadiusMaxFiles <= 6);
  });

  it('handles empty/null opts gracefully', () => {
    assert.doesNotThrow(() => select.computeAdaptiveStrategyPolicy({}));
    assert.doesNotThrow(() => select.computeAdaptiveStrategyPolicy(null));
    assert.doesNotThrow(() => select.computeAdaptiveStrategyPolicy(undefined));
  });
});

// ---------------------------------------------------------------------------
// selectAndMutate
// ---------------------------------------------------------------------------
describe('selectAndMutate', () => {
  let tmpDir, origEnv;
  beforeEach(() => { ({ tmpDir, origEnv } = setupTmpEnv()); });
  afterEach(() => { teardownTmpEnv(tmpDir, origEnv); });

  const baseCtx = {
    genes: [],
    capsules: [],
    signals: [],
    recentEvents: [],
    memoryAdvice: null,
    recentFailedCapsules: [],
    heartbeatCapGaps: [],
    heartbeatNovelty: null,
    plateauOverride: null,
    observations: {
      agent: 'test',
      session_scope: null,
      drift_enabled: false,
      review_mode: false,
      dry_run: false,
      system_health: '',
      mood: null,
      scan_ms: 0,
      memory_size_bytes: 0,
      recent_error_count: 0,
      node: process.version,
      platform: process.platform,
      cwd: process.cwd(),
      evidence: {},
    },
    IS_RANDOM_DRIFT: false,
    hubHit: null,
  };

  it('returns ctx with all expected selection fields', async () => {
    const result = await select.selectAndMutate(baseCtx);
    assert.ok('selectedGene' in result);
    assert.ok('strategyPolicy' in result);
    assert.ok('personalitySelection' in result);
    assert.ok('personalityState' in result);
    assert.ok('mutation' in result, 'mutation should be present');
    assert.ok('mutationInnovateMode' in result);
    assert.ok('hypothesisId' in result);
    assert.ok('selectedBy' in result);
    assert.ok(Array.isArray(result.capsulesUsed));
  });

  it('preserves existing ctx fields', async () => {
    const ctx = { ...baseCtx, cycleNum: 7, someField: 'preserved' };
    const result = await select.selectAndMutate(ctx);
    assert.equal(result.cycleNum, 7);
    assert.equal(result.someField, 'preserved');
  });

  it('passes ctx.forcedGeneId into gene selection', async () => {
    const genes = [
      {
        type: 'Gene',
        id: 'gene_repair_runtime',
        category: 'repair',
        signals_match: ['error'],
        strategy: ['fix the error'],
        validation: ['node -e "true"'],
      },
      {
        type: 'Gene',
        id: 'gene_forced_runtime',
        category: 'optimize',
        signals_match: ['unrelated'],
        strategy: ['honor runtime override'],
        validation: ['node -e "true"'],
      },
    ];
    const result = await select.selectAndMutate({
      ...baseCtx,
      genes,
      signals: ['error'],
      forcedGeneId: 'gene_forced_runtime',
    });

    assert.ok(result.selectedGene);
    assert.equal(result.selectedGene.id, 'gene_forced_runtime');
    assert.equal(result.selector.selectionPath, 'forced_gene');
  });

  it('records forced gene provenance when memory preference exists', async () => {
    const genes = [
      {
        type: 'Gene',
        id: 'gene_memory_preferred',
        category: 'repair',
        signals_match: ['error', 'exception', 'failed'],
        strategy: ['fix the preferred error'],
        validation: ['node -e "true"'],
      },
      {
        type: 'Gene',
        id: 'gene_forced_runtime',
        category: 'optimize',
        signals_match: ['unrelated'],
        strategy: ['honor runtime override'],
        validation: ['node -e "true"'],
      },
    ];
    const result = await select.selectAndMutate({
      ...baseCtx,
      genes,
      signals: ['error', 'exception', 'failed'],
      memoryAdvice: {
        bannedGeneIds: new Set(),
        preferredGeneId: 'gene_memory_preferred',
        totalAttempts: 1,
      },
      forcedGeneId: 'gene_forced_runtime',
    });

    assert.ok(result.selectedGene);
    assert.equal(result.selectedGene.id, 'gene_forced_runtime');
    assert.equal(result.selectedBy, 'forced_gene');
    assert.equal(result.selector.selectionPath, 'forced_gene');
    assert.equal(result.selector.memoryUsed, false);

    const events = readMemoryGraphEvents(process.env.MEMORY_GRAPH_PATH);
    const hypothesis = events.find((event) => event.kind === 'hypothesis');
    const attempt = events.find((event) => event.kind === 'attempt');
    assert.ok(hypothesis, 'hypothesis event should be recorded');
    assert.ok(attempt, 'attempt event should be recorded');
    assert.equal(hypothesis.action.selected_by, 'forced_gene');
    assert.equal(attempt.action.selected_by, 'forced_gene');
    assert.notEqual(hypothesis.action.selected_by, 'memory_graph+selector');
    assert.notEqual(attempt.action.selected_by, 'memory_graph+selector');
  });

  it('passes ctx.requiredGeneId into gene selection', async () => {
    const genes = [
      {
        type: 'Gene',
        id: 'gene_repair_runtime',
        category: 'repair',
        signals_match: ['error'],
        strategy: ['fix the error'],
        validation: ['node -e "true"'],
      },
      {
        type: 'Gene',
        id: 'gene_required_runtime',
        category: 'optimize',
        signals_match: ['unrelated'],
        strategy: ['honor required runtime override'],
        validation: ['node -e "true"'],
      },
    ];
    const result = await select.selectAndMutate({
      ...baseCtx,
      genes,
      signals: ['error'],
      requiredGeneId: 'gene_required_runtime',
    });

    assert.ok(result.selectedGene);
    assert.equal(result.selectedGene.id, 'gene_required_runtime');
    assert.equal(result.selector.selectionPath, 'forced_gene');
  });

  it('sets mutationInnovateMode true when IS_RANDOM_DRIFT is true', async () => {
    const result = await select.selectAndMutate({ ...baseCtx, IS_RANDOM_DRIFT: true });
    assert.equal(result.mutationInnovateMode, true);
  });

  it('sets mutationInnovateMode true when FORCE_INNOVATION env is set', async () => {
    const orig = process.env.FORCE_INNOVATION;
    process.env.FORCE_INNOVATION = 'true';
    try {
      const result = await select.selectAndMutate(baseCtx);
      assert.equal(result.mutationInnovateMode, true);
    } finally {
      if (orig === undefined) delete process.env.FORCE_INNOVATION;
      else process.env.FORCE_INNOVATION = orig;
    }
  });

  it('mutation object is always present', async () => {
    const result = await select.selectAndMutate(baseCtx);
    assert.ok(result.mutation !== null && result.mutation !== undefined, 'mutation is mandatory');
  });

  // Regression: tests must not pollute the developer's real memory_graph.jsonl
  // with `agent: "test"` events. If this assertion fires it means the env
  // redirect above broke -- fix the tmp env, NOT the assertion. See B) hunt
  // in the WebUI diagnose chat for context.
  it('writes to the redirected tmp memory graph, not the real one', async () => {
    await select.selectAndMutate(baseCtx);
    const tmpGraphPath = process.env.MEMORY_GRAPH_PATH;
    assert.ok(tmpGraphPath && tmpGraphPath.startsWith(os.tmpdir()),
      'MEMORY_GRAPH_PATH must point inside os.tmpdir()');
    assert.ok(fs.existsSync(tmpGraphPath), 'tmp memory_graph.jsonl should be created by the call');
  });
});
