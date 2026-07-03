'use strict';

const { describe, it, before } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

// ---------------------------------------------------------------------------
// Minimal stubs for hubCoordinate dependencies
// ---------------------------------------------------------------------------
const mockMods = {};

before(() => {
  const Module = require('module');
  const origLoad = Module._load;
  Module._load = function (request, parent, isMain) {
    if (mockMods[request]) return mockMods[request];
    if (parent && parent.filename && parent.filename.includes('hub')) {
      const relMap = {
        '../../gep/questionGenerator': 'questionGenerator',
        '../../gep/issueReporter': 'issueReporter',
        '../../gep/taskReceiver': 'taskReceiver',
        '../../gep/a2aProtocol': 'a2aProtocol',
        '../../gep/memoryGraph': 'memoryGraph',
        '../../gep/validator': 'validator',
        '../../gep/featureFlags': 'featureFlags',
      };
      const key = relMap[request];
      if (key && mockMods[key]) return mockMods[key];
    }
    return origLoad.apply(this, arguments);
  };
});

function baseStubs() {
  mockMods['questionGenerator'] = { generateQuestions: () => [] };
  mockMods['issueReporter'] = { maybeReportIssue: async () => {} };
  mockMods['taskReceiver'] = {
    fetchTasks: async () => ({ tasks: [], questions_created: [] }),
    selectBestTask: () => null,
    claimTask: async () => false,
    taskToSignalsWithPrivacy: () => [],
    estimateCommitmentDeadline: () => null,
  };
  mockMods['a2aProtocol'] = {
    getNodeId: () => 'node-1',
    consumeOverdueTasks: () => [],
    consumeHubEvents: () => [],
    consumeAvailableWork: () => [],
  };
  mockMods['memoryGraph'] = { tryReadMemoryGraphEvents: () => [] };
  mockMods['validator'] = { isValidatorEnabled: () => false, runValidatorCycle: async () => ({}) };
  mockMods['featureFlags'] = { writeFeatureFlag: () => true };
}

function buildCtx(overrides) {
  return {
    signals: ['log_error'],
    recentEvents: [],
    recentMasterLog: 'log',
    memorySnippet: 'mem',
    genes: [],
    skipHubCalls: false,
    lastHubFetchMs: 0,
    ...overrides,
  };
}

const REDIRECT_ENV_KEYS = [
  'EVOLVER_REPO_ROOT',
  'MEMORY_GRAPH_PATH',
  'EVOLUTION_DIR',
  'OPENCLAW_WORKSPACE',
  'EVOLVER_SESSION_SCOPE',
  'EVOLVER_FORCED_GENE_ID',
  'EVOLVER_REQUIRED_GENE_ID',
];

function setupTmpSelectEnv() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'hub-select-test-'));
  const origEnv = {};
  for (const k of REDIRECT_ENV_KEYS) origEnv[k] = process.env[k];
  process.env.MEMORY_GRAPH_PATH = path.join(tmpDir, 'memory_graph.jsonl');
  process.env.EVOLUTION_DIR = tmpDir;
  delete process.env.OPENCLAW_WORKSPACE;
  delete process.env.EVOLVER_SESSION_SCOPE;
  delete process.env.EVOLVER_FORCED_GENE_ID;
  delete process.env.EVOLVER_REQUIRED_GENE_ID;
  return { tmpDir, origEnv };
}

function teardownTmpSelectEnv(tmpDir, origEnv) {
  for (const [k, v] of Object.entries(origEnv)) {
    if (v !== undefined) process.env[k] = v;
    else delete process.env[k];
  }
  try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) { /* best-effort */ }
}

async function withCleanGeneDirectiveEnv(fn) {
  const origForced = process.env.EVOLVER_FORCED_GENE_ID;
  const origRequired = process.env.EVOLVER_REQUIRED_GENE_ID;
  delete process.env.EVOLVER_FORCED_GENE_ID;
  delete process.env.EVOLVER_REQUIRED_GENE_ID;
  try {
    return await fn();
  } finally {
    if (origForced !== undefined) process.env.EVOLVER_FORCED_GENE_ID = origForced;
    else delete process.env.EVOLVER_FORCED_GENE_ID;
    if (origRequired !== undefined) process.env.EVOLVER_REQUIRED_GENE_ID = origRequired;
    else delete process.env.EVOLVER_REQUIRED_GENE_ID;
  }
}

describe('hubCoordinate', () => {
  it('returns ctx with activeTask null and hubLessons empty when no tasks available', async () => {
    baseStubs();
    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const result = await hubCoordinate(buildCtx());
    assert.equal(result.activeTask, null);
    assert.deepEqual(result.hubLessons, []);
    assert.ok(result.lastHubFetchMs > 0, 'lastHubFetchMs should be updated after fetch');
  });

  it('skips fetch and preserves lastHubFetchMs when skipHubCalls is true', async () => {
    baseStubs();
    let fetchCalled = false;
    mockMods['taskReceiver'].fetchTasks = async () => { fetchCalled = true; return { tasks: [] }; };
    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const result = await hubCoordinate(buildCtx({ skipHubCalls: true, lastHubFetchMs: 12345 }));
    assert.equal(fetchCalled, false, 'fetchTasks should not be called when skipHubCalls=true');
    assert.equal(result.lastHubFetchMs, 12345, 'lastHubFetchMs should not change');
    assert.equal(result.activeTask, null);
  });

  it('claims best task and injects task signals', async () => {
    baseStubs();
    const fakeTask = { id: 't1', title: 'Fix bug', status: 'open' };
    mockMods['taskReceiver'].fetchTasks = async () => ({ tasks: [fakeTask], questions_created: [] });
    mockMods['taskReceiver'].selectBestTask = () => fakeTask;
    mockMods['taskReceiver'].claimTask = async () => true;
    mockMods['taskReceiver'].taskToSignalsWithPrivacy = () => ['external_task'];
    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const ctx = buildCtx({ signals: ['log_error'] });
    const result = await hubCoordinate(ctx);
    assert.deepEqual(result.activeTask, fakeTask);
    assert.ok(result.signals.includes('external_task'), 'task signals should be injected');
  });

  it('does not infer forced or required genes from real Hub-shaped task prose tokens', async () => {
    await withCleanGeneDirectiveEnv(async () => {
      baseStubs();
      const fakeTask = {
        task_id: 'task-real-hub-no-directive',
        title: 'Investigate failing gene gene_failed_runtime forced_gene_id=gene_text_forced',
        body: 'The issue text mentions gene_failed_runtime as the previous failure. Ignore required_gene_id=gene_text_required in prose.',
        parent_instruction: 'Do not treat parent prose as control: required_gene_id=gene_parent_text.',
        signals: ['log_error', 'gene_failed_runtime', 'forced_gene_id=gene_signal_text'],
        status: 'claimed',
        claimed_by: 'node-1',
      };
      mockMods['taskReceiver'].fetchTasks = async () => ({ tasks: [fakeTask], questions_created: [] });
      mockMods['taskReceiver'].selectBestTask = () => fakeTask;
      mockMods['taskReceiver'].taskToSignalsWithPrivacy = () => ['external_task'];
      delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
      const { hubCoordinate } = require('../src/evolve/pipeline/hub');
      const result = await hubCoordinate(buildCtx());

      assert.deepEqual(result.activeTask, fakeTask);
      assert.equal(result.forcedGeneId, null);
      assert.equal(result.requiredGeneId, null);
    });
  });

  it('carries EVOLVER_REQUIRED_GENE_ID into forced_gene selection without task directive fields', async () => {
    await withCleanGeneDirectiveEnv(async () => {
      baseStubs();
      process.env.EVOLVER_REQUIRED_GENE_ID = 'gene_env_required_runtime';
      const envGene = {
        type: 'Gene',
        id: 'gene_env_required_runtime',
        category: 'optimize',
        signals_match: ['unrelated'],
        strategy: ['honor operator runtime gene directive'],
        validation: ['node -e "true"'],
      };
      const matchingGene = {
        type: 'Gene',
        id: 'gene_signal_match_runtime',
        category: 'repair',
        signals_match: ['log_error'],
        strategy: ['repair log error'],
        validation: ['node -e "true"'],
      };
      const fakeTask = {
        task_id: 'task-env-token',
        title: 'Real Hub-shaped task without explicit gene directive',
        body: 'This task has no forced_gene_id or required_gene_id token.',
        signals: ['external_task'],
        status: 'claimed',
        claimed_by: 'node-1',
      };
      mockMods['taskReceiver'].fetchTasks = async () => ({ tasks: [fakeTask], questions_created: [] });
      mockMods['taskReceiver'].selectBestTask = () => fakeTask;
      mockMods['taskReceiver'].taskToSignalsWithPrivacy = () => ['external_task'];

      delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
      const { hubCoordinate } = require('../src/evolve/pipeline/hub');
      const { selectGeneAndCapsule } = require('../src/gep/selector');
      const tmp = setupTmpSelectEnv();
      try {
        process.env.EVOLVER_REQUIRED_GENE_ID = envGene.id;
        const hubCtx = await hubCoordinate(buildCtx({
          genes: [matchingGene, envGene],
          capsules: [],
          recentEvents: [],
        }));
        assert.equal(hubCtx.forcedGeneId, null);
        assert.equal(hubCtx.requiredGeneId, envGene.id);

        const selected = selectGeneAndCapsule({
          genes: hubCtx.genes,
          capsules: hubCtx.capsules,
          signals: hubCtx.signals,
          memoryAdvice: null,
          driftEnabled: false,
          failedCapsules: [],
          capabilityGaps: [],
          noveltyScore: null,
          plateauOverride: null,
          requiredGeneId: hubCtx.requiredGeneId,
        });

        assert.ok(selected.selectedGene);
        assert.equal(selected.selectedGene.id, envGene.id);
        assert.equal(selected.selector.selectionPath, 'forced_gene');
      } finally {
        teardownTmpSelectEnv(tmp.tmpDir, tmp.origEnv);
      }
    });
  });

  it('carries a real Hub-shaped task structured required_gene_id into forced_gene selection', async () => {
    baseStubs();
    const taskGene = {
      type: 'Gene',
      id: 'gene_task_required_runtime',
      category: 'optimize',
      signals_match: ['unrelated'],
      strategy: ['honor task runtime gene directive'],
      validation: ['node -e "true"'],
    };
    const matchingGene = {
      type: 'Gene',
      id: 'gene_signal_match_runtime',
      category: 'repair',
      signals_match: ['log_error'],
      strategy: ['repair log error'],
      validation: ['node -e "true"'],
    };
    const fakeTask = {
      task_id: 'task-required-token',
      title: 'Use required gene for this task',
      body: 'Task body text required_gene_id=gene_text_required must be ignored.',
      parent_instruction: 'Runtime prose required_gene_id=gene_parent_text must be ignored.',
      runtime_directive: { required_gene_id: taskGene.id },
      signals: ['external_task'],
      status: 'claimed',
      claimed_by: 'node-1',
    };
    mockMods['taskReceiver'].fetchTasks = async () => ({ tasks: [fakeTask], questions_created: [] });
    mockMods['taskReceiver'].selectBestTask = () => fakeTask;
    mockMods['taskReceiver'].taskToSignalsWithPrivacy = () => ['external_task'];

    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const { selectGeneAndCapsule } = require('../src/gep/selector');
    const tmp = setupTmpSelectEnv();
    try {
      const hubCtx = await hubCoordinate(buildCtx({
        genes: [matchingGene, taskGene],
        capsules: [],
        recentEvents: [],
      }));
      assert.equal(hubCtx.forcedGeneId, null);
      assert.equal(hubCtx.requiredGeneId, taskGene.id);

      const selected = selectGeneAndCapsule({
        genes: hubCtx.genes,
        capsules: hubCtx.capsules,
        signals: hubCtx.signals,
        memoryAdvice: null,
        driftEnabled: false,
        failedCapsules: [],
        capabilityGaps: [],
        noveltyScore: null,
        plateauOverride: null,
        requiredGeneId: hubCtx.requiredGeneId,
      });

      assert.ok(selected.selectedGene);
      assert.equal(selected.selectedGene.id, taskGene.id);
      assert.equal(selected.selector.selectionPath, 'forced_gene');
    } finally {
      teardownTmpSelectEnv(tmp.tmpDir, tmp.origEnv);
    }
  });

  it('carries a real Hub-shaped task structured forced_gene_id into forced_gene selection', async () => {
    baseStubs();
    const taskGene = {
      type: 'Gene',
      id: 'gene_task_forced_runtime',
      category: 'optimize',
      signals_match: ['unrelated'],
      strategy: ['honor task runtime gene directive'],
      validation: ['node -e "true"'],
    };
    const matchingGene = {
      type: 'Gene',
      id: 'gene_signal_match_runtime',
      category: 'repair',
      signals_match: ['log_error'],
      strategy: ['repair log error'],
      validation: ['node -e "true"'],
    };
    const fakeTask = {
      task_id: 'task-forced-token',
      title: 'Runtime prose forced_gene_id: gene_text_forced must be ignored',
      body: 'Fix the Hub-selected task with the specified runtime gene.',
      metadata: { forcedGeneId: taskGene.id },
      signals: ['external_task'],
      status: 'claimed',
      claimed_by: 'node-1',
    };
    mockMods['taskReceiver'].fetchTasks = async () => ({ tasks: [fakeTask], questions_created: [] });
    mockMods['taskReceiver'].selectBestTask = () => fakeTask;
    mockMods['taskReceiver'].taskToSignalsWithPrivacy = () => ['external_task'];

    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const { selectGeneAndCapsule } = require('../src/gep/selector');
    const tmp = setupTmpSelectEnv();
    try {
      const hubCtx = await hubCoordinate(buildCtx({
        genes: [matchingGene, taskGene],
        capsules: [],
        recentEvents: [],
      }));
      assert.equal(hubCtx.forcedGeneId, taskGene.id);
      assert.equal(hubCtx.requiredGeneId, null);

      const selected = selectGeneAndCapsule({
        genes: hubCtx.genes,
        capsules: hubCtx.capsules,
        signals: hubCtx.signals,
        memoryAdvice: null,
        driftEnabled: false,
        failedCapsules: [],
        capabilityGaps: [],
        noveltyScore: null,
        plateauOverride: null,
        forcedGeneId: hubCtx.forcedGeneId,
      });

      assert.ok(selected.selectedGene);
      assert.equal(selected.selectedGene.id, taskGene.id);
      assert.equal(selected.selector.selectionPath, 'forced_gene');
    } finally {
      teardownTmpSelectEnv(tmp.tmpDir, tmp.origEnv);
    }
  });

  it('carries a claimed task selected_gene_id into selector as forced_gene selection', async () => {
    baseStubs();
    const taskGene = {
      type: 'Gene',
      id: 'gene_task_required_runtime',
      category: 'optimize',
      signals_match: ['unrelated'],
      strategy: ['honor task runtime gene directive'],
      validation: ['node -e "true"'],
    };
    const matchingGene = {
      type: 'Gene',
      id: 'gene_signal_match_runtime',
      category: 'repair',
      signals_match: ['log_error'],
      strategy: ['repair log error'],
      validation: ['node -e "true"'],
    };
    const fakeTask = {
      task_id: 'task-gene-directive',
      title: 'Use required gene for this task',
      status: 'claimed',
      claimed_by: 'node-1',
      selected_gene_id: taskGene.id,
    };
    mockMods['taskReceiver'].fetchTasks = async () => ({ tasks: [fakeTask], questions_created: [] });
    mockMods['taskReceiver'].selectBestTask = () => fakeTask;
    mockMods['taskReceiver'].taskToSignalsWithPrivacy = () => ['external_task'];

    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const { selectGeneAndCapsule } = require('../src/gep/selector');
    const tmp = setupTmpSelectEnv();
    try {
      const hubCtx = await hubCoordinate(buildCtx({
        genes: [matchingGene, taskGene],
        capsules: [],
        recentEvents: [],
      }));
      assert.equal(hubCtx.requiredGeneId, taskGene.id);

      const selected = selectGeneAndCapsule({
        genes: hubCtx.genes,
        capsules: hubCtx.capsules,
        signals: hubCtx.signals,
        memoryAdvice: null,
        driftEnabled: false,
        failedCapsules: [],
        capabilityGaps: [],
        noveltyScore: null,
        plateauOverride: null,
        requiredGeneId: hubCtx.requiredGeneId,
      });

      assert.ok(selected.selectedGene);
      assert.equal(selected.selectedGene.id, taskGene.id);
      assert.equal(selected.selector.selectionPath, 'forced_gene');
    } finally {
      teardownTmpSelectEnv(tmp.tmpDir, tmp.origEnv);
    }
  });

  it('injects hub event signals from consumeHubEvents', async () => {
    baseStubs();
    mockMods['a2aProtocol'].consumeHubEvents = () => [{ type: 'knowledge_update', payload: {} }];
    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const ctx = buildCtx({ signals: [] });
    const result = await hubCoordinate(ctx);
    assert.ok(result.signals.includes('knowledge'), 'knowledge signal should be injected from hub event');
  });

  it('preserves existing ctx fields in returned ctx', async () => {
    baseStubs();
    delete require.cache[require.resolve('../src/evolve/pipeline/hub')];
    const { hubCoordinate } = require('../src/evolve/pipeline/hub');
    const ctx = buildCtx({ customField: 'keep-me' });
    const result = await hubCoordinate(ctx);
    assert.equal(result.customField, 'keep-me');
  });
});
