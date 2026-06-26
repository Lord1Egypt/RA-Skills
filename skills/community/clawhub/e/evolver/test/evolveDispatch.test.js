'use strict';

const { describe, it, mock, before, after } = require('node:test');
const assert = require('node:assert/strict');

// ---------------------------------------------------------------------------
// Inline stubs for all external dependencies of dispatch.js
// ---------------------------------------------------------------------------

const mockMods = {};

before(() => {
  const Module = require('module');
  const origLoad = Module._load;
  Module._load = function (request, parent, isMain) {
    if (mockMods[request]) return mockMods[request];
    // Resolve relative requires from dispatch.js
    if (parent && parent.filename && parent.filename.includes('dispatch')) {
      const relMap = {
        '../../gep/assetStore': 'assetStore',
        '../../gep/prompt': 'prompt',
        '../../gep/assetCallLog': 'assetCallLog',
        '../../gep/solidify': 'solidify',
        '../../gep/bridge': 'bridge',
        '../../gep/paths': 'paths',
        '../../gep/explore': 'explore',
      };
      const key = relMap[request];
      if (key && mockMods[key]) return mockMods[key];
    }
    return origLoad.apply(this, arguments);
  };
});

after(() => {
  // No teardown needed — mocks are cleaned up per test via Object.assign resets
});

function buildCtx(overrides) {
  return {
    bridgeEnabled: false,
    recentMasterLog: 'recent log',
    todayLog: 'today log',
    memorySnippet: 'memory',
    userSnippet: 'user',
    cycleNum: 42,
    cycleId: 'cycle-42',
    mutationDirective: 'mutate x',
    healthReport: 'ok',
    fileList: 'skill1.js',
    reportingDirective: 'report to hub',
    moodStatus: 'calm',
    memorySize: 1024,
    syncDirective: 'sync',
    localStateSummary: 'local state',
    genes: [{ id: 'g1' }],
    capsules: [{ id: 'c1' }],
    recentEvents: [],
    signals: ['log_error'],
    skipHubCalls: false,
    hubHit: { hit: false },
    activeTask: null,
    hubLessons: [],
    heartbeatActionContext: '',
    sharedKnowledgeContext: '',
    externalCandidatesPreview: '(none)',
    capabilityCandidatesPreview: '(none)',
    recentFailedCapsules: [],
    selectedGene: { id: 'g1', constraints: { max_files: 5 } },
    capsuleCandidates: [],
    selector: 'signal_match',
    selectedBy: 'selector',
    selectedCapsuleId: 'c1',
    strategyPolicy: { blastRadiusMaxFiles: 5 },
    personalitySelection: { personality_key: 'explorer', personality_known: true, personality_mutations: [] },
    personalityState: { creativity: 0.8, rigor: 0.7, risk_tolerance: 0.2 },
    mutation: { id: 'm1', category: 'innovate' },
    forceInnovation: false,
    IS_RANDOM_DRIFT: false,
    IS_REVIEW_MODE: false,
    IS_DRY_RUN: false,
    AGENT_NAME: 'test-agent',
    scanTime: 500,
    initialUserPrompt: 'fix the bug',
    ...overrides,
  };
}

describe('dispatch', () => {
  it('calls writeStateForSolidify and outputs prompt to stdout when not bridged', async () => {
    let solidifyWritten = null;
    let loggedLines = [];

    mockMods['assetStore'] = { getLastEventId: () => 'evt-1' };
    mockMods['prompt'] = {
      buildGepPrompt: () => 'BUILT_PROMPT',
      buildReusePrompt: () => 'REUSE_PROMPT',
      buildHubMatchedBlock: () => 'HUB_BLOCK',
    };
    mockMods['assetCallLog'] = { logAssetCall: () => {} };
    mockMods['solidify'] = {
      readStateForSolidify: () => ({}),
      writeStateForSolidify: (state) => { solidifyWritten = state; },
    };
    mockMods['bridge'] = {
      clip: (s) => s,
      writePromptArtifact: () => ({ promptPath: '/tmp/prompt.txt' }),
      renderSessionsSpawnCall: () => 'sessions_spawn({...})',
    };
    mockMods['paths'] = { getEvolutionDir: () => '/tmp/evo', getRepoRoot: () => '/tmp/repo' };
    mockMods['explore'] = { tryExplore: async () => ({ signals: [] }) };

    // Patch execSync so git calls don't fail
    mockMods['child_process'] = { execSync: () => '' };

    delete require.cache[require.resolve('../src/evolve/pipeline/dispatch')];
    const { dispatch } = require('../src/evolve/pipeline/dispatch');

    const origLog = console.log;
    console.log = (...args) => loggedLines.push(args.join(' '));
    try {
      await dispatch(buildCtx({ bridgeEnabled: false }));
    } finally {
      console.log = origLog;
    }

    assert.ok(solidifyWritten !== null, 'writeStateForSolidify should have been called');
    assert.ok(solidifyWritten.last_run, 'last_run should be set');
    assert.equal(solidifyWritten.last_run.selected_gene_id, 'g1');
    assert.ok(loggedLines.some(l => l.includes('BUILT_PROMPT')), 'prompt should be logged');
    assert.ok(loggedLines.some(l => l.includes('SOLIDIFY REQUIRED')), 'solidify required message should be logged');
  });

  it('emits sessions_spawn when bridgeEnabled is true', async () => {
    let loggedLines = [];

    mockMods['assetStore'] = { getLastEventId: () => 'evt-2' };
    mockMods['prompt'] = {
      buildGepPrompt: () => 'BUILT_PROMPT',
      buildReusePrompt: () => 'REUSE_PROMPT',
      buildHubMatchedBlock: () => null,
    };
    mockMods['assetCallLog'] = { logAssetCall: () => {} };
    mockMods['solidify'] = {
      readStateForSolidify: () => ({ last_run: { run_id: 'run_stored' } }),
      writeStateForSolidify: () => {},
    };
    mockMods['bridge'] = {
      clip: (s) => s,
      writePromptArtifact: () => ({ promptPath: '/tmp/prompt.txt' }),
      renderSessionsSpawnCall: () => 'sessions_spawn({...})',
    };
    mockMods['paths'] = { getEvolutionDir: () => '/tmp/evo', getRepoRoot: () => '/tmp/repo' };
    mockMods['explore'] = { tryExplore: async () => ({ signals: [] }) };

    delete require.cache[require.resolve('../src/evolve/pipeline/dispatch')];
    const { dispatch } = require('../src/evolve/pipeline/dispatch');

    const origLog = console.log;
    console.log = (...args) => loggedLines.push(args.join(' '));
    try {
      await dispatch(buildCtx({ bridgeEnabled: true }));
    } finally {
      console.log = origLog;
    }

    assert.ok(loggedLines.some(l => l.includes('BRIDGE ENABLED')), 'bridge log should appear');
    assert.ok(loggedLines.some(l => l.includes('sessions_spawn')), 'sessions_spawn call should be logged');
  });

  it('skips prompt output when skipHubCalls is true', async () => {
    let loggedLines = [];
    let solidifyWritten = false;

    mockMods['assetStore'] = { getLastEventId: () => null };
    mockMods['prompt'] = { buildGepPrompt: () => 'PROMPT', buildReusePrompt: () => '', buildHubMatchedBlock: () => null };
    mockMods['assetCallLog'] = { logAssetCall: () => {} };
    mockMods['solidify'] = {
      readStateForSolidify: () => ({}),
      writeStateForSolidify: () => { solidifyWritten = true; },
    };
    mockMods['bridge'] = { clip: s => s, writePromptArtifact: () => ({}), renderSessionsSpawnCall: () => '' };
    mockMods['paths'] = { getEvolutionDir: () => '/tmp/evo', getRepoRoot: () => '/tmp/repo' };
    mockMods['explore'] = { tryExplore: async () => ({ signals: [] }) };

    delete require.cache[require.resolve('../src/evolve/pipeline/dispatch')];
    const { dispatch } = require('../src/evolve/pipeline/dispatch');

    const origLog = console.log;
    console.log = (...args) => loggedLines.push(args.join(' '));
    try {
      await dispatch(buildCtx({ skipHubCalls: true }));
    } finally {
      console.log = origLog;
    }

    assert.ok(solidifyWritten, 'solidify should still be written in idle path');
    assert.ok(loggedLines.some(l => l.includes('Idle cycle complete')), 'idle log should appear');
    assert.ok(!loggedLines.some(l => l.includes('BUILT_PROMPT')), 'prompt should NOT be logged');
  });

  it('uses buildReusePrompt when hubHit is direct-reuse', async () => {
    let loggedLines = [];
    let reusePromptCalled = false;

    mockMods['assetStore'] = { getLastEventId: () => null };
    mockMods['prompt'] = {
      buildGepPrompt: () => { throw new Error('should not call buildGepPrompt'); },
      buildReusePrompt: (opts) => { reusePromptCalled = true; return 'REUSE_PROMPT'; },
      buildHubMatchedBlock: () => null,
    };
    mockMods['assetCallLog'] = { logAssetCall: () => {} };
    mockMods['solidify'] = { readStateForSolidify: () => ({}), writeStateForSolidify: () => {} };
    mockMods['bridge'] = { clip: s => s, writePromptArtifact: () => ({}), renderSessionsSpawnCall: () => '' };
    mockMods['paths'] = { getEvolutionDir: () => '/tmp/evo', getRepoRoot: () => '/tmp/repo' };
    mockMods['explore'] = { tryExplore: async () => ({ signals: [] }) };

    delete require.cache[require.resolve('../src/evolve/pipeline/dispatch')];
    const { dispatch } = require('../src/evolve/pipeline/dispatch');

    const origLog = console.log;
    console.log = (...args) => loggedLines.push(args.join(' '));
    try {
      await dispatch(buildCtx({
        bridgeEnabled: false,
        hubHit: { hit: true, mode: 'direct', match: { id: 'asset1' }, asset_id: 'asset1', score: 0.9 },
      }));
    } finally {
      console.log = origLog;
    }

    assert.ok(reusePromptCalled, 'buildReusePrompt should be called for direct-reuse hit');
    assert.ok(loggedLines.some(l => l.includes('REUSE_PROMPT')), 'reuse prompt should be logged');
  });

  it('emits thought process block when EVOLVE_EMIT_THOUGHT_PROCESS=true', async () => {
    let loggedLines = [];

    mockMods['assetStore'] = { getLastEventId: () => null };
    mockMods['prompt'] = { buildGepPrompt: () => 'PROMPT', buildReusePrompt: () => '', buildHubMatchedBlock: () => null };
    mockMods['assetCallLog'] = { logAssetCall: () => {} };
    mockMods['solidify'] = { readStateForSolidify: () => ({}), writeStateForSolidify: () => {} };
    mockMods['bridge'] = { clip: s => s, writePromptArtifact: () => ({}), renderSessionsSpawnCall: () => '' };
    mockMods['paths'] = { getEvolutionDir: () => '/tmp/evo', getRepoRoot: () => '/tmp/repo' };
    mockMods['explore'] = { tryExplore: async () => ({ signals: [] }) };

    delete require.cache[require.resolve('../src/evolve/pipeline/dispatch')];
    const { dispatch } = require('../src/evolve/pipeline/dispatch');

    const origEnv = process.env.EVOLVE_EMIT_THOUGHT_PROCESS;
    process.env.EVOLVE_EMIT_THOUGHT_PROCESS = 'true';
    const origLog = console.log;
    console.log = (...args) => loggedLines.push(args.join(' '));
    try {
      await dispatch(buildCtx({ bridgeEnabled: false }));
    } finally {
      console.log = origLog;
      if (origEnv === undefined) delete process.env.EVOLVE_EMIT_THOUGHT_PROCESS;
      else process.env.EVOLVE_EMIT_THOUGHT_PROCESS = origEnv;
    }

    assert.ok(loggedLines.some(l => l.includes('[THOUGHT_PROCESS]')), 'thought process block should be emitted');
    assert.ok(loggedLines.some(l => l.includes('force_innovation:')), 'force_innovation field should appear');
  });

  function reuseMocks(logged) {
    mockMods['assetStore'] = { getLastEventId: () => null };
    mockMods['prompt'] = { buildGepPrompt: () => 'P', buildReusePrompt: () => 'REUSE_PROMPT', buildHubMatchedBlock: () => null };
    mockMods['assetCallLog'] = { logAssetCall: (e) => logged.push(e), assetCostIndex: () => ({}) };
    mockMods['solidify'] = { readStateForSolidify: () => ({}), writeStateForSolidify: () => {} };
    mockMods['bridge'] = { clip: s => s, writePromptArtifact: () => ({}), renderSessionsSpawnCall: () => '' };
    mockMods['paths'] = { getEvolutionDir: () => '/tmp/evo', getRepoRoot: () => '/tmp/repo' };
    mockMods['explore'] = { tryExplore: async () => ({ signals: [] }) };
    delete require.cache[require.resolve('../src/evolve/pipeline/dispatch')];
    return require('../src/evolve/pipeline/dispatch').dispatch;
  }

  it('logs MEASURED tokens_saved from the reused asset derivation_tokens', async () => {
    const logged = [];
    const dispatch = reuseMocks(logged);
    const origLog = console.log; console.log = () => {};
    try {
      await dispatch(buildCtx({
        bridgeEnabled: false,
        hubHit: {
          hit: true, mode: 'direct', asset_id: 'asset1', score: 0.9,
          match: { id: 'asset1', derivation_tokens: { total_tokens: 123456, basis: 'measured' } },
        },
      }));
    } finally { console.log = origLog; }
    const reuse = logged.find(e => e.action === 'asset_reuse');
    assert.ok(reuse, 'asset_reuse should be logged');
    assert.equal(reuse.tokens_saved, 123456);
    assert.equal(reuse.tokens_saved_basis, 'measured');
  });

  it('falls back to an ESTIMATED tokens_saved when the asset has no measured cost', async () => {
    const logged = [];
    const dispatch = reuseMocks(logged);
    const origLog = console.log; console.log = () => {};
    try {
      await dispatch(buildCtx({
        bridgeEnabled: false,
        hubHit: {
          hit: true, mode: 'direct', asset_id: 'asset2', score: 0.8,
          match: { id: 'asset2', blast_radius: { lines: 50 } },
        },
      }));
    } finally { console.log = origLog; }
    const reuse = logged.find(e => e.action === 'asset_reuse');
    assert.ok(reuse);
    assert.equal(reuse.tokens_saved_basis, 'estimated_blast_radius');
    assert.equal(reuse.tokens_saved, 160000); // 120000 + 50*800
  });

  it('discounts MEASURED tokens_saved for a reference reuse (Bugbot: was crediting the full cost)', async () => {
    const logged = [];
    const dispatch = reuseMocks(logged);
    const origLog = console.log; console.log = () => {};
    try {
      await dispatch(buildCtx({
        bridgeEnabled: false,
        hubHit: {
          hit: true, mode: 'reference', asset_id: 'asset3', score: 0.7,
          match: { id: 'asset3', derivation_tokens: { total_tokens: 123456, basis: 'measured' } },
        },
      }));
    } finally { console.log = origLog; }
    const ref = logged.find(e => e.action === 'asset_reference');
    assert.ok(ref, 'asset_reference should be logged');
    assert.equal(ref.tokens_saved_basis, 'measured');
    assert.equal(ref.tokens_saved, Math.round(123456 * 0.4)); // 49382, not the full 123456
  });
});
