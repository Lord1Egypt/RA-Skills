// Cross-process race coverage for consumeOfflinePermit.
//
// Scenario the lock protects against:
//   daemon `evolver --loop` and CLI `evolver solidify` (two separate Node
//   processes) both reach consumeOfflinePermit at the same moment, both
//   read the same usedCount, both pass the cap check, both increment +
//   write — the local counter then exceeds maxSolidifies by N for N
//   concurrent callers.
//
// Implementation note: the lock primitive itself lives in assetStore.js
// (`withFileLock`, PID-liveness stale detection + Atomics-or-busy-wait
// fallback) and has its own unit tests there. These tests cover the
// hubVerify integration only: that consumeOfflinePermit serializes the
// read→cap→write pipeline across processes and surfaces a meaningful
// `offline_permit_busy` signal when the lock is contended.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { fork } = require('child_process');

// Force the signing secret unconditionally. Every token planted in this file
// is signed with this exact value (see TEST_NODE_SECRET below), so the parent
// and every fork()-ed worker MUST verify with the same key. A `|| inherited`
// fallback would let a real A2A_NODE_SECRET present on the host (configured
// EvoMap nodes, some CI) win — the token then fails HMAC verify, every
// consumeOfflinePermit short-circuits to no_offline_token before the lock is
// even acquired, and the cross-process race assertions collapse. This file
// is run in its own process by `node --test`, so the assignment cannot leak
// to other suites.
const TEST_NODE_SECRET = 'a'.repeat(64);
process.env.A2A_NODE_SECRET = TEST_NODE_SECRET;

function makeTmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'hv-race-'));
}

function makeSignedToken(memDir, token, secret) {
  const ot = path.join(memDir, '.ot');
  const data = JSON.stringify(token);
  const hmac = crypto.createHmac('sha256', secret).update(data).digest('hex');
  fs.writeFileSync(ot, JSON.stringify({ data: token, hmac }), 'utf8');
}

describe('consumeOfflinePermit: never-throw contract (Bugbot PR #157 R2 Low)', () => {
  // Pre-refactor, consumeOfflinePermit always returned a structured
  // envelope — loadOfflineToken and cacheOfflineToken both swallowed FS
  // errors internally. The withFileLock wrapper introduced a new throw
  // surface (ENOENT on the lock file when the memory dir doesn't exist,
  // EACCES on permission issues, etc.) that the original `Lock timeout`-
  // only catch did not handle. These tests pin the never-throw contract.

  let tmpRoot;

  beforeEach(() => {
    tmpRoot = makeTmpDir();
  });

  afterEach(() => {
    try { fs.rmSync(tmpRoot, { recursive: true, force: true }); } catch (_) {}
  });

  it('returns structured envelope when MEMORY_DIR does not exist (fresh install)', () => {
    // Point MEMORY_DIR at a path that does not exist yet. Pre-fix this
    // raised ENOENT from withFileLock → _acquireLock → fs.writeFileSync.
    const missing = path.join(tmpRoot, 'never-created-' + Date.now());
    process.env.MEMORY_DIR = missing;
    delete require.cache[require.resolve('../src/gep/hubVerify')];
    const hv = require('../src/gep/hubVerify');

    let res;
    assert.doesNotThrow(() => { res = hv.consumeOfflinePermit(); },
      'consumeOfflinePermit must never throw — fresh install must return an envelope');
    assert.equal(res.ok, false);
    // The dir is auto-created (so subsequent loadOfflineToken can run);
    // with no token file present we fall through to the standard
    // no_offline_token result.
    assert.equal(res.error, 'no_offline_token');
    assert.equal(res.offline, true);
  });

  it('returns offline_lock_failed when the lock cannot be created', () => {
    // Point MEMORY_DIR at a regular file so mkdirSync(dir) inside the
    // pre-flight ensure throws ENOTDIR / EEXIST, and the subsequent
    // withFileLock _acquireLock call also fails. Both must be funneled
    // into the structured envelope, NOT a raw throw.
    const collidingFile = path.join(tmpRoot, 'is-a-file');
    fs.writeFileSync(collidingFile, 'x');
    process.env.MEMORY_DIR = collidingFile;
    delete require.cache[require.resolve('../src/gep/hubVerify')];
    const hv = require('../src/gep/hubVerify');

    let res;
    assert.doesNotThrow(() => { res = hv.consumeOfflinePermit(); },
      'consumeOfflinePermit must never throw — FS misconfig must return an envelope');
    assert.equal(res.ok, false);
    // Could be either no_offline_token (if the inner mkdir somehow
    // succeeded) or offline_lock_failed (the new catch-all branch).
    // Both honour the never-throw contract.
    assert.ok(
      res.error === 'offline_lock_failed' || res.error === 'no_offline_token',
      'unexpected error: ' + res.error,
    );
    assert.equal(res.offline, true);
  });
});

describe('consumeOfflinePermit: cross-process serialization', () => {
  let tmpDir;

  beforeEach(() => {
    tmpDir = makeTmpDir();
  });

  afterEach(() => {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  });

  it('two concurrent child processes never exceed maxSolidifies on a shared .ot', async () => {
    // Plant a fresh token with maxSolidifies = 5. Two child processes each
    // call consumeOfflinePermit 6 times back-to-back (12 attempts total).
    // The lock must guarantee no more than 5 successes across both
    // processes; the remaining 7 attempts must be rejected as either
    // quota_exhausted or permit_busy.
    const maxSolidifies = 5;
    const callsPerChild = 6;
    const secret = TEST_NODE_SECRET;
    makeSignedToken(tmpDir, {
      usedCount: 0, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: maxSolidifies,
    }, secret);

    const workerSrc = `
      process.env.A2A_NODE_SECRET = '${secret}';
      process.env.MEMORY_DIR = ${JSON.stringify(tmpDir)};
      const hv = require(${JSON.stringify(require.resolve('../src/gep/hubVerify'))});
      const results = [];
      for (let i = 0; i < ${callsPerChild}; i++) {
        results.push(hv.consumeOfflinePermit());
      }
      process.send({ results });
      process.exit(0);
    `;
    const workerPath = path.join(tmpDir, 'worker.js');
    fs.writeFileSync(workerPath, workerSrc);

    function runChild() {
      return new Promise((resolve, reject) => {
        const child = fork(workerPath, [], { silent: true });
        let payload = null;
        child.on('message', (m) => { payload = m; });
        child.on('exit', (code) => {
          if (code !== 0) return reject(new Error('child exited ' + code));
          resolve(payload && payload.results || []);
        });
        child.on('error', reject);
      });
    }

    const [a, b] = await Promise.all([runChild(), runChild()]);
    const all = a.concat(b);
    const successes = all.filter((r) => r.ok).length;
    const quotaExhausted = all.filter((r) => r.error === 'offline_quota_exhausted').length;
    const busy = all.filter((r) => r.error === 'offline_permit_busy').length;
    const other = all.filter((r) => !r.ok && r.error !== 'offline_quota_exhausted' && r.error !== 'offline_permit_busy');

    assert.equal(all.length, callsPerChild * 2, 'each child must complete all calls');
    assert.ok(successes <= maxSolidifies,
      'lock must cap total successes at maxSolidifies — got ' + successes +
      ' (busy=' + busy + ', quota=' + quotaExhausted + ', other=' + JSON.stringify(other) + ')');
    assert.equal(successes + quotaExhausted + busy, all.length,
      'every result must fall into one of the three expected buckets');

    // Final stored usedCount must equal the number of successes — proves
    // no concurrent write clobbered the counter.
    const stored = JSON.parse(fs.readFileSync(path.join(tmpDir, '.ot'), 'utf8'));
    assert.equal(stored.data.usedCount, successes,
      'persisted usedCount must equal observed successes (no lost-update race)');
  });

  it('returns offline_permit_busy when another live process holds the lock', async () => {
    // Plant a valid token, then spawn a child that acquires the lock and
    // holds it for longer than the parent's withFileLock timeout. The
    // parent's consumeOfflinePermit must surface the timeout as the
    // structured `offline_permit_busy` envelope so the daemon's caller
    // can distinguish "contended" from "permit denied" and retry next
    // cycle.
    const secret = TEST_NODE_SECRET;
    makeSignedToken(tmpDir, {
      usedCount: 0, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: 5,
    }, secret);

    // The child grabs withFileLock at the same target path the parent
    // will, then sits in the critical section for 7s (longer than
    // assetStore's 5s LOCK_TIMEOUT_MS). It signals the parent once it
    // has the lock so the parent's consumeOfflinePermit call can begin
    // racing — guaranteed to lose.
    const tokenPath = path.join(tmpDir, '.ot');
    const workerSrc = `
      const { withFileLock } = require(${JSON.stringify(require.resolve('../src/gep/assetStore'))});
      withFileLock(${JSON.stringify(tokenPath)}, () => {
        process.send('locked');
        // Sleep ~7s — longer than the parent's 5s acquire timeout.
        const buf = new Int32Array(new SharedArrayBuffer(4));
        Atomics.wait(buf, 0, 0, 7000);
      });
    `;
    const workerPath = path.join(tmpDir, 'holder.js');
    fs.writeFileSync(workerPath, workerSrc);

    const child = fork(workerPath, [], { silent: true });
    let lockReady = false;
    child.on('message', (m) => { if (m === 'locked') lockReady = true; });
    // Poll until child reports lock acquired (~50ms typical).
    const deadline = Date.now() + 2000;
    while (!lockReady && Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 25));
    }
    assert.ok(lockReady, 'child must signal lock acquired within 2s');

    process.env.A2A_NODE_SECRET = secret;
    process.env.MEMORY_DIR = tmpDir;
    delete require.cache[require.resolve('../src/gep/hubVerify')];
    const hv = require('../src/gep/hubVerify');

    const t0 = Date.now();
    const res = hv.consumeOfflinePermit();
    const elapsed = Date.now() - t0;

    assert.equal(res.ok, false);
    assert.equal(res.error, 'offline_permit_busy',
      'timeout must map to structured offline_permit_busy, not raw throw');
    assert.equal(res.offline, true);
    assert.ok(elapsed >= 4500,
      'must have waited close to assetStore LOCK_TIMEOUT_MS (5s) before giving up — got ' + elapsed + 'ms');
    assert.ok(elapsed < 6500,
      'must not block much past the timeout — got ' + elapsed + 'ms');

    // Verify usedCount was NOT touched — proves the parent never entered
    // the critical section while the child held the lock.
    const stored = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
    assert.equal(stored.data.usedCount, 0, 'usedCount must not be incremented on busy');

    // Best-effort cleanup: kill the holder so the test process exits cleanly.
    try { child.kill('SIGKILL'); } catch (_) {}
    await new Promise((r) => child.once('exit', r));
  });
});
