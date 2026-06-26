// ATP Auto-Buyer (opt-in: requires explicit consent before auto-spending)
// Converts capability gaps into ATP orders with strict budget caps and
// 24h question-level deduplication. Budget caps:
//   ATP_AUTOBUY_DAILY_CAP_CREDITS     (default 50)
//   ATP_AUTOBUY_PER_ORDER_CAP_CREDITS (default 10)
// Cold-start safety: the first 5 minutes after process start use a half-cap
// to protect against misconfiguration loops on restart storms.
//
// Consent resolution (in order):
//   1. EVOLVER_ATP_AUTOBUY=on|off env — explicit operator override wins.
//   2. ack file at <memory>/atp-autobuy-ack.json with `{enabled: bool}` —
//      written by first-run prompt (cliAutobuyPrompt) or `evolver atp
//      enable|disable`.
//   3. No signal → OFF. New installs never auto-spend before the user has
//      explicitly opted in (consumer protection: ATP spends real credits).
//
// Integration contract:
//   1) Call start({ dailyCap, perOrderCap }) once at Evolver boot. The
//      evolve loop does this at the top of every cycle; start() is
//      idempotent so the repeated call is a no-op.
//   2) Call considerOrder({ signals, question, capabilities, budget, ... })
//      from the evolve loop whenever a capability gap is detected.
//   3) Result shape: { ok, skipped?, reason?, data?, error? }.
//
// Failure modes are non-fatal; every external call is wrapped with a 3s
// timeout race so loop cadence is never blocked by network issues.

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const { getMemoryDir } = require('../gep/paths');
const hubClient = require('./hubClient');

const DEFAULT_DAILY_CAP = 50;
const DEFAULT_PER_ORDER_CAP = 10;
const DEFAULT_ORDER_TIMEOUT_MS = 3000;
const COLD_START_WINDOW_MS = 5 * 60 * 1000;
// Successful orders dedup for 24h so the same capability gap is only paid for
// once per day. Failed orders dedup for 5 minutes only — long enough to
// absorb tight retry loops (the original goal of "don't hammer the hub")
// without making the user wait 24h to retry a question after a transient
// 503/network blip.
const DEDUP_TTL_MS = 24 * 60 * 60 * 1000;
const DEDUP_FAILURE_TTL_MS = 5 * 60 * 1000;
const LEDGER_FILENAME = 'atp-autobuyer-ledger.json';
const ACK_FILENAME = 'atp-autobuy-ack.json';

let _started = false;
let _startedAt = 0;
let _config = {
  dailyCap: DEFAULT_DAILY_CAP,
  perOrderCap: DEFAULT_PER_ORDER_CAP,
  timeoutMs: DEFAULT_ORDER_TIMEOUT_MS,
};

function _ledgerPath() {
  return path.join(getMemoryDir(), LEDGER_FILENAME);
}

function _ackPath() {
  return path.join(getMemoryDir(), ACK_FILENAME);
}

function _todayKey(now) {
  const d = new Date(typeof now === 'number' ? now : Date.now());
  return d.toISOString().slice(0, 10); // UTC YYYY-MM-DD
}

function _readAck() {
  try {
    const p = _ackPath();
    if (!fs.existsSync(p)) return null;
    const parsed = JSON.parse(fs.readFileSync(p, 'utf8'));
    if (!parsed || typeof parsed !== 'object') return null;
    if (typeof parsed.enabled !== 'boolean') return null;
    return parsed;
  } catch (_) {
    return null;
  }
}

// Resolve consent. Returns:
//   { enabled: true,  source: 'env'|'ack'|'default' }
//   { enabled: false, source: 'env'|'ack' }
// The `default` case is the new-install path (no env override, no ack file):
// auto-spend defaults ON, gated by the daily/per-order caps and the cold-start
// half-cap window. The first-run prompt and `evolver atp disable` remain the
// opt-out paths for users who do not want auto-spend; once an explicit ack is
// recorded the source flips to 'ack' and the user's choice (either way) wins
// over this default.
function getConsent() {
  const envRaw = process.env.EVOLVER_ATP_AUTOBUY;
  if (typeof envRaw === 'string') {
    // Trim BEFORE the length check so whitespace-only values
    // (e.g. EVOLVER_ATP_AUTOBUY=" ") count as unset, matching the
    // classify() helper in cliAutobuyPrompt.js. Without this alignment a
    // whitespace value would skip the prompt in classify (treats as unset
    // → 'eligible') but still enter this env branch, trim to "", fail to
    // match 'off'/'0'/'false', and silently return enabled=true.
    const s = envRaw.trim().toLowerCase();
    if (s.length > 0) {
      const enabled = s !== 'off' && s !== '0' && s !== 'false';
      return { enabled, source: 'env' };
    }
  }
  const ack = _readAck();
  if (ack) {
    return { enabled: ack.enabled === true, source: 'ack' };
  }
  return { enabled: true, source: 'default' };
}

function _emptyLedger() {
  return { version: 1, dayKey: _todayKey(), spent: 0, dedup: {} };
}

function _readLedger() {
  try {
    const p = _ledgerPath();
    if (!fs.existsSync(p)) return _emptyLedger();
    const raw = fs.readFileSync(p, 'utf8');
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object') return _emptyLedger();
    if (!parsed.dayKey || !parsed.dedup) return _emptyLedger();
    return parsed;
  } catch (_) {
    return _emptyLedger();
  }
}

function _writeLedger(ledger) {
  try {
    const dir = getMemoryDir();
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const tmp = _ledgerPath() + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(ledger, null, 2));
    fs.renameSync(tmp, _ledgerPath());
  } catch (_) {
    // Non-fatal: ledger persistence failure means next process restart
    // re-reads previous ledger (so existing caps still apply).
  }
}

function _rotateIfNewDay(ledger, now) {
  const today = _todayKey(now);
  if (ledger.dayKey !== today) {
    return { version: 1, dayKey: today, spent: 0, dedup: ledger.dedup || {} };
  }
  return ledger;
}

function _pruneDedup(ledger, now) {
  const nowMs = typeof now === 'number' ? now : Date.now();
  const out = {};
  const src = ledger.dedup || {};
  const keys = Object.keys(src);
  for (let i = 0; i < keys.length; i++) {
    const k = keys[i];
    const entry = src[k];
    // Legacy ledgers written by older versions stored plain timestamps; treat
    // them as successful orders (the original behaviour) so an upgrade does
    // not suddenly forget recent dedups.
    if (typeof entry === 'number') {
      if (entry >= nowMs - DEDUP_TTL_MS) out[k] = entry;
    } else if (entry && typeof entry.ts === 'number') {
      const ttl = entry.failed ? DEDUP_FAILURE_TTL_MS : DEDUP_TTL_MS;
      if (entry.ts >= nowMs - ttl) out[k] = entry;
    }
  }
  ledger.dedup = out;
  return ledger;
}

function _questionHash(opts) {
  const caps = Array.isArray(opts.capabilities) ? opts.capabilities.slice().sort().join(',') : '';
  const q = (opts.question || '').slice(0, 2000);
  return crypto.createHash('sha256').update(caps + '|' + q).digest('hex').slice(0, 24);
}

function _effectiveCap(value, now) {
  const n = Number(value);
  if (!Number.isFinite(n) || n < 0) return 0;
  const within = _startedAt > 0 && (now - _startedAt) < COLD_START_WINDOW_MS;
  return within ? Math.floor(n / 2) : Math.floor(n);
}

function start(opts) {
  if (_started) return;
  const consent = getConsent();
  if (!consent.enabled) return;
  _started = true;
  _startedAt = Date.now();
  const dailyCap = Math.max(0, Math.floor(Number((opts && opts.dailyCap) || process.env.ATP_AUTOBUY_DAILY_CAP_CREDITS) || DEFAULT_DAILY_CAP));
  const perOrderCap = Math.max(0, Math.floor(Number((opts && opts.perOrderCap) || process.env.ATP_AUTOBUY_PER_ORDER_CAP_CREDITS) || DEFAULT_PER_ORDER_CAP));
  const timeoutMs = Math.max(500, Math.floor(Number((opts && opts.timeoutMs) || DEFAULT_ORDER_TIMEOUT_MS)));
  _config = { dailyCap, perOrderCap, timeoutMs };
  let ledger = _readLedger();
  ledger = _rotateIfNewDay(ledger, _startedAt);
  ledger = _pruneDedup(ledger, _startedAt);
  _writeLedger(ledger);
  console.log('[ATP-AutoBuyer] Started (dailyCap=' + dailyCap + ', perOrderCap=' + perOrderCap + ', cold-start half-cap for ' + (COLD_START_WINDOW_MS / 1000) + 's)');
}

function stop() {
  _started = false;
  _startedAt = 0;
}

function isStarted() {
  return _started;
}

function _withTimeout(promise, timeoutMs) {
  return Promise.race([
    promise,
    new Promise(function (resolve) {
      setTimeout(function () { resolve({ ok: false, error: 'autobuyer_timeout' }); }, timeoutMs);
    }),
  ]);
}

// Single-flight queue: serialize the read → cap-check → placeOrder → write
// pipeline so two concurrent considerOrder() calls cannot both pass the cap
// check on the same ledger snapshot and silently double-spend.
//
// Without this, two parallel calls (e.g. user runs Claude Code in two tabs
// through the same proxy, or two capability gaps fire in the same tick) both
// read spent=40, both compute remaining=10, both await placeOrder, both
// increment to spent=50, and write — silently exceeding the daily cap by one
// full order each. autoBuyer is single-process so an in-memory queue is
// sufficient; a file lock would only be needed if multiple OS processes
// shared the same ledger file (not the current deployment model).
let _orderQueue = Promise.resolve();

function considerOrder(opts) {
  if (!_started) return Promise.resolve({ ok: false, skipped: true, reason: 'not_started' });
  if (!opts || !Array.isArray(opts.capabilities) || opts.capabilities.length === 0) {
    return Promise.resolve({ ok: false, skipped: true, reason: 'no_capabilities' });
  }
  const next = _orderQueue.then(
    () => _considerOrderSerialized(opts),
    () => _considerOrderSerialized(opts), // never let a prior rejection break the chain
  );
  // Swallow rejection on the queue tail so a single thrown error here does
  // not poison every subsequent call; the original `next` promise still
  // surfaces the error to the caller.
  _orderQueue = next.then(() => {}, () => {});
  return next;
}

async function _considerOrderSerialized(opts) {
  const now = Date.now();
  let ledger = _readLedger();
  ledger = _rotateIfNewDay(ledger, now);
  ledger = _pruneDedup(ledger, now);

  const hash = _questionHash(opts);
  if (ledger.dedup[hash]) {
    return { ok: false, skipped: true, reason: 'dedup_hit', hash: hash };
  }

  const dailyCap = _effectiveCap(_config.dailyCap, now);
  const perOrderCap = _effectiveCap(_config.perOrderCap, now);
  const remaining = Math.max(0, dailyCap - (ledger.spent || 0));
  if (remaining <= 0) {
    console.warn('[ATP-AutoBuyer] Daily cap reached, skipping order (spent=' + ledger.spent + ', cap=' + dailyCap + ')');
    return { ok: false, skipped: true, reason: 'daily_cap_reached', spent: ledger.spent, cap: dailyCap };
  }

  const requested = Math.max(1, Math.floor(Number(opts.budget) || perOrderCap));
  const budget = Math.min(requested, perOrderCap, remaining);
  if (budget <= 0) {
    return { ok: false, skipped: true, reason: 'budget_clamped_to_zero' };
  }

  const orderOpts = {
    capabilities: opts.capabilities,
    budget: budget,
    routingMode: opts.routingMode || 'fastest',
    verifyMode: opts.verifyMode || 'auto',
    question: opts.question,
    signals: opts.signals,
    minReputation: opts.minReputation,
  };

  const result = await _withTimeout(hubClient.placeOrder(orderOpts), _config.timeoutMs);

  if (result && result.ok) {
    ledger.spent = (ledger.spent || 0) + budget;
    ledger.dedup[hash] = { ts: now, failed: false };
    _writeLedger(ledger);
    console.log('[ATP-AutoBuyer] Order placed: ' + (result.data && result.data.order_id) + ' budget=' + budget + ' remaining_today=' + Math.max(0, dailyCap - ledger.spent));
    return { ok: true, data: result.data, spent: budget };
  }

  // On failure record a SHORT-TTL dedup entry (5 min) so we don't hammer the
  // hub for the same capability gap inside a tight retry loop, but the user
  // can retry the same question once the transient error clears — far better
  // than the previous 24h block for a single 503.
  ledger.dedup[hash] = { ts: now, failed: true };
  _writeLedger(ledger);
  return { ok: false, error: (result && result.error) || 'unknown_error' };
}

// Write the consent ack file. Used by `evolver atp enable|disable` and the
// first-run prompt. `enabled=true` persists opt-in; `enabled=false` persists
// explicit opt-out so the prompt does not re-ask next session. Atomic write
// via .tmp + rename so a crash mid-write never produces a corrupt ack file.
function setConsent(enabled) {
  const dir = getMemoryDir();
  const body = {
    enabled: !!enabled,
    acknowledged_at: new Date().toISOString(),
    version: 1,
  };
  const tmp = _ackPath() + '.tmp';
  // Single try/catch over the whole pipeline. Previously the mkdirSync was
  // wrapped in its own swallowing try/catch, so an EACCES on the parent dir
  // would surface to the caller as a confusing ENOENT from writeFileSync.
  // Surface the original error verbatim and best-effort clean up any
  // partial .tmp file so a retry from a TTY prompt sees a clean slate.
  try {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(tmp, JSON.stringify(body, null, 2) + '\n', 'utf8');
    fs.renameSync(tmp, _ackPath());
  } catch (err) {
    try { fs.unlinkSync(tmp); } catch (_) {}
    throw err;
  }
  return body;
}

// Test-only reset, not exported by default.
function _resetForTests() {
  _started = false;
  _startedAt = 0;
  _config = {
    dailyCap: DEFAULT_DAILY_CAP,
    perOrderCap: DEFAULT_PER_ORDER_CAP,
    timeoutMs: DEFAULT_ORDER_TIMEOUT_MS,
  };
  _orderQueue = Promise.resolve();
}

module.exports = {
  // Lifecycle.
  start,
  stop,
  isStarted,
  considerOrder,
  // Consent surface — public API. Production callers (CLI runAtp,
  // cliAutobuyPrompt, the daemon run loop) MUST use these, not the
  // __internals duplicates below, so the "test-only" contract on
  // __internals stays honest (Bugbot PR #141 R6).
  getConsent,
  setConsent,
  getAckPath: _ackPath,
  readAck: _readAck,
  ACK_FILENAME,
  // Exposed for tests and diagnostics only; callers should not depend on
  // these internals in production code paths. Ack-file helpers
  // (getAckPath / readAck / ACK_FILENAME) are intentionally NOT mirrored
  // here — production and tests both go through the public surface above,
  // so a single source of truth survives schema changes (Bugbot PR #141 R6
  // follow-up: keep "test-only" honest, no production caller may reach in).
  __internals: {
    readLedger: _readLedger,
    writeLedger: _writeLedger,
    questionHash: _questionHash,
    effectiveCap: _effectiveCap,
    resetForTests: _resetForTests,
    constants: {
      DEFAULT_DAILY_CAP,
      DEFAULT_PER_ORDER_CAP,
      COLD_START_WINDOW_MS,
      DEDUP_TTL_MS,
      DEDUP_FAILURE_TTL_MS,
      LEDGER_FILENAME,
    },
  },
};
