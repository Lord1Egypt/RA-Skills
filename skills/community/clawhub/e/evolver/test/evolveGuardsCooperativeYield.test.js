'use strict';

// Cooperative-yield guards: lock file + release window.
//
// Background (2026-05-16): the daemon (`evolver --loop`) and the user
// repeatedly raced for control of the same working tree. v1.80.8 release
// failed once because daemon dirtied the tree mid-publish; mid-edit work
// was reset twice by daemon's solidify rollback. These guards give the user
// a cooperative way to tell daemon to stand down without killing it.
//
// evaluateUserLock: explicit `.evolver.lock` file → yield until removed
//   or until EVOLVE_USER_LOCK_TTL_MS (default 1h) makes it stale.
// evaluateReleaseWindow: most recent commit subject starts with
//   "chore(release)" and is younger than EVOLVE_RELEASE_WINDOW_MS (default
//   5min) → yield. Prevents daemon waking mid-deploy.

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { evaluateUserLock, evaluateReleaseWindow } = require('../src/evolve/guards');

describe('evaluateUserLock', () => {
  it('does not yield when the lock file does not exist', () => {
    const r = evaluateUserLock({
      lockPath: '/tmp/no-such-lock-' + Math.random(),
      now: Date.now(),
      ttlMs: 3600 * 1000,
      existsFn: () => false,
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'no_lock');
  });

  it('yields when a fresh lock exists', () => {
    const now = 1_000_000_000_000;
    const r = evaluateUserLock({
      lockPath: '/fake/.evolver.lock',
      now,
      ttlMs: 3600 * 1000,
      existsFn: () => true,
      statFn: () => ({ mtimeMs: now - 30_000 }), // 30s old
    });
    assert.equal(r.yield, true);
    assert.equal(r.reason, 'lock_active');
    assert.equal(r.ageMs, 30_000);
  });

  it('does NOT yield when the lock is stale (older than ttlMs)', () => {
    const now = 1_000_000_000_000;
    const r = evaluateUserLock({
      lockPath: '/fake/.evolver.lock',
      now,
      ttlMs: 60_000, // 1min
      existsFn: () => true,
      statFn: () => ({ mtimeMs: now - 5 * 60_000 }), // 5min old
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'lock_stale');
    // ageMs is still reported so the caller can log it
    assert.equal(r.ageMs, 5 * 60_000);
  });

  it('does not crash on stat errors', () => {
    const r = evaluateUserLock({
      lockPath: '/fake/.evolver.lock',
      now: Date.now(),
      ttlMs: 3600 * 1000,
      existsFn: () => true,
      statFn: () => { throw new Error('eperm'); },
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'stat_failed');
  });

  // Bugbot review on PR #46 caught this: NaN ttlMs makes every fresh lock
  // classify as 'lock_stale' and silently disables the entire user-yield
  // feature. evaluateUserLock now rejects non-finite, non-positive, AND
  // suspiciously-small ttlMs values — see MIN_USER_LOCK_TTL_MS in guards.js.
  it('returns invalid_ttl for NaN ttlMs', () => {
    const r = evaluateUserLock({
      lockPath: '/fake/.evolver.lock',
      now: Date.now(),
      ttlMs: NaN,
      existsFn: () => true,
      statFn: () => ({ mtimeMs: Date.now() - 1000 }),
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'invalid_ttl');
  });

  it('returns invalid_ttl for zero/negative ttlMs', () => {
    const r1 = evaluateUserLock({
      lockPath: '/fake/.evolver.lock', now: Date.now(), ttlMs: 0,
      existsFn: () => true, statFn: () => ({ mtimeMs: Date.now() }),
    });
    assert.equal(r1.reason, 'invalid_ttl');
    const r2 = evaluateUserLock({
      lockPath: '/fake/.evolver.lock', now: Date.now(), ttlMs: -1,
      existsFn: () => true, statFn: () => ({ mtimeMs: Date.now() }),
    });
    assert.equal(r2.reason, 'invalid_ttl');
  });

  // Bugbot review on PR #46 round 3 caught this: the previous fix relied on
  // envInt() to reject non-numeric env values, but parseInt('5m', 10) === 5,
  // not NaN. A user who writes `EVOLVE_USER_LOCK_TTL_MS=5m` expecting "5
  // minutes" would silently get a 5ms TTL and every fresh lock would
  // classify as 'lock_stale'. The MIN_USER_LOCK_TTL_MS floor (1000ms) in
  // evaluateUserLock catches this even when the upstream envInt happily
  // accepts the parseInt-prefix value.
  it('rejects ttlMs below the minimum sensible TTL (e.g. parseInt("5m")===5)', () => {
    const r = evaluateUserLock({
      lockPath: '/fake/.evolver.lock',
      now: Date.now(),
      ttlMs: 5, // simulates the EVOLVE_USER_LOCK_TTL_MS=5m parseInt quirk
      existsFn: () => true,
      statFn: () => ({ mtimeMs: Date.now() }),
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'invalid_ttl');
  });

  it('accepts the minimum sensible TTL of 1000ms exactly', () => {
    const now = 1_000_000_000_000;
    const r = evaluateUserLock({
      lockPath: '/fake/.evolver.lock',
      now,
      ttlMs: 1000,
      existsFn: () => true,
      statFn: () => ({ mtimeMs: now - 500 }), // 500ms old, well within 1000ms TTL
    });
    assert.equal(r.yield, true);
    assert.equal(r.reason, 'lock_active');
  });

  // Bugbot review on PR #46 (round 2) caught this: NFS / containers / hosts
  // with skewed clocks can produce a lock file whose mtime is slightly in
  // the future relative to Date.now(), making ageMs negative. The original
  // `ageMs >= 0 && ageMs <= ttlMs` guard treated that as 'lock_stale' and
  // silently dropped the yield. Now we treat future mtime as fresh.
  it('treats a future-mtime lock as fresh, not stale (clock skew)', () => {
    const now = 1_000_000_000_000;
    const r = evaluateUserLock({
      lockPath: '/fake/.evolver.lock',
      now,
      ttlMs: 60_000,
      existsFn: () => true,
      statFn: () => ({ mtimeMs: now + 5_000 }), // 5s in the future
    });
    assert.equal(r.yield, true);
    assert.equal(r.reason, 'lock_active_future_mtime');
    assert.ok(r.ageMs < 0);
  });
});

describe('evaluateReleaseWindow', () => {
  it('does not yield when windowMs is exactly 0 (feature disabled)', () => {
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): prepare v1.80.9',
      lastCommitUnixTs: Math.floor(Date.now() / 1000),
      now: Date.now(),
      windowMs: 0,
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'disabled');
  });

  // Bugbot review on PR #46 round 4 caught this: a tiny windowMs is NOT
  // harmless ("we'd yield one cycle we didn't have to") — git log alone
  // takes longer than 5ms, so a 5ms window means ageMs always exceeds it
  // and the daemon never yields. That's silent-disable, same failure mode
  // as the user-lock parseInt('5m')===5 case Bugbot caught earlier.
  it('returns invalid_window for parseInt-prefix-style windowMs (e.g. 5)', () => {
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): bump',
      lastCommitUnixTs: Math.floor(Date.now() / 1000),
      now: Date.now(),
      windowMs: 5, // simulates EVOLVE_RELEASE_WINDOW_MS=5m → parseInt(5)
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'invalid_window');
  });

  it('returns invalid_window for negative windowMs', () => {
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): x',
      lastCommitUnixTs: Math.floor(Date.now() / 1000),
      now: Date.now(),
      windowMs: -1,
    });
    assert.equal(r.reason, 'invalid_window');
  });

  it('returns invalid_window for NaN/Infinity windowMs', () => {
    assert.equal(
      evaluateReleaseWindow({
        lastCommitSubject: 'chore(release): x',
        lastCommitUnixTs: Math.floor(Date.now() / 1000),
        now: Date.now(),
        windowMs: NaN,
      }).reason,
      'invalid_window'
    );
    assert.equal(
      evaluateReleaseWindow({
        lastCommitSubject: 'chore(release): x',
        lastCommitUnixTs: Math.floor(Date.now() / 1000),
        now: Date.now(),
        windowMs: Infinity,
      }).reason,
      'invalid_window'
    );
  });

  it('accepts the minimum sensible window of 1000ms exactly', () => {
    const nowSec = 1_700_000_000;
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): bump',
      lastCommitUnixTs: nowSec,
      now: nowSec * 1000 + 500, // 500ms after commit
      windowMs: 1000,
    });
    assert.equal(r.yield, true);
    assert.equal(r.reason, 'release_window_active');
  });

  it('yields when most-recent commit is a fresh release bump', () => {
    const nowSec = 1_700_000_000;
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): prepare v1.80.9',
      lastCommitUnixTs: nowSec - 30, // 30s ago
      now: nowSec * 1000,
      windowMs: 5 * 60 * 1000, // 5min
    });
    assert.equal(r.yield, true);
    assert.equal(r.reason, 'release_window_active');
    assert.equal(r.ageMs, 30_000);
  });

  it('does NOT yield once the release window has passed', () => {
    const nowSec = 1_700_000_000;
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): prepare v1.80.9',
      lastCommitUnixTs: nowSec - 10 * 60, // 10min ago
      now: nowSec * 1000,
      windowMs: 5 * 60 * 1000, // 5min
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'window_passed');
  });

  it('does NOT yield for non-release commits even if recent', () => {
    const nowSec = 1_700_000_000;
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'fix(gep): some fix',
      lastCommitUnixTs: nowSec - 30,
      now: nowSec * 1000,
      windowMs: 5 * 60 * 1000,
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'not_release_commit');
  });

  it('matches case-insensitively (Chore(release): style)', () => {
    const nowSec = 1_700_000_000;
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'Chore(release): bump 1.80.10',
      lastCommitUnixTs: nowSec - 60,
      now: nowSec * 1000,
      windowMs: 5 * 60 * 1000,
    });
    assert.equal(r.yield, true);
  });

  it('does not yield when commit timestamp is unparseable', () => {
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): bump',
      lastCommitUnixTs: NaN,
      now: Date.now(),
      windowMs: 5 * 60 * 1000,
    });
    assert.equal(r.yield, false);
    assert.equal(r.reason, 'no_commit');
  });

  it('treats a future-dated release commit as fresh (clock skew symmetry)', () => {
    const nowSec = 1_700_000_000;
    const r = evaluateReleaseWindow({
      lastCommitSubject: 'chore(release): bump',
      lastCommitUnixTs: nowSec + 5, // 5s in the future
      now: nowSec * 1000,
      windowMs: 5 * 60 * 1000,
    });
    assert.equal(r.yield, true);
    assert.equal(r.reason, 'release_window_future_commit');
    assert.ok(r.ageMs < 0);
  });
});
