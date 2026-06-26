// Feature flags persistence layer.
//
// Provides three-tier override semantics (read by callers):
//   1. Local env (highest priority, user escape hatch)
//   2. Persisted flag from disk (set by hub mailbox or manual write)
//   3. Code default (lowest priority)
//
// File location: ~/.evomap/feature_flags.json (same dir as node_id / node_secret).
// Schema: { "<key>": { value: any, source: string, updatedAt: ISO8601 } }
//
// Whitelist enforcement happens at the caller (HUB_EVENT_HANDLERS).

'use strict';

const fs = require('fs');
const path = require('path');

// Lazy resolution via paths.getEvomapDir() — honors EVOLVER_HOME (#114).
const { getEvomapDir } = require('./paths');
function _flagsDir() { return getEvomapDir(); }
function _flagsFile() { return path.join(_flagsDir(), 'feature_flags.json'); }
const LOCAL_FLAGS_FILE = path.resolve(__dirname, '..', '..', '.evomap_feature_flags.json');

let _cache = null;
let _cacheLoaded = false;

function _readFile(p) {
  try {
    if (!fs.existsSync(p)) return null;
    const raw = fs.readFileSync(p, 'utf8');
    if (!raw) return null;
    const obj = JSON.parse(raw);
    if (obj && typeof obj === 'object') return obj;
  } catch (_) {}
  return null;
}

function _loadFromDisk() {
  if (_cacheLoaded) return _cache;
  _cacheLoaded = true;
  _cache = _readFile(_flagsFile()) || _readFile(LOCAL_FLAGS_FILE) || {};
  return _cache;
}

function _writeToDisk(obj) {
  // NOTE(windows): mode 0o700 / 0o600 are silently ignored on Windows.
  // Feature-flag files will NOT be owner-only on Windows; they are protected
  // only by user-profile directory ACLs. This is acceptable as feature flags
  // are not security-critical secrets.
  try {
    const dir = _flagsDir();
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    }
    fs.writeFileSync(_flagsFile(), JSON.stringify(obj, null, 2), { encoding: 'utf8', mode: 0o600 });
    return true;
  } catch (_) {}
  try {
    fs.writeFileSync(LOCAL_FLAGS_FILE, JSON.stringify(obj, null, 2), { encoding: 'utf8', mode: 0o600 });
    return true;
  } catch (_) {}
  return false;
}

/**
 * Read a persisted feature flag value. Returns undefined if not set.
 * @param {string} key
 * @returns {any|undefined}
 */
function readFeatureFlag(key) {
  if (!key || typeof key !== 'string') return undefined;
  const all = _loadFromDisk();
  const entry = all[key];
  if (!entry || typeof entry !== 'object') return undefined;
  return entry.value;
}

/**
 * Persist a feature flag. Returns true on success.
 * @param {string} key
 * @param {any} value
 * @param {string} [source] - origin tag, e.g. "hub_mailbox", "manual"
 */
function writeFeatureFlag(key, value, source) {
  if (!key || typeof key !== 'string') return false;
  const all = _loadFromDisk();
  all[key] = {
    value,
    source: typeof source === 'string' && source ? source : 'unknown',
    updatedAt: new Date().toISOString(),
  };
  const ok = _writeToDisk(all);
  if (ok) _cache = all;
  return ok;
}

/**
 * Returns the full flags object (read-only view). For diagnostics/tests.
 */
function getAllFeatureFlags() {
  const all = _loadFromDisk();
  return JSON.parse(JSON.stringify(all));
}

/**
 * Reset the in-process cache. Test-only.
 */
function _resetCacheForTests() {
  _cache = null;
  _cacheLoaded = false;
}

module.exports = {
  readFeatureFlag,
  writeFeatureFlag,
  getAllFeatureFlags,
  _resetCacheForTests,
  // Getter so callers see the current EVOLVER_HOME at call time (#114).
  get FLAGS_FILE() { return _flagsFile(); },
  LOCAL_FLAGS_FILE,
};
