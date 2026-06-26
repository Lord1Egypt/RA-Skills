// test/validatorDaemon.test.js
// Tests the independent validator daemon: starts/stops cleanly, honors
// isValidatorEnabled at each tick, and processes tasks via runValidatorCycle.
'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

function freshRequire(id) {
  delete require.cache[require.resolve(id)];
  return require(id);
}

function withFakeFetch(impl, fn) {
  const original = global.fetch;
  global.fetch = impl;
  return Promise.resolve()
    .then(fn)
    .finally(() => { global.fetch = original; });
}

function mkRes(body) {
  return {
    ok: true,
    status: 200,
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
}

describe('validator daemon', function () {
  const originalEnv = { ...process.env };
  const fs = require('fs');
  const path = require('path');
  const os = require('os');
  let tmpHome;

  beforeEach(() => {
    tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'validator-daemon-'));
    process.env.EVOLVER_HOME = tmpHome;
    process.env.A2A_HUB_URL = 'http://hub.local';
    process.env.HUB_NODE_SECRET = 'secret';
    process.env.A2A_NODE_ID = 'node_test_daemon';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    // Tight intervals so tests run fast
    process.env.EVOLVER_VALIDATOR_DAEMON_INTERVAL_MS = '20000';
    process.env.EVOLVER_VALIDATOR_DAEMON_FIRST_DELAY_MS = '0';
    try {
      const sb = freshRequire('../src/gep/validator/stakeBootstrap');
      if (sb && typeof sb._resetStateForTests === 'function') sb._resetStateForTests();
    } catch (_) {}
  });

  afterEach(() => {
    try {
      const v = require('../src/gep/validator');
      if (v.stopValidatorDaemon) v.stopValidatorDaemon();
    } catch (_) {}
    for (const k of Object.keys(process.env)) {
      if (!(k in originalEnv)) delete process.env[k];
    }
    Object.assign(process.env, originalEnv);
    if (tmpHome) {
      try { fs.rmSync(tmpHome, { recursive: true, force: true }); } catch (_) {}
    }
  });

  it('startValidatorDaemon is idempotent and reports stats', async function () {
    const v = freshRequire('../src/gep/validator');
    assert.equal(v.startValidatorDaemon(), true);
    assert.equal(v.startValidatorDaemon(), false, 'second call no-ops');
    const stats = v.getValidatorDaemonStats();
    assert.equal(stats.running, true);
    assert.ok(stats.intervalMs > 0);
    v.stopValidatorDaemon();
    assert.equal(v.getValidatorDaemonStats().running, false);
  });

  it('skips ticks when EVOLVER_VALIDATOR_ENABLED=0', async function () {
    process.env.EVOLVER_VALIDATOR_ENABLED = '0';
    let fetchCalls = 0;
    await withFakeFetch(async () => { fetchCalls += 1; return mkRes({ validation_tasks: [] }); }, async () => {
      const v = freshRequire('../src/gep/validator');
      v.startValidatorDaemon();
      await new Promise((r) => setTimeout(r, 50));
      v.stopValidatorDaemon();
    });
    assert.equal(fetchCalls, 0, 'no hub calls when disabled');
  });

  it('poke mid-tick does not fork the timer chain (generation guard)', async function () {
    // Regression for the P2 bug where pokeValidatorDaemon would arm a new
    // timer (T2) while a tick was awaiting the hub, and the in-flight
    // tick's finally would then overwrite _daemonTimer from T2 -> T3
    // without clearTimeout(T2). Both T2 and T3 would then fire, leaking
    // timers and doubling cadence on every poke.
    //
    // Strategy: pick an interval short enough that a leaked chain will
    // fire visibly within the test window. With the bug, after the
    // poked tick #2 completes, BOTH the leaked T3 (from tick #1's
    // finally) and the freshly-armed T3' (from tick #2's finally) will
    // fire within DAEMON_INTERVAL_MS, producing fetchCount >= 4 in a
    // window of (interval + slack). With the fix, only ONE timer chain
    // exists, so fetchCount === 3 (tick #1 + poked #2 + scheduled #3).
    process.env.EVOLVER_VALIDATOR_ENABLED = '1';
    process.env.EVOLVER_VALIDATOR_DAEMON_INTERVAL_MS = '15000';
    process.env.EVOLVER_VALIDATOR_DAEMON_FIRST_DELAY_MS = '0';

    let inflightResolve;
    const inflightStarted = new Promise((r) => { inflightResolve = r; });
    let releaseFetch;
    const fetchGate = new Promise((r) => { releaseFetch = r; });
    let fetchCount = 0;
    const fetchImpl = async (url) => {
      if (url.endsWith('/a2a/validator/stake')) return mkRes({ stake: { stake_amount: 100 } });
      if (url.endsWith('/a2a/fetch')) {
        fetchCount += 1;
        if (fetchCount === 1) {
          // Signal that tick #1 is now awaiting and block until we poke.
          inflightResolve();
          await fetchGate;
        }
        return mkRes({ validation_tasks: [] });
      }
      return mkRes({});
    };

    await withFakeFetch(fetchImpl, async () => {
      const v = freshRequire('../src/gep/validator');
      v.startValidatorDaemon();
      // Wait for tick #1 to enter the awaiting state.
      await inflightStarted;
      // Poke while tick #1 is in flight -- this arms T2 (0ms).
      assert.equal(v.pokeValidatorDaemon(), true);
      // Release tick #1; its finally must NOT arm an extra 15s timer.
      releaseFetch();
      // Wait long enough for: tick #1 to finish, T2 to fire (~0ms), tick
      // #2 to complete (~100ms), and the next 15s timer to fire ONCE
      // (~15s after tick #2). Use 15.5s to cover scheduling slack.
      await new Promise((r) => setTimeout(r, 15500));
      v.stopValidatorDaemon();
      // With the generation guard fix:
      //   fetchCount === 3 (tick #1 + tick #2 from poke + tick #3 from
      //   tick #2's re-arm).
      // Without the fix, tick #1's finally would arm a second 15s timer
      // *in addition to* T2, and after T2 runs and re-arms its own 15s
      // timer there would be TWO 15s timers firing in this window,
      // producing fetchCount === 4.
      assert.equal(
        fetchCount, 3,
        'expected 3 fetches (no forked chain), got ' + fetchCount
      );
    });
  });

  it('processes tasks on tick when enabled', async function () {
    process.env.EVOLVER_VALIDATOR_ENABLED = '1';
    let fetchCount = 0;
    let reportCount = 0;
    const fetchImpl = async (url) => {
      if (url.endsWith('/a2a/validator/stake')) return mkRes({ stake: { stake_amount: 100 } });
      if (url.endsWith('/a2a/fetch')) {
        fetchCount += 1;
        if (fetchCount === 1) {
          return mkRes({
            validation_tasks: [
              {
                task_id: 'vt_daemon_1',
                nonce: 'n1',
                validation_commands: ['echo daemon-ok'],
              },
            ],
          });
        }
        return mkRes({ validation_tasks: [] });
      }
      if (url.endsWith('/a2a/report')) {
        reportCount += 1;
        return mkRes({ status: 'accepted', payload: {} });
      }
      return mkRes({});
    };
    await withFakeFetch(fetchImpl, async () => {
      const v = freshRequire('../src/gep/validator');
      v.startValidatorDaemon();
      // Wait for first tick + sandbox exec; sandbox is real but `echo` is fast.
      await new Promise((r) => setTimeout(r, 1500));
      v.stopValidatorDaemon();
      const stats = v.getValidatorDaemonStats();
      assert.ok(stats.ticks >= 1, 'at least one tick happened: ' + stats.ticks);
    });
    assert.ok(fetchCount >= 1, 'daemon fetched tasks');
    assert.ok(reportCount >= 1, 'daemon submitted at least one report');
  });
});
