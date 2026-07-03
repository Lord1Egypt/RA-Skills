'use strict';

const fs = require('fs');
const path = require('path');

const PRIVATE_DIR_MODE = 0o700;
const PRIVATE_FILE_MODE = 0o600;
const STATE_LOCK_STALE_MS = 10_000;
const STATE_LOCK_WAIT_MS = 10;

const MAILBOX_NODE_SECRET_STATE_KEYS = Object.freeze([
  'node_secret',
  'node_secret_version',
  'node_secret_source',
  'node_secret_env_suppressed',
]);

const MAILBOX_NODE_SECRET_STATE_KEY_SET = new Set(MAILBOX_NODE_SECRET_STATE_KEYS);
const MAILBOX_NODE_SECRET_TUPLE_KEYS = Object.freeze([
  'node_secret',
  'node_secret_version',
  'node_secret_source',
]);
const MAILBOX_NODE_SECRET_TUPLE_KEY_SET = new Set(MAILBOX_NODE_SECRET_TUPLE_KEYS);

function bestEffortChmod(filePath, mode) {
  try { fs.chmodSync(filePath, mode); } catch { /* best effort; no-op on Windows */ }
}

function ensurePrivateDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true, mode: PRIVATE_DIR_MODE });
  }
  bestEffortChmod(dir, PRIVATE_DIR_MODE);
}

function writePrivateFile(filePath, content) {
  fs.writeFileSync(filePath, content, { encoding: 'utf8', mode: PRIVATE_FILE_MODE });
  bestEffortChmod(filePath, PRIVATE_FILE_MODE);
}

function sleepSync(ms) {
  try {
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
  } catch {
    const end = Date.now() + ms;
    while (Date.now() < end) {}
  }
}

function acquireStateFileLock(stateFile) {
  ensurePrivateDir(path.dirname(stateFile));
  const lockDir = `${stateFile}.lock`;
  const startedAt = Date.now();
  while (true) {
    try {
      fs.mkdirSync(lockDir, { mode: PRIVATE_DIR_MODE });
      bestEffortChmod(lockDir, PRIVATE_DIR_MODE);
      return function releaseStateFileLock() {
        try { fs.rmdirSync(lockDir); } catch {}
      };
    } catch (e) {
      if (!e || e.code !== 'EEXIST') throw e;
      try {
        const ageMs = Date.now() - fs.statSync(lockDir).mtimeMs;
        if (ageMs > STATE_LOCK_STALE_MS) {
          fs.rmSync(lockDir, { recursive: true, force: true });
          continue;
        }
      } catch (statErr) {
        if (statErr && statErr.code === 'ENOENT') continue;
        throw statErr;
      }
      if (Date.now() - startedAt > STATE_LOCK_STALE_MS) {
        const err = new Error('timed out waiting for mailbox state lock');
        err.code = 'MAILBOX_STATE_LOCK_TIMEOUT';
        throw err;
      }
      sleepSync(STATE_LOCK_WAIT_MS);
    }
  }
}

function isPlainState(value) {
  return value && typeof value === 'object' && !Array.isArray(value);
}

function isHubRotatedNodeSecretState(state) {
  return isPlainState(state)
    && state.node_secret_source === 'hub_rotate'
    && typeof state.node_secret === 'string'
    && Boolean(state.node_secret.trim());
}

function parseNodeSecretVersion(value) {
  const n = Number(value);
  return Number.isInteger(n) && n > 0 ? n : null;
}

function isFullNodeSecretTupleUpdate(updatedSet) {
  return Boolean(updatedSet) && MAILBOX_NODE_SECRET_TUPLE_KEYS.every((key) => updatedSet.has(key));
}

function canApplyPartialNodeSecretTupleWrite(key, disk, next) {
  if (key !== 'node_secret_version') return false;
  if (!isHubRotatedNodeSecretState(disk)) return true;
  if (!isHubRotatedNodeSecretState(next)) return false;
  if (String(next.node_secret).trim() !== String(disk.node_secret).trim()) return false;
  const nextVersion = parseNodeSecretVersion(next.node_secret_version);
  const diskVersion = parseNodeSecretVersion(disk.node_secret_version);
  return Boolean(nextVersion && (!diskVersion || nextVersion >= diskVersion));
}

/**
 * @param {string} stateFile
 * @returns {Record<string, unknown>|null}
 */
function readMailboxStateFile(stateFile) {
  try {
    if (!fs.existsSync(stateFile)) return null;
    const parsed = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
    return isPlainState(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

function replaceStateFile(stateFile, state) {
  const dir = path.dirname(stateFile);
  ensurePrivateDir(dir);
  const tmp = `${stateFile}.${process.pid}.tmp`;
  writePrivateFile(tmp, JSON.stringify(state || {}, null, 2) + '\n');
  // Windows: renameSync throws EPERM when the destination file already
  // exists, unlike POSIX where rename(2) atomically replaces the target.
  if (process.platform === 'win32') {
    try { fs.unlinkSync(stateFile); } catch (e) {
      if (e.code !== 'ENOENT') throw e;
    }
  }
  fs.renameSync(tmp, stateFile);
  bestEffortChmod(stateFile, PRIVATE_FILE_MODE);
}

/**
 * Merge a partial state write with the latest on-disk state.
 *
 * Callers pass the keys they intentionally changed. Secret-bearing keys are
 * only written when they are in `updatedKeys`, so an old long-running
 * MailboxStore cannot overwrite a fresher Hub-rotated or divergence-cleared
 * secret tuple that was written by another process between load and persist.
 *
 * @param {string} stateFile
 * @param {Record<string, unknown>} nextState
 * @param {Iterable<string>} updatedKeys
 * @returns {Record<string, unknown>}
 */
function writeMergedMailboxStateFile(stateFile, nextState, updatedKeys) {
  const releaseLock = acquireStateFileLock(stateFile);
  try {
    const next = isPlainState(nextState) ? nextState : {};
    const disk = readMailboxStateFile(stateFile);
    const hasDiskState = isPlainState(disk);
    const merged = hasDiskState ? { ...disk } : {};
    const updatedSet = updatedKeys ? new Set(Array.from(updatedKeys)) : null;
    const keys = updatedSet ? Array.from(updatedSet) : Object.keys(next);
    const touchesNodeSecretTuple = keys.some((key) => MAILBOX_NODE_SECRET_TUPLE_KEY_SET.has(key));
    const preserveDiskNodeSecretTuple = touchesNodeSecretTuple
      && hasDiskState
      && isHubRotatedNodeSecretState(disk)
      && !isFullNodeSecretTupleUpdate(updatedSet);

    for (const key of keys) {
      if (MAILBOX_NODE_SECRET_STATE_KEY_SET.has(key) && hasDiskState && (!updatedSet || !updatedSet.has(key))) {
        continue;
      }
      if (
        MAILBOX_NODE_SECRET_TUPLE_KEY_SET.has(key) &&
        preserveDiskNodeSecretTuple &&
        !canApplyPartialNodeSecretTupleWrite(key, disk, next)
      ) {
        continue;
      }
      if (!Object.prototype.hasOwnProperty.call(next, key)) {
        delete merged[key];
        continue;
      }
      merged[key] = next[key];
    }

    replaceStateFile(stateFile, merged);
    return merged;
  } finally {
    releaseLock();
  }
}

module.exports = {
  PRIVATE_DIR_MODE,
  PRIVATE_FILE_MODE,
  MAILBOX_NODE_SECRET_STATE_KEYS,
  bestEffortChmod,
  ensurePrivateDir,
  writePrivateFile,
  readMailboxStateFile,
  isHubRotatedNodeSecretState,
  writeMergedMailboxStateFile,
};
