// Centralized configuration for evolver runtime thresholds and timeouts.
// All values support environment variable override where specified.
// Groups: network, solidify, evolution, ops, limits.

function envInt(key, fallback) {
  const v = process.env[key];
  if (v === undefined || v === '') return fallback;
  const n = parseInt(v, 10);
  return isNaN(n) ? fallback : n;
}

// Strict variant for timing / timeout / interval values that must be
// positive. Rejects: NaN (e.g. "5min" silently parses to 5 -- here 5 is
// accepted but a suffix-only "ms" becomes NaN), 0 (which would turn an
// interval into a hot loop or zero out a timeout signal), and negatives
// (setTimeout clamps to 1 ms). Also rejects values >= 2^31 because
// setTimeout silently downgrades those to 1 ms in Node. Misconfigured
// values fall back to the default with a one-time warning so the user
// is not silently running a broken setup.
const _envPositiveIntWarned = new Set();
function envPositiveInt(key, fallback) {
  const v = process.env[key];
  if (v === undefined || v === '') return fallback;
  const n = parseInt(v, 10);
  const valid = Number.isFinite(n) && n > 0 && n < 2 ** 31;
  if (!valid) {
    if (!_envPositiveIntWarned.has(key)) {
      _envPositiveIntWarned.add(key);
      try {
        console.warn(
          '[config] ' + key + '=' + JSON.stringify(v) + ' is not a positive integer; ' +
          'falling back to ' + fallback + '. Set a value in (0, 2^31) ms.'
        );
      } catch (_) {}
    }
    return fallback;
  }
  return n;
}

function envFloat(key, fallback) {
  const v = process.env[key];
  if (v === undefined || v === '') return fallback;
  const n = parseFloat(v);
  return isNaN(n) ? fallback : n;
}

function envStr(key, fallback) {
  const v = process.env[key];
  return (v !== undefined && v !== '') ? v : fallback;
}

// --- Network & A2A ---

// Hot-path timers / intervals use envPositiveInt: a misconfigured 0,
// negative, or non-numeric value would otherwise turn the heartbeat
// loop into a hot spin (setTimeout(0)) or zero out a timeout signal
// (AbortSignal.timeout(0) immediately aborts every request). Falls back
// to the default with a one-time warning when the env var is invalid.
const HELLO_TIMEOUT_MS = envPositiveInt('EVOLVER_HELLO_TIMEOUT_MS', 15000);
const HEARTBEAT_TIMEOUT_MS = envPositiveInt('EVOLVER_HEARTBEAT_TIMEOUT_MS', 10000);
const HEARTBEAT_INTERVAL_MS = envPositiveInt('HEARTBEAT_INTERVAL_MS', 360000);
const HEARTBEAT_FIRST_DELAY_MS = envPositiveInt('EVOLVER_HEARTBEAT_FIRST_DELAY_MS', 30000);
const EVENT_POLL_TIMEOUT_MS = envPositiveInt('EVOLVER_EVENT_POLL_TIMEOUT_MS', 60000);
const HTTP_TRANSPORT_TIMEOUT_MS = envPositiveInt('EVOLVER_HTTP_TRANSPORT_TIMEOUT_MS', 15000);
const SECRET_CACHE_TTL_MS = envPositiveInt('EVOLVER_SECRET_CACHE_TTL_MS', 60000);
const HUB_SEARCH_TIMEOUT_MS = envPositiveInt('EVOLVER_HUB_SEARCH_TIMEOUT_MS', 8000);

// Hub URL resolution (since v1.69.7).
//
// Precedence at runtime (re-evaluated on every call of resolveHubUrl()):
//   1. process.env.A2A_HUB_URL   -- primary override used by most modules
//   2. process.env.EVOMAP_HUB_URL -- secondary, kept for backward compat
//   3. process.env.EVOLVER_DEFAULT_HUB_URL -- deployment-time default override
//      (useful for air-gapped deployments that point all clients at a private
//       hub endpoint without having to rewrite A2A_HUB_URL in every service)
//   4. PUBLIC_DEFAULT_HUB_URL below (compile-time literal)
//
// IMPORTANT: callers MUST NOT cache the return value at module-load time.
// Before v1.69.7 several modules (validator/*, taskReceiver, directoryClient,
// privacyClient) bound their HUB_URL fallback at require()-time, which meant
// that setting process.env.A2A_HUB_URL later (common in tests and wrappers)
// had no effect. Use resolveHubUrl() inside the function body that builds the
// HTTP request instead.
const PUBLIC_DEFAULT_HUB_URL = 'https://evomap.ai';

function resolveHubUrl() {
  // Trim each candidate and fall through on empty/whitespace-only values.
  // A trailing space in a `.env` value (common with quoted entries like
  // A2A_HUB_URL="https://evomap.ai ") otherwise survives into endpoint
  // construction: `hubUrl.replace(/\/+$/, '')` strips trailing slashes but
  // NOT whitespace, producing "https://evomap.ai /a2a/events/poll" which
  // fails URL validation (#580 Bug 1). `||` alone would also pick a
  // whitespace-only override as "truthy", so trim-then-fall-through here.
  const pick = (v) => { const t = (v == null ? '' : String(v)).trim(); return t || null; };
  const raw = pick(process.env.A2A_HUB_URL)
    || pick(process.env.EVOMAP_HUB_URL)
    || pick(process.env.EVOLVER_DEFAULT_HUB_URL)
    || PUBLIC_DEFAULT_HUB_URL;

  if (process.env.EVOMAP_HUB_ALLOW_INSECURE !== '1') {
    let parsed;
    try {
      parsed = new URL(raw);
    } catch {
      throw new Error(
        '[config] Hub URL is not a valid URL: ' + JSON.stringify(raw) + '. ' +
        'Set EVOMAP_HUB_ALLOW_INSECURE=1 to bypass (local dev / mock hub only).'
      );
    }
    if (parsed.protocol !== 'https:') {
      throw new Error(
        '[config] Hub URL must use https:// — got ' + JSON.stringify(raw) + '. ' +
        'Set EVOMAP_HUB_ALLOW_INSECURE=1 to bypass (local dev / mock hub only).'
      );
    }
  }
  return raw;
}

// --- Solidify & Validation ---

const BLAST_RADIUS_HARD_CAP_FILES = envInt('EVOLVER_HARD_CAP_FILES', 60);
const BLAST_RADIUS_HARD_CAP_LINES = envInt('EVOLVER_HARD_CAP_LINES', 20000);
const VALIDATION_TIMEOUT_MS = envInt('EVOLVER_VALIDATION_TIMEOUT_MS', 180000);
const CANARY_TIMEOUT_MS = envInt('EVOLVER_CANARY_TIMEOUT_MS', 30000);
const CAPSULE_CONTENT_MAX_CHARS = envInt('EVOLVER_CAPSULE_MAX_CHARS', 8000);
const SOLIDIFY_MAX_RETRIES = envInt('SOLIDIFY_MAX_RETRIES', 2);
const SOLIDIFY_RETRY_INTERVAL_MS = envInt('EVOLVER_SOLIDIFY_RETRY_INTERVAL_MS', 1000);
const MIN_PUBLISH_SCORE = envFloat('EVOLVER_MIN_PUBLISH_SCORE', 0.78);
const BROADCAST_SCORE_THRESHOLD = 0.7;
const BROADCAST_SUCCESS_STREAK = 2;
const MAX_REGEX_PATTERN_LEN = 1024;

// --- Evolution Loop ---

const REPAIR_LOOP_THRESHOLD = envInt('EVOLVER_REPAIR_LOOP_THRESHOLD', 3);

// --- Gene Suppression (saturated / repeatedly failing genes) ---
// These thresholds control when a Gene is forcibly excluded from selection
// regardless of drift state. Without this, a Gene that fails repeatedly can
// trigger plateau detection -> drift mode -> the legacy ban skip path,
// resulting in the same failed Gene being re-selected forever.
//
// GENE_BAN_PER_KEY_ATTEMPTS:    minimum attempts on the same signal key
// GENE_BAN_BEST_THRESHOLD:      best success rate at or below which the Gene is banned
// GENE_INERT_BAN_STREAK:        consecutive inert (stable_no_error, zero-work) outcomes
//                               on a signal key after which a Gene with no real
//                               success is banned, so --loop selection explores
//                               instead of re-running a do-nothing gene (#562)
// GENE_EPIGENETIC_HARD_BOOST:   epigenetic boost at or below which the Gene is hard-suppressed
const GENE_BAN_PER_KEY_ATTEMPTS = envInt('EVOLVER_GENE_BAN_PER_KEY_ATTEMPTS', 4);
const GENE_BAN_BEST_THRESHOLD = envFloat('EVOLVER_GENE_BAN_BEST_THRESHOLD', 0.15);
const GENE_INERT_BAN_STREAK = envInt('EVOLVER_GENE_INERT_BAN_STREAK', 8);
const GENE_EPIGENETIC_HARD_BOOST = envFloat('EVOLVER_GENE_EPIGENETIC_HARD_BOOST', -0.3);
const SESSION_ARCHIVE_TRIGGER = envInt('EVOLVER_SESSION_ARCHIVE_TRIGGER', 100);
const SESSION_ARCHIVE_KEEP = envInt('EVOLVER_SESSION_ARCHIVE_KEEP', 50);
const MEMORY_FRAGMENT_MAX_CHARS = envInt('EVOLVER_MEMORY_FRAGMENT_MAX_CHARS', 50000);
const IDLE_FETCH_INTERVAL_MS = envInt('EVOLVER_IDLE_FETCH_INTERVAL_MS', 600000);
const PROMPT_MAX_CHARS = envInt('EVOLVER_PROMPT_MAX_CHARS', 24000);
const ACTIVE_WINDOW_MS = 24 * 60 * 60 * 1000;
const TARGET_BYTES = 120000;
const PER_FILE_BYTES = 20000;
const PER_SESSION_BYTES = 20000;
const RECENCY_GUARD_MS = 30 * 1000;
const DORMANT_TTL_MS = 3600 * 1000;
const PACKAGE_DESC_CACHE_TTL_MS = 6 * 60 * 60 * 1000;
const MEMORY_GRAPH_READ_LIMIT = 1000;
const NARRATIVE_SUMMARY_MAX_CHARS = 3000;

// --- Ops ---

const MAX_SILENCE_MS = envInt('EVOLVER_MAX_SILENCE_MS', 30 * 60 * 1000);
const CLEANUP_MAX_AGE_MS = envInt('EVOLVER_CLEANUP_MAX_AGE_MS', 24 * 60 * 60 * 1000);
const CLEANUP_MIN_KEEP = envInt('EVOLVER_CLEANUP_MIN_KEEP', 10);
const CLEANUP_MAX_FILES = envInt('EVOLVER_CLEANUP_MAX_FILES', 10);
const LOCK_MAX_AGE_MS = envInt('EVOLVER_LOCK_MAX_AGE_MS', 10 * 60 * 1000);

// --- Self-PR (auto-contribute mutations back to public repo) ---

const SELF_PR_MIN_SCORE = envFloat('EVOLVER_SELF_PR_MIN_SCORE', 0.85);
const SELF_PR_MIN_STREAK = envInt('EVOLVER_SELF_PR_MIN_STREAK', 3);
const SELF_PR_MAX_FILES = envInt('EVOLVER_SELF_PR_MAX_FILES', 3);
const SELF_PR_MAX_LINES = envInt('EVOLVER_SELF_PR_MAX_LINES', 100);
const SELF_PR_COOLDOWN_MS = envInt('EVOLVER_SELF_PR_COOLDOWN_MS', 24 * 60 * 60 * 1000);
const SELF_PR_REPO = envStr('EVOLVER_SELF_PR_REPO', 'EvoMap/evolver');
const SELF_PR_TIMEOUT_MS = envInt('EVOLVER_SELF_PR_TIMEOUT_MS', 30000);

// --- Leak Check ---

const LEAK_CHECK_MODE = envStr('EVOLVER_LEAK_CHECK', 'strict');

// --- Reuse attribution (P4-a, Slice A) ---
// Controls whether the evolver attaches a `reuse_attribution` block to the
// synced `outcome` MemoryGraphEvent so the Hub can LATER (P4-a Slice B, gated +
// team-signed-off) credit the SOURCE node when its asset is reused. Modes:
//   off    (default) — attach nothing; byte-identical to pre-P4-a behavior.
//   shadow           — attach the attribution block; it rides the existing
//                      syncEventToHub -> /a2a/memory/event into the Hub's
//                      MemoryGraphEvent.payload blob, which is GDI-inert and
//                      read by NO payout path today.
// There is intentionally NO `enforce` on the CLIENT: the evolver cannot move
// money, so an enforce word would be a lie. The report stays economy-inert
// until a SIGNED-OFF Hub reader converts it to credit (which MUST add the
// anti-sybil gating — see P4-a Slice B). Until then it only emits honest,
// runtime-observed attribution data (never agent-supplied identity).
const REUSE_ATTRIBUTION_MODE = envStr('EVOLVER_REUSE_ATTRIBUTION', 'off');
function reuseAttributionMode() {
  const v = String(process.env.EVOLVER_REUSE_ATTRIBUTION || REUSE_ATTRIBUTION_MODE || 'off').toLowerCase().trim();
  return v === 'shadow' ? 'shadow' : 'off';
}

// Opt-in Hub reuse-OUTCOME reporting (P4-a Slice B, client side). When 'on', the
// evolver POSTs {signals, status, used_asset_ids} to the Hub's /a2a/memory/record
// so the reuse-reward attribution pipeline (which reads THAT endpoint, not the
// inert reuse_attribution blob on /a2a/memory/event) finally gets data.
// MONEY-ADJACENT and charges Hub credits -> default 'off'. The Hub still
// re-verifies every used_asset_id against its own AssetFetcher rows before
// crediting. Also requires EVOLVER_REUSE_ATTRIBUTION=shadow, which is what builds
// the cycle-correlated, timestamp-guarded attribution this report consumes.
const OUTCOME_REPORT_MODE = envStr('EVOLVER_OUTCOME_REPORT', 'off');
function outcomeReportMode() {
  const v = String(process.env.EVOLVER_OUTCOME_REPORT || OUTCOME_REPORT_MODE || 'off').toLowerCase().trim();
  return v === 'on' || v === 'enforce' || v === 'true' ? 'on' : 'off';
}

// --- Anti-abuse telemetry (privacy-preserving heartbeat summary) ---
// Enabled by default. In heartbeat mode, clients attach a small
// `meta.anti_abuse` envelope with low-sensitive hashes, source-confidence
// labels, and explicit placeholders for data that must be observed by Hub
// services instead of trusted from the client.
const ANTI_ABUSE_TELEMETRY_MODE = envStr('EVOLVER_ANTI_ABUSE_TELEMETRY', 'heartbeat');
function antiAbuseTelemetryMode() {
  const raw = process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
  const v = String(raw == null ? '' : raw).toLowerCase().trim();
  // Empty / whitespace-only counts as UNSET (same as envStr's '' -> fallback
  // above): a blank `EVOLVER_ANTI_ABUSE_TELEMETRY=` line in a .env file must
  // not silently disable the documented default-on behavior. Opt-out is
  // explicit only.
  if (v === '') return 'heartbeat';
  if (v === '0' || v === 'false' || v === 'no' || v === 'off') return 'off';
  return (v === '1' || v === 'true' || v === 'yes' || v === 'on' || v === 'heartbeat')
    ? 'heartbeat'
    : 'off';
}

// --- Validator mode (opt-out) ---
// Node role: the evolver periodically fetches assigned validation tasks from
// the Hub, runs the commands in an isolated sandbox, and submits
// ValidationReports. Default is ON (opt-out). Set EVOLVER_VALIDATOR_ENABLED=false
// to skip the validator role. Note: the exported VALIDATOR_ENABLED below is a
// legacy helper that resolves only from env (no persisted flag). Real runtime
// gating lives in src/gep/validator/index.js:isValidatorEnabled().

const VALIDATOR_ENABLED = (function () {
  const v = String(process.env.EVOLVER_VALIDATOR_ENABLED || '').toLowerCase().trim();
  return v === '1' || v === 'true' || v === 'yes' || v === 'on';
})();
const VALIDATOR_STAKE_AMOUNT = envInt('EVOLVER_VALIDATOR_STAKE_AMOUNT', 100);
const VALIDATOR_MAX_TASKS_PER_CYCLE = envInt('EVOLVER_VALIDATOR_MAX_TASKS_PER_CYCLE', 2);
const VALIDATOR_FETCH_TIMEOUT_MS = envInt('EVOLVER_VALIDATOR_FETCH_TIMEOUT_MS', 8000);
const VALIDATOR_REPORT_TIMEOUT_MS = envInt('EVOLVER_VALIDATOR_REPORT_TIMEOUT_MS', 10000);
const VALIDATOR_STAKE_TIMEOUT_MS = envInt('EVOLVER_VALIDATOR_STAKE_TIMEOUT_MS', 10000);
const VALIDATOR_CMD_TIMEOUT_MS = envInt('EVOLVER_VALIDATOR_CMD_TIMEOUT_MS', 60000);
const VALIDATOR_BATCH_TIMEOUT_MS = envInt('EVOLVER_VALIDATOR_BATCH_TIMEOUT_MS', 180000);

module.exports = {
  // Network
  HELLO_TIMEOUT_MS,
  HEARTBEAT_TIMEOUT_MS,
  HEARTBEAT_INTERVAL_MS,
  HEARTBEAT_FIRST_DELAY_MS,
  EVENT_POLL_TIMEOUT_MS,
  HTTP_TRANSPORT_TIMEOUT_MS,
  SECRET_CACHE_TTL_MS,
  HUB_SEARCH_TIMEOUT_MS,
  PUBLIC_DEFAULT_HUB_URL,
  resolveHubUrl,
  // Solidify
  VALIDATION_TIMEOUT_MS,
  CANARY_TIMEOUT_MS,
  CAPSULE_CONTENT_MAX_CHARS,
  SOLIDIFY_MAX_RETRIES,
  SOLIDIFY_RETRY_INTERVAL_MS,
  MIN_PUBLISH_SCORE,
  BROADCAST_SCORE_THRESHOLD,
  BROADCAST_SUCCESS_STREAK,
  MAX_REGEX_PATTERN_LEN,
  // Evolution
  REPAIR_LOOP_THRESHOLD,
  GENE_BAN_PER_KEY_ATTEMPTS,
  GENE_BAN_BEST_THRESHOLD,
  GENE_INERT_BAN_STREAK,
  GENE_EPIGENETIC_HARD_BOOST,
  SESSION_ARCHIVE_TRIGGER,
  SESSION_ARCHIVE_KEEP,
  MEMORY_FRAGMENT_MAX_CHARS,
  IDLE_FETCH_INTERVAL_MS,
  PROMPT_MAX_CHARS,
  ACTIVE_WINDOW_MS,
  TARGET_BYTES,
  PER_FILE_BYTES,
  PER_SESSION_BYTES,
  RECENCY_GUARD_MS,
  DORMANT_TTL_MS,
  PACKAGE_DESC_CACHE_TTL_MS,
  MEMORY_GRAPH_READ_LIMIT,
  NARRATIVE_SUMMARY_MAX_CHARS,
  // Ops
  MAX_SILENCE_MS,
  CLEANUP_MAX_AGE_MS,
  CLEANUP_MIN_KEEP,
  CLEANUP_MAX_FILES,
  LOCK_MAX_AGE_MS,
  // Self-PR
  SELF_PR_MIN_SCORE,
  SELF_PR_MIN_STREAK,
  SELF_PR_MAX_FILES,
  SELF_PR_MAX_LINES,
  SELF_PR_COOLDOWN_MS,
  SELF_PR_REPO,
  SELF_PR_TIMEOUT_MS,
  // Policy
  BLAST_RADIUS_HARD_CAP_FILES,
  BLAST_RADIUS_HARD_CAP_LINES,
  // Security
  LEAK_CHECK_MODE,
  // Reuse attribution (P4-a Slice A)
  REUSE_ATTRIBUTION_MODE,
  reuseAttributionMode,
  // Reuse-outcome Hub reporting (P4-a Slice B, opt-in)
  OUTCOME_REPORT_MODE,
  outcomeReportMode,
  // Anti-abuse telemetry
  ANTI_ABUSE_TELEMETRY_MODE,
  antiAbuseTelemetryMode,
  // Validator (opt-in role)
  VALIDATOR_ENABLED,
  VALIDATOR_STAKE_AMOUNT,
  VALIDATOR_MAX_TASKS_PER_CYCLE,
  VALIDATOR_FETCH_TIMEOUT_MS,
  VALIDATOR_REPORT_TIMEOUT_MS,
  VALIDATOR_STAKE_TIMEOUT_MS,
  VALIDATOR_CMD_TIMEOUT_MS,
  VALIDATOR_BATCH_TIMEOUT_MS,
  // Helpers
  envInt,
  envPositiveInt,
  envFloat,
  envStr,
};
