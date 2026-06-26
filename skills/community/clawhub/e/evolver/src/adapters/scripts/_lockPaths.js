// _lockPaths.js
// Single source of truth for the daemon singleton-lock location and lease
// tunables, shared by the daemon (index.js) and the session-start hook's
// auto-restart guard (evolver-session-start.js).
//
// Issue #176: the hook used to replicate this logic inline ("keep index.js
// out of the hook's require graph"), which could silently diverge whenever
// the daemon's lock resolution changed. This module keeps that property —
// it depends only on fs/os/path — while making divergence structurally
// impossible.
//
// Deployed-layout constraint (PR #163): hook scripts are COPIED into the
// host's hooks dir (e.g. `.claude/hooks/`) and run from there, so every
// same-dir helper they require must be a sibling file listed in
// hookAdapter.js's copy/remove lists (enforced by test/adapters.test.js).

const fs = require('fs');
const os = require('os');
const path = require('path');

// Round-4 (see the history note above index.js's daemon-lock block): the
// pidfile previously defaulted to __dirname, which differs per install mode
// (global install vs dev clone vs npx cache), so two daemons launched under
// different install modes never saw each other's lock. Default now lives
// under the per-user state dir so all install modes converge.
// EVOLVER_LOCK_DIR still overrides for tests / sandboxed runs — note the
// basename differs from the default in that case (`evolver.pid` vs
// `instance.lock`).
function getLockFilePath(env) {
  const e = env || process.env;
  if (e.EVOLVER_LOCK_DIR) {
    return path.join(e.EVOLVER_LOCK_DIR, 'evolver.pid');
  }
  // os.homedir() is cross-platform; process.env.HOME is unset on Windows.
  return path.join(os.homedir(), '.evomap', 'instance.lock');
}

// Round-9: lease tunables for the daemon lock. A live daemon refreshes the
// lock mtime every LOCK_REFRESH_MS; a lock whose mtime is older than
// STALE_LOCK_TTL_MS (and that was written by a lease-aware daemon) is
// treated as stale even if its PID happens to be alive — closing the
// "crash + PID reuse -> new daemon silently refuses to start" hole and the
// "SIGKILL leaves a stale lock nobody reclaims" hole. The TTL is well above
// the heartbeat interval (default 6min) so a healthy daemon never trips it.
// On Windows, SIGTERM is implemented as TerminateProcess() (not a catchable
// signal), so the daemon's releaseLock() never runs and the lock file stays
// on disk with the dead PID — hence the shorter Windows TTL, with a 1-min
// refresh (3x margin against transient FS hiccups). Unix: 5 min TTL is
// 2.5x the 2-min refresh cadence.
const STALE_LOCK_TTL_MS = process.platform === 'win32' ? 3 * 60_000 : 5 * 60_000;
const LOCK_REFRESH_MS = process.platform === 'win32' ? 1 * 60_000 : 2 * 60_000;

// Returns true if the lock was written by a lease-aware daemon AND its
// mtime is older than the stale TTL — i.e. no live owner is refreshing it,
// so it is safe to treat the recorded PID as dead regardless of whether
// process.kill(pid, 0) resolves (the PID may have been reused). Locks
// written by pre-lease daemons (payload.lease !== true) are never judged
// stale by mtime, so we never falsely steal an older daemon's lock.
function lockIsStaleByLease(lockFile, payload) {
  if (!payload || payload.lease !== true) return false;
  try {
    const ageMs = Date.now() - fs.statSync(lockFile).mtimeMs;
    return ageMs > STALE_LOCK_TTL_MS;
  } catch (_) {
    return false;
  }
}

module.exports = {
  getLockFilePath,
  lockIsStaleByLease,
  STALE_LOCK_TTL_MS,
  LOCK_REFRESH_MS,
};
