const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

if (!process.env.A2A_NODE_SECRET) {
  process.env.A2A_NODE_SECRET = 'a'.repeat(64);
}

// Rigged require cache: swap the forceUpdate module for a spy BEFORE
// a2aProtocol is required, so _maybeTriggerForceUpdateFromHeartbeat picks up
// the spy instead of spawning npm/degit against the real network.
const forceUpdatePath = require.resolve('../src/forceUpdate');
let executeForceUpdateCalls = [];
let executeForceUpdateReturn = false;
let executeForceUpdateReturns = [];
const SPY_NOOP = Symbol('SPY_FORCE_UPDATE_NOOP');
require.cache[forceUpdatePath] = {
  id: forceUpdatePath,
  filename: forceUpdatePath,
  loaded: true,
  exports: {
    executeForceUpdate: function (fu) {
      executeForceUpdateCalls.push(fu);
      if (executeForceUpdateReturns.length > 0) return executeForceUpdateReturns.shift();
      return executeForceUpdateReturn;
    },
    FORCE_UPDATE_NOOP: SPY_NOOP,
  },
};

const a2aProtocol = require('../src/gep/a2aProtocol');
const { sendHeartbeat } = a2aProtocol;
const { _resetForceUpdateStateForTesting } = a2aProtocol._testing;

describe('heartbeat-triggered force_update', () => {
  var tmpDir;
  var originalFetch;
  var originalHubUrl;
  var originalLogsDir;
  var originalProcessExit;
  var exitCalls;

  var originalInsecure;
  var originalAntiAbuseTelemetry;
  var originalAntiAbuseSalt;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-fu-test-'));
    originalHubUrl = process.env.A2A_HUB_URL;
    originalLogsDir = process.env.EVOLVER_LOGS_DIR;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    originalAntiAbuseTelemetry = process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
    originalAntiAbuseSalt = process.env.EVOLVER_ANTI_ABUSE_SALT;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOLVER_LOGS_DIR = tmpDir;
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    originalFetch = global.fetch;
    originalProcessExit = process.exit;
  });

  after(() => {
    global.fetch = originalFetch;
    process.exit = originalProcessExit;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalLogsDir === undefined) delete process.env.EVOLVER_LOGS_DIR;
    else process.env.EVOLVER_LOGS_DIR = originalLogsDir;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
    if (originalAntiAbuseTelemetry === undefined) delete process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
    else process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = originalAntiAbuseTelemetry;
    if (originalAntiAbuseSalt === undefined) delete process.env.EVOLVER_ANTI_ABUSE_SALT;
    else process.env.EVOLVER_ANTI_ABUSE_SALT = originalAntiAbuseSalt;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  beforeEach(() => {
    executeForceUpdateCalls = [];
    executeForceUpdateReturn = false;
    executeForceUpdateReturns = [];
    exitCalls = [];
    process.exit = function (code) { exitCalls.push(code); };
    // Default: cooldown 0 so each test starts fresh. The cooldown test
    // overrides to a large value inside its own body.
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '0';
    delete process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
    delete process.env.EVOLVER_ANTI_ABUSE_SALT;
    _resetForceUpdateStateForTesting();
  });

  it('calls executeForceUpdate exactly once when Hub returns force_update', async () => {
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        status: 'ok',
        force_update: {
          required_version: '>=1.74.1',
          reason: 'atp_auto_deliver',
          deadline_ms: 90000,
        },
      }),
      text: async () => '',
    });

    var result = await sendHeartbeat();
    assert.ok(result.ok, 'heartbeat should succeed');
    // Give the microtask a tick to run.
    await new Promise(resolve => setImmediate(resolve));

    assert.equal(executeForceUpdateCalls.length, 1, 'executeForceUpdate called exactly once');
    assert.equal(executeForceUpdateCalls[0].required_version, '>=1.74.1');
    assert.deepEqual(exitCalls, [], 'no process.exit when upgrade fails');
  });

  it('calls process.exit(78) when executeForceUpdate returns true', async () => {
    executeForceUpdateReturn = true;
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'test' },
      }),
      text: async () => '',
    });

    var result = await sendHeartbeat();
    assert.ok(result.ok);
    await new Promise(resolve => setImmediate(resolve));

    assert.equal(exitCalls.length, 1);
    assert.equal(exitCalls[0], 78);
  });

  it('does nothing when heartbeat response has no force_update', async () => {
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });

    var result = await sendHeartbeat();
    assert.ok(result.ok);
    await new Promise(resolve => setImmediate(resolve));

    assert.equal(executeForceUpdateCalls.length, 0);
  });

  it('respects cooldown: does not call executeForceUpdate twice back-to-back', async () => {
    // Large cooldown for this test to verify the second call is blocked.
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '3600000';
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        status: 'ok',
        force_update: { required_version: '>=1.74.1', reason: 'test' },
      }),
      text: async () => '',
    });

    await sendHeartbeat();
    await new Promise(resolve => setImmediate(resolve));
    // Second heartbeat comes in before cooldown expires.
    await sendHeartbeat();
    await new Promise(resolve => setImmediate(resolve));

    // In beforeEach we reset counters before each `it`, so within this single
    // test we should see at most 1 call (the second one is blocked by
    // in-flight lock / recent-attempt cooldown).
    assert.equal(executeForceUpdateCalls.length, 1,
      'second back-to-back heartbeat must not re-trigger executeForceUpdate');
  });

  it('does not let a no-op force_update consume cooldown for a later higher version', async () => {
    process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS = '3600000';
    executeForceUpdateReturns = [SPY_NOOP, false];
    var heartbeatCount = 0;
    global.fetch = async () => {
      heartbeatCount++;
      return {
        ok: true,
        status: 200,
        json: async () => ({
          status: 'ok',
          force_update: {
            required_version: heartbeatCount === 1 ? '>=1.88.3' : '>=1.89.1',
            reason: 'test',
          },
        }),
        text: async () => '',
      };
    };

    await sendHeartbeat();
    await new Promise(resolve => setImmediate(resolve));
    await sendHeartbeat();
    await new Promise(resolve => setImmediate(resolve));

    assert.equal(executeForceUpdateCalls.length, 2,
      'a no-op stale floor must not delay a newer force_update directive');
    assert.equal(executeForceUpdateCalls[0].required_version, '>=1.88.3');
    assert.equal(executeForceUpdateCalls[1].required_version, '>=1.89.1');
  });

  it('attaches default anti_abuse heartbeat telemetry without leaking salt', async () => {
    process.env.EVOLVER_ANTI_ABUSE_SALT = 'integration-test-salt';
    var capturedBody = null;
    global.fetch = async (url, opts) => {
      capturedBody = JSON.parse(opts.body);
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    var result = await sendHeartbeat();
    assert.ok(result.ok);
    assert.equal(capturedBody.meta.anti_abuse.schema_version, 'anti_abuse.v1');
    assert.equal(capturedBody.meta.anti_abuse.source, 'evolver-client');
    assert.equal(capturedBody.meta.anti_abuse.source_confidence.network_source, 'server_observed_required');
    assert.equal(JSON.stringify(capturedBody).includes('integration-test-salt'), false);
  });

  it('does not attach anti_abuse heartbeat telemetry when disabled', async () => {
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = 'off';
    var capturedBody = null;
    global.fetch = async (url, opts) => {
      capturedBody = JSON.parse(opts.body);
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    var result = await sendHeartbeat();
    assert.ok(result.ok);
    assert.equal(capturedBody.meta && capturedBody.meta.anti_abuse, undefined);
  });
});
