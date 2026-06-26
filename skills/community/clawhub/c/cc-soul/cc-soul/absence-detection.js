import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { getProfile } from "./user-profiles.ts";
import { estimateTokens } from "./prompt-builder.ts";
import { memoryState, ensureMemoriesLoaded } from "./memory.ts";
const ABSENCE_PATH = resolve(DATA_DIR, "absence_detection.json");
const TOPIC_ABSENCE_PATH = resolve(DATA_DIR, "topic_absence.json");
const DAY_MS = 864e5;
const WEEK_MS = 7 * DAY_MS;
const TOPIC_STOP_WORDS = /* @__PURE__ */ new Set([
  "\u7684",
  "\u4E86",
  "\u662F",
  "\u5728",
  "\u6211",
  "\u4F60",
  "\u4ED6",
  "\u5979",
  "\u5B83",
  "\u4EEC",
  "\u8FD9",
  "\u90A3",
  "\u6709",
  "\u548C",
  "\u4E0D",
  "\u4E5F",
  "\u5C31",
  "\u90FD",
  "\u4F1A",
  "\u5230",
  "\u8BF4",
  "\u8981",
  "\u53BB",
  "\u80FD",
  "\u628A",
  "\u8BA9",
  "\u88AB",
  "\u4ECE",
  "\u4E0A",
  "\u4E0B",
  "\u4E2D",
  "\u5927",
  "\u5C0F",
  "\u5F88",
  "\u597D",
  "\u5417",
  "\u5462",
  "\u554A",
  "\u5427",
  "\u55EF",
  "\u54E6",
  "\u4EC0\u4E48",
  "\u600E\u4E48",
  "\u4E3A\u4EC0\u4E48",
  "\u53EF\u4EE5",
  "\u77E5\u9053",
  "\u89C9\u5F97",
  "\u4E00\u4E2A",
  "\u6CA1\u6709",
  "\u56E0\u4E3A",
  "\u6240\u4EE5",
  "\u8FD8\u662F",
  "\u4F46\u662F",
  "\u5982\u679C",
  "\u8FD9\u4E2A",
  "\u90A3\u4E2A",
  "\u4E00\u4E0B",
  "\u5DF2\u7ECF",
  "\u73B0\u5728",
  "\u65F6\u5019",
  "\u5E94\u8BE5",
  "the",
  "a",
  "an",
  "is",
  "are",
  "was",
  "were",
  "be",
  "been",
  "being",
  "i",
  "you",
  "he",
  "she",
  "it",
  "we",
  "they",
  "me",
  "my",
  "your",
  "and",
  "or",
  "but",
  "in",
  "on",
  "at",
  "to",
  "for",
  "of",
  "with",
  "that",
  "this",
  "do",
  "did",
  "have",
  "has",
  "had",
  "not",
  "no",
  "what",
  "how",
  "why",
  "can",
  "will",
  "just",
  "like",
  "know",
  "think"
]);
const ABSENCE_THRESHOLD_MS = 4 * 60 * 60 * 1e3;
const LONG_ABSENCE_MS = 3 * 24 * 60 * 60 * 1e3;
const VERY_LONG_ABSENCE_MS = 7 * 24 * 60 * 60 * 1e3;
function personalizedAbsenceThreshold(userId) {
  const record = state[userId];
  const avgGapMs = record?.avgAbsenceDuration || 144e5;
  return {
    short: Math.max(36e5, avgGapMs * 1.5),
    // 1.5 倍平均间隔（至少 1h）
    long: Math.max(864e5, avgGapMs * 8),
    // 8 倍（至少 1 天）
    veryLong: Math.max(2592e5, avgGapMs * 24)
    // 24 倍（至少 3 天）
  };
}
let state = {};
function loadAbsenceState() {
  state = loadJson(ABSENCE_PATH, {});
}
function save() {
  debouncedSave(ABSENCE_PATH, state);
}
function getRecord(userId) {
  if (!state[userId]) {
    state[userId] = {
      lastSeen: 0,
      isAbsent: false,
      absentSince: 0,
      welcomeShown: false,
      totalAbsences: 0,
      avgAbsenceDuration: 0
    };
  }
  return state[userId];
}
function heartbeatScanAbsence() {
  const now = Date.now();
  let changed = false;
  for (const [userId, record] of Object.entries(state)) {
    if (record.lastSeen <= 0) continue;
    const silenceDuration = now - record.lastSeen;
    const thresholds = personalizedAbsenceThreshold(userId);
    if (!record.isAbsent && silenceDuration > thresholds.short) {
      record.isAbsent = true;
      record.absentSince = record.lastSeen;
      record.welcomeShown = false;
      changed = true;
    }
  }
  if (changed) save();
  scanTopicAbsences();
}
function scanTopicAbsences() {
  const today = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const existing = loadJson(TOPIC_ABSENCE_PATH, { entries: [], lastRunDate: "" });
  if (existing.lastRunDate === today) return;
  const now = Date.now();
  const cutoff90d = now - 90 * DAY_MS;
  const cutoff2w = now - 2 * WEEK_MS;
  const cutoff8w = now - 8 * WEEK_MS;
  ensureMemoriesLoaded();
  const memories = memoryState.memories.filter((m) => m.ts >= cutoff90d);
  if (memories.length < 10) {
    debouncedSave(TOPIC_ABSENCE_PATH, { entries: [], lastRunDate: today });
    return;
  }
  const topicTimestamps = {};
  for (const mem of memories) {
    const cjkWords = mem.content.match(/[\u4e00-\u9fff]{2,6}/g) || [];
    const enWords = (mem.content.match(/[a-zA-Z]{3,}/g) || []).map((w) => w.toLowerCase());
    const words = [...cjkWords, ...enWords].filter((w) => !TOPIC_STOP_WORDS.has(w));
    const seen = /* @__PURE__ */ new Set();
    for (const w of words) {
      if (seen.has(w)) continue;
      seen.add(w);
      if (!topicTimestamps[w]) topicTimestamps[w] = [];
      topicTimestamps[w].push(mem.ts);
    }
  }
  const absences = [];
  for (const [topic, timestamps] of Object.entries(topicTimestamps)) {
    const recentCount = timestamps.filter((t) => t >= cutoff2w).length;
    if (recentCount > 0) continue;
    const olderCount = timestamps.filter((t) => t >= cutoff8w && t < cutoff2w).length;
    if (olderCount < 3) continue;
    const weekSpan = Math.max(1, (cutoff2w - cutoff8w) / WEEK_MS);
    const avgPerWeek = Math.round(olderCount / weekSpan * 10) / 10;
    const lastTs = Math.max(...timestamps);
    const lastSeenWeeksAgo = Math.round((now - lastTs) / WEEK_MS * 10) / 10;
    absences.push({ topic, avgPerWeek, lastSeenWeeksAgo, detectedAt: now });
  }
  absences.sort((a, b) => b.avgPerWeek - a.avgPerWeek);
  const result = {
    entries: absences.slice(0, 5),
    lastRunDate: today
  };
  debouncedSave(TOPIC_ABSENCE_PATH, result);
  if (result.entries.length > 0) {
    console.log(`[cc-soul][absence] detected ${result.entries.length} absent topics: ${result.entries.map((e) => e.topic).join(", ")}`);
  }
}
let _topicHintInjected = false;
function getTopicAbsenceAugment() {
  if (_topicHintInjected) return null;
  const data = loadJson(TOPIC_ABSENCE_PATH, { entries: [], lastRunDate: "" });
  if (data.entries.length === 0) return null;
  const e = data.entries[0];
  const content = `[\u7F3A\u5E2D\u68C0\u6D4B] \u7528\u6237\u6700\u8FD1\u6CA1\u518D\u63D0\u5230\u300C${e.topic}\u300D\uFF08\u4E4B\u524D\u5E73\u5747\u6BCF\u5468\u63D0${e.avgPerWeek}\u6B21\uFF0C\u5DF2\u7ECF${Math.round(e.lastSeenWeeksAgo)}\u5468\u6CA1\u63D0\u4E86\uFF09\u3002\u5982\u679C\u81EA\u7136\u7684\u8BDD\u53EF\u4EE5\u5173\u5FC3\u4E00\u4E0B`;
  _topicHintInjected = true;
  return { content, priority: 6, tokens: estimateTokens(content) };
}
function resetTopicAbsenceFlag() {
  _topicHintInjected = false;
}
function recordUserActivity(userId) {
  if (!userId) return 0;
  const record = getRecord(userId);
  const now = Date.now();
  let absenceDuration = 0;
  if (record.isAbsent && record.absentSince > 0) {
    absenceDuration = now - record.absentSince;
    if (record.totalAbsences === 0) {
      record.avgAbsenceDuration = absenceDuration;
    } else {
      record.avgAbsenceDuration = record.avgAbsenceDuration * 0.8 + absenceDuration * 0.2;
    }
    record.totalAbsences++;
  }
  record.lastSeen = now;
  record.isAbsent = false;
  record.absentSince = 0;
  save();
  return absenceDuration;
}
function getAbsenceAugment(userId) {
  if (!userId) return null;
  const record = state[userId];
  if (!record) return null;
  if (!record.isAbsent) return null;
  if (record.welcomeShown) return null;
  const now = Date.now();
  const absenceDuration = record.absentSince > 0 ? now - record.absentSince : 0;
  const thresholds = personalizedAbsenceThreshold(userId);
  if (absenceDuration < thresholds.short) return null;
  record.welcomeShown = true;
  save();
  const profile = getProfile(userId);
  const name = profile.displayName || "\u7528\u6237";
  let hint;
  const daysAway = Math.floor(absenceDuration / (24 * 60 * 60 * 1e3));
  const hoursAway = Math.floor(absenceDuration / (60 * 60 * 1e3));
  if (absenceDuration >= thresholds.veryLong) {
    hint = `[\u56DE\u5F52\u68C0\u6D4B] ${name}\u5DF2\u7ECF\u79BB\u5F00\u4E86${daysAway}\u5929\u3002\u8BF7\u81EA\u7136\u5730\u8868\u8FBE\u6B22\u8FCE\u56DE\u6765\uFF0C\u7B80\u77ED\u63D0\u53CA\u4E0A\u6B21\u804A\u5929\u7684\u8BDD\u9898\uFF08\u5982\u679C\u8BB0\u5F97\uFF09\uFF0C\u4E0D\u8981\u8FC7\u5EA6\u70ED\u60C5\u6216\u8BA9\u7528\u6237\u611F\u5230\u538B\u529B\u3002`;
  } else if (absenceDuration >= thresholds.long) {
    hint = `[\u56DE\u5F52\u68C0\u6D4B] ${name}\u6709${daysAway}\u5929\u6CA1\u6765\u4E86\u3002\u53EF\u4EE5\u8F7B\u677E\u5730\u6253\u4E2A\u62DB\u547C\uFF0C\u63D0\u5230"\u597D\u4E45\u4E0D\u89C1"\u5373\u53EF\uFF0C\u4E0D\u8981\u523B\u610F\u5217\u4E3E\u4E4B\u524D\u7684\u5BF9\u8BDD\u3002`;
  } else {
    hint = `[\u56DE\u5F52\u68C0\u6D4B] ${name}\u79BB\u5F00\u4E86\u7EA6${hoursAway}\u5C0F\u65F6\u3002\u5982\u679C\u5BF9\u8BDD\u81EA\u7136\u5141\u8BB8\uFF0C\u53EF\u4EE5\u7B80\u77ED\u95EE\u5019\u4E00\u4E0B\uFF0C\u4F46\u4E0D\u8981\u523B\u610F\u63D0\u53CA\u7F3A\u5E2D\u3002`;
  }
  if (record.totalAbsences >= 3 && record.avgAbsenceDuration > 0) {
    const avgDays = Math.round(record.avgAbsenceDuration / (24 * 60 * 60 * 1e3));
    if (avgDays >= 1) {
      hint += ` (\u7528\u6237\u5E73\u5747\u6BCF\u9694${avgDays}\u5929\u56DE\u6765\u4E00\u6B21\uFF0C\u8FD9\u662F\u6B63\u5E38\u8282\u594F)`;
    }
  }
  return {
    content: hint,
    priority: 7,
    // moderately high — greeting matters but shouldn't override core context
    tokens: estimateTokens(hint)
  };
}
function isUserAbsent(userId) {
  return state[userId]?.isAbsent ?? false;
}
function getAbsenceDuration(userId) {
  const record = state[userId];
  if (!record?.isAbsent || !record.absentSince) return 0;
  return Date.now() - record.absentSince;
}
const absenceDetectionModule = {
  id: "absence-detection",
  name: "\u79BB\u5F00\u68C0\u6D4B",
  priority: 40,
  init() {
    loadAbsenceState();
  },
  onHeartbeat() {
    heartbeatScanAbsence();
  },
  onPreprocessed(event) {
    const senderId = event?.context?.senderId;
    if (!senderId) return;
    recordUserActivity(senderId);
    const augment = getAbsenceAugment(senderId);
    if (augment) return [augment];
  }
};
export {
  absenceDetectionModule,
  getAbsenceAugment,
  getAbsenceDuration,
  getTopicAbsenceAugment,
  heartbeatScanAbsence,
  isUserAbsent,
  loadAbsenceState,
  recordUserActivity,
  resetTopicAbsenceFlag
};
