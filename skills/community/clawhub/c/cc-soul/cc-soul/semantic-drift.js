import { tokenize } from "./memory-utils.ts";
import { isKnownWord } from "./aam.ts";
import { DATA_DIR, debouncedSave } from "./persistence.ts";
import { resolve } from "path";
import { existsSync, readFileSync } from "fs";
const SHORT_WINDOW_MS = 7 * 864e5;
const LONG_WINDOW_MS = 30 * 864e5;
const CHECK_INTERVAL_MS = 36e5;
const MIN_SHORT_SAMPLES = 10;
const MIN_LONG_SAMPLES = 20;
const SHORT_CAP = 500;
const LONG_CAP = 2e3;
const THRESH_MILD = 0.05;
const THRESH_MODERATE = 0.15;
const THRESH_SIGNIFICANT = 0.3;
const RISING_RATIO = 2;
const FALLING_RATIO = 0.3;
const FALLING_MIN_LONG_FREQ = 0.02;
const STABLE_MIN_FREQ = 0.01;
const MAX_TOPICS_PER_CATEGORY = 10;
const STATE_FILE = resolve(DATA_DIR, "semantic_drift.json");
let _state = { shortWindow: [], longWindow: [], lastJSD: 0, lastCheck: 0 };
let _cachedSignal = null;
let _cacheTs = 0;
const CACHE_TTL_MS = 6e4;
function trackMessage(msg, ts) {
  const now = ts || Date.now();
  const tokens = tokenize(msg);
  const topics = tokens.filter((t) => t.length >= 2 && isKnownWord(t));
  if (topics.length === 0) return;
  for (const topic of topics) {
    _state.shortWindow.push({ topic, ts: now });
    _state.longWindow.push({ topic, ts: now });
  }
  _state.shortWindow = _state.shortWindow.filter((e) => now - e.ts < SHORT_WINDOW_MS);
  _state.longWindow = _state.longWindow.filter((e) => now - e.ts < LONG_WINDOW_MS);
  _cachedSignal = null;
  if (now - _state.lastCheck > CHECK_INTERVAL_MS) {
    _state.lastCheck = now;
    saveDriftState();
  }
}
function getDriftSignal() {
  const now = Date.now();
  if (_cachedSignal && now - _cacheTs < CACHE_TTL_MS) return _cachedSignal;
  if (_state.shortWindow.length < MIN_SHORT_SAMPLES || _state.longWindow.length < MIN_LONG_SAMPLES) {
    return null;
  }
  const shortDist = buildDistribution(_state.shortWindow.map((e) => e.topic));
  const longDist = buildDistribution(_state.longWindow.map((e) => e.topic));
  const jsd = jensenShannonDivergence(shortDist, longDist);
  _state.lastJSD = jsd;
  const rising = [];
  const falling = [];
  const stable = [];
  const allTopics = /* @__PURE__ */ new Set([...Object.keys(shortDist), ...Object.keys(longDist)]);
  for (const topic of allTopics) {
    const sf = shortDist[topic] || 0;
    const lf = longDist[topic] || 0;
    const ratio = lf > 1e-3 ? sf / lf : sf > 0 ? 10 : 0;
    if (ratio > RISING_RATIO) {
      rising.push(topic);
    } else if (ratio < FALLING_RATIO && lf > FALLING_MIN_LONG_FREQ) {
      falling.push(topic);
    } else if (sf > STABLE_MIN_FREQ && lf > STABLE_MIN_FREQ) {
      stable.push(topic);
    }
  }
  rising.sort((a, b) => (shortDist[b] || 0) - (shortDist[a] || 0));
  falling.sort((a, b) => (longDist[b] || 0) - (longDist[a] || 0));
  stable.sort((a, b) => {
    const aSum = (shortDist[a] || 0) + (longDist[a] || 0);
    const bSum = (shortDist[b] || 0) + (longDist[b] || 0);
    return bSum - aSum;
  });
  let driftLevel = "none";
  if (jsd > THRESH_SIGNIFICANT) driftLevel = "significant";
  else if (jsd > THRESH_MODERATE) driftLevel = "moderate";
  else if (jsd > THRESH_MILD) driftLevel = "mild";
  const signal = {
    jsd,
    rising: rising.slice(0, MAX_TOPICS_PER_CATEGORY),
    falling: falling.slice(0, MAX_TOPICS_PER_CATEGORY),
    stable: stable.slice(0, MAX_TOPICS_PER_CATEGORY),
    driftLevel
  };
  _cachedSignal = signal;
  _cacheTs = now;
  return signal;
}
function getTopicRecallModifier(topic) {
  const signal = getDriftSignal();
  if (!signal || signal.driftLevel === "none") return 1;
  const t = topic.toLowerCase();
  if (signal.rising.includes(t)) return 1 + Math.min(0.3, signal.jsd);
  if (signal.falling.includes(t)) return 1 - Math.min(0.2, signal.jsd * 0.5);
  if (signal.stable.includes(t)) return 1.05;
  return 1;
}
function getDriftSummary() {
  const signal = getDriftSignal();
  if (!signal) return "";
  if (signal.driftLevel === "none") return "";
  const parts = [`drift=${signal.driftLevel}(${signal.jsd.toFixed(3)})`];
  if (signal.rising.length) parts.push(`\u2191${signal.rising.slice(0, 5).join(",")}`);
  if (signal.falling.length) parts.push(`\u2193${signal.falling.slice(0, 5).join(",")}`);
  return parts.join(" ");
}
function buildDistribution(topics) {
  const counts = {};
  for (const t of topics) counts[t] = (counts[t] || 0) + 1;
  const total = topics.length;
  if (total === 0) return {};
  const dist = {};
  for (const [k, v] of Object.entries(counts)) dist[k] = v / total;
  return dist;
}
function jensenShannonDivergence(p, q) {
  const allKeys = /* @__PURE__ */ new Set([...Object.keys(p), ...Object.keys(q)]);
  if (allKeys.size === 0) return 0;
  const m = {};
  for (const k of allKeys) {
    m[k] = 0.5 * ((p[k] || 0) + (q[k] || 0));
  }
  let klPM = 0;
  let klQM = 0;
  for (const k of allKeys) {
    const pk = p[k] || 0;
    const qk = q[k] || 0;
    const mk = m[k];
    if (pk > 0) klPM += pk * Math.log2(pk / mk);
    if (qk > 0) klQM += qk * Math.log2(qk / mk);
  }
  return Math.max(0, Math.min(1, 0.5 * klPM + 0.5 * klQM));
}
function saveDriftState() {
  try {
    debouncedSave(STATE_FILE, {
      shortWindow: _state.shortWindow.slice(-SHORT_CAP),
      longWindow: _state.longWindow.slice(-LONG_CAP),
      lastJSD: _state.lastJSD,
      lastCheck: _state.lastCheck
    });
  } catch {
  }
}
function loadDriftState() {
  try {
    if (existsSync(STATE_FILE)) {
      const raw = readFileSync(STATE_FILE, "utf-8");
      const data = JSON.parse(raw);
      if (data && Array.isArray(data.shortWindow) && Array.isArray(data.longWindow)) {
        _state = {
          shortWindow: data.shortWindow,
          longWindow: data.longWindow,
          lastJSD: data.lastJSD || 0,
          lastCheck: data.lastCheck || 0
        };
      }
    }
  } catch {
  }
}
loadDriftState();
export {
  getDriftSignal,
  getDriftSummary,
  getTopicRecallModifier,
  trackMessage
};
