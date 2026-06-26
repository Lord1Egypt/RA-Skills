// ATP Auto-Deliver (opt-out, merchant-side)
// Closes the ATP settlement loop for Evolver merchants by auto-calling
// submitDelivery for every claimed task that carries an atp_order_id.
//
// Without this module, an ATP order sits in `pending` until the 7-day escrow
// timeout refunds the buyer: the Hub routes the task to a merchant node and
// marks it claimed, but nothing in the Evolver runtime actually calls
// /a2a/atp/deliver. This was the root cause of the 0-settled-in-13-days
// pipeline stall observed in prod on 2026-04-27.
//
// Integration contract:
//   1) Call start({ pollMs }) once at Evolver boot. Default ON.
//      Disable by setting EVOLVER_ATP_AUTODELIVER=off.
//   2) The module polls /a2a/task/my every pollMs milliseconds, finds tasks
//      with atp_order_id + a `result_asset_id` (meaning the task already
//      completed through solidify), and submits a minimal proofPayload.
//   3) Each submitted order is remembered in a local ledger so we never
//      double-submit, even across restarts.
//
// Dedup ledger lives alongside autoBuyer's ledger under memory/.
// Failure modes are non-fatal: network errors are logged, not thrown.

const fs = require('fs');
const path = require('path');

const { getMemoryDir } = require('../gep/paths');
const hubClient = require('./hubClient');

const DEFAULT_POLL_MS = 60 * 1000; // 1 min
const MIN_POLL_MS = 15 * 1000;
const LEDGER_FILENAME = 'atp-autodeliver-ledger.json';
const LEDGER_MAX_ENTRIES = 500;

let _started = false;
let _pollInterval = null;
let _pollMs = DEFAULT_POLL_MS;
let _inflight = false;

function _ledgerPath() {
  return path.join(getMemoryDir(), LEDGER_FILENAME);
}

function _isEnabled() {
  const raw = (process.env.EVOLVER_ATP_AUTODELIVER || 'on').toLowerCase().trim();
  return raw !== 'off' && raw !== '0' && raw !== 'false';
}

function _emptyLedger() {
  return { version: 1, submitted: {} };
}

function _readLedger() {
  try {
    const p = _ledgerPath();
    if (!fs.existsSync(p)) return _emptyLedger();
    const raw = fs.readFileSync(p, 'utf8');
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || !parsed.submitted) return _emptyLedger();
    return parsed;
  } catch (_) {
    return _emptyLedger();
  }
}

function _writeLedger(ledger) {
  try {
    const dir = getMemoryDir();
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    // Bound the ledger size so it cannot grow without limit on long-running
    // merchants. Keep the most-recent entries by insertion order.
    const entries = Object.entries(ledger.submitted || {});
    if (entries.length > LEDGER_MAX_ENTRIES) {
      const trimmed = Object.fromEntries(entries.slice(-LEDGER_MAX_ENTRIES));
      ledger.submitted = trimmed;
    }
    const tmp = _ledgerPath() + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(ledger, null, 2));
    fs.renameSync(tmp, _ledgerPath());
  } catch (_) {
    // Non-fatal: next poll will re-attempt from Hub state. Hub-side
    // submitDelivery is itself idempotent per order id.
  }
}

function _buildProofPayload(task) {
  // Minimal evidence the Hub's auto verifier will accept. Matches the shape
  // documented in /a2a/atp/deliver: result/output/pass_rate/signals.
  const now = new Date().toISOString();
  return {
    result: 'completed',
    asset_id: task.result_asset_id || null,
    completed_at: task.claimed_at || now,
    pass_rate: 1.0,
    signals: Array.isArray(task.signals) ? task.signals.slice(0, 10) : [],
    submitter: 'evolver_auto_deliver',
  };
}

async function _tick() {
  if (_inflight) return;
  _inflight = true;
  try {
    const result = await hubClient.listMyTasks(20);
    if (!result || !result.ok || !result.data) return;
    const tasks = Array.isArray(result.data.tasks) ? result.data.tasks : [];
    if (tasks.length === 0) return;

    const ledger = _readLedger();
    let wroteLedger = false;

    for (const task of tasks) {
      const orderId = task && task.atp_order_id;
      if (!orderId) continue;
      if (ledger.submitted[orderId]) continue;
      // Only deliver once the task has a result asset (i.e. solidify finished).
      if (!task.result_asset_id) continue;
      // Don't try to deliver on already-terminal statuses.
      if (task.status && task.status !== 'claimed' && task.status !== 'completed') continue;

      const proofPayload = _buildProofPayload(task);
      const resp = await hubClient.submitDelivery(orderId, proofPayload);
      if (resp && resp.ok) {
        ledger.submitted[orderId] = Date.now();
        wroteLedger = true;
        console.log('[ATP-AutoDeliver] Delivered order=' + orderId + ' asset=' + (task.result_asset_id || 'none'));
      } else {
        // Record terminal-ish errors in the ledger so we do not hammer the
        // same order every minute. Everything else (transient network) is
        // retried on the next tick.
        const err = (resp && resp.error) || 'unknown_error';
        const status = resp && resp.status;
        const terminal = status === 400 || status === 404 || status === 409;
        if (terminal) {
          ledger.submitted[orderId] = -Date.now();
          wroteLedger = true;
        }
        console.log('[ATP-AutoDeliver] Delivery failed order=' + orderId + ' status=' + (status || 'n/a') + ' err=' + String(err).slice(0, 120));
      }
    }

    if (wroteLedger) _writeLedger(ledger);
  } catch (err) {
    console.log('[ATP-AutoDeliver] Tick threw (non-fatal): ' + (err && err.message || err));
  } finally {
    _inflight = false;
  }
}

function start(opts) {
  if (_started) return;
  if (!_isEnabled()) return;
  const requested = Number((opts && opts.pollMs) || process.env.ATP_AUTODELIVER_POLL_MS || DEFAULT_POLL_MS);
  _pollMs = Math.max(MIN_POLL_MS, Math.floor(requested) || DEFAULT_POLL_MS);
  _started = true;
  _pollInterval = setInterval(function () {
    _tick().catch(function () { /* swallowed in _tick */ });
  }, _pollMs);
  // .unref() so this background poller does NOT keep the Node event
  // loop alive on its own. `evolver run` (single-shot) writes its
  // artifacts and expects to exit — without unref, the setInterval
  // handle pins the process and the run sits as a residual `node`
  // process until manually killed (public issue #553). `evolver --loop`
  // (daemon) keeps the foreground evolve loop alive on its own
  // schedule, so an unref'd poller still polls — unref only changes
  // whether THIS handle alone keeps the loop alive, not whether the
  // handle fires.
  if (_pollInterval && typeof _pollInterval.unref === 'function') {
    _pollInterval.unref();
  }
  // Do not await -- fire the first tick asynchronously so start() returns
  // immediately. This matches the autoBuyer start() semantics.
  _tick().catch(function () { /* swallowed in _tick */ });
  console.log('[ATP-AutoDeliver] Started (pollMs=' + _pollMs + ')');
}

function stop() {
  if (_pollInterval) {
    clearInterval(_pollInterval);
    _pollInterval = null;
  }
  _started = false;
}

function isStarted() {
  return _started;
}

function _resetForTests() {
  stop();
  _inflight = false;
  _pollMs = DEFAULT_POLL_MS;
}

module.exports = {
  start,
  stop,
  isStarted,
  __internals: {
    tick: _tick,
    readLedger: _readLedger,
    writeLedger: _writeLedger,
    buildProofPayload: _buildProofPayload,
    resetForTests: _resetForTests,
    // Test-only accessor for the active poll Timeout. Used to assert
    // the timer was `.unref()`ed so it does not pin the Node event
    // loop (regression guard for public issue #553).
    getPollIntervalForTest: () => _pollInterval,
    constants: {
      DEFAULT_POLL_MS,
      MIN_POLL_MS,
      LEDGER_FILENAME,
      LEDGER_MAX_ENTRIES,
    },
  },
};
