// src/gep/claimNudge.js
//
// Prints a highlighted, rate-limited console message when the Hub tells us
// this node has an outstanding claim_code (meaning: no user account is
// bound to this agent yet). The goal is to nudge the human operator to
// claim the node on the web so they can see earnings / credits.
//
// Behavior:
//  - Printed at most once per CLAIM_NUDGE_COOLDOWN_MS (default 6h) per
//    unique claim_code, so repeated hellos don't spam the terminal.
//  - Suppressed entirely when EVOLVER_DISABLE_CLAIM_NUDGE=1.
'use strict';

const fs = require('fs');
const path = require('path');
const { getEvomapDir } = require('./paths');

const CLAIM_NUDGE_COOLDOWN_MS = Math.max(
  60_000,
  Number(process.env.EVOLVER_CLAIM_NUDGE_COOLDOWN_MS) || 6 * 60 * 60 * 1000,
);

// Evaluated lazily via a function so EVOLVER_HOME changes between calls
// are honored (#114). Existing constants captured the env at module load,
// which broke test isolation.
function _stateFile() { return path.join(getEvomapDir(), 'claim_nudge_state.json'); }

let _memory = { lastPrintedCode: null, lastPrintedAt: 0 };

function _ensureDir(file) {
  try { fs.mkdirSync(path.dirname(file), { recursive: true }); } catch (_) {}
}

function _loadState() {
  try {
    const raw = fs.readFileSync(_stateFile(), 'utf8');
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === 'object') return parsed;
  } catch (_) {}
  return null;
}

function _saveState(state) {
  _ensureDir(_stateFile());
  try {
    fs.writeFileSync(_stateFile(), JSON.stringify(state), 'utf8');
  } catch (_) {
    // best-effort
  }
}

function _shouldPrint(claimCode, now) {
  if (process.env.EVOLVER_DISABLE_CLAIM_NUDGE === '1') return false;
  if (!claimCode || typeof claimCode !== 'string') return false;

  const disk = _loadState();
  const state = disk && typeof disk === 'object' ? disk : _memory;
  if (state.lastPrintedCode === claimCode && (now - Number(state.lastPrintedAt || 0)) < CLAIM_NUDGE_COOLDOWN_MS) {
    return false;
  }
  return true;
}

function _markPrinted(claimCode, now) {
  const state = { lastPrintedCode: claimCode, lastPrintedAt: now };
  _memory = state;
  _saveState(state);
}

/**
 * Print a highlighted console prompt telling the user how to claim this
 * unbound agent. Idempotent across boots (persists state on disk). Pass
 * opts.force=true to bypass cooldown (used by tests).
 *
 * @param {{claim_code?: string, claim_url?: string, claim_note?: string}} responsePayload
 * @param {{force?: boolean, now?: number}} [opts]
 * @returns {boolean} whether the nudge was actually printed
 */
function maybePrintClaimNudge(responsePayload, opts) {
  const options = opts || {};
  const now = typeof options.now === 'number' ? options.now : Date.now();
  const payload = responsePayload && typeof responsePayload === 'object' ? responsePayload : {};
  const code = payload.claim_code || null;
  const url = payload.claim_url || null;

  if (!options.force && !_shouldPrint(code, now)) return false;
  if (!code || !url) return false;

  const rule = '--------------------------------------------------------------------------------';
  const lines = [
    '',
    rule,
    '  [evomap] This agent is not linked to an EvoMap web account yet.',
    '',
    '    Claim URL : ' + url,
    '    Claim code: ' + code,
    '',
    '  Claiming links this agent to your account so you can track earnings,',
    '  withdraw credits, and manage nodes on the website. The agent runs',
    '  fine without claiming -- this is optional, but recommended.',
    rule,
    '',
  ];
  for (const line of lines) {
    try { console.log(line); } catch (_) {}
  }
  _markPrinted(code, now);
  return true;
}

function _resetForTests() {
  _memory = { lastPrintedCode: null, lastPrintedAt: 0 };
  try { fs.unlinkSync(_stateFile()); } catch (_) {}
}

module.exports = {
  maybePrintClaimNudge,
  CLAIM_NUDGE_COOLDOWN_MS,
  get STATE_FILE() { return _stateFile(); },
  _resetForTests,
};
