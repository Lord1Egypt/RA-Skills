// test/stakeBootstrap.test.js
// Unit tests for src/gep/validator/stakeBootstrap.js: retry state machine,
// failure classification, backoff behavior, and disk persistence across
// process boundaries (v1.69.11+). Mocks global.fetch and the a2aProtocol
// node-id/hub-url resolvers.
'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const Module = require('module');

function freshRequire(id) {
  delete require.cache[require.resolve(id)];
  return require(id);
}

function installA2aProtocolStub(nodeId, hubUrl) {
  const target = require.resolve('../src/gep/a2aProtocol');
  const sbPath = require.resolve('../src/gep/validator/stakeBootstrap');
  delete require.cache[target];
  delete require.cache[sbPath];
  const origLoad = Module._load;
  Module._load = function (request, parent, isMain) {
    let resolved = null;
    try { resolved = Module._resolveFilename(request, parent, isMain); } catch (_) {}
    if (resolved === target) {
      return {
        buildHubHeaders: () => ({ 'content-type': 'application/json' }),
        getHubUrl: () => hubUrl,
        getNodeId: () => nodeId,
      };
    }
    return origLoad.apply(this, arguments);
  };
  return () => {
    Module._load = origLoad;
    delete require.cache[target];
    delete require.cache[sbPath];
  };
}

describe('stakeBootstrap retry state machine', function () {
  let restoreFetch;
  let restoreA2a;
  let tmpHome;
  let prevHome;

  let prevInsecure;
  beforeEach(() => {
    tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-stake-test-'));
    prevHome = process.env.EVOLVER_HOME;
    prevInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.EVOLVER_HOME = tmpHome;
    // stakeBootstrap routes via hubFetch; tests stub global.fetch and use
    // a fake https hubUrl. Insecure mode makes hubFetch route through
    // global.fetch so the stubs apply.
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    restoreA2a = installA2aProtocolStub('node-test-stake', 'https://hub.example.com');
  });

  afterEach(() => {
    if (restoreA2a) restoreA2a();
    if (restoreFetch) restoreFetch();
    restoreFetch = null;
    restoreA2a = null;
    if (prevHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = prevHome;
    if (prevInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = prevInsecure;
    try { fs.rmSync(tmpHome, { recursive: true, force: true }); } catch (_) {}
  });

  function stubFetch(responder) {
    const original = global.fetch;
    global.fetch = async (url, init) => responder(url, init);
    return () => { global.fetch = original; };
  }

  it('success resets backoff and schedules next attempt ~24h away', async () => {
    const sb = freshRequire('../src/gep/validator/stakeBootstrap');
    sb._resetStateForTests();
    restoreFetch = stubFetch(async () => ({
      ok: true,
      status: 200,
      text: async () => JSON.stringify({ status: 'ok', stake: { stake_amount: 100, status: 'active', node_id: 'node-test-stake' } }),
    }));

    const result = await sb.ensureValidatorStake({});
    assert.equal(result.ok, true);
    const state = sb._getStateForTests();
    assert.equal(state.transientFailures, 0);
    assert.equal(state.fundsFailures, 0);
    assert.ok(state.nextAttemptAt > Date.now() + (23 * 60 * 60 * 1000), 'next attempt should be ~24h from now');
  });

  it('network error increments transient failures and schedules first backoff (5min)', async () => {
    const sb = freshRequire('../src/gep/validator/stakeBootstrap');
    sb._resetStateForTests();
    restoreFetch = stubFetch(async () => { throw new Error('network down'); });

    const r = await sb.ensureValidatorStake({});
    assert.equal(r.ok, false);
    const state = sb._getStateForTests();
    assert.equal(state.transientFailures, 1);
    const delay = state.nextAttemptAt - Date.now();
    assert.ok(delay >= 4 * 60 * 1000 && delay <= 6 * 60 * 1000, `first transient delay should be ~5min, got ${delay}`);
  });

  it('402 insufficient_credits classified as funds and uses funds backoff (~60min first)', async () => {
    const sb = freshRequire('../src/gep/validator/stakeBootstrap');
    sb._resetStateForTests();
    restoreFetch = stubFetch(async () => ({
      ok: false,
      status: 402,
      text: async () => JSON.stringify({ error: 'insufficient_credits: need 100, have 42' }),
    }));

    const r = await sb.ensureValidatorStake({});
    assert.equal(r.ok, false);
    assert.equal(r.kind, 'funds');
    const state = sb._getStateForTests();
    assert.equal(state.fundsFailures, 1);
    assert.equal(state.transientFailures, 0);
    const delay = state.nextAttemptAt - Date.now();
    assert.ok(delay >= 59 * 60 * 1000 && delay <= 61 * 60 * 1000, `first funds delay should be ~60min, got ${delay}`);
  });

  it('400 stake_amount_must_be_at_least_100 classified as permanent (disabled_until_restart)', async () => {
    const sb = freshRequire('../src/gep/validator/stakeBootstrap');
    sb._resetStateForTests();
    restoreFetch = stubFetch(async () => ({
      ok: false,
      status: 400,
      text: async () => JSON.stringify({ error: 'stake_amount_must_be_at_least_100' }),
    }));

    const r1 = await sb.ensureValidatorStake({});
    assert.equal(r1.ok, false);
    assert.equal(r1.kind, 'permanent');

    const r2 = await sb.ensureValidatorStake({});
    assert.equal(r2.ok, false);
    assert.equal(r2.skipped, 'disabled_until_restart');
  });

  it('backoff skip short-circuits until nextAttemptAt, then allows retry after force', async () => {
    const sb = freshRequire('../src/gep/validator/stakeBootstrap');
    sb._resetStateForTests();
    let calls = 0;
    restoreFetch = stubFetch(async () => {
      calls += 1;
      throw new Error('boom');
    });

    await sb.ensureValidatorStake({});
    const skipped = await sb.ensureValidatorStake({});
    assert.equal(skipped.skipped, 'backoff');
    assert.equal(calls, 1);

    const forced = await sb.ensureValidatorStake({ force: true });
    assert.equal(forced.ok, false);
    assert.equal(calls, 2);
    const state = sb._getStateForTests();
    assert.equal(state.transientFailures, 2);
    const delay = state.nextAttemptAt - Date.now();
    assert.ok(delay >= 14 * 60 * 1000 && delay <= 16 * 60 * 1000, `second transient delay should be ~15min, got ${delay}`);
  });

  it('exports DEFAULT_STAKE_AMOUNT = 100', function () {
    const sb = freshRequire('../src/gep/validator/stakeBootstrap');
    assert.equal(sb.DEFAULT_STAKE_AMOUNT, 100);
  });

  // --- Disk persistence (v1.69.11+) ---

  it('success persists nextAttemptAt to disk under EVOLVER_HOME', async () => {
    const sb = freshRequire('../src/gep/validator/stakeBootstrap');
    sb._resetStateForTests();
    restoreFetch = stubFetch(async () => ({
      ok: true,
      status: 200,
      text: async () => JSON.stringify({ status: 'ok', stake: { stake_amount: 100, status: 'active', node_id: 'node-test-stake' } }),
    }));

    await sb.ensureValidatorStake({});

    assert.ok(fs.existsSync(sb.STATE_FILE), 'state file should exist after success');
    const raw = JSON.parse(fs.readFileSync(sb.STATE_FILE, 'utf8'));
    assert.ok(raw.nextAttemptAt > Date.now() + 23 * 60 * 60 * 1000, 'persisted nextAttemptAt should be ~24h out');
    assert.equal(raw.transientFailures, 0);
    assert.equal(raw.fundsFailures, 0);
    // disabledUntilRestart intentionally not persisted
    assert.equal(raw.disabledUntilRestart, undefined);
  });

  it('persisted backoff survives a simulated process restart (module re-require)', async () => {
    // First "process": record a transient failure and persist its backoff.
    const sb1 = freshRequire('../src/gep/validator/stakeBootstrap');
    sb1._resetStateForTests();
    restoreFetch = stubFetch(async () => { throw new Error('network down'); });
    await sb1.ensureValidatorStake({});
    const persistedNext = sb1._getStateForTests().nextAttemptAt;
    assert.ok(persistedNext > Date.now(), 'pre-restart state should have a future nextAttemptAt');
    restoreFetch();
    restoreFetch = null;

    // Second "process": re-require the module. State file is still on disk.
    let networkCalls = 0;
    restoreFetch = stubFetch(async () => {
      networkCalls += 1;
      throw new Error('still down');
    });
    const sb2 = freshRequire('../src/gep/validator/stakeBootstrap');
    // Skip should come from disk, NOT fetch the hub again.
    const result = await sb2.ensureValidatorStake({});
    assert.equal(result.skipped, 'backoff');
    assert.equal(networkCalls, 0, 'must not hit hub while within persisted backoff window');
    const state = sb2._getStateForTests();
    assert.equal(state.transientFailures, 1, 'failure counter should be loaded from disk');
    // nextAttemptAt round-trip should be within 1ms of original.
    assert.ok(Math.abs(state.nextAttemptAt - persistedNext) < 2, `nextAttemptAt should round-trip, got ${state.nextAttemptAt} vs ${persistedNext}`);
  });

  it('disabledUntilRestart is NOT persisted -- restart lets retry happen once', async () => {
    // First process: trigger permanent failure.
    const sb1 = freshRequire('../src/gep/validator/stakeBootstrap');
    sb1._resetStateForTests();
    restoreFetch = stubFetch(async () => ({
      ok: false,
      status: 400,
      text: async () => JSON.stringify({ error: 'stake_amount_must_be_at_least_100' }),
    }));
    const r1 = await sb1.ensureValidatorStake({});
    assert.equal(r1.kind, 'permanent');
    const r2 = await sb1.ensureValidatorStake({});
    assert.equal(r2.skipped, 'disabled_until_restart');

    // Simulate restart: re-require with successful fetch.
    restoreFetch();
    let hubHits = 0;
    restoreFetch = stubFetch(async () => {
      hubHits += 1;
      return {
        ok: true,
        status: 200,
        text: async () => JSON.stringify({ status: 'ok', stake: { stake_amount: 100, status: 'active' } }),
      };
    });
    const sb2 = freshRequire('../src/gep/validator/stakeBootstrap');
    const r3 = await sb2.ensureValidatorStake({});
    assert.equal(r3.ok, true, 'after restart, permanent flag must clear');
    assert.equal(hubHits, 1, 'restart should allow exactly one fresh attempt');
  });

  it('load clamps absurdly-far nextAttemptAt (clock-skew or corrupt file)', async () => {
    const sb1 = freshRequire('../src/gep/validator/stakeBootstrap');
    sb1._resetStateForTests();
    // Write a poisoned state file: nextAttemptAt 10 years in the future.
    fs.mkdirSync(path.dirname(sb1.STATE_FILE), { recursive: true });
    fs.writeFileSync(sb1.STATE_FILE, JSON.stringify({
      nextAttemptAt: Date.now() + 10 * 365 * 24 * 60 * 60 * 1000,
      transientFailures: 99,
      fundsFailures: 0,
      lastSuccessAt: 0,
    }));

    restoreFetch = stubFetch(async () => ({
      ok: true,
      status: 200,
      text: async () => JSON.stringify({ status: 'ok' }),
    }));

    const sb2 = freshRequire('../src/gep/validator/stakeBootstrap');
    // Load; nextAttemptAt should be clamped to <= now + 24h.
    sb2._loadStateFromDisk();
    const loaded = sb2._getStateForTests();
    assert.ok(loaded.nextAttemptAt <= Date.now() + 24 * 60 * 60 * 1000 + 1000,
      `nextAttemptAt should be clamped to <= now+24h, got ${loaded.nextAttemptAt - Date.now()}ms out`);
  });

  it('gracefully tolerates corrupt state file (falls back to defaults)', async () => {
    const sb1 = freshRequire('../src/gep/validator/stakeBootstrap');
    sb1._resetStateForTests();
    fs.mkdirSync(path.dirname(sb1.STATE_FILE), { recursive: true });
    fs.writeFileSync(sb1.STATE_FILE, 'not json at all {{{');

    restoreFetch = stubFetch(async () => ({
      ok: true,
      status: 200,
      text: async () => JSON.stringify({ status: 'ok' }),
    }));

    const sb2 = freshRequire('../src/gep/validator/stakeBootstrap');
    const r = await sb2.ensureValidatorStake({});
    assert.equal(r.ok, true, 'corrupt file must not prevent stake attempt');
  });
});
