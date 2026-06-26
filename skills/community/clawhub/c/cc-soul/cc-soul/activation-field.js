import { trigrams, trigramSimilarity, WORD_PATTERN, TRIGRAM_THRESHOLD } from "./memory-utils.ts";
import { expandQuery as _aamExpandQuery, learnAssociation as _aamLearn, isKnownWord as _aamIsKnownWord, getTemporalSuccessors as _aamGetTemporalSuccessors, getAAMNeighbors as _aamGetAAMNeighbors, learnTemporalLink as _aamLearnTemporalLink } from "./aam.ts";
import { extractTimeRange as _extractTimeRange, _primingCache as _primingCacheRef, _predictivePrimingCache as _predictivePrimingRef } from "./memory-recall.ts";
import { extractTagsLocal as _extractTagsLocal } from "./memory.ts";
import { detectDomain as _detectDomain } from "./epistemic.ts";
import * as _graphMod from "./graph.ts";
import * as _factStoreMod from "./fact-store.ts";
import { extractAnchors as _extractAnchors, inferTimeRange as _inferTemporalRange } from "./temporal-anchor.ts";
import { getTopicRecallModifier as _getDriftModifier } from "./semantic-drift.ts";
import { confidenceRecallModifier as _getConfModifier } from "./confidence-cascade.ts";
import { getParam as _getAutoTuneParam } from "./auto-tune.ts";
function porterStem(word) {
  if (word.length < 4) return word;
  let w = word.toLowerCase();
  if (w.endsWith("ies") && w.length > 4) w = w.slice(0, -3) + "i";
  else if (w.endsWith("sses")) w = w.slice(0, -2);
  else if (w.endsWith("s") && !w.endsWith("ss") && !w.endsWith("us")) w = w.slice(0, -1);
  if (w.endsWith("eed")) {
  } else if (w.endsWith("ed") && w.length > 4) w = w.slice(0, -2);
  else if (w.endsWith("ing") && w.length > 5) w = w.slice(0, -3);
  if (w.endsWith("tion")) w = w.slice(0, -4) + "t";
  else if (w.endsWith("ness") && w.length > 5) w = w.slice(0, -4);
  else if (w.endsWith("ment") && w.length > 5) w = w.slice(0, -4);
  else if (w.endsWith("ful") && w.length > 5) w = w.slice(0, -3);
  else if (w.endsWith("ous") && w.length > 5) w = w.slice(0, -3);
  else if (w.endsWith("ive") && w.length > 5) w = w.slice(0, -3);
  else if (w.endsWith("able") && w.length > 6) w = w.slice(0, -4);
  else if (w.endsWith("ible") && w.length > 6) w = w.slice(0, -4);
  else if (w.endsWith("ally") && w.length > 6) w = w.slice(0, -4) + "al";
  else if (w.endsWith("ly") && w.length > 4) w = w.slice(0, -2);
  return w;
}
const _traceBuffer = /* @__PURE__ */ new Map();
let _currentAvgDocLen = 20;
let _sshMemDims = /* @__PURE__ */ new Map();
let _sshDimFreqMap = /* @__PURE__ */ new Map();
let _sshQueryDims = /* @__PURE__ */ new Set();
const _signalBuffer = [];
function recordRecallEngagement(engaged, signals) {
  _signalBuffer.push({ engaged, signals: {
    base: signals.base || 0,
    context: signals.context || 0,
    emotion: signals.emotion || 0,
    spread: signals.spread || 0,
    interference: signals.interference || 0,
    temporal: signals.temporal || 0,
    pam: signals.pam || 0
  } });
  if (_signalBuffer.length > 200) _signalBuffer.shift();
  if (_signalBuffer.length % 50 === 0 && _signalBuffer.length >= 50) {
    adjustSignalWeights();
  }
}
let _baseWeight = 0.3;
let _contextWeight = 0.7;
let _emotionCoeff = 0.5;
let _spreadCoeff = 1;
let _temporalCoeff = 0.2;
let _pamCoeff = 1;
let _momentumCoeff = 1;
function getSignalWeights() {
  return { base: _baseWeight, context: _contextWeight };
}
function adjustSignalWeights() {
  const good = _signalBuffer.filter((s) => s.engaged);
  const bad = _signalBuffer.filter((s) => !s.engaged);
  if (good.length < 10 || bad.length < 5) return;
  const avgGoodContext = good.reduce((s, g) => s + g.signals.context, 0) / good.length;
  const avgBadContext = bad.reduce((s, b) => s + b.signals.context, 0) / bad.length;
  const avgGoodBase = good.reduce((s, g) => s + g.signals.base, 0) / good.length;
  const avgBadBase = bad.reduce((s, b) => s + b.signals.base, 0) / bad.length;
  const contextDelta = avgGoodContext - avgBadContext;
  const baseDelta = avgGoodBase - avgBadBase;
  _baseWeight = Math.max(0.15, Math.min(0.45, _baseWeight + baseDelta * 0.01));
  _contextWeight = 1 - _baseWeight;
  const signalNames = ["emotion", "spread", "temporal", "pam"];
  const correlations = {};
  for (const name of signalNames) {
    const avgGood = good.reduce((s, g) => s + g.signals[name], 0) / good.length;
    const avgBad = bad.reduce((s, b) => s + b.signals[name], 0) / bad.length;
    correlations[name] = avgGood - avgBad;
  }
  _emotionCoeff = Math.max(0.1, Math.min(1, _emotionCoeff + (correlations.emotion || 0) * 3e-3));
  _spreadCoeff = Math.max(0.2, Math.min(2, _spreadCoeff + (correlations.spread || 0) * 3e-3));
  _temporalCoeff = Math.max(0.1, Math.min(0.5, _temporalCoeff + (correlations.temporal || 0) * 3e-3));
  _pamCoeff = Math.max(0.3, Math.min(2, _pamCoeff + (correlations.pam || 0) * 3e-3));
  _momentumCoeff = Math.max(0.3, Math.min(2, _momentumCoeff));
  try {
    const corrStr = signalNames.map((n) => `${n}=${correlations[n].toFixed(3)}`).join(", ");
    const coeffStr = `emo=${_emotionCoeff.toFixed(3)},spr=${_spreadCoeff.toFixed(3)},tmp=${_temporalCoeff.toFixed(3)},pam=${_pamCoeff.toFixed(3)}`;
    require("./decision-log.ts").logDecision("recall_thermostat", "weight_adjust", `base=${_baseWeight.toFixed(3)}, ctx=${_contextWeight.toFixed(3)}, ${coeffStr}, samples=${_signalBuffer.length}, corr: ${corrStr}`);
  } catch {
  }
}
function getRecentTrace() {
  const now = Date.now();
  const recent = [..._traceBuffer.entries()].filter(([ts]) => now - ts < 3e4).sort(([a], [b]) => b - a);
  return recent[0]?.[1] ?? null;
}
function pruneTraceBuffer() {
  if (_traceBuffer.size <= 3) return;
  const sorted = [..._traceBuffer.keys()].sort((a, b) => a - b);
  while (sorted.length > 3) {
    _traceBuffer.delete(sorted.shift());
  }
}
const _topicMomentum = /* @__PURE__ */ new Map();
const MOMENTUM_DECAY = {
  technical: 0.9,
  // 工作项目：惯性持续 ~2 周
  emotional: 0.7,
  // 生活琐事：~5 天
  default: 0.7
};
function updateMomentum(query) {
  let domain = "default";
  try {
    domain = _detectDomain(query) || "default";
  } catch {
  }
  const words = (query.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase());
  let overlapCount = 0;
  for (const w of words) {
    if (_topicMomentum.has(w) && _topicMomentum.get(w) > 0.5) overlapCount++;
  }
  const overlapRatio = words.length > 0 ? overlapCount / words.length : 1;
  const isSwitched = _topicMomentum.size > 3 && (overlapRatio < 0.15 && words.length >= 5 || overlapCount === 0 && words.length >= 2);
  const decayRate = isSwitched ? 0.1 : MOMENTUM_DECAY[domain] || MOMENTUM_DECAY.default;
  for (const [topic, score] of _topicMomentum) {
    const decayed = score * decayRate;
    if (decayed < 0.1) _topicMomentum.delete(topic);
    else _topicMomentum.set(topic, decayed);
  }
  for (const w of words) {
    const current = _topicMomentum.get(w) || 0;
    _topicMomentum.set(w, current + 1);
  }
}
function getMomentumBoost(memContent) {
  const words = (memContent.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase());
  let totalMomentum = 0;
  for (const w of words) {
    totalMomentum += _topicMomentum.get(w) || 0;
  }
  if (words.length === 0) return 0;
  return Math.min(0.8, totalMomentum / words.length * 0.15);
}
const CATEGORY_KEYWORDS = {
  work: ["\u5DE5\u4F5C", "\u4E0A\u73ED", "\u516C\u53F8", "\u540C\u4E8B", "\u52A0\u73ED", "\u85AA\u8D44", "\u9762\u8BD5", "\u7B80\u5386", "\u8001\u677F", "\u664B\u5347", "work", "job", "company", "boss", "salary", "career", "office", "colleague"],
  tech: ["\u4EE3\u7801", "\u7F16\u7A0B", "\u670D\u52A1\u5668", "\u6570\u636E\u5E93", "bug", "Python", "code", "deploy", "\u5F00\u53D1", "\u63A5\u53E3", "API", "\u6846\u67B6", "debug", "programming", "software"],
  health: ["\u8840\u538B", "\u7761\u7720", "\u8FD0\u52A8", "\u51CF\u80A5", "\u8FC7\u654F", "\u4F53\u68C0", "\u533B\u9662", "\u5403\u836F", "\u611F\u5192", "\u5934\u75BC", "health", "doctor", "exercise", "running", "fitness", "gym", "marathon", "yoga", "workout"],
  family: ["\u8001\u5A46", "\u5973\u670B\u53CB", "\u5B69\u5B50", "\u7236\u6BCD", "\u5BB6\u4EBA", "\u5B9D\u5B9D", "\u8001\u516C", "\u7537\u670B\u53CB", "\u7238", "\u5988", "wife", "family", "husband", "kid", "children", "mother", "father", "daughter", "son", "sibling", "grandma", "grandmother"],
  finance: ["\u623F\u8D37", "\u5DE5\u8D44", "\u80A1\u7968", "\u7406\u8D22", "\u5B58\u6B3E", "\u57FA\u91D1", "\u6295\u8D44", "\u8D26\u5355", "mortgage", "salary", "stock", "invest", "budget", "savings"],
  food: ["\u5403", "\u505A\u996D", "\u706B\u9505", "\u5916\u5356", "\u9910\u5385", "\u83DC", "\u70E7\u70E4", "\u5976\u8336", "food", "restaurant", "cook", "recipe", "bake", "dinner", "lunch"],
  travel: ["\u65C5\u6E38", "\u51FA\u5DEE", "\u673A\u7968", "\u9152\u5E97", "\u7B7E\u8BC1", "\u666F\u70B9", "travel", "trip", "flight", "hotel", "vacation", "road trip", "camping", "hiking", "beach"],
  emotion: ["\u5F00\u5FC3", "\u96BE\u8FC7", "\u7126\u8651", "\u538B\u529B", "\u5FC3\u60C5", "\u70E6", "\u5D29\u6E83", "\u90C1\u95F7", "happy", "sad", "anxious", "stress", "excited", "worried", "proud", "grateful", "scared"],
  housing: ["\u623F\u5B50", "\u79DF\u623F", "\u88C5\u4FEE", "\u642C\u5BB6", "\u7269\u4E1A", "\u5C0F\u533A", "house", "rent", "apartment", "move", "home", "neighborhood"],
  social: ["\u670B\u53CB", "\u805A\u4F1A", "\u7EA6\u4F1A", "\u793E\u4EA4", "\u996D\u5C40", "friend", "party", "date", "hangout", "reunion", "catch up", "meeting"],
  education: ["\u5B66\u4E60", "\u5927\u5B66", "\u8003\u8BD5", "\u8BFE\u7A0B", "\u8BBA\u6587", "\u6BD5\u4E1A", "study", "university", "exam", "course", "school", "teacher", "graduate", "degree"],
  entertainment: ["\u7535\u5F71", "\u6E38\u620F", "\u97F3\u4E50", "\u770B\u4E66", "\u8FFD\u5267", "\u7EFC\u827A", "movie", "game", "music", "book", "read", "concert", "painting", "art", "pottery", "piano", "guitar", "ukulele"],
  pet: ["\u732B", "\u72D7", "\u5BA0\u7269", "\u94F2\u5C4E", "\u732B\u7CAE", "\u72D7\u7CAE", "cat", "dog", "pet", "kitten", "puppy", "animal", "foster", "shelter"],
  identity: ["adoption", "adopted", "religion", "religious", "church", "faith", "LGBTQ", "transgender", "pride", "community", "volunteer", "charity", "mentorship", "counseling", "advocacy"],
  outdoor: ["hike", "bike", "camp", "trail", "park", "garden", "nature", "sunrise", "photography", "landscape", "mountain", "lake"]
};
const _categoryWordSets = /* @__PURE__ */ new Map();
for (const [cat, words] of Object.entries(CATEGORY_KEYWORDS)) {
  _categoryWordSets.set(cat, new Set(words.map((w) => w.toLowerCase())));
}
function detectCategories(text) {
  const lower = text.toLowerCase();
  const textWords = /* @__PURE__ */ new Set();
  for (const w of lower.match(/[a-z]{3,}/g) || []) {
    textWords.add(w);
    textWords.add(porterStem(w));
  }
  for (const w of lower.match(/[\u4e00-\u9fff]{2,4}/g) || []) textWords.add(w);
  const scores = [];
  for (const [cat, wordSet] of _categoryWordSets) {
    let hits = 0;
    for (const kw of wordSet) {
      if (lower.includes(kw)) {
        hits++;
        continue;
      }
      const kwStem = kw.length >= 3 && /^[a-z]+$/.test(kw) ? porterStem(kw) : kw;
      if (textWords.has(kwStem)) hits++;
    }
    if (hits > 0) scores.push([cat, hits]);
  }
  scores.sort((a, b) => b[1] - a[1]);
  return scores.map((s) => s[0]);
}
const _memCategoryCache = /* @__PURE__ */ new Map();
const MEM_CATEGORY_CACHE_MAX = 5e3;
function getMemCategories(mem) {
  const key = (mem.content || "").slice(0, 80);
  let cats = _memCategoryCache.get(key);
  if (cats !== void 0) return cats;
  cats = detectCategories(mem.content || "");
  if (_memCategoryCache.size >= MEM_CATEGORY_CACHE_MAX) {
    const keys = [..._memCategoryCache.keys()];
    for (let i = 0; i < keys.length / 2; i++) _memCategoryCache.delete(keys[i]);
  }
  _memCategoryCache.set(key, cats);
  return cats;
}
const CATEGORY_PRUNE_THRESHOLD = 100;
const CATEGORY_PRUNE_MIN_POOL = 20;
const CATEGORY_HIGH_IMPORTANCE = 8;
const _categoryPenalty = /* @__PURE__ */ new Map();
function categoryPrePrune(memories, query) {
  _categoryPenalty.clear();
  if (memories.length <= CATEGORY_PRUNE_THRESHOLD) return memories;
  if (_currentQueryType === "temporal") return memories;
  const queryCats = detectCategories(query);
  if (queryCats.length === 0) return memories;
  const queryCatSet = new Set(queryCats.slice(0, 3));
  const partitioned = [];
  const seen = /* @__PURE__ */ new Set();
  for (const mem of memories) {
    if ((mem.importance || 0) >= CATEGORY_HIGH_IMPORTANCE || mem.tags?.includes("summary") || mem.scope === "consolidated" || mem.scope === "fact" || mem.scope === "insight") {
      if (!seen.has(mem)) {
        partitioned.push(mem);
        seen.add(mem);
      }
      continue;
    }
    const memCats = getMemCategories(mem);
    if (memCats.length === 0) {
      if (!seen.has(mem)) {
        partitioned.push(mem);
        seen.add(mem);
      }
      continue;
    }
    for (const mc of memCats) {
      if (queryCatSet.has(mc)) {
        if (!seen.has(mem)) {
          partitioned.push(mem);
          seen.add(mem);
        }
        break;
      }
    }
  }
  if (partitioned.length < Math.max(CATEGORY_PRUNE_MIN_POOL, memories.length * 0.5)) {
    for (const mem of memories) {
      if ((mem.importance || 0) >= CATEGORY_HIGH_IMPORTANCE) continue;
      const memCats = getMemCategories(mem);
      if (memCats.length === 0) continue;
      let matched = false;
      for (const mc of memCats) {
        if (queryCatSet.has(mc)) {
          matched = true;
          break;
        }
      }
      if (!matched) _categoryPenalty.set(memKey(mem), 0.5);
    }
    console.log(`[activation-field] topic-partition fallback: pool ${partitioned.length}/${memories.length} too small, soft-weight`);
    return memories;
  }
  console.log(`[activation-field] topic-partition: ${partitioned.length}/${memories.length} (topics: ${[...queryCatSet].join(",")})`);
  return partitioned;
}
function getCategoryWeight(mem) {
  return _categoryPenalty.get(memKey(mem)) ?? 1;
}
const _activations = /* @__PURE__ */ new Map();
function memKey(mem) {
  return `${(mem.content || "").slice(0, 50)}\0${mem.ts || 0}`;
}
function getActivation(mem) {
  return _activations.get(memKey(mem)) || 0;
}
function setActivation(mem, value) {
  _activations.set(memKey(mem), Math.max(0, Math.min(1, value)));
}
function baseActivation(mem, now) {
  const n = Math.max(mem.recallCount || 1, 1);
  const createdAgo = Math.max((now - (mem.ts || now)) / 1e3, 1);
  const lastAgo = Math.max((now - (mem.lastAccessed || mem.ts || now)) / 1e3, 1);
  let sum = 0;
  const cap = Math.min(n, 20);
  if (cap === 1) {
    sum = Math.pow(lastAgo, -0.5);
  } else {
    for (let i = 0; i < cap; i++) {
      const fraction = i / (cap - 1);
      const accessAgo = createdAgo - fraction * (createdAgo - lastAgo);
      sum += Math.pow(Math.max(accessAgo, 1), -0.5);
    }
  }
  const rawB = sum > 0 ? Math.log(sum) : -5;
  return 1 / (1 + Math.exp(-rawB - 1));
}
let _idfCache = null;
let _idfVersion = 0;
let _currentIdfVersion = -1;
let _wordActivationSum = null;
function invalidateFieldIDF() {
  _idfVersion++;
}
function buildIdfCache(memories) {
  const docFreq = /* @__PURE__ */ new Map();
  const activationSum = /* @__PURE__ */ new Map();
  const N = memories.length;
  const now = Date.now();
  for (const mem of memories) {
    const content = mem.content || "";
    const seen = /* @__PURE__ */ new Set();
    const enWords = content.match(/[a-zA-Z]{2,}|\d+/gi) || [];
    for (const w of enWords) seen.add(w.toLowerCase());
    const cjk = content.match(/[\u4e00-\u9fff]+/g) || [];
    for (const seg of cjk) {
      if (seg.length >= 2 && seg.length <= 4) seen.add(seg);
      for (let i = 0; i <= seg.length - 2; i++) seen.add(seg.slice(i, i + 2));
    }
    const ba = baseActivation(mem, now);
    for (const w of seen) {
      docFreq.set(w, (docFreq.get(w) || 0) + 1);
      activationSum.set(w, (activationSum.get(w) || 0) + ba);
    }
  }
  _wordActivationSum = activationSum;
  const idf = /* @__PURE__ */ new Map();
  for (const [word, df] of docFreq) {
    const floor = N < 20 ? 0.1 : 0.02;
    const raw = Math.log(N / Math.max(1, df));
    const maxIdf = Math.log(N);
    idf.set(word, maxIdf > 0 ? Math.max(floor, raw / maxIdf) : 1);
  }
  return idf;
}
const QUERY_TYPE_MULTIPLIERS = {
  precise: { k1Mult: 1.5, bMult: 1, temporalBoost: 1 },
  temporal: { k1Mult: 1, bMult: 0.67, temporalBoost: 2 },
  broad: { k1Mult: 0.67, bMult: 0.4, temporalBoost: 1 },
  multi_entity: { k1Mult: 0.8, bMult: 0.5, temporalBoost: 1 }
  // 宽松匹配，让多实体都能命中
};
const PRECISE_RE = /什么|哪个|哪里|几[个岁号]|多少|谁是|who|what|where|how\s*many/i;
const TEMPORAL_RE = /上次|之前|以前|上周|昨天|前天|上个月|最近|那时|那年|当时|when|last|before|after|ago|first\s+time|how\s+long|since\s+when|back\s+when|at\s+what\s+point|which\s+session|what\s+time/i;
let _currentQueryType = "broad";
let _twoPassInProgress = false;
function detectQueryType(query) {
  if (TEMPORAL_RE.test(query)) return "temporal";
  const names = (query.match(/\b[A-Z][a-z]{2,}\b/g) || []).filter((n) => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not|And|But|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|May|June|July|August|September|October|November|December)$/.test(n));
  if (names.length >= 2) return "multi_entity";
  if (PRECISE_RE.test(query)) return "precise";
  return "broad";
}
function getAdaptiveParams(queryType, query) {
  const baseK1 = _getAutoTuneParam("memory.bm25_k1");
  const baseB = _getAutoTuneParam("memory.bm25_b");
  const mult = QUERY_TYPE_MULTIPLIERS[queryType];
  const isChinese = query ? /[\u4e00-\u9fff]/.test(query) : true;
  const langK1 = isChinese ? 1 : 1.25;
  const langB = isChinese ? 1 : 0.67;
  return {
    k1: baseK1 * mult.k1Mult * langK1,
    b: baseB * mult.bMult * langB,
    temporalBoost: mult.temporalBoost
  };
}
function contextMatch(query, mem, expandedWords, memBaseActivation) {
  const content = mem.content || "";
  const contentLower = content.toLowerCase();
  const memWords = /* @__PURE__ */ new Set();
  const cjkSegs = content.match(/[\u4e00-\u9fff]+/g) || [];
  for (const seg of cjkSegs) {
    if (seg.length >= 2 && seg.length <= 4) memWords.add(seg);
    if (seg.length > 4) {
      for (let i = 0; i <= seg.length - 2; i++) {
        const frag = seg.slice(i, i + 2);
        if (expandedWords.has(frag)) memWords.add(frag);
      }
      for (let len = 3; len <= Math.min(4, seg.length); len++) {
        for (let i = 0; i <= seg.length - len; i++) memWords.add(seg.slice(i, i + len));
      }
    }
    if (seg.length > 2 && seg.length <= 4) {
      for (let i = 0; i <= seg.length - 2; i++) memWords.add(seg.slice(i, i + 2));
    }
  }
  const enWords = content.match(/[a-zA-Z]{2,}|\d+/gi) || [];
  for (const w of enWords) {
    const wl = w.toLowerCase();
    memWords.add(wl);
    if (/^[a-zA-Z]{2,}$/.test(w)) memWords.add(porterStem(wl));
  }
  const _mk = mem._mergedKeywords;
  if (_mk) for (const w of _mk) {
    memWords.add(w);
    memWords.add(porterStem(w));
  }
  const adaptiveParams = getAdaptiveParams(_currentQueryType, query);
  const BM25_DELTA = adaptiveParams.k1;
  const _bm25Denom = _currentAvgDocLen >= 10 ? _currentAvgDocLen : Math.max(expandedWords.size, 10);
  const lengthNorm = 1 - adaptiveParams.b + adaptiveParams.b * (memWords.size / _bm25Denom);
  let originalHits = 0, originalDenom = 0;
  let expansionHits = 0, expansionTotal = 0;
  let tier2Hits = 0, tier2Total = 0;
  for (const [word, weight] of expandedWords) {
    const idfWeight = _idfCache?.get(word) ?? 1;
    const AWDF_ALPHA = 0.5;
    const totalAct = _wordActivationSum?.get(word) ?? 0;
    const awdf = memBaseActivation !== void 0 && totalAct > 0 ? memBaseActivation / totalAct : 0;
    const effectiveWeight = weight * idfWeight * (1 + AWDF_ALPHA * awdf);
    const saturation = (adaptiveParams.k1 + 1) / (lengthNorm + adaptiveParams.k1);
    const hitValue = effectiveWeight * saturation + BM25_DELTA;
    const maxValue = effectiveWeight * ((adaptiveParams.k1 + 1) / (1 + adaptiveParams.k1)) + BM25_DELTA;
    const isOriginal = weight >= 0.9;
    const stemmed = /^[a-zA-Z]{2,}$/.test(word) ? porterStem(word) : null;
    const matched = memWords.has(word) || stemmed !== null && memWords.has(stemmed);
    if (isOriginal) {
      originalDenom += maxValue;
      if (matched) originalHits += hitValue;
    } else {
      expansionTotal += maxValue;
      if (matched) expansionHits += hitValue;
    }
    tier2Total += maxValue;
    if (matched) tier2Hits += hitValue;
  }
  const safeDenom = Math.max(originalDenom, 0.01);
  const safeExpDenom = Math.max(expansionTotal, 0.01);
  const baseScore = originalHits / safeDenom;
  const expansionBonus = expansionHits * 0.5 / safeExpDenom;
  const tier1Score = baseScore + expansionBonus;
  const tier2Score = tier2Total > 0 ? tier2Hits / tier2Total : 0;
  const rawWordScore = Math.max(tier1Score, tier2Score * 0.7);
  const _hasCJK = /[\u4e00-\u9fff]/.test(query);
  const _expandedCount = Math.max(1, expandedWords.size);
  const minCoverage = _hasCJK ? _currentQueryType === "broad" ? 0.01 : 0.03 : Math.max(5e-3, 1 / _expandedCount);
  const wordScore = rawWordScore < minCoverage ? 0 : rawWordScore;
  const queryLower = query.toLowerCase();
  const queryTokens = (queryLower.match(WORD_PATTERN.CJK24_EN2_NUM) || []).map((w) => w.toLowerCase());
  let phraseScore = 0;
  if (queryTokens.length >= 2) {
    let phraseHits = 0, phrasePossible = 0;
    for (let i = 0; i < queryTokens.length - 1; i++) {
      const bigram = queryTokens[i] + " " + queryTokens[i + 1];
      const bigramNoSpace = queryTokens[i] + queryTokens[i + 1];
      phrasePossible++;
      if (contentLower.includes(bigram) || contentLower.includes(bigramNoSpace)) phraseHits++;
    }
    for (let i = 0; i < queryTokens.length - 2; i++) {
      const trigram = queryTokens[i] + " " + queryTokens[i + 1] + " " + queryTokens[i + 2];
      phrasePossible++;
      if (contentLower.includes(trigram)) phraseHits += 2;
    }
    phraseScore = phrasePossible > 0 ? phraseHits / phrasePossible : 0;
  }
  const triScore = trigramSimilarity(trigrams(query), trigrams(content));
  const _enRatio = (query.match(/[a-zA-Z]+/g) || []).join("").length / Math.max(query.length, 1);
  const _triWeight = _enRatio > 0.5 ? 1 : 0.8;
  let sshScore = 0;
  if (_sshQueryDims.size > 0) {
    const memDims = _sshMemDims.get(contentLower);
    if (memDims && memDims.size > 0) {
      let wo = 0, tw = 0;
      for (const d of _sshQueryDims) {
        const df = _sshDimFreqMap.get(d) || 1;
        const idf = 1 / Math.max(1, df);
        tw += idf;
        if (memDims.has(d)) wo += idf;
      }
      sshScore = tw > 0 ? wo / tw : 0;
    }
  }
  let cerScore = 0;
  const _cerEntities = (query.match(/\b[A-Z][a-z]{2,}\b/g) || []).filter((n) => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$/.test(n));
  if (_cerEntities.length > 0) {
    const entityHit = _cerEntities.some((n) => contentLower.includes(n.toLowerCase()));
    if (entityHit) {
      const _cerContentWords = (query.match(/[a-zA-Z]{4,}/gi) || []).map((w) => w.toLowerCase()).filter((w) => !EN_STOP_WORDS.has(w) && !_cerEntities.map((e) => e.toLowerCase()).includes(w));
      const contentHits = _cerContentWords.filter((w) => {
        if (contentLower.includes(w)) return true;
        const stem = porterStem(w);
        return stem !== w && contentLower.includes(stem);
      }).length;
      if (contentHits > 0) {
        cerScore = Math.min(0.8, contentHits / Math.max(_cerContentWords.length, 1));
      }
    }
  }
  const _cmScores = [wordScore, phraseScore * 1.2, triScore * _triWeight, sshScore * 0.8, cerScore * 0.9].sort((a, b) => b - a);
  return _cmScores[0] + (_cmScores.length >= 2 && _cmScores[1] > 0.05 ? _cmScores[1] * 0.15 : 0);
}
function emotionResonance(mem, currentMood, currentAlertness) {
  let score = 0.5;
  if (mem.situationCtx?.mood !== void 0) {
    const moodDist = Math.abs(currentMood - mem.situationCtx.mood);
    const alertDist = Math.abs(currentAlertness - (mem.situationCtx.energy || 0.5));
    const stateDist = Math.sqrt(moodDist * moodDist + alertDist * alertDist);
    const gate = 1 / (1 + Math.exp(stateDist * 3 - 1.5));
    score *= Math.max(0.2, gate);
  }
  if (currentMood > 0.3 && mem.emotion === "warm") score *= 1.4;
  if (currentMood < -0.3 && mem.emotion === "painful") score *= 1.4;
  const ei = mem.emotionIntensity || 0;
  score *= 1 + ei * 0.5;
  return Math.min(1, score);
}
let _aamGetNeighbors = null;
function getAAMNeighborsFn() {
  if (_aamGetNeighbors === false) return null;
  if (_aamGetNeighbors) return _aamGetNeighbors;
  try {
    _aamGetNeighbors = _aamGetAAMNeighbors || false;
    return _aamGetNeighbors || null;
  } catch {
    _aamGetNeighbors = false;
    return null;
  }
}
let _erfCache = null;
let _aamNeighborCache = null;
function buildEntityResonanceField(query, memories) {
  const erf = /* @__PURE__ */ new Map();
  try {
    const graph = _graphMod;
    if (!graph.findMentionedEntities || !graph.getRelatedEntities) return erf;
    const queryEntities = graph.findMentionedEntities(query);
    for (const e of queryEntities) erf.set(e, 1);
    const queryWords = query.match(WORD_PATTERN.CJK24_EN3) || [];
    for (const w of queryWords) {
      if (!erf.has(w) && graph.findMentionedEntities(w).length > 0) {
        erf.set(w, 0.8);
      }
    }
    if (erf.size === 0) return erf;
    const hop1 = graph.getRelatedEntities([...erf.keys()], 1, 20);
    for (const e of hop1) {
      if (!erf.has(e)) erf.set(e, 0.5);
    }
    const hop2 = graph.getRelatedEntities(hop1, 1, 15);
    for (const e of hop2) {
      if (!erf.has(e)) erf.set(e, 0.25);
    }
  } catch {
  }
  return erf;
}
function getEntityResonance(mem, erf) {
  if (erf.size === 0) return 0;
  const content = mem.content || "";
  let totalResonance = 0;
  let entityCount = 0;
  for (const [entity, activation] of erf) {
    if (content.includes(entity)) {
      totalResonance += activation;
      entityCount++;
    }
  }
  if (entityCount === 0) return 0;
  const capBase = entityCount >= 2 ? 0.65 : entityCount === 1 ? 0.5 : 0.4;
  return Math.min(capBase, totalResonance * 0.15 * Math.sqrt(entityCount));
}
function spreadingActivation(mem, allMemories, query) {
  const hasTags = mem.tags && mem.tags.length > 0;
  const myTags = hasTags ? new Set(mem.tags.map((t) => t.toLowerCase())) : /* @__PURE__ */ new Set();
  let totalSpread = 0;
  let count = 0;
  if (hasTags) {
    for (const other of allMemories) {
      if (other === mem || !other.tags || other.tags.length === 0) continue;
      const otherActivation = getActivation(other);
      if (otherActivation < 0.2) continue;
      const shared = other.tags.filter((t) => myTags.has(t.toLowerCase())).length;
      if (shared > 0) {
        totalSpread += otherActivation * (shared / Math.max(myTags.size, 1)) * 0.3;
        count++;
      }
      if (count >= 10) break;
    }
  }
  if (count < 3 && query && _aamNeighborCache && _aamNeighborCache.size > 0) {
    const memKeywords = (mem.content || "").match(WORD_PATTERN.CJK24_EN3) || [];
    let aamBoost = 0;
    for (const kw of memKeywords.slice(0, 8)) {
      const score = _aamNeighborCache.get(kw.toLowerCase());
      if (score) aamBoost += score;
    }
    totalSpread += Math.min(0.3, aamBoost);
  }
  if (_erfCache && _erfCache.size > 0) {
    const erfBoost = getEntityResonance(mem, _erfCache);
    if (erfBoost > 0) totalSpread += erfBoost;
  }
  return Math.min(0.6, totalSpread);
}
function interferenceMMR(memTri, selectedTris, isSummary, memAge, selectedAges) {
  if (selectedTris.length === 0) return 1;
  let maxSim = 0;
  let maxSimIdx = 0;
  for (let i = 0; i < selectedTris.length; i++) {
    const sim = trigramSimilarity(memTri, selectedTris[i]);
    if (sim > maxSim) {
      maxSim = sim;
      maxSimIdx = i;
    }
  }
  let temporalFactor = 1;
  if (memAge !== void 0 && selectedAges && selectedAges.length > maxSimIdx) {
    const selAge = selectedAges[maxSimIdx];
    if (selAge > 0 && memAge > 0) {
      const logDist = Math.abs(Math.log(memAge + 1) - Math.log(selAge + 1));
      temporalFactor = 1 + 0.3 * Math.exp(-2 * logDist);
    }
  }
  const effectiveSim = Math.min(1, maxSim * temporalFactor);
  if (isSummary) {
    if (effectiveSim > TRIGRAM_THRESHOLD.DEDUP_MERGE) return 0.5;
    if (effectiveSim > TRIGRAM_THRESHOLD.INTERFERENCE_STRONG) return 0.8;
  } else {
    if (effectiveSim > TRIGRAM_THRESHOLD.INTERFERENCE_STRONG) return 0.3;
    if (effectiveSim > TRIGRAM_THRESHOLD.INTERFERENCE_LIGHT) return 0.7;
  }
  return 1;
}
function temporalContext(mem, timeRange, queryWords) {
  if (timeRange) {
    const ts = mem.ts || 0;
    if (ts >= timeRange.fromMs && ts <= timeRange.toMs) return 1;
    const span = timeRange.toMs - timeRange.fromMs || 864e5;
    const dist = Math.min(Math.abs(ts - timeRange.fromMs), Math.abs(ts - timeRange.toMs));
    return Math.max(0, 1 - dist / span);
  }
  const now = /* @__PURE__ */ new Date();
  const memDate = new Date(mem.ts || Date.now());
  const hourDiff = Math.abs(now.getHours() - memDate.getHours());
  const timeMatch = 1 - Math.min(hourDiff, 24 - hourDiff) / 12;
  const sameType = (now.getDay() === 0 || now.getDay() === 6) === (memDate.getDay() === 0 || memDate.getDay() === 6) ? 1 : 0.8;
  let encodingSpecificity = 0;
  if (queryWords && queryWords.size > 0 && mem.recallContexts && mem.recallContexts.length > 0) {
    for (const ctx of mem.recallContexts) {
      const ctxWords = (ctx.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase());
      const overlap = ctxWords.filter((w) => queryWords.has(w)).length;
      if (overlap >= 2) {
        encodingSpecificity = Math.min(0.3, overlap * 0.08);
        break;
      }
    }
  }
  const base = timeMatch * 0.5 + sameType * 0.5 + encodingSpecificity;
  const tBoost = QUERY_TYPE_MULTIPLIERS[_currentQueryType]?.temporalBoost ?? 1;
  return Math.min(1, base * tBoost);
}
function computeActivationField(memories, query, mood, alertness, expandedWords, topN = 10, timeRange, cogHints) {
  const now = Date.now();
  const _imaf = (() => {
    if (cogHints) {
      const h = cogHints;
      const isTemporalQ = /什么时候|上次|上周|when did|last time|recently|what happened|ago|how long/i.test(query);
      const hasEntityName = !!query.match(/\b[A-Z][a-z]{2,}\b/g)?.filter((n) => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n)).length;
      const isCausalQ = /为什么|原因|导致|why|because|cause|reason|how come/i.test(query);
      let s1 = 1 - 0.3 * h.casualProb;
      let s2 = 1 + 0.5 * h.technicalProb;
      let s3 = 0.3 + 1.7 * h.emotionalProb;
      let s4 = 1 + 1 * h.complexity;
      let s6 = 1 + 0.5 * h.correctionProb;
      if (isTemporalQ) {
        s1 += 1;
        s6 += 2;
        s3 *= 0.3;
        s4 *= 0.5;
      }
      if (hasEntityName) {
        s2 += 0.5;
        s4 += 1;
      }
      if (isCausalQ) {
        s4 += 1;
        s6 += 0.5;
      }
      return { s1, s2, s3, s4, s6 };
    }
    if (/为什么|原因|导致|why|because|cause|reason|how come/i.test(query))
      return { s1: 1, s2: 1, s3: 0.5, s4: 2, s6: 1.5 };
    if (/什么时候|上次|上周|when did|last time|recently|what happened|ago/i.test(query))
      return { s1: 2, s2: 0.8, s3: 0.3, s4: 0.5, s6: 3 };
    if (query.match(/\b[A-Z][a-z]{2,}\b/g)?.filter((n) => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could)$/.test(n)).length)
      return { s1: 0.8, s2: 1.5, s3: 0.5, s4: 2, s6: 0.8 };
    if (/感觉|心情|开心|难过|焦虑|feel|happy|sad|anxious|stressed|mood/i.test(query))
      return { s1: 0.8, s2: 1, s3: 2, s4: 0.5, s6: 0.5 };
    return { s1: 1, s2: 1, s3: 1, s4: 1, s6: 1 };
  })();
  _currentAvgDocLen = memories.reduce((s, m) => s + ((m.content || "").match(/[\u4e00-\u9fff]|[a-zA-Z]+/g) || []).length, 0) / Math.max(memories.length, 1);
  if (!_idfCache || _currentIdfVersion !== _idfVersion) {
    _idfCache = buildIdfCache(memories);
    _currentIdfVersion = _idfVersion;
  }
  _erfCache = buildEntityResonanceField(query, memories);
  _sshMemDims = /* @__PURE__ */ new Map();
  _sshDimFreqMap = /* @__PURE__ */ new Map();
  _sshQueryDims = /* @__PURE__ */ new Set();
  if (!/[\u4e00-\u9fff]/.test(query)) {
    try {
      const { getSemanticDimensions: _getSSD } = require("./aam.ts");
      if (_getSSD) {
        for (const mem of memories) {
          const cl = (mem.content || "").toLowerCase();
          const ws = cl.match(/[a-zA-Z]{3,}/gi) || [];
          const dims = /* @__PURE__ */ new Set();
          for (const w of ws.slice(0, 20)) {
            const wd = _getSSD(w.toLowerCase());
            for (const d of wd) dims.add(d);
          }
          if (dims.size > 0) {
            _sshMemDims.set(cl, dims);
            for (const d of dims) _sshDimFreqMap.set(d, (_sshDimFreqMap.get(d) || 0) + 1);
          }
        }
        for (const [w, wt] of expandedWords) {
          if (wt >= 0.5) {
            const wd = _getSSD(w);
            for (const d of wd) _sshQueryDims.add(d);
          }
        }
      }
    } catch {
    }
  }
  _aamNeighborCache = /* @__PURE__ */ new Map();
  try {
    const fn = getAAMNeighborsFn();
    if (fn) {
      const queryWords = new Set(
        (query.toLowerCase().match(WORD_PATTERN.CJK24_EN3) || []).map((w) => w.toLowerCase())
      );
      for (const qw of queryWords) {
        const neighbors = fn(qw, 5);
        for (const n of neighbors) {
          const fanDamping = 1 / Math.sqrt(Math.max(1, n.fanOut));
          const score = n.pmiScore / 5 * fanDamping;
          const existing = _aamNeighborCache.get(n.word) || 0;
          if (score > existing) _aamNeighborCache.set(n.word, score);
        }
      }
    }
  } catch {
  }
  const results = [];
  const currentTop = [];
  const queryWordSet = /* @__PURE__ */ new Set();
  const queryLower = query.toLowerCase();
  const qCjk = queryLower.match(/[\u4e00-\u9fff]{2,4}/g) || [];
  for (const s of qCjk) queryWordSet.add(s);
  const qEn = queryLower.match(/[a-zA-Z]{3,}/gi) || [];
  for (const w of qEn) queryWordSet.add(w.toLowerCase());
  let temporalSuccessors = null;
  try {
    if (_aamGetTemporalSuccessors) {
      temporalSuccessors = /* @__PURE__ */ new Set();
      for (const qw of queryWordSet) {
        const succs = _aamGetTemporalSuccessors(qw, 5);
        if (succs) for (const s of succs) temporalSuccessors.add(s.word);
      }
    }
  } catch {
  }
  const isColdStart = _activations.size < 10;
  if (isColdStart) {
    _baseWeight = 0.15;
    _contextWeight = 0.85;
  }
  const rawResults = [];
  for (const mem of memories) {
    if (mem.scope === "expired" || mem.scope === "decayed") continue;
    if (!mem.content || mem.content.length < 3) continue;
    const s1 = baseActivation(mem, now);
    const s2 = contextMatch(query, mem, expandedWords, s1);
    if (s2 < 2e-3) continue;
    const s3 = emotionResonance(mem, mood, alertness);
    const s4 = spreadingActivation(mem, memories, query);
    const s6 = temporalContext(mem, timeRange, queryWordSet);
    const { base: wBase, context: wCtx } = getSignalWeights();
    const baseContextScore = wBase * _imaf.s1 * s1 + wCtx * _imaf.s2 * s2;
    const raw = baseContextScore * (0.5 + _emotionCoeff * _imaf.s3 * s3) * (1 + _spreadCoeff * _imaf.s4 * s4) * (0.8 + _temporalCoeff * _imaf.s6 * s6);
    const conf = mem.confidence ?? 0.7;
    const confScale = 0.6 + conf * 0.4;
    let impBoost = 1 + Math.max(0, (mem.importance ?? 5) - 5) * 0.05;
    if (mem.scope === "correction") impBoost *= 1.5;
    if (mem.supersededBy) impBoost *= 0.3;
    let s7 = 0;
    if (temporalSuccessors && temporalSuccessors.size > 0) {
      const memContentLower = (mem.content || "").toLowerCase();
      const memW = memContentLower.match(WORD_PATTERN.CJK24_EN3) || [];
      let hits = 0;
      for (const w of memW) {
        if (temporalSuccessors.has(w.toLowerCase())) hits++;
        if (hits >= 3) break;
      }
      s7 = Math.min(0.3, hits * 0.1);
    }
    const momentum = getMomentumBoost(mem.content || "");
    let s8 = 0;
    if (mem.prospectiveTags?.length > 0) {
      let ptHits = 0;
      for (const tag of mem.prospectiveTags) {
        const tl = tag.toLowerCase();
        if (expandedWords.has(tl) || queryLower.includes(tl)) ptHits++;
      }
      if (ptHits > 0) s8 = Math.min(1, ptHits / mem.prospectiveTags.length * 2);
    }
    const utilityMod = 1 + (mem.utility ?? 0) * 0.1;
    let microLinkBoost = 1;
    if (mem.microLinks && mem.microLinks.length > 0) {
      const qWords = new Set((queryLower.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase()));
      let linkHits = 0;
      for (const link of mem.microLinks) {
        if (link.sharedKeywords?.some((k) => qWords.has(k.toLowerCase()))) linkHits++;
      }
      if (linkHits > 0) microLinkBoost = 1 + Math.min(0.2, linkHits * 0.05);
    }
    const insightBoost = mem.scope === "insight" || mem.scope === "reflexion" ? 1.15 : 1;
    let personModelMod = 1;
    try {
      const { getPersonModel } = require("./person-model.ts");
      const pm = getPersonModel();
      if (pm?.thinkingStyle) {
        const style = pm.thinkingStyle;
        if (style === "analytical" && (mem.scope === "fact" || mem.tags?.some((t) => t.includes("tech")))) personModelMod = 1.1;
        if (style === "emotional" && (mem.scope === "event" || mem.tags?.some((t) => t.includes("emotion")))) personModelMod = 1.1;
      }
    } catch {
    }
    const catWeight = getCategoryWeight(mem);
    const finalRaw = raw * confScale * impBoost * (1 + _momentumCoeff * momentum) * (1 + _pamCoeff * s7) * (1 + s8 * 0.5) * utilityMod * catWeight * microLinkBoost * insightBoost * personModelMod;
    const path = [
      { stage: "candidate_selection", via: s2 > 0.3 ? "aam_context" : "bm25", rawScore: s2 },
      { stage: "signal_boost", via: "base_activation", rawScore: s1 }
    ];
    if (s3 > 0.6) path.push({ stage: "signal_boost", via: "emotion", rawScore: s3 });
    if (s4 > 0.05) path.push({ stage: "signal_boost", via: "spread", rawScore: s4 });
    if (s6 > 0.7) path.push({ stage: "signal_boost", via: "temporal", rawScore: s6 });
    if (confScale > 0.8) path.push({ stage: "signal_boost", via: "confidence", rawScore: confScale });
    if (impBoost > 1) path.push({ stage: "signal_boost", via: "importance", rawScore: impBoost });
    if (momentum > 0.05) path.push({ stage: "signal_boost", via: "momentum", rawScore: momentum });
    if (s7 > 0.01) path.push({ stage: "signal_boost", via: "temporal_cooccur", rawScore: s7 });
    if (finalRaw > 1e-3) {
      rawResults.push({
        mem,
        raw: finalRaw,
        signals: { base: s1, context: s2, emotion: s3, spread: s4, interference: 1, temporal: s6 },
        path
      });
    }
  }
  rawResults.sort((a, b) => b.raw - a.raw);
  const PAM_TS_WINDOW = 5e3;
  const PAM_BATCH_BOOST = 1.2;
  const topK = Math.min(3, rawResults.length);
  for (let i = topK; i < rawResults.length; i++) {
    const cTs = rawResults[i].mem.ts || 0;
    for (let j = 0; j < topK; j++) {
      const tTs = rawResults[j].mem.ts || 0;
      if (Math.abs(cTs - tTs) < PAM_TS_WINDOW && rawResults[i].mem.content !== rawResults[j].mem.content) {
        rawResults[i].raw *= PAM_BATCH_BOOST;
        break;
      }
    }
  }
  rawResults.sort((a, b) => b.raw - a.raw);
  const _trigramCache = /* @__PURE__ */ new Map();
  const _getTriCached = (content) => {
    let tri = _trigramCache.get(content);
    if (!tri) {
      tri = trigrams(content);
      _trigramCache.set(content, tri);
    }
    return tri;
  };
  const selectedTris = [];
  const selectedAges = [];
  for (const r of rawResults) {
    const memContent = r.mem.content || "";
    const memTri = _getTriCached(memContent);
    const isSummary = r.mem.scope === "fact" || r.mem.scope === "consolidated" || memContent.startsWith("[summary]") || memContent.startsWith("[Session");
    const memAge = now - (r.mem.ts || now);
    const s5 = interferenceMMR(memTri, selectedTris, isSummary, memAge, selectedAges);
    let activation = r.raw * s5;
    try {
      const content = r.mem.content || "";
      const contentWords = content.match(WORD_PATTERN.CJK2_EN3) || [];
      let driftMod = 1;
      for (const w of contentWords.slice(0, 5)) {
        const m = _getDriftModifier(w.toLowerCase());
        if (m !== 1) {
          driftMod = m;
          break;
        }
      }
      activation *= driftMod;
    } catch {
    }
    try {
      activation *= _getConfModifier(r.mem);
    } catch {
    }
    r.signals.interference = s5;
    if (s5 < 1) r.path.push({ stage: "signal_suppress", via: "interference", rawScore: s5 });
    setActivation(r.mem, activation);
    if (activation > 1e-3) {
      results.push({
        memory: r.mem,
        activation,
        signals: r.signals,
        path: r.path
      });
      currentTop.push(r.mem);
      selectedTris.push(memTri);
      selectedAges.push(memAge);
    }
    if (results.length >= topN) break;
  }
  if (results.length > 0) {
    const selectedContents = new Set(results.map((r) => (r.memory.content || "").slice(0, 50)));
    const selectedWords = /* @__PURE__ */ new Set();
    for (const r of results) {
      const ws = (r.memory.content || "").match(WORD_PATTERN.CJK2_EN3) || [];
      for (const w of ws) selectedWords.add(w.toLowerCase());
    }
    const rifStart = Math.min(results.length, rawResults.length);
    const rifEnd = Math.min(rifStart + 30, rawResults.length);
    for (let i = rifStart; i < rifEnd; i++) {
      const r = rawResults[i];
      if (selectedContents.has((r.mem.content || "").slice(0, 50))) continue;
      if (r.mem.scope === "core_memory" || r.mem.scope === "correction") continue;
      const mw = (r.mem.content || "").match(WORD_PATTERN.CJK2_EN3) || [];
      let overlap = 0;
      for (const w of mw) {
        if (selectedWords.has(w.toLowerCase())) overlap++;
      }
      if (mw.length > 0 && overlap / mw.length > 0.4) {
        const curAct = getActivation(r.mem);
        if (curAct > 0.05) setActivation(r.mem, curAct * 0.95);
      }
    }
  }
  const turnTs = Date.now();
  const traces = results.map((r) => ({
    memory: r.memory,
    score: r.activation,
    path: r.path || []
  }));
  const rejections = [];
  const selectedSet = new Set(results.map((r) => memKey(r.memory)));
  for (let i = 0; i < Math.min(20, rawResults.length); i++) {
    if (!selectedSet.has(memKey(rawResults[i].mem))) {
      rejections.push({
        content: (rawResults[i].mem.content || "").slice(0, 30),
        originalRank: i + 1,
        finalRank: -1,
        reason: rawResults[i].signals.interference < 1 ? "interference" : "below_threshold"
      });
    }
  }
  _traceBuffer.set(turnTs, { traces, rejections });
  pruneTraceBuffer();
  return results;
}
function decayAllActivations(factor = 0.995) {
  for (const [key, val] of _activations) {
    const newVal = val * factor;
    if (newVal < 0.01) {
      _activations.delete(key);
    } else {
      _activations.set(key, newVal);
    }
  }
}
const EN_STOP_WORDS = /* @__PURE__ */ new Set([
  "the",
  "and",
  "for",
  "that",
  "this",
  "with",
  "from",
  "are",
  "was",
  "were",
  "not",
  "but",
  "have",
  "has",
  "had",
  "will",
  "can",
  "you",
  "your",
  "they",
  "them",
  "their",
  "what",
  "when",
  "where",
  "which",
  "who",
  "whom",
  "how",
  "did",
  "does",
  "would",
  "could",
  "should",
  "been",
  "being",
  "its",
  "she",
  "her",
  "his",
  "him",
  "all",
  "also",
  "than",
  "then",
  "some",
  "such",
  "about",
  "after",
  "before",
  "between",
  "into",
  "through",
  "during",
  "each",
  "very",
  "just",
  "other",
  "more",
  "most",
  "only",
  "over"
]);
function expandQueryForField(query) {
  const expanded = /* @__PURE__ */ new Map();
  const cjkSegs = query.match(/[\u4e00-\u9fff]+/g) || [];
  for (const seg of cjkSegs) {
    for (let i = 0; i <= seg.length - 2; i++) expanded.set(seg.slice(i, i + 2), 1);
    if (seg.length >= 3 && seg.length <= 4) expanded.set(seg, 1);
  }
  const _QUERY_SIGNAL_WORDS = /* @__PURE__ */ new Set(["what", "where", "when", "how", "which", "did", "does", "who", "whom"]);
  const enWords = query.match(/[a-zA-Z]{2,}|\d+/gi) || [];
  for (const w of enWords) {
    const wl = w.toLowerCase();
    const weight = _QUERY_SIGNAL_WORDS.has(wl) ? 0.5 : EN_STOP_WORDS.has(wl) ? 0.1 : 1;
    expanded.set(wl, weight);
    if (/^[a-zA-Z]{2,}$/.test(w)) {
      const stemmed = porterStem(wl);
      if (stemmed !== wl && !expanded.has(stemmed)) expanded.set(stemmed, weight);
    }
  }
  if (query.length < 15) {
    const singleChars = query.match(/[\u4e00-\u9fff]/g) || [];
    for (const ch of singleChars) {
      if (!expanded.has(ch)) expanded.set(ch, 0.5);
    }
  }
  const KNOWN_SINGLE_CJK = new Set("\u5403\u559D\u7761\u8D70\u8DD1\u5750\u7AD9\u770B\u542C\u8BF4\u5199\u8BFB\u6D17\u7A7F\u4E70\u5356\u8F66\u94B1\u623F\u4E66\u836F\u9152\u8336\u6015\u86C7\u732B\u72D7\u9C7C\u5B66\u73A9\u4F4F\u98DE\u9A91\u6E38".split(""));
  const queryWords = [];
  for (const [w, wt] of expanded) {
    if (wt < 0.3) continue;
    if (w.length === 1 && /[\u4e00-\u9fff]/.test(w)) {
      if (KNOWN_SINGLE_CJK.has(w)) queryWords.push(w);
    } else if (w.length < 2) {
    } else if (/[a-zA-Z]/.test(w) || w.length >= 3) {
      queryWords.push(w);
    } else {
      if (_aamIsKnownWord(w)) queryWords.push(w);
    }
  }
  const _ABSTRACT_WORDS = /* @__PURE__ */ new Set([
    "\u65B9\u5F0F",
    "\u4E60\u60EF",
    "\u54C1\u5473",
    "\u7231\u597D",
    "\u7279\u70B9",
    "\u6027\u683C",
    "\u89C4\u5212",
    "\u60F3\u6CD5",
    "\u538B\u529B",
    "\u8D1F\u62C5",
    "\u6D3B\u52A8",
    "\u60C5\u51B5",
    "\u7ECF\u5386",
    "\u504F\u597D",
    "\u98CE\u683C",
    "\u6C34\u5E73",
    "\u80FD\u529B",
    "\u72B6\u51B5",
    "\u6001\u5EA6",
    "\u76EE\u6807",
    "\u8BA1\u5212",
    "\u6761\u4EF6",
    "\u80CC\u666F",
    "\u5708\u5B50",
    "style",
    "habit",
    "taste",
    "hobby",
    "trait",
    "plan",
    "idea",
    "preference",
    "routine",
    "activity",
    "experience",
    "skill"
  ]);
  const _contentWords = queryWords.filter((w) => !EN_STOP_WORDS.has(w) && w.length >= 2);
  const _queryAbstract = _contentWords.length > 0 && _contentWords.some((w) => _ABSTRACT_WORDS.has(w));
  try {
    const _aamMaxExp = _queryAbstract ? 30 : 20;
    const _aamMinW = _queryAbstract ? 0.1 : 0.15;
    const aamExpanded = _aamExpandQuery(queryWords, _aamMaxExp);
    for (const { word, weight } of aamExpanded) {
      if (weight >= _aamMinW && !expanded.has(word)) {
        const idf = _idfCache?.get(word) ?? 0.5;
        const adjustedWeight = weight * Math.max(0.3, idf);
        expanded.set(word, adjustedWeight);
      }
    }
    if (_queryAbstract) {
      console.log(`[activation-field] abstract query detected: maxExp=${_aamMaxExp}, minW=${_aamMinW}, expanded=${expanded.size}`);
    }
  } catch {
  }
  if (query.length < 10) {
    const singleChars = query.match(/[\u4e00-\u9fff]/g) || [];
    for (const ch of singleChars) {
      if (!expanded.has(ch)) expanded.set(ch, 0.3);
    }
  }
  try {
    for (const [w, wt] of [...expanded.entries()]) {
      if (w.length === 1 && /[\u4e00-\u9fff]/.test(w) && wt <= 0.3) {
        if (_aamIsKnownWord(w)) {
          expanded.set(w, 0.8);
        }
      }
    }
  } catch {
  }
  if (!process.env.CC_SOUL_BENCHMARK) {
    try {
      const { getTopPredictions } = require("./behavioral-phase-space.ts");
      const predictions = getTopPredictions?.(3) || [];
      for (const pred of predictions) {
        const word = (pred.topic || pred.word || "").toLowerCase();
        if (word.length >= 2 && !expanded.has(word)) {
          expanded.set(word, (pred.probability || 0.3) * 0.3);
        }
      }
    } catch {
    }
  }
  return expanded;
}
function activationRecall(memories, query, topN = 5, mood = 0, alertness = 0.5, cogHints) {
  if (!query || memories.length === 0) return [];
  const _queryNames = [];
  const _enNameCandidates = query.match(/\b([A-Z][a-z]{2,})\b/g) || [];
  const _NON_NAMES = /* @__PURE__ */ new Set(["What", "When", "Where", "Which", "Who", "How", "Why", "The", "This", "That", "Does", "Did", "Has", "Have", "Was", "Were", "Can", "Could", "Would", "Should", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]);
  for (const n of _enNameCandidates) {
    if (!_NON_NAMES.has(n)) _queryNames.push(n.toLowerCase());
  }
  let _isAggregation = false;
  const _originalTopN = topN;
  _currentQueryType = detectQueryType(query);
  if (_currentQueryType === "temporal") {
    topN = Math.max(topN, 10);
  }
  const expanded = expandQueryForField(query);
  updateMomentum(query);
  let timeRange = null;
  try {
    timeRange = _extractTimeRange(query);
  } catch {
  }
  if (!timeRange) {
    try {
      const anchors = _extractAnchors(memories);
      if (anchors.length > 0) {
        const inferred = _inferTemporalRange(query, anchors);
        if (inferred) {
          timeRange = { fromMs: inferred.from, toMs: inferred.to };
          console.log(`[activation-field] temporal-anchor: inferred range [${new Date(inferred.from).toLocaleDateString()} ~ ${new Date(inferred.to).toLocaleDateString()}] from ${anchors.length} anchors`);
        }
      }
    } catch {
    }
  }
  let recencyBias = 0;
  if (!timeRange) {
    if (/最近|目前|现在|these days|lately|recently/i.test(query)) recencyBias = 7;
    if (/以前|之前|曾经|过去|当年|before|used to/i.test(query)) recencyBias = -1;
  }
  let lexicalQuery = query;
  try {
    const keywords = _extractTagsLocal(query);
    if (keywords.length > 0) lexicalQuery = keywords.join(" ");
  } catch {
  }
  const _NEG_PATTERNS = /不擅长|不喜欢|不爱|不想|不敢|不吃|不看|不会|害怕|讨厌|恐惧|反感|忌口|don't like|afraid of|hate|bad at|can't stand/i;
  const _NEG_QUESTION = /什么|吗|呢|哪|几|\?|？/;
  const _isNegationQuery = _NEG_PATTERNS.test(query) && _NEG_QUESTION.test(query);
  if (_isNegationQuery) {
    const _negSeedWords = [
      "\u653E\u5F03",
      "\u5931\u8D25",
      "\u4E0D\u4F1A",
      "\u6015",
      "\u8BA8\u538C",
      "\u96BE",
      "\u5DEE",
      "\u7CDF",
      "\u4E8F",
      "quit",
      "failed",
      "afraid",
      "hate",
      "bad",
      "lost"
    ];
    for (const nw of _negSeedWords) {
      if (!expanded.has(nw)) expanded.set(nw, 0.5);
    }
    try {
      const negExpanded = _aamExpandQuery(_negSeedWords.filter((w) => w.length >= 2), 10);
      for (const { word, weight } of negExpanded) {
        if (!expanded.has(word)) expanded.set(word, weight * 0.6);
      }
    } catch {
    }
    console.log(`[activation-field] negation query detected, expanded +${_negSeedWords.length} neg seeds`);
  }
  memories = categoryPrePrune(memories, query);
  let _parallelFactMems = [];
  try {
    const factStore = _factStoreMod;
    const allFacts = factStore.getAllFacts();
    const queryLowerS1 = query.toLowerCase();
    const queryTokensS1 = new Set((queryLowerS1.match(WORD_PATTERN.CJK24_EN2_NUM) || []).map((w) => w.toLowerCase()));
    for (const [w] of expanded) queryTokensS1.add(w.toLowerCase());
    const scoredFacts = [];
    for (const fact of allFacts) {
      if (fact.validUntil && fact.validUntil > 0 && fact.validUntil < Date.now()) continue;
      const objLower = (fact.object || "").toLowerCase();
      const predLower = (fact.predicate || "").toLowerCase();
      const subjLower = (fact.subject || "").toLowerCase();
      const factText = `${subjLower} ${predLower} ${objLower}`;
      const factTokens = (factText.match(WORD_PATTERN.CJK24_EN2_NUM) || []).map((w) => w.toLowerCase());
      let matchScore = 0;
      for (const token of queryTokensS1) {
        if (objLower.includes(token) || token.includes(objLower)) matchScore += 2;
        if (predLower.includes(token)) matchScore += 1.5;
        if (subjLower.includes(token)) matchScore += 0.5;
      }
      for (const ft of factTokens) {
        if (queryTokensS1.has(ft)) matchScore += 1;
      }
      matchScore *= fact.confidence || 0.7;
      if (matchScore > 0) {
        scoredFacts.push({
          mem: {
            content: `[\u4E8B\u5B9E] ${fact.predicate}: ${fact.object}`,
            scope: "fact",
            ts: fact.ts || Date.now(),
            confidence: fact.confidence || 0.9,
            source: "fact_store_parallel",
            recallCount: 10,
            lastAccessed: Date.now(),
            importance: 9
          },
          matchScore
        });
      }
    }
    scoredFacts.sort((a, b) => b.matchScore - a.matchScore);
    const predCount = /* @__PURE__ */ new Map();
    for (const sf of scoredFacts) {
      const pred = sf.mem.content.match(/\[事实\]\s*([^:]+)/)?.[1] || "";
      const count = predCount.get(pred) || 0;
      if (count < 2) {
        sf.mem._matchScore = sf.matchScore;
        _parallelFactMems.push(sf.mem);
        predCount.set(pred, count + 1);
      }
    }
    if (_parallelFactMems.length > 0) {
      console.log(`[activation-field] fact-store parallel: ${_parallelFactMems.length} facts scored from ${allFacts.length} total`);
    }
  } catch {
  }
  try {
    const aamExpansion = _aamExpandQuery(
      (query.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase()),
      5
    );
    if (aamExpansion.length > 0) {
      for (const exp of aamExpansion) {
        if (!expanded.has(exp.word)) {
          expanded.set(exp.word, exp.weight);
        }
      }
    }
  } catch {
  }
  const _baseOversample = memories.length <= 100 ? 2 : memories.length <= 300 ? 3 : 4;
  const _oversample = cogHints ? Math.min(4, Math.max(2, Math.round(_baseOversample * (0.7 + 0.6 * cogHints.complexity)))) : _baseOversample;
  let results = computeActivationField(memories, lexicalQuery, mood, alertness, expanded, topN * _oversample, timeRange, cogHints);
  if (results.length > 0 && results[0].activation < 0.5 && expanded.size > 5) {
    try {
      const altWords = [...expanded.entries()].filter(([w, wt]) => wt < 0.95 && wt >= 0.5 && w.length >= 3).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([w]) => w);
      if (altWords.length >= 2) {
        const altQuery = altWords.join(" ");
        const altExpanded = new Map(expanded);
        const altResults = computeActivationField(memories, altQuery, mood, alertness, altExpanded, topN * 2, timeRange, cogHints);
        const seenContent = new Set(results.map((r) => r.memory.content));
        for (const r of altResults) {
          if (!seenContent.has(r.memory.content)) {
            results.push(r);
            seenContent.add(r.memory.content);
          }
        }
        results.sort((a, b) => b.activation - a.activation);
      }
    } catch {
    }
  }
  if (_queryNames && _queryNames.length >= 1 && results.length > 0 && results[0].activation < 0.8) {
    try {
      const verbs = (lexicalQuery.match(/\b[a-z]{3,}(?:ed|ing|s|es)?\b/gi) || []).filter((w) => !EN_STOP_WORDS.has(w.toLowerCase()) && !_queryNames.includes(w.toLowerCase())).slice(0, 3);
      if (verbs.length >= 1) {
        const focusedQuery = _queryNames.join(" ") + " " + verbs.join(" ");
        const focusedResults = computeActivationField(memories, focusedQuery, mood, alertness, expanded, topN * 2, timeRange, cogHints);
        const seenContent = new Set(results.map((r) => r.memory.content));
        for (const r of focusedResults) {
          if (!seenContent.has(r.memory.content)) {
            results.push(r);
            seenContent.add(r.memory.content);
          }
        }
        results.sort((a, b) => b.activation - a.activation);
      }
    } catch {
    }
  }
  if (_currentQueryType === "temporal" && _queryNames && _queryNames.length >= 1 && results.length > 0) {
    try {
      const entityQuery = _queryNames.join(" ");
      const entityResults = computeActivationField(memories, entityQuery, mood, alertness, expanded, topN, timeRange, cogHints);
      const seenContent = new Set(results.map((r) => r.memory.content));
      let added = 0;
      for (const r of entityResults) {
        if (!seenContent.has(r.memory.content)) {
          results.push(r);
          seenContent.add(r.memory.content);
          added++;
          if (added >= 5) break;
        }
      }
      if (added > 0) results.sort((a, b) => b.activation - a.activation);
    } catch {
    }
  }
  if (results.length >= 5) {
    const _scores = results.slice(0, Math.min(10, results.length)).map((r) => r.activation);
    const _topScore = _scores[0];
    const _tailScore = _scores[_scores.length - 1];
    const _dropoff = _topScore > 0 ? (_topScore - _tailScore) / _topScore : 1;
    let _dropoffThreshold = 0.3;
    try {
      _dropoffThreshold = require("./auto-tune.ts").getParam("recall.aggregation_dropoff") || 0.3;
    } catch {
    }
    if (_dropoff < _dropoffThreshold) {
      _isAggregation = true;
      topN = Math.max(topN, 8);
      console.log(`[activation-field] aggregation detected: dropoff=${_dropoff.toFixed(3)} < ${_dropoffThreshold}, topN ${_originalTopN}\u2192${topN}`);
    }
  }
  if (recencyBias !== 0 && results.length > 0) {
    const now = Date.now();
    const scored = results.map((r) => {
      const ageDays = (now - (r.memory.ts || now)) / 864e5;
      let boost = 1;
      if (recencyBias > 0 && ageDays <= recencyBias) boost = 1.5;
      if (recencyBias < 0 && ageDays > 30) boost = 1.3;
      return { ...r, _recencyScore: r.activation * boost };
    });
    scored.sort((a, b) => b._recencyScore - a._recencyScore);
    results = scored.map(({ _recencyScore, ...r }) => r);
  }
  if (_currentQueryType === "temporal" && results.length > 1) {
    const DATE_PATTERN = /\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b|\b\d{4}\b|\b\d{1,2}\s+\w+\s+\d{4}\b/i;
    for (const r of results) {
      if (DATE_PATTERN.test(r.memory.content || "")) {
        r.activation *= 1.15;
      }
    }
    results.sort((a, b) => b.activation - a.activation);
  }
  const _prfThreshold = results.length >= topN ? 0.15 : 0.03;
  if (results.length > 0 && results[0].activation < _prfThreshold) {
    const prfTopN = Math.min(3, results.length);
    const prfKeywords = /* @__PURE__ */ new Map();
    for (let i = 0; i < prfTopN; i++) {
      const content = results[i].memory.content || "";
      const words = content.match(WORD_PATTERN.CJK24_EN3) || [];
      for (const w of words) {
        const wl = w.toLowerCase();
        if (EN_STOP_WORDS.has(wl)) continue;
        const idf = _idfCache?.get(wl) ?? 0.5;
        prfKeywords.set(wl, Math.max(prfKeywords.get(wl) || 0, idf));
      }
    }
    const sortedPrfWords = [...prfKeywords.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5);
    let prfAdded = 0;
    for (const [word, idf] of sortedPrfWords) {
      if (!expanded.has(word)) {
        expanded.set(word, idf * 0.5);
        prfAdded++;
      }
    }
    if (prfAdded > 0) {
      const prfResults = computeActivationField(memories, lexicalQuery, mood, alertness, expanded, topN * 2, timeRange, cogHints);
      const seen = new Set(results.map((r) => r.memory.content));
      for (const r of prfResults) {
        if (!seen.has(r.memory.content)) {
          results.push(r);
          seen.add(r.memory.content);
        }
      }
      results.sort((a, b) => b.activation - a.activation);
      console.log(`[activation-field] PRF: +${prfAdded} keywords, ${prfResults.length} second-pass \u2192 ${results.length} merged`);
    }
  }
  try {
    if (_primingCacheRef && _primingCacheRef.size > 0) {
      const now = Date.now();
      const PRIMING_WINDOW = 5 * 60 * 1e3;
      for (const r of results) {
        const words = r.memory.content.match(WORD_PATTERN.CJK2_EN3) || [];
        let hits = 0;
        for (const w of words) {
          const ts = _primingCacheRef.get(w.toLowerCase());
          if (ts && now - ts < PRIMING_WINDOW) hits++;
        }
        if (hits > 0 && words.length > 0) {
          const boost = Math.min(0.3, hits / words.length);
          r.activation *= 1 + boost;
          try {
            require("./decision-log.ts").logDecision("priming", (r.memory.content || "").slice(0, 30), `hits=${hits}/${words.length}, boost=${boost.toFixed(2)}`);
          } catch {
          }
        }
      }
      results.sort((a, b) => b.activation - a.activation);
    }
  } catch {
  }
  try {
    if (_predictivePrimingRef && _predictivePrimingRef.size > 0) {
      const now = Date.now();
      const PP_WINDOW = 5 * 60 * 1e3;
      let ppHits = 0;
      for (const r of results) {
        const cached = _predictivePrimingRef.get(r.memory.content);
        if (cached && now - cached.primedAt < PP_WINDOW) {
          const boost = Math.min(0.25, cached.predictedRelevance * 0.5);
          r.activation *= 1 + boost;
          ppHits++;
          try {
            require("./decision-log.ts").logDecision("predictive_priming_hit", (r.memory.content || "").slice(0, 30), `relevance=${cached.predictedRelevance.toFixed(2)}, boost=${boost.toFixed(2)}, age=${((now - cached.primedAt) / 1e3).toFixed(0)}s`);
          } catch {
          }
        }
      }
      if (ppHits > 0) results.sort((a, b) => b.activation - a.activation);
    }
  } catch {
  }
  const queryLower = lexicalQuery.toLowerCase();
  const SCOPE_KW = {
    correction: ["\u7EA0\u6B63", "\u9519\u4E86", "\u4E0D\u5BF9", "correct", "fix"],
    preference: ["\u559C\u6B22", "\u504F\u597D", "prefer", "like"],
    fact: ["\u4E8B\u5B9E", "\u77E5\u9053", "\u8BB0\u4F4F", "fact", "know"],
    event: ["\u53D1\u751F", "\u7ECF\u5386", "event", "happen"]
  };
  const EMO_KW = {
    warm: ["\u5F00\u5FC3", "\u9AD8\u5174", "\u5FEB\u4E50", "happy"],
    painful: ["\u96BE\u8FC7", "\u4F24\u5FC3", "\u75DB\u82E6", "sad"],
    important: ["\u91CD\u8981", "\u5173\u952E", "important"],
    funny: ["\u641E\u7B11", "\u597D\u7B11", "\u54C8\u54C8", "funny"]
  };
  for (let i = 0; i < Math.min(50, results.length); i++) {
    const m = results[i].memory;
    let bonus = 0;
    if (m.tags?.length) {
      bonus += m.tags.filter((t) => queryLower.includes(t.toLowerCase())).length / m.tags.length * 3;
    }
    const sk = SCOPE_KW[m.scope || ""];
    if (sk?.some((k) => queryLower.includes(k))) bonus += 1.5;
    const ek = EMO_KW[m.emotion || ""];
    if (ek?.some((k) => queryLower.includes(k))) bonus += 2;
    if (_isNegationQuery) {
      if (m.scope === "correction") bonus += 2;
      if (m.emotion === "painful") bonus += 2;
    }
    if (m.tags?.includes("summary") || m.scope === "fact") bonus += 2.5;
    if (m.tags?.length) {
      const speakerMatch = /speaker\s*1|speaker\s*2|user|assistant/i.exec(queryLower);
      if (speakerMatch) {
        const targetRole = /speaker\s*1|user/i.test(speakerMatch[0]) ? "user" : "assistant";
        if (m.tags.some((t) => t === `speaker:${targetRole}`)) bonus += 2;
      }
    }
    if (_queryNames && _queryNames.length > 0) {
      const ml = (m.content || "").toLowerCase();
      for (const name of _queryNames) {
        if (ml.includes(name)) {
          bonus += 2.5;
          break;
        }
      }
    }
    results[i].activation *= 1 + Math.min(0.3, bonus / 6.5);
  }
  results.sort((a, b) => b.activation - a.activation);
  if (_parallelFactMems.length > 0) {
    const seenContent = new Set(results.map((r) => r.memory.content));
    const factResults = [];
    const namTopActivation = results.length > 0 ? results[0].activation : 0.5;
    for (const fm of _parallelFactMems) {
      if (seenContent.has(fm.content)) continue;
      const factObj = fm.content.replace(/^\[事实\]\s*\S+:\s*/, "");
      const hasSimilar = results.some((r) => r.memory.content.includes(factObj) && factObj.length >= 2);
      if (hasSimilar) continue;
      const ms = fm._matchScore || 3;
      const factActivation = namTopActivation * Math.min(1, ms / 6);
      factResults.push({
        memory: fm,
        activation: factActivation,
        signals: { base: 0, context: 1, emotion: 0, spread: 0, interference: 1, temporal: 0 }
      });
      seenContent.add(fm.content);
    }
    if (factResults.length > 0) {
      results = [...results, ...factResults];
      results.sort((a, b) => b.activation - a.activation);
      console.log(`[activation-field] fusion: ${factResults.length} facts merged into ${results.length} total results`);
    }
  }
  try {
    const entities = _graphMod.findMentionedEntities(lexicalQuery);
    if (entities.length > 0) {
      const graphResults = _graphMod.graphWalkRecallScored(entities, memories, 2, topN);
      if (graphResults.length > 0) {
        const seenContent = new Set(results.map((r) => r.memory.content));
        const namTopActivation = results.length > 0 ? results[0].activation : 0.5;
        const maxGraphScore = graphResults[0].graphScore || 1;
        let graphAdded = 0;
        for (const gr of graphResults) {
          if (seenContent.has(gr.content)) continue;
          const mem = memories.find((m) => m.content === gr.content);
          if (!mem) continue;
          const graphActivation = namTopActivation * Math.min(1, gr.graphScore / maxGraphScore) * 0.8;
          results.push({ memory: mem, activation: graphActivation, signals: { base: 0, context: 0, emotion: 0, spread: 1, interference: 1, temporal: 0 } });
          seenContent.add(gr.content);
          graphAdded++;
        }
        if (graphAdded > 0) {
          results.sort((a, b) => b.activation - a.activation);
          console.log(`[activation-field] graph-fusion: ${graphAdded} graph memories merged (entities: ${entities.slice(0, 3).join(",")})`);
        }
      }
    }
  } catch {
  }
  if (results.length > topN && !_isAggregation) {
    const mmrResults = [];
    const remaining = [...results];
    const LAMBDA = 0.7;
    while (mmrResults.length < topN && remaining.length > 0) {
      let bestIdx = 0;
      let bestScore = -Infinity;
      for (let i = 0; i < remaining.length; i++) {
        const relevance = remaining[i].activation;
        let maxSim = 0;
        for (const selected of mmrResults) {
          const sim = trigramSimilarity(
            trigrams(remaining[i].memory.content || ""),
            trigrams(selected.memory.content || "")
          );
          if (sim > maxSim) maxSim = sim;
        }
        const mmrScore = LAMBDA * relevance - (1 - LAMBDA) * maxSim;
        if (mmrScore > bestScore) {
          bestScore = mmrScore;
          bestIdx = i;
        }
      }
      mmrResults.push(remaining[bestIdx]);
      remaining.splice(bestIdx, 1);
    }
    results = mmrResults;
  }
  if (results.length >= 4) {
    const getSegment = (mem) => {
      if (mem.segmentId !== void 0 && mem.segmentId > 0) return `seg:${mem.segmentId}`;
      if (mem.tags?.length) {
        const st = mem.tags.find((t) => /^session:/.test(t));
        if (st) return st;
      }
      return null;
    };
    const topSlice = results.slice(0, Math.min(topN * 2, results.length));
    const segCounts = /* @__PURE__ */ new Map();
    for (const r of topSlice) {
      const seg = getSegment(r.memory);
      if (seg) segCounts.set(seg, (segCounts.get(seg) || 0) + 1);
    }
    let boosted = 0;
    for (const r of results) {
      const seg = getSegment(r.memory);
      if (seg) {
        const count = segCounts.get(seg) || 0;
        if (count >= 2) {
          r.activation *= 1 + Math.min(0.15, (count - 1) * 0.05);
          boosted++;
        }
      }
    }
    if (boosted > 0) {
      results.sort((a, b) => b.activation - a.activation);
      console.log(`[activation-field] segment-cohesion: boosted ${boosted} memories across ${[...segCounts.values()].filter((v) => v >= 2).length} segments`);
    }
  }
  if (_queryNames && _queryNames.length >= 2 && results.length > topN) {
    const constraints = /* @__PURE__ */ new Set();
    for (const n of _queryNames) constraints.add("entity:" + n);
    const contentWords = (lexicalQuery.match(/[a-z]{4,}/gi) || []).filter((w) => !EN_STOP_WORDS.has(w.toLowerCase())).slice(0, 6);
    for (const w of contentWords) constraints.add("kw:" + w.toLowerCase());
    const pool = results.slice(0, topN * 2);
    const selected = [];
    const uncovered = new Set(constraints);
    while (selected.length < topN && pool.length > 0) {
      let bestIdx = 0, bestScore = -1;
      for (let i = 0; i < pool.length; i++) {
        const ml2 = pool[i].memory.content.toLowerCase();
        let gain = 0;
        for (const c of uncovered) {
          if (ml2.includes(c.split(":")[1])) gain++;
        }
        const rankScore = 1 / (1 + i);
        const combined = 0.6 * rankScore + 0.4 * (gain / Math.max(constraints.size, 1));
        if (combined > bestScore) {
          bestScore = combined;
          bestIdx = i;
        }
      }
      const picked = pool.splice(bestIdx, 1)[0];
      selected.push(picked);
      const ml = picked.memory.content.toLowerCase();
      for (const c of [...uncovered]) {
        if (ml.includes(c.split(":")[1])) uncovered.delete(c);
      }
    }
    results = selected;
  }
  if (results.length > topN && topN >= 6) {
    const seen = /* @__PURE__ */ new Set();
    const coordinated = [];
    for (const r of results) {
      if (coordinated.length >= Math.ceil(topN * 0.5)) break;
      if (!seen.has(r.memory.content)) {
        coordinated.push(r);
        seen.add(r.memory.content);
      }
    }
    const byContext = [...results].sort((a, b) => b.signals.context - a.signals.context);
    for (const r of byContext) {
      if (coordinated.length >= Math.ceil(topN * 0.7)) break;
      if (!seen.has(r.memory.content)) {
        coordinated.push(r);
        seen.add(r.memory.content);
      }
    }
    const byBase = [...results].sort((a, b) => b.signals.base - a.signals.base);
    for (const r of byBase) {
      if (coordinated.length >= Math.ceil(topN * 0.9)) break;
      if (!seen.has(r.memory.content)) {
        coordinated.push(r);
        seen.add(r.memory.content);
      }
    }
    if (_currentQueryType === "temporal") {
      const byTemporal = [...results].sort((a, b) => b.signals.temporal - a.signals.temporal);
      for (const r of byTemporal) {
        if (coordinated.length >= topN - 1) break;
        if (!seen.has(r.memory.content) && r.signals.temporal > 0) {
          coordinated.push(r);
          seen.add(r.memory.content);
        }
      }
    }
    const bySpread = [...results].sort((a, b) => b.signals.spread - a.signals.spread);
    for (const r of bySpread) {
      if (coordinated.length >= topN - 1) break;
      if (!seen.has(r.memory.content) && r.signals.spread > 0) {
        coordinated.push(r);
        seen.add(r.memory.content);
      }
    }
    const episodeOnly = results.filter((r) => r.memory.scope === "episode" && !r.memory.tags?.includes("summary")).sort((a, b) => b.activation - a.activation);
    for (const r of episodeOnly) {
      if (coordinated.length >= topN) break;
      if (!seen.has(r.memory.content)) {
        coordinated.push(r);
        seen.add(r.memory.content);
      }
    }
    for (const r of results) {
      if (coordinated.length >= topN) break;
      if (!seen.has(r.memory.content)) {
        coordinated.push(r);
        seen.add(r.memory.content);
      }
    }
    coordinated.sort((a, b) => b.activation - a.activation);
    results = coordinated;
  }
  if (_currentQueryType === "multi_entity" && !_twoPassInProgress && _queryNames && _queryNames.length >= 2) {
    try {
      const top5 = results.slice(0, 5);
      const topTokens = /* @__PURE__ */ new Map();
      for (const r of top5) {
        for (const t of (r.memory.content || "").toLowerCase().match(WORD_PATTERN.CJK2_EN3) || []) {
          if (!EN_STOP_WORDS.has(t)) topTokens.set(t, (topTokens.get(t) || 0) + 1);
        }
      }
      const bridgeTokens = [...topTokens.entries()].filter(([t, freq]) => freq >= 2 && !expanded.has(t) && (_idfCache?.get(t) ?? 0.5) > 0.3).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([t]) => t);
      if (bridgeTokens.length >= 1) {
        _twoPassInProgress = true;
        const seen = new Set(results.map((r) => r.memory.content));
        let p2Added = 0;
        for (const entity of _queryNames.slice(0, 2)) {
          const p2Query = entity + " " + bridgeTokens.join(" ");
          const p2Res = computeActivationField(memories, p2Query, mood, alertness, expanded, topN, timeRange, cogHints);
          for (const r of p2Res.slice(0, 3)) {
            if (!seen.has(r.memory.content)) {
              r.activation *= 0.6;
              results.push(r);
              seen.add(r.memory.content);
              p2Added++;
            }
          }
        }
        if (p2Added > 0) {
          results.sort((a, b) => b.activation - a.activation);
          console.log(`[activation-field] dispatch:multi_entity iterative recall +${p2Added} results`);
        }
        _twoPassInProgress = false;
      }
    } catch {
      _twoPassInProgress = false;
    }
  }
  if (_currentQueryType === "temporal") {
    const DATE_PATTERN = /\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b|\b\d{4}\b|\b\d{1,2}\s+\w+\s+\d{4}\b/i;
    for (const r of results) {
      if (DATE_PATTERN.test(r.memory.content || "")) r.activation *= 1.05;
    }
    results.sort((a, b) => b.activation - a.activation);
  }
  const topResults = results.slice(0, topN);
  if (topResults.length > 0) {
    console.log(`[activation-field] cascade: ${expanded.size} expanded words \u2192 ${results.length} candidates \u2192 ${topResults.length} selected`);
  }
  try {
    _aamLearn(query, Math.abs(mood));
    _aamLearnTemporalLink(query);
  } catch {
  }
  if (!process.env.CC_SOUL_BENCHMARK && (topResults.length === 0 || topResults.length > 0 && topResults[0].activation < 0.1)) {
    try {
      const { hasLLM } = require("./cli.ts");
      if (hasLLM()) {
        const { spawnCLI } = require("./cli.ts");
        spawnCLI(
          `\u7528\u6237\u95EE\u4E86"${query.slice(0, 100)}"\uFF0C\u8BF7\u5217\u51FA3-5\u4E2A\u76F8\u5173\u7684\u5173\u952E\u8BCD\u6216\u540C\u4E49\u8BCD\uFF0C\u6BCF\u884C\u4E00\u4E2A\uFF0C\u53EA\u8F93\u51FA\u5173\u952E\u8BCD\u4E0D\u8981\u89E3\u91CA`,
          (output) => {
            if (!output) return;
            const keywords = output.split("\n").map((l) => l.trim()).filter((l) => l.length >= 2 && l.length <= 20);
            try {
              const aam = require("./aam.ts");
              const queryWords = query.match(WORD_PATTERN.CJK2_EN3) || [];
              for (const kw of keywords) {
                for (const qw of queryWords) {
                  aam.learnAssociation?.(qw + " " + kw);
                }
              }
            } catch {
            }
            try {
              require("./decision-log.ts").logDecision("system2_escalation", query.slice(0, 30), `expanded: ${keywords.join(",")}`);
            } catch {
            }
          },
          1e4
          // 10s timeout, low priority
        );
      }
    } catch {
    }
  }
  return topResults.map((r) => r.memory);
}
function activationRecallWithScores(memories, query, topK, mood, alertness, cogHints) {
  const expandedWords = (() => {
    try {
      const aam = require("./aam.ts");
      const words = query.toLowerCase().match(/[a-z]{2,}/gi) || [];
      return aam.expandQuery?.(words.slice(0, 5).map((w) => w.toLowerCase()), 10) || /* @__PURE__ */ new Map();
    } catch {
      return /* @__PURE__ */ new Map();
    }
  })();
  const results = computeActivationField(memories, query, mood, alertness, expandedWords, topK * 3, null, cogHints);
  return results.slice(0, topK).map((r) => ({ memory: r.memory, activation: r.activation }));
}
function getIdfCache() {
  return _idfCache;
}
function explainActivation(result) {
  const s = result.signals;
  const parts = [
    `base=${s.base.toFixed(2)}`,
    `ctx=${s.context.toFixed(2)}`,
    `emo=${s.emotion.toFixed(2)}`,
    `spread=${s.spread.toFixed(2)}`,
    `inhib=${s.interference.toFixed(2)}`,
    `time=${s.temporal.toFixed(2)}`
  ];
  return `activation=${result.activation.toFixed(3)} [${parts.join(" ")}]`;
}
function getFieldStats() {
  const values = [..._activations.values()];
  return {
    totalActivated: values.filter((v) => v > 0.05).length,
    avgActivation: values.length > 0 ? values.reduce((s, v) => s + v, 0) / values.length : 0
  };
}
export {
  activationRecall,
  activationRecallWithScores,
  computeActivationField,
  decayAllActivations,
  expandQueryForField,
  explainActivation,
  getFieldStats,
  getIdfCache,
  getMomentumBoost,
  getRecentTrace,
  getSignalWeights,
  invalidateFieldIDF,
  recordRecallEngagement
};
