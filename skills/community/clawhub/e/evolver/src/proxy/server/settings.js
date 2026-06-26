'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

// Settings paths are resolved on every call rather than snapshotted at module
// load. Tests run in parallel by default (`node --test`); when multiple test
// files exercise the proxy server, each one starting writes
// `~/.evolver/settings.json` and the sibling webui observer would read those
// bytes back and report mode='proxy_only' instead of the expected 'idle'.
// Lazy resolution lets a test set EVOLVER_SETTINGS_DIR to a temp dir before
// calling start()/readSettings() and stay isolated from concurrent workers.
function getSettingsDir() {
  return process.env.EVOLVER_SETTINGS_DIR || path.join(os.homedir(), '.evolver');
}

function getSettingsFile() {
  return path.join(getSettingsDir(), 'settings.json');
}

function readSettings() {
  try {
    const file = getSettingsFile();
    if (fs.existsSync(file)) {
      return JSON.parse(fs.readFileSync(file, 'utf8'));
    }
  } catch {}
  return {};
}

function writeSettings(data) {
  const dir = getSettingsDir();
  const file = getSettingsFile();
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const current = readSettings();
  const merged = { ...current, ...data };
  // NOTE(windows): mode 0o600 is silently ignored on Windows. The settings
  // file (which may contain proxy credentials) will NOT be owner-read-only.
  // Only Windows user-profile directory ACLs provide isolation. The chmodSync
  // call below is also a no-op on Windows but is retained for Unix correctness.
  fs.writeFileSync(file, JSON.stringify(merged, null, 2), { encoding: 'utf8', mode: 0o600 });
  // mode: 0o600 only applies on creation; explicitly chmod to tighten pre-existing files
  try { fs.chmodSync(file, 0o600); } catch { /* best-effort; no-op on Windows */ }
  return merged;
}

function clearSettings(opts = {}) {
  try {
    const file = getSettingsFile();
    if (fs.existsSync(file)) {
      const current = readSettings();
      const proxyPid = current.proxy?.pid;
      if (!opts.force && proxyPid && proxyPid !== process.pid) return false;
      delete current.proxy;
      fs.writeFileSync(file, JSON.stringify(current, null, 2), 'utf8');
      return true;
    }
  } catch {}
  return false;
}

function isStaleProxy() {
  const settings = readSettings();
  const pid = settings.proxy?.pid;
  if (!pid) return false;
  try {
    // process.kill(pid, 0) probes whether the process exists without sending a
    // signal. On POSIX it throws ESRCH when the PID is gone. On Windows the
    // Node.js runtime maps this to the same behavior (ESRCH via uv_kill), so
    // the cross-platform semantics are consistent. If the current process does
    // not have permission to query the target PID, EPERM is thrown -- that
    // means the PID exists and is owned by another user, so we treat it as
    // live (not stale) rather than crashing.
    process.kill(pid, 0);
    return false;
  } catch (err) {
    // ESRCH: process does not exist -> stale.
    // EPERM: process exists but is not ours -> not stale (leave settings alone).
    if (err.code === 'EPERM') return false;
    return true;
  }
}

function clearIfStale() {
  if (isStaleProxy()) {
    clearSettings({ force: true });
    return true;
  }
  return false;
}

function getProxyUrl() {
  const settings = readSettings();
  return settings.proxy?.url || null;
}

function getProxyToken() {
  const settings = readSettings();
  return settings.proxy?.token || null;
}

module.exports = {
  readSettings,
  writeSettings,
  clearSettings,
  clearIfStale,
  isStaleProxy,
  getProxyUrl,
  getProxyToken,
  getSettingsDir,
  getSettingsFile,
};
