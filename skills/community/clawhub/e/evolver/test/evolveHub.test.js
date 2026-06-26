'use strict';

const { describe, it, before } = require('node:test');
const assert = require('node:assert/strict');

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
