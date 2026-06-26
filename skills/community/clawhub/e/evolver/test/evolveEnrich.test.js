'use strict';

const { describe, it, before } = require('node:test');
const assert = require('node:assert/strict');

// ---------------------------------------------------------------------------
// Inline stubs for all external dependencies of enrich.js
// ---------------------------------------------------------------------------

const mockMods = {};

before(() => {
  const Module = require('module');
  const origLoad = Module._load;
  Module._load = function (request, parent, isMain) {
    if (mockMods[request]) return mockMods[request];
    if (parent && parent.filename && parent.filename.includes('enrich')) {
      const relMap = {
        '../../gep/hubSearch': 'hubSearch',
        '../../gep/candidateEval': 'candidateEval',
        '../../gep/memoryGraphAdapter': 'memoryGraphAdapter',
        '../../gep/reflection': 'reflection',
        '../../gep/narrativeMemory': 'narrativeMemory',
        '../../gep/assetStore': 'assetStore',
        '../../gep/paths': 'paths',
        '../../forceUpdate': 'forceUpdate',
        '../../gep/a2aProtocol': 'a2aProtocol',
        '../../atp/autoBuyer': 'autoBuyer',
        '../../gep/personality': 'personality',
      };
      const key = relMap[request];
      if (key && mockMods[key]) return mockMods[key];
    }
    return origLoad.apply(this, arguments);
  };
});

function baseStubs() {
  mockMods['hubSearch'] = { hubSearch: async () => ({ hit: false, reason: 'no_match' }) };
  mockMods['candidateEval'] = {
    buildCandidatePreviews: () => ({ capabilityCandidatesPreview: '(none)', externalCandidatesPreview: '(none)' }),
  };
  mockMods['memoryGraphAdapter'] = {
    getAdvice: () => ({ preferredGeneId: null, bannedGeneIds: [] }),
    recordSignalSnapshot: () => {},
    recordOutcome: () => {},
    memoryGraphPath: () => '/tmp/memory.json',
  };
  mockMods['reflection'] = {
    shouldReflect: () => false,
    buildReflectionContext: () => '',
    recordReflection: () => {},
    buildSuggestedMutations: () => [],
  };
  mockMods['narrativeMemory'] = { loadNarrativeSummary: () => '' };
  mockMods['assetStore'] = { readRecentFailedCapsules: () => [] };
  mockMods['paths'] = {
    getSessionScope: () => null,
    getEvolutionDir: () => '/tmp/evo',
  };
  mockMods['forceUpdate'] = { executeForceUpdate: () => false };
  mockMods['a2aProtocol'] = {
    getNoveltyHint: () => null,
    getCapabilityGaps: () => [],
    consumeSharedKnowledgeDelta: () => null,
    consumeForceUpdate: () => null,
    consumeHeartbeatActions: () => null,
    getNodeId: () => 'node-1',
  };
  mockMods['autoBuyer'] = { isStarted: () => false };
  mockMods['personality'] = { forcePivot: () => {} };
}

function buildCtx(overrides) {
  return {
    signals: ['log_error'],
    recentEvents: [],
    recentMasterLog: 'some log',
    todayLog: 'today',
    genes: [],
    capsules: [],
    skipHubCalls: false,
    activeTask: null,
    hubLessons: [],
    IS_RANDOM_DRIFT: false,
    IS_REVIEW_MODE: false,
    IS_DRY_RUN: false,
    AGENT_NAME: 'test-agent',
    scanTime: 100,
    memorySize: 1024,
    healthReport: 'ok',
    moodStatus: 'calm',
    ...overrides,
  };
}

describe('enrich', () => {
  it('returns expected ctx additions with default stubs', async () => {
    baseStubs();
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    const result = await enrich(buildCtx());
    assert.ok('observations' in result, 'observations should be present');
    assert.ok('capabilityCandidatesPreview' in result, 'capabilityCandidatesPreview should be present');
    assert.ok('externalCandidatesPreview' in result, 'externalCandidatesPreview should be present');
    assert.ok('hubHit' in result, 'hubHit should be present');
    assert.ok('memoryAdvice' in result, 'memoryAdvice should be present');
    assert.ok(Array.isArray(result.recentFailedCapsules), 'recentFailedCapsules should be an array');
    assert.equal(result.observations.agent, 'test-agent');
    assert.equal(result.observations.dry_run, false);
  });

  it('throws when recordOutcomeFromState fails (blocking — no memoryless evolution)', async () => {
    baseStubs();
    mockMods['memoryGraphAdapter'] = {
      ...mockMods['memoryGraphAdapter'],
      recordOutcome: () => { throw new Error('disk full'); },
    };
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    await assert.rejects(
      () => enrich(buildCtx()),
      /MemoryGraph Outcome write failed/
    );
  });

  it('throws when recordSignalSnapshot fails (blocking — no memoryless evolution)', async () => {
    baseStubs();
    mockMods['memoryGraphAdapter'] = {
      ...mockMods['memoryGraphAdapter'],
      recordSignalSnapshot: () => { throw new Error('permission denied'); },
    };
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    await assert.rejects(
      () => enrich(buildCtx()),
      /MemoryGraph Signal snapshot write failed/
    );
  });

  it('throws when getMemoryAdvice fails (blocking — no memoryless evolution)', async () => {
    baseStubs();
    mockMods['memoryGraphAdapter'] = {
      ...mockMods['memoryGraphAdapter'],
      getAdvice: () => { throw new Error('corrupt graph'); },
    };
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    await assert.rejects(
      () => enrich(buildCtx()),
      /MemoryGraph Read failed/
    );
  });

  it('sets hubHit to idle_skip when skipHubCalls is true', async () => {
    baseStubs();
    let hubSearchCalled = false;
    mockMods['hubSearch'] = { hubSearch: async () => { hubSearchCalled = true; return { hit: true }; } };
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    const result = await enrich(buildCtx({ skipHubCalls: true }));
    assert.equal(hubSearchCalled, false, 'hubSearch should not be called when skipHubCalls=true');
    assert.equal(result.hubHit.hit, false);
    assert.equal(result.hubHit.reason, 'idle_skip');
  });

  it('injects hub_search_miss_with_problem when problem signal present but hub misses', async () => {
    baseStubs();
    mockMods['hubSearch'] = { hubSearch: async () => ({ hit: false, reason: 'no_match' }) };
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    const result = await enrich(buildCtx({ signals: ['log_error'] }));
    assert.ok(result.signals.includes('hub_search_miss_with_problem'), 'should inject hub_search_miss_with_problem');
  });

  it('does not inject hub_search_miss_with_problem when hub hits', async () => {
    baseStubs();
    mockMods['hubSearch'] = {
      hubSearch: async () => ({ hit: true, asset_id: 'a1', score: 0.9, mode: 'direct' }),
    };
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    const result = await enrich(buildCtx({ signals: ['log_error'] }));
    assert.ok(!result.signals.includes('hub_search_miss_with_problem'), 'should NOT inject miss signal on hub hit');
    assert.ok(result.hubHit.hit, 'hubHit.hit should be true');
  });

  it('local plateau FORCE (>=10 consecutive failures) sets IS_RANDOM_DRIFT=true and injects plateau_pivot_required', async () => {
    baseStubs();
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    const failEvents = Array.from({ length: 10 }, () => ({ outcome: { status: 'failure' } }));
    const result = await enrich(buildCtx({ recentEvents: failEvents }));
    assert.equal(result.IS_RANDOM_DRIFT, true, 'IS_RANDOM_DRIFT should be set to true on forced plateau');
    assert.ok(result.signals.includes('plateau_pivot_required'), 'plateau_pivot_required signal should be injected');
    assert.ok(result.plateauOverride && result.plateauOverride.severity === 'required', 'plateauOverride.severity should be required');
    assert.equal(result.plateauOverride.source, 'local');
  });

  it('local plateau SUGGEST (5-9 consecutive failures) injects plateau_pivot_suggested without forcing drift', async () => {
    baseStubs();
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    const failEvents = Array.from({ length: 5 }, () => ({ outcome: { status: 'failure' } }));
    const result = await enrich(buildCtx({ recentEvents: failEvents }));
    assert.ok(result.signals.includes('plateau_pivot_suggested'), 'plateau_pivot_suggested signal should be injected');
    assert.ok(result.plateauOverride && result.plateauOverride.severity === 'suggested', 'plateauOverride.severity should be suggested');
    // IS_RANDOM_DRIFT is NOT forced to true for suggested level
    assert.equal(result.IS_RANDOM_DRIFT, false, 'IS_RANDOM_DRIFT should NOT be forced for suggested pivot');
  });

  it('preserves existing ctx fields in returned ctx', async () => {
    baseStubs();
    delete require.cache[require.resolve('../src/evolve/pipeline/enrich')];
    const { enrich } = require('../src/evolve/pipeline/enrich');
    const result = await enrich(buildCtx({ customField: 'keep-me', activeTask: { id: 't1' } }));
    assert.equal(result.customField, 'keep-me');
    assert.deepEqual(result.activeTask, { id: 't1' });
  });
});
