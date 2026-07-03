'use strict';

const fs = require('fs');
const path = require('path');
const { PROXY_PROTOCOL_VERSION } = require('../mailbox/store');
const { readMailboxStateFile } = require('../mailbox/state');
const { buildEnvelope } = require('../envelope');
const crypto = require('crypto');
const {
  hubFetch,
  hubUnreachableBackoffMs,
  isHubUnreachableError,
  readHubResponseJson,
  readHubResponseText,
  sanitizeHubResponseForLog,
  throwIfHubUnreachableResponse,
} = require('../../gep/hubFetch');
const { getEvomapPath } = require('../../gep/paths');
// last_update transit (PR #188): proxy heartbeat ferries a pending
// force_update outcome to the hub, then clears the state file on 2xx.
// Proxy DOES run the upgrade now (PR #188 follow-up, HIGH bug): the
// original comment "Proxy itself never runs the upgrade — telemetry-only
// here" reflected pre-fix behaviour. Pure proxy-mode nodes (EVOMAP_PROXY=1,
// no evolve loop) never traversed a2aProtocol.js sendHeartbeat, so the
// canonical `_maybeTriggerForceUpdateFromHeartbeat` block at
// a2aProtocol.js:2304 never fired for them — Hub could push force_update
// forever with no upgrade attempt and no EvolverUpgradeAttempt row. The
// proxy heartbeat (200 with force_update, AND 426 with force_update in the
// error envelope) must mirror that logic. reportForceUpdateOutcome writes
// the state file the next heartbeat will pick up via body.last_update.
const {
  readPendingLastUpdate,
  clearLastUpdateOnAck,
  reportForceUpdateOutcome,
} = require('../../gep/a2aProtocol');

// Hub's nodeId regex; mirror of src/gep/a2aProtocol.js so a malformed
// legacy file can never feed garbage into the hello payload.
const NODE_ID_RE = /^node_[a-f0-9]{12,32}$/;

const DEFAULT_HEARTBEAT_INTERVAL = 360_000;
// Heartbeat backoff ceiling. Was 30min; reporter (#544) showed that
// a single transient failure could park the loop at 30min and feel
// indistinguishable from a daemon that had crashed. 15min sits above
// `DEFAULT_HEARTBEAT_INTERVAL` (6min) so the `interval * 2^failures`
// growth still has headroom — capping below the interval would invert
// the backoff and make failures retry FASTER than success ticks.
// 15min ≈ 2.5× the default, giving one full doubling step before park.
const HEARTBEAT_BACKOFF_CAP_MS = 15 * 60_000;
const HELLO_TIMEOUT = 15_000;
const HEARTBEAT_TIMEOUT = 10_000;
const MAX_REAUTH_ATTEMPTS = 2;
// First failure = 2 min, subsequent consecutive failures double up to ~4h.
// Aligned with a2aProtocol.js Round-9 reduction (was 30 min, caused
// "idle-death" for proxy-mode users: one benign 401 silenced the node for 30
// min, triggering stagnation kills and manual restart loops).
const REAUTH_BACKOFF_BASE_MS = 2 * 60_000;
const REAUTH_BACKOFF_MAX_MS = 4 * 60 * 60_000;

// Wall-clock drift detector tunables. Mirrors DRIFT_CHECK_MS /
// DRIFT_SLEEP_THRESHOLD_MS / DRIFT_LONG_SLEEP_THRESHOLD_MS in
// src/gep/a2aProtocol.js. setTimeout / setInterval fire on libuv's
// monotonic clock, which freezes while the host is suspended -- so a
// laptop closed for hours and reopened would not trigger any heartbeat
// tick until the next scheduled time, which under exponential backoff
// can sit at HEARTBEAT_BACKOFF_CAP_MS (15 min). Sampling Date.now()
// (wall clock) every DRIFT_CHECK_MS lets us detect the jump and
// immediately poke the heartbeat so recovery does not have to wait for
// the next natural tick. Long-sleep gap also clears reauth backoff:
// hub-side state we cached is almost certainly stale after a 30min+
// suspend, so force a clean retry path on wake instead of carrying the
// pre-sleep penalty through. R10 (#544).
const DRIFT_CHECK_MS = 30 * 1000;
const DRIFT_SLEEP_THRESHOLD_MS = 90 * 1000;
const DRIFT_LONG_SLEEP_THRESHOLD_MS = 30 * 60_000;

// Heartbeat-driven force_update lifecycle tracking. Mirrors
// `_forceUpdateInFlight` / `_forceUpdateLastAttemptAt` /
// `_getForceUpdateRetryCooldownMs` in src/gep/a2aProtocol.js so the proxy
// path uses the same in-flight + cooldown contract as the canonical path.
// Module-level (not instance-level) so multiple LifecycleManager instances
// in the same process serialize through one upgrade attempt — matches
// a2aProtocol.js's module-level guard. Process-local is sufficient: the
// proxy daemon runs in a single process and any sibling process would
// have its own require-cached state; cross-process serialization is the
// hub's job via directive_id dedup, not the client's.
let _proxyForceUpdateInFlight = false;
let _proxyForceUpdateLastAttemptAt = 0;
function _getProxyForceUpdateRetryCooldownMs() {
  // Share the env var with a2aProtocol.js: an operator who sets
  // EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS=0 in a test or production tune
  // expects BOTH code paths to honour it. Default 15min matches
  // a2aProtocol.js exactly.
  const v = Number(process.env.EVOLVER_FORCE_UPDATE_RETRY_COOLDOWN_MS);
  if (Number.isFinite(v) && v >= 0) return v;
  return 15 * 60 * 1000;
}

let _cachedFingerprint = null;
function _getEnvFingerprint() {
  if (_cachedFingerprint) return _cachedFingerprint;
  try {
    const { captureEnvFingerprint } = require('../../gep/envFingerprint');
    _cachedFingerprint = captureEnvFingerprint();
  } catch {
    _cachedFingerprint = {
      platform: process.platform,
      arch: process.arch,
      node_version: process.version,
    };
  }
  return _cachedFingerprint;
}

// Recover a node_id persisted by the legacy GEP path
// (`src/gep/a2aProtocol.js` writes ~/.evomap/node_id, falling back to
// `<install>/.evomap_node_id` when the home dir isn't writable). Without
// this fallback, a daemon whose MailboxStore was created AFTER the legacy
// GEP file (any install upgrading from pre-lifecycle to lifecycle, or any
// state.json wiped without also wiping the legacy file) mints a fresh
// `node_${randomBytes(6)}` identity in hello(), which the hub registers
// as a *new* A2ANode under the same owner — the original (with stake,
// reputation, aliases) gets silently abandoned. Mirror the writer's two
// candidates in the same order as `_loadPersistedNodeId` so both code
// paths land on the single identity.
//
// Resolve both paths on every call:
//   - getEvomapPath() reads EVOLVER_HOME (and falls through to os.homedir())
//     at call time, so tests and privileged-drop daemons can flip the
//     resolved location without monkey-patching globals.
//   - The install-root path uses __dirname so it's stable across cwd changes.
function _readLegacyNodeId() {
  const candidates = [
    getEvomapPath('node_id'),
    path.resolve(__dirname, '..', '..', '..', '.evomap_node_id'),
  ];
  for (const file of candidates) {
    try {
      if (!fs.existsSync(file)) continue;
      const raw = fs.readFileSync(file, 'utf8').trim();
      if (NODE_ID_RE.test(raw)) return raw;
    } catch {
      // Unreadable / racing writer — try the next location.
    }
  }
  return null;
}

// Mirror of src/gep/a2aProtocol.js `_persistNodeId`. Pure-proxy daemons
// (EVOMAP_PROXY=1, no a2aProtocol heartbeat thread) mint their own
// node_id and ONLY persist it to MailboxStore state.json. The legacy
// `~/.evomap/node_id` file never gets written, so:
//
//   1. `_shortNodeIdForStatePath` in a2aProtocol.js (used by the proxy
//      heartbeat to pick the per-node `force_update_last.<suffix>.json`
//      path) falls all the way through to 'anon' — every proxy node on
//      the same EVOLVER_HOME would collide on the same state file.
//   2. A mixed-mode install (legacy evolve loop ran once, then user
//      switched to proxy mode) is even worse: the legacy file holds a
//      DIFFERENT id than the one in MailboxStore. The proxy heartbeats
//      with body.node_id = its OWN id while writing
//      `force_update_last.<legacy-suffix>.json`. The hub-side upgrade
//      attempt row gets attributed to the wrong node.
//
// Calling this helper from hello() after the nodeId is resolved unifies
// the two persistence paths onto a single identity. Atomic write
// (per-pid tmp + rename) mirrors `_persistNodeSecret` in a2aProtocol.js;
// 0o600 mode keeps the file owner-read-only on POSIX (silently ignored
// on Windows, where %USERPROFILE% isolation is the only protection).
//
// Idempotent: if the file already holds the same id, we skip the write
// to avoid an inode churn on every hello tick. If it holds a DIFFERENT
// valid id, we still overwrite — the proxy's MailboxStore wins because
// that is the id the hub already knows us by (any rotation away from
// the legacy id was a deliberate operator action). The only way to
// re-seed a legacy id back onto a proxy install is to clear
// MailboxStore state.json (`evolver reset-local-secret`).
function _persistLegacyNodeId(id) {
  if (!id || !NODE_ID_RE.test(id)) return;
  const targets = [
    getEvomapPath('node_id'),
    path.resolve(__dirname, '..', '..', '..', '.evomap_node_id'),
  ];
  // Try targets in order until one succeeds, matching the read order in
  // _readLegacyNodeId. We only need ONE persistent copy; once the home
  // path takes the write, the install-root path is unused.
  for (const file of targets) {
    try {
      // Skip if the file already matches — common steady-state path,
      // saves a syscall storm under heartbeat backoff doubling.
      try {
        if (fs.existsSync(file)) {
          const existing = fs.readFileSync(file, 'utf8').trim();
          if (existing === id) return;
        }
      } catch {
        // Unreadable -- treat as missing and try to write.
      }
      const dir = path.dirname(file);
      try {
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
        }
      } catch (_) {
        // mkdir failed (read-only fs, EPERM under sandboxing). Skip
        // this candidate; the next one (install-root .evomap_node_id)
        // may still work.
        continue;
      }
      // Atomic write: a sibling evolver process (mixed-mode upgrade, two
      // proxy daemons started by hand) could otherwise race on this
      // path and leave a half-written file. Matches the pattern in
      // a2aProtocol.js `_persistNodeSecret`.
      const tmp = file + '.' + process.pid + '.tmp';
      fs.writeFileSync(tmp, id, { encoding: 'utf8', mode: 0o600 });
      fs.renameSync(tmp, file);
      return;
    } catch {
      // Best-effort: continue to the next candidate. If both fail (no
      // home, no writable install root) we accept the legacy file is
      // unavailable — the proxy will still function, it just cannot
      // unify state-file suffixes with a co-resident a2aProtocol path.
    }
  }
}

// Heartbeat-driven force_update trigger for proxy-mode nodes. Mirrors
// `_maybeTriggerForceUpdateFromHeartbeat` in src/gep/a2aProtocol.js
// (search there for that name to compare). Pure proxy-mode deployments
// (EVOMAP_PROXY=1) never run the evolve run() loop or sendHeartbeat, so
// without this trigger Hub can push force_update on every heartbeat
// forever and the node will keep heartbeating on the old version — which
// is exactly what shipped before PR #188's H1 fix.
//
// Drives `executeForceUpdate` directly, gated by an in-flight lock + a
// cooldown on failures so we do not hammer npm/degit on every tick. After
// the attempt, persists the outcome via `reportForceUpdateOutcome` so the
// next heartbeat carries it as body.last_update — that's the path that
// finally writes a row to the hub's EvolverUpgradeAttempt table.
//
// Logger is injected (not a console fallback) so tests can capture the
// upgrade-path stderr without polluting CI output. The logger contract
// matches what the LifecycleManager already uses.
function _maybeTriggerForceUpdateFromHeartbeat(forceUpdate, logger) {
  if (!forceUpdate || typeof forceUpdate !== 'object') return;
  if (_proxyForceUpdateInFlight) return;
  const nowMs = Date.now();
  if (
    _proxyForceUpdateLastAttemptAt &&
    (nowMs - _proxyForceUpdateLastAttemptAt) < _getProxyForceUpdateRetryCooldownMs()
  ) {
    // A recent attempt already ran and either succeeded (process exited
    // and we wouldn't be here on the post-restart heartbeat — see the
    // FORCE_UPDATE_NOOP path in forceUpdate.js / reportForceUpdateOutcome
    // status="skipped") or failed. Back off.
    return;
  }
  _proxyForceUpdateInFlight = true;
  _proxyForceUpdateLastAttemptAt = nowMs;

  // Capture from_version BEFORE executeForceUpdate runs. A successful
  // upgrade calls process.exit(78); the post-restart heartbeat reads the
  // state file from a fresh process where require('package.json').version
  // is the NEW version — so snapshot the CURRENTLY running version now.
  let fromVersion = '';
  try {
    fromVersion = String((require('../../../package.json') || {}).version || '');
  } catch (_) { /* best-effort */ }

  // Kick off in a microtask so the heartbeat promise chain can still
  // complete (log + return {ok:true}) before the long-running upgrade
  // takes over the process. Matches a2aProtocol.js exactly.
  Promise.resolve().then(() => {
    let updated = false;
    let noop = false;
    let busy = false;
    let thrownErr = null;
    // Structured failure object ({ ok:false, code, detail }) when the upgrader
    // RETURNED a failure; forwarded to reportForceUpdateOutcome so the hub gets
    // the precise branch code instead of "executeForceUpdate returned false".
    // Hoisted out of the try because `result` is block-scoped there.
    let failureResult = null;
    try {
      const mod = require('../../forceUpdate');
      const result = mod.executeForceUpdate(forceUpdate);
      // Sentinel === comparison: executeForceUpdate returns the
      // FORCE_UPDATE_NOOP symbol when the install is already at the
      // required version. We must NOT treat that as "success" — doing so
      // would (a) write a phantom {status:"success", from==to} row to
      // EvolverUpgradeAttempt, and (b) trigger an exit(78) restart with
      // nothing to restart for. The hub schema accepts status="skipped".
      noop = (result === mod.FORCE_UPDATE_NOOP);
      // FORCE_UPDATE_BUSY: another caller (e.g. a2aProtocol heartbeat
      // trigger or an evolve tick) already holds the module-level
      // _inFlight mutex in forceUpdate.js. Defensive only — the
      // instance-level _proxyForceUpdateInFlight gate above and the
      // single-caller property of pure proxy mode make BUSY unreachable
      // in practice. If it does fire (mixed-mode regression, future
      // additional caller, etc.), the other caller owns the telemetry:
      // we MUST NOT write a state file or exit(78). Mirrors
      // src/gep/a2aProtocol.js (search FORCE_UPDATE_BUSY).
      busy = (result === mod.FORCE_UPDATE_BUSY);
      updated = (result === true);
      // Inline the failure-shape check rather than calling mod.isForceUpdateFailure:
      // keeps this robust against partial test mocks of forceUpdate that stub
      // executeForceUpdate but omit the helper (a missing-function throw here
      // would otherwise demote a real success to "failed").
      failureResult = (result && typeof result === 'object' && result.ok === false) ? result : null;
    } catch (e) {
      thrownErr = e;
      try {
        logger.warn(`[ForceUpdate] proxy heartbeat-trigger failed (non-fatal): ${e && e.message || e}`);
      } catch (_) { /* logger broken; non-fatal */ }
      updated = false;
    } finally {
      _proxyForceUpdateInFlight = false;
    }
    if (busy) {
      _proxyForceUpdateLastAttemptAt = 0;
      try {
        logger.log('[ForceUpdate] proxy heartbeat-trigger observed BUSY (concurrent invocation). Skipping telemetry; in-flight caller owns the outcome.');
      } catch (_) { /* logger broken; non-fatal */ }
      return;
    }
    // Persist outcome via the shared helper so the heartbeat-thread
    // trigger and the proxy trigger stay in lockstep on payload assembly
    // + validation. The next heartbeat reads this file and ferries it as
    // body.last_update — same contract as the canonical path.
    try {
      reportForceUpdateOutcome(forceUpdate, {
        updated: updated,
        noop: noop,
        error: thrownErr,
        failure: failureResult,
        fromVersion: fromVersion,
      });
    } catch (e) {
      try {
        logger.warn(`[ForceUpdate] proxy reportForceUpdateOutcome failed (non-fatal): ${e && e.message || e}`);
      } catch (_) { /* logger broken; non-fatal */ }
    }
    if (updated) {
      try { logger.log('[ForceUpdate] Update complete (proxy heartbeat-trigger). Exiting for restart...'); } catch (_) {}
      try { process.exit(78); } catch (_) {}
    } else if (noop) {
      _proxyForceUpdateLastAttemptAt = 0;
      try {
        logger.log('[ForceUpdate] No-op (proxy heartbeat-trigger): already at required version. Skipping restart.');
      } catch (_) {}
    } else {
      try {
        logger.warn('[ForceUpdate] proxy heartbeat-trigger failed. Will retry after cooldown (' +
          Math.round(_getProxyForceUpdateRetryCooldownMs() / 60000) + 'min).');
      } catch (_) {}
    }
  });
}

class AuthError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = 'AuthError';
    this.statusCode = statusCode;
  }
}

function parseNodeSecretVersion(value) {
  const n = Number(value);
  return Number.isInteger(n) && n > 0 ? n : null;
}

const NODE_SECRET_RE = /^[a-f0-9]{64}$/i;
const NODE_SECRET_SUPPRESSION_RE = /^sha256:[a-f0-9]{64}$/i;
const SECRET_DIVERGENCE_ERROR = 'secret_diverged_cleared';
const SECRET_DIVERGENCE_REASON_CODES = [
  'node_secret_invalid',
  'invalid_secret',
  'rotation_requires_current_secret',
];

function validNodeSecret(value) {
  return typeof value === 'string' && NODE_SECRET_RE.test(value);
}

function getEnvNodeSecret() {
  return ((process.env.A2A_NODE_SECRET || process.env.EVOMAP_NODE_SECRET || '').trim() || null);
}

function fingerprintNodeSecret(secret) {
  if (!validNodeSecret(secret)) return null;
  const normalized = String(secret).trim().toLowerCase();
  return 'sha256:' + crypto.createHash('sha256').update(normalized).digest('hex');
}

function truthyState(value) {
  const v = String(value || '').trim().toLowerCase();
  return v === '1' || v === 'true' || v === 'yes' || v === 'on';
}

function matchSecretDivergenceReason(value) {
  const reason = String(value || '').trim().toLowerCase();
  if (!reason) return null;
  return SECRET_DIVERGENCE_REASON_CODES.find((code) => reason.includes(code)) || null;
}

function extractSecretDivergenceReason(data) {
  const candidates = [
    data?.payload?.reason,
    data?.payload?.error,
    data?.reason,
    data?.error,
  ];
  for (const value of candidates) {
    const reason = matchSecretDivergenceReason(value);
    if (reason) return reason;
  }
  return null;
}

function isSecretDivergenceError(error) {
  return error === SECRET_DIVERGENCE_ERROR || Boolean(matchSecretDivergenceReason(error));
}

function safeHubErrorCode(data, statusCode) {
  const candidates = [
    data?.error,
    data?.reason,
    data?.payload?.error,
    data?.payload?.reason,
  ];
  for (const value of candidates) {
    if (typeof value !== 'string') continue;
    const code = value.trim();
    if (/^[a-z][a-z0-9_:-]{0,79}$/i.test(code)) return code;
  }
  return `http_${statusCode}`;
}

function normalizeNodeSecretEnvSuppression(value) {
  const raw = String(value || '').trim();
  if (!raw) return null;
  if (truthyState(raw)) return 'true';
  const lower = raw.toLowerCase();
  return NODE_SECRET_SUPPRESSION_RE.test(lower) ? lower : null;
}

class LifecycleManager {
  constructor({ hubUrl, store, logger, getTaskMeta } = {}) {
    this.hubUrl = (hubUrl || process.env.A2A_HUB_URL || '').replace(/\/+$/, '');
    this.store = store;
    this.logger = logger || console;
    this.getTaskMeta = getTaskMeta || null;
    this._heartbeatTimer = null;
    this._running = false;
    this._startedAt = null;
    this._lastHeartbeatTickAt = 0;
    this._consecutiveFailures = 0;
    this._reauthInProgress = false;
    this._helloRateLimitUntil = 0;
    this._reauthBackoffUntil = 0;
    this._consecutiveReauthFailures = 0;
    this._driftInterval = null;
    this._lastDriftCheckAt = 0;
    this._hubUnreachableFailures = 0;
    this._hubUnreachableUntil = 0;
    this._envSecretSuppressionMarker = normalizeNodeSecretEnvSuppression(this.store && this.store.getState
      ? this.store.getState('node_secret_env_suppressed')
      : null);
    this._envSuppressionClearedForSecret = null;
    this._suppressEnvSecret = Boolean(this._envSecretSuppressionMarker && getEnvNodeSecret());

    // H4 fix: persist the legacy node_id file as soon as the in-memory
    // node_id is known, NOT only after a successful hello(). The original
    // code persisted only in hello() (see ~L390-398) — but proxy-mode boot
    // can fire `reportForceUpdateOutcome` BEFORE hello() returns:
    //
    //   - First-tick heartbeat hits 426 → executeForceUpdate() → exit(78)
    //     all happens BEFORE the hello() response is processed.
    //   - enrich.js force_update path can fire during the same window.
    //
    // `_shortNodeIdForStatePath` in a2aProtocol.js then picks the
    // state-file suffix from `_cachedNodeId` (never set in proxy mode —
    // only getNodeId() sets it, and proxy never calls getNodeId()) or the
    // legacy ~/.evomap/node_id file. With both empty, it falls through
    // to 'anon', and the outcome lands at `force_update_last.anon.json`.
    // Next boot's hello() writes the real id, the heartbeat reads
    // `force_update_last.<8hex>.json`, the anon file is orphaned and the
    // outcome is silently lost.
    //
    // Persisting at construction closes the window. _persistLegacyNodeId
    // early-returns on invalid input (NODE_ID_RE gate, same regex as the
    // hello() path uses) so a malformed/empty store value is a no-op,
    // and it is idempotent on matching content so the cost is one
    // existsSync + one readFileSync per construction. We keep the
    // existing post-hello call as a safety net in case hello() mints or
    // mutates the id.
    try {
      const earlyNodeId = this.store && this.store.getState
        ? this.store.getState('node_id')
        : null;
      if (earlyNodeId && NODE_ID_RE.test(earlyNodeId)) {
        _persistLegacyNodeId(earlyNodeId);
      }
    } catch (e) {
      // Best-effort: persistence failure must never break construction.
      // Logger may not exist if tests passed undefined; guard the call.
      try {
        this.logger.warn(
          `[lifecycle] early persist of legacy node_id failed (non-fatal): ${e && e.message || e}`
        );
      } catch (_) { /* logger broken; non-fatal */ }
    }
  }

  get nodeId() {
    return this.store.getState('node_id');
  }

  get nodeSecret() {
    return this._resolveNodeSecret();
  }

  get nodeSecretVersion() {
    this._resolveNodeSecret();
    const storeVersion = parseNodeSecretVersion(this.store.getState('node_secret_version'));
    const storeSecret = this.store.getState('node_secret') || null;
    const storeSource = this.store.getState('node_secret_source') || null;
    const envSecret = this._effectiveEnvNodeSecret();
    const envVersion = parseNodeSecretVersion(process.env.A2A_NODE_SECRET_VERSION || process.env.EVOMAP_NODE_SECRET_VERSION);
    const validStoreSecret = validNodeSecret(storeSecret);
    if (this._suppressEnvSecret) return validStoreSecret ? storeVersion : null;
    if (storeSource === 'hub_rotate' && validStoreSecret) return storeVersion;
    if (envSecret) {
      if (envVersion) return envVersion;
      return storeSecret === envSecret ? storeVersion : null;
    }
    return validStoreSecret ? storeVersion : null;
  }

  /**
   * Resolve the active node_secret with conflict reconciliation between the
   * persistent MailboxStore and `process.env.A2A_NODE_SECRET`.
   *
   * Two opposite failure modes shape this logic:
   *
   *   #529 (env-fresh, store-stale): operator exports a freshly minted
   *     secret in A2A_NODE_SECRET (e.g. from .env), but the MailboxStore
   *     still holds a long-stale value. The store value would otherwise
   *     win and produce a 403 -> rotate -> 30-min backoff loop.
   *
   *   "store-fresh, env-stale": process A rotates the secret via /a2a/hello,
   *     so the store holds the value the hub now recognises. Process A then
   *     restarts (typical: daemon respawn after upgrade or crash). The shell
   *     it inherits its env from still exports the *previous* value of
   *     A2A_NODE_SECRET. Without source-tracking we would treat this as
   *     env-vs-store conflict, env-wins, and silently overwrite the
   *     hub-recognised secret with a stale shell value -- exactly the loop
   *     #529 was meant to fix, just symmetrical.
   *
   * Resolution: track *who wrote* the store value. When the hub returns a
   * rotated secret (`hello`), we tag the store entry with
   * `node_secret_source = 'hub_rotate'`. On conflict we honour that tag:
   *
   *   source=hub_rotate -> store wins (recent rotation; env is stale)
   *   source missing/'env_seed' -> env wins (legacy / first-boot bootstrap)
   *
   * Single-source mode (only one of store/env present) is unchanged.
   * @returns {string|null}
   */
  _resolveNodeSecret() {
    const envSecret = this._effectiveEnvNodeSecret();
    const envUpdatedAfterSuppression = this._envSuppressionClearedForSecret === envSecret;
    const storeSecret = this.store.getState('node_secret') || null;
    const storeSource = this.store.getState('node_secret_source') || null;

    if (
      envSecret &&
      envUpdatedAfterSuppression &&
      validNodeSecret(envSecret) &&
      (!storeSecret || envSecret === storeSecret) &&
      !(storeSecret && envSecret === storeSecret && storeSource === 'hub_rotate')
    ) {
      this._syncEnvNodeSecretToStore(envSecret);
      return envSecret;
    }

    if (envSecret && storeSecret && envSecret !== storeSecret) {
      // Store value came from a successful hub rotation -> trust it.
      // The env var is necessarily stale: it was captured by the parent
      // shell before the rotation and a child process cannot mutate it
      // back into its parent.
      if (storeSource === 'hub_rotate' && validNodeSecret(storeSecret) && !envUpdatedAfterSuppression) {
        if (!this._storeSourceLogged) {
          this._storeSourceLogged = true;
          this.logger.warn(
            '[lifecycle] A2A_NODE_SECRET env var differs from MailboxStore; ' +
              'store value originated from a hub rotation, treating env as stale. ' +
              'After a manual web reset, run `evolver reset-local-secret` to clear local ' +
              'secret and env suppression state before relying only on updated env vars.'
          );
        }
        return storeSecret;
      }
      if (validNodeSecret(envSecret)) {
        const diskRotated = this._latestDiskHubRotatedSecret();
        if (diskRotated) {
          this._setNodeSecretState({
            secret: diskRotated.secret,
            version: diskRotated.version ? String(diskRotated.version) : '',
            source: 'hub_rotate',
            envSuppressed: this.store.getState('node_secret_env_suppressed') || '',
          });
          if (!this._storeSourceLogged) {
            this._storeSourceLogged = true;
            this.logger.warn(
              '[lifecycle] MailboxStore memory differs from disk hub-rotated node_secret; ' +
                'using disk value and treating env as stale.'
            );
          }
          return diskRotated.secret;
        }
        this._syncEnvNodeSecretToStore(envSecret);
        if (!this._envOverrideLogged) {
          this._envOverrideLogged = true;
          this.logger.warn(
            '[lifecycle] A2A_NODE_SECRET env var differs from MailboxStore; using env value and syncing store. ' +
              'Clear ~/.evomap/mailbox/state.json or unset A2A_NODE_SECRET to silence this warning.'
          );
        }
        return envSecret;
      }
      // env var malformed -- ignore it, fall back to store
      return storeSecret;
    }

    return storeSecret || envSecret || null;
  }

  _latestDiskHubRotatedSecret() {
    const file = this.store && this.store._stateFile;
    if (!file) return null;
    const state = readMailboxStateFile(file);
    const secret = typeof state?.node_secret === 'string' ? state.node_secret.trim() : null;
    if (!validNodeSecret(secret) || state?.node_secret_source !== 'hub_rotate') return null;
    return {
      secret,
      version: parseNodeSecretVersion(state.node_secret_version),
    };
  }

  _syncEnvNodeSecretToStore(envSecret) {
    const envVersion = parseNodeSecretVersion(process.env.A2A_NODE_SECRET_VERSION || process.env.EVOMAP_NODE_SECRET_VERSION);
    this._setNodeSecretState({
      secret: envSecret,
      version: envVersion ? String(envVersion) : '',
      source: 'env_seed',
      envSuppressed: '',
    });
    this._clearEnvSecretSuppression();
  }

  _setNodeSecretState({ secret = '', version = '', source = '', envSuppressed = '' } = {}) {
    if (this.store && typeof this.store.setNodeSecretState === 'function') {
      this.store.setNodeSecretState({ secret, version, source, envSuppressed });
      return;
    }
    this.store.setState('node_secret', secret);
    this.store.setState('node_secret_version', version ? String(version) : '');
    this.store.setState('node_secret_source', source);
    this.store.setState('node_secret_env_suppressed', envSuppressed);
  }

  _effectiveEnvNodeSecret() {
    const envSecret = getEnvNodeSecret();
    return this._isEnvNodeSecretSuppressed(envSecret) ? null : envSecret;
  }

  _isEnvNodeSecretSuppressed(envSecret) {
    this._envSuppressionClearedForSecret = null;
    const persistedMarker = normalizeNodeSecretEnvSuppression(this.store && this.store.getState
      ? this.store.getState('node_secret_env_suppressed')
      : null);
    const marker = persistedMarker || this._envSecretSuppressionMarker;
    if (!marker) {
      this._envSecretSuppressionMarker = null;
      this._suppressEnvSecret = false;
      return false;
    }
    this._envSecretSuppressionMarker = marker;
    if (marker === 'true') {
      this._suppressEnvSecret = Boolean(envSecret);
      return Boolean(envSecret);
    }
    const envFingerprint = fingerprintNodeSecret(envSecret);
    if (!envFingerprint) {
      this._suppressEnvSecret = false;
      return false;
    }
    if (envFingerprint === marker) {
      this._suppressEnvSecret = true;
      return true;
    }
    this._clearEnvSecretSuppression();
    this._envSuppressionClearedForSecret = envSecret;
    return false;
  }

  _markCurrentEnvSecretSuppressed() {
    const marker = fingerprintNodeSecret(getEnvNodeSecret());
    if (!marker) {
      this._clearEnvSecretSuppression();
      return;
    }
    try { this.store.setState('node_secret_env_suppressed', marker); } catch { /* best-effort */ }
    this._envSecretSuppressionMarker = marker;
    this._suppressEnvSecret = true;
  }

  _clearEnvSecretSuppression() {
    try { this.store.setState('node_secret_env_suppressed', ''); } catch { /* best-effort */ }
    this._envSecretSuppressionMarker = null;
    this._suppressEnvSecret = false;
  }

  _buildHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    const secret = this.nodeSecret;
    if (secret) headers['Authorization'] = 'Bearer ' + secret;
    const secretVersion = this.nodeSecretVersion;
    if (secretVersion) headers['X-EvoMap-Node-Secret-Version'] = String(secretVersion);
    headers['x-correlation-id'] = crypto.randomUUID();
    return headers;
  }

  _hubUnreachableWaitMs() {
    return Math.max(0, this._hubUnreachableUntil - Date.now());
  }

  _recordHubReachable() {
    this._hubUnreachableFailures = 0;
    this._hubUnreachableUntil = 0;
  }

  _recordHubUnreachable(err) {
    this._hubUnreachableFailures += 1;
    const retryAfterMs = hubUnreachableBackoffMs(this._hubUnreachableFailures);
    this._hubUnreachableUntil = Date.now() + retryAfterMs;
    this.logger.warn?.(
      `[lifecycle] Hub unreachable; backing off for ${Math.ceil(retryAfterMs / 1000)}s: ` +
        `${err && err.message || err}`
    );
    return retryAfterMs;
  }

  async hello({ rotateSecret = false } = {}) {
    if (!this.hubUrl) return { ok: false, error: 'no_hub_url' };

    if (this._helloRateLimitUntil > Date.now()) {
      const waitSec = Math.ceil((this._helloRateLimitUntil - Date.now()) / 1000);
      this.logger.warn(`[lifecycle] hello suppressed: rate limited for ${waitSec}s`);
      return { ok: false, error: 'hello_rate_limit_active', waitSec };
    }

    const waitMs = this._hubUnreachableWaitMs();
    if (waitMs > 0) {
      return {
        ok: false,
        error: 'hub_unreachable_backoff',
        retryAfterMs: waitMs,
      };
    }

    const endpoint = `${this.hubUrl}/a2a/hello`;
    const nodeId = this.store.getState('node_id')
      || _readLegacyNodeId()
      || `node_${crypto.randomBytes(6).toString('hex')}`;

    const payload = { capabilities: {} };
    if (rotateSecret) payload.rotate_secret = true;

    const fp = _getEnvFingerprint();

    const body = {
      ...buildEnvelope('hello', payload, nodeId),
      env_fingerprint: fp,
    };

    try {
      const res = await hubFetch(endpoint, {
        method: 'POST',
        headers: this._buildHeaders(),
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(HELLO_TIMEOUT),
      });
      await throwIfHubUnreachableResponse(res, 'lifecycle hello');
      this._recordHubReachable();
      if (!res.ok) {
        const errText = await readHubResponseText(res).catch(() => '');
        let errData = {};
        try { errData = errText ? JSON.parse(errText) : {}; } catch (_) { /* non-JSON API error */ }
        const errMsg = safeHubErrorCode(errData, res.status);
        if (res.status === 429) {
          const retryAfter = parseInt(res.headers.get('retry-after') || '3600', 10);
          this._helloRateLimitUntil = Date.now() + retryAfter * 1000;
          this.logger.error(`[lifecycle] hello rate limited (429): retry after ${retryAfter}s`);
          return { ok: false, error: 'hello_rate_limited', retryAfter };
        }
        const divergenceReason = (res.status === 401 || res.status === 403)
          ? extractSecretDivergenceReason(errData)
          : null;
        if (divergenceReason) {
          this.logger.warn(
            `[lifecycle] hello rejected secret rotation (${res.status}, reason=${divergenceReason}); ` +
              'local secret divergence detected'
          );
          return {
            ok: false,
            error: SECRET_DIVERGENCE_ERROR,
            reason: divergenceReason,
            statusCode: res.status,
          };
        }
        const safeErrText = errText ? sanitizeHubResponseForLog(errText) : errMsg;
        this.logger.error(`[lifecycle] hello HTTP ${res.status}: ${safeErrText}`);
        return { ok: false, error: errMsg, statusCode: res.status };
      }

      const data = await readHubResponseJson(res);

      if (data?.payload?.status === 'rejected') {
        const divergenceReason = extractSecretDivergenceReason(data);
        if (divergenceReason) {
          this.logger.warn(
            `[lifecycle] hello rejected secret rotation (reason=${divergenceReason}); ` +
              'local secret divergence detected'
          );
          return {
            ok: false,
            error: SECRET_DIVERGENCE_ERROR,
            reason: divergenceReason,
            response: data,
          };
        }
        const reason = data.payload.reason || 'unknown';
        const safeReason = sanitizeHubResponseForLog(reason);
        this.logger.error(`[lifecycle] hello rejected: ${safeReason}`);
        const error = String(reason || '').startsWith('node_id_already_claimed')
          ? reason
          : 'hello_rejected';
        return { ok: false, error, response: data };
      }

      const secret = data?.payload?.node_secret || data?.node_secret || null;
      const secretVersion = parseNodeSecretVersion(data?.payload?.node_secret_version || data?.node_secret_version);
      if (secret && validNodeSecret(secret)) {
        // Hub just handed us a fresh secret. Whatever sits in
        // A2A_NODE_SECRET is now older than the store, so suppress the
        // env-wins reconciliation in _resolveNodeSecret for the rest of
        // this process. Without this, the very next _buildHeaders call
        // (e.g. the verification heartbeat in reAuthenticate) would see
        // env vs store as a conflict, treat the env value as authoritative,
        // and overwrite the freshly rotated secret with the stale one,
        // re-creating the auth loop the previous patch fixed (see #529
        // and the Bugbot review on PR #22).
        if (getEnvNodeSecret() && getEnvNodeSecret() !== secret) {
          this._markCurrentEnvSecretSuppressed();
        } else {
          this._clearEnvSecretSuppression();
        }
        this._setNodeSecretState({
          secret,
          version: secretVersion ? String(secretVersion) : '',
          source: 'hub_rotate',
          envSuppressed: this.store.getState('node_secret_env_suppressed') || '',
        });
        this.logger.log('[lifecycle] new node_secret stored from hello response');
      } else if (secretVersion) {
        this.store.setState('node_secret_version', String(secretVersion));
      } else {
        this.store.setState('node_secret_version', '');
      }

      this.store.setState('node_id', nodeId);
      // Unify proxy node_id with the legacy GEP file. Without this, the
      // proxy-only fast path (EVOMAP_PROXY=1) never seeds
      // ~/.evomap/node_id and `_shortNodeIdForStatePath` in a2aProtocol
      // (used to pick the per-node `force_update_last.<suffix>.json`
      // path for upgrade telemetry) falls through to 'anon' — every
      // proxy node under the same EVOLVER_HOME would collide on the
      // same state file. In a mixed-mode install where the legacy file
      // holds a DIFFERENT (stale) id, the helper overwrites it so the
      // state-file suffix matches `this.nodeId` — the id the hub sees
      // in body.node_id. We persist AFTER hello succeeds so a rejected
      // first-boot mint never commits to disk; on a rejection the next
      // tick will mint fresh again (existing behaviour).
      try {
        _persistLegacyNodeId(nodeId);
      } catch (e) {
        // Best-effort: persistence failure must never break hello. Log
        // and move on — the proxy still functions, the state-file
        // suffix just falls back to 'anon' until the next successful
        // hello retries the write.
        this.logger.warn(`[lifecycle] failed to persist legacy node_id (non-fatal): ${e && e.message || e}`);
      }
      this.logger.log(`[lifecycle] hello OK, node_id=${nodeId}${rotateSecret ? ' (secret rotated)' : ''}`);
      return { ok: true, nodeId, response: data };
    } catch (err) {
      if (isHubUnreachableError(err)) {
        const retryAfterMs = this._recordHubUnreachable(err);
        return {
          ok: false,
          error: 'hub_unreachable',
          detail: err.message,
          retryAfterMs,
        };
      }
      this.logger.error(`[lifecycle] hello failed: ${err.message}`);
      return { ok: false, error: err.message };
    }
  }

  /**
   * Re-authenticate after 403: rotate secret via hello, then verify with a
   * heartbeat. Returns true if auth is restored, false otherwise.
   *
   * Recovery sequence (issue EvoMap/evolver#529):
   *   attempt 1 -> hello with current Bearer + rotate_secret=true
   *                (works when the stale secret is still recognised)
   *   attempt 2 -> drop the bearer locally, hello WITHOUT Authorization
   *                + rotate_secret=true. If the node is owned by someone
   *                else, hub returns node_id_already_claimed; we surface a
   *                manual-reset hint to the user instead of churning forever.
   */
  async reAuthenticate() {
    if (this._reauthInProgress) return false;
    if (this._reauthBackoffUntil > Date.now()) {
      const waitSec = Math.ceil((this._reauthBackoffUntil - Date.now()) / 1000);
      this.logger.warn(`[lifecycle] re-auth suppressed: backoff active for ${waitSec}s`);
      return false;
    }
    this._reauthInProgress = true;
    let manualResetRequired = false;
    let hubUnreachable = false;
    let droppedDivergedSecret = false;
    try {
      for (let attempt = 1; attempt <= MAX_REAUTH_ATTEMPTS; attempt++) {
        this.logger.warn(`[lifecycle] re-auth attempt ${attempt}/${MAX_REAUTH_ATTEMPTS}: rotating secret via hello...`);
        const helloResult = await this.hello({ rotateSecret: true });
        if (!helloResult.ok) {
          this.logger.error(`[lifecycle] re-auth hello failed: ${helloResult.error}`);
          if (helloResult.error === 'hello_rate_limited' || helloResult.error === 'hello_rate_limit_active') break;
          // Hub link is down (WAF HTML, network error, timeout) -- NOT an auth
          // failure. Bail without arming the re-auth backoff: otherwise a
          // transient outage that arrives mid-rotate would burn both attempts
          // (attempt 2's hello short-circuits on the hub-unreachable window)
          // and suppress genuine auth recovery for up to REAUTH_BACKOFF_MAX_MS,
          // even though a JSON 401/403 retry would succeed once the hub is
          // reachable again. The hub-unreachable window already gates re-entry.
          if (helloResult.error === 'hub_unreachable' || helloResult.error === 'hub_unreachable_backoff') {
            hubUnreachable = true;
            break;
          }
          if (isSecretDivergenceError(helloResult.error)) {
            // The hub has explicitly rejected our current secret as diverged
            // from its record. Drop store/env-derived auth once, then spend
            // the second attempt on an unauthenticated rotate hello instead
            // of backing off while still presenting the same stale Bearer.
            if (attempt < MAX_REAUTH_ATTEMPTS && !droppedDivergedSecret) {
              this._dropLocalSecret(SECRET_DIVERGENCE_ERROR);
              droppedDivergedSecret = true;
              continue;
            }
            break;
          }
          if (typeof helloResult.error === 'string' && helloResult.error.startsWith('node_id_already_claimed')) {
            // Hub does not believe we own this nodeId. Our locally cached
            // secret(s) are useless. Drop them so attempt 2 retries WITHOUT
            // a Bearer (lenient hello path). If even unauthenticated rotate
            // is rejected, only a manual reset can recover.
            if (attempt < MAX_REAUTH_ATTEMPTS) {
              this._dropLocalSecret('node_id_already_claimed');
              continue;
            }
            manualResetRequired = true;
            break;
          }
          continue;
        }
        const newSecret = helloResult.response?.payload?.node_secret;
        if (!newSecret) {
          this.logger.error('[lifecycle] re-auth: hub did not return a new secret (rotate may not have taken effect)');
          break;
        }
        const hbResult = await this.heartbeat({ _skipReauth: true });
        if (hbResult.ok) {
          this.logger.log('[lifecycle] re-auth succeeded: heartbeat confirmed with new secret');
          this._consecutiveReauthFailures = 0;
          // Note: _envOverrideLogged is intentionally NOT reset here.
          // The successful hello path above already set _suppressEnvSecret=true,
          // which means _resolveNodeSecret will never hit the env-vs-store
          // conflict branch again in this process, so the warning would never
          // fire a second time anyway. Resetting the flag was misleading.
          return true;
        }
        // Same as the hello path: if the verification heartbeat fails because
        // the hub link dropped (not an auth rejection), defer without arming
        // the re-auth backoff.
        if (hbResult.error === 'hub_unreachable' || hbResult.error === 'hub_unreachable_backoff') {
          hubUnreachable = true;
          break;
        }
        this.logger.warn(`[lifecycle] re-auth attempt ${attempt}: heartbeat still failing after rotate`);
      }
      if (hubUnreachable) {
        this.logger.warn('[lifecycle] re-auth deferred: hub unreachable (no re-auth backoff armed)');
        return false;
      }
      if (manualResetRequired) {
        this._emitManualResetNeeded();
      }
      this._consecutiveReauthFailures += 1;
      const backoffMs = Math.min(
        REAUTH_BACKOFF_BASE_MS * Math.pow(2, this._consecutiveReauthFailures - 1),
        REAUTH_BACKOFF_MAX_MS
      );
      const backoffMin = Math.round(backoffMs / 60_000);
      this.logger.error(
        `[lifecycle] re-auth exhausted all attempts (failure #${this._consecutiveReauthFailures}), ` +
          `backing off for ${backoffMin} minutes`
      );
      this._reauthBackoffUntil = Date.now() + backoffMs;
      return false;
    } finally {
      this._reauthInProgress = false;
    }
  }

  /**
   * Drop the cached node_secret in MailboxStore AND signal the env-var path to
   * skip its value for this process lifetime. Used when the hub explicitly
   * disowns our claim.
   * @param {string} reason - log tag describing why we are dropping it.
   */
  _dropLocalSecret(reason) {
    this.logger.warn(`[lifecycle] dropping cached node_secret (reason=${reason}); next hello will run unauthenticated`);
    const diskRotated = this._latestDiskHubRotatedSecret();
    const storeSecret = this.store.getState('node_secret') || null;
    if (diskRotated && diskRotated.secret !== storeSecret) {
      try {
        this._setNodeSecretState({
          secret: diskRotated.secret,
          version: diskRotated.version ? String(diskRotated.version) : '',
          source: 'hub_rotate',
          envSuppressed: this.store.getState('node_secret_env_suppressed') || '',
        });
        this.logger.warn('[lifecycle] local in-memory node_secret is stale; preserving newer disk hub-rotated secret');
        return;
      } catch (err) {
        const reason = err && (err.code || err.name) ? (err.code || err.name) : 'error';
        this.logger.warn(`[lifecycle] failed to sync newer disk hub-rotated node_secret into memory (reason=${reason})`);
      }
    }
    try {
      this._setNodeSecretState({
        secret: '',
        version: '',
        source: '',
        envSuppressed: this.store.getState('node_secret_env_suppressed') || '',
      });
    } catch (err) {
      const reason = err && (err.code || err.name || err.message) ? (err.code || err.name || err.message) : 'error';
      this.logger.warn(`[lifecycle] failed to clear local node_secret state (reason=${reason})`);
    }
    // Suppress only the exact env secret that was just proven stale. If no
    // env secret is present, do not leave a marker that blocks a future reset.
    this._markCurrentEnvSecretSuppressed();
  }

  _emitManualResetNeeded() {
    try {
      this.store.writeInbound({
        type: 'system',
        priority: 'high',
        channel: 'evomap-hub',
        payload: {
          action: 'manual_secret_reset_required',
          message:
            'Hub disowns this node_id (node_id_already_claimed). Local node_secret and the current node secret env value are invalid. Visit https://evomap.ai/account, click "Reset Secret" on the agent card, run `evolver reset-local-secret` to clear local secret and env suppression state, then update A2A_NODE_SECRET/EVOMAP_NODE_SECRET and restart proxy. Only changing env before clearing suppression state can keep an older local marker active.',
          docs_url: 'https://evomap.ai/account',
        },
      });
    } catch (err) {
      this.logger.warn(`[lifecycle] failed to emit manual_secret_reset_required event: ${err.message}`);
    }
  }

  async heartbeat({ _skipReauth = false } = {}) {
    // Wrap the entire body — including pre-fetch helpers (hello,
    // getTaskMeta, store.countPending, env_fingerprint) — in a single
    // try/catch. Reporter (#544) showed a single throw from any of
    // these (store corrupt, hello rejecting, fingerprint failing under
    // sandboxing) used to escape and kill `tick()`, leaving the
    // daemon "alive but never heartbeating". The post-fetch path is
    // unchanged; only the boundary moved earlier.
    if (!this.hubUrl) return { ok: false, error: 'no_hub_url' };
    try {
      const waitMs = this._hubUnreachableWaitMs();
      if (waitMs > 0) {
        return {
          ok: false,
          error: 'hub_unreachable_backoff',
          retryAfterMs: waitMs,
        };
      }

      const nodeId = this.nodeId;
      if (!nodeId) {
        const helloResult = await this.hello();
        if (!helloResult.ok) return helloResult;
      }

      const endpoint = `${this.hubUrl}/a2a/heartbeat`;
      const taskMeta = typeof this.getTaskMeta === 'function' ? this.getTaskMeta() : {};
      const fp = _getEnvFingerprint();
      const secretVersion = this.nodeSecretVersion;
      const body = {
        node_id: this.nodeId,
        sender_id: this.nodeId,
        evolver_version: fp.evolver_version || PROXY_PROTOCOL_VERSION,
        env_fingerprint: fp,
        meta: {
          proxy_version: PROXY_PROTOCOL_VERSION,
          proxy_protocol_version: PROXY_PROTOCOL_VERSION,
          outbound_pending: this.store.countPending({ direction: 'outbound' }),
          inbound_pending: this.store.countPending({ direction: 'inbound' }),
          ...taskMeta,
        },
      };
      if (secretVersion) {
        body.node_secret_version = secretVersion;
        body.meta.node_secret_version = secretVersion;
      }

      try {
        const cfg = require('../../config');
        if (cfg.antiAbuseTelemetryMode && cfg.antiAbuseTelemetryMode() === 'heartbeat') {
          const { buildHeartbeatAntiAbuseTelemetry } = require('../../gep/antiAbuseTelemetry');
          body.meta.anti_abuse = buildHeartbeatAntiAbuseTelemetry({
            source: 'evolver-proxy',
            nodeId: this.nodeId,
            envFingerprint: fp,
            taskMeta: body.meta,
            // This heartbeat is sent FROM the running proxy — ground truth,
            // not env sniffing (this process usually has neither EVOMAP_PROXY
            // nor EVOMAP_PROXY_PORT set, which would misreport false).
            proxyPortConfigured: true,
          });
        }
      } catch (e) {
        this.logger.warn(`[AntiAbuseTelemetry] failed to build heartbeat summary: ${e && e.message || e}`);
      }

      // Attach any pending force_update outcome so the hub-side
      // EvolverUpgradeAttempt table gets a row. Captured in a local so the
      // post-2xx clear matches identity (rotation-safe — see
      // _clearLastUpdateStateIfMatches). Never let telemetry throw.
      let capturedLastUpdate = null;
      try {
        const pending = readPendingLastUpdate();
        if (pending) {
          body.last_update = pending;
          capturedLastUpdate = pending;
        }
      } catch (e) {
        this.logger.warn(`[lifecycle] readPendingLastUpdate failed (non-fatal): ${e && e.message || e}`);
      }

      const res = await hubFetch(endpoint, {
        method: 'POST',
        headers: this._buildHeaders(),
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(HEARTBEAT_TIMEOUT),
      });

      await throwIfHubUnreachableResponse(res, 'lifecycle heartbeat');
      this._recordHubReachable();

      if (res.status === 403 || res.status === 401) {
        this._consecutiveFailures++;
        const errText = await readHubResponseText(res).catch(() => '');
        const safeErrText = sanitizeHubResponseForLog(errText);
        this.logger.error(`[lifecycle] heartbeat auth failed (${res.status}): ${safeErrText}`);
        if (!_skipReauth) {
          const recovered = await this.reAuthenticate();
          if (recovered) {
            this._consecutiveFailures = 0;
            return { ok: true, recovered: true };
          }
        }
        return { ok: false, error: `auth_failed_${res.status}`, statusCode: res.status };
      }

      if (!res.ok) {
        const errText = await readHubResponseText(res).catch(() => '');
        const safeErrText = sanitizeHubResponseForLog(errText);
        // 426 Upgrade Required: hub emits this when our evolver_version is
        // below the minimum version it requires. The body is JSON of shape
        // `{ error: 'evolver_min_version_required', force_update: {...} }`
        // (see hub `src/routes/a2a/_middleware.js`). Pre-fix this fell
        // through to the generic `http_426` error and the proxy never
        // attempted the upgrade — defeating the very mechanism that 426
        // exists to drive. Mirror the 200+force_update path: parse the
        // body, fire executeForceUpdate (which writes the state file via
        // reportForceUpdateOutcome), and let the next heartbeat carry the
        // attempt as body.last_update. Still return an error so the
        // caller's failure counter ticks and the loop backs off.
        if (res.status === 426) {
          let parsed = null;
          try { parsed = JSON.parse(errText); } catch (_) { /* body not JSON */ }
          const fu = parsed && parsed.force_update;
          if (fu && typeof fu === 'object') {
            this.logger.warn(
              `[lifecycle] heartbeat HTTP 426 with force_update directive (required=${
                fu.required_version || '?'
              }) — triggering executeForceUpdate`
            );
            _maybeTriggerForceUpdateFromHeartbeat(fu, this.logger);
          } else {
            this.logger.warn(
              `[lifecycle] heartbeat HTTP 426 without parseable force_update payload: ${safeErrText}`
            );
          }
        }
        // Hub 400 circuit breaker (mirrors a2aProtocol.js sendHeartbeat
        // ~L2376-2411): if last_update was attached this tick and the hub
        // rejected the body with 400 AND the rejection names the
        // last_update field, the state file is poisoning every heartbeat
        // (e.g. downgrade-then-upgrade left a payload the new hub schema
        // rejects, or a manual edit corrupted the JSON shape). The proxy
        // path used to lack this breaker entirely, so a single bad payload
        // would block telemetry forever -- every retry re-sends the same
        // poison and re-fails with 400. Single-strike (no counter): the
        // 400 + last_update substring pair is unambiguous enough that
        // waiting for repeats just delays recovery. Scope intentionally
        // narrowed to 400-only (NOT any 4xx): 401/403 are auth errors
        // (handled above), 404/405/409 etc. are hub-routing problems that
        // are not the payload's fault. The existing _consecutiveFailures
        // backoff is preserved -- the breaker runs BEFORE the early
        // return so the file is cleared, and then the normal failure
        // path continues unchanged.
        if (res.status === 400 && capturedLastUpdate) {
          const errorText = 'http_400: ' + errText;
          if (/last[_-]?update/i.test(errorText)) {
            // Bypass any rate-limited warn helper: this is a critical
            // recovery signal that must surface even if other ForceUpdate
            // warns fired recently.
            this.logger.warn(
              '[lifecycle] hub 400 with last_update attached (error names last_update); ' +
                'clearing poisoning state file.'
            );
            try {
              clearLastUpdateOnAck(capturedLastUpdate);
            } catch (e) {
              this.logger.warn(`[lifecycle] clearLastUpdateOnAck failed (non-fatal): ${e && e.message || e}`);
            }
          }
        }
        this._consecutiveFailures++;
        this.logger.error(`[lifecycle] heartbeat HTTP ${res.status}: ${safeErrText}`);
        return { ok: false, error: `http_${res.status}`, statusCode: res.status };
      }

      const data = await readHubResponseJson(res);

      this._consecutiveFailures = 0;
      this.store.setState('last_heartbeat_at', new Date().toISOString());

      // Semantic parity with a2aProtocol.js sendHeartbeat: a 2xx with
      // `{ok:false}` or `status:'unknown_node'` is NOT a hub-side persist,
      // so the state file must survive for the next heartbeat to retry
      // (unknown_node triggers a re-hello below).
      //
      // PR #188 follow-up (HIGH H1-client): the hub now writes a top-level
      // `last_update_ack: { ok, reason? }` whenever the request carried a
      // last_update payload. Gate the clear on the ack so we do not unlink
      // the only evidence of the upgrade attempt when the hub's
      // fire-and-forget persist throws / dedup-misses / schema-rejects /
      // bypass-path returns false. Backward compat: an old hub that has not
      // yet rolled out the ack writer falls back to the original bare-2xx
      // semantics so this client keeps working against pre-rollout hubs.
      // See src/gep/a2aProtocol.js sendHeartbeat for the canonical comment.
      const hubAccepted = !(data && data.ok === false) && data?.status !== 'unknown_node';
      if (capturedLastUpdate) {
        const ack = data && data.last_update_ack;
        const hasAck = ack && typeof ack === 'object';
        let shouldClear;
        if (hasAck) {
          shouldClear = ack.ok === true
            || ack.reason === 'duplicate'
            || ack.reason === 'invalid';
          if (ack.reason === 'failed') {
            this.logger.warn('[lifecycle] hub last_update_ack=failed; ' +
              'keeping state file for retry on next heartbeat.');
          } else if (ack.reason === 'invalid') {
            this.logger.warn('[lifecycle] hub last_update_ack=invalid; ' +
              'clearing state file (retry will not help).');
          }
        } else {
          shouldClear = hubAccepted;
        }
        if (shouldClear) {
          try {
            clearLastUpdateOnAck(capturedLastUpdate);
          } catch (e) {
            this.logger.warn(`[lifecycle] clearLastUpdateOnAck failed (non-fatal): ${e && e.message || e}`);
          }
        }
      }

      if (data?.status === 'unknown_node') {
        this.logger.warn('[lifecycle] Node unknown, re-registering...');
        await this.hello();
      }

      // PR #188 H1 fix: 200 with a `force_update` directive must drive
      // executeForceUpdate the same way a2aProtocol.js does for
      // non-proxy nodes (see a2aProtocol.js:2292-2305 and
      // _maybeTriggerForceUpdateFromHeartbeat). Pure proxy-mode nodes
      // never enter the evolve run() loop, so the consumeForceUpdate
      // path never fires for them — without this block the hub could
      // push force_update forever with zero upgrade attempts and zero
      // EvolverUpgradeAttempt rows. The helper is in-flight + cooldown
      // gated; placing the call here (post-events, pre-min_version
      // banner) means a single response carrying both events AND a
      // force_update still processes the events first.
      if (data && data.force_update && typeof data.force_update === 'object') {
        this.logger.log(
          '[ForceUpdate] Hub requires update to ' +
          (data.force_update.required_version || '?') +
          ' -- reason: ' + (data.force_update.reason || 'unspecified')
        );
        _maybeTriggerForceUpdateFromHeartbeat(data.force_update, this.logger);
      }

      if (Array.isArray(data?.events) && data.events.length > 0) {
        this.store.writeInboundBatch(
          data.events.map(e => ({
            type: e.type || 'hub_event',
            payload: e,
            channel: 'evomap-hub',
          }))
        );
      }

      if (data?.min_proxy_version && this._shouldUpgrade(data.min_proxy_version)) {
        this.store.writeInbound({
          type: 'system',
          payload: {
            action: 'proxy_upgrade_required',
            min_version: data.min_proxy_version,
            current_version: PROXY_PROTOCOL_VERSION,
            upgrade_url: data.upgrade_url || null,
            message: data.upgrade_message || 'Proxy version is below the minimum required by Hub.',
          },
          channel: 'evomap-hub',
          priority: 'high',
        });
        this.logger.warn(`[lifecycle] Hub requires proxy >= ${data.min_proxy_version}, current: ${PROXY_PROTOCOL_VERSION}`);
      }

      return { ok: true, response: data };
    } catch (err) {
      if (isHubUnreachableError(err)) {
        this._consecutiveFailures++;
        const retryAfterMs = this._recordHubUnreachable(err);
        return {
          ok: false,
          error: 'hub_unreachable',
          detail: err.message,
          retryAfterMs,
        };
      }
      this._consecutiveFailures++;
      this.logger.error(`[lifecycle] heartbeat failed (${this._consecutiveFailures}): ${err.message}`);
      return { ok: false, error: err.message };
    }
  }

  startHeartbeatLoop(intervalMs) {
    if (this._running) return;
    this._running = true;
    this._startedAt = Date.now();
    this._heartbeatInterval = Math.max(30_000, intervalMs || DEFAULT_HEARTBEAT_INTERVAL);
    // Generation counter: every poke / stop bumps this. Tick captures
    // its gen at entry; if it doesn't match on resume, the tick refuses
    // to schedule its own next timer (a fresher path already owns it).
    this._heartbeatGen = (this._heartbeatGen || 0) + 1;
    this._heartbeatTick(this._heartbeatGen);
    this._startDriftDetector();
  }

  // Sample wall-clock every DRIFT_CHECK_MS so macOS sleep / hypervisor
  // pause / debugger break is detected and the heartbeat loop is poked
  // back into action without waiting for the (possibly 15-min) backoff
  // timer to fire on libuv's monotonic clock. R10 (#544).
  _startDriftDetector() {
    if (this._driftInterval) return;
    this._lastDriftCheckAt = Date.now();
    this._driftInterval = setInterval(() => {
      // Wrap the whole body in try/catch -- this is a setInterval
      // callback; any throw escaping it kills the detector itself,
      // which is the bug we're protecting against.
      try {
        if (!this._running) return;
        const now = Date.now();
        const gap = now - this._lastDriftCheckAt;
        this._lastDriftCheckAt = now;
        if (gap > DRIFT_SLEEP_THRESHOLD_MS) {
          try {
            this.logger.warn(
              `[lifecycle] wall-clock jump detected (+${Math.round(gap / 1000)}s); ` +
                'likely sleep/wake or process suspension, poking heartbeat'
            );
          } catch (_) { /* logger broken; detector must still poke */ }
          // Long-sleep recovery: the hub-side cached state we carried
          // through the suspend is almost certainly stale. Clear reauth
          // backoff so the next tick can try a clean recovery path
          // instead of sitting out a pre-sleep penalty for up to 4h.
          if (gap > DRIFT_LONG_SLEEP_THRESHOLD_MS) {
            this._consecutiveReauthFailures = 0;
            this._reauthBackoffUntil = 0;
            try {
              this.logger.warn(
                `[lifecycle] long sleep (+${Math.round(gap / 60_000)}min) cleared reauth backoff`
              );
            } catch (_) { /* logger broken; non-fatal */ }
          }
          this.pokeHeartbeatLoop();
        }
      } catch (err) {
        try { this.logger.error(`[lifecycle] drift detector threw: ${err && err.message}`); }
        catch (_) { /* never let the detector escape */ }
      }
    }, DRIFT_CHECK_MS);
    // Don't keep the event loop alive on behalf of the detector alone --
    // matches the unref() used on _heartbeatTimer.
    if (this._driftInterval.unref) this._driftInterval.unref();
  }

  async _heartbeatTick(myGen) {
    if (!this._running) return;
    this._lastHeartbeatTickAt = Date.now();
    // Defence-in-depth: even with heartbeat() now fully wrapped (see
    // its body), an unforeseen synchronous throw inside the awaited
    // path or a defective stub passed in tests would still bubble
    // into this closure as a rejected promise and cancel the next
    // setTimeout. Catching here guarantees the loop schedules its
    // own next tick under all conditions short of `stopHeartbeatLoop`.
    try {
      await this.heartbeat();
    } catch (err) {
      this._consecutiveFailures++;
      this.logger.error(`[lifecycle] heartbeat tick threw (${this._consecutiveFailures}): ${err && err.message}`);
    }
    if (!this._running) return;
    // Generation guard: a poke or stop fired while we were awaiting
    // `heartbeat()`. The fresher path already armed its own timer (or
    // tore the loop down); scheduling here would orphan the new timer
    // or fork the loop into two concurrent ticks (Bugbot #147 finding
    // 2026-05-28).
    if (myGen !== undefined && myGen !== this._heartbeatGen) return;
    // 15min cap (was 30min, then briefly 5min). Must stay above
    // `DEFAULT_HEARTBEAT_INTERVAL` (6min) or the exponential branch
    // retries faster than the success branch (Bugbot #147 finding).
    const interval = this._heartbeatInterval || DEFAULT_HEARTBEAT_INTERVAL;
    const hubWaitMs = this._hubUnreachableWaitMs();
    // While a hub-unreachable window is active, wake exactly when it elapses
    // (1s floor to avoid a busy 0ms reschedule), mirroring SyncEngine's
    // `Math.max(1_000, retryAfterMs)`. A 30s floor over-waited up to ~30s past
    // the window's end, delaying recovery once the hub was reachable again.
    const backoff = hubWaitMs > 0
      ? Math.max(1_000, hubWaitMs)
      : this._consecutiveFailures > 0
      ? Math.min(interval * Math.pow(2, this._consecutiveFailures), HEARTBEAT_BACKOFF_CAP_MS)
      : interval;
    const armedGen = this._heartbeatGen;
    this._heartbeatTimer = setTimeout(() => this._heartbeatTick(armedGen), backoff);
    if (this._heartbeatTimer.unref) this._heartbeatTimer.unref();
  }

  /// Reset the heartbeat schedule immediately. Call when an external
  /// signal (Hub push, tab visibility, manual `evolver heartbeat now`)
  /// indicates the next tick should not wait out its current backoff.
  /// No-op when the loop is not running.
  pokeHeartbeatLoop() {
    if (!this._running) return;
    if (this._heartbeatTimer) {
      clearTimeout(this._heartbeatTimer);
      this._heartbeatTimer = null;
    }
    this._consecutiveFailures = 0;
    // Bump generation: any in-flight `_heartbeatTick` from before the
    // poke will see its captured gen mismatch on resume and skip its
    // tail-`setTimeout`, so we don't end up with two concurrent timers.
    this._heartbeatGen = (this._heartbeatGen || 0) + 1;
    const myGen = this._heartbeatGen;
    // setImmediate-equivalent: defer to the next event-loop turn so
    // re-entrant pokes (e.g. from a Hub event handler) don't run
    // synchronously inside the caller's frame.
    this._heartbeatTimer = setTimeout(() => this._heartbeatTick(myGen), 0);
    if (this._heartbeatTimer.unref) this._heartbeatTimer.unref();
  }

  stopHeartbeatLoop() {
    this._running = false;
    if (this._heartbeatTimer) {
      clearTimeout(this._heartbeatTimer);
      this._heartbeatTimer = null;
    }
    if (this._driftInterval) {
      clearInterval(this._driftInterval);
      this._driftInterval = null;
    }
  }

  getHeartbeatStats() {
    return {
      running: this._running,
      intervalMs: this._heartbeatInterval || DEFAULT_HEARTBEAT_INTERVAL,
      uptimeMs: this._startedAt ? Date.now() - this._startedAt : 0,
      consecutiveFailures: this._consecutiveFailures,
      lastTickAt: this._lastHeartbeatTickAt,
    };
  }

  _shouldUpgrade(minVersion) {
    // parseInt strips trailing non-digit chars in prerelease segments like
    // `1-beta`, so `0.1.1-beta.1`.split('.')[2] -> `1-beta` -> parseInt = 1.
    // Using Number() here returned NaN and was treated as 0, under-counting
    // prerelease minimums. See community PR #516.
    const parse = (v) => String(v || '0.0.0').split('.').map((part) => parseInt(part, 10));
    const min = parse(minVersion);
    const cur = parse(PROXY_PROTOCOL_VERSION);
    for (let i = 0; i < 3; i++) {
      if ((cur[i] || 0) < (min[i] || 0)) return true;
      if ((cur[i] || 0) > (min[i] || 0)) return false;
    }
    return false;
  }
}

module.exports = {
  LifecycleManager,
  AuthError,
  DEFAULT_HEARTBEAT_INTERVAL,
  HEARTBEAT_BACKOFF_CAP_MS,
  // Test hooks behind `_testing` to mirror the namespacing used by
  // a2aProtocol.js — production callers must not accidentally tweak the
  // proxy force_update lifecycle state.
  _testing: {
    // Reset proxy heartbeat-driven force_update state. Avoids cooldown
    // leakage between sibling tests that share one process.
    _resetProxyForceUpdateStateForTesting: function () {
      _proxyForceUpdateInFlight = false;
      _proxyForceUpdateLastAttemptAt = 0;
    },
  },
};
