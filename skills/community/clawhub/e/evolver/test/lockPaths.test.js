// test/lockPaths.test.js
//
// Unit tests for src/adapters/scripts/_lockPaths.js — the single source of
// truth for the daemon singleton-lock location and lease staleness (issue
// #176). Both index.js and the session-start hook's auto-restart guard
// require this module, so its contract is what keeps them from drifting.
'use strict';

const { describe, it, beforeEach, after } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const lockPaths = require('../src/adapters/scripts/_lockPaths');

const originalLockDir = process.env.EVOLVER_LOCK_DIR;

beforeEach(() => {
  delete process.env.EVOLVER_LOCK_DIR;
});

after(() => {
  if (originalLockDir === undefined) delete process.env.EVOLVER_LOCK_DIR;
  else process.env.EVOLVER_LOCK_DIR = originalLockDir;
});

describe('getLockFilePath', () => {
  it('defaults to the per-user state dir so all install modes converge', () => {
    assert.equal(lockPaths.getLockFilePath(),
      path.join(os.homedir(), '.evomap', 'instance.lock'));
  });

  it('EVOLVER_LOCK_DIR overrides — and switches the basename to evolver.pid', () => {
    process.env.EVOLVER_LOCK_DIR = path.join(os.tmpdir(), 'evolver-lock-test');
    assert.equal(lockPaths.getLockFilePath(),
      path.join(os.tmpdir(), 'evolver-lock-test', 'evolver.pid'));
  });

  it('accepts an explicit env object (testability without mutating process.env)', () => {
    assert.equal(lockPaths.getLockFilePath({ EVOLVER_LOCK_DIR: '/x' }),
      path.join('/x', 'evolver.pid'));
    assert.equal(lockPaths.getLockFilePath({}),
      path.join(os.homedir(), '.evomap', 'instance.lock'));
  });
});

describe('lockIsStaleByLease', () => {
  let tmpDir;
  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-lease-'));
  });

  function writeLock(ageMs) {
    const lockFile = path.join(tmpDir, 'evolver.pid');
    fs.writeFileSync(lockFile, JSON.stringify({ pid: 12345, lease: true }));
    const t = new Date(Date.now() - ageMs);
    fs.utimesSync(lockFile, t, t);
    return lockFile;
  }

  it('fresh lease-aware lock is NOT stale', () => {
    const lockFile = writeLock(1000);
    assert.equal(lockPaths.lockIsStaleByLease(lockFile, { pid: 12345, lease: true }), false);
  });

  it('lease-aware lock older than the TTL IS stale', () => {
    const lockFile = writeLock(lockPaths.STALE_LOCK_TTL_MS + 60_000);
    assert.equal(lockPaths.lockIsStaleByLease(lockFile, { pid: 12345, lease: true }), true);
  });

  it('pre-lease lock is NEVER judged stale by mtime (no false takeover of old daemons)', () => {
    const lockFile = writeLock(lockPaths.STALE_LOCK_TTL_MS + 60_000);
    assert.equal(lockPaths.lockIsStaleByLease(lockFile, { pid: 12345 }), false);
    assert.equal(lockPaths.lockIsStaleByLease(lockFile, null), false);
  });

  it('stat failure (lock vanished) reports not-stale', () => {
    assert.equal(
      lockPaths.lockIsStaleByLease(path.join(tmpDir, 'missing.pid'), { pid: 1, lease: true }),
      false);
  });

  it('refresh cadence leaves headroom against the TTL on every platform', () => {
    assert.ok(lockPaths.STALE_LOCK_TTL_MS >= 2.5 * lockPaths.LOCK_REFRESH_MS,
      'TTL must be comfortably above the refresh cadence or healthy daemons get stolen');
  });
});
