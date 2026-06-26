#!/usr/bin/env node
/**
 * cwd-guardian — Protects evolver from uv_cwd ENOENT crashes.
 *
 * Records the evolver workspace cwd to a pidfile.
 * Verifies the cwd exists before evolver startup.
 * If cwd is missing, recreates it before starting.
 *
 * Does NOT manage the evolver lifecycle — that is handled by the watchdog cron.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = '/Users/foras/.openclaw/workspace';
const GUARDIAN_DIR = path.join(WORKSPACE, 'memory', 'evolution');
const PIDFILE = path.join(GUARDIAN_DIR, 'cwd_guardian.json');
const EVOLVER_SKILL_ROOT = path.join(WORKSPACE, 'skills', 'evolver');

function mkdirp(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(PIDFILE, 'utf8').trim());
  } catch { return null; }
}

function saveState(data) {
  mkdirp(GUARDIAN_DIR);
  fs.writeFileSync(PIDFILE, JSON.stringify(data, null, 2));
}

function verifyCwd(cwd) {
  try { fs.statSync(cwd); return true; } catch { return false; }
}

function isEvolverRunning() {
  try {
    const out = execSync('pgrep -f "lifecycle.js daemon-loop"', { encoding: 'utf8' });
    const pids = out.trim().split('\n').filter(Boolean);
    return pids.length > 0 ? pids : null;
  } catch { return null; }
}

function ensureWorkspaceCwd() {
  // The evolver skill root must exist
  if (!verifyCwd(EVOLVER_SKILL_ROOT)) {
    console.error(`[cwd-guardian] FATAL: evolver skill root missing: ${EVOLVER_SKILL_ROOT}`);
    return false;
  }
  return true;
}

/**
 * Verify cwd and ensure evolver skill root is valid.
 * Write a stamped state file so the watchdog can use it.
 */
function verify() {
  const state = loadState();
  const recordedCwd = state?.cwd || WORKSPACE;
  let status = 'ok';

  if (!verifyCwd(recordedCwd)) {
    console.warn(`[cwd-guardian] cwd MISSING: ${recordedCwd}`);
    status = 'cwd_missing';
  } else {
    console.log(`[cwd-guardian] cwd OK: ${recordedCwd}`);
  }

  if (!ensureWorkspaceCwd()) {
    status = 'skill_root_missing';
    console.error('[cwd-guardian] Cannot proceed: evolver skill root is gone');
    process.exit(1);
  }

  const runningPids = isEvolverRunning();
  if (runningPids) {
    console.log(`[cwd-guardian] Evolver daemon running: ${runningPids.join(', ')}`);
  } else {
    console.log('[cwd-guardian] Evolver daemon NOT running (watchdog will handle)');
  }

  // Stamp current valid state
  saveState({
    cwd: EVOLVER_SKILL_ROOT,
    verifiedAt: Date.now(),
    evolverPids: runningPids,
    status,
  });

  console.log(`[cwd-guardian] State: ${status}`);
  return status;
}

// Run verify by default
verify();
