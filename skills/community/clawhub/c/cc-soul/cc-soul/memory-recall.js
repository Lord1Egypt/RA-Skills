import { resolve } from "path";
import { existsSync } from "fs";
import { homedir } from "os";
import { DATA_DIR, loadJson } from "./persistence.ts";
import { getParam } from "./auto-tune.ts";
import { findMentionedEntities, getRelatedEntities, graphWalkRecall } from "./graph.ts";
import {
  memoryState,
  scopeIndex,
  saveMemories,
  syncToSQLite,
  getLazyModule,
  bayesBoost,
  bayesPenalize,
  bayesCorrect,
  coreMemories
} from "./memory.ts";
import { queryFacts } from "./fact-store.ts";
import {
  trigrams,
  trigramSimilarity,
  expandQueryWithSynonyms,
  timeDecay,
  onCacheEvent,
  tokenize as unifiedTokenize,
  WORD_PATTERN
} from "./memory-utils.ts";
import { getTemporalSuccessors as _getTemporalSuccessors } from "./aam.ts";
import { positiveEvidence as _posEvidence, negativeEvidence as _negEvidence } from "./confidence-cascade.ts";
onCacheEvent("memory_added", () => {
  idfCache = null;
  lastIdfBuildTs = 0;
});
onCacheEvent("memory_deleted", () => {
  idfCache = null;
  lastIdfBuildTs = 0;
  _bm25TokenCache.clear();
});
onCacheEvent("consolidation", () => {
  idfCache = null;
  lastIdfBuildTs = 0;
  _bm25TokenCache.clear();
});
onCacheEvent("identity_changed", () => {
  idfCache = null;
  lastIdfBuildTs = 0;
});
onCacheEvent("fact_updated", () => {
  idfCache = null;
  lastIdfBuildTs = 0;
});
onCacheEvent("correction_received", () => {
  _bm25TokenCache.clear();
});
const DATE_PATTERNS = [
  { re: /昨天|yesterday/gi, replacer: () => {
    const d = new Date(Date.now() - 864e5);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  } },
  { re: /前天/g, replacer: () => {
    const d = new Date(Date.now() - 2 * 864e5);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  } },
  { re: /今天|today/gi, replacer: () => {
    const d = /* @__PURE__ */ new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  } },
  { re: /明天|tomorrow/gi, replacer: () => {
    const d = new Date(Date.now() + 864e5);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  } },
  { re: /上周|last week/gi, replacer: () => "7\u5929\u524D" },
  { re: /上个月|last month/gi, replacer: () => "30\u5929\u524D" }
];
function getContentForRecall(mem) {
  if (mem.contentNormalized !== void 0) return mem.contentNormalized;
  let text = mem.content;
  let changed = false;
  for (const { re, replacer } of DATE_PATTERNS) {
    if (re.test(text)) {
      text = text.replace(re, replacer);
      changed = true;
    }
  }
  if (changed) {
    mem.contentNormalized = text;
  }
  return mem.contentNormalized ?? mem.content;
}
const _contentMap = /* @__PURE__ */ new Map();
const _memLookup = /* @__PURE__ */ new Map();
const _primingCache = /* @__PURE__ */ new Map();
function updatePrimingCache(userMsg) {
  const now = Date.now();
  const words = userMsg.match(WORD_PATTERN.CJK2_EN3) || [];
  for (const w of words) _primingCache.set(w.toLowerCase(), now);
  if (_primingCache.size > 200) {
    for (const [k, ts] of _primingCache) {
      if (now - ts > 10 * 60 * 1e3) _primingCache.delete(k);
    }
  }
}
const _predictivePrimingCache = /* @__PURE__ */ new Map();
const PREDICTIVE_PRIMING_WINDOW_MS = 5 * 60 * 1e3;
const PREDICTIVE_PRIMING_MAX = 30;
function predictivePrime(recalledMemories, allMemories) {
  if (recalledMemories.length === 0 || allMemories.length === 0) return;
  const recalledWords = /* @__PURE__ */ new Set();
  for (const m of recalledMemories) {
    const words = m.content.match(WORD_PATTERN.CJK2_EN3) || [];
    for (const w of words) recalledWords.add(w.toLowerCase());
  }
  const predictedWords = /* @__PURE__ */ new Map();
  for (const w of recalledWords) {
    try {
      const successors = _getTemporalSuccessors(w, 3);
      for (const s of successors) {
        const existing = predictedWords.get(s.word) || 0;
        if (s.count > existing) predictedWords.set(s.word, s.count);
      }
    } catch {
    }
  }
  if (predictedWords.size === 0) return;
  const now = Date.now();
  for (const [k, v] of _predictivePrimingCache) {
    if (now - v.primedAt > PREDICTIVE_PRIMING_WINDOW_MS) _predictivePrimingCache.delete(k);
  }
  const recalledContentSet = new Set(recalledMemories.map((m) => m.content));
  const scored = [];
  for (const mem of allMemories) {
    if (!mem || !mem.content || recalledContentSet.has(mem.content)) continue;
    const tokens = bm25Tokenize(getContentForRecall(mem));
    if (tokens.length === 0) continue;
    let matchScore = 0;
    for (const t of tokens) {
      const succCount = predictedWords.get(t);
      if (succCount) matchScore += succCount;
    }
    if (matchScore > 0) {
      const relevance = Math.min(1, matchScore / (tokens.length * 2));
      scored.push({ content: mem.content, relevance });
    }
  }
  scored.sort((a, b) => b.relevance - a.relevance);
  const topPrimed = scored.slice(0, PREDICTIVE_PRIMING_MAX);
  for (const s of topPrimed) {
    _predictivePrimingCache.set(s.content, { predictedRelevance: s.relevance, primedAt: now });
  }
  if (topPrimed.length > 0) {
    try {
      require("./decision-log.ts").logDecision("predictive_prime", `${topPrimed.length} memories`, `predicted_words=${predictedWords.size}, top="${topPrimed[0].content.slice(0, 30)}"`);
    } catch {
    }
  }
}
const COREF_QUERY_PRONOUNS = /他|她|它|这个|那个/;
const COREF_QUERY_PLURAL = /他们|她们|它们/;
function expandQueryWithCoreference(query, chatHistory) {
  if (!COREF_QUERY_PRONOUNS.test(query) || COREF_QUERY_PLURAL.test(query)) return query;
  let entities = [];
  try {
    const { findMentionedEntities: fme } = require("./graph.ts");
    const recentText = chatHistory.slice(-3).map((h) => h.user).join(" ");
    entities = fme(recentText);
  } catch {
  }
  if (entities.length === 0 || entities.length > 3) return query;
  const expanded = query + " " + entities.join(" ");
  try {
    require("./decision-log.ts").logDecision("coreference_recall", query.slice(0, 30), `expanded: +${entities.join(",")}`);
  } catch {
  }
  return expanded;
}
function extractTimeRange(query) {
  const now = Date.now();
  const DAY = 864e5;
  if (/昨天|yesterday/i.test(query)) return { fromMs: now - 2 * DAY, toMs: now - DAY };
  if (/前天/.test(query)) return { fromMs: now - 3 * DAY, toMs: now - 2 * DAY };
  if (/上周|last week/i.test(query)) return { fromMs: now - 14 * DAY, toMs: now - 7 * DAY };
  if (/上个月|last month/i.test(query)) return { fromMs: now - 60 * DAY, toMs: now - 30 * DAY };
  if (/最近|recently/i.test(query)) return { fromMs: now - 7 * DAY, toMs: now };
  if (/今天|today/i.test(query)) return { fromMs: now - DAY, toMs: now };
  if (/明天|tomorrow/i.test(query)) return { fromMs: now, toMs: now + DAY };
  const daysAgo = query.match(/(\d+)\s*(?:天前|days?\s*ago)/i);
  if (daysAgo) {
    const d = parseInt(daysAgo[1]);
    return { fromMs: now - (d + 1) * DAY, toMs: now - (d - 1 < 0 ? 0 : d - 1) * DAY };
  }
  const weeksAgo = query.match(/(\d+)\s*(?:周前|weeks?\s*ago)/i);
  if (weeksAgo) {
    const w = parseInt(weeksAgo[1]);
    return { fromMs: now - (w + 1) * 7 * DAY, toMs: now - (w - 1 < 0 ? 0 : w - 1) * 7 * DAY };
  }
  return null;
}
const ROUTE_THRESHOLD = 800;
const ROUTE_MIN_CANDIDATES = 150;
function routeMemories(memories, query, userId) {
  if (memories.length < ROUTE_THRESHOLD) return memories;
  let candidates = memories;
  if (userId) {
    const userMems = candidates.filter((m) => !m.userId || m.userId === userId);
    if (userMems.length > 0) candidates = userMems;
  }
  const timeRange = extractTimeRange(query);
  if (timeRange) {
    const timeMems = candidates.filter((m) => m.ts >= timeRange.fromMs && m.ts <= timeRange.toMs);
    if (timeMems.length >= 5) candidates = timeMems;
  }
  if (candidates.length > ROUTE_THRESHOLD) {
    try {
      const { findMentionedEntities: findMentionedEntities2 } = require("./graph.ts");
      const entities = findMentionedEntities2(query);
      if (entities.length > 0) {
        const entityMems = candidates.filter((m) => entities.some((e) => m.content?.includes(e)));
        const minKeep = Math.max(ROUTE_MIN_CANDIDATES, Math.floor(candidates.length * 0.3));
        if (entityMems.length >= minKeep) candidates = entityMems;
      }
    } catch {
    }
  }
  if (candidates.length < ROUTE_MIN_CANDIDATES && memories.length > ROUTE_MIN_CANDIDATES) {
    const candidateSet = new Set(candidates);
    const recent = memories.filter((m) => !candidateSet.has(m)).sort((a, b) => (b.ts || 0) - (a.ts || 0)).slice(0, ROUTE_MIN_CANDIDATES - candidates.length);
    candidates = [...candidates, ...recent];
  }
  return candidates;
}
function updateRecallIndex(mem) {
  _contentMap.set(mem.content, mem);
  _memLookup.set(`${mem.content}\0${mem.ts}`, mem);
}
function rebuildRecallIndex(memories) {
  _contentMap.clear();
  _memLookup.clear();
  for (const m of memories) {
    _contentMap.set(m.content, m);
    _memLookup.set(`${m.content}\0${m.ts}`, m);
  }
}
const AB_INTERVAL = 20;
const AB_TESTABLE_CHANNELS = ["rrfGraph", "rrfDirichlet", "rrfScope"];
let _abCounter = 0;
let _abDisabledChannel = null;
let _abEngagementWithChannel = [];
let _abEngagementWithout = [];
function tickABExperiment() {
  _abCounter++;
  if (_abCounter % AB_INTERVAL === 0) {
    if (_abDisabledChannel && _abEngagementWithout.length >= 5) {
      const withAvg = _abEngagementWithChannel.length > 0 ? _abEngagementWithChannel.reduce((s, v) => s + v, 0) / _abEngagementWithChannel.length : 0.5;
      const withoutAvg = _abEngagementWithout.reduce((s, v) => s + v, 0) / _abEngagementWithout.length;
      const diff = withAvg - withoutAvg;
      try {
        const { logDecision } = require("./decision-log.ts");
        logDecision(
          "ab_test",
          _abDisabledChannel,
          `with=${withAvg.toFixed(3)}, without=${withoutAvg.toFixed(3)}, diff=${diff.toFixed(3)}, ${Math.abs(diff) < 0.05 ? "\u4E0D\u663E\u8457" : diff > 0 ? "\u901A\u9053\u6709\u7528" : "\u901A\u9053\u53EF\u80FD\u6709\u5BB3"}`
        );
      } catch {
      }
    }
    _abDisabledChannel = AB_TESTABLE_CHANNELS[Math.floor(Math.random() * AB_TESTABLE_CHANNELS.length)];
    _abEngagementWithChannel = [];
    _abEngagementWithout = [];
  }
}
function recordABEngagement(engagementScore) {
  if (_abDisabledChannel) {
    _abEngagementWithout.push(engagementScore);
  } else {
    _abEngagementWithChannel.push(engagementScore);
  }
  if (engagementScore > 0.3) {
    try {
      const { getRecentTrace } = require("./activation-field.ts");
      const { logDecision } = require("./decision-log.ts");
      const recent = getRecentTrace();
      if (recent?.traces?.length) {
        const topTrace = recent.traces[0];
        const topStep = topTrace.path?.[0];
        if (topStep) {
          logDecision(
            "ab_test",
            `engaged_via_${topStep.via}`,
            `engagement=${engagementScore.toFixed(3)}, disabled=${_abDisabledChannel || "none"}`,
            { via: topStep.via, score: topTrace.score }
          );
        }
      }
    } catch {
    }
  }
}
let recallStats = { total: 0, successful: 0, rate: 0 };
function getRecallRate() {
  const rate = recallStats.total > 0 ? recallStats.successful / recallStats.total * 100 : recallStats.rate * 100;
  return { total: recallStats.total, successful: recallStats.successful, rate };
}
const recallImpact = /* @__PURE__ */ new Map();
let _lastImpactCleanup = 0;
let _smartForgetMod = null;
function getSmartForget() {
  if (!_smartForgetMod) {
    try {
      _smartForgetMod = require("./smart-forget.ts");
    } catch {
      import("./smart-forget.ts").then((m) => {
        _smartForgetMod = m;
      }).catch((e) => {
        console.error(`[cc-soul] module load failed (smart-forget): ${e.message}`);
      });
    }
  }
  return _smartForgetMod;
}
function trackRecallImpact(recalledContents, qualityScore) {
  const sf = getSmartForget();
  if (sf) {
    const n = recalledContents.length;
    if (qualityScore >= 5) {
      for (let i = 0; i < n; i++) sf.recordRecallHit();
    } else {
      for (let i = 0; i < n; i++) sf.recordRecallMiss();
    }
  }
  for (const content of recalledContents) {
    const key = content.slice(0, 80);
    const entry = recallImpact.get(key) || { recalled: 0, helpedQuality: 0, avgImpact: 0 };
    entry.recalled++;
    entry.helpedQuality += qualityScore;
    entry.avgImpact = entry.helpedQuality / entry.recalled;
    recallImpact.set(key, entry);
    if (entry.recalled >= 2) {
      const keyPrefix = key.slice(0, 40);
      let mem = _contentMap.get(key);
      if (!mem || mem.scope === "expired") {
        mem = void 0;
        for (const [content2, m] of _contentMap) {
          if (content2.startsWith(keyPrefix) && m.scope !== "expired") {
            mem = m;
            break;
          }
        }
      }
      if (mem) {
        if (qualityScore >= 7) {
          bayesBoost(mem, 1);
        } else if (qualityScore <= 3) {
          bayesPenalize(mem, 1);
          if (mem.confidence < 0.2) {
            console.log(`[cc-soul][recall-feedback] low-quality memory demoted: "${content.slice(0, 50)}" (avgImpact=${entry.avgImpact.toFixed(1)})`);
          }
        }
        syncToSQLite(mem, { confidence: mem.confidence });
      }
    }
  }
  if (recallImpact.size > 500 && Date.now() - _lastImpactCleanup > 6e4) {
    _lastImpactCleanup = Date.now();
    const sorted = [...recallImpact.entries()].sort((a, b) => a[1].recalled - b[1].recalled);
    const deleteCount = recallImpact.size - 300;
    for (const [key] of sorted.slice(0, deleteCount)) recallImpact.delete(key);
  }
}
function getRecallImpactBoost(content) {
  const key = content.slice(0, 80);
  const entry = recallImpact.get(key);
  if (!entry || entry.recalled < 3) return 1;
  if (entry.avgImpact >= 7) return 1.3;
  if (entry.avgImpact >= 5) return 1.1;
  if (entry.avgImpact < 3) return 0.7;
  return 1;
}
let idfCache = null;
let avgDocLenCache = null;
let lastIdfBuildTs = 0;
function getBM25K1() {
  return getParam("memory.bm25_k1");
}
function getBM25B() {
  return getParam("memory.bm25_b");
}
const BM25_STOP_WORDS = /* @__PURE__ */ new Set([..."\u7684\u4E86\u662F\u5728\u6211\u4F60\u4ED6\u4E0D\u6709\u8FD9\u90A3\u5C31\u4E5F\u548C\u4F46".split(""), "the", "a", "an", "is", "are", "was", "were", "to", "for", "in", "on", "at", "and", "or", "but", "not"]);
function bm25Tokenize(text) {
  return unifiedTokenize(text, "bm25");
}
const IDF_CACHE_TTL = 3e5;
function buildIDF() {
  if (idfCache && idfCache.size > 0 && Date.now() - lastIdfBuildTs < IDF_CACHE_TTL) return idfCache;
  const df = /* @__PURE__ */ new Map();
  const N = memoryState.memories.length || 1;
  let totalDocLen = 0;
  for (const mem of memoryState.memories) {
    const words = bm25Tokenize(getContentForRecall(mem));
    totalDocLen += words.length;
    const unique = new Set(words);
    for (const w of unique) {
      df.set(w, (df.get(w) || 0) + 1);
    }
  }
  const idf = /* @__PURE__ */ new Map();
  for (const [word, count] of df) {
    idf.set(word, Math.log(N / (1 + count)));
  }
  idfCache = idf;
  avgDocLenCache = N > 0 ? totalDocLen / N : 1;
  lastIdfBuildTs = Date.now();
  return idf;
}
const _bm25TokenCache = /* @__PURE__ */ new Map();
function _getDocTokens(doc) {
  const cached = _bm25TokenCache.get(doc);
  if (cached) {
    _bm25TokenCache.delete(doc);
    _bm25TokenCache.set(doc, cached);
    return cached;
  }
  const words = bm25Tokenize(doc);
  const tf = /* @__PURE__ */ new Map();
  for (const w of words) tf.set(w, (tf.get(w) || 0) + 1);
  const entry = { words, tf };
  _bm25TokenCache.set(doc, entry);
  if (_bm25TokenCache.size > 2e3) {
    const evict = Math.floor(_bm25TokenCache.size * 0.2);
    const iter = _bm25TokenCache.keys();
    for (let i = 0; i < evict; i++) {
      const k = iter.next().value;
      if (k !== void 0) _bm25TokenCache.delete(k);
    }
  }
  return entry;
}
function invalidateBM25TokenCache() {
  _bm25TokenCache.clear();
}
function mmrRerank(candidates, topN, _lambda = 0.7) {
  if (candidates.length <= topN) return candidates;
  const MAX_PER_TOPIC = 3;
  const topicCounts = /* @__PURE__ */ new Map();
  const selected = [];
  for (const mem of candidates) {
    if (selected.length >= topN) break;
    const topicKey = (mem.scope || "other") + "|" + (mem.content || "").slice(0, 10);
    const count = topicCounts.get(topicKey) || 0;
    if (count >= MAX_PER_TOPIC) continue;
    topicCounts.set(topicKey, count + 1);
    selected.push(mem);
  }
  return selected;
}
function recallWithScores(msg, topN = 3, userId, channelId, moodCtx) {
  if (memoryState.memories.length === 0 || !msg) return [];
  const cjkMinLen = msg.length < 10 ? 1 : 2;
  const cjkPattern = cjkMinLen === 1 ? /[\u4e00-\u9fff]+/gi : /[\u4e00-\u9fff]{2,}/gi;
  const rawWords = new Set(
    (msg.match(cjkPattern) || []).concat(msg.match(/[a-z]{3,}/gi) || []).map((w) => w.toLowerCase())
  );
  if (msg.length < 15) {
    const QUERY_EXPAND = {
      "\u4F4F": ["\u4F4F\u5728", "\u5317\u4EAC", "\u4E0A\u6D77", "\u6DF1\u5733", "\u5E7F\u5DDE", "\u676D\u5DDE", "\u5730\u5740"],
      "\u54EA": [],
      // 疑问词不扩展
      "\u5BA0\u7269": ["\u732B", "\u72D7", "\u517B\u4E86", "\u517B"],
      "\u7535\u8111": ["macbook", "mac", "thinkpad", "\u7B14\u8BB0\u672C", "\u53F0\u5F0F"],
      "\u996E\u6599": ["\u5496\u5561", "\u8336", "\u9152", "\u559D"],
      "\u559D": ["\u5496\u5561", "\u8336", "\u9152", "\u996E\u6599"],
      "\u5DE5\u4F5C": ["\u516C\u53F8", "\u4E0A\u73ED", "\u5C31\u804C", "\u5B57\u8282", "\u817E\u8BAF", "\u963F\u91CC"],
      "\u8BA8\u538C": ["\u4E0D\u559C\u6B22", "\u4E0D\u60F3", "\u53D7\u4E0D\u4E86"],
      "\u8DD1\u6B65": ["\u8FD0\u52A8", "\u953B\u70BC", "\u516C\u91CC"],
      "live": ["\u4F4F\u5728", "location", "city", "moved"],
      "pet": ["cat", "dog", "\u732B", "\u72D7", "\u517B\u4E86"],
      "work": ["company", "job", "office", "\u516C\u53F8", "\u4E0A\u73ED"],
      "hate": ["dislike", "don't like", "\u8BA8\u538C", "\u4E0D\u559C\u6B22"],
      "like": ["love", "enjoy", "prefer", "\u559C\u6B22"],
      "family": ["daughter", "son", "wife", "husband", "\u5973\u513F", "\u513F\u5B50"],
      "computer": ["macbook", "mac", "laptop", "desktop", "\u7535\u8111"],
      "drink": ["coffee", "tea", "\u5496\u5561", "\u8336"],
      "run": ["exercise", "workout", "running", "\u8DD1\u6B65", "\u8FD0\u52A8"]
    };
    for (const w of [...rawWords]) {
      const expand = QUERY_EXPAND[w];
      if (expand) for (const e of expand) rawWords.add(e);
    }
  }
  if (rawWords.size === 0) return [];
  const mentionedEntities = findMentionedEntities(msg);
  const relatedEntities = mentionedEntities.length > 0 ? getRelatedEntities(mentionedEntities, 2, 8) : [];
  const expansionWords = /* @__PURE__ */ new Set();
  for (const entity of relatedEntities) {
    const words = (entity.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    for (const w of words) {
      if (!rawWords.has(w)) expansionWords.add(w);
    }
  }
  const queryWords = expandQueryWithSynonyms(rawWords);
  let idf = null;
  let avgDocLen = 1;
  let queryTrigrams = null;
  let bm25QueryTokens = null;
  const SKIP_SCOPES = /* @__PURE__ */ new Set(["expired", "decayed"]);
  const activeMemories = [];
  for (const [scope, mems] of scopeIndex) {
    if (SKIP_SCOPES.has(scope)) continue;
    for (const m of mems) {
      const eng = m.injectionEngagement ?? 0;
      const miss = m.injectionMiss ?? 0;
      if (miss >= 5 && eng === 0) continue;
      activeMemories.push(m);
    }
  }
  const _scopeBoostPref = getParam("recall.scope_boost_preference");
  const _scopeBoostCorr = getParam("recall.scope_boost_correction");
  const _emotionBoostImportant = getParam("recall.emotion_boost_important");
  const _emotionBoostPainful = getParam("recall.emotion_boost_painful");
  const _emotionBoostWarm = getParam("recall.emotion_boost_warm");
  const _userBoostSame = getParam("recall.user_boost_same");
  const _userBoostOther = getParam("recall.user_boost_other");
  const _tierWeightHot = getParam("recall.tier_weight_hot");
  const _tierWeightWarm = getParam("recall.tier_weight_warm");
  const _tierWeightCool = getParam("recall.tier_weight_cool");
  const _tierWeightCold = getParam("recall.tier_weight_cold");
  const _consolidatedBoost = getParam("recall.consolidated_boost");
  const _reflexionBoost = getParam("recall.reflexion_boost");
  const _flashbulbHigh = getParam("recall.flashbulb_high");
  const _flashbulbMedium = getParam("recall.flashbulb_medium");
  const scored = [];
  for (const mem of activeMemories) {
    const vis = mem.visibility || "global";
    if (vis === "channel" && channelId && mem.channelId && mem.channelId !== channelId) continue;
    if (vis === "private" && userId && mem.userId && mem.userId !== userId) continue;
    if (mem.supersededBy && mem.scope === "historical") {
      if (!/之前|以前|曾经|过去|原来|上次|before|previously|used to|in the past|last time/i.test(msg)) continue;
    }
    let sim = 0;
    const memContent = getContentForRecall(mem);
    const memWords = new Set(
      (memContent.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase())
    );
    if (mem.tags && mem.tags.length > 0) {
      const tagStr = mem.tags.join("|").toLowerCase();
      let tagHits = 0;
      for (const qw of queryWords) {
        if (tagStr.includes(qw)) {
          tagHits++;
          continue;
        }
        if (mem.tags.some((t) => qw.includes(t))) tagHits++;
      }
      sim = tagHits / Math.max(1, queryWords.size);
    }
    if (sim < 0.3) {
      if (!idf) {
        idf = buildIDF();
        avgDocLen = avgDocLenCache || 1;
      }
      const QUESTION_STOPWORDS = /* @__PURE__ */ new Set(["\u4EC0\u4E48", "\u600E\u4E48", "\u54EA\u4E2A", "\u54EA\u91CC", "\u591A\u5C11", "\u4E3A\u4EC0\u4E48", "\u662F\u5426", "\u6709\u6CA1\u6709", "\u662F\u4E0D\u662F", "\u8FD8", "\u8BB0\u5F97", "\u77E5\u9053", "\u53EB", "what", "who", "where", "when", "why", "how", "which", "does", "did", "the", "a", "an", "is", "are", "was", "were", "to", "for", "in", "on", "at", "and", "or", "but", "not"]);
      const BM25_DELTA = 1;
      let matchedWeight = 0, totalWeight = 0;
      for (const qw of queryWords) {
        if (QUESTION_STOPWORDS.has(qw)) continue;
        const w = idf.get(qw) ?? 1;
        totalWeight += w;
        if (memWords.has(qw)) matchedWeight += w + BM25_DELTA;
      }
      const maxWeight = totalWeight + queryWords.size * BM25_DELTA;
      const coverage = maxWeight > 0 ? matchedWeight / maxWeight : 0;
      sim = Math.max(sim, coverage);
      if (sim < 0.3 && memWords.size > 0) {
        let reverseHits = 0;
        for (const mw of memWords) {
          if (queryWords.has(mw)) reverseHits++;
        }
        const reverseCoverage = reverseHits / memWords.size;
        sim = Math.max(sim, reverseCoverage * 0.7);
      }
    }
    if (sim < 0.2) {
      try {
        const aamMod = require("./aam.ts");
        const queryTerms = [...queryWords].slice(0, 5);
        const expanded = aamMod.expandQuery(queryTerms, 3);
        let semanticMatch = 0;
        for (const exp of expanded) {
          if (memWords.has(exp.word)) {
            semanticMatch += exp.weight * (idf?.get(exp.word) ?? 0.5);
          }
        }
        const semanticCoverage = expanded.length > 0 ? semanticMatch / expanded.length : 0;
        sim = Math.max(sim, semanticCoverage * 0.8);
      } catch {
      }
    }
    if (mem.situationCtx && moodCtx) {
      const moodDelta = Math.abs((mem.situationCtx.mood ?? 0) - (moodCtx.mood ?? 0));
      const ctxBonus = moodDelta < 0.3 ? 0.1 : 0;
      sim += ctxBonus;
    }
    if (sim < 0.05) {
      if (!queryTrigrams) queryTrigrams = trigrams(msg);
      const memTri = trigrams(memContent);
      const triSim = trigramSimilarity(queryTrigrams, memTri);
      sim = Math.max(sim, triSim * 0.6);
    }
    if (mem.reasoning) {
      const rText = `${mem.reasoning.context || ""} ${mem.reasoning.conclusion || ""}`.toLowerCase();
      if (rText.length > 5) {
        let rHits = 0;
        for (const qw of queryWords) {
          if (rText.includes(qw)) rHits++;
        }
        const rSim = rHits / Math.max(1, queryWords.size) * 0.6;
        if (rSim > 0) sim = Math.max(sim, sim + rSim * 0.5);
      }
    }
    if (mem.reasoning && mem.reasoning.conclusion && /为什么|因为|原因|怎么回事|why|because|导致|所以/.test(msg)) {
      const reasonWords = (mem.reasoning.context + " " + mem.reasoning.conclusion).match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || [];
      let reasonHits = 0;
      for (const rw of reasonWords) {
        if (queryWords.has(rw.toLowerCase())) reasonHits++;
      }
      if (reasonHits > 0) {
        sim = Math.max(sim, sim + reasonHits * 0.12);
      }
    }
    if (mem.because && queryWords.size > 0) {
      const becauseWords = (mem.because.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
      const becauseHits = becauseWords.filter((w) => queryWords.has(w)).length;
      if (becauseHits > 0) {
        sim += becauseHits * 0.08;
      }
    }
    if (sim < 0.03) continue;
    const _isCausalQuery = /为什么|因为|原因|怎么回事|why|because|caused|reason/i.test(msg);
    const causalBoost = _isCausalQuery && (mem.because || mem.reasoning) ? 1.5 : 1;
    const recency = timeDecay(mem);
    const usageBoost = mem.tags && mem.tags.length > 5 ? 1.2 : 1;
    const scopeBoost = mem.scope === "preference" || mem.scope === "fact" ? _scopeBoostPref : mem.scope === "correction" ? _scopeBoostCorr : 1;
    let emotionBoost = 1;
    if (mem.emotion === "important") emotionBoost = _emotionBoostImportant;
    else if (mem.emotion === "painful") emotionBoost = _emotionBoostPainful;
    else if (mem.emotion === "warm") emotionBoost = _emotionBoostWarm;
    const eLabel = mem.emotionLabel;
    if (eLabel === "anger" || eLabel === "anxiety") emotionBoost = Math.max(emotionBoost, 1.4);
    else if (eLabel === "pride" || eLabel === "relief") emotionBoost = Math.max(emotionBoost, 1.3);
    else if (eLabel === "frustration" || eLabel === "sadness") emotionBoost = Math.max(emotionBoost, 1.3);
    const userBoost = userId && mem.userId && mem.userId === userId ? _userBoostSame : userId && mem.userId && mem.userId !== userId ? _userBoostOther : 1;
    const lastAcc = mem.lastAccessed || mem.ts || 0;
    const accAgeDays = (Date.now() - lastAcc) / 864e5;
    const tierWeight = accAgeDays <= 1 || (mem.recallCount ?? 0) >= 5 ? _tierWeightHot : accAgeDays <= 7 ? _tierWeightWarm : accAgeDays <= 30 ? _tierWeightCool : _tierWeightCold;
    const consolidatedBoost = mem.scope === "consolidated" ? _consolidatedBoost : mem.scope === "pinned" ? 2 : 1;
    const reflexionBoost = mem.scope === "reflexion" ? _reflexionBoost : 1;
    const confidenceWeight = mem.confidence ?? 0.7;
    const temporalWeight = mem.validUntil && mem.validUntil > 0 && mem.validUntil < Date.now() ? 0.3 : 1;
    let graphBoost = 1;
    if (expansionWords.size > 0) {
      const memLower = mem.content.toLowerCase();
      let graphHits = 0;
      for (const w of expansionWords) {
        if (memLower.includes(w)) graphHits++;
      }
      if (graphHits > 0) {
        graphBoost = 1 + Math.min(0.5, graphHits * 0.15);
      }
    }
    const impactBoost = getRecallImpactBoost(mem.content);
    const archiveWeight = mem.scope === "archived" ? 0.3 : 1;
    let moodMatchBoost = 1;
    if (moodCtx) {
      if (moodCtx.mood > 0.3 && mem.emotion === "warm") moodMatchBoost = 1.5;
      else if (moodCtx.mood < -0.3 && mem.emotion === "painful") moodMatchBoost = 1.5;
      else if (moodCtx.mood < -0.3 && mem.emotion === "warm") moodMatchBoost = 0.6;
      else if (moodCtx.mood > 0.3 && mem.emotion === "painful") moodMatchBoost = 0.7;
      if (moodCtx.alertness > 0.7 && (mem.emotion === "important" || mem.scope === "correction")) moodMatchBoost *= 1.3;
      if (eLabel && moodCtx) {
        try {
          const bodyM = getLazyModule("body");
          const lastDetectedEmotion = bodyM?.lastDetectedEmotion;
          if (lastDetectedEmotion && eLabel === lastDetectedEmotion.label) {
            moodMatchBoost *= 1.4;
          }
        } catch {
        }
      }
      if (mem.situationCtx?.mood !== void 0) {
        const moodDelta = Math.abs(moodCtx.mood - mem.situationCtx.mood);
        if (moodDelta < 0.3) moodMatchBoost *= 1.2;
      }
    }
    const ei = mem.emotionIntensity ?? 0;
    if (ei >= 0.8) moodMatchBoost *= _flashbulbHigh;
    else if (ei >= 0.5) moodMatchBoost *= _flashbulbMedium;
    const _l = Math.log;
    const _e = 0.01;
    const logScore = getParam("recall.w_sim") * _l(sim + _e) + getParam("recall.w_recency") * _l(recency + _e) + getParam("recall.w_scope") * _l(scopeBoost) + getParam("recall.w_emotion") * _l(emotionBoost) + getParam("recall.w_user") * _l(userBoost) + getParam("recall.w_mood") * _l(consolidatedBoost) + 0.3 * _l(usageBoost) + 0.3 * _l(reflexionBoost) + getParam("recall.w_confidence") * _l(confidenceWeight + _e) + 0.5 * _l(temporalWeight + _e) + 0.7 * _l(graphBoost) + 0.3 * _l(tierWeight) + 0.3 * _l(impactBoost) + 0.2 * _l(archiveWeight) + getParam("recall.w_mood") * _l(moodMatchBoost) + 0.4 * _l(causalBoost);
    let stateGate = 1;
    if (mem.situationCtx && moodCtx) {
      const moodDist = Math.abs((moodCtx.mood || 0) - (mem.situationCtx.mood || 0));
      const alertDist = Math.abs((moodCtx.alertness || 0) - (mem.situationCtx.alertness || 0));
      const stateDist = Math.sqrt(moodDist * moodDist + alertDist * alertDist);
      stateGate = 1 / (1 + Math.exp(stateDist * 3 - 1.5));
      stateGate = Math.max(0.1, stateGate);
    }
    let encodingBoost = 1;
    if (mem.recallContexts && mem.recallContexts.length > 0) {
      const queryWordsStr = [...queryWords].join(" ");
      for (const ctx of mem.recallContexts) {
        const ctxWords = (ctx.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
        const overlap = ctxWords.filter((w) => queryWords.has(w)).length;
        if (overlap >= 2) {
          encodingBoost = Math.max(encodingBoost, 1 + overlap * 0.1);
          break;
        }
      }
    }
    if (mem.tags && mem.tags.length > 0) {
      const tagHits = mem.tags.filter((t) => queryWords.has(t.toLowerCase())).length;
      if (tagHits >= 3) encodingBoost = Math.max(encodingBoost, 1.3);
    }
    scored.push({ ...mem, score: logScore * stateGate * encodingBoost });
  }
  if (scored.length >= 3) {
    scored.sort((a, b) => b.score - a.score);
    const spreadLimit = Math.min(scored.length, topN * 3);
    const topActivators = scored.slice(0, 3).filter((s) => s.score > 0.1);
    if (topActivators.length > 0) {
      const idfMap = buildIDF();
      const activatedWordWeights = /* @__PURE__ */ new Map();
      for (const act of topActivators) {
        const words = act.content.match(WORD_PATTERN.CJK24_EN3) || [];
        for (const w of words) {
          const wl = w.toLowerCase();
          const idfW = idfMap.get(wl) ?? 1;
          activatedWordWeights.set(wl, Math.max(activatedWordWeights.get(wl) ?? 0, idfW));
        }
      }
      for (let si = 3; si < spreadLimit; si++) {
        const s = scored[si];
        const sWords = (s.content.match(WORD_PATTERN.CJK24_EN3) || []).map((w) => w.toLowerCase());
        let activation = 0;
        for (const w of sWords) {
          const wt = activatedWordWeights.get(w);
          if (wt !== void 0) activation += wt;
        }
        if (activation > 0) {
          s.score *= 1 + Math.min(activation * 0.1, 0.5);
        }
      }
    }
  }
  const PRIMING_WINDOW_MS = 5 * 60 * 1e3;
  const now = Date.now();
  if (_primingCache.size > 0) {
    for (const s of scored) {
      const sWords = (s.content.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase());
      let primingHits = 0;
      for (const w of sWords) {
        const primedAt = _primingCache.get(w);
        if (primedAt && now - primedAt < PRIMING_WINDOW_MS) primingHits++;
      }
      if (primingHits > 0 && sWords.length > 0) {
        const primingBoost = Math.min(0.3, primingHits / sWords.length);
        s.score *= 1 + primingBoost;
      }
    }
  }
  scored.sort((a, b) => b.score - a.score);
  let _corpusFreq = null;
  function getCorpusFreq() {
    if (_corpusFreq) return _corpusFreq;
    _corpusFreq = /* @__PURE__ */ new Map();
    let total = 0;
    for (const mem of activeMemories) {
      const tokens = bm25Tokenize(mem.content);
      for (const t of tokens) {
        _corpusFreq.set(t, (_corpusFreq.get(t) || 0) + 1);
        total++;
      }
    }
    _corpusFreq.set("__total__", total || 1e4);
    return _corpusFreq;
  }
  if (scored.length >= 4) {
    const ch1 = scored.map((s, i) => ({ idx: i, key: s.score }));
    const ch2 = scored.map((s, i) => ({ idx: i, key: s.lastAccessed || s.ts || 0 }));
    ch2.sort((a, b) => b.key - a.key);
    const ch3 = scored.map((s, i) => {
      const scopeW = s.scope === "correction" ? 3 : s.scope === "preference" || s.scope === "fact" ? 2 : s.scope === "consolidated" ? 2.5 : s.scope === "pinned" ? 4 : 1;
      const emotionW = s.emotion === "important" ? 1.4 : s.emotion === "painful" ? 1.3 : 1;
      const eiW = (s.emotionIntensity ?? 0) >= 0.8 ? 1.6 : (s.emotionIntensity ?? 0) >= 0.5 ? 1.2 : 1;
      return { idx: i, key: scopeW * emotionW * eiW };
    });
    ch3.sort((a, b) => b.key - a.key);
    const ch4 = scored.map((s, i) => {
      let graphHits = 0;
      if (expansionWords.size > 0) {
        const ml = s.content.toLowerCase();
        for (const w of expansionWords) {
          if (ml.includes(w)) graphHits++;
        }
      }
      return { idx: i, key: graphHits + (s.recallCount ?? 0) * 0.1 };
    });
    ch4.sort((a, b) => b.key - a.key);
    const cf = getCorpusFreq();
    const corpusSize = cf.get("__total__") || 1e4;
    const dirichletMu = 2e3;
    if (!bm25QueryTokens) bm25QueryTokens = new Set(bm25Tokenize(msg));
    const queryTermsArr = [...bm25QueryTokens];
    const ch5 = scored.map((s, i) => {
      const docTokens = _getDocTokens(s.content).words;
      const docLen = docTokens.length;
      if (docLen === 0) return { idx: i, key: -Infinity };
      let dlmScore = 0;
      for (const qt of queryTermsArr) {
        const tf = docTokens.filter((t) => t === qt).length;
        const cfVal = cf.get(qt) || 1;
        dlmScore += Math.log((tf + dirichletMu * cfVal / corpusSize) / (docLen + dirichletMu));
      }
      return { idx: i, key: dlmScore };
    });
    ch5.sort((a, b) => b.key - a.key);
    const rankMaps = [];
    for (const channel of [ch1, ch2, ch3, ch4, ch5]) {
      const rm = /* @__PURE__ */ new Map();
      for (let r = 0; r < channel.length; r++) rm.set(channel[r].idx, r);
      rankMaps.push(rm);
    }
    const hasTimeKeyword = /上次|之前|昨天|上周|那次|上个月|以前/.test(msg);
    const isNegated = /不记得|忘了|想不起/.test(msg);
    const isCausalQuery = /为什么|怎么回事|原因|导致|因为/.test(msg);
    let graphWeights = [0.3, 0.2, 0.2, 0.2, 0.1];
    if (hasTimeKeyword && !isNegated) {
      graphWeights = [0.1, 0.5, 0.1, 0.2, 0.1];
    } else if (isCausalQuery) {
      graphWeights = [0.1, 0.1, 0.1, 0.6, 0.1];
    } else if (cog?.spectrum?.information > 0.6) {
      graphWeights = [0.4, 0.1, 0.1, 0.3, 0.1];
    }
    const RRF_K = 60;
    const channelConfidences = [];
    for (const channel of [ch1, ch2, ch3, ch4, ch5]) {
      if (channel.length >= 3) {
        const top1 = Math.max(1e-3, channel[0]?.score ?? 1e-3);
        const top2 = Math.max(1e-3, channel[1]?.score ?? 1e-3);
        channelConfidences.push(Math.min(3, top1 / top2));
      } else {
        channelConfidences.push(1);
      }
    }
    for (let i = 0; i < scored.length; i++) {
      let cwrfScore = 0;
      for (let c = 0; c < rankMaps.length; c++) {
        const rank = rankMaps[c].get(i) ?? scored.length;
        cwrfScore += channelConfidences[c] * graphWeights[c] / (RRF_K + rank);
      }
      scored[i].score = 0.6 * scored[i].score + 0.4 * (cwrfScore * 1e3);
    }
    scored.sort((a, b) => b.score - a.score);
  }
  const topResults = mmrRerank(scored.slice(0, topN * 3), topN);
  if (mentionedEntities.length > 0 && topResults.length < topN) {
    const topContents = new Set(topResults.map((r) => r.content));
    for (const entity of mentionedEntities) {
      const walked = graphWalkRecall(entity, memoryState.memories, 2, 6);
      for (const wContent of walked) {
        if (topContents.has(wContent) || topResults.length >= topN) break;
        const mem = _contentMap.get(wContent);
        if (mem) {
          topResults.push({ ...mem, score: 0 });
          topContents.add(wContent);
        }
      }
    }
  }
  for (const result of topResults) {
    const mem = _memLookup.get(`${result.content}\0${result.ts}`);
    if (mem) {
      mem.lastAccessed = Date.now();
      mem.recallCount = (mem.recallCount ?? 0) + 1;
      mem.lastRecalled = Date.now();
      const retrievalDifficulty = 1 - Math.min(1, result.score / 0.5);
      const testingBoost = 0.01 + retrievalDifficulty * 0.04;
      bayesBoost(mem, 0.3 + retrievalDifficulty * 0.7);
      mem.confidence = Math.min(1, (mem.confidence ?? 0.7) + testingBoost);
      if (mem.fsrs) {
        const difficultyBonus = 1 + retrievalDifficulty * 0.5;
        try {
          const { fsrsUpdate } = require("./smart-forget.ts");
          const ageDays = (Date.now() - (mem.ts || Date.now())) / 864e5;
          const rating = difficultyBonus > 1.2 ? 4 : 3;
          mem.fsrs = fsrsUpdate(mem.fsrs, rating, ageDays);
        } catch {
          mem.fsrs.stability *= difficultyBonus;
        }
      }
      syncToSQLite(mem, { confidence: mem.confidence, recallCount: mem.recallCount, lastAccessed: mem.lastAccessed, lastRecalled: mem.lastRecalled });
      if (!mem.recallContexts) mem.recallContexts = [];
      const ctxSnippet = msg.slice(0, 40);
      if (!mem.recallContexts.includes(ctxSnippet)) {
        mem.recallContexts.push(ctxSnippet);
        if (mem.recallContexts.length > 5) mem.recallContexts.shift();
      }
      if ((mem.recallCount ?? 0) >= 5 && !mem.content.includes("[\u591A\u6B21\u88AB\u63D0\u53CA]")) {
        const uniqueContexts = new Set(mem.recallContexts).size;
        if (uniqueContexts >= 3) {
          if (!mem.history) mem.history = [];
          mem.history.push({ content: mem.content, ts: Date.now() });
          mem.content = `[\u591A\u6B21\u88AB\u63D0\u53CA] ${mem.content}`;
          mem.tier = "long_term";
          syncToSQLite(mem, { content: mem.content, tier: mem.tier });
        }
      }
      try {
        const memWords = (result.content.match(WORD_PATTERN.CJK24_EN3) || []).map((w) => w.toLowerCase());
        const sharedWords = memWords.filter((w) => queryWords.has(w));
        if (sharedWords.length >= 1) {
          const microLink = {
            query: msg.slice(0, 40),
            memoryRef: result.content.slice(0, 40),
            sharedKeywords: sharedWords.slice(0, 5),
            ts: Date.now()
          };
          if (!mem.microLinks) mem.microLinks = [];
          mem.microLinks.push(microLink);
          if (mem.microLinks.length > 10) mem.microLinks.shift();
          const keywordFreq = /* @__PURE__ */ new Map();
          for (const link of mem.microLinks) {
            for (const kw of link.sharedKeywords) {
              keywordFreq.set(kw, (keywordFreq.get(kw) || 0) + 1);
            }
          }
          for (const [kw, freq] of keywordFreq) {
            if (freq >= 3 && mem.tags && !mem.tags.includes(kw)) {
              mem.tags.push(kw);
              console.log(`[cc-soul][living-network] emergent tag: "${kw}" on memory "${mem.content.slice(0, 30)}"`);
            }
          }
        }
      } catch {
      }
    }
  }
  if (topResults.length > 0) saveMemories();
  try {
    const ocMemDb = resolve(homedir(), ".openclaw/memory/main.sqlite");
    if (existsSync(ocMemDb)) {
      const { DatabaseSync } = require("node:sqlite");
      const db = new DatabaseSync(ocMemDb, { open: true, readOnly: true });
      const ftsResults = db.prepare(
        `SELECT text, path FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY rank LIMIT ?`
      ).all(msg.replace(/['"*(){}^~<>|\\]/g, "").replace(/\b(AND|OR|NOT|NEAR)\b/gi, ""), topN);
      db.close();
      if (ftsResults.length > 0) {
        const existingContents = new Set(topResults.map((r) => r.content.slice(0, 200)));
        for (const fts of ftsResults) {
          if (!existingContents.has(fts.text.slice(0, 200))) {
            topResults.push({
              content: fts.text,
              scope: "fact",
              ts: Date.now(),
              source: "openclaw-memory",
              confidence: 0.7,
              recallCount: 0,
              lastAccessed: Date.now()
            });
          }
        }
        console.log(`[cc-soul][memory-hybrid] merged ${ftsResults.length} OpenClaw FTS results`);
      }
    }
  } catch {
  }
  recallStats.total++;
  if (topResults.length > 0) recallStats.successful++;
  if (recallStats.total > 1e3) {
    recallStats.rate = recallStats.successful / recallStats.total;
    recallStats.total = 0;
    recallStats.successful = 0;
  }
  return topResults;
}
const MEMORY_RECALL_TRIGGERS = /你还记得|你记不记得|之前说过|上次提到|我们聊过|你忘了吗|还记得吗|do you remember|did i mention|we talked about|you forgot/i;
const SYSTEM2_KEYWORDS = /为什么|怎么看|如何|对比|区别|上次|之前|总结|分析|比较|回顾|why|how come|compare|difference|last time|before|summarize|analyze|review/i;
const PRED_LABELS = {
  likes: "\u559C\u6B22",
  dislikes: "\u8BA8\u538C",
  works_at: "\u5728",
  lives_in: "\u4F4F\u5728",
  uses: "\u7528",
  has_pet: "\u517B\u4E86",
  has_family: "\u6709",
  habit: "\u4E60\u60EF",
  occupation: "\u804C\u4E1A\u662F",
  age: "\u5E74\u9F84",
  educated_at: "\u6BD5\u4E1A\u4E8E",
  relationship: "\u7684\u4F34\u4FA3",
  uses_os: "\u7528",
  prefers: "\u504F\u597D",
  family_name: "\u7684"
};
const FACT_QUERY_PATTERNS = [
  { pattern: /叫什么|我是谁|名字|what.?s my name|who am i|my name/i, predicates: [] },
  // empty = all user facts
  { pattern: /工作|公司|在哪.*工作|上班|where do i work|my job|my company|what do i do/i, predicates: ["works_at", "occupation"] },
  { pattern: /住哪|住在|地址|where do i live|my address|where.?m i based/i, predicates: ["lives_in"] },
  { pattern: /喜欢|偏好|最爱|what do i like|my favorite|my preference/i, predicates: ["likes", "prefers"] },
  { pattern: /讨厌|不喜欢|受不了|what do i hate|what do i dislike/i, predicates: ["dislikes"] },
  { pattern: /职业|做什么的|my occupation|what.?s my job/i, predicates: ["occupation"] },
  { pattern: /多大|几岁|年龄|how old|my age/i, predicates: ["age"] },
  { pattern: /宠物|猫|狗|养|my pet|my cat|my dog/i, predicates: ["has_pet"] },
  { pattern: /家人|女儿|儿子|孩子|老婆|老公|my family|my daughter|my son|my kid|my wife|my husband/i, predicates: ["has_family", "family_name", "relationship"] },
  { pattern: /习惯|每天|my habit|my routine|daily/i, predicates: ["habit"] },
  { pattern: /用什么|电脑|设备|what do i use|my computer|my device/i, predicates: ["uses", "uses_os"] },
  { pattern: /喝什么|饮料|咖啡|茶|what do i drink|coffee|tea/i, predicates: ["likes", "dislikes"] },
  { pattern: /毕业|学校|大学|my school|my university|where did i graduate/i, predicates: ["educated_at"] }
];
function system1FastRecall(msg, topN, _userId) {
  if (msg.length > 30) return null;
  if (SYSTEM2_KEYWORDS.test(msg)) return null;
  const results = [];
  try {
    const matchedPredicates = /* @__PURE__ */ new Set();
    let matchedAny = false;
    for (const { pattern, predicates } of FACT_QUERY_PATTERNS) {
      if (pattern.test(msg)) {
        matchedAny = true;
        if (predicates.length === 0) {
          const allFacts = queryFacts({ subject: "user" });
          for (const f of allFacts) {
            const label = PRED_LABELS[f.predicate] || f.predicate;
            results.push({
              content: `\u7528\u6237${label}${f.object}`,
              scope: "fact",
              ts: f.ts || Date.now(),
              confidence: f.confidence || 0.8,
              source: "system1_fact"
            });
          }
        } else {
          for (const pred of predicates) {
            if (matchedPredicates.has(pred)) continue;
            matchedPredicates.add(pred);
            const facts = queryFacts({ subject: "user", predicate: pred });
            for (const f of facts) {
              const label = PRED_LABELS[f.predicate] || f.predicate;
              results.push({
                content: `\u7528\u6237${label}${f.object}`,
                scope: "fact",
                ts: f.ts || Date.now(),
                confidence: f.confidence || 0.8,
                source: "system1_fact"
              });
            }
          }
        }
      }
    }
    if (!matchedAny) {
    }
  } catch {
  }
  try {
    if (coreMemories && coreMemories.length > 0) {
      const queryWords = (msg.match(/[\u4e00-\u9fff]+|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
      if (queryWords.length > 0 && queryWords.length <= 3) {
        for (const cm of coreMemories) {
          const cmLower = (cm.content || "").toLowerCase();
          const hits = queryWords.filter((w) => cmLower.includes(w)).length;
          if (hits >= 1) {
            const dup = results.some((r) => r.content.includes(cm.content.slice(0, 20)));
            if (!dup) {
              results.push({
                content: cm.content,
                scope: cm.category || "fact",
                ts: cm.addedAt || Date.now(),
                confidence: 0.9,
                source: "system1_core"
              });
            }
          }
        }
      }
    }
  } catch {
  }
  if (results.length > 0) {
    console.log(`[cc-soul][recall] System 1 hit: ${results.length} results (dual-channel)`);
    return results.slice(0, topN);
  }
  return null;
}
function recall(msg, topN = 3, userId, channelId, moodCtx, opts, cogHints) {
  if (!msg || memoryState.memories.length === 0) return [];
  if (!process.env.CC_SOUL_BENCHMARK) {
    try {
      const { getInjectionStrategy, shouldInjectMemories } = require("./cognitive-load.ts");
      if (!shouldInjectMemories(msg)) return [];
      const strategy = getInjectionStrategy(msg);
      if (strategy.topN < topN) topN = strategy.topN;
    } catch {
    }
  }
  if (!process.env.CC_SOUL_BENCHMARK) tickABExperiment();
  updatePrimingCache(msg);
  const _expandedMsg = process.env.CC_SOUL_BENCHMARK ? msg : expandQueryWithCoreference(msg, memoryState.chatHistory);
  const candidates = process.env.CC_SOUL_BENCHMARK ? memoryState.memories : routeMemories(memoryState.memories, _expandedMsg, userId);
  try {
    const { activationRecall } = require("./activation-field.ts");
    const results = activationRecall(
      candidates,
      _expandedMsg,
      topN,
      moodCtx?.mood || 0,
      moodCtx?.alertness || 0.5,
      cogHints || null
    );
    if (results.length > 0) console.log(`[cc-soul][recall] activationRecall returned ${results.length} results, top: "${(results[0]?.content || "").slice(0, 40)}"`);
    if (results.length < 3) {
      try {
        const { reviveFromGraveyard } = require("./smart-forget.ts");
        const revived = reviveFromGraveyard(msg, memoryState.memories, 3 - results.length);
        if (revived.length > 0) {
          results.push(...revived);
        }
      } catch {
      }
    }
    recallStats.total++;
    if (results.length > 0) recallStats.successful++;
    if (recallStats.total > 1e3) {
      recallStats.rate = recallStats.successful / recallStats.total;
      recallStats.total = 0;
      recallStats.successful = 0;
    }
    for (const mem of results) {
      const original = _memLookup.get(`${mem.content}\0${mem.ts}`) || _contentMap.get(mem.content);
      if (original) {
        original.lastAccessed = Date.now();
        original.recallCount = (original.recallCount ?? 0) + 1;
        original.lastRecalled = Date.now();
        const idx = results.indexOf(mem);
        const difficulty = idx / Math.max(1, results.length);
        try {
          _posEvidence(original, difficulty);
        } catch {
          original.confidence = Math.min(1, (original.confidence ?? 0.7) + 0.02);
        }
        if (original.fsrs) {
          try {
            const { fsrsUpdate } = require("./smart-forget.ts");
            const ageDays = (Date.now() - (original.ts || Date.now())) / 864e5;
            const rating = difficulty < 0.3 ? 4 : difficulty < 0.7 ? 3 : 2;
            original.fsrs = fsrsUpdate(original.fsrs, rating, ageDays);
          } catch {
          }
        }
        if (!process.env.CC_SOUL_BENCHMARK) {
          syncToSQLite(original, { confidence: original.confidence, recallCount: original.recallCount, lastAccessed: original.lastAccessed, lastRecalled: original.lastRecalled });
        }
        try {
          const queryWords = new Set((_expandedMsg.match(WORD_PATTERN.CJK24_EN3) || []).map((w) => w.toLowerCase()));
          const memWords = (original.content.match(WORD_PATTERN.CJK24_EN3) || []).map((w) => w.toLowerCase());
          const shared = memWords.filter((w) => queryWords.has(w));
          if (shared.length >= 1) {
            if (!original.microLinks) original.microLinks = [];
            original.microLinks.push({
              query: _expandedMsg.slice(0, 40),
              memoryRef: original.content.slice(0, 40),
              sharedKeywords: shared.slice(0, 5),
              ts: Date.now()
            });
            if (original.microLinks.length > 10) original.microLinks.shift();
          }
        } catch {
        }
      }
    }
    if (results.length > 0) {
      const recalledContents = new Set(results.map((r) => r.content));
      const recalledWords = /* @__PURE__ */ new Set();
      for (const r of results) {
        const words = r.content.match(WORD_PATTERN.CJK2_EN3) || [];
        for (const w of words) recalledWords.add(w.toLowerCase());
      }
      for (const m of memoryState.memories) {
        if (!m || !m.content || recalledContents.has(m.content)) continue;
        if (m.scope === "core_memory" || m.scope === "correction") continue;
        const mWords = m.content.match(WORD_PATTERN.CJK2_EN3) || [];
        let overlap = 0;
        for (const w of mWords) {
          if (recalledWords.has(w.toLowerCase())) overlap++;
        }
        if (overlap >= 3 && mWords.length > 0 && overlap / mWords.length > 0.4) {
          const oldConf = m.confidence ?? 0.7;
          try {
            _negEvidence(m, overlap / mWords.length * 0.3);
          } catch {
            m.confidence = Math.max(0.1, oldConf - 0.02);
          }
          try {
            require("./decision-log.ts").logDecision("rif_suppress", (m.content || "").slice(0, 30) + "|" + m.ts, `conf=${oldConf.toFixed(2)}\u2192${m.confidence.toFixed(2)}, overlap=${overlap}/${mWords.length}`);
          } catch {
          }
        }
      }
    }
    for (const m of memoryState.memories) {
      if (m && m._preheated) {
        const wasUsed = results.some((r) => r.content === m.content);
        if (wasUsed) {
          try {
            require("./decision-log.ts").logDecision("preheat_hit", (m.content || "").slice(0, 30), "preheated memory was recalled");
          } catch {
          }
        }
        delete m._preheated;
      }
    }
    if (results.length > 0) saveMemories();
    try {
      predictivePrime(results, memoryState.memories);
    } catch {
    }
    return results;
  } catch (e) {
    console.log(`[cc-soul][recall] activation-field error: ${e.message}, fallback to legacy`);
  }
  return recallWithScores(msg, topN, userId, channelId, moodCtx).map(({ score, ...rest }) => rest);
}
let _lastVectorResults = [];
let _lastVectorResultsKey = "";
let _openclawMemDb = null;
let _openclawMemDbAttempted = false;
function getOpenClawMemDb() {
  if (_openclawMemDbAttempted) return _openclawMemDb;
  _openclawMemDbAttempted = true;
  try {
    const Database = require("better-sqlite3");
    const dbPath = resolve(homedir(), ".openclaw/memory/cc.sqlite");
    if (existsSync(dbPath)) {
      _openclawMemDb = new Database(dbPath, { readonly: true, fileMustExist: true });
    }
  } catch (_) {
  }
  return _openclawMemDb;
}
function recallFromJsonFile(msg, topN) {
  try {
    const memPath = resolve(DATA_DIR, "memories.json");
    if (!existsSync(memPath)) return [];
    const data = loadJson(memPath, []);
    const keywords = (msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    if (keywords.length === 0) return [];
    const scored = [];
    for (const m of data) {
      if (m.scope === "expired" || m.scope === "decayed") continue;
      const content = m.content.toLowerCase();
      const tags = (m.tags || []).map((t) => t.toLowerCase());
      let hits = 0;
      for (const kw of keywords) {
        if (content.includes(kw) || tags.some((t) => t.includes(kw) || kw.includes(t))) hits++;
      }
      if (hits === 0) continue;
      const sim = hits / Math.max(1, keywords.length);
      const scopeBoost = m.scope === "preference" || m.scope === "fact" ? 1.3 : m.scope === "correction" ? 1.5 : 1;
      const archiveWeight = m.scope === "archived" ? 0.3 : 1;
      scored.push({ ...m, score: sim * scopeBoost * archiveWeight });
    }
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, topN).map(({ score, ...rest }) => rest);
  } catch (e) {
    console.error(`[cc-soul][recall] JSON file search failed: ${e.message}`);
    return [];
  }
}
function recallFromOpenClawMemory(msg, topN) {
  const db = getOpenClawMemDb();
  if (!db) return [];
  try {
    const results = db.prepare(
      `SELECT text, updated_at FROM chunks WHERE text LIKE ? ORDER BY updated_at DESC LIMIT ?`
    ).all(`%${msg.slice(0, 20)}%`, topN);
    return results.map((r) => ({
      content: r.text,
      scope: "fact",
      ts: r.updated_at || Date.now(),
      emotion: "neutral",
      confidence: 0.5,
      tier: "long_term"
    }));
  } catch (_) {
    return [];
  }
}
let cachedFusedRecall = null;
function getCachedFusedRecall() {
  if (!cachedFusedRecall) return [];
  if (Date.now() - cachedFusedRecall.ts > 3e5) {
    cachedFusedRecall = null;
    return [];
  }
  return cachedFusedRecall.results;
}
let idfInvalidateCount = 0;
function incrementalIDFUpdate(content) {
  if (!idfCache) return;
  const words = (content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
  if (words.length === 0) return;
  const N = memoryState.memories.length || 1;
  const unique = new Set(words);
  for (const w of unique) {
    const oldIdf = idfCache.get(w);
    const oldDf = oldIdf !== void 0 ? Math.round(N / Math.exp(oldIdf)) - 1 : 0;
    const newDf = oldDf + 1;
    idfCache.set(w, Math.log(N / (1 + newDf)));
  }
  if (avgDocLenCache !== null) {
    const prevTotal = avgDocLenCache * (N - 1);
    avgDocLenCache = (prevTotal + words.length) / N;
  }
}
function invalidateIDF() {
  idfInvalidateCount++;
  if (idfInvalidateCount < 50 && idfCache && Date.now() - lastIdfBuildTs < 6e4) return;
  idfCache = null;
  avgDocLenCache = null;
  idfInvalidateCount = 0;
  _bm25TokenCache.clear();
}
function degradeMemoryConfidence(content) {
  const mem = memoryState.memories.find((m) => m.content === content);
  if (mem) {
    bayesCorrect(mem, 2);
    if (mem.confidence <= 0.1) {
      mem.scope = "expired";
    }
    syncToSQLite(mem, { confidence: mem.confidence, scope: mem.scope });
    saveMemories();
    console.log(`[cc-soul][confidence] degraded: "${content.slice(0, 50)}" \u2192 ${mem.confidence.toFixed(2)}${mem.scope === "expired" ? " (expired)" : ""}`);
  }
}
export {
  _memLookup,
  _predictivePrimingCache,
  _primingCache,
  degradeMemoryConfidence,
  extractTimeRange,
  getCachedFusedRecall,
  getContentForRecall,
  getRecallImpactBoost,
  getRecallRate,
  incrementalIDFUpdate,
  invalidateBM25TokenCache,
  invalidateIDF,
  predictivePrime,
  rebuildRecallIndex,
  recall,
  recallImpact,
  recallStats,
  recallWithScores,
  recordABEngagement,
  trackRecallImpact,
  updatePrimingCache,
  updateRecallIndex
};
