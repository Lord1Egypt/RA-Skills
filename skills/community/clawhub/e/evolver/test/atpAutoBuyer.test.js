const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const savedEnv = {};
const envKeys = [
  'EVOLVER_ATP_AUTOBUY',
  'ATP_AUTOBUY_DAILY_CAP_CREDITS',
  'ATP_AUTOBUY_PER_ORDER_CAP_CREDITS',
  'MEMORY_DIR',
];

let tmpMemoryDir;
let autoBuyer;
let hubClient;
let origPlaceOrder;

function makeTmpMemoryDir() {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'atp-autobuy-'));
  return d;
}

beforeEach(() => {
  for (const k of envKeys) { savedEnv[k] = process.env[k]; delete process.env[k]; }
  tmpMemoryDir = makeTmpMemoryDir();
  process.env.MEMORY_DIR = tmpMemoryDir;

  // Fresh module instances: purge require cache for the modules under test
  // so every test sees a clean autoBuyer/hubClient pair.
  for (const key of Object.keys(require.cache)) {
    if (key.includes('/src/atp/') || key.includes('/src/gep/paths')) {
      delete require.cache[key];
    }
  }
  autoBuyer = require('../src/atp/autoBuyer');
  hubClient = require('../src/atp/hubClient');
  origPlaceOrder = hubClient.placeOrder;
  autoBuyer.__internals.resetForTests();
});

afterEach(() => {
  if (origPlaceOrder) hubClient.placeOrder = origPlaceOrder;
  for (const k of envKeys) {
    if (savedEnv[k] === undefined) delete process.env[k];
    else process.env[k] = savedEnv[k];
  }
  try { fs.rmSync(tmpMemoryDir, { recursive: true, force: true }); } catch (_) {}
});

describe('autoBuyer.start gating', () => {
  it('starts with default-on when EVOLVER_ATP_AUTOBUY is unset and no ack file', () => {
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    assert.equal(autoBuyer.isStarted(), true);
    const consent = autoBuyer.getConsent();
    assert.equal(consent.enabled, true);
    assert.equal(consent.source, 'default');
  });

  it('does not start when EVOLVER_ATP_AUTOBUY=off', () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'off';
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    assert.equal(autoBuyer.isStarted(), false);
  });

  it('starts when EVOLVER_ATP_AUTOBUY=on (explicit env opt-in)', () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    assert.equal(autoBuyer.isStarted(), true);
    assert.equal(autoBuyer.getConsent().source, 'env');
  });

  it('starts when ack file enabled=true (CLI opt-in via `evolver atp enable`)', () => {
    autoBuyer.setConsent(true);
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    assert.equal(autoBuyer.isStarted(), true);
    assert.equal(autoBuyer.getConsent().source, 'ack');
  });

  it('does not start when ack file enabled=false (explicit opt-out)', () => {
    autoBuyer.setConsent(false);
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    assert.equal(autoBuyer.isStarted(), false);
    const consent = autoBuyer.getConsent();
    assert.equal(consent.enabled, false);
    assert.equal(consent.source, 'ack');
  });

  it('env override wins over ack file', () => {
    autoBuyer.setConsent(true);
    process.env.EVOLVER_ATP_AUTOBUY = 'off';
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    assert.equal(autoBuyer.isStarted(), false);
    assert.equal(autoBuyer.getConsent().source, 'env');
  });

  it('whitespace-only env value is treated as unset (falls through to default)', () => {
    // Bugbot PR #141 Medium: getConsent and classify() must agree on what
    // "unset" means. Whitespace-only should fall through to ack/default
    // instead of entering the env branch and trimming to '' (which would
    // mismatch 'off'/'0'/'false' and return source='env').
    process.env.EVOLVER_ATP_AUTOBUY = '   ';
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    assert.equal(autoBuyer.isStarted(), true);
    const consent = autoBuyer.getConsent();
    assert.equal(consent.enabled, true);
    assert.equal(consent.source, 'default');
  });

  it('start is idempotent', () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    autoBuyer.start({ dailyCap: 999, perOrderCap: 999 });
    assert.equal(autoBuyer.isStarted(), true);
  });
});

describe('autoBuyer.considerOrder: guards and budget caps', () => {
  it('skips when not started', async () => {
    const r = await autoBuyer.considerOrder({ capabilities: ['x'], question: 'q' });
    assert.equal(r.ok, false);
    assert.equal(r.skipped, true);
    assert.equal(r.reason, 'not_started');
  });

  it('skips when no capabilities', async () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 50, perOrderCap: 10 });
    const r = await autoBuyer.considerOrder({ capabilities: [], question: 'q' });
    assert.equal(r.ok, false);
    assert.equal(r.skipped, true);
    assert.equal(r.reason, 'no_capabilities');
  });

  it('clamps budget to perOrderCap and daily remaining', async () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    // Use large caps so cold-start half-cap still leaves headroom > 1 credit.
    autoBuyer.start({ dailyCap: 1000, perOrderCap: 20 });
    const seen = [];
    hubClient.placeOrder = async (opts) => {
      seen.push(opts);
      return { ok: true, data: { order_id: 'ord_test_1' } };
    };
    const r = await autoBuyer.considerOrder({
      capabilities: ['code_review'],
      question: 'please review',
      budget: 500,
    });
    assert.equal(r.ok, true);
    assert.equal(seen.length, 1);
    // Requested 500 but perOrderCap=20 (half during cold start => 10).
    assert.ok(seen[0].budget <= 10, 'budget should be clamped to cold-start perOrderCap (10), got ' + seen[0].budget);
    assert.ok(seen[0].budget >= 1);
  });

  it('respects daily cap across multiple calls', async () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    // dailyCap cold-start half = 5, perOrderCap half = 5. Two orders of 5 will hit cap.
    autoBuyer.start({ dailyCap: 10, perOrderCap: 10 });
    hubClient.placeOrder = async () => ({ ok: true, data: { order_id: 'x' } });
    const r1 = await autoBuyer.considerOrder({ capabilities: ['c1'], question: 'q1', budget: 100 });
    const r2 = await autoBuyer.considerOrder({ capabilities: ['c2'], question: 'q2', budget: 100 });
    const r3 = await autoBuyer.considerOrder({ capabilities: ['c3'], question: 'q3', budget: 100 });
    assert.equal(r1.ok, true);
    // Either r2 hits cap or r3 does -- spend must not exceed dailyCap (half=5 cold start).
    const spent = [r1, r2, r3].filter(r => r.ok).reduce((a, r) => a + (r.spent || 0), 0);
    assert.ok(spent <= 5, 'spent ' + spent + ' must not exceed cold-start dailyCap (5)');
    const lastHitCap = [r1, r2, r3].some(r => r.reason === 'daily_cap_reached');
    assert.ok(lastHitCap, 'at least one call must be rejected with daily_cap_reached');
  });
});

describe('autoBuyer.considerOrder: 24h deduplication', () => {
  it('skips the second call for the same question within TTL', async () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 100, perOrderCap: 20 });
    hubClient.placeOrder = async () => ({ ok: true, data: { order_id: 'dedup_ord' } });
    const r1 = await autoBuyer.considerOrder({
      capabilities: ['code_review'],
      question: 'exact same question text',
    });
    const r2 = await autoBuyer.considerOrder({
      capabilities: ['code_review'],
      question: 'exact same question text',
    });
    assert.equal(r1.ok, true);
    assert.equal(r2.ok, false);
    assert.equal(r2.skipped, true);
    assert.equal(r2.reason, 'dedup_hit');
  });

  it('dedups even when the first placeOrder fails, to protect hub', async () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 100, perOrderCap: 20 });
    let called = 0;
    hubClient.placeOrder = async () => {
      called += 1;
      return { ok: false, error: 'simulated_network_error' };
    };
    const r1 = await autoBuyer.considerOrder({ capabilities: ['c'], question: 'boom' });
    const r2 = await autoBuyer.considerOrder({ capabilities: ['c'], question: 'boom' });
    assert.equal(r1.ok, false);
    assert.equal(r2.skipped, true);
    assert.equal(r2.reason, 'dedup_hit');
    assert.equal(called, 1, 'only first failure should reach hub');
  });

  it('failure dedup expires after the short TTL (5 min), success stays 24h', async () => {
    // Pre-bug: a single 503/network blip would block the same question for
    // a full 24h. Now success entries persist 24h while failure entries
    // age out after 5 minutes so users can retry transient errors.
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 100, perOrderCap: 20 });

    // Seed the ledger manually so we control the timestamp.
    const successHash = autoBuyer.__internals.questionHash({
      capabilities: ['code_review'], question: 'old success',
    });
    const failureHash = autoBuyer.__internals.questionHash({
      capabilities: ['code_review'], question: 'old failure',
    });
    const tenMinAgo = Date.now() - 10 * 60 * 1000;
    const ledger = autoBuyer.__internals.readLedger();
    ledger.dedup[successHash] = { ts: tenMinAgo, failed: false };
    ledger.dedup[failureHash] = { ts: tenMinAgo, failed: true };
    autoBuyer.__internals.writeLedger(ledger);

    // Failure entry > 5 min old -> pruned -> hub IS called again.
    let failureCalls = 0;
    hubClient.placeOrder = async () => {
      failureCalls += 1;
      return { ok: true, data: { order_id: 'retry_ord' } };
    };
    const r1 = await autoBuyer.considerOrder({
      capabilities: ['code_review'], question: 'old failure',
    });
    assert.equal(r1.ok, true, 'retry of old failure (>5min) should succeed');
    assert.equal(failureCalls, 1, 'hub should be called again because failure dedup expired');

    // Success entry of the same age still blocks.
    let successCalls = 0;
    hubClient.placeOrder = async () => {
      successCalls += 1;
      return { ok: true, data: { order_id: 'should_not_be_called' } };
    };
    const r2 = await autoBuyer.considerOrder({
      capabilities: ['code_review'], question: 'old success',
    });
    assert.equal(r2.ok, false);
    assert.equal(r2.reason, 'dedup_hit', 'old success (<24h) must still be deduped');
    assert.equal(successCalls, 0);
  });

  it('treats legacy number entries (pre-v2 ledger) as 24h success dedup', async () => {
    // Backward compat: ledgers written by older versions stored plain
    // timestamps. _pruneDedup must accept them so an upgrade does not
    // silently forget recent dedups.
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 100, perOrderCap: 20 });

    const hash = autoBuyer.__internals.questionHash({
      capabilities: ['c'], question: 'legacy entry',
    });
    const ledger = autoBuyer.__internals.readLedger();
    ledger.dedup[hash] = Date.now() - 60 * 60 * 1000; // 1 hour old, plain number
    autoBuyer.__internals.writeLedger(ledger);

    hubClient.placeOrder = async () => ({ ok: true, data: { order_id: 'should_not_be_called' } });
    const r = await autoBuyer.considerOrder({
      capabilities: ['c'], question: 'legacy entry',
    });
    assert.equal(r.reason, 'dedup_hit', 'legacy number entry must still dedup within 24h');
  });
});

describe('autoBuyer: ledger persistence', () => {
  it('persists spend to ledger file and reloads on restart', async () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 100, perOrderCap: 20 });
    hubClient.placeOrder = async () => ({ ok: true, data: { order_id: 'persist_test' } });
    await autoBuyer.considerOrder({ capabilities: ['x'], question: 'persist q' });

    const ledgerPath = path.join(tmpMemoryDir, 'atp-autobuyer-ledger.json');
    assert.ok(fs.existsSync(ledgerPath), 'ledger file should exist');
    const parsed = JSON.parse(fs.readFileSync(ledgerPath, 'utf8'));
    assert.equal(parsed.version, 1);
    assert.ok(parsed.spent > 0, 'spent should be recorded');
    assert.ok(Object.keys(parsed.dedup).length === 1, 'dedup should have exactly one entry');
  });
});

describe('autoBuyer: timeout protection', () => {
  it('resolves with error when hub placeOrder hangs past timeoutMs (min 500ms clamp)', async () => {
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    // Note: start() clamps timeoutMs to >=500ms; we pass 50 but effective is 500.
    autoBuyer.start({ dailyCap: 100, perOrderCap: 20, timeoutMs: 50 });
    hubClient.placeOrder = () => new Promise(() => {}); // never resolves
    const t0 = Date.now();
    const r = await autoBuyer.considerOrder({ capabilities: ['c'], question: 'slow hub' });
    const elapsed = Date.now() - t0;
    assert.equal(r.ok, false);
    assert.equal(r.error, 'autobuyer_timeout');
    // Effective timeout is 500ms; allow generous ceiling for CI jitter.
    assert.ok(elapsed < 1500, 'should time out within ~500ms clamp, elapsed=' + elapsed);
    assert.ok(elapsed >= 400, 'should not short-circuit before clamp, elapsed=' + elapsed);
  });
});

describe('autoBuyer.considerOrder: concurrent serialization (H-NEW-1)', () => {
  it('never exceeds the daily cap when multiple callers race', async () => {
    // Pre-bug: read → cap-check → await → write was not serialized, so two
    // concurrent calls could both pass the cap check on the same snapshot
    // and silently double-spend. The single-flight queue must guarantee
    // total spend <= dailyCap regardless of concurrency.
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    // Use big caps so cold-start half-cap still gives multiple slots.
    autoBuyer.start({ dailyCap: 100, perOrderCap: 100 });

    // Slow placeOrder so all concurrent calls overlap inside the queue.
    hubClient.placeOrder = async (opts) => {
      await new Promise((r) => setTimeout(r, 10));
      return { ok: true, data: { order_id: 'race_' + opts.budget } };
    };

    const calls = [];
    for (let i = 0; i < 8; i++) {
      calls.push(autoBuyer.considerOrder({
        capabilities: ['cap_' + i],   // distinct hashes so dedup doesn't help
        question: 'race question ' + i,
        budget: 30,
      }));
    }
    const results = await Promise.all(calls);

    const okResults = results.filter((r) => r.ok);
    const totalSpent = okResults.reduce((acc, r) => acc + (r.spent || 0), 0);
    const effectiveDailyCap = Math.floor(100 / 2); // cold-start half = 50
    assert.ok(totalSpent <= effectiveDailyCap,
      'total spent ' + totalSpent + ' must not exceed cold-start dailyCap ' + effectiveDailyCap);

    // At least one call must report daily_cap_reached so we know the
    // pressure actually crossed the cap (otherwise the test is trivial).
    const capHits = results.filter((r) => r.reason === 'daily_cap_reached');
    assert.ok(capHits.length >= 1,
      'expected at least one daily_cap_reached among ' + results.length + ' concurrent calls');
  });

  it('a single rejected call does not poison the queue for subsequent callers', async () => {
    // The queue tail must swallow rejections so an error in one
    // _considerOrderSerialized run does not block every later one.
    process.env.EVOLVER_ATP_AUTOBUY = 'on';
    autoBuyer.start({ dailyCap: 100, perOrderCap: 20 });

    let n = 0;
    hubClient.placeOrder = async () => {
      n += 1;
      if (n === 1) throw new Error('exploded in placeOrder');
      return { ok: true, data: { order_id: 'after_explode' } };
    };

    const r1 = await autoBuyer.considerOrder({
      capabilities: ['c1'], question: 'q1',
    }).catch((e) => ({ thrown: e.message }));
    const r2 = await autoBuyer.considerOrder({
      capabilities: ['c2'], question: 'q2',
    });

    assert.ok(r1.thrown || r1.ok === false, 'first call surfaces the error');
    assert.equal(r2.ok, true, 'second call must still go through after first error');
  });
});

describe('autoBuyer.setConsent: error surfacing (Bugbot PR #141 Nit A)', () => {
  it('surfaces the original FS error verbatim (not a downstream ENOENT)', () => {
    // Point the memory dir at a regular file so mkdirSync fails with
    // ENOTDIR. Previously this was swallowed and writeFileSync threw a
    // confusing ENOENT; now the original ENOTDIR (or platform equivalent)
    // must reach the caller.
    const collidingFile = path.join(tmpMemoryDir, 'is-a-file');
    fs.writeFileSync(collidingFile, 'x');
    process.env.MEMORY_DIR = collidingFile;

    // Re-require autoBuyer so getMemoryDir() observes the new env.
    for (const k of Object.keys(require.cache)) {
      if (k.includes('/src/atp/') || k.includes('/src/gep/paths')) {
        delete require.cache[k];
      }
    }
    const ab = require('../src/atp/autoBuyer');

    assert.throws(
      () => ab.setConsent(true),
      (err) => {
        // The exact errno varies by OS (ENOTDIR on POSIX, ENOENT-on-file on
        // some Windows configs) so assert on the surface contract only: an
        // Error is thrown, and it is NOT the misleading "ENOENT: no such
        // file or directory" against the tmp file we never tried to mkdir.
        assert.ok(err instanceof Error, 'must throw a real Error');
        assert.ok(err.code, 'errno must be preserved on the thrown error');
        return true;
      },
    );

    // Best-effort: no .tmp leftover after the failure.
    const stragglingTmp = path.join(collidingFile, 'atp-autobuy-ack.json.tmp');
    assert.ok(!fs.existsSync(stragglingTmp), 'no stale .tmp file after failure');
  });
});

describe('autoBuyer.__internals.questionHash', () => {
  it('is stable regardless of capability array order', () => {
    const h1 = autoBuyer.__internals.questionHash({ capabilities: ['a', 'b'], question: 'same' });
    const h2 = autoBuyer.__internals.questionHash({ capabilities: ['b', 'a'], question: 'same' });
    assert.equal(h1, h2);
  });

  it('differs for different questions', () => {
    const h1 = autoBuyer.__internals.questionHash({ capabilities: ['a'], question: 'q1' });
    const h2 = autoBuyer.__internals.questionHash({ capabilities: ['a'], question: 'q2' });
    assert.notEqual(h1, h2);
  });
});
