import { loadJson, debouncedSave, STATS_PATH } from "./persistence.ts";
import { spawnCLI } from "./cli.ts";
import { innerState, getRecentJournal } from "./inner-life.ts";
import { setNarrativeCache, narrativeCache } from "./prompt-builder.ts";
const CJK_TOPIC_REGEX = /[\u4e00-\u9fff]{3,}/g;
const CJK_WORD_REGEX = /[\u4e00-\u9fff]{2,4}/g;
let _readAloudPending = false;
function getReadAloudPending() {
  return _readAloudPending;
}
function setReadAloudPending(v) {
  _readAloudPending = v;
}
const metrics = {
  /** @deprecated Use stats.totalMessages — this getter avoids double counting */
  get totalMessages() {
    return stats.totalMessages;
  },
  avgResponseTimeMs: 0,
  recallCalls: 0,
  cliCalls: 0,
  augmentsInjected: 0,
  lastHeartbeat: 0,
  uptime: Date.now(),
  // internal: rolling average helper
  _responseTimeSum: 0,
  _responseTimeCount: 0,
  // ── Context compression tracking ──
  totalAugmentTokens: 0,
  // cumulative augment tokens injected
  totalConversationTokens: 0
  // estimated full-context tokens if no augment compression
};
function metricsRecordResponseTime(ms) {
  metrics._responseTimeSum += ms;
  metrics._responseTimeCount++;
  metrics.avgResponseTimeMs = Math.round(metrics._responseTimeSum / metrics._responseTimeCount);
}
function metricsRecordAugmentTokens(augmentTokens, conversationTokens) {
  metrics.totalAugmentTokens += augmentTokens;
  metrics.totalConversationTokens += conversationTokens;
}
function getCompressionRate() {
  const a = metrics.totalAugmentTokens;
  const c = metrics.totalConversationTokens;
  if (c === 0) return { rate: 0, augmentTokens: a, conversationTokens: c, saved: 0 };
  const rate = 1 - a / c;
  return { rate, augmentTokens: a, conversationTokens: c, saved: c - a };
}
function formatMetrics() {
  const uptimeH = ((Date.now() - metrics.uptime) / 36e5).toFixed(1);
  const lastHbAgo = metrics.lastHeartbeat > 0 ? Math.round((Date.now() - metrics.lastHeartbeat) / 6e4) : -1;
  const comp = getCompressionRate();
  const compLine = comp.conversationTokens > 0 ? `Context compression: ${(comp.rate * 100).toFixed(1)}% (saved ~${comp.saved} tokens)` : `Context compression: N/A (no data yet)`;
  return [
    `cc-soul Metrics`,
    `\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500`,
    `Uptime: ${uptimeH}h`,
    `Total messages: ${metrics.totalMessages}`,
    `Avg response time: ${metrics.avgResponseTimeMs}ms`,
    `Recall calls: ${metrics.recallCalls}`,
    `CLI calls: ${metrics.cliCalls}`,
    `Augments injected: ${metrics.augmentsInjected}`,
    compLine,
    `Last heartbeat: ${lastHbAgo >= 0 ? lastHbAgo + "min ago" : "never"}`
  ].join("\n");
}
const stats = {
  totalMessages: 0,
  firstSeen: 0,
  corrections: 0,
  positiveFeedback: 0,
  tasks: 0,
  topics: /* @__PURE__ */ new Set(),
  driftCount: 0
};
function loadStats() {
  const raw = loadJson(STATS_PATH, null);
  if (raw) {
    stats.totalMessages = raw.totalMessages || 0;
    stats.firstSeen = raw.firstSeen || Date.now();
    stats.corrections = raw.corrections || 0;
    stats.positiveFeedback = raw.positiveFeedback || 0;
    stats.tasks = raw.tasks || 0;
    stats.topics = new Set(raw.topics || []);
    stats.driftCount = raw.driftCount || 0;
  } else {
    stats.firstSeen = Date.now();
  }
}
function saveStats() {
  debouncedSave(STATS_PATH, {
    totalMessages: stats.totalMessages,
    firstSeen: stats.firstSeen,
    corrections: stats.corrections,
    positiveFeedback: stats.positiveFeedback,
    tasks: stats.tasks,
    topics: [...stats.topics].slice(-100),
    driftCount: stats.driftCount
  });
}
function getStats() {
  return { totalMessages: stats.totalMessages, corrections: stats.corrections, firstSeen: stats.firstSeen };
}
let soulMode = false;
let soulModeSpeaker = "";
function getSoulMode() {
  return { active: soulMode, speaker: soulModeSpeaker };
}
function setSoulMode(active, speaker) {
  soulMode = active;
  soulModeSpeaker = speaker || "";
  console.log(`[cc-soul][soul-mode] ${active ? `ON (speaker: ${soulModeSpeaker})` : "OFF"}`);
}
const sessionStates = /* @__PURE__ */ new Map();
const MAX_SESSIONS = 20;
function getSessionState(sessionKey) {
  let state = sessionStates.get(sessionKey);
  if (!state) {
    state = { lastPrompt: "", lastResponseContent: "", lastSenderId: "", lastChannelId: "", lastAugmentsUsed: [], lastRecalledContents: [], lastMatchedRuleTexts: [], lastAccessed: Date.now(), turnCount: 0, lastTopicKeywords: [], lastQualityScore: -1 };
    sessionStates.set(sessionKey, state);
    if (sessionStates.size > MAX_SESSIONS) {
      const oldestKey = sessionStates.keys().next().value;
      if (oldestKey !== void 0 && oldestKey !== sessionKey) sessionStates.delete(oldestKey);
    }
  } else {
    sessionStates.delete(sessionKey);
    state.lastAccessed = Date.now();
    sessionStates.set(sessionKey, state);
  }
  return state;
}
const TOPIC_SHIFT_MIN_TURNS = 3;
const TOPIC_SHIFT_THRESHOLD = 0.15;
const GREETING_PATTERNS = /^(你好|hi|hello|hey|嗨|哈喽|早|晚上好|下午好|在吗|在不在)/i;
function extractTopicKeywords(msg) {
  const cjk = msg.match(/[\u4e00-\u9fff]{2,}/g) || [];
  const latin = msg.match(/[a-zA-Z]{4,}/gi) || [];
  return [...cjk, ...latin.map((w) => w.toLowerCase())];
}
function keywordOverlap(a, b) {
  if (a.length === 0 || b.length === 0) return 0;
  const setA = new Set(a);
  const setB = new Set(b);
  let intersection = 0;
  for (const w of setA) if (setB.has(w)) intersection++;
  const union = (/* @__PURE__ */ new Set([...a, ...b])).size;
  return union > 0 ? intersection / union : 0;
}
function detectTopicShiftAndReset(session, userMsg, sessionKey) {
  const currentKeywords = extractTopicKeywords(userMsg);
  const isGreeting = GREETING_PATTERNS.test(userMsg.trim()) && userMsg.trim().length < 20;
  const shouldReset = session.turnCount >= TOPIC_SHIFT_MIN_TURNS && (isGreeting || session.lastTopicKeywords.length > 0 && keywordOverlap(currentKeywords, session.lastTopicKeywords) < TOPIC_SHIFT_THRESHOLD);
  if (currentKeywords.length > 0) {
    session.lastTopicKeywords = currentKeywords.slice(0, 20);
  }
  session.turnCount++;
  if (shouldReset) {
    resetCliSession(sessionKey);
    session.turnCount = 0;
    session.lastTopicKeywords = currentKeywords.slice(0, 20);
    return true;
  }
  return false;
}
async function resetCliSession(sessionKey) {
  try {
    const { readFileSync, writeFileSync } = await import("fs");
    const { resolve } = await import("path");
    const home = process.env.HOME || process.env.USERPROFILE || "";
    const parts = sessionKey.split(":");
    const agentId = parts.length >= 2 ? parts[1] : "cc";
    const storePath = resolve(home, ".openclaw", "agents", agentId, "sessions", "sessions.json");
    const raw = readFileSync(storePath, "utf-8");
    const store = JSON.parse(raw);
    const entry = store[sessionKey];
    if (!entry) return;
    let changed = false;
    if (entry.claudeCliSessionId) {
      delete entry.claudeCliSessionId;
      changed = true;
    }
    if (entry.cliSessionIds) {
      for (const key of Object.keys(entry.cliSessionIds)) {
        if (key.includes("claude")) {
          delete entry.cliSessionIds[key];
          changed = true;
        }
      }
      if (Object.keys(entry.cliSessionIds).length === 0) {
        delete entry.cliSessionIds;
      }
    }
    if (changed) {
      entry.updatedAt = Date.now();
      writeFileSync(storePath, JSON.stringify(store, null, 2));
      console.log(`[cc-soul][topic-shift] CLI session reset for ${sessionKey}`);
    }
  } catch (err) {
    console.log(`[cc-soul][topic-shift] reset failed: ${err}`);
  }
}
let lastActiveSessionKey = "_default";
function getLastActiveSessionKey() {
  return lastActiveSessionKey;
}
function setLastActiveSessionKey(v) {
  lastActiveSessionKey = v;
}
import { resolve as _resolve } from "path";
import { homedir as _homedir } from "os";
import { existsSync as _existsSync, writeFileSync as _writeFileSync } from "fs";
const _privacyLockPath = _resolve(_homedir(), ".openclaw/plugins/cc-soul/data/.privacy-mode");
let privacyMode = (() => {
  try {
    return _existsSync(_privacyLockPath);
  } catch {
    return false;
  }
})();
function getPrivacyMode() {
  return privacyMode;
}
function setPrivacyMode(v) {
  privacyMode = v;
  try {
    if (v) _writeFileSync(_privacyLockPath, "1", "utf-8");
    else try {
      import("fs").then(({ unlinkSync }) => unlinkSync(_privacyLockPath)).catch(() => {
      });
    } catch {
    }
  } catch {
  }
}
const shortcuts = {
  "s": "\u529F\u80FD\u72B6\u6001",
  "m": "\u8BB0\u5FC6\u56FE\u8C31",
  "?": "\u6700\u8FD1\u5728\u804A\u4EC0\u4E48",
  "!": "\u7D27\u6025\u6A21\u5F0F"
};
let initialized = false;
function getInitialized() {
  return initialized;
}
function setInitialized(v) {
  initialized = v;
}
let heartbeatRunning = false;
function getHeartbeatRunning() {
  return heartbeatRunning;
}
function setHeartbeatRunning(v) {
  heartbeatRunning = v;
}
let heartbeatStartedAt = 0;
function getHeartbeatStartedAt() {
  return heartbeatStartedAt;
}
function setHeartbeatStartedAt(v) {
  heartbeatStartedAt = v;
}
let heartbeatInterval = null;
function getHeartbeatInterval() {
  return heartbeatInterval;
}
function setHeartbeatInterval(v) {
  heartbeatInterval = v;
}
const NARRATIVE_CACHE_MS = 3600 * 1e3;
function refreshNarrativeAsync() {
  if (narrativeCache.text && Date.now() - narrativeCache.ts < NARRATIVE_CACHE_MS) return;
  const daysKnown = Math.max(1, Math.floor((Date.now() - stats.firstSeen) / 864e5));
  const facts = [
    `\u4E92\u52A8${stats.totalMessages}\u6B21\uFF0C\u8BA4\u8BC6${daysKnown}\u5929`,
    `\u88AB\u7EA0\u6B63${stats.corrections}\u6B21\uFF0C\u5B8C\u6210${stats.tasks}\u4E2A\u4EFB\u52A1`,
    innerState.userModel ? `\u7406\u89E3: ${innerState.userModel.slice(0, 200)}` : "",
    getRecentJournal(3)
  ].filter(Boolean).join("\n");
  const prompt = `\u6839\u636E\u4EE5\u4E0B\u4FE1\u606F\uFF0C\u7528\u7B2C\u4E00\u4EBA\u79F0\u51992-3\u53E5\u8BDD\u63CF\u8FF0\u4F60\u548C\u8FD9\u4E2A\u7528\u6237\u7684\u5173\u7CFB\u3002\u8981\u6709\u611F\u60C5\uFF0C\u50CF\u5199\u7ED9\u81EA\u5DF1\u770B\u7684\u65E5\u8BB0\u3002\u4E0D\u8981\u8BF4"\u4F5C\u4E3AAI"\u3002

${facts}`;
  spawnCLI(prompt, (output) => {
    if (output && output.length > 20) {
      setNarrativeCache(output.slice(0, 500));
    }
  });
}
export {
  CJK_TOPIC_REGEX,
  CJK_WORD_REGEX,
  detectTopicShiftAndReset,
  formatMetrics,
  getCompressionRate,
  getHeartbeatInterval,
  getHeartbeatRunning,
  getHeartbeatStartedAt,
  getInitialized,
  getLastActiveSessionKey,
  getPrivacyMode,
  getReadAloudPending,
  getSessionState,
  getSoulMode,
  getStats,
  loadStats,
  metrics,
  metricsRecordAugmentTokens,
  metricsRecordResponseTime,
  refreshNarrativeAsync,
  saveStats,
  setHeartbeatInterval,
  setHeartbeatRunning,
  setHeartbeatStartedAt,
  setInitialized,
  setLastActiveSessionKey,
  setPrivacyMode,
  setReadAloudPending,
  setSoulMode,
  shortcuts,
  stats
};
