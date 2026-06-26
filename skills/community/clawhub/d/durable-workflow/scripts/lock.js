#!/usr/bin/env node
// lock.js — File-based process lock for single-instance enforcement
// Prevents two instances of the same workflow from running concurrently.
//
// Usage:
//   const { acquireLock, releaseLock, withLock } = require('./lock');
//   await withLock('/tmp/my-workflow.lock', async () => { ... });

'use strict';

const fs   = require('fs');
const path = require('path');

class LockError extends Error {
  constructor(msg, lockPath, pid) {
    super(msg);
    this.name = 'LockError';
    this.lockPath = lockPath;
    this.pid = pid;
  }
}

/**
 * Acquire a file-based lock.
 *
 * @param {string} lockPath     - Path to the lock file
 * @param {number} [timeoutMs]  - Unused (reserved for future polling mode); throws immediately if locked
 * @throws {LockError} if another live process holds the lock
 */
async function acquireLock(lockPath, timeoutMs = 5000) {
  const absPath = path.resolve(lockPath);

  if (fs.existsSync(absPath)) {
    let existing;
    try {
      existing = JSON.parse(fs.readFileSync(absPath, 'utf8'));
    } catch (_) {
      // Corrupt lock file — take it over
      console.warn(`[lock] Corrupt lock file at ${absPath}, taking over.`);
      existing = null;
    }

    if (existing && typeof existing.pid === 'number') {
      const isAlive = _isPidAlive(existing.pid);
      if (isAlive) {
        throw new LockError(
          `Lock held by PID ${existing.pid} (acquired ${existing.ts ? new Date(existing.ts).toISOString() : 'unknown'}). ` +
          `Kill that process or delete ${absPath} manually if it is stale.`,
          absPath,
          existing.pid
        );
      }
      // Stale lock from a dead process — log and take over
      console.warn(`[lock] Stale lock from dead PID ${existing.pid} at ${absPath}, taking over.`);
    }
  }

  // Write our lock
  const lockData = { pid: process.pid, ts: Date.now() };
  const tmpPath = absPath + '.tmp';
  fs.writeFileSync(tmpPath, JSON.stringify(lockData), 'utf8');
  fs.renameSync(tmpPath, absPath); // atomic on same filesystem
}

/**
 * Release a lock. Safe to call even if the lock doesn't exist.
 *
 * @param {string} lockPath
 */
function releaseLock(lockPath) {
  const absPath = path.resolve(lockPath);
  try {
    fs.unlinkSync(absPath);
  } catch (e) {
    if (e.code !== 'ENOENT') {
      console.warn(`[lock] Could not release lock at ${absPath}: ${e.message}`);
    }
  }
}

/**
 * Acquire lock, run fn, release lock in finally (even on error).
 *
 * @param {string}   lockPath
 * @param {Function} fn        - async function to run while holding the lock
 * @param {number}   [timeoutMs]
 * @returns the return value of fn
 * @throws {LockError} if lock cannot be acquired
 */
async function withLock(lockPath, fn, timeoutMs = 5000) {
  await acquireLock(lockPath, timeoutMs);
  try {
    return await fn();
  } finally {
    releaseLock(lockPath);
  }
}

/**
 * Check if a PID is alive using signal 0 (does not kill the process).
 * Returns false if the process does not exist or we lack permission to signal it.
 */
function _isPidAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (e) {
    // EPERM = process exists but we can't signal it (still alive)
    // ESRCH = no such process
    return e.code === 'EPERM';
  }
}

module.exports = { acquireLock, releaseLock, withLock, LockError };

// ---------------------------------------------------------------------------
// CLI demo — run this file directly to test
// ---------------------------------------------------------------------------
if (require.main === module) {
  const lockPath = process.argv[2] || '/tmp/test-workflow.lock';
  console.log(`Testing lock at: ${lockPath}`);

  withLock(lockPath, async () => {
    console.log(`Lock acquired by PID ${process.pid}`);
    await new Promise(r => setTimeout(r, 2000));
    console.log('Work done inside lock.');
  })
    .then(() => console.log('Lock released.'))
    .catch(e => {
      if (e.name === 'LockError') {
        console.error(`Could not acquire lock: ${e.message}`);
      } else {
        console.error(`Error: ${e.message}`);
      }
      process.exit(1);
    });
}
