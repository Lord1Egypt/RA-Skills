const RELAY_PUBLISH_GRACE_MS = 5_000;
const DEFAULT_RELAY_HARD_TIMEOUT_MS = 65_000;
const DEFAULT_DELAYED_MS = 60_000;
const DEFAULT_STALLED_MS = 180_000;
const DEFAULT_FAILED_MS_TEST = 600_000;
const DEFAULT_FAILED_MS_PROD = 1_800_000;

function parsePositiveInt(value) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : null;
}

function resolveRelayTimeout(timeoutMs, fallbackMs = DEFAULT_RELAY_HARD_TIMEOUT_MS) {
  return parsePositiveInt(timeoutMs) || fallbackMs;
}

function resolveRelayLifecyclePolicy(env = process.env) {
  const profile = String(env.EKYBOT_RELAY_PROFILE || env.NODE_ENV || 'production').toLowerCase();
  const delayedMs = parsePositiveInt(env.EKYBOT_RELAY_DELAYED_MS) || DEFAULT_DELAYED_MS;
  const stalledMs = parsePositiveInt(env.EKYBOT_RELAY_STALLED_MS) || DEFAULT_STALLED_MS;
  const defaultFailedMs = profile === 'test' ? DEFAULT_FAILED_MS_TEST : DEFAULT_FAILED_MS_PROD;
  const failedMs = parsePositiveInt(env.EKYBOT_RELAY_FAILED_MS) || defaultFailedMs;

  return {
    profile,
    delayedMs,
    stalledMs,
    failedMs,
  };
}

module.exports = {
  RELAY_PUBLISH_GRACE_MS,
  DEFAULT_RELAY_HARD_TIMEOUT_MS,
  DEFAULT_DELAYED_MS,
  DEFAULT_STALLED_MS,
  DEFAULT_FAILED_MS_TEST,
  DEFAULT_FAILED_MS_PROD,
  resolveRelayTimeout,
  resolveRelayLifecyclePolicy,
};
